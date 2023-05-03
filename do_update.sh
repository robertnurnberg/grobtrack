#!/bin/bash

python3 grobtrack.py

git add f3.poll g4.poll h4.poll Na3.poll Nh3.poll
git add f3.png g4.png h4.png Na3.png Nh3.png
git add f3week.png g4week.png h4week.png Na3week.png Nh3week.png
git add f3day.png g4day.png h4day.png Na3day.png Nh3day.png
git diff --staged --quiet || git commit -m "update poll data and plots"
git push origin main >& push.log
