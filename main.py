import sys

from crib_trainer import crib_trainer
from protocards import standard

# aces are low
CRIBBAGE_RANKS = [standard.ACE] + standard.RANKS[:-1]

def score_from_string(hand_string):
  pass

def main():
  if len(sys.argv) > 1:
    score_from_string(sys.argv[1].lower())
  else:
    crib_trainer()

if __name__ == "__main__":
    main()
