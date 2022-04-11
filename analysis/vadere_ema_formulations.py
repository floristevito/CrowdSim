from ema_workbench import (
    RealParameter,
    CategoricalParameter,
    ScalarOutcome,
    IntegerParameter,
    RealParameter)
from ema_workbench.em_framework.parameters import Category
from ema_workbench.connectors.vadere import VadereModel, SingleReplicationVadereModel
import numpy as np


def get_vadere_formulation(id, replications, model_file):
    """reduce vadere problem formulations with simple function. Supports multiple configurations depedening on id.

    Args:
        id (int): id for problem configuration
        replications (int): number of model replications
        model_file (str): Vadere .scenario file, relative to wd

    Returns:
        model (EMA Model instance): the EMA Workbench Vadere formulation

    Raises:
        ValueError: if no valid id is given
    """
    # This model saves scalar results to a density.txt and speed.txt file.
    # check if replications is 1, then take single rep model
    if replications == 1:
        model = SingleReplicationVadereModel('model',
                                            vadere_jar='vadere-console.jar',
                                            processor_files=[
                                                'density.txt',
                                                'speed.txt'
                                            ],
                                            model_file=model_file,
                                            wd='/home/tevito/Documents/EPA/Year2/thesis/git/CrowdSim/analysis/emaWorkingDirectory')
    else:
        model = VadereModel('model',
                            vadere_jar='vadere-console.jar',
                            processor_files=[
                                'density.txt',
                                'speed.txt'
                            ],
                            model_file=model_file,
                            wd='/home/tevito/Documents/EPA/Year2/thesis/thesis-drive/model/connector/output')
        # set the number of replications to handle model stochasticity
        model.replications = replications

    # id 1 described a configuration with all 10 uncertainties and single
    # speed outcome + 6 density based outcomes
    if id == 1:
        model.uncertainties = [
            IntegerParameter(
                name='spawnFrequencyA',
                lower_bound=1,
                upper_bound=5,
                variable_name=[
                    '("scenario", "topography", "sources", 0, "distributionParameters", "updateFrequency")',
                ]
            ),
            IntegerParameter(
                name='spawnFrequencyB',
                lower_bound=1,
                upper_bound=5,
                variable_name=[
                    '("scenario", "topography", "sources", 1, "distributionParameters", "updateFrequency")',
                ]
            ),
            IntegerParameter(
                name='spawnFrequencyC',
                lower_bound=1,
                upper_bound=5,
                variable_name=[
                    '("scenario", "topography", "sources", 2, "distributionParameters", "updateFrequency")',
                ]
            ),
            IntegerParameter(
                name='spawnFrequencyA',
                lower_bound=1,
                upper_bound=5,
                variable_name=[
                    '("scenario", "topography", "sources", 3, "distributionParameters", "updateFrequency")',
                ]
            ),
            RealParameter(
                name='μFreeFlowSpeed',
                lower_bound=0.66,
                upper_bound=1.16,
                variable_name=[
                    '("scenario", "topography", "attributesPedestrian", "speedDistributionMean")',
                ]
            ),
            RealParameter(
                name='pedPotentialHeight',
                lower_bound=5.0,
                upper_bound=50.0,
                variable_name=[
                    '("scenario", "attributesModel", "org.vadere.state.attributes.models.AttributesPotentialCompactSoftshell", "pedPotentialHeight")',
                ]
            )
        ]
        # if single replication model, no function on outcomes is needed
        # multiple replications are instead averaged by np.mean
        if replications == 1:
            model.outcomes = [
                ScalarOutcome(
                    name='meanSpeed',
                    variable_name='mean_area_speed_processor-PID4',
                ),
                ScalarOutcome(
                    name='meanDensityArea1',
                    variable_name='mean_density_counting_normed_processor-PID6',
                ),
                ScalarOutcome(
                    name='maxDensityArea1',
                    variable_name='max_density_counting_normed_processor-PID7',
                ),
                ScalarOutcome(
                    name='meanDensityArea1',
                    variable_name='mean_density_counting_normed_processor-PID9',
                ),
                ScalarOutcome(
                    name='maxDensityArea1',
                    variable_name='max_density_counting_normed_processor-PID10',
                ),
                ScalarOutcome(
                    name='meanDensityArea1',
                    variable_name='mean_density_counting_normed_processor-PID12',
                ),
                ScalarOutcome(
                    name='maxDensityArea1',
                    variable_name='max_density_counting_normed_processor-PID13',
                ),
                ScalarOutcome(
                    name='meanDensityArea1',
                    variable_name='mean_density_counting_normed_processor-PID15',
                ),
                ScalarOutcome(
                    name='maxDensityArea1',
                    variable_name='max_density_counting_normed_processor-PID16',
                ),
            ]
        else:
            model.outcomes = [
                ScalarOutcome(
                    name='meanSpeed',
                    variable_name='mean_area_speed_processor-PID4',
                    function=np.mean
                ),
                ScalarOutcome(
                    name='meanDensityArea1',
                    variable_name='mean_density_counting_normed_processor-PID6',
                    function=np.mean
                ),
                ScalarOutcome(
                    name='maxDensityArea1',
                    variable_name='max_density_counting_normed_processor-PID7',
                    function=np.mean
                ),
                ScalarOutcome(
                    name='meanDensityArea1',
                    variable_name='mean_density_counting_normed_processor-PID9',
                    function=np.mean
                ),
                ScalarOutcome(
                    name='maxDensityArea1',
                    variable_name='max_density_counting_normed_processor-PID10',
                    function=np.mean
                ),
                ScalarOutcome(
                    name='meanDensityArea1',
                    variable_name='mean_density_counting_normed_processor-PID12',
                    function=np.mean
                ),
                ScalarOutcome(
                    name='maxDensityArea1',
                    variable_name='max_density_counting_normed_processor-PID13',
                    function=np.mean
                ),
                ScalarOutcome(
                    name='meanDensityArea1',
                    variable_name='mean_density_counting_normed_processor-PID15',
                    function=np.mean
                ),
                ScalarOutcome(
                    name='maxDensityArea1',
                    variable_name='max_density_counting_normed_processor-PID16',
                    function=np.mean
                ),
            ]
    else:
        raise ValueError('no valid id specified')

    return model
