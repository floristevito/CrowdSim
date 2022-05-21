import numpy as np
import pandas as pd
from ema_workbench import (
    MultiprocessingEvaluator,
    Samplers,
    ema_logging,
    perform_experiments,
    save_results,
)

from vadere_ema_formulations import get_vadere_formulation

# enable EMA logging
ema_logging.log_to_stderr(ema_logging.INFO)

# set the right vadere formulations
model = get_vadere_formulation(
    id=1, replications=10, model_file="baseCaseData.scenario"
)

if __name__ == "__main__":
    with MultiprocessingEvaluator(model, n_processes=32) as evaluator:
        sa_results = evaluator.perform_experiments(
            scenarios=10, uncertainty_sampling=Samplers.SOBOL
        )

    # store results
    save_results(sa_results, "../data/output/EMA/sobol.tar.gz")
