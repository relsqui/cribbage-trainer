# Cribbage Trainer

This is a little utility for helping me test my intuition about which cards to discard from a cribbage hand, by calculating the expected value of every option.

Install requirements and run it with:

```
python -m pip install -r requirements.txt
python main.py
```

Example output:

```
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