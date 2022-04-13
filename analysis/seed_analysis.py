from ema_workbench import (perform_experiments, ema_logging,
                           MultiprocessingEvaluator, save_results,
                           Scenario, SequentialEvaluator)
import pandas as pd
import numpy as np
from vadere_ema_formulations import get_vadere_formulation

# enable EMA logging
ema_logging.log_to_stderr(ema_logging.INFO)

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
    total = pd.DataFrame()

    # base case loop
    for i in range(1,51):
        model = get_vadere_formulation(
            id=3,
            replications=i,
            model_file='baseCaseData.scenario'
        )

        with MultiprocessingEvaluator(model) as evaluator:
            experiments, results = evaluator.perform_experiments(get_base_scenarios(1))

        sample_res = pd.DataFrame(results)
        sample_res['sampleSize'] = i
        total = pd.concat([total, sample_res])

    # save
    total.to_csv('../data/output/EMA/seedAnalysis.csv')