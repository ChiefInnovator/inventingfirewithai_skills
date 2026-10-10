#!/usr/bin/env python3
"""Independently implemented Figma JSON → Flutter draft compiler.

Reads REST node JSON enriched with Plugin API styledTextSegments/asset paths.
Never fetches Figma, guesses application behavior, or overwrites canonical code.
"""
import argparse
import copy
import json
import math
from pathlib import Path
import re



def number(value):
    value = float(value)
    if not math.isfinite(value):
        raise ValueError('Non-finite design measurement')
    return format(value, '.6f').rstrip('0').rstrip('.') or '0'


def quote(value):
    return json.dumps(str(value), ensure_ascii=False).replace('$', r'\$')


def call(kind, **props):
    return kind + '(' + ', '.join(f'{k}: {v}' for k, v in props.items() if v is not None) + ')'


def sequence(values):
    return '[' + ', '.join(values) + ']'


class Compiler:
    def __init__(self, file_key, assets=None, variables=None):
        self.file_key = file_key
        self.assets = assets or {}
        self.variables = variables or {}
        self.colors = {}
        self.warnings = []
        self.trace = []
        self.uses_svg = False
        self.uses_blur = False
        self.uses_gradient_stroke = False
        self.fonts = set()
        self.font_weights = {}
        self.font_styles = {}

    def warn(self, node, message, reason='no-rule'):
        entry = {'nodeId': node.get('id'), 'reason': reason, 'message': message}
        if entry not in self.warnings:
            self.warnings.append(entry)

    def supports_gradient_stroke(self, node, paint):
        transform = paint.get('gradientTransform')
        stops = paint.get('gradientStops', [])
        finite = lambda v: type(v) in (int, float) and math.isfinite(v)
        return (paint.get('type') == 'GRADIENT_LINEAR'
                and node['type'] in ('FRAME', 'INSTANCE', 'COMPONENT', 'RECTANGLE')
                and not node.get('individualStrokeWeights') and not node.get('dashPattern')
                and node.get('strokeAlign', 'INSIDE') in ('INSIDE', 'CENTER', 'OUTSIDE')
                and isinstance(transform, list) and len(transform) == 2
                and all(isinstance(row, list) and len(row) == 3 for row in transform)
                and all(finite(v) for row in transform for v in row)
                and math.hypot(*transform[0][:2]) > 0
                and isinstance(stops, list) and len(stops) >= 2
                and all(isinstance(stop, dict) and finite(stop.get('position'))
                        and 0 <= stop['position'] <= 1
                        and isinstance(stop.get('color'), dict)
                        and all(finite(stop['color'].get(c, 1 if c == 'a' else None))
                                for c in ('r', 'g', 'b', 'a')) for stop in stops)
                and all(a['position'] <= b['position'] for a, b in zip(stops, stops[1:]))
                and finite(node.get('strokeWeight', 1)) and node.get('strokeWeight', 1) > 0)

    def normalize(self, original, parent=None):
        node = copy.deepcopy(original)
        if not isinstance(node, dict) or not node.get('id'):
            raise ValueError('Every node needs its original Figma id')
        if not re.fullmatch(r'[A-Za-z0-9_:;.-]+', node['id']):
            raise ValueError('Invalid Figma node id')
        if node.get('visible', True) is False:
            return None
        bounds = node.get('absoluteBoundingBox', {})
        local_size = node.get('size', {})
        node['width'] = node.get('width', local_size.get('x', bounds.get('width', 0)))
        node['height'] = node.get('height', local_size.get('y', bounds.get('height', 0)))
        for dimension in ('width', 'height'):
            if node[dimension] < 0:
                self.warn(node, f'Negative {dimension}; clamped to zero')
                node[dimension] = 0
        parent_bounds = (parent or {}).get('absoluteBoundingBox', {})
        for axis in ('x', 'y'):
            node[axis] = node.get(axis, bounds.get(axis, 0) - parent_bounds.get(axis, 0))
        if parent is None:
            node['x'] = node['y'] = 0
        node['layoutMode'] = node.get('layoutMode', 'NONE')
        # Retain groups: their opacity, masks, clipping and coordinates matter.
        node['children'] = [child for item in node.get('children', [])
                            if (child := self.normalize(item, node)) is not None]
        if node.get('rotation') and not node.get('relativeTransform'):
            self.warn(node, 'Rotated bounding boxes need a relativeTransform or original local size')
        transform = node.get('relativeTransform')
        if transform and (transform[0][:2], transform[1][:2]) != ([1, 0], [0, 1]) and not (
                ('width' in original and 'height' in original) or ('x' in local_size and 'y' in local_size)):
            self.warn(node, 'Transform supplied without original local size; bounding-box dimensions are approximate')
        return node

    def color(self, paint, node):
        rgb = paint.get('color', {})
        alias = paint.get('boundVariables', {}).get('color', {})
        variable = paint.get('variableColorName') or alias.get('name') or self.variables.get(alias.get('id'))
        alpha = rgb.get('a', 1) * paint.get('opacity', 1)
        channels = [alpha, rgb.get('r', 0), rgb.get('g', 0), rgb.get('b', 0)]
        rgba = ''.join(f'{max(0, min(255, math.floor(c * 255 + .5))):02X}' for c in channels)
        key = 'color' + rgba
        self.colors[key] = rgba
        if variable:
            self.warn(node, f'Bound variable {variable}: retained captured #{rgba}; map to verified project tokens during adoption', 'unlinked-colour')
        return 'DraftTokens.' + key

    def paints(self, node, field='fills'):
        paints = [p for p in node.get(field, []) if p.get('visible', True)]
        if len(paints) > 1:
            self.warn(node, f'Multiple {field} need explicit compositing; using the last visible paint')
        return paints[-1] if paints else None

    def gradient(self, paint, node):
        stops = paint.get('gradientStops', [])
        if len(stops) < 2:
            self.warn(node, 'Gradient has fewer than two stops')
            return None
        colors = sequence([self.color({'color': stop['color'], 'opacity': paint.get('opacity', 1),
                                       'boundVariables': stop.get('boundVariables', {})}, node) for stop in stops])
        positions = sequence([number(stop['position']) for stop in stops])
        handles = paint.get('gradientHandlePositions')
        if not handles:
            self.warn(node, 'Gradient transform needs resolved normalized handle positions')
            return None
        alignment = lambda p: f'Alignment({number(p["x"] * 2 - 1)}, {number(p["y"] * 2 - 1)})'
        props = {'colors': colors, 'stops': positions}
        kind = paint['type']
        if kind == 'GRADIENT_LINEAR':
            return call('LinearGradient', begin=alignment(handles[0]), end=alignment(handles[1]), **props)
        if kind == 'GRADIENT_RADIAL':
            center, edge = handles[:2]
            shortest = max(.000001, min(node['width'], node['height']))
            radius = math.hypot((edge['x'] - center['x']) * node['width'],
                                (edge['y'] - center['y']) * node['height']) / shortest
            if len(handles) > 2:
                other = math.hypot((handles[2]['x'] - center['x']) * node['width'],
                                  (handles[2]['y'] - center['y']) * node['height']) / shortest
                if not math.isclose(radius, other, abs_tol=1e-5):
                    self.warn(node, 'Elliptical radial gradient requires a shader or exported asset')
            return call('RadialGradient', center=alignment(center), radius=number(max(radius, .000001)), **props)
        if kind == 'GRADIENT_ANGULAR':
            self.warn(node, 'Angular gradient direction requires visual comparison')
            return call('SweepGradient', center=alignment(handles[0]), **props)
        self.warn(node, f'Unsupported gradient: {kind}')
        return None

    def asset(self, node, paint=None):
        path = self.assets.get(node['id']) or self.assets.get((paint or {}).get('imageRef')) or self.assets.get((paint or {}).get('imageHash'))
        if not path:
            self.warn(node, 'Missing local asset; visible placeholder retained')
            return 'const Placeholder()'
        if Path(path).is_absolute() or '..' in Path(path).parts or re.match(r'\w+://', path):
            raise ValueError(f'Asset must be a bundled relative path: {path}')
        fit = {'FILL': 'cover', 'FIT': 'contain', 'STRETCH': 'fill', 'CROP': 'cover'}.get((paint or {}).get('scaleMode'), 'fill')
        if (paint or {}).get('imageTransform') or (paint or {}).get('scaleMode') == 'TILE':
            self.warn(node, 'Image crop/tiling transform requires explicit reproduction')
        if path.lower().endswith('.svg'):
            self.uses_svg = True
            return f'SvgPicture.asset({quote(path)}, fit: BoxFit.{fit})'
        return f'Image.asset({quote(path)}, fit: BoxFit.{fit})'

    def radius(self, node):
        radii = node.get('rectangleCornerRadii')
        if radii:
            return call('BorderRadius.only', **{corner: f'Radius.circular({number(max(0, value))})'
                        for corner, value in zip(('topLeft', 'topRight', 'bottomRight', 'bottomLeft'), radii)})
        if any(key in node for key in ('topLeftRadius', 'topRightRadius', 'bottomLeftRadius', 'bottomRightRadius')):
            return call('BorderRadius.only', **{corner: f'Radius.circular({number(max(0, node.get(corner + "Radius", 0)))})'
                        for corner in ('topLeft', 'topRight', 'bottomLeft', 'bottomRight')})
        radius = node.get('cornerRadius', 0)
        return f'BorderRadius.circular({number(max(0, radius))})' if isinstance(radius, (int, float)) and radius else None

    def decoration(self, node):
        props = {}
        paint = self.paints(node)
        if paint:
            if paint['type'] == 'SOLID':
                props['color'] = self.color(paint, node)
            elif paint['type'].startswith('GRADIENT_'):
                props['gradient'] = self.gradient(paint, node)
            elif paint['type'] != 'IMAGE':
                self.warn(node, f'Unsupported paint: {paint["type"]}')
        border = self.paints(node, 'strokes')
        if border:
            if border.get('type') != 'SOLID':
                if not self.supports_gradient_stroke(node, border):
                    self.warn(node, 'Unsupported non-solid stroke requires a painter or exported asset')
            else:
                color = self.color(border, node)
                align = {'INSIDE': 'Inside', 'CENTER': 'Center', 'OUTSIDE': 'Outside'}.get(node.get('strokeAlign'), 'Inside')
                weights = node.get('individualStrokeWeights')
                if weights:
                    props['border'] = call('Border', **{side: call('BorderSide', color=color,
                        width=number(weights.get(side, 0)), strokeAlign='BorderSide.strokeAlign' + align)
                        for side in ('top', 'right', 'bottom', 'left')})
                else:
                    props['border'] = call('Border.all', color=color, width=number(node.get('strokeWeight', 1)),
                                           strokeAlign='BorderSide.strokeAlign' + align)
        if node['type'] == 'ELLIPSE':
            props['shape'] = 'BoxShape.circle'
            if node['width'] != node['height']:
                self.warn(node, 'Non-circular ellipse needs an oval clip or exported SVG')
        else:
            props['borderRadius'] = self.radius(node)
        shadows = []
        for effect in node.get('effects', []):
            if not effect.get('visible', True):
                continue
            if effect['type'] == 'DROP_SHADOW':
                offset = effect.get('offset', {})
                shadows.append(call('BoxShadow', color=self.color({'color': effect['color']}, node),
                    offset=f'Offset({number(offset.get("x", 0))}, {number(offset.get("y", 0))})',
                    blurRadius=number(effect.get('radius', 0)), spreadRadius=number(effect.get('spread', 0))))
            elif effect['type'] not in ('LAYER_BLUR', 'BACKGROUND_BLUR'):
                self.warn(node, f'Unsupported effect: {effect["type"]}')
        if shadows:
            props['boxShadow'] = sequence(shadows)
        return call('BoxDecoration', **props)

    def line_ratio(self, style, node):
        """Line height ÷ font size; AUTO (normal) single-line text uses the measured box (mapping.md rule b)."""
        size = style.get('fontSize', 14)
        line = style.get('lineHeight', {})
        if size <= 0:
            return None
        if line.get('unit') == 'PIXELS':
            return line['value'] / size
        if line.get('unit') == 'PERCENT':
            return line['value'] / 100
        if style.get('lineHeightPx'):
            return style['lineHeightPx'] / size
        # Only a content-sized box is the line box: a fixed (NONE/TRUNCATE) box can
        # hold spare space that textAlignVertical distributes.
        characters = node.get('characters', '')
        if line.get('unit') == 'AUTO' and node.get('textAutoResize') in ('WIDTH_AND_HEIGHT', 'HEIGHT') \
                and '\n' not in characters and '\u2028' not in characters \
                and 0 < node.get('height', 0) < 2 * size:
            return node['height'] / size
        return None

    @staticmethod
    def flutter_family(style):
        # Preserve the captured family; project-specific registrations are an adoption concern.
        return style.get('fontFamily') or style.get('fontName', {}).get('family')

    def text_style(self, style, node):
        size = style.get('fontSize', 14)
        source_family = style.get('fontFamily') or style.get('fontName', {}).get('family')
        variations = style.get('fontName', {}).get('variationSettings', {})
        family = self.flutter_family(style)
        if source_family:
            self.fonts.add(source_family)
        else:
            self.warn(node, 'Font family unresolved; theme fallback is draft-only and cannot pass visual approval', 'missing-font')
        props = {'fontSize': number(size), 'fontFamily': quote(family) if family else 'Theme.of(context).textTheme.bodyMedium?.fontFamily'}
        weight = variations.get('wght', style.get('fontWeight'))
        if weight is None:
            # Plugin text segments supply fontName.style, not REST fontWeight.
            name = re.sub(r'[\s_-]', '', style.get('fontName', {}).get('style', '').lower()).replace('italic', '')
            weight = {'thin': 100, 'extralight': 200, 'ultralight': 200, 'light': 300,
                      'regular': 400, 'normal': 400, 'book': 400, 'medium': 500,
                      'semibold': 600, 'demibold': 600, 'bold': 700, 'extrabold': 800,
                      'ultrabold': 800, 'black': 900, 'heavy': 900}.get(name, 400)
            if name and name not in {'thin', 'extralight', 'ultralight', 'light', 'regular',
                    'normal', 'book', 'medium', 'semibold', 'demibold', 'bold', 'extrabold',
                    'ultrabold', 'black', 'heavy'}:
                self.warn(node, 'Font style weight unresolved: ' + name, 'missing-font')
        if source_family:
            self.font_weights.setdefault(source_family, set()).add(weight)
            self.font_styles.setdefault(source_family, set()).add((weight, bool(
                'italic' in style.get('fontName', {}).get('style', '').lower() or style.get('italic'))))
        if variations:
            props['fontVariations'] = sequence(
                f'FontVariation({quote(axis)}, {number(value)})'
                for axis, value in sorted(variations.items()))
        features = style.get('openTypeFeatures', {})
        if not isinstance(features, dict):
            self.warn(node, 'Mixed OpenType features require resolved text segments')
        elif features:
            enabled = []
            for tag, value in features.items():
                if not isinstance(tag, str) or not re.fullmatch(r'[A-Za-z0-9]{4}', tag) or not isinstance(value, bool):
                    self.warn(node, 'Invalid OpenType feature; expected a four-character tag and boolean')
                    continue
                enabled.append((tag.lower(), value))
            if enabled:
                props['fontFeatures'] = sequence(
                    f'FontFeature({quote(tag)}, {int(value)})'
                    for tag, value in sorted(enabled))
        if weight % 100 and 'wght' not in variations:
            self.warn(node, f'Weight {weight} requires captured variable-font axis support; rounded draft weight cannot pass visual approval', 'missing-font')
        if 'wght' not in variations:
            # A variable run carries its weight only in the wght axis (preserve captured variation axes).
            props['fontWeight'] = f'FontWeight.w{max(100, min(900, round(weight / 100) * 100))}'
        if 'italic' in style.get('fontName', {}).get('style', '').lower() or style.get('italic'):
            props['fontStyle'] = 'FontStyle.italic'
        ratio = self.line_ratio(style, node)
        if ratio is not None:
            props['height'] = number(ratio)
        spacing = style.get('letterSpacing', 0)
        if isinstance(spacing, dict):
            spacing = spacing.get('value', 0) * (size / 100 if spacing.get('unit') == 'PERCENT' else 1)
        props['letterSpacing'] = number(spacing)
        decoration = {'UNDERLINE': 'underline', 'STRIKETHROUGH': 'lineThrough'}.get(style.get('textDecoration'))
        if decoration:
            props['decoration'] = 'TextDecoration.' + decoration
        paints = [p for p in style.get('fills', []) if p.get('visible', True)]
        if paints:
            if paints[-1]['type'] == 'SOLID':
                props['color'] = self.color(paints[-1], node)
            else:
                self.warn(node, 'Gradient text requires ShaderMask or captured asset')
        role = style.get('styleName', '')
        match = re.fullmatch(r'M3/(display|headline|title|body|label)/(small|medium|large)(-emphasized)?', role)
        if match:
            base = 'Theme.of(context).textTheme.' + match[1] + match[2].title() + '!'
            # Role identity is useful, but must not replace resolved visual metrics.
            return call(base + '.copyWith', **props)
        return call('TextStyle', **props)

    def text(self, node):
        if node.get('hasMissingFont') is True:
            self.warn(node, 'Figma reports a missing source font; preserve the declared family and resolve source rendering before visual approval', 'missing-font')
        base = {**node.get('style', {}), **{k: v for k, v in node.items() if k != 'style'}}
        segments = node.get('styledTextSegments')
        if not segments:
            if node.get('characterStyleOverrides') and node.get('styleOverrideTable'):
                # REST stores one style index per character; retain complete runs.
                segments = []
                for i, char in enumerate(node.get('characters', '')):
                    index = node['characterStyleOverrides'][i] if i < len(node['characterStyleOverrides']) else 0
                    style = {**base, **node['styleOverrideTable'].get(str(index), {})}
                    if segments and segments[-1]['styleIndex'] == index:
                        segments[-1]['characters'] += char
                    else:
                        segments.append({**style, 'characters': char, 'styleIndex': index})
            else:
                segments = [base]
        spans = []
        struts = set()
        paragraph_spacing_warned = False
        for segment in segments:
            resolved = {**base, **segment}
            if resolved.get('paragraphSpacing', 0) != 0 and not paragraph_spacing_warned:
                self.warn(node, 'Nonzero source paragraphSpacing requires measured paragraph layout; literal newlines alone do not preserve this metric', 'paragraph-spacing')
                paragraph_spacing_warned = True
            if segment.get('fontName'):
                # A resolved Plugin segment overrides inherited REST defaults.
                resolved['fontFamily'] = segment.get('fontFamily') or segment['fontName'].get('family')
                if 'fontWeight' not in segment:
                    resolved.pop('fontWeight', None)
                resolved['italic'] = segment.get('italic', 'italic' in segment['fontName'].get('style', '').lower())
            value = segment.get('characters', '')
            case = segment.get('textCase')
            value = value.upper() if case == 'UPPER' else value.lower() if case == 'LOWER' else value
            if segment.get('hyperlink') or segment.get('listOptions'):
                self.warn(node, 'Hyperlinks and lists require explicit review')
            spans.append(call('TextSpan', text=quote(value), style=self.text_style(resolved, node)))
            struts.add((self.flutter_family(resolved), resolved.get('fontSize', 14), self.line_ratio(resolved, node)))
        align = {'LEFT': 'left', 'RIGHT': 'right', 'CENTER': 'center', 'JUSTIFIED': 'justify'}.get(base.get('textAlignHorizontal'), 'left')
        strut = None
        if len(struts) == 1:
            family, size, ratio = next(iter(struts))
            if ratio is not None and family:
                # Figma and CSS split leading evenly above and below the glyphs.
                # Use an explicit strut for a consistent measured line box.
                strut = call('StrutStyle', fontFamily=quote(family), fontSize=number(size), height=number(ratio),
                             leadingDistribution='TextLeadingDistribution.even', forceStrutHeight='true')
        elif any(ratio is not None for _, _, ratio in struts):
            self.warn(node, 'Runs with different fonts, sizes or line heights keep per-span height; check the baseline against the source')
        body = 'Text.rich(' + call('TextSpan', children=sequence(spans)) + (', strutStyle: ' + strut if strut else '') + ', textAlign: TextAlign.' + align + ')'
        if (base.get('textTruncation') not in (None, 'DISABLED')
                or base.get('maxLines') or base.get('textAutoResize') == 'TRUNCATE'):
            self.warn(node, 'Text truncation requires captured constraints and explicit review')
        vertical = base.get('textAlignVertical', 'TOP')
        if vertical not in (None, 'TOP'):
            # Only a measured fixed box establishes the spare vertical space.
            # Align loosens height; keep the paragraph's full width so RIGHT,
            # CENTER and JUSTIFIED continue to operate on the source text box.
            bounded = (all(type(node.get(d)) in (int, float)
                           and math.isfinite(node[d]) and node[d] > 0
                           for d in ('width', 'height'))
                       and node.get('layoutSizingHorizontal', 'FIXED') == 'FIXED'
                       and node.get('layoutSizingVertical', 'FIXED') == 'FIXED'
                       and base.get('textAutoResize', 'NONE') == 'NONE')
            if vertical in ('CENTER', 'BOTTOM') and bounded:
                body = call('Align', alignment='Alignment.' +
                            ('centerLeft' if vertical == 'CENTER' else 'bottomLeft'),
                            child=call('SizedBox', width='double.infinity', child=body))
            else:
                self.warn(node, 'Vertical text alignment requires a positive measured fixed text box; hug, fill and auto-resize layouts remain unresolved', 'text-vertical-alignment')
        return body

    def flow(self, node, regular):
        mode = node['layoutMode']
        main = {'MIN': 'start', 'MAX': 'end', 'CENTER': 'center', 'SPACE_BETWEEN': 'spaceBetween'}.get(node.get('primaryAxisAlignItems'), 'start')
        cross = {'MIN': 'start', 'MAX': 'end', 'CENTER': 'center', 'BASELINE': 'baseline'}.get(node.get('counterAxisAlignItems'), 'start')
        gap = node.get('itemSpacing', 0)
        children = [self.emit(child, node) for child in regular]
        if gap < 0 and main != 'spaceBetween' and node.get('layoutWrap') != 'WRAP':
            # Figma's negative gap is CSS mb-/mr-[-n] on every item but the last:
            # the slot shrinks by n and the item paints its full size.
            dimension = 'height' if mode == 'VERTICAL' else 'width'
            fill = 'layoutSizing' + ('Vertical' if mode == 'VERTICAL' else 'Horizontal')
            if all(0 < -gap <= child[dimension] and child.get(fill) != 'FILL' for child in regular[:-1]):
                for i, child in enumerate(regular[:-1]):
                    size = number(child[dimension])
                    factor = f'({size} - {number(-gap)}) / {size}'
                    children[i] = call('Align', alignment='Alignment.topLeft',
                        widthFactor=factor if mode == 'HORIZONTAL' else '1',
                        heightFactor=factor if mode == 'VERTICAL' else '1',
                        child=call('SizedBox', **{dimension: size}, child=children[i]))
            else:
                self.warn(node, 'Negative gap larger than an item, or on a filling item, requires overlapping stack layout')
            gap = 0
        elif gap < 0:
            self.warn(node, 'Negative gap requires overlapping stack layout')
            gap = 0
        if node.get('layoutWrap') == 'WRAP':
            return call('Wrap', direction='Axis.' + ('horizontal' if mode == 'HORIZONTAL' else 'vertical'),
                        alignment='WrapAlignment.' + main, spacing=number(gap),
                        runSpacing=number(max(0, node.get('counterAxisSpacing', 0))), children=sequence(children))
        # Hug the flow content on its own axis. emit() applies explicit FIXED/FILL
        # constraints independently; Expanded in a Row must not make a nested
        # Column consume the field height and strand its label at the top.
        return call('Row' if mode == 'HORIZONTAL' else 'Column', mainAxisSize='MainAxisSize.min',
                    mainAxisAlignment='MainAxisAlignment.' + main, crossAxisAlignment='CrossAxisAlignment.' + cross,
                    textBaseline='TextBaseline.alphabetic' if cross == 'baseline' else None,
                    spacing=number(gap) if main != 'spaceBetween' else None, children=sequence(children))

    def emit(self, node, parent=None, positioned=False):
        kind = node['type']
        if node.get('isMask'):
            self.warn(node, 'Mask geometry requires a clip/painter or exported asset')
        if node.get('arcData'):
            self.warn(node, 'Ellipse arc geometry requires a painter or exported SVG')
        if node.get('blendMode', 'NORMAL') not in ('NORMAL', 'PASS_THROUGH'):
            self.warn(node, 'Blend mode needs an explicit compositing implementation')
        if kind == 'TEXT':
            body = self.text(node)
        elif kind in ('VECTOR', 'BOOLEAN_OPERATION', 'STAR', 'POLYGON', 'LINE'):
            body = self.asset(node)
        elif kind in ('FRAME', 'GROUP', 'INSTANCE', 'COMPONENT', 'COMPONENT_SET', 'SECTION', 'SLOT', 'RECTANGLE', 'ELLIPSE'):
            children = node['children']
            if node.get('itemReverseZIndex'):
                self.warn(node, 'Reverse z-order requires comparison without reversing flow order')
            if node['layoutMode'] in ('HORIZONTAL', 'VERTICAL'):
                regular = [c for c in children if c.get('layoutPositioning') != 'ABSOLUTE']
                overlays = [c for c in children if c.get('layoutPositioning') == 'ABSOLUTE']
                body = self.flow(node, regular)
                pads = [node.get('padding' + side, 0) for side in ('Left', 'Top', 'Right', 'Bottom')]
                if any(pads):
                    body = call('Padding', padding='EdgeInsets.fromLTRB(' + ', '.join(number(p) for p in pads) + ')', child=body)
                if overlays:
                    # Retain Row/Column semantics beneath positioned overlays.
                    body = call('Stack', clipBehavior='Clip.none', children=sequence([body] + [self.emit(c, node, True) for c in overlays]))
            elif children:
                body = call('Stack', clipBehavior='Clip.none', children=sequence([self.emit(c, node, True) for c in children]))
            else:
                body = 'const SizedBox.shrink()'
            paint = self.paints(node)
            if paint and paint['type'] == 'IMAGE':
                body = call('Stack', fit='StackFit.passthrough', children=sequence([
                    call('Positioned.fill', child=self.asset(node, paint)), body]))
            decoration = self.decoration(node)
            if decoration != 'BoxDecoration()':
                body = call('DecoratedBox', decoration=decoration, child=body)
            if node.get('clipsContent'):
                body = call('ClipRRect', borderRadius=self.radius(node), child=body)
        else:
            self.warn(node, f'Unsupported node type: {kind}; placeholder retained')
            body = 'const Placeholder()'

        constraints = {key: number(node[key]) for key in ('minWidth', 'maxWidth', 'minHeight', 'maxHeight') if node.get(key) is not None}
        sizes = {}
        expanded = False
        for axis, dimension in (('Horizontal', 'width'), ('Vertical', 'height')):
            sizing = node.get('layoutSizing' + axis, 'FIXED')
            text_resize = node.get('textAutoResize', 'NONE')
            if kind == 'TEXT' and (text_resize == 'WIDTH_AND_HEIGHT' or (text_resize == 'HEIGHT' and dimension == 'height')):
                sizing = 'HUG'
            if sizing == 'FILL' and not positioned:
                main_axis = (parent or {}).get('layoutMode') == ('HORIZONTAL' if dimension == 'width' else 'VERTICAL')
                parent_hugs = (parent or {}).get('layoutSizing' + axis) == 'HUG'
                if main_axis and not (parent or {}).get('layoutWrap') == 'WRAP' and not parent_hugs:
                    expanded = True
                elif main_axis:
                    self.warn(node, 'Fill in Wrap or a hugging parent uses captured size; Expanded is illegal here')
                    sizes[dimension] = number(node[dimension])
                else:
                    sizes[dimension] = 'double.infinity'
            elif sizing != 'HUG':
                sizes[dimension] = number(node[dimension])
        if sizes:
            body = call('SizedBox', **sizes, child=body)
        if constraints:
            body = call('ConstrainedBox', constraints=call('BoxConstraints', **constraints), child=body)
        for effect in node.get('effects', []):
            if effect.get('visible', True) and effect['type'] in ('LAYER_BLUR', 'BACKGROUND_BLUR'):
                self.uses_blur = True
                radius = number(effect.get('radius', 0))
                body = call('ImageFiltered' if effect['type'] == 'LAYER_BLUR' else 'BackdropFilter',
                            **{'imageFilter' if effect['type'] == 'LAYER_BLUR' else 'filter': f'ImageFilter.blur(sigmaX: {radius}, sigmaY: {radius})'}, child=body)
                if effect['type'] == 'BACKGROUND_BLUR':
                    # Clipping only the child leaves the backdrop effect square.
                    body = (call('ClipOval', child=body) if kind == 'ELLIPSE' else
                            call('ClipRRect', borderRadius=self.radius(node), child=body))
        stroke = self.paints(node, 'strokes')
        if stroke and self.supports_gradient_stroke(node, stroke):
            self.uses_gradient_stroke = True
            row = stroke['gradientTransform'][0]
            colors = sequence([self.color({'color': stop['color'], 'opacity': stroke.get('opacity', 1),
                                           'boundVariables': stop.get('boundVariables', {}),
                                           'variableColorName': stop.get('variableColorName')}, node)
                               for stop in stroke['gradientStops']])
            stops = sequence([number(stop['position']) for stop in stroke['gradientStops']])
            painter = call('DraftGradientStroke', a=number(row[0]), b=number(row[1]), offset=number(row[2]),
                           colors=colors, stops=stops, radius=self.radius(node) or 'BorderRadius.zero',
                           width=number(node.get('strokeWeight', 1)),
                           align=number({'INSIDE': -1, 'CENTER': 0, 'OUTSIDE': 1}.get(node.get('strokeAlign'), -1)))
            body = call('CustomPaint', foregroundPainter=painter, child=body)
        opacity = node.get('opacity', 1)
        if opacity <= 0:
            # Figma keeps an opacity-0 layer's Auto Layout space; a
            # hidden layer (visible: false) takes none and is omitted earlier.
            body = call('Visibility', visible='false', maintainSize='true', maintainAnimation='true',
                        maintainState='true', child=body)
        elif opacity != 1:
            body = call('Opacity', opacity=number(min(1, opacity)), child=body)
        transform = node.get('relativeTransform')
        if transform:
            # Translation belongs to Positioned; linear terms include rotation/skew/scale.
            a, b = transform
            if (a[:2], b[:2]) != ([1, 0], [0, 1]):
                matrix = [a[0], b[0], 0, 0, a[1], b[1], 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
                body = call('Transform', alignment='Alignment.topLeft', transform='Matrix4.fromList(' + sequence([number(v) for v in matrix]) + ')', child=body)
            if positioned:
                node = {**node, 'x': a[2], 'y': b[2]}
        if expanded:
            body = call('Expanded', child=body)
        if positioned:
            offsets = {'left': number(node['x']), 'top': number(node['y'])}
            # Figma MAX constraints pin the measured child, not an export's
            # viewport-sized sticky wrapper. Keep the child's own dimensions.
            # Rotated/scaled bounds need a separate transform-aware solution.
            linear_identity = not node.get('rotation', 0) and (
                not transform or (transform[0][:2], transform[1][:2]) == ([1, 0], [0, 1]))
            if parent and linear_identity:
                for axis, dimension, start, end, coordinate in (
                    ('horizontal', 'width', 'left', 'right', 'x'),
                    ('vertical', 'height', 'top', 'bottom', 'y'),
                ):
                    if node.get('constraints', {}).get(axis) == 'MAX':
                        offsets.pop(start)
                        offsets[end] = number(parent[dimension] - node[coordinate] - node[dimension])
            body = call('Positioned', **offsets, child=body)
        self.trace.append({'nodeId': node['id'], 'name': node.get('name'), 'type': kind,
                           'figmaUrl': f'https://www.figma.com/design/{self.file_key}?node-id={node["id"].replace(":", "-")}&m=dev'})
        return f'/* figma {node["id"]} */ ' + body

    def compile(self, original, class_name='FigmaDraft'):
        if not re.fullmatch(r'[A-Z][A-Za-z0-9]*', class_name):
            raise ValueError('Use a valid PascalCase Dart class name')
        normalized = self.normalize(original)
        if normalized is None:
            raise ValueError('Selected root is hidden')
        body = self.emit(normalized)
        imports = ["import 'package:flutter/material.dart';"]
        if self.uses_svg:
            imports.append("import 'package:flutter_svg/flutter_svg.dart';")
        if self.uses_blur:
            imports.append("import 'dart:ui' show ImageFilter;")
        if self.uses_gradient_stroke:
            imports.append("import 'dart:ui' as ui;")
        todos = '\n'.join('// FIGMA-TODO(' + w['reason'] + '): ' + str(w['nodeId']) + ' ' + w['message'].replace('\n', ' ') for w in self.warnings)
        tokens = '\n'.join(f'  static const {name} = Color(0x{value});' for name, value in self.colors.items())
        code = '\n'.join(imports) + '\n\n' + todos + f'''\nclass {class_name} extends StatelessWidget {{
  const {class_name}({{super.key}});
  @override
  Widget build(BuildContext context) {{
    return {body};
  }}
}}
''' + ('\nclass DraftTokens {\n' + tokens + '\n}\n' if tokens else '')
        if self.uses_gradient_stroke:
            code += GRADIENT_STROKE
        return {'dart': code, 'normalized': normalized, 'report': {'status': 'draft',
                'fileKey': self.file_key, 'rootNodeId': original['id'], 'warnings': self.warnings,
                'trace': self.trace, 'assets': self.assets, 'requiredFonts': sorted(self.fonts),
                'requiredFontWeights': {f: sorted(w) for f, w in sorted(self.font_weights.items())},
                'requiredFontStyles': {f: [{'weight': w, 'italic': i} for w, i in sorted(styles)]
                                       for f, styles in sorted(self.font_styles.items())},
                'visualApproval': 'unchecked',
                'review': 'Apply references/mapping.md and references/fidelity.md; bundle requiredFonts, split tokens and fixtures, and compare against immutable Figma evidence before canonical adoption.'}}


GRADIENT_STROKE = r"""
class DraftGradientStroke extends CustomPainter {
  const DraftGradientStroke({required this.a, required this.b, required this.offset,
    required this.colors, required this.stops, required this.radius,
    required this.width, required this.align});
  final double a, b, offset, width, align;
  final List<Color> colors;
  final List<double> stops;
  final BorderRadius radius;
  @override
  void paint(Canvas canvas, Size size) {
    if (size.isEmpty) return;
    final direction = Offset(a / size.width, b / size.height);
    final norm = direction.distanceSquared;
    final paint = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = width
      ..shader = ui.Gradient.linear(direction * (-offset / norm),
        direction * ((1 - offset) / norm), colors, stops);
    canvas.drawRRect(radius.toRRect(Offset.zero & size).inflate(align * width / 2), paint);
  }
  @override
  bool shouldRepaint(covariant DraftGradientStroke oldDelegate) =>
    a != oldDelegate.a || b != oldDelegate.b || offset != oldDelegate.offset ||
    width != oldDelegate.width || align != oldDelegate.align ||
    radius != oldDelegate.radius || colors != oldDelegate.colors || stops != oldDelegate.stops;
}
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path, help='Single node, document wrapper, or REST nodes response')
    parser.add_argument('--file-key', required=True)
    parser.add_argument('--repo-root', required=True, type=Path, help='Target repository root; draft output must stay outside it')
    parser.add_argument('--node-id', help='Select a node from a REST nodes response')
    parser.add_argument('--assets', type=Path, help='JSON map of original node id/imageRef to local bundled asset path')
    parser.add_argument('--variables', type=Path, help='JSON map of variable id to original variable name')
    parser.add_argument('--class-name', default='FigmaDraft')
    parser.add_argument('--output', required=True, type=Path, help='Scratch directory outside the repository')
    args = parser.parse_args()
    output = args.output.resolve()
    repo = args.repo_root.resolve()
    if not repo.is_dir():
        parser.error('Repository root must be an existing directory')
    if output == repo or repo in output.parents:
        parser.error('Draft output must be outside the repository; canonical code requires reviewed adoption')
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        parser.error('Draft output must be a new or empty directory')
    data = json.loads(args.input.read_text())
    if 'nodes' in data:
        if not args.node_id:
            parser.error('--node-id is required for a REST nodes response')
        data = data['nodes'][args.node_id]['document']
    else:
        data = data.get('document', data)
    compiler = Compiler(args.file_key,
        json.loads(args.assets.read_text()) if args.assets else None,
        json.loads(args.variables.read_text()) if args.variables else None)
    result = compiler.compile(data, args.class_name)
    output.mkdir(parents=True, exist_ok=True)
    (output / 'draft.dart').write_text(result['dart'])
    for name in ('normalized', 'report'):
        (output / (name + '.json')).write_text(json.dumps(result[name], ensure_ascii=False, indent=2) + '\n')
    print(f'Draft: {output / "draft.dart"}; {len(compiler.trace)} nodes, {len(compiler.warnings)} review items')


if __name__ == '__main__':
    main()
