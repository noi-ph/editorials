#!/usr/bin/env python3.10

from argparse import ArgumentParser
from pathlib import Path
from shutil import copytree, rmtree


def main():
    parser = ArgumentParser(description="Copy editorial files from somewhere else. WARNING: DON'T USE THIS UNLESS THE CONTEST IS ALREADY OVER!")

    parser.add_argument('source', type=Path, help="Source folder")
    parser.add_argument('year', type=Path, help="Contest year")
    parser.add_argument('contest', type=Path, help="Contest name")

    args = parser.parse_args()

    def _sources():
        yield args.source / args.year / 'editorials' / args.contest
        yield args.source / args.year / args.contest / 'editorials'

    def get_sources():
        for source in _sources():
            print(f"Trying source folder {source}")
            if source.is_dir():
                yield source

    if len(sources := [*get_sources()]) != 1:
        raise RuntimeError(f"Unique source folder not found. Got {sources}")

    [source] = sources
    target = args.year / args.contest
    print("SOURCE IS", source)
    print("TARGET IS", target)

    if not source.is_dir():
        raise RuntimeError(f"{source} is not an existing folder")

    print(f"CLEARING FOLDER: {target}")
    rmtree(target, ignore_errors=True)

    print("COPYING STUFF")
    copytree(source, target)

    print()
    print("DONE. PLEASE RUN ./compileall.py NEXT")


if __name__ == '__main__':
    main()
