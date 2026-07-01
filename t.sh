#!/bin/bash

find . -mindepth 1 -print0 |
while IFS= read -r -d '' a; do
    case "$a" in
        *json*|*data*|*html*|*css*|*.git*|*t.sh*|*tt*)
            continue
            ;;
    esac

    if [[ -f "$a" ]]; then
        rm "$a"
        echo "Removed file: $a"
    elif [[ -d "$a" ]]; then
        rm -rf "$a"
        echo "Removed directory: $a"
    fi
done
