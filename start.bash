#!/usr/bin/env bash
cd "$(dirname "$0")/src"
python repoLangs.py
python repoTops.py
