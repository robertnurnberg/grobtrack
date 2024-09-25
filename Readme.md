# Track eval and PV of 1. g4 on chessdb.cn

Track the evaluation and PV of 1. g4, as well as the other four (historically) non-zero
opening moves for white, on [chessdb.cn](https://chessdb.cn/queryc_en/) (cdb).

The raw polling data (e.g. [`g4.poll`](g4.poll)) are obtained with the help of the script
`cdbpvpoll.py` from [cdblib](https://github.com/robertnurnberg/cdblib).
Note that the displayed evaluations in each case are for the position _after_ the first 
move by white was made, so (a) they are positive and (b) they will 
in general differ slightly from the evaluation shown for the move in the start
position at [chessdb.cn](https://chessdb.cn/queryc_en/).

The polling data and plots are updated daily. In addition, we use 
[Stockfish](https://github.com/noobpwnftw/Stockfish)'s WDL evaluations
of cdb's PV leafs, and the positions 6 and 12 plies from the end of the PVs, to
monitor cdb's progress in exploring and evaluating 1. g4 (and the other four
moves). These evaluations are performed daily for the newly aquired polling
data, using e.g. the command `stockfish bench 1024 16 30 g4.epd depth`
for the new PV leafs in `g4.poll`, and then stored in [`g4.wdl`](wdl/g4.wdl).
The order of the data in `g4.wdl`, and the associated PVs found by Stockfish
in [`g4_sfpvs.epd`](wdl/g4_sfpvs.epd), 
[`g4m6_sfpvs.epd`](wdl/g4m6_sfpvs.epd) and
[`g4m12_sfpvs.epd`](wdl/g4m12_sfpvs.epd), respectively,
corresponds to the order in `g4.poll`.

## Quick links
* [1. g4](#1-g4)
* [1. h4](#1-h4)
* [1. Na3](#1-Na3)
* [1. Nh3](#1-Nh3)
* [1. f3](#1-f3)

<sub>
For past version changes of the cdb worker check
<a href = "https://github.com/noobpwnftw/Stockfish/commits/siever">here</a>.
<a href = "https://github.com/noobpwnftw/chessdb/commit/3d1ff4660c761193ed4479346ef11a06912ac66f">Stable</a>
PV polling in place since 2023-08-24.
</sub>

---

## 1. g4

### Rolling weekly average of cdb's eval and SF's d30 WDL
<p align="center"> <img src="images/g4rolling.png?raw=true"> </p>

### cdb's eval and PV: All time 
<p align="center"> <img src="images/g4.png?raw=true"> </p>

### cdb's eval and PV: Last 7 days 
<p align="center"> <img src="images/g4week.png?raw=true"> </p>

### cdb's eval and PV: Last 24 hours
<p align="center"> <img src="images/g4day.png?raw=true"> </p>

### SF's d30 WDL: Leafs in cdb's PVs
<p align="center"> <img src="images/g4wdl.png?raw=true"> </p>

### SF's d30 WDL: 6 plies from leafs in cdb's PVs
<p align="center"> <img src="images/g4m6wdl.png?raw=true"> </p>

### SF's d30 WDL: 12 plies from leafs in cdb's PVs
<p align="center"> <img src="images/g4m12wdl.png?raw=true"> </p>

---

## 1. h4

### Rolling weekly average of cdb's eval and SF's d30 WDL
<p align="center"> <img src="images/h4rolling.png?raw=true"> </p>

### cdb's eval and PV: All time 
<p align="center"> <img src="images/h4.png?raw=true"> </p>

### cdb's eval and PV: Last 7 days 
<p align="center"> <img src="images/h4week.png?raw=true"> </p>

### cdb's eval and PV: Last 24 hours
<p align="center"> <img src="images/h4day.png?raw=true"> </p>

### SF's d30 WDL: Leafs in cdb's PVs
<p align="center"> <img src="images/h4wdl.png?raw=true"> </p>

### SF's d30 WDL: 6 plies from leafs in cdb's PVs
<p align="center"> <img src="images/h4m6wdl.png?raw=true"> </p>

### SF's d30 WDL: 12 plies from leafs in cdb's PVs
<p align="center"> <img src="images/h4m12wdl.png?raw=true"> </p>

---

## 1. Na3

### Rolling weekly average of cdb's eval and SF's d30 WDL
<p align="center"> <img src="images/Na3rolling.png?raw=true"> </p>

### cdb's eval and PV: All time 
<p align="center"> <img src="images/Na3.png?raw=true"> </p>

### cdb's eval and PV: Last 7 days 
<p align="center"> <img src="images/Na3week.png?raw=true"> </p>

### cdb's eval and PV: Last 24 hours
<p align="center"> <img src="images/Na3day.png?raw=true"> </p>

### SF's d30 WDL: Leafs in cdb's PVs
<p align="center"> <img src="images/Na3wdl.png?raw=true"> </p>

### SF's d30 WDL: 6 plies from leafs in cdb's PVs
<p align="center"> <img src="images/Na3m6wdl.png?raw=true"> </p>

### SF's d30 WDL: 12 plies from leafs in cdb's PVs
<p align="center"> <img src="images/Na3m12wdl.png?raw=true"> </p>

---

## 1. Nh3

### Rolling weekly average of cdb's eval and SF's d30 WDL
<p align="center"> <img src="images/Nh3rolling.png?raw=true"> </p>

### cdb's eval and PV: All time 
<p align="center"> <img src="images/Nh3.png?raw=true"> </p>

### cdb's eval and PV: Last 7 days 
<p align="center"> <img src="images/Nh3week.png?raw=true"> </p>

### cdb's eval and PV: Last 24 hours
<p align="center"> <img src="images/Nh3day.png?raw=true"> </p>

### SF's d30 WDL: Leafs in cdb's PVs
<p align="center"> <img src="images/Nh3wdl.png?raw=true"> </p>

### SF's d30 WDL: 6 plies from leafs in cdb's PVs
<p align="center"> <img src="images/Nh3m6wdl.png?raw=true"> </p>

### SF's d30 WDL: 12 plies from leafs in cdb's PVs
<p align="center"> <img src="images/Nh3m12wdl.png?raw=true"> </p>

---

## 1. f3

### Rolling weekly average of cdb's eval and SF's d30 WDL
<p align="center"> <img src="images/f3rolling.png?raw=true"> </p>

### cdb's eval and PV: All time 
<p align="center"> <img src="images/f3.png?raw=true"> </p>

### cdb's eval and PV: Last 7 days 
<p align="center"> <img src="images/f3week.png?raw=true"> </p>

### cdb's eval and PV: Last 24 hours
<p align="center"> <img src="images/f3day.png?raw=true"> </p>

### SF's d30 WDL: Leafs in cdb's PVs
<p align="center"> <img src="images/f3wdl.png?raw=true"> </p>

### SF's d30 WDL: 6 plies from leafs in cdb's PVs
<p align="center"> <img src="images/f3m6wdl.png?raw=true"> </p>

### SF's d30 WDL: 12 plies from leafs in cdb's PVs
<p align="center"> <img src="images/f3m12wdl.png?raw=true"> </p>

---

