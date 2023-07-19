import itertools
import joblib

from cribbage_hand import CribbageHand, make_cribbage_deck
from protocards import cribbage

memory = joblib.Memory("~/.protocards-cache", verbose=0)

@memory.cache
def get_crib_scores(discards, turned, deck, dealer):
  deck.shuffle()
  min_score = 40
  max_score = 0
  ev = 0
  outcome_count = (len(deck) * (len(deck) - 1))/2
  for opponent_discards in itertools.combinations(deck, 2):
    crib = CribbageHand(discards + opponent_discards)
    score = sum(cribbage.score_hand(crib, turned=turned, crib=True, dealer=dealer).values())
    min_score = min(min_score, score)
    max_score = max(max_score, score)
    ev += score/outcome_count
  return {
    "Min": min_score if dealer else -max_score,
    "Max": max_score if dealer else -min_score,
    "EV": ev if dealer else -ev
  }

@memory.cache
def get_hand_scores(discard_option, deck, dealer):
  min_hand = 40
  max_hand = 0
  hand_ev = 0
  min_crib = 40
  max_crib = -40
  crib_ev = 0
  outcome_count = len(deck)
  for turned in deck:
    hand_score = sum(cribbage.score_hand(discard_option["Remaining"], turned=turned, dealer=dealer).values())
    min_hand = min(min_hand, hand_score)
    max_hand = max(max_hand, hand_score)
    hand_ev += hand_score/outcome_count
    remaining_deck = CribbageHand([card for card in deck if card is not turned])
    crib_scores = get_crib_scores(discard_option["Discard"], turned=turned, deck=remaining_deck, dealer=dealer)
    min_crib = min(min_crib, crib_scores["Min"])
    max_crib = max(max_crib, crib_scores["Max"])
    crib_ev += crib_scores["EV"]/outcome_count
  return {
    "H Min": min_hand,
    "H Max": max_hand,
    "H EV": hand_ev,
    "C Min": min_crib,
    "C Max": max_crib,
    "C EV": crib_ev,
    "Min": min_hand + min_crib,
    "Max": max_hand + max_crib,
    "EV": hand_ev + crib_ev
  }

def yield_discard_options(hand):
  for discard in itertools.combinations(hand, 2):
     yield {
       "Discard": CribbageHand(discard),
       "Remaining": CribbageHand(filter(lambda card: card not in discard, hand))
     }

@memory.cache
def choose_discards(hand, dealer, show_progress=False):
  remaining_deck = CribbageHand([card for card in make_cribbage_deck(shuffle=False) if card not in hand])
  discards_table = []
  if show_progress:
    print(f"Evaluating {int((len(hand)*(len(hand)-1))/2)} possibilities ", end="")
  for discard_option in yield_discard_options(hand):
    print(".", end="", flush=True)
    discard_option.update(get_hand_scores(discard_option, remaining_deck, dealer))
    discards_table.append(discard_option)
  if show_progress:
    print()
  discards_table.sort(key = lambda row: row["Min"], reverse = True)
  discards_table.sort(key = lambda row: row["Max"], reverse = True)
  discards_table.sort(key = lambda row: row["EV"], reverse = True)
  return discards_table
