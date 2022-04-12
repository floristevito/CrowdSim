from ema_workbench import (perform_experiments, ema_logging,
                           MultiprocessingEvaluator, save_results,
                           Scenario)
import pandas as pd
import numpy as np
from vadere_ema_formulations import get_vadere_formulation

# enable EMA logging
ema_logging.log_to_stderr(ema_logging.INFO)

# set the right vadere formulations
model = get_vadere_formulation(
    id=1,
    replications=1,
    model_file='baseCaseData.scenario'
)

# set up base case values (note that group size vector is already set in the model)
base = {
    'spawnFrequencyA': 1,
    'spawnFrequencyB': 1,
    'spawnFrequencyC': 1,
    'spawnFrequencyD': 1,
    'meanFreeFlowSpeed': 1,
    'sdFreeFlowSpeed': 0.26,
    'pedPotentialHeight': 50,
    'obstPotentialHeight': 6.0
}

def get_base_scenarios(n):
    return [Scenario('base_case', **base) for i in range(n)]

if __name__ == '__main__':

    ema_logging.log_to_stderr(ema_logging.INFO)

    # base case
    with MultiprocessingEvaluator(model, n_processes=6) as evaluator:
        results = evaluator.perform_experiments(get_base_scenarios(100))

    # store results
    save_results(results, '../data/output/EMA/seedAnalysis01.tar.gz')