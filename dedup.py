#!/usr/bin/env python3
"""Remove duplicate images by perceptual hashing.
Prefers wallhaven-* named files when resolving duplicates."""

import sys
from pathlib import Path
from PIL import Image
import imagehash

THRESHOLD = 5


def find_duplicates(directory):
    images = sorted(
        f for f in directory.iterdir()
        if f.suffix.lower() in ('.jpg', '.jpeg', '.png') and f.is_file()
    )
    if not images:
        return []

    print(f"Hashing {len(images)} images in {directory} ...")
    hashes = {}
    for f in images:
        try:
            img = Image.open(f)
            hashes[f] = imagehash.phash(img)
        except Exception as e:
            print(f"  SKIP {f.name}: {e}")

    print(f"Computing duplicate groups (threshold={THRESHOLD}) ...")
    visited = set()
    groups = []
    for f1, h1 in hashes.items():
        if f1 in visited:
            continue
        group = [f1]
        visited.add(f1)
        for f2, h2 in hashes.items():
            if f2 in visited:
                continue
            if h1 - h2 <= THRESHOLD:
                group.append(f2)
                visited.add(f2)
        if len(group) > 1:
            groups.append(group)

    return groups


def resolve_group(group):
    wallhaven = [f for f in group if f.name.startswith("wallhaven-")]
    if wallhaven:
        keep = wallhaven[0]
    else:
        keep = group[0]
    return keep, [f for f in group if f != keep]


def main():
    if len(sys.argv) < 2:
        directories = ["ultrawide", "vertical"]
    else:
        directories = sys.argv[1:]

    total_deleted = 0

    for dir_name in directories:
        directory = Path(dir_name)
        if not directory.is_dir():
            print(f"Skipping {dir_name}: not a directory")
            continue

        groups = find_duplicates(directory)
        if not groups:
            print(f"\n{dir_name}: no duplicates found")
            continue

        print(f"\n{dir_name}: found {len(groups)} duplicate groups")
        deleted = 0
        for group in groups:
            keep, to_delete = resolve_group(group)
            names = [f.name for f in group]
            print(f"  {'/'.join(names)} -> keeping {keep.name}")
            for f in to_delete:
                print(f"    deleting {f.name}")
                f.unlink()
                deleted += 1

        print(f"{dir_name}: deleted {deleted} duplicates")
        total_deleted += deleted

    print(f"\nTotal deleted: {total_deleted}")
    return total_deleted


if __name__ == "__main__":
    sys.exit(0 if main() == 0 else 0)
