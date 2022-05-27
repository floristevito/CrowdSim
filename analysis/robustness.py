import pandas as pd
from ema_workbench import load_results


def calculate_robustness_averted(results):
    """calculation of the averted density areas robustness metric

    Args:
        results (df): pd DataFrame with experimental results

    Returns:
        dict: absolute and mean averted density areas,
            absolute and percentage completly averted cases
    """

    # make copy of original results
    r = results.copy()

    # evaluate per area per row if critical density is averted
    r["boolean1"] = r["maxDensityArea1"] <= 1
    r["boolean2"] = r["maxDensityArea2"] <= 1
    r["boolean3"] = r["maxDensityArea3"] <= 1
    r["boolean4"] = r["maxDensityArea4"] <= 1

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
        "complete cases averted": sum(r["averted"] == 4),
        "percentage_cases_averted": round(sum(r["averted"] == 4) / len(r), 2),
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
    r_maxDensityArea1 = (
        results["maxDensityArea1"].mean() * results["maxDensityArea1"].std()
    )
    r_maxDensityArea2 = (
        results["maxDensityArea2"].mean() * results["maxDensityArea2"].std()
    )
    r_maxDensityArea3 = (
        results["maxDensityArea3"].mean() * results["maxDensityArea3"].std()
    )
    r_maxDensityArea4 = (
        results["maxDensityArea4"].mean() * results["maxDensityArea4"].std()
    )

    # return final scores in a dict
    return {
        "meanSpeed": r_meanSpeed,
        "maxDensityArea1": r_maxDensityArea1,
        "maxDensityArea2": r_maxDensityArea2,
        "maxDensityArea3": r_maxDensityArea3,
        "maxDensityArea4": r_maxDensityArea4,
    }


if __name__ == "__main__":
    # load results PRIM problematic cases
    cases_prim = pd.read_csv("../data/output/EMA/casesPrim.csv")
    rp = pd.read_csv("../data/output/EMA/resultscasesPrim.csv")

    print(calculate_robustness_averted(rp))
    print(calculate_robustness_mean_variance(rp))
