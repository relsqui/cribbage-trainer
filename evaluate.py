import itertools
import joblib

from cribbage_hand import CribbageHand, make_cribbage_deck
from protocards import cribbage

memory = joblib.Memory("~/.cribbage-trainer-cache", verbose=0)

def total_score(score_block):
  return sum(score_block.values())

@memory.cache
def get_crib_scores(discards, turned, deck, dealer):
  scores = [
    total_score(cribbage.score_hand(discards + opponent_discards, turned=turned, crib=True, dealer=dealer))
    for opponent_discards in itertools.combinations(deck, 2)
  ]
  min_score = min(scores)
  max_score = max(scores)
  ev = sum(scores)/len(scores)
  return {
    "Min": min_score if dealer else -max_score,
    "Max": max_score if dealer else -min_score,
    "EV": ev if dealer else -ev
  }

def get_hand_scores(hand, turned, dealer):
  return total_score(cribbage.score_hand(hand, turned=turned, dealer=dealer))

def get_scores(discard_option, deck, dealer):
  scores = [{
      "Hand": get_hand_scores(discard_option["Remaining"], turned=turned, dealer=dealer),
      "Crib": get_crib_scores(discard_option["Discard"], turned=turned, deck=(make_cribbage_deck() - turned), dealer=dealer)
    } for turned in deck
  ]
  min_hand = min(s["Hand"] for s in scores)
  max_hand = max(s["Hand"] for s in scores)
  hand_ev = sum(s["Hand"] for s in scores)/len(scores)
  min_crib = min(s["Crib"]["Min"] for s in scores)
  max_crib = min(s["Crib"]["Max"] for s in scores)
  crib_ev = sum(s["Crib"]["EV"] for s in scores)/len(scores)
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
    discard_hand = CribbageHand(discard)
    remaining_hand = hand - discard_hand
    yield {
      "Discard": discard_hand,
      "Remaining": remaining_hand
    }

def choose_discards(hand, dealer, show_progress=False):
  remaining_deck = CribbageHand([card for card in make_cribbage_deck() if card not in hand])
  discards_table = []
  if show_progress:
    print(f"Evaluating {int((len(hand)*(len(hand)-1))/2)} possibilities ", end="")
  for discard_option in yield_discard_options(hand):
    if show_progress:
      print(".", end="", flush=True)
    discard_option.update(get_scores(discard_option, remaining_deck, dealer))
    discards_table.append(discard_option)
  if show_progress:
    print()
  discards_table.sort(key = lambda row: row["Min"], reverse = True)
  discards_table.sort(key = lambda row: row["Max"], reverse = True)
  discards_table.sort(key = lambda row: row["EV"], reverse = True)
  return discards_table
