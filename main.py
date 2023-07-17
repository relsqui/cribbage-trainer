import sys

from crib_trainer import crib_trainer
from hand_checker import check_hand

def main():
  if len(sys.argv) > 1:
    check_hand(" ".join(sys.argv[1:]))
  else:
    crib_trainer()

if __name__ == "__main__":
    main()
