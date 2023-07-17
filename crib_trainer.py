import random
import sys

from evaluate import choose_discards
from protocards import standard
from tabulate import tabulate

# aces are low
CRIBBAGE_RANKS = [standard.ACE] + standard.RANKS[:-1]

def breaking_input(*args, **kwargs):
  try:
    input(*args, **kwargs)
  except (EOFError, KeyboardInterrupt):
    print()
    sys.exit(0)

def test_hand(dealer):
    deck = standard.make_deck(shuffle=True)
    hand = deck.deal(6)
    hand.sort(key = lambda card: CRIBBAGE_RANKS.index(card.rank))
    keys = "abcdef"
    print(f"You {'are' if dealer else 'are not'} the dealer. Your hand is:")
    for i in range(6):
      print(f"  {keys[i]}. {hand[i]}")
    breaking_input("\nConsider your options, then hit enter to see discard stats.\n")
    discards_table = choose_discards(hand, deck, dealer)
    print(tabulate(discards_table, headers="keys"))

def crib_trainer():
  with open("intro.txt", "r") as f:
    print(f.read())
  dealer = random.randrange(1) == 0
  while True:
    dealer = not dealer
    test_hand(dealer)
    breaking_input("\nHit enter for a new hand.\n")
