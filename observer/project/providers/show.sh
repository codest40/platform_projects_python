#!/usr/bin/env bash

set -euo pipefail

EXTENSIONS=(
    ".py"
    ".sh"
    ".js"
    ".ts"
    ".go"
    ".rs"
    ".c"
    ".cpp"
    ".h"
    ".hpp"
)

show_file() {
    local file="$1"

    echo
    echo "================================================================================"
    echo "                              FILE: ${file#./}"
    echo "================================================================================"
    cat "$file"
}

recursive=false

if [[ "${*: -1}" == "all" ]]; then
    recursive=true
    set -- "${@:1:$(($#-1))}"
fi

for arg in "$@"; do

    #
    # Extension mode
    #

    if [[ ! "$arg" =~ ^\. ]]; then
        ext=".$arg"
    else
        ext="$arg"
    fi

    for known in "${EXTENSIONS[@]}"; do
        if [[ "$ext" == "$known" ]]; then

            if $recursive; then
                while IFS= read -r file; do
                    show_file "$file"
                done < <(find . -type f -name "*$ext" | sort)
            else
                while IFS= read -r file; do
                    show_file "$file"
                done < <(find . -maxdepth 1 -type f -name "*$ext" | sort)
            fi

            continue 2
        fi
    done

    #
    # Existing filename mode
    #

    found=""

    if [[ -f "$arg" ]]; then
        found="$arg"
    else
        for ext in "" "${EXTENSIONS[@]}"; do
            if [[ -f "${arg}${ext}" ]]; then
                found="${arg}${ext}"
                break
            fi
        done
    fi

    if [[ -n "$found" ]]; then
        show_file "$found"
    else
        echo "❌ File not found: $arg" >&2
    fi

done
