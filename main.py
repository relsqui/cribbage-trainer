import click
import itertools

from crib_trainer import crib_trainer
from cribbage_hand import CribbageHand, make_cribbage_deck
from evaluate import choose_discards
from hand_checker import check_hand

help_text = """
Find more details at: https://github.com/relsqui/cribbage-trainer

If you provide a string describing a cribbage hand, this program prints the table of
expected values for each possible discard (assuming the opponent is dealer; use --dealer
to override). Describe hands using a letter or number for each rank (A2..9TJQK). Adding
a suit letter (cdhs) after any group of ranks is optional (arbitrary suits will be assigned
if you omit them). The case and order of cards doesn't otherwise matter.

If no hand is given, generates random cribbage hands and shows the expected value table for
each hand after a pause to let you think about it.

Both of these are slow because they evaluate many options. You can pre-fill the cache
and make future usage faster by running with --fill-cache. (This is safe to interrupt
and resume at any time, it will by definition skip anything already cached.)
"""

def build_cache():
   for hand in itertools.combinations(make_cribbage_deck(), 6):
      hand = CribbageHand(hand)
      hand.sort()
      print(f"{hand} ... ", end="", flush=True)
      choose_discards(hand)
      print("Done.")

@click.command(help=help_text)
@click.option("--dealer", is_flag=True, help="If set, hand will be checked as if the player is the dealer. Otherwise, opponent will be dealer.")
@click.option("--fill-cache", is_flag=True, help="Non-interactively evaluate hands to fill the score cache. This makes other queries faster.")
@click.argument("hand", nargs=-1)
def main(hand, dealer=False, fill_cache=False):
  if fill_cache:
     build_cache()
  elif len(hand):
    check_hand(" ".join(hand), dealer)
  else:
    crib_trainer(dealer)

if __name__ == "__main__":
    main()
