#!/bin/bash

python3 grobtrack.py

for m in g4 h4 Na3 Nh3 f3
do
  git add "$m".poll
  git add images/"$m".png images/"$m"week.png images/"$m"day.png 
done

git diff --staged --quiet || git commit -m "update poll data and plots"
git push origin main >& push.log

./do_sfwdl.sh >& sfwdl.log
