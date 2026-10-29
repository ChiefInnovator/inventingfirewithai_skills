import copy
import unittest

from convert import Compiler, number, quote


def node(kind='RECTANGLE', **values):
    return {'id': '1:1', 'type': kind, 'width': 100, 'height': 40, **values}


class ConversionTests(unittest.TestCase):
    def test_absolute_background_stays_behind_bounded_flow(self):
        for sizing in ('FIXED', 'FILL'):
            source = node('FRAME', layoutMode='HORIZONTAL', layoutSizingHorizontal=sizing,
                primaryAxisAlignItems='CENTER', children=[
                    node(id='1:2', layoutPositioning='ABSOLUTE'), node(id='1:3', width=20)])
            before = copy.deepcopy(source)
            result = Compiler('file').compile(source)
            dart = result['dart']
            self.assertEqual(source, before)
            self.assertLess(dart.index('/* figma 1:2 */'), dart.index('Positioned.fill('))
            self.assertIn('Positioned.fill(child: Row(', dart)
            self.assertIn('MainAxisAlignment.center', dart)

    def test_hug_flow_is_not_stretched_and_interleaving_is_reported(self):
        source = node('FRAME', layoutMode='HORIZONTAL', layoutSizingVertical='HUG', children=[
            node(id='1:2'), node(id='1:3', layoutPositioning='ABSOLUTE'), node(id='1:4')])
        result = Compiler('file').compile(source)
        self.assertNotIn('Positioned.fill(child: Row(', result['dart'])
        self.assertTrue(any(w['reason'] == 'paint-order' for w in result['report']['warnings']))

    def test_stroke_paints_foreground_and_counts_layout_padding_once(self):
        for align, padding in [('OUTSIDE', 8), ('INSIDE', 11), ('CENTER', 11)]:
            source = node('FRAME', layoutMode='HORIZONTAL', paddingLeft=8,
                strokesIncludedInLayout=True, strokeAlign=align, strokeWeight=3,
                fills=[{'type': 'SOLID', 'color': {'r': 1, 'g': 0, 'b': 0}}],
                strokes=[{'type': 'SOLID', 'color': {'r': 0, 'g': 0, 'b': 1}}],
                children=[node(id='1:2')])
            dart = Compiler('file').compile(source)['dart']
            self.assertIn(f'padding: EdgeInsets.fromLTRB({padding},', dart)
            self.assertIn('position: DecorationPosition.foreground', dart)
            self.assertIn('strokeAlign: BorderSide.strokeAlign' + align.title(), dart)
            self.assertEqual(dart.count('Border.all('), 1)
            self.assertEqual(dart.count('color: DraftTokens.colorFFFF0000'), 1)
        source['individualStrokeWeights'] = {'left': 2, 'top': 4, 'right': 6, 'bottom': 8}
        self.assertIn('EdgeInsets.fromLTRB(10, 4, 6, 8)', Compiler('file').compile(source)['dart'])
        source['strokes'][0]['visible'] = False
        self.assertIn('EdgeInsets.fromLTRB(8, 0, 0, 0)', Compiler('file').compile(source)['dart'])

    def test_solid_dashed_strokes_remain_unresolved(self):
        result = Compiler('file').compile(node(dashPattern=[2, 3],
            strokes=[{'type': 'SOLID', 'color': {'r': 0, 'g': 0, 'b': 0}}]))
        self.assertTrue(any(w['reason'] == 'dashed-stroke' for w in result['report']['warnings']))

    def test_layer_and_background_blur_convert_radius_to_sigma(self):
        for kind in ('LAYER_BLUR', 'BACKGROUND_BLUR'):
            dart = Compiler('file').compile(node(effects=[{'type': kind, 'radius': 13}]))['dart']
            self.assertIn('ImageFilter.blur(sigmaX: 6.5, sigmaY: 6.5)', dart)

    def test_hug_centered_trailing_space_keeps_start_of_run(self):
        source = node('TEXT', characters='Label ', fontFamily='Example', fontSize=14,
            textAlignHorizontal='CENTER', textAutoResize='WIDTH_AND_HEIGHT')
        self.assertIn('textAlign: TextAlign.left', Compiler('file').compile(source)['dart'])
        source['textAutoResize'] = 'NONE'
        self.assertIn('textAlign: TextAlign.center', Compiler('file').compile(source)['dart'])

    def test_material_role_retains_source_height_or_reports_unknown_metrics(self):
        source = node('TEXT', characters='Label', fontFamily='Example', fontSize=14,
            styleName='M3/label/large', lineHeight={'unit': 'PIXELS', 'value': 21})
        result = Compiler('file').compile(source)
        self.assertIn('height: 1.5', result['dart'])
        self.assertFalse(any(w['reason'] == 'line-height' for w in result['report']['warnings']))
        del source['lineHeight']
        self.assertTrue(any(w['reason'] == 'line-height' for w in Compiler('file').compile(source)['report']['warnings']))

    def test_fixed_text_vertical_alignment_preserves_width_and_source(self):
        for vertical, flutter in [('CENTER', 'centerLeft'), ('BOTTOM', 'bottomLeft')]:
            for horizontal in ('LEFT', 'CENTER', 'RIGHT', 'JUSTIFIED'):
                for location in ('node', 'style'):
                    with self.subTest(vertical=vertical, horizontal=horizontal, location=location):
                        source = node('TEXT', width=143.5, height=65.25, characters='First line\nSecond',
                            fontFamily='Inter', fontSize=14)
                        properties = {'textAlignVertical': vertical, 'textAlignHorizontal': horizontal}
                        source.update(properties if location == 'node' else {'style': properties})
                        before = copy.deepcopy(source)
                        result = Compiler('file').compile(source)
                        self.assertEqual(source, before)
                        self.assertIn('SizedBox(width: 143.5, height: 65.25, child: Align(', result['dart'])
                        self.assertIn('alignment: Alignment.' + flutter, result['dart'])
                        self.assertIn('SizedBox(width: double.infinity, child: Text.rich(', result['dart'])
                        self.assertIn('textAlign: TextAlign.' + ('justify' if horizontal == 'JUSTIFIED' else horizontal.lower()), result['dart'])
                        self.assertFalse(any(w['reason'] == 'text-vertical-alignment' for w in result['report']['warnings']))

    def test_vertical_alignment_does_not_invent_hug_or_unmeasured_height(self):
        changes = [
            {'layoutSizingVertical': 'HUG'}, {'layoutSizingVertical': 'FILL'},
            {'layoutSizingHorizontal': 'HUG'}, {'layoutSizingHorizontal': 'FILL'},
            {'textAutoResize': 'HEIGHT'}, {'textAutoResize': 'WIDTH_AND_HEIGHT'},
            {'height': 0}, {'width': 0}, {'textAlignVertical': 'UNKNOWN'},
        ]
        for change in changes:
            with self.subTest(change=change):
                source = node('TEXT', characters='Text', fontFamily='Inter',
                    textAlignVertical='CENTER', **{k: v for k, v in change.items() if k != 'textAlignVertical'})
                source.update(change)
                result = Compiler('file').compile(source)
                self.assertNotIn('Align(', result['dart'])
                self.assertTrue(any(w['reason'] == 'text-vertical-alignment' for w in result['report']['warnings']))
        source = {'id': '1:1', 'type': 'TEXT', 'characters': 'Unmeasured', 'textAlignVertical': 'BOTTOM'}
        self.assertTrue(any(w['reason'] == 'text-vertical-alignment' for w in Compiler('file').compile(source)['report']['warnings']))

    def test_vertical_alignment_uses_rest_bounds_and_keeps_truncation_warning(self):
        source = {'id': '1:1', 'type': 'TEXT', 'characters': 'Log in',
            'absoluteBoundingBox': {'x': 100, 'y': 200, 'width': 48, 'height': 16},
            'style': {'textAlignVertical': 'CENTER', 'fontFamily': 'Inter', 'fontSize': 12}}
        self.assertIn('SizedBox(width: 48, height: 16, child: Align(', Compiler('file').compile(source)['dart'])
        for flag in ({'maxLines': 1}, {'textTruncation': 'ENDING'}, {'textAutoResize': 'TRUNCATE'}):
            with self.subTest(flag=flag):
                source['style'].update(flag)
                self.assertTrue(any('Text truncation' in w['message'] for w in Compiler('file').compile(source)['report']['warnings']))
                for key in flag:
                    del source['style'][key]
        for vertical in (None, 'TOP'):
            source['style']['textAlignVertical'] = vertical
            self.assertNotIn('Align(', Compiler('file').compile(source)['dart'])

    def test_gradient_stroke_preserves_affine_alpha_alignment_and_round_clip(self):
        source = node('FRAME', cornerRadius=12, clipsContent=True, opacity=.5,
            relativeTransform=[[0, -1, 0], [1, 0, 0]],
            effects=[{'type': 'BACKGROUND_BLUR', 'radius': 10}],
            strokeWeight=1, strokeAlign='OUTSIDE', strokes=[{
                'type': 'GRADIENT_LINEAR', 'opacity': .5,
                'gradientTransform': [[-.64, -.038, .82], [.7, -.13, 0]],
                'gradientStops': [
                    {'position': 0, 'color': {'r': 1, 'g': 0, 'b': 0, 'a': 1}},
                    {'position': 1, 'color': {'r': 1, 'g': 1, 'b': 1, 'a': .05}}]}])
        before = copy.deepcopy(source)
        result = Compiler('file').compile(source)
        dart = result['dart']
        self.assertEqual(source, before)
        self.assertIn('DraftGradientStroke(a: -0.64, b: -0.038, offset: 0.82', dart)
        self.assertIn('Color(0x80FF0000)', dart)
        self.assertIn('Color(0x06FFFFFF)', dart)
        self.assertIn('width: 1, align: 1', dart)
        self.assertIn('ClipRRect(borderRadius: BorderRadius.circular(12), child: BackdropFilter(', dart)
        self.assertLess(dart.index('Transform('), dart.index('Opacity('))
        self.assertLess(dart.index('Opacity('), dart.index('CustomPaint('))
        self.assertFalse(any('non-solid stroke' in w['message'] for w in result['report']['warnings']))
        for align, value in [('INSIDE', -1), ('CENTER', 0)]:
            source['strokeAlign'] = align
            self.assertIn(f'width: 1, align: {value}', Compiler('file').compile(source)['dart'])

    def test_square_gradient_stroke_retains_zero_radius_and_bound_stop(self):
        source = node(strokes=[{'type': 'GRADIENT_LINEAR',
            'gradientTransform': [[1, 0, 0], [0, 1, 0]], 'gradientStops': [
                {'position': 0, 'color': {'r': 0, 'g': .5, 'b': 1},
                 'boundVariables': {'color': {'name': 'Palette/Accent'}}},
                {'position': 1, 'color': {'r': 1, 'g': 1, 'b': 1}}]}])
        result = Compiler('file').compile(source)
        self.assertIn('radius: BorderRadius.zero', result['dart'])
        self.assertIn('colors: [DraftTokens.colorFF0080FF,', result['dart'])
        self.assertTrue(any('Palette/Accent' in w['message'] for w in result['report']['warnings']))

    def test_unsupported_gradient_strokes_remain_explicit(self):
        base = node(strokes=[{'type': 'GRADIENT_LINEAR',
            'gradientTransform': [[1, 0, 0], [0, 1, 0]],
            'gradientStops': [{'position': 0, 'color': {'r': 1, 'g': 0, 'b': 0}},
                              {'position': 1, 'color': {'r': 0, 'g': 0, 'b': 1}}]}])
        for change in ({'type': 'ELLIPSE'}, {'dashPattern': [2, 2]},
                       {'individualStrokeWeights': {'top': 1}}, {'strokeAlign': 'INVALID'}):
            result = Compiler('file').compile({**base, **change})
            self.assertNotIn('class DraftGradientStroke', result['dart'])
            self.assertTrue(any('Unsupported non-solid stroke' in w['message'] for w in result['report']['warnings']))
        for field, value in [('gradientTransform', [[0, 0, 0], [0, 1, 0]]),
                             ('gradientStops', [{'position': 'bad'}])]:
            source = copy.deepcopy(base)
            source['strokes'][0][field] = value
            self.assertNotIn('class DraftGradientStroke', Compiler('file').compile(source)['dart'])

    def test_nonzero_paragraph_spacing_is_explicitly_unresolved(self):
        for location in ('node', 'style', 'segment'):
            source = node('TEXT', characters='One\nTwo', fontName={'family': 'Inter', 'style': 'Regular'}, fontSize=16)
            target = source
            if location == 'style':
                target = source.setdefault('style', {})
            elif location == 'segment':
                target = {'characters': 'One\nTwo'}
                source['styledTextSegments'] = [target]
            target['paragraphSpacing'] = 12
            before = copy.deepcopy(source)
            warnings = Compiler('file').compile(source)['report']['warnings']
            self.assertEqual(source, before)
            self.assertEqual(len([w for w in warnings if w['reason'] == 'paragraph-spacing']), 1)
            target['paragraphSpacing'] = 0
            self.assertFalse(any(w['reason'] == 'paragraph-spacing' for w in Compiler('file').compile(source)['report']['warnings']))

    def test_source_missing_font_blocks_approval_even_with_declared_family(self):
        source = node('TEXT', characters='Reply\n\nHeads up', hasMissingFont=True,
            fontName={'family': 'SF Pro Display', 'style': 'Regular'}, fontSize=15)
        before = copy.deepcopy(source)
        result = Compiler('file').compile(source)
        self.assertEqual(source, before)
        self.assertEqual(result['report']['requiredFonts'], ['SF Pro Display'])
        missing = [w for w in result['report']['warnings'] if w['reason'] == 'missing-font']
        self.assertEqual(len(missing), 1)
        self.assertEqual(missing[0]['nodeId'], '1:1')
        source['hasMissingFont'] = False
        self.assertFalse(any(w['reason'] == 'missing-font'
            for w in Compiler('file').compile(source)['report']['warnings']))

    def test_max_constraints_anchor_measured_child_without_viewport_height(self):
        for keyboard_height in (0, 336):
            height = 140.25 + keyboard_height
            source = node('FRAME', width=393, height=852, children=[
                node('FRAME', id='1:2', x=0, y=852-height, width=393,
                     height=height, constraints={'horizontal': 'MIN', 'vertical': 'MAX'})])
            result = Compiler('file').compile(source)['dart']
            self.assertIn('Positioned(left: 0, bottom: 0,', result)
            self.assertIn('height: ' + number(height), result)
            self.assertEqual(result.count('height: 852'), 1)

    def test_max_constraints_keep_trailing_insets_and_transformed_fallback(self):
        child = node(id='1:2', x=270, y=180, width=100, height=40,
                     constraints={'horizontal': 'MAX', 'vertical': 'MAX'})
        source = node('FRAME', width=393, height=240, children=[child])
        self.assertIn('Positioned(right: 23, bottom: 20,', Compiler('file').compile(source)['dart'])
        for matrix in (
            [[0, -1, 270], [1, 0, 180]],  # rotation
            [[2, 0, 270], [0, .5, 180]],  # non-unit scale
            [[1, .2, 270], [0, 1, 180]],  # skew
        ):
            with self.subTest(matrix=matrix):
                child['relativeTransform'] = matrix
                dart = Compiler('file').compile(source)['dart']
                self.assertIn('Positioned(left: 270, top: 180,', dart)
                self.assertNotIn('Positioned(right:', dart)
                self.assertNotIn('bottom:', dart)
        child.pop('relativeTransform')
        child['rotation'] = 90
        result = Compiler('file').compile(source)
        self.assertIn('Positioned(left: 270, top: 180,', result['dart'])
        self.assertNotIn('Positioned(right:', result['dart'])

    def test_opentype_features_preserve_enabled_disabled_and_segment_overrides(self):
        source = node('TEXT', fontFamily='Roboto', fontSize=14,
            openTypeFeatures={'LIGA': True}, styledTextSegments=[
                {'characters': '9:30', 'openTypeFeatures':
                 {'SS02': True, 'DLIG': True, 'LNUM': True, 'PNUM': True, 'LIGA': False}},
                {'characters': ' ffi', 'openTypeFeatures': {}},
            ])
        result = Compiler('file').compile(source)
        for tag in ('ss02', 'dlig', 'lnum', 'pnum'):
            self.assertIn(f'FontFeature("{tag}", 1)', result['dart'])
        self.assertIn('FontFeature("liga", 0)', result['dart'])
        self.assertNotIn('FontFeature("liga", 1)', result['dart'])
        self.assertEqual(result['dart'].count('fontFeatures:'), 1)
        self.assertFalse(any('OpenType' in w['message'] for w in result['report']['warnings']))

    def test_unresolved_or_invalid_opentype_features_remain_explicit(self):
        for features in ('mixed', {'BAD': True}, {'LIGA': 'false'}):
            result = Compiler('file').compile(node('TEXT', characters='text',
                fontFamily='Roboto', openTypeFeatures=features))
            self.assertTrue(any('OpenType' in w['message'] for w in result['report']['warnings']))
            self.assertNotIn('fontFeatures:', result['dart'])

    def test_variable_font_axes_override_named_weight_without_rounding_geometry(self):
        source = node('TEXT', characters='25', textAutoResize='WIDTH_AND_HEIGHT',
            fontName={'family': 'Roboto', 'style': 'Medium',
                      'variationSettings': {'wght': 550, 'wdth': 87.5}}, fontSize=16)
        result = Compiler('file').compile(source)
        self.assertIn('FontVariation("wght", 550)', result['dart'])
        self.assertIn('FontVariation("wdth", 87.5)', result['dart'])
        self.assertEqual(result['report']['requiredFontWeights']['Roboto'], [550])
        self.assertFalse(any(w['reason'] == 'missing-font' for w in result['report']['warnings']))
        self.assertNotIn('SizedBox(width:', result['dart'])

    def test_input_is_preserved_and_hidden_children_omitted(self):
        source = node('FRAME', children=[node(id='1:2', visible=False)])
        before = copy.deepcopy(source)
        result = Compiler('file').compile(source)
        self.assertEqual(source, before)
        self.assertEqual(len(result['report']['trace']), 1)

    def test_mixed_flow_keeps_row_under_absolute_overlay(self):
        source = node('FRAME', layoutMode='HORIZONTAL', children=[
            node(id='1:2', layoutSizingHorizontal='FILL'),
            node(id='1:3', layoutPositioning='ABSOLUTE', x=5, y=7)])
        result = Compiler('file').compile(source)['dart']
        self.assertIn('Row(', result)
        self.assertIn('Stack(', result)
        self.assertIn('Expanded(', result)
        self.assertIn('Positioned(left: 5, top: 7', result)

    def test_rest_absolute_bounds_become_parent_relative(self):
        source = {'id': '1:1', 'type': 'GROUP', 'absoluteBoundingBox':
                  {'x': 100, 'y': 200, 'width': 100, 'height': 100},
                  'children': [{'id': '1:2', 'type': 'RECTANGLE',
                    'absoluteBoundingBox': {'x': 110, 'y': 225, 'width': 20, 'height': 30}}]}
        result = Compiler('file').compile(source)
        self.assertIn('Positioned(left: 10, top: 25', result['dart'])
        self.assertEqual(result['normalized']['x'], 0)

    def test_rotated_rest_node_uses_local_size_not_axis_aligned_bounds(self):
        source = {'id': '1:1', 'type': 'RECTANGLE', 'size': {'x': 60, 'y': 30},
                  'relativeTransform': [[0, -1, 0], [1, 0, 0]],
                  'absoluteBoundingBox': {'x': 0, 'y': 0, 'width': 30, 'height': 60}}
        result = Compiler('file').compile(source)
        self.assertEqual(result['normalized']['width'], 60)
        self.assertEqual(result['normalized']['height'], 30)

    def test_wrap_does_not_emit_illegal_expanded(self):
        compiler = Compiler('file')
        result = compiler.compile(node('FRAME', layoutMode='HORIZONTAL', layoutWrap='WRAP',
            itemSpacing=8, counterAxisSpacing=12, children=[node(id='1:2', layoutSizingHorizontal='FILL')]))
        self.assertIn('Wrap(', result['dart'])
        self.assertNotIn('Expanded(', result['dart'])
        self.assertTrue(any('Wrap' in w['message'] for w in compiler.warnings))

    def test_gradient_coordinates_stops_and_alpha_preserved(self):
        source = node(fills=[{'type': 'GRADIENT_LINEAR', 'opacity': .5,
            'gradientHandlePositions': [{'x': 0, 'y': 0}, {'x': 1, 'y': 1}],
            'gradientStops': [{'position': .1, 'color': {'r': 1, 'g': 0, 'b': 0, 'a': .5}},
                              {'position': .9, 'color': {'r': 0, 'g': 1, 'b': 0, 'a': 1}}]}])
        result = Compiler('file').compile(source)['dart']
        self.assertIn('Alignment(-1, -1)', result)
        self.assertIn('stops: [0.1, 0.9]', result)
        self.assertIn('Color(0x40FF0000)', result)

    def test_bound_variable_keeps_source_colour_without_app_dependency(self):
        source = node(fills=[{'type': 'SOLID', 'color': {'r': 0, 'g': .5, 'b': 1},
                             'variableColorName': 'Palette/Accent'}])
        result = Compiler('ExampleFile').compile(source)
        self.assertIn('Color(0xFF0080FF)', result['dart'])
        self.assertNotIn('Theme.of(', result['dart'])
        self.assertIn('Palette/Accent', str(result['report']['warnings']))

    def test_rich_text_and_m3_roles_retain_resolved_fonts_and_metrics(self):
        source = node('TEXT', styledTextSegments=[
            {'characters': '12,345,678', 'styleName': 'M3/display/small',
             'fontName': {'family': 'Funnel Display', 'style': 'Regular'},
             'fontSize': 38, 'fontWeight': 400, 'lineHeightPx': 44, 'letterSpacing': -.8},
            {'characters': '.31', 'fontFamily': 'Poppins', 'fontSize': 22, 'fontWeight': 500}])
        result = Compiler('file').compile(source)
        self.assertIn('fontFamily: "Funnel Display"', result['dart'])
        self.assertIn('fontFamily: "Poppins"', result['dart'])
        self.assertIn('fontSize: 38', result['dart'])
        self.assertIn('height: 1.157895', result['dart'])
        self.assertIn('letterSpacing: -0.8', result['dart'])
        self.assertEqual(result['report']['requiredFonts'], ['Funnel Display', 'Poppins'])
        self.assertEqual(result['report']['visualApproval'], 'unchecked')

    def test_font_absence_is_an_explicit_visual_blocker(self):
        result = Compiler('file').compile(node('TEXT', characters='Continue', fontSize=16))
        self.assertTrue(any(w['reason'] == 'missing-font' for w in result['report']['warnings']))

    def test_plugin_font_name_resolves_weight_without_rest_font_weight(self):
        result = Compiler('file').compile(node('TEXT', characters='Continue', fontSize=16,
            fontName={'family': 'Poppins', 'style': 'SemiBold Italic'}))
        self.assertIn('FontWeight.w600', result['dart'])
        self.assertIn('FontStyle.italic', result['dart'])
        self.assertEqual(result['report']['requiredFontWeights'], {'Poppins': [600]})

    def test_plugin_segment_font_overrides_inherited_rest_style(self):
        result = Compiler('file').compile(node('TEXT',
            style={'fontFamily': 'Inter', 'fontWeight': 400, 'italic': True, 'fontSize': 16},
            styledTextSegments=[{'characters': 'Heading', 'fontName': {'family': 'Poppins', 'style': 'SemiBold'}},
                                {'characters': 'detail', 'fontName': {'family': 'Inter', 'style': 'Medium Italic'}}]))
        self.assertEqual(result['report']['requiredFontWeights'], {'Poppins': [600], 'Inter': [500]})
        self.assertEqual(result['report']['requiredFontStyles']['Poppins'], [{'weight': 600, 'italic': False}])
        self.assertEqual(result['report']['requiredFontStyles']['Inter'], [{'weight': 500, 'italic': True}])
        self.assertIn('fontFamily: "Poppins"', result['dart'])
        self.assertIn('FontWeight.w600', result['dart'])
        self.assertEqual(result['dart'].count('fontStyle: FontStyle.italic'), 1)

    def test_bound_token_preserves_colour_alpha_and_paint_opacity(self):
        result = Compiler('file').compile(node(fills=[{'type': 'SOLID', 'opacity': .5,
            'color': {'r': 1, 'g': 1, 'b': 1, 'a': .5},
            'variableColorName': 'Palette/White'}]))
        self.assertIn('Color(0x40FFFFFF)' , result['dart'])

    def test_rich_text_is_complete_and_dart_strings_are_escaped(self):
        source = node('TEXT', styledTextSegments=[
            {'characters': "I'm $here\n", 'fontSize': 16, 'fontWeight': 400},
            {'characters': 'Bold', 'fontSize': 16, 'fontWeight': 700}])
        result = Compiler('file').compile(source)['dart']
        self.assertIn('Text.rich(', result)
        self.assertIn(r'\$here\n', result)
        self.assertIn('FontWeight.w700', result)
        self.assertIn('"I\'m', result)

    def test_rest_mixed_text_runs_are_reconstructed(self):
        source = node('TEXT', characters='abcd', characterStyleOverrides=[0, 0, 1, 1],
                      styleOverrideTable={'1': {'fontWeight': 700}}, style={'fontSize': 16})
        result = Compiler('file').compile(source)['dart']
        self.assertIn('text: "ab"', result)
        self.assertIn('text: "cd"', result)

    def test_asset_path_is_local_and_missing_vector_is_visible(self):
        compiler = Compiler('file', {'1:1': 'assets/icons/icon.svg'})
        self.assertIn('SvgPicture.asset', compiler.compile(node('VECTOR'))['dart'])
        missing = Compiler('file').compile(node('VECTOR'))
        self.assertIn('Placeholder()', missing['dart'])
        self.assertTrue(missing['report']['warnings'])
        with self.assertRaises(ValueError):
            Compiler('file', {'1:1': '../outside.png'}).compile(node('VECTOR'))

    def test_opacity_and_transform_both_apply(self):
        result = Compiler('file').compile(node(opacity=.5, relativeTransform=[[0, -1, 5], [1, 0, 7]]))
        self.assertIn('Opacity(opacity: 0.5', result['dart'])
        self.assertIn('Transform(', result['dart'])

    def test_unsupported_features_remain_explicit(self):
        result = Compiler('file').compile(node(isMask=True, effects=[{'type': 'INNER_SHADOW'}],
            fills=[{'type': 'GRADIENT_DIAMOND', 'gradientStops': []}]))
        self.assertGreaterEqual(len(result['report']['warnings']), 3)
        self.assertEqual(result['report']['status'], 'draft')

    def test_opacity_zero_keeps_layout_space_and_hidden_layers_take_none(self):
        bar = node(id='1:3', width=40, height=2, opacity=0)
        source = node('FRAME', layoutMode='VERTICAL', itemSpacing=12, children=[node(id='1:2'), bar])
        dart = Compiler('file').compile(source)['dart']
        self.assertIn('Visibility(visible: false, maintainSize: true, maintainAnimation: true, '
                      'maintainState: true, child: SizedBox(width: 40, height: 2', dart)
        self.assertNotIn('Opacity(', dart)
        bar['visible'] = False
        self.assertNotIn('Visibility(', Compiler('file').compile(source)['dart'])

    def test_line_boxes_use_an_even_strut(self):
        source = node('TEXT', characters='9:30', width=29, height=20, fontSize=14,
            fontName={'family': 'Roboto', 'style': 'Medium', 'variationSettings': {'wght': 500, 'wdth': 100}},
            lineHeight={'unit': 'PIXELS', 'value': 20})
        dart = Compiler('file').compile(source)['dart']
        self.assertIn('strutStyle: StrutStyle(fontFamily: "Roboto", fontSize: 14, height: 1.428571, '
                      'leadingDistribution: TextLeadingDistribution.even, forceStrutHeight: true)', dart)
        # Normal leading on a single line takes the measured box (Poppins 10.5 -> 16).
        source = node('TEXT', characters='Legal', width=30, height=16, fontSize=10.5, textAutoResize='WIDTH_AND_HEIGHT',
            fontName={'family': 'Poppins', 'style': 'Regular'}, lineHeight={'unit': 'AUTO'})
        dart = Compiler('file').compile(source)['dart']
        self.assertIn('height: 1.52381', dart)
        self.assertIn('StrutStyle(fontFamily: "Poppins", fontSize: 10.5, height: 1.52381', dart)
        # A fixed box is not the line box: its spare space belongs to
        # textAlignVertical, so normal leading keeps natural metrics.
        fixed = dict(source, textAutoResize='NONE', height=40, textAlignVertical='BOTTOM')
        dart = Compiler('file').compile(fixed)['dart']
        self.assertNotIn('StrutStyle(', dart)
        self.assertIn('Align(alignment: Alignment.bottomLeft', dart)
        # A wrapped normal-leading paragraph has no single measured line box.
        source.update(characters='One\nTwo', height=32)
        self.assertNotIn('StrutStyle(', Compiler('file').compile(source)['dart'])
        # An explicit line height in a fixed aligned box keeps both the strut and the alignment.
        both = Compiler('file').compile(node('TEXT', characters='Log in', width=48, height=24, fontSize=16,
            fontName={'family': 'Inter', 'style': 'Medium'}, lineHeight={'unit': 'PIXELS', 'value': 16},
            textAutoResize='NONE', textAlignVertical='CENTER'))['dart']
        self.assertIn('Align(alignment: Alignment.centerLeft', both)
        self.assertIn('StrutStyle(fontFamily: "Inter", fontSize: 16, height: 1,', both)
        # Mixed run sizes keep per-span heights and say so.
        mixed = Compiler('file').compile(node('TEXT', characters='$10.31', height=44, styledTextSegments=[
            {'characters': '$10', 'fontFamily': 'Poppins', 'fontSize': 38, 'lineHeightPx': 44},
            {'characters': '.31', 'fontFamily': 'Poppins', 'fontSize': 22, 'lineHeightPx': 44}]))
        self.assertNotIn('StrutStyle(', mixed['dart'])
        self.assertTrue(any('per-span height' in w['message'] for w in mixed['report']['warnings']))

    def test_negative_gap_shrinks_each_slot_but_the_last(self):
        source = node('FRAME', layoutMode='VERTICAL', itemSpacing=-2, children=[
            node(id='1:2', width=85, height=40), node(id='1:3', width=120, height=16)])
        result = Compiler('file').compile(source)
        dart = result['dart']
        self.assertIn('Align(alignment: Alignment.topLeft, widthFactor: 1, heightFactor: (40 - 2) / 40, '
                      'child: SizedBox(height: 40, child: /* figma 1:2 */', dart)
        self.assertEqual(dart.count('Align('), 1)
        self.assertIn('spacing: 0', dart)
        self.assertFalse(any('Negative gap' in w['message'] for w in result['report']['warnings']))
        source.update(layoutMode='HORIZONTAL')
        self.assertIn('widthFactor: (85 - 2) / 85, heightFactor: 1, child: SizedBox(width: 85',
                      Compiler('file').compile(source)['dart'])
        source['children'][0]['layoutSizingHorizontal'] = 'FILL'
        self.assertTrue(any('Negative gap' in w['message']
                            for w in Compiler('file').compile(source)['report']['warnings']))

    def test_variable_runs_preserve_family_and_weight_axis(self):
        source = node('TEXT', characters='© 2026', fontSize=11,
            fontName={'family': 'Inter', 'style': 'Medium', 'variationSettings': {'wght': 500, 'slnt': 0}})
        result = Compiler('file').compile(source)
        self.assertIn('fontFamily: "Inter"', result['dart'])
        self.assertIn('FontVariation("wght", 500)', result['dart'])
        self.assertNotIn('fontWeight:', result['dart'])
        self.assertEqual(result['report']['requiredFonts'], ['Inter'])
        static = Compiler('file').compile(node('TEXT', characters='Go', fontSize=16,
            fontName={'family': 'Inter', 'style': 'Semi Bold'}))['dart']
        self.assertIn('fontFamily: "Inter"', static)
        self.assertIn('FontWeight.w600', static)

    def test_precision_and_non_finite_inputs(self):
        self.assertEqual(number(.000004), '0.000004')
        self.assertEqual(quote('$x'), '"\\$x"')
        with self.assertRaises(ValueError):
            number(float('inf'))


if __name__ == '__main__':
    unittest.main()
