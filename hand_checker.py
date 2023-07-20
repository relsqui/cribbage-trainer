from cribbage_hand import CribbageCard, CribbageHand, make_cribbage_deck
from evaluate import choose_discards
from protocards import standard
from tabulate import tabulate

class NullSuit(standard.Suit):
  def __init__(self):
    super().__init__(name="Null", plural="Null", short="")

  def __eq__(self, other):
    # unspecified suits shouldn't form flushes
    return False

NULL_SUIT = NullSuit()

def match_suit(letter):
  for suit in standard.SUITS:
    if letter == suit.short:
      return suit
  return None

def match_rank(letter):
  for rank in standard.RANKS:
    if letter == rank.short:
      return rank
  return None

def hand_from_string(hand_string):
  hand = CribbageHand()
  ranks_so_far = []
  for letter in hand_string:
    if letter == " ":
      for rank in ranks_so_far:
        hand.append(CribbageCard(rank, NULL_SUIT))
      ranks_so_far = []
    suit = match_suit(letter.lower())
    if suit:
      for rank in ranks_so_far:
        hand.append(CribbageCard(rank, suit))
      ranks_so_far = []
    else:
      rank = match_rank(letter.upper())
      if rank:
        ranks_so_far.append(rank)
  for rank in ranks_so_far:
    hand.append(CribbageCard(rank, NULL_SUIT))
  return hand

def assign_suits(hand):
  # sort so the same hand in a different order can hit cache
  hand = CribbageHand(sorted(hand))
  suit_counts = {
    # kind of a silly workaround for suits being unhashable
    index: len(hand.by_rank(suit)) for index, suit in enumerate(standard.SUITS)
  }
  for hand_index, card in enumerate(hand):
    # can't compare to NULL_SUIT because of its __eq__
    if type(card.suit) == NullSuit:
      suit_index = min(suit_counts, key=suit_counts.get)
      # can't just set the suit because it sets name etc. in __init__
      hand[hand_index] = CribbageCard(card.rank, standard.SUITS[suit_index])
      suit_counts[suit_index] += 1
  return hand

def check_hand(input_string, dealer=False):
  hand = hand_from_string(input_string)
  print(f"I interpreted that hand as: {hand}")
  hand = assign_suits(hand)
  print(f"Assigning arbitrary suits: {hand}")
  discard_table = choose_discards(hand, dealer=dealer, show_progress=True)
  print(f"I would have cribbed: {discard_table[0]['Discard']}. Full stats:\n")
  print(tabulate(discard_table, headers = "keys"))
