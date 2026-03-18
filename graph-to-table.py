import numpy as np

m = np.array(
    [
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
        [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    ]
)

final_string = []

for idx, row in enumerate(m):
    row_string = [f"{idx + 1} & "]
    if idx == 12 or idx == 13:
        mine_count = 1
        scen_prob = 0.25
    else:
        mine_count = 2
        scen_prob = 0.04
    for cell_idx, cell in enumerate(row):
        string_insert = f"{cell} & "
        if cell_idx == 11:
            string_insert += f"{mine_count} & {scen_prob} \\\\\n"
        row_string.append(string_insert)
    final_string.append("".join(row_string))

# string_start = "\\begin{table}\n\\centering\n\\begin{tabular}{c | cccccccccccc | c | c}\n"
print("".join(final_string))

