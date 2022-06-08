import matplotlib.pyplot as plt
import pandas as pd
from ema_workbench import load_results

from robustness import calculate_robustness_averted, calculate_robustness_mean_variance

if __name__ == "__main__":

    # load results as DataFrame for each Measure and set of cases
    s1_zero = pd.read_csv("../data/output/EMA/resultsCasesOeBad.csv").drop(
        columns=["Unnamed: 0"], axis=1
    )
    s1_controlGuidance100 = pd.DataFrame(
        load_results("../data/output/EMA/cases1controlGuidance100.tar.gz")[1]
    )
    s1_controlGuidance25 = pd.DataFrame(
        load_results("../data/output/EMA/cases1controlGuidance25.tar.gz")[1]
    )
    s1_controlObjects = pd.DataFrame(
        load_results("../data/output/EMA/cases1controlObjects.tar.gz")[1]
    )
    s1_controlRegulators = pd.DataFrame(
        load_results("../data/output/EMA/cases1controlRegulators.tar.gz")[1]
    )

    s2_zero = pd.read_csv("../data/output/EMA/resultsCasesOeGood.csv").drop(
        columns=["Unnamed: 0"], axis=1
    )
    s2_controlGuidance100 = pd.DataFrame(
        load_results("../data/output/EMA/cases2controlGuidance100.tar.gz")[1]
    )
    s2_controlGuidance25 = pd.DataFrame(
        load_results("../data/output/EMA/cases2controlGuidance25.tar.gz")[1]
    )
    s2_controlObjects = pd.DataFrame(
        load_results("../data/output/EMA/cases2controlObjects.tar.gz")[1]
    )
    s2_controlRegulators = pd.DataFrame(
        load_results("../data/output/EMA/cases2controlRegulators.tar.gz")[1]
    )

    s3_zero = pd.read_csv("../data/output/EMA/directedSearch.csv")
    s3_controlGuidance100 = pd.DataFrame(
        load_results("../data/output/EMA/cases3controlGuidance100.tar.gz")[1]
    )
    s3_controlGuidance25 = pd.DataFrame(
        load_results("../data/output/EMA/cases3controlGuidance25.tar.gz")[1]
    )
    s3_controlObjects = pd.DataFrame(
        load_results("../data/output/EMA/cases3controlObjects.tar.gz")[1]
    )
    s3_controlRegulators = pd.DataFrame(
        load_results("../data/output/EMA/cases3controlRegulators.tar.gz")[1]
    )

    # calculate robustness scores
    rob_averted_s1_zero = calculate_robustness_averted(s1_zero.head(100))
    rob_averted_s2_zero = calculate_robustness_averted(s2_zero.head(100))
    rob_averted_s3_zero = calculate_robustness_averted(s3_zero.head(100))

    rob_averted_s1_controlGuidance100 = calculate_robustness_averted(
        s1_controlGuidance100
    )
    rob_averted_s2_controlGuidance100 = calculate_robustness_averted(
        s2_controlGuidance100
    )
    rob_averted_s3_controlGuidance100 = calculate_robustness_averted(
        s3_controlGuidance100
    )

    rob_averted_s1_controlGuidance25 = calculate_robustness_averted(
        s1_controlGuidance25
    )
    rob_averted_s2_controlGuidance25 = calculate_robustness_averted(
        s2_controlGuidance25
    )
    rob_averted_s3_controlGuidance25 = calculate_robustness_averted(
        s3_controlGuidance25
    )

    rob_averted_s1_controlObjects = calculate_robustness_averted(s1_controlObjects)
    rob_averted_s2_controlObjects = calculate_robustness_averted(s2_controlObjects)
    rob_averted_s3_controlObjects = calculate_robustness_averted(s3_controlObjects)

    rob_averted_s1_controlRegulators = calculate_robustness_averted(
        s1_controlRegulators
    )
    rob_averted_s2_controlRegulators = calculate_robustness_averted(
        s2_controlRegulators
    )
    rob_averted_s3_controlRegulators = calculate_robustness_averted(
        s3_controlRegulators
    )

    rob_variance_s1_zero = calculate_robustness_mean_variance(s1_zero)
    rob_variance_s2_zero = calculate_robustness_mean_variance(s2_zero)
    rob_variance_s3_zero = calculate_robustness_mean_variance(s3_zero)

    rob_variance_s1_controlGuidance100 = calculate_robustness_mean_variance(
        s1_controlGuidance100
    )
    rob_variance_s2_controlGuidance100 = calculate_robustness_mean_variance(
        s2_controlGuidance100
    )
    rob_variance_s3_controlGuidance100 = calculate_robustness_mean_variance(
        s3_controlGuidance100
    )

    rob_variance_s1_controlGuidance25 = calculate_robustness_mean_variance(
        s1_controlGuidance25
    )
    rob_variance_s2_controlGuidance25 = calculate_robustness_mean_variance(
        s2_controlGuidance25
    )
    rob_variance_s3_controlGuidance25 = calculate_robustness_mean_variance(
        s3_controlGuidance25
    )

    rob_variance_s1_controlObjects = calculate_robustness_mean_variance(
        s1_controlObjects
    )
    rob_variance_s2_controlObjects = calculate_robustness_mean_variance(
        s2_controlObjects
    )
    rob_variance_s3_controlObjects = calculate_robustness_mean_variance(
        s3_controlObjects
    )

    rob_variance_s1_controlRegulators = calculate_robustness_mean_variance(
        s1_controlRegulators
    )
    rob_variance_s2_controlRegulators = calculate_robustness_mean_variance(
        s2_controlRegulators
    )
    rob_variance_s3_controlRegulators = calculate_robustness_mean_variance(
        s3_controlRegulators
    )

    # merge results
    r_averted_s1 = (
        pd.DataFrame(
            [
                rob_averted_s1_zero,
                rob_averted_s1_controlGuidance100,
                rob_averted_s1_controlGuidance25,
                rob_averted_s1_controlObjects,
                rob_averted_s1_controlRegulators,
            ]
        )
        .assign(strategy=["zero", "guidance100", "guidance25", "objects", "regulators"])
        .set_index("strategy")
    )
    r_averted_s2 = (
        pd.DataFrame(
            [
                rob_averted_s2_zero,
                rob_averted_s2_controlGuidance100,
                rob_averted_s2_controlGuidance25,
                rob_averted_s2_controlObjects,
                rob_averted_s2_controlRegulators,
            ]
        )
        .assign(strategy=["zero", "guidance100", "guidance25", "objects", "regulators"])
        .set_index("strategy")
    )
    r_averted_s3 = (
        pd.DataFrame(
            [
                rob_averted_s3_zero,
                rob_averted_s3_controlGuidance100,
                rob_averted_s3_controlGuidance25,
                rob_averted_s3_controlObjects,
                rob_averted_s3_controlRegulators,
            ]
        )
        .assign(strategy=["zero", "guidance100", "guidance25", "objects", "regulators"])
        .set_index("strategy")
    )
    r_mean_variance_s1 = (
        pd.DataFrame(
            [
                rob_variance_s1_zero,
                rob_variance_s1_controlGuidance100,
                rob_variance_s1_controlGuidance25,
                rob_variance_s1_controlObjects,
                rob_variance_s1_controlRegulators,
            ]
        )
        .assign(strategy=["zero", "guidance100", "guidance25", "objects", "regulators"])
        .set_index("strategy")
    )
    r_mean_variance_s2 = (
        pd.DataFrame(
            [
                rob_variance_s2_zero,
                rob_variance_s2_controlGuidance100,
                rob_variance_s2_controlGuidance25,
                rob_variance_s2_controlObjects,
                rob_variance_s2_controlRegulators,
            ]
        )
        .assign(strategy=["zero", "guidance100", "guidance25", "objects", "regulators"])
        .set_index("strategy")
    )
    r_mean_variance_s3 = (
        pd.DataFrame(
            [
                rob_variance_s3_zero,
                rob_variance_s3_controlGuidance100,
                rob_variance_s3_controlGuidance25,
                rob_variance_s3_controlObjects,
                rob_variance_s3_controlRegulators,
            ]
        )
        .assign(strategy=["zero", "guidance100", "guidance25", "objects", "regulators"])
        .set_index("strategy")
    )
    raw_outcomes_s1 = (
        pd.DataFrame()
        .assign(zero=s1_zero.mean())
        .assign(guidance100=s1_controlGuidance100.mean())
        .assign(guidance25=s1_controlGuidance25.mean())
        .assign(objects=s1_controlObjects.mean())
        .assign(regulators=s1_controlRegulators.mean())
    )
    raw_outcomes_s2 = (
        pd.DataFrame()
        .assign(zero=s2_zero.mean())
        .assign(guidance100=s2_controlGuidance100.mean())
        .assign(guidance25=s2_controlGuidance25.mean())
        .assign(objects=s2_controlObjects.mean())
        .assign(regulators=s2_controlRegulators.mean())
    )
    raw_outcomes_s3 = (
        pd.DataFrame()
        .assign(zero=s3_zero.mean())
        .assign(guidance100=s3_controlGuidance100.mean())
        .assign(guidance25=s3_controlGuidance25.mean())
        .assign(objects=s3_controlObjects.mean())
        .assign(regulators=s3_controlRegulators.mean())
    )

    # plotting raw max density scores
    fig, ax = plt.subplots(figsize=(8, 6))
    raw_outcomes_s1.loc[
        raw_outcomes_s1.index.isin(
            [
                "maxDensityArea1",
                "maxDensityArea2",
                "maxDensityArea3",
                "maxDensityArea4",
            ]
        )
    ].rename(
        index={
            "maxDensityArea1": "area 1",
            "maxDensityArea2": "area 2",
            "maxDensityArea3": "area 3",
            "maxDensityArea4": "area 4",
        }
    ).plot.bar(
        ax=ax, colormap="viridis", rot=0
    ).legend(
        prop={"size": 20}
    )
    fig.suptitle("Problematic cases \n raw max density", fontsize=22)
    ax.set_ylabel("max density [#/m²]", fontsize=22)
    plt.xticks(fontsize=22, weight="bold")
    fig.savefig("../figures/controlStrategiesRawMaxDensityS1.png", bbox_inches="tight")

    fig, ax = plt.subplots(figsize=(8, 6))
    raw_outcomes_s2.loc[
        raw_outcomes_s2.index.isin(
            [
                "maxDensityArea1",
                "maxDensityArea2",
                "maxDensityArea3",
                "maxDensityArea4",
            ]
        )
    ].rename(
        index={
            "maxDensityArea1": "area 1",
            "maxDensityArea2": "area 2",
            "maxDensityArea3": "area 3",
            "maxDensityArea4": "area 4",
        }
    ).plot.bar(
        ax=ax, colormap="viridis", rot=0
    ).legend(
        prop={"size": 20}
    )
    fig.suptitle("Good cases \n raw max density", fontsize=22)
    ax.set_ylabel("max density [#/m²]", fontsize=22)
    plt.xticks(fontsize=22, weight="bold")
    fig.savefig("../figures/controlStrategiesRawMaxDensityS2.png", bbox_inches="tight")

    fig, ax = plt.subplots(figsize=(8, 6))
    raw_outcomes_s3.loc[
        raw_outcomes_s3.index.isin(
            [
                "maxDensityArea1",
                "maxDensityArea2",
                "maxDensityArea3",
                "maxDensityArea4",
            ]
        )
    ].rename(
        index={
            "maxDensityArea1": "area 1",
            "maxDensityArea2": "area 2",
            "maxDensityArea3": "area 3",
            "maxDensityArea4": "area 4",
        }
    ).plot.bar(
        ax=ax, colormap="viridis", rot=0
    ).legend(
        prop={"size": 20}
    )
    fig.suptitle("worst cases \n raw max density", fontsize=22)
    ax.set_ylabel("max density [#/m²]", fontsize=22)
    plt.xticks(fontsize=22, weight="bold")
    fig.savefig("../figures/controlStrategiesRawMaxDensityS3.png", bbox_inches="tight")

    # plotting raw mean speed scores
    fig, ax = plt.subplots(figsize=(12, 7))
    raw_outcomes_s1.loc[raw_outcomes_s1.index == "meanSpeed"].plot.barh(
        ax=ax, colormap="viridis"
    )
    fig.suptitle("Problematic cases \n raw mean speed", fontsize=22)
    ax.set_xlabel("mean speed [m/s]", fontsize=22)
    plt.yticks([])
    fig.savefig("../figures/controlStrategiesRawMeanSpeedS1.png", bbox_inches="tight")

    fig, ax = plt.subplots(figsize=(12, 7))
    raw_outcomes_s2.loc[raw_outcomes_s2.index == "meanSpeed"].plot.barh(
        ax=ax, colormap="viridis"
    )
    fig.suptitle("Good cases \n raw mean speed", fontsize=22)
    ax.set_xlabel("mean speed [m/s]", fontsize=22)
    plt.yticks([])
    fig.savefig("../figures/controlStrategiesRawMeanSpeedS2.png", bbox_inches="tight")

    fig, ax = plt.subplots(figsize=(12, 7))
    raw_outcomes_s1.loc[raw_outcomes_s1.index == "meanSpeed"].plot.barh(
        ax=ax, colormap="viridis"
    )
    fig.suptitle("worst cases \n raw mean speed", fontsize=22)
    ax.set_xlabel("mean speed [m/s]", fontsize=22)
    plt.yticks([])
    fig.savefig("../figures/controlStrategiesRawMeanSpeedS3.png", bbox_inches="tight")

    # plotting robustness averted scores
    fig, ax = plt.subplots(figsize=(12, 7))
    r_averted_s1[["complete cases averted", "number of averted areas"]].plot.barh(
        ax=ax, colormap="viridis", rot=0
    ).legend(bbox_to_anchor=(0.25, 1.25), prop={"size": 20})
    fig.suptitle("Problematic cases \n robustness: total averted", fontsize=22)
    ax.set_xlabel("Total count", fontsize=22)
    ax.set_ylabel(ylabel="Measure", fontsize=22)
    plt.yticks(fontsize=22, weight="bold")
    fig.savefig("../figures/controlStrategiesAvertedS1.png", bbox_inches="tight")

    fig, ax = plt.subplots(figsize=(12, 7))
    r_averted_s2[["complete cases averted", "number of averted areas"]].plot.barh(
        ax=ax, colormap="viridis", rot=0
    ).legend(bbox_to_anchor=(0.25, 1.25), prop={"size": 20})
    fig.suptitle("Good cases \n robustness: total averted", fontsize=22)
    ax.set_xlabel("Total count", fontsize=22)
    ax.set_ylabel(ylabel="Measure", fontsize=22)
    plt.yticks(fontsize=22, weight="bold")
    fig.savefig("../figures/controlStrategiesAvertedS2.png", bbox_inches="tight")

    fig, ax = plt.subplots(figsize=(12, 7))
    r_averted_s3[["complete cases averted", "number of averted areas"]].plot.barh(
        ax=ax, colormap="viridis", rot=0
    ).legend(bbox_to_anchor=(0.25, 1.25), prop={"size": 20})
    fig.suptitle("worst cases", fontsize=22)
    ax.set_xlabel("Total count", fontsize=22)
    ax.set_ylabel(ylabel="Measure", fontsize=22)
    plt.yticks(fontsize=22, weight="bold")
    fig.savefig("../figures/controlStrategiesAvertedS3.png", bbox_inches="tight")

    # plotting robustness mean variance speed
    fig, ax = plt.subplots(figsize=(12, 7))
    r_mean_variance_s1[["meanSpeed"]].plot.barh(
        ax=ax, colormap="viridis", rot=0, legend=False
    )
    fig.suptitle("Problematic cases", fontsize=28)
    ax.set_xlabel("Mean variance score", fontsize=28)
    ax.set_ylabel("Measure", fontsize=28)
    plt.yticks(fontsize=28, weight="bold")
    fig.savefig(
        "../figures/controlStrategiesMeanVarianceSpeedS1.png", bbox_inches="tight"
    )
    fig, ax = plt.subplots(figsize=(12, 7))
    r_mean_variance_s2[["meanSpeed"]].plot.barh(
        ax=ax, colormap="viridis", rot=0, legend=False
    )
    fig.suptitle("Good cases", fontsize=28)
    ax.set_xlabel("Mean variance score", fontsize=28)
    ax.set_ylabel("Measure", fontsize=28)
    plt.yticks(fontsize=28, weight="bold")
    fig.savefig(
        "../figures/controlStrategiesMeanVarianceSpeedS2.png", bbox_inches="tight"
    )
    fig, ax = plt.subplots(figsize=(12, 7))
    r_mean_variance_s3[["meanSpeed"]].plot.barh(
        ax=ax, colormap="viridis", rot=0, legend=False
    )
    fig.suptitle("worst cases", fontsize=28)
    ax.set_xlabel("Mean variance score", fontsize=28)
    ax.set_ylabel("Measure", fontsize=28)
    plt.yticks(fontsize=28, weight="bold")
    fig.savefig(
        "../figures/controlStrategiesMeanVarianceSpeedS3.png", bbox_inches="tight"
    )

    # plotting robustness mean variance density
    fig, ax = plt.subplots(figsize=(14, 7))
    d1 = r_mean_variance_s1.T.rename(
        index={
            "maxDensityArea1": "area 1",
            "maxDensityArea2": "area 2",
            "maxDensityArea3": "area 3",
            "maxDensityArea4": "area 4",
        }
    ).drop("meanSpeed")
    d1.plot.bar(ax=ax, colormap="viridis", rot=0).legend(prop={"size": 20})
    fig.suptitle("Problematic cases", fontsize=28)
    ax.set_xlabel("Measure", fontsize=28)
    ax.set_ylabel("Mean variance score", fontsize=28)
    plt.xticks(fontsize=28, weight="bold")
    fig.savefig(
        "../figures/controlStrategiesMeanVarianceMaxDensityS1.png", bbox_inches="tight"
    )
    fig, ax = plt.subplots(figsize=(14, 7))
    d2 = r_mean_variance_s2.T.rename(
        index={
            "maxDensityArea1": "area 1",
            "maxDensityArea2": "area 2",
            "maxDensityArea3": "area 3",
            "maxDensityArea4": "area 4",
        }
    ).drop("meanSpeed")
    d2.plot.bar(ax=ax, colormap="viridis", rot=0).legend(prop={"size": 20})
    fig.suptitle("Good cases", fontsize=28)
    ax.set_xlabel("Measure", fontsize=28)
    ax.set_ylabel("Mean variance score", fontsize=28)
    plt.xticks(fontsize=28, weight="bold")
    fig.savefig(
        "../figures/controlStrategiesMeanVarianceMaxDensityS2.png", bbox_inches="tight"
    )
    fig, ax = plt.subplots(figsize=(14, 7))
    d3 = r_mean_variance_s3.T.rename(
        index={
            "maxDensityArea1": "area 1",
            "maxDensityArea2": "area 2",
            "maxDensityArea3": "area 3",
            "maxDensityArea4": "area 4",
        }
    ).drop("meanSpeed")
    d3.plot.bar(ax=ax, colormap="viridis", rot=0).legend(prop={"size": 20})
    fig.suptitle("Worst cases", fontsize=28)
    ax.set_xlabel("Measure", fontsize=28)
    ax.set_ylabel("Mean variance score", fontsize=28)
    plt.xticks(fontsize=28, weight="bold")
    fig.savefig(
        "../figures/controlStrategiesMeanVarianceMaxDensityS3.png", bbox_inches="tight"
    )
