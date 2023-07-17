import itertools
import sys

from protocards import cribbage, standard
from tabulate import tabulate

# aces are low
CRIBBAGE_RANKS = [standard.ACE] + standard.RANKS[:-1]

def breaking_input(*args, **kwargs):
  try:
    input(*args, **kwargs)
  except (EOFError, KeyboardInterrupt):
    print()
    sys.exit(0)

def get_hand_scores(hand, deck):
  min_score = 40
  max_score = 0
  ev = 0
  deck_len = len(deck)
  for card in deck:
    score = sum(cribbage.score_hand(hand, turned=card).values())
    min_score = min(min_score, score)
    max_score = max(max_score, score)
    ev += score/deck_len
  return (min_score, max_score, ev)

def yield_discard_options(hand):
  for discard in itertools.combinations(hand, 2):
     yield (standard.StandardHand(discard), standard.StandardHand(filter(lambda card: card not in discard, hand)))

def choose_discards(hand, remaining_deck):
  discards_table = []
  table_headers = ["Discard", "Remaining", "Min", "Max", "EV"]
  for discard, remaining_hand in yield_discard_options(hand):
    min_score, max_score, ev = get_hand_scores(remaining_hand, remaining_deck)
    discards_table.append([discard, remaining_hand, min_score, max_score, ev])
  # this set of sorts prioritizes ev, then max, then min
  discards_table.sort(key = lambda row: row[-3], reverse = True)
  discards_table.sort(key = lambda row: row[-2], reverse = True)
  discards_table.sort(key = lambda row: row[-1], reverse = True)
  print(tabulate(discards_table, headers = table_headers))

def test_hand():
    deck = standard.make_deck(shuffle=True)
    hand = deck.deal(6)
    hand.sort(key = lambda card: CRIBBAGE_RANKS.index(card.rank))
    keys = "abcdef"
    print(f"Your hand is:")
    for i in range(6):
      print(f"  {keys[i]}. {hand[i]}")
    breaking_input("\nConsider your options, then hit enter to see discard stats.\n")
    choose_discards(hand, deck)

def main():
  with open("intro.txt", "r") as f:
    print(f.read())
  while True:
    test_hand()
    breaking_input("\nHit enter for a new hand.\n")

if __name__ == "__main__":
    main()
