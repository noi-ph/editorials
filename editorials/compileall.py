#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
from subprocess import run

def main():
    parser = ArgumentParser(description='Compile .md files to .html files')

    parser.add_argument('loc', nargs='*', default=[Path()], type=Path,
        help='Folder containing files to compile (default: current folder)')
    parser.add_argument('-t', '--template', default='editorial_template.html', type=Path,
        help='HTML template for pandoc to use (default: %(default)s)')

    args = parser.parse_args()

    print(f"USING TEMPLATE {args.template}")

    for loc in args.loc:
        if not loc.is_dir():
            raise RuntimeError(f"{loc} is not an existing folder")

    for loc in args.loc:
        print()
        print(f"COMPILING .md FILES IN FOLDER: {loc}")
        for file in loc.glob('**/*.md'):
            target = file.with_suffix('.html')
            print(f"COMPILING: {file} --> {target}")
            run(['pandoc',
                str(file),
                '-o', str(target),
                '-s',
                '--mathjax',
                f'--template={args.template}',
            ])

    print()
    print("DONE")

if __name__ == '__main__':
    main()
