#!/bin/bash

python3 grobtrack.py

git add f3.poll g4.poll h4.poll Na3.poll Nh3.poll
git add images/f3.png images/g4.png images/h4.png images/Na3.png images/Nh3.png
git add images/f3week.png images/g4week.png images/h4week.png images/Na3week.png images/Nh3week.png
git add images/f3day.png images/g4day.png images/h4day.png images/Na3day.png images/Nh3day.png
git diff --staged --quiet || git commit -m "update poll data and plots"
git push origin main >& push.log
