# Initializing shared state once in Python UDFs

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Use the `@udf_init_once` decorator to optimize batch inference in Python UDFs. Large objects such as ML models
load once and are shared across worker processes, instead of loading separately in every worker. This reduces
memory use and startup time for large-model inference workloads on Snowflake warehouses.

Snowflake Model Registry uses the same mechanism for models deployed to a warehouse. For more information, see
[Using with Snowflake Model Registry](#label-udf-python-init-once-model-registry).

## What is @udf\_init\_once?

`@udf_init_once` is a decorator that allows you to define initialization logic that executes exactly once per
query execution in a global process within a UDF, before Snowflake creates worker processes for parallel execution.
All worker processes then share the initialized state.

Key behavior:

- Initialization runs once in the global process.
- Initialized state is shared across all workers.
- Avoids redundant loading of large objects such as ML models.

## Why use this feature?

`@udf_init_once` improves memory efficiency, execution performance, and model capacity for batch inference
workloads on Snowflake warehouses. By initializing heavy objects such as ML models once and sharing them across
workers, this feature significantly reduces total memory consumption, eliminates repeated startup overhead, and
enables larger models, or multiple models, to run more efficiently on the warehouse.

## When to use this feature

Use this feature when your workload involves:

- **Batch inference with large ML models**: Model scoring over datasets using XGBoost, PyTorch, and other frameworks.
- **Multiple ML models**: Loading several models for ensemble predictions or multi-model pipelines.
- **Heavy initialization logic**: Complex setup that should run only once.
- **Large lookup tables**: Static reference data that all workers need to access.
- **Any operation that needs to run once in a UDF**: Expensive computations or data loading that shouldn’t repeat.

## Getting started

Before using this feature, review the following guidelines.

### Use fork-safe initialization logic

When a `@udf_init_once` function is detected, all module-level code and all functions decorated with
`@udf_init_once` run once in a parent process before worker processes are created. It should only perform
initialization that produces read-only, in-memory state that can be safely shared across workers.

Avoid operations that:

- Depend on process-specific resources such as network connections, file handles, or client sessions.
- Start background threads or subprocesses.
- Require per-process initialization.

These can lead to errors, inconsistent behavior, or loss of memory-sharing benefits after forking.

### Design for shared, read-only state

Objects initialized using `@udf_init_once` are shared across worker processes. For best memory efficiency,
design these objects to be read-only during execution.

If a worker process modifies the shared state, the system creates a separate copy for that worker. This ensures
safe, isolated execution, but increases memory usage and reduces the memory-sharing benefits of this feature.

### Use global variables for access

Store initialized objects (for example, models or configuration) in global variables so they are accessible
within the UDF handler.

## Examples

### XGBoost batch inference

The following example shows how to use `@udf_init_once` to load an XGBoost model once and share it across
workers:

Copy code

```
CREATE OR REPLACE FUNCTION xgb_predict(f0 float, f1 float, f2 float, f3 float, f4 float)
RETURNS float
LANGUAGE PYTHON
RUNTIME_VERSION = 3.11
PACKAGES = ('numpy', 'xgboost', 'snowflake-snowpark-python')
HANDLER = 'predict'
AS $$
import numpy as np
import xgboost as xgb
from _snowflake import udf_init_once

@udf_init_once
def load_model():
    global model

    # Replace this with logic to load your pre-trained model artifact.
    rng = np.random.RandomState(42)
    X = rng.rand(1000, 5)
    y = (X[:, 0] + X[:, 1] > 1.0).astype(int)
    dtrain = xgb.DMatrix(X, label=y)
    params = {'objective': 'binary:logistic', 'max_depth': 3, 'eta': 0.3}
    model = xgb.train(params, dtrain, num_boost_round=20)

def predict(f0, f1, f2, f3, f4):
    features = np.array([[f0, f1, f2, f3, f4]], dtype=np.float32)
    return float(model.predict(xgb.DMatrix(features))[0])
$$;
```

### PyTorch batch inference

The following example shows how to use `@udf_init_once` to load a PyTorch model once and share it across
workers:

Copy code

```
CREATE OR REPLACE FUNCTION pytorch_predict(f0 FLOAT, f1 FLOAT, f2 FLOAT, f3 FLOAT, f4 FLOAT)
RETURNS FLOAT
LANGUAGE PYTHON
RUNTIME_VERSION = 3.11
PACKAGES = ('numpy', 'pytorch', 'snowflake-snowpark-python')
IMPORTS = ('@pytorch_model_stage/model/model.pt')
HANDLER = 'predict'
AS $$
import os
import sys

import numpy as np
import torch
from _snowflake import udf_init_once
torch.set_num_threads(1)

@udf_init_once
def load_model():
    global model
    import_dir = sys._xoptions["snowflake_import_directory"]
    model_path = os.path.join(import_dir, "model.pt")
    model = torch.jit.load(model_path, map_location="cpu")
    model.eval()

def predict(f0, f1, f2, f3, f4):
    with torch.no_grad():
        inp = torch.tensor([[f0, f1, f2, f3, f4]], dtype=torch.float32)
        return float(model(inp).item())
$$;
```

## Using with Snowflake Model Registry

You don’t need to write a UDF to use this optimization with a registered model. Set the `model_init_once` option
when you log the model, and Snowflake loads the model once and shares it across workers when the model runs in a
warehouse. For more information, see [Loading large models once in a warehouse](/developer-guide/snowflake-ml/model-registry/overview#label-snowpark-model-registry-model-init-once).

## Limitations

- The decorated function must produce a read-only, in-memory state. Modifications to shared state trigger
  a per-worker copy, which increases memory usage.
- Execution of module-scoped code and initialization function is now run once in a parent worker. All code
  in the initialization function or at module scope must be fork safe, including any code that executes from
  imported modules. The creation of any of the following could pose a problem:

  - Opening files and storing file descriptors
  - Initializing network connections and database sessions
  - Holding locks and initializing mutexes
  - Spawning additional threads or processes
- Models must be shareable across processes.
- SnowflakeFile is not supported within `@udf_init_once` initialization functions.
