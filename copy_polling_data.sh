#!/bin/bash

for m in g4 h4 Na3 Nh3 f3; do
    mv polling/"$m".poll _tmp_"$m".poll
    sed '/^$/d' _tmp_"$m".poll >>"$m".poll
    rm _tmp_"$m".poll
done
