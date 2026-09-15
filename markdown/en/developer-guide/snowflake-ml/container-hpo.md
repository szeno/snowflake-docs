# Parallel Hyperparameter Optimization (HPO) on Container Runtime

The Snowflake ML Hyperparameter Optimization (HPO) API is a model-agnostic framework that enables efficient,
parallelized hyperparameter tuning of models.
You can use any open-source framework or algorithm. You can also use Snowflake ML APIs.

You can use HPO in a Snowflake Notebook that’s configured to use the Container Runtime on Snowpark
Container Services (SPCS). After you [create such a notebook](/developer-guide/snowflake-ml/notebooks-on-spcs), you can:

- Train a model using any open source package, and use this API to distribute the hyperparameter tuning process
- Train a model using Snowflake ML distributed training APIs, and scale HPO while also scaling each of the training runs

The HPO workload that you initiate from your notebook executes inside Snowpark Container Services on either CPU or GPU
instances. The workload scales out to the CPU or GPU cores that are available on a single node in the SPCS compute pool.

The parallelized HPO API provides the following benefits:

- A single API that automatically handles all the complexities of distributing the training across multiple resources
- The ability to train with virtually any framework or algorithm using open-source ML frameworks or the Snowflake ML
  modeling APIs
- A selection of tuning and sampling options, including Bayesian and random search algorithms along with various
  continuous and non-continuous sampling functions
- Tight integration with the rest of Snowflake; for example efficient data ingestion via Snowflake Datasets or Dataframes
  and automatic ML lineage capture

Note

