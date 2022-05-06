import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from ema_workbench import load_results
from SALib.analyze import sobol


def calculate_robustness_averted(results):
    """calculation of the averted density areas robustness metric

    Args:
        results (df): pd DataFrame with experimental results

    Returns:
        dict: absolute and mean averted density areas,
            absolute and percentage completly averted scenarios
    """

    # make copy of original results
    r = results.copy()

    # evaluate per area per row if critical density is averted
    r["boolean1"] = rp["meanDensityArea1"] <= 0.8
    r["boolean2"] = rp["meanDensityArea2"] <= 0.8
    r["boolean3"] = rp["meanDensityArea3"] <= 0.8
    r["boolean4"] = rp["meanDensityArea4"] <= 0.8

    # cast booleans to int
    r = r.astype(
        {
            "boolean1": int,
            "boolean2": int,
            "boolean3": int,
            "boolean4": int,
        }
    )

    # make on total score, return absolute and mean averted density areas
    r["averted"] = r["boolean1"] + r["boolean2"] + r["boolean3"] + r["boolean4"]
    return {
        "absolute_averted": r["averted"].sum(),
        "mean_averted": r["averted"].sum() / len(r["averted"]),
        "scenarios_averted": sum(r["averted"] == 4),
        "percentage_scenarios_averted": round(sum(r["averted"] == 4) / len(r), 2),
    }


if __name__ == "__main__":
    # load results PRIM problematic scenarios
    scenarios_prim = pd.read_csv("../data/output/EMA/scenariosPrim.csv")
    rp = pd.read_csv("../data/output/EMA/resultsScenariosPrim.csv")

    print(calculate_robustness_averted(rp))
