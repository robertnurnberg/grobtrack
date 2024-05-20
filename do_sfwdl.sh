#!/bin/bash

# we exit immediately if any command exits with a non-zero status
set -e

if [[ ! -e wdl ]]; then
    mkdir wdl
fi

echo "started at: " $(date)

# clone noob's SF fork if needed
if [[ ! -e Stockfish ]]; then
    git clone https://github.com/noobpwnftw/Stockfish.git
fi

# check for new commits and pull if needed
cd Stockfish/src
git checkout master >&checkout.log
git fetch origin >&fetch.log
reslog=$(git log HEAD..origin/master --oneline)
if [[ "${reslog}" != "" ]]; then
    echo "Merging new commits and making clean ... "
    git merge origin/master >&merge.log
    make clean >&clean.log
fi

# re-compile SF if freshly cloned or new commits were pulled
if [[ ! -e stockfish ]]; then
    echo "Make a new profile-build ... "
    CXXFLAGS='-march=native' make -j ARCH=x86-64-avxvnni profile-build >&make.log
fi
sfversion=$(./stockfish quit | sed "s/Stockfish //" | sed "s/ by.*//")
bench="1024 16 30"
echo "Will use \"bench $bench .epd depth NNUE\" w/ sf $sfversion."
cd ../../wdl

for m in g4 h4 Na3 Nh3 f3; do
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
    pvs=$(cat ../"$m".poll | sed '/^$/d' | wc -l)
    # we now analyse the PVs' leaf positions, and 6/12 plies from leafs
    for ply in 0 6 12; do
        if [[ $ply == 0 ]]; then
            fname="$m"
        else
            fname="$m"m"$ply"
        fi
        if [[ ! -e "$fname".wdl ]]; then
            wdls=0
        else
            wdls=$(cat "$fname".wdl | wc -l)
        fi
        echo "Found $pvs PVs in the polling data, and $wdls computed (leaf - $ply ply) wdl values."
        wdls=$((pvs - wdls))
        if [[ $wdls -gt 0 ]]; then
            echo "Computing the missing $wdls wdl values ..."
            cat ../"$m".poll | sed '/^$/d' | cut -d'-' -f5- | cut -c2- | awk -v ply="$ply" '{for(i=1;i<=NF-ply;i++) {printf(" %s",$i)}; printf("\n")}' | tail -n $wdls | awk -v uci="$uci" '{print "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 moves",uci,$0}' >"$fname".epd
            printf "setoption name UCI_ShowWDL value true\nbench %s %s.epd depth NNUE\n" "$bench" "$fname" | ../Stockfish/src/stockfish >&"$fname"_sf.out
            # save WDL output forever
            cat "$fname"_sf.out | grep -B1 bestmove | grep -o 'wdl [0-9 ]* ' | sed 's/wdl //' | sed 's/$/   /' | sed 's/.\{11\}/& # bench '"$bench"' .epd depth NNUE w\/ sf '"$sfversion"'/' | sed 's/ *$//' >>"$fname".wdl
            # save SF's last depth PV forever
            cat "$fname"_sf.out | grep -B1 bestmove | grep -o ' pv [a-z0-9 ]*' | sed 's/pv//' >"$fname".pvs && paste -d "" "$fname".epd "$fname".pvs >>"$fname"_sfpvs.epd
            # save SF's scores for 24h
            cat "$fname"_sf.out | grep -B1 bestmove | grep -o ' score [a-z0-9 -]*' | sed 's/wdl.*pv/pv/' >"$fname".pvs && paste -d "" "$fname".epd "$fname".pvs >"$fname"_sfscores.epd
        fi
    done
done

cd ..

python3 plotwdl.py
python3 plotrolling.py

for m in g4 h4 Na3 Nh3 f3; do
    git add images/"$m"wdl.png images/"$m"m6wdl.png images/"$m"m12wdl.png images/"$m"rolling.png
    git add wdl/"$m".wdl wdl/"$m"m6.wdl wdl/"$m"m12.wdl
    git add wdl/"$m"_sfpvs.epd wdl/"$m"m6_sfpvs.epd wdl/"$m"m12_sfpvs.epd
done

git diff --staged --quiet || git commit -m "update wdl data and plots"
git push origin main >&pushwdl.log

echo "wdl stuff ended at: " $(date)

if [[ $wdls -gt 0 ]]; then
    echo "Finally, starting shallow cdbsearches along all of SF's newly found PVs ..."
    cd wdl
    echo -n "" >cdbbulk.epd
    for m in g4 h4 Na3 Nh3 f3; do
        tail "$m"_sfpvs.epd -n "$wdls" >>cdbbulk.epd
        tail "$m"m6_sfpvs.epd -n "$wdls" >>cdbbulk.epd
        tail "$m"m12_sfpvs.epd -n "$wdls" >>cdbbulk.epd
    done

    #  python3 ../../cdbexplore/cdbbulksearch.py cdbbulk.epd --plyBegin -28 --shuffle --bulkConcurrency 48 --concurrency 24 --depthLimit 2 --evalDecay 2 --user rob >& cdbbulk.log
    python3 ../../cdbexplore/cdbbulksearch.py cdbbulk.epd --plyBegin -30 --shuffle --bulkConcurrency 16 --depthLimit 1 --user rob >&cdbbulk.log

    cd ..
    echo "ended at: " $(date)
fi
