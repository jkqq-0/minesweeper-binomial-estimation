import itertools
import math
from string import ascii_uppercase
import csv
import numpy as np
from tabulate import tabulate
from scipy import stats


def iter_all_strings():
    for size in itertools.count(1):
        for s in itertools.product(ascii_uppercase, repeat=size):
            yield "".join(s)


# Function to check whether
# position is valid or not
def isValidPos(i, j, n, m):
    if i < 0 or j < 0 or i >= n or j >= m:
        return 0
    return 1


# Function that returns all adjacent elements
def getAdjacent(arr, i, j):

    # Size of given 2d array
    n = len(arr)
    m = len(arr[0])

    ans = []

    # directions
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dx, dy in dirs:
        x, y = i + dx, j + dy
        if isValidPos(x, y, n, m):
            ans.append(arr[x][y])

    return ans


class Mines:
    filename = str()
    board = list()
    bomb_perimiter_coord_dict = dict()
    number_square_coord_list = list()
    bomb_square_coord_list = list()
    safe_square_coord_list = list()
    flat_perimiter_labels = list()
    valid_scenarios = list()
    probabilities = dict()
    height = 0
    width = 0

    def __init__(self, filename, board_bomb_count, board_square_count):
        with open(filename, "r") as csvfile:
            csvreader = csv.reader(csvfile)  # Reader object

            for row_idx, row in enumerate(csvreader):  # Read rows
                for col_idx in range(len(row)):
                    if row[col_idx].isdigit():
                        row[col_idx] = int(row[col_idx])
                        self.number_square_coord_list.append((row_idx, col_idx))
                    if row[col_idx] == "":
                        row[col_idx] = 0
                    if row[col_idx] == "💣":
                        self.bomb_square_coord_list.append((row_idx, col_idx))
                    if row[col_idx] == "✅":
                        self.safe_square_coord_list.append((row_idx, col_idx))
                self.board.append(row)

            print("Board height: %d" % csvreader.line_num)
            print("Board width: %d" % len(self.board[0]))
            print("Board:")
            for row in self.board:
                print(row)
            print()
            self.height = csvreader.line_num
            self.width = len(self.board[0])
            unknown_squares = (
                board_square_count
                - len(self.number_square_coord_list)
                - len(self.safe_square_coord_list)
                - len(self.bomb_square_coord_list)
            )
            self.rho = (
                board_bomb_count - len(self.bomb_square_coord_list)
            ) / unknown_squares
            print(f"Rho: {self.rho}")
        self.__generate_coord_dict()
        self.__generate_scenarios()
        self.__generate_probabilities()

    def __generate_coord_dict(self):
        labels = list()
        for s in itertools.islice(iter_all_strings(), self.width * self.height):
            labels.append(s)

        count = 0

        number_coords = set(self.number_square_coord_list)
        known_coords = set(
            self.number_square_coord_list
            + self.safe_square_coord_list
            + self.bomb_square_coord_list
        )

        for row_idx, row in enumerate(self.board):
            for col_idx, col in enumerate(row):
                if (row_idx, col_idx) in known_coords:
                    continue
                is_perimeter = False
                dirs = [
                    (-1, -1),
                    (-1, 0),
                    (-1, 1),
                    (0, -1),
                    (0, 1),
                    (1, -1),
                    (1, 0),
                    (1, 1),
                ]
                for dx, dy in dirs:
                    x, y = row_idx + dx, col_idx + dy
                    if (x, y) in number_coords:
                        is_perimeter = True
                        break

                if is_perimeter:
                    self.bomb_perimiter_coord_dict[(row_idx, col_idx)] = labels[count]
                    self.flat_perimiter_labels.append(labels[count])
                    count += 1

    def __generate_scenarios(self):
        for scenario in itertools.product(
            (0, 1), repeat=len(self.flat_perimiter_labels)
        ):
            mapping = list(zip(self.bomb_perimiter_coord_dict.keys(), scenario))

            # create a board with the current mapping
            grid_from_scenario = np.zeros((self.height, self.width))

            for (row, col), bomb in mapping:
                assert col < self.width
                assert row < self.height
                grid_from_scenario[row][col] = bomb

            # add known bomb locations to all potential scenarios
            for row, col in self.bomb_square_coord_list:
                grid_from_scenario[row][col] = 1

            check_passed = True

            for row, col in self.number_square_coord_list:
                scenario_neighbors = getAdjacent(grid_from_scenario, row, col)
                required_bomb_count = self.board[row][col]
                if sum(scenario_neighbors) != required_bomb_count:
                    check_passed = False
                    break

            if not check_passed:
                continue
            else:
                self.valid_scenarios.append(grid_from_scenario)

    def __generate_probabilities(self):
        unique_bomb_counts = set()
        bombs_per_scenario = list()
        for scenario in self.valid_scenarios:
            bombs_in_labeled_squares = list()
            for row, col in self.bomb_perimiter_coord_dict.keys():
                bombs_in_labeled_squares.append(scenario[row][col])
            scenario_bomb_count = sum(bombs_in_labeled_squares)
            unique_bomb_counts.add(scenario_bomb_count)
            bombs_per_scenario.append(scenario_bomb_count)

        unknown_squares_count = len(self.flat_perimiter_labels)
        case_probabilities = stats.binom.pmf(
            list(unique_bomb_counts), unknown_squares_count, self.rho
        )
        sum_of_probs = sum(case_probabilities)
        for count, prob in list(zip(unique_bomb_counts, case_probabilities)):
            self.probabilities[int(count)] = {
                "probability": prob,
                "normalized_probability": (prob) / sum_of_probs,
            }

        case_scenario_counts = dict()
        for count in bombs_per_scenario:
            if count not in case_scenario_counts:
                case_scenario_counts[int(count)] = 0
            case_scenario_counts[int(count)] += 1
        print(case_scenario_counts)

        for count, probs in self.probabilities.items():
            probs["scenario_weighted_probability"] = (
                probs["normalized_probability"] / case_scenario_counts[count]
            )

    def print_probabilities(self):
        for count, probs in self.probabilities.items():
            table_data = [[f"Case with {count} Bombs", "Value"]]
            table_data.extend(
                [[f"{key}", f"{value}"] for (key, value) in probs.items()]
            )
            print(
                tabulate(
                    table_data, headers="firstrow", tablefmt="grid", floatfmt=".8f"
                )
            )

    def print_scenarios(self):
        table = list()
        header_row = ["Scenario"]
        for label in self.flat_perimiter_labels:
            header_row.append(label)
        header_row.append("Bomb Count")
        header_row.append("Scenario Probability")
        table.append(header_row)
        count = 1
        for scenario in self.valid_scenarios:
            bomb_count = 0
            scenario_row = list()
            scenario_row.append(count)
            for row, col in self.bomb_perimiter_coord_dict.keys():
                scenario_row.append(scenario[row][col])
                bomb_count += scenario[row][col]
            scenario_row.append(bomb_count)
            scenario_row.append(
                self.probabilities[bomb_count]["scenario_weighted_probability"]
            )
            table.append(scenario_row)
            count += 1
        print(tabulate(table, headers="firstrow", tablefmt="grid", floatfmt=".2f"))

    def print_scenarios_latex(
        self, caption_text="Placeholder Text", table_label="tab:placeholder-label"
    ):
        print("\\begin{table}")
        print("\t\\centering")
        print(
            "\t\\begin{tabular}{c | "
            + ("c" * len(self.flat_perimiter_labels) + "c | c}")
        )
        print(
            "\tScenario & "
            + "".join([f"${i}$ & " for i in self.flat_perimiter_labels])
            + "\\makecell{Mine\\\\Count} & \\makecell{Scenario\\\\Probability} \\\\[1ex]"
        )
        print("\t\\midrule")
        table = list()
        for scenario in self.valid_scenarios:
            scenario_row = list()
            for row, col in self.bomb_perimiter_coord_dict.keys():
                scenario_row.append(int(scenario[row][col]))
            table.append(scenario_row)

        scenario_number = 1

        for row in table:
            row_string = ["\t"]
            row_string.append(f"{scenario_number} & ")
            bomb_count = 0
            for i in range(len(row)):
                row_string.append(f"{row[i]} & ")
                bomb_count += row[i]
            row_string.append(
                f"{bomb_count} & {self.probabilities[bomb_count]["scenario_weighted_probability"]:.3f} \\\\"
            )
            print("".join(row_string))
            scenario_number += 1
        print("\t\\end{tabular}")
        print("\t\\caption{" + caption_text + "}")
        print("\t\\label{" + table_label + "}")
        print("\\end{table}")


filename = "grid-8.csv"
complex_grid = Mines(filename, 40, 256)
complex_grid.print_probabilities()
print()
complex_grid.print_scenarios_latex()
