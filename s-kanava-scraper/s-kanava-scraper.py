import os
import sys

import typer

def main(directory: str,
    output: str = typer.Option(None, help="Path to save output csv file.")):
    """
    directory: relative path to the folder of S-group text receipts;
    each of which can be copied and pasted from s-kanava.fi
    """

    if output is not None:
        sys.stdout = open(output, "w")

    for x in [f for f in os.listdir(directory) if not f.startswith('.')]:
        with open(f"{directory}/{x}") as fp:
            print(x)
            while True:

                line = fp.readline()
        
                if not line:
                    break

                if line[0] == ' ':
                    continue

                # reverse line so as to split on last comma
                comma_broken = line[::-1].split(',', 1)
                if len(comma_broken) < 2:
                    # more commas than expected => not an item line
                    continue
                pre_comma = comma_broken[1]
                try:
                    cents = int(comma_broken[0][::-1].strip())
                except(ValueError):
                    # what follows the comma is not an int => not an item line
                    continue
                euros_rev, item_rev = tuple(pre_comma.split(' ', 1))
                if item_rev[::-1].strip() == 'YHTEENSÄ':
                    # not keeping the total, nor anything after it
                    break
                print(item_rev[::-1] + ';' + euros_rev[::-1] + ',' + str(cents))

if __name__ == "__main__":
    typer.run(main)
