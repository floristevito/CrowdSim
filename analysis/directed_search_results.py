import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from ema_workbench.analysis import parcoords

from vadere_ema_formulations import get_vadere_formulation

# load model formulation and results
model = get_vadere_formulation(id=2, replications=1, model_file="baseCaseData.scenario")
worst_scenarios = pd.read_csv("../data/output/EMA/directedSearch.csv")
convergence = pd.read_csv("../data/output/EMA/directedSearchConvergence.csv")

# plot convergence
fig, (ax1, ax2) = plt.subplots(ncols=2, sharex=True, figsize=(8, 4))
ax1.plot(convergence.nfe, convergence.epsilon_progress)
ax1.set_ylabel("$\epsilon$-progress")
ax2.plot(convergence.nfe, convergence.hypervolume)
ax2.set_ylabel("hypervolume")

ax1.set_xlabel("number of function evaluations")
ax2.set_xlabel("number of function evaluations")
plt.show()

# plot parallel coordinate plots
data = worst_scenarios.loc[:, [o.name for o in model.outcomes]].sample(10)
limits = parcoords.get_limits(data)
limits.loc[
    0,
    [
        "maxDensityArea1",
        "maxDensityArea2",
        "maxDensityArea3",
        "maxDensityArea4",
    ],
] = 0
limits.loc[
    1,
    [
        "maxDensityArea1",
        "maxDensityArea2",
        "maxDensityArea3",
        "maxDensityArea4",
    ],
] = 4

paraxes = parcoords.ParallelAxes(limits)
paraxes.plot(data)
paraxes.invert_axis("meanSpeed")
plt.show()
