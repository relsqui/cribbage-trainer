import random
import sys

from cribbage_hand import CribbageHand, make_cribbage_deck
from evaluate import choose_discards
from tabulate import tabulate

intro = """
Welcome to the cribbage trainer. Good luck!
Send EOF (Ctrl-D) or an interrupt (Ctrl-C) at any prompt to exit.
Note that this program only considers hands and cribs -- not points in the play.
"""

def breaking_input(*args, **kwargs):
  try:
    input(*args, **kwargs)
  except (EOFError, KeyboardInterrupt):
    print()
    sys.exit(0)

def test_hand(dealer):
    deck = make_cribbage_deck(shuffle=True)
    hand = CribbageHand(deck.deal(6))
    hand.sort()
    keys = "abcdef"
    print(f"You {'are' if dealer else 'are not'} the dealer. Your hand is:")
    for i in range(6):
      print(f"  {keys[i]}. {hand[i]}")
    breaking_input("\nConsider your options, then hit enter to see discard stats.")
    discards_table = choose_discards(hand, dealer, show_progress=True)
    print()
    print(tabulate(discards_table, headers="keys"))

def crib_trainer(dealer):
  print(intro)
  while True:
    test_hand(dealer)
    breaking_input("\nHit enter for a new hand.\n")
    dealer = not dealer
