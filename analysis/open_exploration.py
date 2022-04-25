from ema_workbench import Samplers, perform_experiments, ema_logging, MultiprocessingEvaluator, save_results
import pandas as pd
import numpy as np
from vadere_ema_formulations import get_vadere_formulation


"""Model run for open exploration"""

# enable EMA logging
ema_logging.log_to_stderr(ema_logging.INFO)

# set the right vadere formulations
model = get_vadere_formulation(
    id=1,
    replications=60,
    model_file='baseCaseData.scenario'
)

if __name__ == '__main__':
    with MultiprocessingEvaluator(model, n_processes=20) as evaluator:
        results = evaluator.perform_experiments(
            scenarios=1000, 
            uncertainty_sampling=Samplers.LHS
    )
    
    # results = perform_experiments(
    #     scenarios = 2, 
    #     uncertainty_sampling=Samplers.LHS
    # )

    # store results
    save_results(results, '../data/output/EMA/resultsOpenExploration.tar.gz')
