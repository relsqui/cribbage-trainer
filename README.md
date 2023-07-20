# Cribbage Trainer

## Purpose and limitations

This is a little utility for helping me test my intuition about which cards to discard from a cribbage hand by calculating the expected value of every option.

### Accuracy

This script considers:
* The cards remaining in your hand
* Possible turn cards
* Possible cribs
* Who's dealing

It does not consider:
* Points you could score in the play
* How likely your opponent is to crib one card vs. another
* The score

So its expected values for subtler real-life situations will be wrong.

### Speed and storage

Because it's exhaustively checking a lot of possibilities, the script is slow, especially the first few times you run it. It caches results in `~/.cribbage-trainer-cache` so it gets faster over time, at the cost of storage in that directory. Feel free to delete the cache at any time to trade back the speed for the storage.

## Usage

### Installation

Install requirements like so:

```
python -m pip install -r requirements.txt
```

### Get advice about a specific hand

Specify a hand on the command line to get stats about what you could have cribbed. Include the rank of each card as a number, J, Q, K, or A, and optionally the suit for a card or group of cards as C, D, H or S after the rank(s). (Both can also be lowercase.)

All of these are valid inputs that could describe the same hand:
* A8s 56Qc Kd (all suits specified)
* 56QCA8KD (all suits specified without spaces)
* aSq6k58 (unsorted, only the ace's suit specified)
* a8k 56qc (the space separates specified and unspecified suits)


```
$ python main.py a568qk
I interpreted that hand as: A 5 6 8 Q K
Evaluating 15 possibilities ...............
I would have cribbed: A 8. Full stats:

Discard    Remaining      H Min    H Max     H EV    C Min    C Max      C EV    Min    Max         EV
---------  -----------  -------  -------  -------  -------  -------  --------  -----  -----  ---------
A 8        5 6 Q K            4       10  6.53846      -18        0  -4.23059    -14     10   2.30787
A 6        5 8 Q K            4       10  6.07692      -16        0  -4.3971     -12     10   1.67982
Q K        A 5 6 8            4        8  5.30769      -20        0  -4.10552    -16      8   1.20217
6 8        A 5 Q K            4       10  6.23077      -24        0  -5.04851    -20     10   1.18226
8 K        A 5 6 Q            2        9  4.76923      -14        0  -3.65104    -12      9   1.11819
8 Q        A 5 6 K            2        9  4.76923      -14        0  -3.75385    -12      9   1.01538
A K        5 6 8 Q            2        8  4.69231      -14        0  -3.87186    -12      8   0.820452
A Q        5 6 8 K            2        8  4.69231      -14        0  -3.97466    -12      8   0.717647
6 K        A 5 8 Q            2        6  4.30769      -16        0  -3.73538    -14      6   0.572308
6 Q        A 5 8 K            2        6  4.30769      -16        0  -3.83819    -14      6   0.469502
5 K        A 6 8 Q            2        7  3.92308      -28       -2  -7.15475    -26      5  -3.23167
5 Q        A 6 8 K            2        7  3.92308      -28       -2  -7.25756    -26      5  -3.33448
A 5        6 8 Q K            0        5  1.84615      -20       -2  -5.86787    -20      3  -4.02172
5 8        A 6 Q K            0        4  1.76923      -20       -2  -5.8686     -20      2  -4.09937
5 6        A 8 Q K            0        4  1.76923      -24       -2  -7.28036    -24      2  -5.51113
```

### Train on random cribbage hands

Call the script with no argument to practice discards.

```
$ python main.py

Welcome to the cribbage trainer. Good luck!
Send EOF (Ctrl-D) or an interrupt (Ctrl-C) at any prompt to exit.
Note that this program only considers hands and cribs -- not points in the play.

You are not the dealer. Your hand is:
  a. Two of Spades
  b. Seven of Spades
  c. Seven of Diamonds
  d. Nine of Spades
  e. Ten of Diamonds
  f. King of Diamonds

Consider your options, then hit enter to see discard stats.
Evaluating 15 possibilities ...............

Discard    Remaining      H Min    H Max     H EV    C Min    C Max      C EV    Min    Max          EV
---------  -----------  -------  -------  -------  -------  -------  --------  -----  -----  ----------
Td Kd      2s 7s 7d 9s        2       12  4.17391      -20        0  -3.62398    -18     12   0.549934
2s Kd      7s 7d 9s Td        2       14  4.26087      -14        0  -4.10791    -12     14   0.152964
9s Kd      2s 7s 7d Td        2        6  3.65217      -14        0  -3.63043    -12      6   0.0217391
2s Td      7s 7d 9s Kd        2       12  3.82609      -14        0  -4.30079    -12     12  -0.474704
2s 9s      7s 7d Td Kd        2        6  3.30435      -20        0  -4.35494    -18      6  -1.05059
7s Kd      2s 7d 9s Td        0        6  2.13043      -14        0  -3.65507    -14      6  -1.52464
9s Td      2s 7s 7d Kd        2        6  3.65217      -17        0  -5.1859     -15      6  -1.53373
7d Kd      2s 7s 9s Td        0        6  2.13043      -15        0  -3.6946     -15      6  -1.56416
7s Td      2s 7d 9s Kd        0        5  1.78261      -14        0  -3.79025    -14      5  -2.00764
7d Td      2s 7s 9s Kd        0        5  1.78261      -15        0  -3.82978    -15      5  -2.04717
2s 7d      7s 9s Td Kd        0        6  1.78261      -16        0  -4.43426    -16      6  -2.65165
2s 7s      7d 9s Td Kd        0        6  1.78261      -16        0  -4.47378    -16      6  -2.69117
7d 9s      2s 7s Td Kd        0        4  1.52174      -24        0  -4.46179    -24      4  -2.94005
7s 9s      2s 7d Td Kd        0        4  1.52174      -24        0  -4.50132    -24      4  -2.97958
7s 7d      2s 9s Td Kd        0        4  2.08696      -24       -2  -6.3863     -24      2  -4.29934

Hit enter for a new hand.
```