You can scale the HPO run to use multiple nodes in the SPCS compute pool.
For more information, see [Running a workload on a multi-node cluster](/developer-guide/snowflake-ml/container-runtime-multi-node#label-running-workload-multi-node-cluster).

## Optimize a model’s hyperparameters

Use Snowflake ML HPO API to tune a model. The following steps illustrate the process:

1. Ingest the data.
2. Use the search algorithm to define the strategy used to optimize the hyperparameters.
3. Define how the hyperparameters are sampled.
4. Configure the tuner.
5. Get the hyperparameters and training metrics from each training job.
6. Initiate the training job.
7. Get the training job results.

The following sections walk through the preceding steps. For an example, see [Container Runtime HPO Example](https://github.com/Snowflake-Labs/sf-samples/blob/main/samples/ml/container_runtime_hpo/hpo_example.ipynb).

### Ingest the data

Use the `dataset_map` object to ingest the data into the HPO API. The `dataset_map` object is a dictionary that pairs
the training or test dataset with its corresponding Snowflake DataConnector object. The `dataset_map` object is passed to the
training function. The following is an example of a `dataset_map` object:

Copy code

```
dataset_map = {
  "train": DataConnector.from_dataframe(session.create_dataframe(X_train)),
  "test": DataConnector.from_dataframe(session.create_dataframe(X_test)),

}
```

### Define the search algorithm

Define the search algorithm used to explore the hyperparameter space. The algorithm uses the outcomes of previous trials to determine how to configure the hyperparameters.
You can use the following search algorithms:

- Grid search

  Explores a grid for hyperparameter values that you define. The HPO API evaluates every possible combination of hyperparameters.
  The following is an example of a hyperparameter grid:

  Copy code

  ```
  search_space = {
   "n_estimators": [50, 51],
   "max_depth": [4, 5],
   "learning_rate": [0.01, 0.3],
  }
  ```

  In the preceding example, each parameter has two possible values. There are 8 (2 \* 2 \* 2) possible combinations of hyperparameters.
- Bayesian optimization

  Uses a probabilistic model to determine the next set of hyperparameters to evaluate. The algorithm uses the outcomes of previous trials to determine how to configure the hyperparameters. For more information about Bayesian optimization, see [Bayesian Optimization](https://github.com/bayesian-optimization/BayesianOptimization).
- Random search

  Randomly samples the hyperparameter space. It’s a simple and effective approach that works particularly well with large or mixed (continuous or discrete) search spaces.

You can use the following code to define the search algorithm:

Copy code

```
from snowflake.ml.modeling.tune.search import BayesOpt, RandomSearch, GridSearch
search_alg = BayesOpt()
search_alg = RandomSearch()
search_alg = GridSearch()
```

### Define hyperparameter sampling

Use the search space functions to define the hyperparameter sampling method during each trial. Use them to describe the range and type of the values that the hyperparameters can take.

The following are the available sampling functions:

- uniform(`lower`, `upper`):
  Samples a continuous value uniformly between lower and upper. Useful for parameters like dropout rates or regularization strengths.
- loguniform(`lower`, `upper`):
  Samples a value in logarithmic space, ideal for parameters that span several orders of magnitude (for example, learning rates).
- randint(`lower`, `upper`):
  Samples an integer uniformly between lower (inclusive) and upper (exclusive). Suitable for discrete parameters like the number of layers.
- choice(options):
  Randomly selects a value from a provided list. Often used for categorical parameters.

The following is an example of how you can define the search space with the uniform function:

Copy code

```
search_space = {
    "n_estimators": tune.uniform(50, 200),
    "max_depth": tune.uniform(3, 10),
    "learning_rate": tune.uniform(0.01, 0.3),
}
```

### Configure the tuner

Use the `TunerConfig` object to configure the tuner. Within the object, you specify the metric being optimized, the optimization mode, and the other execution parameters. The following are the available configuration options:

- Metric
  The performance metric, such as accuracy or loss that you’re optimizing.
- Mode
  Determines whether the objective is to maximize or minimize the metric (`"max"` or `"min"`).
- Search Algorithm
  Specifies the strategy for exploring the hyperparameter space.
- Number of Trials
  Sets the total number of hyperparameter configurations to evaluate.
- Concurrency
  Defines how many trials can run concurrently.

The following example code uses the Bayesian optimization library to maximize the accuracy of a model over five trials.

Copy code

```
from snowflake.ml.modeling import tune
tuner_config = tune.TunerConfig(
  metric="accuracy",
  mode="max",
  search_alg=BayesOpt(
      utility_kwargs={"kind": "ucb", "kappa": 2.5, "xi": 0.0}
  ),
  num_trials=5,
  max_concurrent_trials=1,
)
```

### Get the hyperparameters and training metrics

The Snowflake ML HPO API requires the training metrics and hyperparameters from each training run to optimize the hyperparameters effectively. Use the `TunerContext` object to get the hyperparameters and training metrics. The following example creates a training function to get the hyperparameters and training metrics:

Copy code

```
def train_func():
  tuner_context = get_tuner_context()
  config = tuner_context.get_hyper_params()
  dm = tuner_context.get_dataset_map()
  ...
  tuner_context.report(metrics={"accuracy": accuracy}, model=model)
```

### Initiate the training job

Use the `Tuner` object to initiate the training job. The `Tuner` object takes the training function, search space, and tuner configuration as arguments. The following is an example of how to initiate the training job:

Copy code

```
from snowflake.ml.modeling import tune
tuner = tune.Tuner(train_func, search_space, tuner_config)
tuner_results = tuner.run(dataset_map=dataset_map)
```

The preceding code distributes the training function across the available resources. It collects and summarizes the trial outcomes and identifies the best performing
configuration.

### Get the training job results

> After all trials are completed, the `TunerResults` object consolidates the outcomes of each trial. It provides structured access to the performance metrics, the best configuration, and the best model.
>
> The following are its available attributes:

- results: A Pandas DataFrame containing metrics and configurations for every trial.
- best\_result: A DataFrame row summarizing the trial with the best performance.
- best\_model: The model instance associated with the best trial, if applicable.

The following code gets the results, the best model, and the best result:

Copy code

```
print(tuner_results.results)
print(tuner_results.best_model)
print(tuner_results.best_result)
```

## API reference

### Tuner

The following is the import statement for the Tuner module:

Copy code

```
from snowflake.ml.modeling.tune import Tuner
```

The Tuner class is the main interface for interacting with the container runtime HPO API. To run an HPO job, use the following code to initialize a Tuner object and call the run method with the Snowflake datasets.

Copy code

```
class Tuner:
  def __init__(
      self,
      train_func: Callable,
      search_space: SearchSpace,
      tuner_config: TunerConfig,
  )

  def run(
      self, dataset_map: Optional[Dict[str, DataConnector]] = None
  ) -> TunerResults
```

### SearchSpace

The following is the import statement for the search space:

Copy code

```
from snowflake.ml.modeling.tune import uniform, choice, loguniform, randint
```

The following code defines the search space functions:

Copy code

```
def uniform(lower: float, upper: float)
    """
    Sample a float value uniformly between lower and upper.

    Use for parameters where all values in range are equally likely to be optimal.
    Examples: dropout rates (0.1 to 0.5), batch normalization momentum (0.1 to 0.9).
    """

def loguniform(lower: float, upper: float) -> float:
    """
    Sample a float value uniformly in log space between lower and upper.

    Use for parameters spanning several orders of magnitude.
    Examples: learning rates (1e-5 to 1e-1), regularization strengths (1e-4 to 1e-1).
    """

def randint(lower: int, upper: int) -> int:
    """
    Sample an integer value uniformly between lower(inclusive) and upper(exclusive).

    Use for discrete parameters with a range of values.
    Examples: number of layers, number of epochs, number of estimators.
    """

def choice(options: List[Union[float, int, str]]) -> Union[float, int, str]:
    """
    Sample a value uniformly from the given options.

    Use for categorical parameters or discrete options.
    Examples: activation functions ['relu', 'tanh', 'sigmoid']
    """
```

### TunerConfig

The following is the import statement for the TunerConfig module:

Copy code

```
from snowflake.ml.modeling.tune import TunerConfig
```

Use the following code to define configuration class for the tuner:

Copy code

```
class TunerConfig:
  """
  Configuration class for the tuning process.

  Attributes:
    metric (str): The name of the metric to optimize. This should correspond
        to a key in the metrics dictionary reported by the training function.

    mode (str): The optimization mode for the metric. Must be either "min"
        for minimization or "max" for maximization.

    search_alg (SearchAlgorithm): The search algorithm to use for
        exploring the hyperparameter space. Defaults to random search.

    num_trials (int): The maximum number of parameter configurations to
        try. Defaults to 5

    max_concurrent_trials (Optional[int]): The maximum number of concurrently running trials per node. If   not specified, it defaults to the total number of nodes in the cluster. This value must be a positive
    integer if provided.

  Example:
      >>> from snowflake.ml.modeling.tune import  TunerConfig
      >>> config = TunerConfig(
      ...     metric="accuracy",
      ...     mode="max",
      ...     num_trials=5,
      ...     max_concurrent_trials=1
      ... )
  """
```

### SearchAlgorithm

The following is the import statement for the search algorithm:

Copy code

```
from snowflake.ml.modeling.tune.search import BayesOpt, RandomSearch, GridSearch
```

The following code creates a Bayesian optimization search algorithm object:

Copy code

```
@dataclass
class BayesOpt():
    """
    Bayesian Optimization class that encapsulates parameters for the acquisition function.

    This class is designed to facilitate Bayesian optimization by configuring
    the acquisition function through a dictionary of keyword arguments.

    Attributes:
        utility_kwargs (Optional[Dict[str, Any]]):
            A dictionary specifying parameters for the utility (acquisition) function.
            If not provided, it defaults to:
                {
                    'kind': 'ucb',   # Upper Confidence Bound acquisition strategy
                    'kappa': 2.576,  # Exploration parameter for UCB
                    'xi': 0.0      # Exploitation parameter
                }
    """
    utility_kwargs: Optional[Dict[str, Any]] = None
```

The following code creates a random search algorithm object:

Copy code

```
@dataclass
class RandomSearch():
    The default and most basic way to do hyperparameter search is via random search.

    Attributes:
Seed or NumPy random generator for reproducible results. If set to None (default), the global generator (np.random) is used.
    random_state: Optional[int] = None
```

### TunerResults

The following code creates a TunerResults object:

Copy code

```
@dataclass
class TunerResults:
    results: pd.DataFrame
    best_result: pd.DataFrame
    best_model: Optional[Any]
```

### get\_tuner\_context

The following is the import statement for the `get_tuner_context` function:

Copy code

```
from snowflake.ml.modeling.tune import get_tuner_context
```

This helper method is designed to be called within the training function. It returns a TunerContext object that encapsulates several useful fields for running the trial, including:

- Hyperparameters selected by the HPO framework for the current trial.
- The dataset required for training.
- A helper function to report metrics, guiding the HPO framework in suggesting the next set of hyperparameters.

The following code creates a tuner context object:

Copy code

```
class TunerContext:
    """
    A centralized context class for managing trial configuration, reporting, and dataset information.
    """

    def get_hyper_params(self) -> Dict[str, Any]:
        """
        Retrieve the configuration dictionary.

        Returns:
            Dict[str, Any]: The configuration dictionary for the trial.
        """
        return self._hyper_params

    def report(self, metrics: Dict[str, Any], model: Optional[Any] = None) -> None:
    """
    Report metrics and optionally the model if provided.

    This method is used to report the performance metrics of a model and, if provided, the model itself.
    The reported metrics will be used to guide the next set of hyperparameters selection in the
    optimization process.

    Args:
        metrics (Dict[str, Any]): A dictionary containing the performance metrics of the model.
            The keys are metric names, and the values are the corresponding metric values.
        model (Optional[Any], optional): The trained model to be reported. Defaults to None.

    Returns:
        None: This method doesn't return anything.
    """

    def get_dataset_map(self) -> Optional[Dict[str, Type[DataConnector]]]:
        """
        Retrieve the dataset mapping.

        Returns:
            Optional[Dict[str, Type[DataConnector]]]: A mapping of dataset names to DataConnector types, if available.
        """
        return self._dataset_map
```

## Limitations

Bayesian optimization requires continuous search spaces and works only with the uniform sampling function. It is incompatible with discrete parameters sampled using the `tune.randint` or `tune.choice` methods. To work around this limitation, either use
`tune.uniform` and cast the parameter inside the training function, or switch to a sampling algorithm that handles
both discrete and continuous spaces, such as `tune.RandomSearch`.

## Troubleshooting

| Error message | Possible causes | Possible solutions |
| --- | --- | --- |
| Invalid search space configuration: BayesOpt requires all sampling functions to be of type ‘Uniform’. | Bayesian optimization works only with uniform sampling, not with discrete samples. (See [Limitations](#limitations) above.) | - Use `tune.uniform` and cast the result in your training function. - Switch to `RandomSearch` algorithm, which accepts both discrete and non-discrete samples. |
| Insufficient CPU resources. Required: 16, Available: 8. The numbers of required and available resources may differ. | `max_concurrent_trials` is set to a value higher than the available cores. | Follow guidance provided by the error message. |
| Insufficient GPU resources. Required: 4, Available: 2. May refer to CPU or GPU. The numbers of required and available resources may differ. | `max_concurrent_trials` is set to a value higher than the available cores. | Follow the guidance provided by the error message. |

Expand

Show lessSee more

## Next steps

- [Container Runtime HPO Example](https://github.com/Snowflake-Labs/sf-samples/blob/main/samples/ml/container_runtime_hpo/hpo_example.ipynb)
