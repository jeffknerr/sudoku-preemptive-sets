# sudoku-preemptive-sets
solve sudoku puzzles using preemptive sets

Trying to follow the paper
["A pencil-and-paper algorithm for solving Sudoku puzzles"](http://www.ams.org/notices/200904/rtx090400460p.pdf)
by J.F. Crook (April 2009,
Notices of the American Mathematical Society 56(4))
 
Basic algorithm so far:

- find all forced numbers
- create the puzzle markup
- repeat until solved:
  * find all preemptive sets
  * use preemptive sets to filter numbers in the markups
  * look for singletons


# example

Still very rough, but can solve *easy* puzzles where
all numbers are "forced", as well as the 
"Beware! Very Challenging Shortz301" puzzle where
preemptive sets are used.

```
$ python3 puzzle.py
-------------------
| :3:9|5: : | : : :
| : : |8: : | :7: :
| : : | :1: |9: :4:
-------------------
|1: : |4: : | : :3:
| : : | : : | : : :
| : :7| : : |8:6: :
-------------------
| : :6|7: :8|2: : :
| :1: | :9: | : :5:
| : : | : :1| : :8:
-------------------

finding forced numbers...looking for 1s
FOUND: 1 in (1, 2)
finding forced numbers...looking for 2s
finding forced numbers...looking for 3s
finding forced numbers...looking for 4s
...
...
creating puzzle markup...
----------------------------------------------------------------------------------------------------
   [24678]        []        [] ||        []    [2467]    [2467] ||      [16]     [128]     [126] ||
    [2456]    [2456]        [] ||        []    [2346]        [] ||     [356]        []      [26] ||
   [25678]   [25678]     [258] ||     [236]        []    [2367] ||        []    [2358]        [] ||
----------------------------------------------------------------------------------------------------
        []   [25689]     [258] ||        []   [25678]    [2567] ||      [57]     [259]        [] ||
 [2345689]  [245689]   [23458] ||   [12369]  [235678]   [23567] ||    [1457]   [12459]    [1279] ||
   [23459]    [2459]        [] ||    [1239]     [235]     [235] ||        []        []     [129] ||
----------------------------------------------------------------------------------------------------
    [3459]     [459]        [] ||        []     [345]        [] ||        []    [1349]      [19] ||
   [23478]        []    [2348] ||     [236]        []    [2346] ||    [3467]      [34]        [] ||
  [234579]   [24579]    [2345] ||     [236]   [23456]        [] ||    [3467]     [349]        [] ||
----------------------------------------------------------------------------------------------------
finding preemptive sets...
current preemptive sets:
size: 3  type: box
(0,6): 16 (1,8): 26 (0,8): 126
size: 3  type: col
(7,3): 236 (8,3): 236 (2,3): 236
size: 4  type: box
(6,8): 19 (7,7): 34 (8,7): 349 (6,7): 1349
...
...
-------------------
|6:3:9|5:7:4|1:8:2:
|5:4:1|8:2:9|3:7:6:
|7:8:2|6:1:3|9:5:4:
-------------------
|1:9:8|4:6:7|5:2:3:
|3:6:5|9:8:2|4:1:7:
|4:2:7|1:3:5|8:6:9:
-------------------
|9:5:6|7:4:8|2:3:1:
|8:1:3|2:9:6|7:4:5:
|2:7:4|3:5:1|6:9:8:
-------------------

```
