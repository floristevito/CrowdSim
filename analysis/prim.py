from ema_workbench import perform_experiments, ema_logging, MultiprocessingEvaluator, save_results
import pandas as pd
import numpy as np
from vadere_ema_formulations import get_vadere_formulation


"""Template for doing EMA based model runs"""

# enable EMA logging
ema_logging.log_to_stderr(ema_logging.INFO)

# set the right vadere formulations
model = get_vadere_formulation(
    id=1,
    replications=60,
    model_file='baseCaseData.scenario'
)

if __name__ == '__main__':
    with MultiprocessingEvaluator(model, n_processes=6) as evaluator:
        sa_results = evaluator.perform_experiments(
            scenarios=1500, 
            uncertainty_sampling='lhs'
    )
    
    # results = perform_experiments(
    #     scenarios = 2, 
    #     uncertainty_sampling='lhs'
    # )

    # store results
    save_results(results, '../data/output/EMA/results.tar.gz')
