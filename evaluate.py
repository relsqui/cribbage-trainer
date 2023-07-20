import itertools
import joblib

from cribbage_hand import CribbageHand, make_cribbage_deck
from protocards import cribbage

memory = joblib.Memory("~/.cribbage-trainer-cache", verbose=0)

def total_score(score_block):
  return sum(score_block.values())

@memory.cache
def get_crib_scores(discard_option, turned):
  discards = discard_option["Discard"]
  deck = make_cribbage_deck() - discard_option["Remaining"] - turned
  scores = [
    total_score(cribbage.score_hand(discards + opponent_discards, turned=turned, crib=True))
    for opponent_discards in itertools.combinations(deck, 2)
  ]
  return {
    "Min": min(scores),
    "Max": max(scores),
    "EV": sum(scores)/len(scores)
  }

def get_hand_score(hand, turned, dealer):
  return total_score(cribbage.score_hand(hand, turned=turned, dealer=dealer))

def get_scores(discard_option, deck, dealer):
  hand_scores = []
  crib_mins = []
  crib_maxes = []
  crib_evs = []
  for turned in deck:
    hand_scores.append(get_hand_score(discard_option["Remaining"], turned=turned, dealer=dealer))
    crib_scores = get_crib_scores(discard_option, turned=turned)
    crib_mins.append(crib_scores["Min"] if dealer else -crib_scores["Max"])
    crib_maxes.append(crib_scores["Max"] if dealer else -crib_scores["Min"])
    crib_evs.append(crib_scores["EV"] if dealer else -crib_scores["EV"])
  min_hand = min(hand_scores)
  max_hand = max(hand_scores)
  hand_ev = sum(hand_scores)/len(hand_scores)
  min_crib = min(crib_mins)
  max_crib = max(crib_maxes)
  crib_ev = sum(crib_evs)/len(crib_evs)
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

@memory.cache(ignore=["show_progress"])
def choose_discards(hand, dealer=False, show_progress=False):
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
