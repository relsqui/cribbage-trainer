import itertools

from protocards import standard

# aces are low
CRIBBAGE_RANKS = [standard.ACE] + standard.RANKS[:-1]

class CribbageCard(standard.StandardCard):
  def __lt__(self, other):
    # ignore suits, which lets us use null when suit wasn't specified
    return CRIBBAGE_RANKS.index(self.rank) < CRIBBAGE_RANKS.index(other.rank)

class CribbageHand(standard.StandardHand):
  def __str__(self):
    # ignore suits, rank is a way more important sorting criterion
    sorted_hand = sorted(self)
    return " ".join([f"{card.rank.short}{card.suit.short}" for card in sorted_hand])

def make_cribbage_deck(shuffle=True):
  # this is just standard.make_deck with CribbageHand/CribbageCard
  deck = CribbageHand([CribbageCard(rank, suit) for rank, suit in itertools.product(CRIBBAGE_RANKS, standard.SUITS)])
  if shuffle:
    deck.shuffle()
  return deck
