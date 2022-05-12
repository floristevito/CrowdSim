import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from ema_workbench import (
    MultiprocessingEvaluator,
    ema_logging,
    perform_experiments,
    save_results,
)
from ema_workbench.em_framework.optimization import EpsilonProgress, HyperVolume

from vadere_ema_formulations import get_vadere_formulation

# enable EMA logging
ema_logging.log_to_stderr(ema_logging.INFO)

# set the right vadere formulations
model = get_vadere_formulation(id=2, replications=1, model_file="baseCaseData.scenario")

if __name__ == "__main__":
    # set convergence matrics
    convergence_metrics = [
        HyperVolume.from_outcomes(model.outcomes),
        EpsilonProgress(),
    ]

    # search for worst cases(s)
    with MultiprocessingEvaluator(model, n_processes=20) as evaluator:
        results, convergence = evaluator.optimize(
            nfe=1000,
            searchover="uncertainties",
            epsilons=[
                0.25,
            ]
            * len(model.outcomes),
            convergence=convergence_metrics,
        )

    # save results
    convergence.to_csv("../data/output/EMA/directedSearchConvergence.csv")
    results.to_csv("../data/output/EMA/directedSearch.csv")
