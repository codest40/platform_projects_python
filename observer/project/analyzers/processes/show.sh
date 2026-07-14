#!/usr/bin/env bash

set -euo pipefail
EXTENSIONS=("" ".py" ".sh" ".js" ".ts" ".go" ".rs" ".c" ".cpp" ".h" ".hpp")

for arg in "$@"; do
    found=""

    if [[ -f "$arg" ]]; then
        found="$arg"
    else
        for ext in "${EXTENSIONS[@]}"; do
            if [[ -f "${arg}${ext}" ]]; then
                found="${arg}${ext}"
                break
            fi
        done
    fi

    if [[ -n "$found" ]]; then
        echo
        echo "================================================================================"
        echo "                              FILE: $found"
        echo "================================================================================"
        cat "$found"
    else
        echo "❌ File not found: $arg" >&2
    fi
done
