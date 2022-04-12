from ema_workbench import perform_experiments, ema_logging, MultiprocessingEvaluator, save_results
from ema_workbench.em_framework.optimization import (HyperVolume, EpsilonProgress)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from vadere_ema_formulations import get_vadere_formulation


# enable EMA logging
ema_logging.log_to_stderr(ema_logging.INFO)

# set the right vadere formulations
model = get_vadere_formulation(
    id=2,
    replications=1,
    model_file='baseCaseData.scenario'
)

# set convergence matrics
convergence_metrics = [HyperVolume(), EpsilonProgress()]

#search for worst cases(s)
with MultiprocessingEvaluator(model, n_processes=6) as evaluator:
    results, convergence = evaluator.optimize(
        nfe=300,
        searchover='uncertainties',
        epsilons=[0.1,]*len(model.outcomes),
        convergence=convergence_metrics
    )

# plot convergence
fig, (ax1, ax2) = plt.subplots(ncols=2, sharex=True, figsize=(8,4))
ax1.plot(convergence.nfe, convergence.epsilon_progress)
ax1.set_ylabel('$\epsilon$-progress')
ax2.plot(convergence.nfe, convergence.hypervolume)
ax2.set_ylabel('hypervolume')

ax1.set_xlabel('number of function evaluations')
ax2.set_xlabel('number of function evaluations')
plt.show()