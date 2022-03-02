from concurrent.futures import process
import os
import numpy
import suqc
import pandas as pd
from functools import reduce
import operator
from ast import literal_eval
import json
from subprocess import PIPE, run
import shutil
from ema_workbench.em_framework.model import Replicator, SingleReplication
from ema_workbench.em_framework.outcomes import TimeSeriesOutcome
from ..em_framework.model import FileModel
from ..util.ema_logging import method_logger

__all__ = ['VadereModel']

def change_vadere_scenario(model_file, variable, value):
    """
    Change variable in vadere .scenario file structure. Note that a vadere scenario takes the format of a nested directory. 
    This function enables to modify any variable in the .scenario file, given the exact level of nesting.

    Parameters
    ----------
    model_file : dict
                loaded Vadere .scenario file, use json.load to load the file as dict
    variable : tuple
                the level of the nested variable that needs to be updates. This should be 
                provided as tuple. So for example, dict['x']['y'][5]['z'] should be provided as
                ('x', 'y', 5, 'z').
    value : float
            new value for the variable.

    """
    index = literal_eval(variable)
    reduce(operator.getitem, index[:-1], model_file)[index[-1]] = value

def update_vadere_scenario(model_file, experiment):
    """
    Load a vadere .scenario file, change it depending on the passed experiment, and save it again as .scenario file.

    Parameters
    ----------
    model_file : str
                path to the vadere .scenario file
    experiment : dict
                EMA experiment object

    """
    with open(model_file, 'r') as file:
        v_model = json.load(file)
    
    for key, value in experiment.items():
        change_vadere_scenario(v_model, key, value)
    
    with open(model_file, 'w') as file:
        json.dump(v_model, file)


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

    def __init__(self, name, vadere_jar, processor_files, wd, model_file):
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
        processor_files : list
                    list of output file names stored by Vadere, depending
                    on set processors. A .csv file is assumed for timeseries output,
                    and a .txt for a scaler output.

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
        self.processor_files = processor_files

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
        # set up the run command for Vadere
        self.vadere = [
            'java',
            '-jar',
            os.path.join(self.working_directory, self.vadere_jar),
            'scenario-run',
            '-f',
            os.path.join(self.working_directory, self.model_file),
        ]
    @method_logger(__name__)
    def run_experiment(self, experiment):
        """
        Method for running an instantiated model structure.

        Parameters
        ----------
        experiment : dict like

        """
        # change the .vadere scenario model file depending on the passed experiment
        update_vadere_scenario(os.path.join(self.working_directory, self.model_file), experiment)
        
        # run the experiment
        process = run(
            self.vadere,
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE
            )

        # load results
        # .csv is assumed to be timeseries, .txt scaler
        # other file types are ignored
        timeseries_res = {}
        scalar_res = []
        for file in self.processor_files:
            if file.endswith('.csv'):
                timeseries_res[file] = pd.read_csv(os.path.join(self.working_directory, file))
            if file.endswith('.txt'):
                scalar_res.append(os.path.join(self.working_directory, file)) 
        

        # format data to EMA structure
        res = {}
        # handle timeseries
        if len(timeseries_res) > 1:
            timeseries_total = pd.concat([results[outcome] for outcome in timeseries_res])
        else:
            timeseries_total = timeseries_res[next(iter(timeseries_res))]
        # drop the timestep column
        timeseries_total.drop('timeStep', axis=1, inplace=True)
        # format according to EMA preference
        res = {col: series.values for col,
                            series in timeseries_total.iteritems()}

        # handle scalar
        for file in scalar_res:
            with open(file, 'r'):
                name = file.readline().strip()
                value = file.readline().strip()
            res[name] = value

        return res

    def cleanup(self):
            """
            This model is called after finishing all the experiments, but
            just prior to returning the results. This method gives a hook for
            doing any cleanup, such as closing applications.

            In case of running in parallel, this method is called during
            the cleanup of the pool, just prior to removing the temporary
            directories.

            """
            for file in self.processor_files:
                try:
                    shutil.rmtree(os.path.join(self.working_directory, file))
                except OSError:
                    pass

class VadereModel(SingleReplication, BaseVadereModel):
    pass
