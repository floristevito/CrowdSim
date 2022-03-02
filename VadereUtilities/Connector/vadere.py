import os
import numpy
import suqc
import pandas as pd
from ema_workbench.em_framework.model import Replicator, SingleReplication
from ema_workbench.em_framework.outcomes import TimeSeriesOutcome
from ..em_framework.model import FileModel
from ..util.ema_logging import method_logger

__all__ = ['VadereModel']


class BaseVadereModel(FileModel):
    """Base class for interfacing with Vadere models. This class
    extends :class:`em_framework.ModelStructureInterface`.

    Attributes
    ----------
    model_file : str
                a relative path from the working directory
                to the model scenario file
    working_directory : str
    name : str

    """

    def __init__(self, name, vadere_jar, qoi, wd, model_file,
                 gui=False):
        """
        init of class

        Parameters
        ----------
        wd   : str
               working directory for the model.
        name : str
               name of the modelInterface. The name should contain only
               alpha-numerical characters.
        vadere_jar : str
               a relative path from the working directory
                to the Vadere console jar file
        qoi : list
               variables to be tracked. The names should correspond to
               Vadere output files (e.g. 'overlaps.csv'). At least
               one item is required.
        gui : bool, optional
               If true, displays the Vadere GUI

        Raises
        ------
        EMAError if name contains non alpha-numerical characters

        Note
        ----
        Anything that is relative to `self.working_directory`should be
        specified in `model_init` and not in `src`. Otherwise, the code
        will not work when running it in parallel. The reason for this is that
        the working directory is being updated by parallelEMA to the worker's
        separate working directory prior to calling `model_init`.

        """
        super(BaseVadereModel, self).__init__(name, wd=wd,
                                              model_file=model_file)

        self.vadere_jar = vadere_jar
        self.qoi = qoi
        self.gui = gui

    @method_logger(__name__)
    def model_init(self, policy):
        """
        Method called to initialize the model.

        Parameters
        ----------
        policy : dict
                 policy to be run.


        """
        super(BaseVadereModel, self).model_init(policy)
        # Vadere suqc has no seperate connect method without experiment data,
        # instead the correct paths will be set here for functional parallel processing
        self.vadere_model_file_path = os.path.join(self.working_directory,
                                        self.model_file)
        self.vadere_jar_path = os.path.join(self.working_directory,
                                        self.vadere_jar)
        self.vadere_output_path = os.path.join(self.working_directory)
    @method_logger(__name__)
    def run_experiment(self, experiment):
        """
        Method for running an instantiated model structure.

        Parameters
        ----------
        experiment : dict like

        """
        # make copy of qoi list, to avoid clearance after Vadere run
        qoi = self.qoi.copy()

        # run model
        # note that suqc requires a dict within a list for the experiment
        print(self.vadere_output_path)
        par, results = suqc.DictVariation(
            scenario_path=self.vadere_model_file_path,
            parameter_dict_list=[experiment], 
            qoi=qoi,
            model=self.vadere_jar_path,
            output_path=self.vadere_output_path,
            remove_output=True,
        ).run()

        # merge dataframes if results include multiple
        if len(results) > 1:
            output_total = pd.concat([results[outcome] for outcome in results])
        else:
            output_total = results[next(iter(results))]
        # drop the first and second index column
        res = output_total.droplevel([1,2])
        # format according to EMA preference
        res = {col: tuple(series.values) for col,
                            series in res.iteritems()}
        return res


class VadereModel(SingleReplication, BaseVadereModel):
    pass
