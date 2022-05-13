import matplotlib.pyplot as plt
import pandas as pd
from ema_workbench import load_results

from robustness import calculate_robustness_averted, calculate_robustness_mean_variance

if __name__ == "__main__":

    # load results as DataFrame for each control strategy
    r_zero = pd.read_csv("../data/output/EMA/resultsScenariosPrim.csv").drop(
        columns=["Unnamed: 0"], axis=1
    )
    controlGuidance100 = load_results("../data/output/EMA/controlGuidance100.tar.gz")
    r_controlGuidance100 = pd.DataFrame(controlGuidance100[1])
    controlObjects = load_results("../data/output/EMA/controlObjects.tar.gz")
    r_controlObjects = pd.DataFrame(controlObjects[1])
    controlRegulators = load_results("../data/output/EMA/controlRegulators.tar.gz")
    r_controlRegulators = pd.DataFrame(controlRegulators[1])

    # calculate robustness scores
    rob_averted_zero = calculate_robustness_averted(r_zero)
    rob_variance_zero = calculate_robustness_mean_variance(r_zero)
    rob_averted_guidance100 = calculate_robustness_averted(r_controlGuidance100)
    rob_variance_guidance100 = calculate_robustness_mean_variance(r_controlGuidance100)
    rob_averted_objects = calculate_robustness_averted(r_controlObjects)
    rob_variance_objects = calculate_robustness_mean_variance(r_controlObjects)
    rob_averted_regulators = calculate_robustness_averted(r_controlRegulators)
    rob_variance_regulators = calculate_robustness_mean_variance(r_controlRegulators)

    # merge results
    r_averted = (
        pd.DataFrame(
            [
                rob_averted_zero,
                rob_averted_guidance100,
                rob_averted_objects,
                rob_averted_regulators,
            ]
        )
        .assign(strategy=["zero", "guidance100", "guidance25", "objects", "regulators"])
        .set_index("strategy")
    )
    r_averted.to_csv("../data/output/intermediate/r_averted.csv")
    r_mean_variance = (
        pd.DataFrame(
            [
                rob_variance_zero,
                rob_variance_guidance100,
                rob_variance_objects,
                rob_variance_regulators,
            ]
        )
        .assign(strategy=["zero", "guidance100", "guidance25", "objects", "regulators"])
        .set_index("strategy")
    )
    r_mean_variance.to_csv("../data/output/intermediate/r_mean_variance.csv")
    raw_outcomes_av = (
        pd.DataFrame()
        .assign(zero=r_zero.mean())
        .assign(guidance100=r_controlGuidance100.mean())
        .assign(objects=r_controlObjects.mean())
        .assign(regulators=r_controlRegulators.mean())
    )
    raw_outcomes_av.to_csv("../data/output/intermediate/raw_outcomes_av.csv")

    # plotting raw outcomes
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    raw_outcomes_av.loc[
        raw_outcomes_av.index.isin(
            [
                "meanDensityArea1",
                "meanDensityArea2",
                "meanDensityArea3",
                "meanDensityArea4",
            ]
        )
    ].plot.bar(ax=ax1, colormap="viridis", rot=0)
    fig1.suptitle("Control strategies \n raw mean density", fontsize=20)
    ax1.set(ylabel="average density [#/m²]")
    fig1.savefig("../figures/controlStrategiesRawMeanDensity.png", bbox_inches="tight")

    fig2, ax2 = plt.subplots(figsize=(8, 6))
    raw_outcomes_av.loc[
        raw_outcomes_av.index.isin(
            [
                "maxDensityArea1",
                "maxDensityArea2",
                "maxDensityArea3",
                "maxDensityArea4",
            ]
        )
    ].plot.bar(ax=ax2, colormap="viridis", rot=0)
    fig2.suptitle("Control strategies \n raw max density", fontsize=20)
    ax2.set(ylabel="max density [#/m²]")
    fig2.savefig("../figures/controlStrategiesRawMaxDensity.png", bbox_inches="tight")

    fig3, ax3 = plt.subplots(figsize=(12, 7))
    raw_outcomes_av.loc[raw_outcomes_av.index == "meanSpeed"].plot.barh(
        ax=ax3, colormap="viridis"
    )
    fig3.suptitle("Control strategies \n mean speed", fontsize=20)
    ax3.set(xlabel="mean speed [m/s]")
    fig3.savefig("../figures/controlStrategiesRawMeanSpeed.png", bbox_inches="tight")

    # plotting robustness averted
    fig4, ax4 = plt.subplots(figsize=(12, 7))
    r_averted[["complete scenarios averted", "number of averted areas"]].plot.barh(
        ax=ax4, colormap="viridis", rot=0
    )
    fig4.suptitle("Control strategies \n robustness: total averted", fontsize=20)
    ax4.set(xlabel="Total count", ylabel="Control strategy")
    fig4.savefig("../figures/controlStrategiesAverted.png", bbox_inches="tight")

    # plotting robustness mean variance
    fig5, ax5 = plt.subplots(figsize=(12, 7))
    r_mean_variance[["meanSpeed"]].plot.barh(ax=ax5, colormap="viridis", rot=0)
    fig5.suptitle("Control strategies \n robustness: mean variance", fontsize=20)
    ax5.set(
        xlabel="Mean variance score \n (higher is better)", ylabel="Control strategy"
    )
    fig5.savefig(
        "../figures/controlStrategiesMeanVarianceSpeed.png", bbox_inches="tight"
    )

    fig6, ax6 = plt.subplots(figsize=(8, 10))
    r_mean_variance[
        ["meanDensityArea1", "meanDensityArea2", "meanDensityArea3", "meanDensityArea4"]
    ].T.plot.barh(ax=ax6, colormap="viridis", rot=0)
    fig6.suptitle("Control strategies \n robustness: mean variance", fontsize=20)
    ax6.set(xlabel="Mean variance score \n (lower is better)")
    fig6.savefig(
        "../figures/controlStrategiesMeanVarianceMeanDensity.png", bbox_inches="tight"
    )

    fig7, ax7 = plt.subplots(figsize=(8, 10))
    r_mean_variance[
        ["maxDensityArea1", "maxDensityArea2", "maxDensityArea3", "maxDensityArea4"]
    ].T.plot.barh(ax=ax7, colormap="viridis", rot=0)
    fig7.suptitle("Control strategies \n robustness: mean variance", fontsize=20)
    ax7.set(xlabel="Mean variance score \n (lower is better)")
    fig7.savefig(
        "../figures/controlStrategiesMeanVarianceMaxDensity.png", bbox_inches="tight"
    )
