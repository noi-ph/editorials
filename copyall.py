#!/usr/bin/env python3.10

from argparse import ArgumentParser
from pathlib import Path
from shutil import copytree, rmtree


def main():
    parser = ArgumentParser(description="Copy editorial files from somewhere else. WARNING: DON'T USE THIS UNLESS THE CONTEST IS ALREADY OVER!")

    parser.add_argument('source', type=Path, help="Source folder")
    parser.add_argument('target', type=Path, help="Target folder (default is computed from 'source')", nargs='?')

    args = parser.parse_args()

    source = args.source

    if not source.is_dir():
        raise RuntimeError(f"{source} is not an existing folder")

    if source.name != 'editorials':
        raise RuntimeError(f"{source} is not an 'editorials' folder")

    print("SOURCE IS", source)

    if not (target := args.target):
        target = args.source.parent
        target = target.relative_to(target.parent.parent)

    print("TARGET IS", target)

    print(f"CLEARING FOLDER: {target}")
    rmtree(target, ignore_errors=True)

    print("COPYING STUFF")
    copytree(source, target)

    print()
    print("DONE. PLEASE RUN ./compileall.py AFTER")


if __name__ == '__main__':
    main()
