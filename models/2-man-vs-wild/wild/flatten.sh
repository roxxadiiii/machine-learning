#!/usr/bin/env bash

set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"

echo "Root directory: $ROOT"

# Step 1: Move all files to root
find "$ROOT" -mindepth 2 -type f | while IFS= read -r file; do
    base="$(basename "$file")"
    target="$ROOT/$base"

    # Handle filename conflicts
    if [[ -e "$target" ]]; then
        name="${base%.*}"
        ext="${base##*.}"
        [[ "$name" == "$ext" ]] && ext="" || ext=".$ext"

        i=1
        while [[ -e "$ROOT/${name}_$i$ext" ]]; do
            ((i++))
        done
        target="$ROOT/${name}_$i$ext"
    fi

    echo "Moving: $file -> $target"
    mv "$file" "$target"
done

echo "All files moved."

# Step 2: Delete ALL remaining subdirectories (but NOT root)
echo "Removing leftover directories..."

find "$ROOT" -mindepth 1 -type d -exec rm -rf {} +

echo "Done: flattened + cleaned."
