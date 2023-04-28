#!/bin/bash

python3 grobtrack.py

git add f3.poll  g4.poll  h4.poll  Na3.poll  Nh3.poll
git add f3.png  g4.png  h4.png  Na3.png  Nh3.png
git diff --staged --quiet || git commit -m "Update results"
git push origin master >& push.log
