from ema_workbench import (TimeSeriesOutcome, perform_experiments,
                           RealParameter, ema_logging, CategoricalParameter,
                           MultiprocessingEvaluator, SequentialEvaluator,
                           ScalarOutcome, IntegerParameter, Scenario)
from ema_workbench.em_framework.parameters import (Category)
from ema_workbench.connectors.vadere import VadereModel

model = VadereModel('model', 
                    vadere_jar='vadere-console.jar',
                    processor_files=[
                        'density.txt',
                        'speed.txt'
                    ],
                    model_file='base_case.scenario',
                    wd='/home/tevito/Documents/EPA/Year2/thesis/git/CrowdSim/analysis/emaWorkingDirectory')

# set up base case values
base = {
    '("scenario", "topography", "sources", 0, "spawnNumber")': 75,
    '("scenario", "topography", "sources", 0, "maxSpawnNumberTotal")': 75,
    '("scenario", "topography", "sources", 1, "spawnNumber")': 20,
    '("scenario", "topography", "sources", 1, "maxSpawnNumberTotal")': 20,
    '("scenario", "topography", "sources", 2, "spawnNumber")': 75,
    '("scenario", "topography", "sources", 2, "maxSpawnNumberTotal")': 75,
    '("scenario", "topography", "sources", 3, "spawnNumber")': 20,
    '("scenario", "topography", "sources", 3, "maxSpawnNumberTotal")': 20,
    '("scenario", "topography", "attributesPedestrian", "speedDistributionMean")': 1.34,
    '("scenario", "topography", "attributesPedestrian", "speedDistributionStandardDeviation")': 0.26
}

# set one uncertainty 
base_case = Scenario('base_case', **base)

model.outcomes = [
    ScalarOutcome('mean_area_speed_processor-PID4'),
    ScalarOutcome('mean_density_counting_normed_processor-PID6'),
    ScalarOutcome('mean_density_counting_normed_processor-PID8'),
    ScalarOutcome('mean_density_counting_normed_processor-PID10'),
    ScalarOutcome('max_density_counting_normed_processor-PID11'),
    ScalarOutcome('max_density_counting_normed_processor-PID12'),
    ScalarOutcome('max_density_counting_normed_processor-PID13'),
]
def get_base_scenarios(n):
    return [Scenario('base_case', **base) for i in range(n)]

if __name__ == '__main__':

    ema_logging.log_to_stderr(ema_logging.INFO)

    with MultiprocessingEvaluator(model, n_processes=8) as evaluator:
        results = evaluator.perform_experiments(get_base_scenarios(25))