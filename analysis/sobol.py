from ema_workbench import perform_experiments, ema_logging, MultiprocessingEvaluator, save_results
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

with MultiprocessingEvaluator(model, n_processes=6) as evaluator:
    sa_results = evaluator.perform_experiments(
        scenarios = 100, 
        uncertainty_sampling='sobol'
)

# store results
save_results(sa_results, '../data/output/EMA/sobolTest01.tar.gz')
