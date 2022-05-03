from ema_workbench import (
    perform_experiments,
    ema_logging,
    MultiprocessingEvaluator,
    save_results,
    Scenario,
    SequentialEvaluator,
)
import pandas as pd
import numpy as np
from vadere_ema_formulations import get_vadere_formulation


"""Test regarding model outcome convergence"""

# enable EMA logging
ema_logging.log_to_stderr(ema_logging.INFO)

# formulate model, set replications to 1
# since we do additional sample calculations in the
# visualization notebook
model = get_vadere_formulation(
    id=1, replications=60, model_file="noGroupsData.scenario"
)

# set up base case values (note that group size vector is already set in
# the model)
base_case = {
    "spawnFrequencyA": 1,
    "spawnFrequencyB": 1,
    "spawnFrequencyC": 1,
    "spawnFrequencyD": 1,
    "meanFreeFlowSpeed": 1,
    "sdFreeFlowSpeed": 0.26,
    "pedPotentialHeight": 50,
    "obstPotentialHeight": 6.0,
}

# set up bad case values (note that group size vector is already set in
# the model)
bad_case = {
    "spawnFrequencyA": 1,
    "spawnFrequencyB": 1,
    "spawnFrequencyC": 1,
    "spawnFrequencyD": 1,
    "meanFreeFlowSpeed": 0.66,
    "sdFreeFlowSpeed": 0.26,
    "pedPotentialHeight": 50,
    "obstPotentialHeight": 10.0,
}


def get_scenarios(name, n, values):
    return [Scenario(name, **values) for i in range(n)]


if __name__ == "__main__":
    # enable logging
    ema_logging.log_to_stderr(ema_logging.INFO)

    # base case
    # 1275
    with MultiprocessingEvaluator(model, n_processes=10) as evaluator:
        results = evaluator.perform_experiments(
            get_scenarios(name="baseCaseNoGroups", n=1, values=base_case)
        )

    # save
    save_results(results, "../data/output/EMA/noGroupsBaseCase.tar.gz")

    # bad case
    with MultiprocessingEvaluator(model, n_processes=10) as evaluator:
        results = evaluator.perform_experiments(
            get_scenarios(name="baseCaseNoGroups", n=1, values=bad_case)
        )

    # save
    save_results(results, "../data/output/EMA/noGroupsBadCase.tar.gz")
