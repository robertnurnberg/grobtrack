#!/bin/bash

for m in g4 h4 Na3 Nh3 f3
do
  sed '/error/d' ./polling/"$m".poll > "$m".poll
done
