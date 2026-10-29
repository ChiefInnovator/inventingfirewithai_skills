#!/usr/bin/env python3
"""Analyze and render synthetic compiler output in a temporary Flutter package.

Uses default test fonts; this checks generated Dart/layout, not real-screen fidelity.
No target repository or private assets are read. Package resolution may use the network.
"""
import argparse
from pathlib import Path
import subprocess
import tempfile

from convert import Compiler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--flutter', default='flutter')
    args = parser.parse_args()
    cases = [
        {'id': '1:1', 'type': 'RECTANGLE', 'width': 80, 'height': 30,
         'fills': [{'type': 'SOLID', 'color': {'r': 0, 'g': .5, 'b': 1}}]},
        {'id': '1:2', 'type': 'FRAME', 'width': 200, 'height': 80,
         'layoutMode': 'HORIZONTAL', 'itemSpacing': 8, 'children': [
             {'id': '1:3', 'type': 'RECTANGLE', 'width': 30, 'height': 30},
             {'id': '1:4', 'type': 'RECTANGLE', 'width': 60, 'height': 30}]},
        {'id': '1:5', 'type': 'TEXT', 'width': 160, 'height': 64,
         'characters': 'Example', 'fontSize': 16, 'textAutoResize': 'NONE',
         'textAlignVertical': 'CENTER'},
        {'id': '1:6', 'type': 'FRAME', 'width': 200, 'height': 160,
         'children': [{'id': '1:7', 'type': 'RECTANGLE', 'width': 50, 'height': 20,
                       'x': 130, 'y': 120, 'constraints': {'horizontal': 'MAX', 'vertical': 'MAX'}}]},
        {'id': '2:1', 'type': 'FRAME', 'width': 200, 'height': 80,
         'layoutMode': 'HORIZONTAL', 'primaryAxisAlignItems': 'CENTER',
         'counterAxisAlignItems': 'CENTER', 'children': [
             {'id': '2:2', 'type': 'RECTANGLE', 'layoutPositioning': 'ABSOLUTE',
              'width': 200, 'height': 80, 'fills': [{'type': 'SOLID', 'color': {'r': 1, 'g': 0, 'b': 0}}]},
             {'id': '2:3', 'type': 'RECTANGLE', 'width': 40, 'height': 10}]},
        {'id': '3:1', 'type': 'FRAME', 'width': 200, 'height': 80,
         'layoutMode': 'HORIZONTAL', 'paddingLeft': 8, 'paddingTop': 8,
         'strokesIncludedInLayout': True, 'strokeAlign': 'OUTSIDE', 'strokeWeight': 3,
         'strokes': [{'type': 'SOLID', 'color': {'r': 0, 'g': 0, 'b': 1}}],
         'children': [{'id': '3:2', 'type': 'RECTANGLE', 'width': 40, 'height': 10}]},
        {'id': '4:1', 'type': 'FRAME', 'width': 200, 'height': 80,
         'layoutMode': 'HORIZONTAL', 'paddingLeft': 8, 'paddingTop': 8,
         'strokesIncludedInLayout': True, 'strokeAlign': 'INSIDE', 'strokeWeight': 3,
         'strokes': [{'type': 'SOLID', 'color': {'r': 0, 'g': 0, 'b': 1}}],
         'children': [{'id': '4:2', 'type': 'RECTANGLE', 'width': 40, 'height': 10}]},
        {'id': '5:1', 'type': 'FRAME', 'width': 200, 'height': 80,
         'layoutMode': 'HORIZONTAL', 'paddingLeft': 8, 'paddingTop': 8,
         'strokesIncludedInLayout': True, 'strokeAlign': 'CENTER', 'strokeWeight': 3,
         'strokes': [{'type': 'SOLID', 'color': {'r': 0, 'g': 0, 'b': 1}}],
         'children': [{'id': '5:2', 'type': 'RECTANGLE', 'width': 40, 'height': 10}]},
        {'id': '6:1', 'type': 'TEXT', 'width': 200, 'height': 40,
         'characters': 'Short\nMuch longer line ', 'fontSize': 14,
         'textAlignHorizontal': 'CENTER', 'textAutoResize': 'WIDTH_AND_HEIGHT'},
    ]
    with tempfile.TemporaryDirectory(prefix='figma-flutter-check-') as directory:
        root = Path(directory)
        (root / 'lib').mkdir()
        (root / 'test').mkdir()
        (root / 'pubspec.yaml').write_text('''name: figma_draft_check
publish_to: none
environment:
  sdk: '>=3.6.0 <4.0.0'
dependencies:
  flutter:
    sdk: flutter
dev_dependencies:
  flutter_test:
    sdk: flutter
''')
        for index, source in enumerate(cases):
            result = Compiler('ExampleFile').compile(source, f'Case{index}')
            (root / 'lib' / f'case_{index}.dart').write_text(result['dart'])
        imports = '\n'.join(f"import 'package:figma_draft_check/case_{i}.dart';" for i in range(len(cases)))
        widgets = ', '.join(f'Case{i}()' for i in range(len(cases)))
        (root / 'test' / 'render_test.dart').write_text("""import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
""" + imports + '\nvoid main() {\n' + f'  final cases = <Widget>[{widgets}];\n' + '''
  for (var i = 0; i < cases.length; i++) {
    testWidgets('generated case $i renders', (tester) async {
      await tester.pumpWidget(MaterialApp(home: Scaffold(body: Center(child: cases[i]))));
      await tester.pump();
      expect(tester.takeException(), isNull);
      if (i == 0) expect(tester.getSize(find.byWidget(cases[i])), const Size(80, 30));
      if (i == 2) {
        final label = find.descendant(of: find.byWidget(cases[i]), matching: find.byType(RichText));
        expect(label, findsOneWidget);
        expect(tester.getCenter(label).dy, closeTo(tester.getCenter(find.byWidget(cases[i])).dy, .01));
      }
      if (i == 3) {
        final positioned = tester.widget<Positioned>(find.descendant(
          of: find.byWidget(cases[i]), matching: find.byType(Positioned)));
        expect(positioned.right, 20);
        expect(positioned.bottom, 20);
      }
      if (i >= 4 && i <= 7) {
        final child = find.descendant(of: find.byWidget(cases[i]),
          matching: find.byWidgetPredicate((w) => w is SizedBox && w.width == 40 && w.height == 10));
        expect(child, findsOneWidget);
        final outer = tester.getRect(find.byWidget(cases[i]));
        final inner = tester.getRect(child);
        if (i == 4) {
          expect(inner.center, outer.center);
          final stack = tester.widget<Stack>(find.descendant(
            of: find.byWidget(cases[i]), matching: find.byType(Stack)));
          expect((stack.children.first as Positioned).left, 0);
        } else {
          final inset = i == 6 ? 11.0 : 8.0;
          expect(inner.left - outer.left, inset);
          expect(inner.top - outer.top, inset);
          final border = tester.widgetList<DecoratedBox>(find.descendant(
            of: find.byWidget(cases[i]), matching: find.byType(DecoratedBox)))
            .where((w) => (w.decoration as BoxDecoration).border != null).single;
          expect(border.position, DecorationPosition.foreground);
        }
      }
      if (i == 8) {
        final text = tester.widget<RichText>(find.descendant(
          of: find.byWidget(cases[i]), matching: find.byType(RichText)));
        expect(text.text.toPlainText().split(String.fromCharCode(10)),
          ['Short', 'Much longer line ']);
        expect(text.textAlign, TextAlign.center);
      }
    });
  }
}
''')
        for command in ([args.flutter, 'pub', 'get'], [args.flutter, 'analyze'],
                        [args.flutter, 'test', '--reporter', 'expanded']):
            subprocess.run(command, cwd=root, check=True)


if __name__ == '__main__':
    main()
