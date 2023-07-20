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

In situations where those things are important (say, when you only need four points to win the game), this script's hand evaluations won't be as helpful.

### Speed and storage

Because it's exhaustively calculating a lot of possibilities, the script is slow, especially the first few times you run it. It caches results in `~/.cribbage-trainer-cache` so it gets faster over time, at the cost of storage in that directory.

To speed up future usage, run the script with `--fill-cache` to pre-fill the cache. You can interrupt this and restart at any time, it won't recalculate anything already cached.

To sacrifice the speed increase and get the storage back, delete the cache directory.

## Usage

### Installation

Install requirements like so:

```
python -m pip install -r requirements.txt
```

### Summary

```
$ python main.py --help
Usage: main.py [OPTIONS] [HAND]...

  Find more details at: https://github.com/relsqui/cribbage-trainer

  If you provide a string describing a cribbage hand, this program prints the
  table of expected values for each possible discard (assuming the opponent is
  dealer; use --dealer to override). Describe hands using a letter or number
  for each rank (A2..9TJQK). Adding a suit letter (cdhs) after any group of
  ranks is optional (arbitrary suits will be assigned if you omit them). The
  case and order of cards doesn't otherwise matter.

  If no hand is given, generates random cribbage hands and shows the expected
  value table for each hand after a pause to let you think about it.

  Both of these are slow because they evaluate many options. You can pre-fill
  the cache and make future usage faster by running with --fill-cache. (This
  is safe to interrupt and resume at any time, it will by definition skip
  anything already cached.)

Options:
  --dealer      If set, hand will be checked as if the player is the dealer.
                Otherwise, opponent will be dealer.
  --fill-cache  Non-interactively evaluate hands to fill the score cache. This
                makes other queries faster.
  --help        Show this message and exit.
```

### Get advice about a specific hand

Specify a hand on the command line to get stats about what you could have cribbed. Include the rank of each card as a number, J, Q, K, or A, and optionally the suit for a card or group of cards as C, D, H or S after the rank(s). (Both can also be lowercase.)

The script will assign arbitrary suits to any cards where you didn't specify them, distributing them carefully to avoid creating a flush.

All of these are valid inputs that could describe the same hand:
* A8s 56Qc Kd (all suits specified)
* 56QCA8KD (all suits specified without spaces)
* aSq6k58 (unsorted, only the ace's suit specified)
* a8k 56qc (the space separates specified and unspecified suits)


```
$ python main.py a568qk
I interpreted that hand as: A 5 6 8 Q K
Assigning arbitrary suits: Ac 5d 6h 8s Qc Kd
Evaluating 15 possibilities ...............
I would have cribbed: Ac 8s. Full stats:

Discard    Remaining      H Min    H Max     H EV    C Min    C Max      C EV    Min    Max         EV
---------  -----------  -------  -------  -------  -------  -------  --------  -----  -----  ---------
Ac 8s      5d 6h Qc Kd        4       10  6.52174      -18       -2  -4.20085    -14      8   2.32089
Ac 6h      5d 8s Qc Kd        4       10  6            -16       -2  -4.34728    -12      8   1.65272
Qc Kd      Ac 5d 6h 8s        4        8  5.30435      -20       -4  -4.04341    -16      4   1.26094
8s Kd      Ac 5d 6h Qc        2        9  4.78261      -14       -2  -3.60914    -12      7   1.17347
6h 8s      Ac 5d Qc Kd        4       10  6.17391      -24       -5  -5.04007    -20      5   1.13384
8s Qc      Ac 5d 6h Kd        2        9  4.78261      -14       -2  -3.72044    -12      7   1.06217
Ac Kd      5d 6h 8s Qc        2        8  4.69565      -14       -2  -3.83195    -12      6   0.8637
Ac Qc      5d 6h 8s Kd        2        8  4.69565      -17       -2  -4.00515    -15      6   0.690503
6h Kd      Ac 5d 8s Qc        2        6  4.21739      -16       -2  -3.67393    -14      4   0.543461
6h Qc      Ac 5d 8s Kd        2        6  4.21739      -16       -2  -3.78523    -14      4   0.432157
5d Kd      Ac 6h 8s Qc        2        7  3.82609      -28       -6  -7.14285    -26      1  -3.31676
5d Qc      Ac 6h 8s Kd        2        7  3.82609      -28       -6  -7.19226    -26      1  -3.36617
Ac 5d      6h 8s Qc Kd        0        5  1.78261      -20       -2  -5.84471    -20      3  -4.0621
5d 8s      Ac 6h Qc Kd        0        4  1.69565      -20       -2  -5.86309    -20      2  -4.16743
5d 6h      Ac 8s Qc Kd        0        4  1.69565      -24       -5  -7.30708    -24     -1  -5.61142
```

### Train on random cribbage hands

Call the script with no argument to practice discards.

```
$ python main.py

Welcome to the cribbage trainer. Good luck!
Send EOF (Ctrl-D) or an interrupt (Ctrl-C) at any prompt to exit.
Note that this program only considers hands and cribs -- not points in the play.

You are not the dealer. Your hand is:
  Two of Spades
  Seven of Spades
  Seven of Diamonds
  Nine of Spades
  Ten of Diamonds
  King of Diamonds

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
