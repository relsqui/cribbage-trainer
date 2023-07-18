# Cribbage Trainer

This is a little utility for helping me test my intuition about which cards to discard from a cribbage hand by calculating the expected value of every option.

Currently it only looks at the cards you'll have left in your hand after discarding and what the possible turn cards are. It ignores cribs and your opponent's choices.

Install requirements like so:

```
python -m pip install -r requirements.txt
```
## Train on random cribbage hands

Call the script with no argument to practice discards.

```
$ python main.py
Welcome to the cribbage trainer! Send EOF (Ctrl-D) or an interrupt (Ctrl-C) at any prompt to exit.

Note that this program only considers the score of the hand right now -- not the crib or the play. Good luck!

Your hand is:
  a. Two of Hearts
  b. Seven of Spades
  c. Ten of Spades
  d. King of Spades
  e. King of Diamonds
  f. King of Hearts

Consider your options, then hit enter to see discard stats.

Discard    Remaining      Min    Max       EV
---------  -----------  -----  -----  -------
T7s        Ks K2h Kd        6     12  7.30435
7s 2h      KTs Kh Kd        6     14  6.95652
Ts 2h      K7s Kh Kd        6     12  6.95652
KTs        7s K2h Kd        2      6  3.3913
Ts Kd      K7s K2h          2      6  3.3913
Ts Kh      K7s 2h Kd        2      6  3.3913
K7s        Ts K2h Kd        2      8  3.3913
7s Kd      KTs K2h          2      8  3.3913
7s Kh      KTs 2h Kd        2      8  3.3913
Ks 2h      T7s Kh Kd        2      8  3.04348
2h Kd      KT7s Kh          2      8  3.04348
K2h        KT7s Kd          2      8  3.04348
Ks Kd      T7s K2h          0      4  1.47826
Ks Kh      T7s 2h Kd        0      4  1.47826
Kh Kd      KT7s 2h          0      4  1.47826

Hit enter for a new hand.
```

## Get advice about a specific hand

Specify a hand on the command line to get stats about what you could have cribbed. Include the rank of each card as a number, J, Q, K, or A, and optionally the suit for a card or group of cards as C, D, H or S after the rank(s). (Both can also be lowercase.)

All of these are valid inputs that could describe the same hand:
* A8s 56Qc Kd (all suits specified)
* 56QCA8KD (all suits specified without spaces)
* aSq6k58 (unsorted, only the ace's suit specified)
* a8k 56qc (the space separates specified and unspecified suits)


```
$ python main.py a568qk
I interpreted that hand as: A 5 6 8 Q K
I would have cribbed: A 8. Full stats:

Discard    Remaining      Min    Max       EV
---------  -----------  -----  -----  -------
A 8        5 6 Q K          4     10  6.53846
6 8        A 5 Q K          4     10  6.23077
A 6        5 8 Q K          4     10  6.07692
Q K        A 5 6 8          4      8  5.30769
8 Q        A 5 6 K          2      9  4.76923
8 K        A 5 6 Q          2      9  4.76923
A Q        5 6 8 K          2      8  4.69231
A K        5 6 8 Q          2      8  4.69231
6 Q        A 5 8 K          2      6  4.30769
6 K        A 5 8 Q          2      6  4.30769
5 K        A 6 8 Q          2      7  3.92308
5 Q        A 6 8 K          2      7  3.92308
A 5        6 8 Q K          0      5  1.84615
5 6        A 8 Q K          0      4  1.76923
5 8        A 6 Q K          0      4  1.76923
```
