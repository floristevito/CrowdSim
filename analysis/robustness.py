import pandas as pd
from ema_workbench import load_results


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
    r["boolean1"] = r["meanDensityArea1"] <= 0.8
    r["boolean2"] = r["meanDensityArea2"] <= 0.8
    r["boolean3"] = r["meanDensityArea3"] <= 0.8
    r["boolean4"] = r["meanDensityArea4"] <= 0.8

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
        "number of averted areas": r["averted"].sum(),
        "mean_averted": r["averted"].sum() / len(r["averted"]),
        "complete scenarios averted": sum(r["averted"] == 4),
        "percentage_scenarios_averted": round(sum(r["averted"] == 4) / len(r), 2),
    }


def calculate_robustness_mean_variance(results):
    """calculation of the mean variance robustness metric

    Args:
        results (df): pd DataFrame with experimental results

    Returns:
        dict: metric score for all 9 outcomes,
            speed is maximised, density values are minimised
    """
    # make copy of results
    r = results.copy()

    # maximize speed, so deviding the mean by the std
    r_meanSpeed = results["meanSpeed"].mean() / results["meanSpeed"].std()

    # minimizing density values, so multipying the mean with the std
    r_meanDensityArea1 = (
        results["meanDensityArea1"].mean() * results["meanDensityArea1"].std()
    )
    r_maxDensityArea1 = (
        results["maxDensityArea1"].mean() * results["maxDensityArea1"].std()
    )
    r_meanDensityArea2 = (
        results["meanDensityArea2"].mean() * results["meanDensityArea2"].std()
    )
    r_maxDensityArea2 = (
        results["maxDensityArea2"].mean() * results["maxDensityArea2"].std()
    )
    r_meanDensityArea3 = (
        results["meanDensityArea3"].mean() * results["meanDensityArea3"].std()
    )
    r_maxDensityArea3 = (
        results["maxDensityArea3"].mean() * results["maxDensityArea3"].std()
    )
    r_meanDensityArea4 = (
        results["meanDensityArea4"].mean() * results["meanDensityArea4"].std()
    )
    r_maxDensityArea4 = (
        results["maxDensityArea4"].mean() * results["maxDensityArea4"].std()
    )

    # return final scores in a dict
    return {
        "meanSpeed": r_meanSpeed,
        "meanDensityArea1": r_meanDensityArea1,
        "maxDensityArea1": r_maxDensityArea1,
        "meanDensityArea2": r_meanDensityArea2,
        "maxDensityArea2": r_maxDensityArea2,
        "meanDensityArea3": r_meanDensityArea3,
        "maxDensityArea3": r_maxDensityArea3,
        "meanDensityArea4": r_meanDensityArea4,
        "maxDensityArea4": r_maxDensityArea4,
    }


if __name__ == "__main__":
    # load results PRIM problematic scenarios
    scenarios_prim = pd.read_csv("../data/output/EMA/scenariosPrim.csv")
    rp = pd.read_csv("../data/output/EMA/resultsScenariosPrim.csv")

    print(calculate_robustness_averted(rp))
    print(calculate_robustness_mean_variance(rp))
