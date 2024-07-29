#!/bin/bash
for file in /home/sanna/demo/populate/*.py; do
    python3 "$file"
done
