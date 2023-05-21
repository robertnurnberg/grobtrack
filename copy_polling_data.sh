#!/bin/bash

for f in g4.poll h4.poll Na3.poll Nh3.poll f3.poll 
do
 sed '/error/d' ./polling/"$f" > "$f"
done
