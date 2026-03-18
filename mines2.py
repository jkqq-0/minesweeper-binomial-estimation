import itertools

grid = [["A", "B", "C", "D"], ["E", 1, 1, "F"], ["G", "H", "I", "J"]]

hidden_cells = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

final_scenarios = []

for scenario in itertools.product([0, 1], repeat=len(hidden_cells)):
    mapping = dict(zip(hidden_cells, scenario))
    sum_neighbors_1 = (
        mapping["A"]
        + mapping["B"]
        + mapping["C"]
        + mapping["E"]
        + mapping["G"]
        + mapping["H"]
        + mapping["I"]
    )
    sum_neighbors_2 = (
        mapping["B"]
        + mapping["C"]
        + mapping["D"]
        + mapping["F"]
        + mapping["H"]
        + mapping["I"]
        + mapping["J"]
    )

    if sum_neighbors_1 == 1 and sum_neighbors_2 == 1:
        final_scenarios.append(mapping)

for scenario in final_scenarios:
    assert len(final_scenarios) == 13
    scenario_sum = 0
    for index in scenario:
        scenario_sum += scenario[index]
    assert scenario_sum < 3
    print(scenario)
