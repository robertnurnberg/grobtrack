#!/bin/bash

# we exit immediately if any command exits with a non-zero status
set -e

echo "started at: " `date`

# clone SF if needed
if [[ ! -e Stockfish ]]; then
   git clone https://github.com/official-stockfish/Stockfish.git
fi

# check for new commits and pull if needed
cd Stockfish/src
git checkout master >& checkout.log
git fetch origin >& fetch.log
reslog=$(git log HEAD..origin/master --oneline)
if [[ "${reslog}" != "" ]]; then
  echo "Merging new commits and making clean ... "
  git merge origin/master >& merge.log 
  make clean >& clean.log
fi

# re-compile SF if freshly cloned or new commits were pulled
if [[ ! -e stockfish ]]; then
  echo "Make a new profile-build ... "
  make -j ARCH=x86-64-modern profile-build >& make.log
fi
cd ../../wdl

for m in g4 h4 Na3 Nh3 f3
do
  echo "Analysing the cdb PVs for the move 1. $m ... "
  if [[ "$m" == "g4" ]]; then
    uci=g2g4
  elif [[ "$m" == "h4" ]]; then
    uci=h2h4
  elif [[ "$m" == "Na3" ]]; then
    uci=b1a3
  elif [[ "$m" == "Nh3" ]]; then
    uci=g1h3
  else
    uci=f2f3
  fi
  pvs=`cat ../"$m".poll | sed '/^$/d' | wc -l`
  # first we analyse the PVs' leaf positions, as needed
  if [[ ! -e "$m".wdl ]]; then
    wdls=0
  else
    wdls=`cat "$m".wdl | wc -l`
  fi
  echo "Found $pvs PVs in the polling data, and $wdls computed leaf wdl values."
  wdls=$((pvs-wdls))
  if [[ $wdls -gt 0 ]]; then
    echo "Computing the missing $wdls wdl values ..."
    cat ../"$m".poll | sed '/^$/d' | cut -d'-' -f5- | cut -c2- | tail -n $wdls | awk -v uci="$uci" '{print "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 moves",uci,$0}' > "$m".epd
    printf "setoption name UCI_ShowWDL value true\nbench 1024 16 28 %s.epd depth NNUE\n" "$m" | ../Stockfish/src/stockfish >& "$m"_sf.out
    # save WDL output forever
    cat "$m"_sf.out | grep -B1 bestmove | grep -o 'wdl [0-9 ]* ' | sed 's/wdl //' >> "$m".wdl
    # save SF's last depth PV forever
    cat "$m"_sf.out | grep -B1 bestmove | grep -o ' pv [a-z0-9 ]*' | sed 's/pv//' > "$m".pvs && paste -d "" "$m".epd "$m".pvs >> "$m"_sfpvs.epd
  fi
  # then we analyse the PVs' positions 6 plies from the leafs, as needed
  if [[ ! -e "$m"m6.wdl ]]; then
    wdls=0
  else
    wdls=`cat "$m"m6.wdl | wc -l`
  fi
  echo "Found $pvs PVs in the polling data, and $wdls computed (leaf - 6ply) wdl values."
  wdls=$((pvs-wdls))
  if [[ $wdls -gt 0 ]]; then
    echo "Computing the missing $wdls wdl m6 values ..."
    cat ../"$m".poll | sed '/^$/d' | cut -d'-' -f5- | cut -c2- | awk '{for(i=1;i<=NF-6;i++) {printf(" %s",$i)}; printf("\n")}' | tail -n $wdls | awk -v uci="$uci" '{print "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 moves",uci,$0}' > "$m"m6.epd
    printf "setoption name UCI_ShowWDL value true\nbench 1024 16 28 %sm6.epd depth NNUE\n" "$m" | ../Stockfish/src/stockfish >& "$m"m6_sf.out
    # save WDL output forever
    cat "$m"m6_sf.out | grep -B1 bestmove | grep -o 'wdl [0-9 ]* ' | sed 's/wdl //' >> "$m"m6.wdl
    # save SF's last depth PV forever
    cat "$m"m6_sf.out | grep -B1 bestmove | grep -o ' pv [a-z0-9 ]*' | sed 's/pv//' > "$m"m6.pvs && paste -d "" "$m"m6.epd "$m"m6.pvs >> "$m"m6_sfpvs.epd
  fi
done

cd ..

python3 plotwdl.py

for m in g4 h4 Na3 Nh3 f3
do
  git add images/"$m"wdl.png images/"$m"m6wdl.png
  git add wdl/"$m".wdl wdl/"$m"m6.wdl wdl/"$m"_sfpvs.epd wdl/"$m"m6_sfpvs.epd
done

git diff --staged --quiet || git commit -m "update wdl data and plots"
git push origin main >& pushwdl.log

echo "wdl stuff ended at: " `date`

if [[ $wdls -gt 0 ]]; then
  echo "Finally, starting shallow cdbsearches along all of SF's newly found PVs ..."
  cd wdl
  echo -n "" > cdbbulk.epd
  for m in g4 h4 Na3 Nh3 f3
  do
    tail "$m"_sfpvs.epd -n "$wdls" >> cdbbulk.epd
    tail "$m"m6_sfpvs.epd -n "$wdls" >> cdbbulk.epd
  done

  python3 ../../cdbexplore/cdbbulksearch.py cdbbulk.epd --shuffle --bulkConcurrency 48 --concurrency 64 --depthLimit 1 --evalDecay 0 --user rob >& cdbbulk.log

  cd ..
  echo "ended at: " `date`
fi
