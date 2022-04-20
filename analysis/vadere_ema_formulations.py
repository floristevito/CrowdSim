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
                                            wd='emaWorkingDirectory/')
    else:
        model = VadereModel('model',
                            vadere_jar='vadere-console.jar',
                            processor_files=[
                                'density.txt',
                                'speed.txt'
                            ],
                            model_file=model_file,
                            wd='emaWorkingDirectory/')
        # set the number of replications to handle model stochasticity
        model.replications = replications

    # make list with categories of group vector distribution
    groups = [
        Category(
            str(50 + num),
            [[round(0.5 - num/100, 2), round(0.38 + num/100, 2), 0.075, 0.03, 0.015] for i in range(4) ])
            for num in range(0, 36)
    ]

    # id 1 describes a configuration with all 10 uncertainties and single
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
                name='spawnFrequencyD',
                lower_bound=1,
                upper_bound=5,
                variable_name=[
                    '("scenario", "topography", "sources", 3, "distributionParameters", "updateFrequency")',
                ]
            ),
            CategoricalParameter(
                name='groupForming',
                categories=groups,
                variable_name=[
                    '("scenario", "topography", "sources", 0, "groupSizeDistribution")',
                    '("scenario", "topography", "sources", 1, "groupSizeDistribution")',
                    '("scenario", "topography", "sources", 2, "groupSizeDistribution")',
                    '("scenario", "topography", "sources", 3, "groupSizeDistribution")',
                    ],
                multivalue=True
            ),
            RealParameter(
                name='meanFreeFlowSpeed',
                lower_bound=0.66,
                upper_bound=1.16,
                variable_name=[
                    '("scenario", "topography", "attributesPedestrian", "speedDistributionMean")',
                ]
            ),
            RealParameter(
                name='sdFreeFlowSpeed',
                lower_bound=0.15,
                upper_bound=0.30,
                variable_name=[
                    '("scenario", "topography", "attributesPedestrian", "speedDistributionStandardDeviation")',
                ]
            ),
            RealParameter(
                name='pedPotentialHeight',
                lower_bound=5.0,
                upper_bound=50.0,
                variable_name=[
                    '("scenario", "attributesModel", "org.vadere.state.attributes.models.AttributesPotentialCompactSoftshell", "pedPotentialHeight")',
                ]
            ),
            RealParameter(
                name='obstPotentialHeight',
                lower_bound=2.0,
                upper_bound=10.0,
                variable_name=[
                    '("scenario", "attributesModel", "org.vadere.state.attributes.models.AttributesPotentialCompactSoftshell", "obstPotentialHeight")',
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
                    name='meanDensityArea2',
                    variable_name='mean_density_counting_normed_processor-PID9',
                ),
                ScalarOutcome(
                    name='maxDensityArea2',
                    variable_name='max_density_counting_normed_processor-PID10',
                ),
                ScalarOutcome(
                    name='meanDensityArea3',
                    variable_name='mean_density_counting_normed_processor-PID12',
                ),
                ScalarOutcome(
                    name='maxDensityArea3',
                    variable_name='max_density_counting_normed_processor-PID13',
                ),
                ScalarOutcome(
                    name='meanDensityArea4',
                    variable_name='mean_density_counting_normed_processor-PID15',
                ),
                ScalarOutcome(
                    name='maxDensityArea4',
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
                    name='meanDensityArea2',
                    variable_name='mean_density_counting_normed_processor-PID9',
                    function=np.mean
                ),
                ScalarOutcome(
                    name='maxDensityArea2',
                    variable_name='max_density_counting_normed_processor-PID10',
                    function=np.mean
                ),
                ScalarOutcome(
                    name='meanDensityArea3',
                    variable_name='mean_density_counting_normed_processor-PID12',
                    function=np.mean
                ),
                ScalarOutcome(
                    name='maxDensityArea3',
                    variable_name='max_density_counting_normed_processor-PID13',
                    function=np.mean
                ),
                ScalarOutcome(
                    name='meanDensityArea4',
                    variable_name='mean_density_counting_normed_processor-PID15',
                    function=np.mean
                ),
                ScalarOutcome(
                    name='maxDensityArea4',
                    variable_name='max_density_counting_normed_processor-PID16',
                    function=np.mean
                ),
            ]

    # id 2 describes a configuration to find the worst case(s)
    # with all 10 uncertainties and single
    # speed outcome + 6 density based outcomes
    elif id == 2:
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
                name='spawnFrequencyD',
                lower_bound=1,
                upper_bound=5,
                variable_name=[
                    '("scenario", "topography", "sources", 3, "distributionParameters", "updateFrequency")',
                ]
            ),
            CategoricalParameter(
                name='groupForming',
                categories=groups,
                variable_name=[
                    '("scenario", "topography", "sources", 0, "groupSizeDistribution")',
                    '("scenario", "topography", "sources", 1, "groupSizeDistribution")',
                    '("scenario", "topography", "sources", 2, "groupSizeDistribution")',
                    '("scenario", "topography", "sources", 3, "groupSizeDistribution")',
                    ],
                multivalue=True
            ),
            RealParameter(
                name='meanFreeFlowSpeed',
                lower_bound=0.66,
                upper_bound=1.16,
                variable_name=[
                    '("scenario", "topography", "attributesPedestrian", "speedDistributionMean")',
                ]
            ),
            RealParameter(
                name='sdFreeFlowSpeed',
                lower_bound=0.15,
                upper_bound=0.30,
                variable_name=[
                    '("scenario", "topography", "attributesPedestrian", "speedDistributionStandardDeviation")',
                ]
            ),
            RealParameter(
                name='pedPotentialHeight',
                lower_bound=5.0,
                upper_bound=50.0,
                variable_name=[
                    '("scenario", "attributesModel", "org.vadere.state.attributes.models.AttributesPotentialCompactSoftshell", "pedPotentialHeight")',
                ]
            ),
            RealParameter(
                name='obstPotentialHeight',
                lower_bound=2.0,
                upper_bound=10.0,
                variable_name=[
                    '("scenario", "attributesModel", "org.vadere.state.attributes.models.AttributesPotentialCompactSoftshell", "obstPotentialHeight")',
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
                    kind=ScalarOutcome.MINIMIZE,
                    expected_range=(0,2.2)
                ),
                ScalarOutcome(
                    name='meanDensityArea1',
                    variable_name='mean_density_counting_normed_processor-PID6',
                    kind=ScalarOutcome.MAXIMIZE,
                    expected_range=(0,1)
                ),
                ScalarOutcome(
                    name='maxDensityArea1',
                    variable_name='max_density_counting_normed_processor-PID7',
                    kind=ScalarOutcome.MAXIMIZE,
                    expected_range=(0,1)
                ),
                ScalarOutcome(
                    name='meanDensityArea2',
                    variable_name='mean_density_counting_normed_processor-PID9',
                    kind=ScalarOutcome.MAXIMIZE,
                    expected_range=(0,1)
                ),
                ScalarOutcome(
                    name='maxDensityArea2',
                    variable_name='max_density_counting_normed_processor-PID10',
                    kind=ScalarOutcome.MAXIMIZE,
                    expected_range=(0,1)
                ),
                ScalarOutcome(
                    name='meanDensityArea3',
                    variable_name='mean_density_counting_normed_processor-PID12',
                    kind=ScalarOutcome.MAXIMIZE,
                    expected_range=(0,1)
                ),
                ScalarOutcome(
                    name='maxDensityArea3',
                    variable_name='max_density_counting_normed_processor-PID13',
                    kind=ScalarOutcome.MAXIMIZE,
                    expected_range=(0,1)
                ),
                ScalarOutcome(
                    name='meanDensityArea4',
                    variable_name='mean_density_counting_normed_processor-PID15',
                    kind=ScalarOutcome.MAXIMIZE,
                    expected_range=(0,1)
                ),
                ScalarOutcome(
                    name='maxDensityArea4',
                    variable_name='max_density_counting_normed_processor-PID16',
                    kind=ScalarOutcome.MAXIMIZE,
                    expected_range=(0,1)
                ),
            ]
        else:
            model.outcomes = [
                ScalarOutcome(
                    name='meanSpeed',
                    variable_name='mean_area_speed_processor-PID4',
                    function=np.mean,
                    kind=ScalarOutcome.MINIMIZE,
                    expected_range=(0, 2.2)
                ),
                ScalarOutcome(
                    name='meanDensityArea1',
                    variable_name='mean_density_counting_normed_processor-PID6',
                    function=np.mean,
                    kind=ScalarOutcome.MAXIMIZE,
                    expected_range=(0,1)
                ),
                ScalarOutcome(
                    name='maxDensityArea1',
                    variable_name='max_density_counting_normed_processor-PID7',
                    function=np.mean,
                    kind=ScalarOutcome.MAXIMIZE,
                    expected_range=(0,1)
                ),
                ScalarOutcome(
                    name='meanDensityArea2',
                    variable_name='mean_density_counting_normed_processor-PID9',
                    function=np.mean,
                    kind=ScalarOutcome.MAXIMIZE,
                    expected_range=(0,1)
                ),
                ScalarOutcome(
                    name='maxDensityArea2',
                    variable_name='max_density_counting_normed_processor-PID10',
                    function=np.mean,
                    kind=ScalarOutcome.MAXIMIZE,
                    expected_range=(0,1)
                ),
                ScalarOutcome(
                    name='meanDensityArea3',
                    variable_name='mean_density_counting_normed_processor-PID12',
                    function=np.mean,
                    kind=ScalarOutcome.MAXIMIZE,
                    expected_range=(0,1)
                ),
                ScalarOutcome(
                    name='maxDensityArea3',
                    variable_name='max_density_counting_normed_processor-PID13',
                    function=np.mean,
                    kind=ScalarOutcome.MAXIMIZE,
                    expected_range=(0,1)
                ),
                ScalarOutcome(
                    name='meanDensityArea4',
                    variable_name='mean_density_counting_normed_processor-PID15',
                    function=np.mean,
                    kind=ScalarOutcome.MAXIMIZE,
                    expected_range=(0,1)
                ),
                ScalarOutcome(
                    name='maxDensityArea4',
                    variable_name='max_density_counting_normed_processor-PID16',
                    function=np.mean,
                    kind=ScalarOutcome.MAXIMIZE,
                    expected_range=(0,1)
                ),
            ]

    # id 3 is for original seed analysis, without replications
    # speed outcome + 2 density based outcomes for area 1
    elif id == 3:
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
                name='spawnFrequencyD',
                lower_bound=1,
                upper_bound=5,
                variable_name=[
                    '("scenario", "topography", "sources", 3, "distributionParameters", "updateFrequency")',
                ]
            ),
            # groups are removed as uncertainty, default value implemented in .scenario file
            # CategoricalParameter(
            #     name='groupForming',
            #     categories=groups,
            #     variable_name=[
            #         '("scenario", "topography", "sources", 0, "groupSizeDistribution")',
            #         '("scenario", "topography", "sources", 1, "groupSizeDistribution")',
            #         '("scenario", "topography", "sources", 2, "groupSizeDistribution")',
            #         '("scenario", "topography", "sources", 3, "groupSizeDistribution")',
            #         ],
            #     multivalue=True
            # ),
            RealParameter(
                name='meanFreeFlowSpeed',
                lower_bound=0.66,
                upper_bound=1.16,
                variable_name=[
                    '("scenario", "topography", "attributesPedestrian", "speedDistributionMean")',
                ]
            ),
            RealParameter(
                name='sdFreeFlowSpeed',
                lower_bound=0.15,
                upper_bound=0.30,
                variable_name=[
                    '("scenario", "topography", "attributesPedestrian", "speedDistributionStandardDeviation")',
                ]
            ),
            RealParameter(
                name='pedPotentialHeight',
                lower_bound=5.0,
                upper_bound=50.0,
                variable_name=[
                    '("scenario", "attributesModel", "org.vadere.state.attributes.models.AttributesPotentialCompactSoftshell", "pedPotentialHeight")',
                ]
            ),
            RealParameter(
                name='obstPotentialHeight',
                lower_bound=2.0,
                upper_bound=10.0,
                variable_name=[
                    '("scenario", "attributesModel", "org.vadere.state.attributes.models.AttributesPotentialCompactSoftshell", "obstPotentialHeight")',
                ]
            )
        ]
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
                )
        ]
    # id 4 is for additional seed analysis, with replications
    # speed outcome + 2 density based outcomes for area 1
    elif id == 4:
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
                name='spawnFrequencyD',
                lower_bound=1,
                upper_bound=5,
                variable_name=[
                    '("scenario", "topography", "sources", 3, "distributionParameters", "updateFrequency")',
                ]
            ),
            # groups are removed as uncertainty, default value implemented in .scenario file
            # CategoricalParameter(
            #     name='groupForming',
            #     categories=groups,
            #     variable_name=[
            #         '("scenario", "topography", "sources", 0, "groupSizeDistribution")',
            #         '("scenario", "topography", "sources", 1, "groupSizeDistribution")',
            #         '("scenario", "topography", "sources", 2, "groupSizeDistribution")',
            #         '("scenario", "topography", "sources", 3, "groupSizeDistribution")',
            #         ],
            #     multivalue=True
            # ),
            RealParameter(
                name='meanFreeFlowSpeed',
                lower_bound=0.66,
                upper_bound=1.16,
                variable_name=[
                    '("scenario", "topography", "attributesPedestrian", "speedDistributionMean")',
                ]
            ),
            RealParameter(
                name='sdFreeFlowSpeed',
                lower_bound=0.15,
                upper_bound=0.30,
                variable_name=[
                    '("scenario", "topography", "attributesPedestrian", "speedDistributionStandardDeviation")',
                ]
            ),
            RealParameter(
                name='pedPotentialHeight',
                lower_bound=5.0,
                upper_bound=50.0,
                variable_name=[
                    '("scenario", "attributesModel", "org.vadere.state.attributes.models.AttributesPotentialCompactSoftshell", "pedPotentialHeight")',
                ]
            ),
            RealParameter(
                name='obstPotentialHeight',
                lower_bound=2.0,
                upper_bound=10.0,
                variable_name=[
                    '("scenario", "attributesModel", "org.vadere.state.attributes.models.AttributesPotentialCompactSoftshell", "obstPotentialHeight")',
                ]
            )
        ]
        model.outcomes = [
            ScalarOutcome(
                    name='AverageMeanSpeed',
                    variable_name='mean_area_speed_processor-PID4',
                    function=np.mean
            ),
            ScalarOutcome(
                    name='StdMeanSpeed',
                    variable_name='mean_area_speed_processor-PID4',
                    function=np.std
            ),
            ScalarOutcome(
                name='AverageMeanDensityArea1',
                variable_name='mean_density_counting_normed_processor-PID6',
                function=np.mean
            ),
            ScalarOutcome(
                name='stdMeanDensityArea1',
                variable_name='mean_density_counting_normed_processor-PID6',
                function=np.std
            ),
            ScalarOutcome(
                name='MeanMaxDensityArea1',
                variable_name='max_density_counting_normed_processor-PID7',
                function=np.mean
            ),
            ScalarOutcome(
                name='stdMaxDensityArea1',
                variable_name='max_density_counting_normed_processor-PID7',
                function=np.std
            )
        ]

    else:
        raise ValueError('no valid id specified')

    return model
