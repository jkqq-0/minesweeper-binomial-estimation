# Minesweeper Binomial Estimation

This project implements a basic strategy for estimating the bomb probabilities of squares in minesweeper grids when guessing is involved. The basic outline of the algorithm is as follows:

1. It exhaustively checks all configurations of bombs within the unknown squares on the board to find the valid oness.
2. It uses the binomial distribution to calculate the probability of there being a certain number of bombs in an arbitrary collection of unknown squares (given information provided about the size of the board and the total number of bombs). It calculates this probability for each of the unique total bomb counts within the hidden squares of the valid scenarios.
3. It normalizes these probabilities by dividing each of them by the sum of the probabilities for all valid bomb counts.
4. It weights these probilities by the number of scenarios in which each bomb count occurs.
5. To find the probability of a bomb being in a given square, it takes the sum of the scenario-weighted normalized probabilities for each scenario there is a bomb in that square.

Basic usage of the program looks like one of the following:

Default behavior (tabulate scenarios, print both probabilities, ignore coord dict)
```
python mines.py grid-9-version-2.csv
```

Print scenarios as LaTeX, hide square probabilities, and print the coord dict
```
python mines.py grid-9-version-2.csv --latex --hide-square-probs --print-coord-dict
```

Hide all probabilities and just print the regular scenarios table
```
python mines.py grid-9-version-2.csv --hide-case-probs --hide-square-probs
```

The program uses board size to be 256 and mine count to be 40 by default. You can run the program with `-h` to see further options.
