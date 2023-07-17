import itertools

from cribbage_hand import CribbageHand
from protocards import cribbage, standard

def get_hand_scores(hand, deck, dealer):
  min_score = 40
  max_score = 0
  ev = 0
  deck_len = len(deck)
  for card in deck:
    score = sum(cribbage.score_hand(hand, turned=card, dealer=dealer).values())
    min_score = min(min_score, score)
    max_score = max(max_score, score)
    ev += score/deck_len
  return {
    "Min": min_score,
    "Max": max_score,
    "EV": ev
  }

def yield_discard_options(hand):
  for discard in itertools.combinations(hand, 2):
     yield {
       "Discard": CribbageHand(discard),
       "Remaining": CribbageHand(filter(lambda card: card not in discard, hand))
     }

def choose_discards(hand, remaining_deck, dealer):
  discards_table = []
  for discard_option in yield_discard_options(hand):
    discard_option.update(get_hand_scores(discard_option["Remaining"], remaining_deck, dealer))
    discards_table.append(discard_option)
  discards_table.sort(key = lambda row: row["Min"], reverse = True)
  discards_table.sort(key = lambda row: row["Max"], reverse = True)
  discards_table.sort(key = lambda row: row["EV"], reverse = True)
  return discards_table
