#!/usr/bin/env bash

for i in {1..5}; do
    bash -c '
        ulimit -n 50
        python3 t.py
    '
    sleep 2
done

echo "Done"
