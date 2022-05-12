from ema_workbench import (
    Samplers,
    perform_experiments,
    ema_logging,
    MultiprocessingEvaluator,
    save_results,
    Scenario,
)
import pandas as pd
import numpy as np
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
    scenarios_prim = pd.read_csv("../data/output/EMA/scenariosPrim.csv")

    strategies = ["controlGuidance100", "controlObjects", "controlRegulators"]

    for s in strategies:
        # set the right vadere formulations
        model = get_vadere_formulation(
            id=1, replications=1, model_file=str(s) + "Data.scenario"
        )

        with MultiprocessingEvaluator(model, n_processes=6) as evaluator:
            results = evaluator.perform_experiments(get_scenarios(scenarios_prim))

        # store results
        save_results(results, "../data/output/EMA/{}.tar.gz".format(s))
