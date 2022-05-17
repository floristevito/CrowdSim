import numpy as np
import pandas as pd
from ema_workbench import (
    MultiprocessingEvaluator,
    Samplers,
    Scenario,
    ema_logging,
    perform_experiments,
    save_results,
)

from vadere_ema_formulations import get_vadere_formulation

"""Template for doing EMA based model runs"""

# enable EMA logging
ema_logging.log_to_stderr(ema_logging.INFO)

# scenario function
def get_scenarios(scenarios):
    """get scenarios in right format

    Args:
        scenarios (df): dataframe with scenarios from PRIM or directed search

    Returns:
        list: list with EMA scenario collections
    """
    s = scenarios.copy()
    # remove unneeded data
    outcomes = [
        "groupForming",
        "meanFreeFlowSpeed",
        "obstPotentialHeight",
        "pedPotentialHeight",
        "sdFreeFlowSpeed",
        "spawnFrequencyA",
        "spawnFrequencyB",
        "spawnFrequencyC",
        "spawnFrequencyD",
    ]
    s = s[outcomes]
    s["groupForming"] = s["groupForming"].apply(eval)
    s = s.to_dict(orient="records")

    # return as collection of EMA scenarios
    return [Scenario(name=None, **scenario) for scenario in s]


if __name__ == "__main__":
    # load sets of scenarios
    scenarios_oe_bad = pd.read_csv("../data/output/EMA/scenariosOeBad.csv").sample(100)
    scenarios_oe_good = pd.read_csv("../data/output/EMA/scenariosOeGood.csv").sample(
        100
    )
    scenarios_opt = pd.read_csv("../data/output/EMA/directedSearch.csv")
    scenarios_opt["groupForming"] = scenarios_opt["groupForming"].str.slice(15, -1)
    scenarios = [scenarios_oe_bad, scenarios_oe_good, scenarios_opt]

    strategies = [
        "controlGuidance100",
        "controlGuidance25",
        "controlObjects",
        "controlRegulators",
    ]

    s_count = 0

    for se in scenarios:
        print("at scenarios {}".format(s_count))
        s_count += 1

        for st in strategies:
            print("at strategy {}".format(st))
            # set the right vadere formulations
            model = get_vadere_formulation(
                id=1, replications=60, model_file=str(st) + "Data.scenario"
            )
            if st == "controlObjects":
                with MultiprocessingEvaluator(model, n_processes=20) as evaluator:
                    results = evaluator.perform_experiments(get_scenarios(se))
            else:
                with MultiprocessingEvaluator(model) as evaluator:
                    results = evaluator.perform_experiments(get_scenarios(se))

            # store results
            save_results(
                results,
                "../data/output/EMA/scenarios{}.tar.gz".format(str(s_count) + st),
            )
