import click

from crib_trainer import crib_trainer
from hand_checker import check_hand

help_text = """
If a hand string is supplied, prints the table of expected values for each possible discard.
Otherwise, generates cribbage hands and shows the expected value table for each hand after
a pause to let you think about it.

Describe hands using a letter or number for each rank (A2..9TJQK). Adding a suit letter
(cdhs) after a group of ranks is optional -- arbitrary suits will be assigned if you
omit them. The case and order of cards doesn't matter (except for associating suits with ranks).
"""

@click.command(epilog=help_text)
@click.option('--dealer', is_flag=True, help="If set, hand will be checked as if the player is the dealer.")
@click.argument('hand', nargs=-1)
def main(dealer, hand):
  if len(hand):
    check_hand(" ".join(hand), dealer)
  else:
    crib_trainer(dealer)

if __name__ == "__main__":
    main()
