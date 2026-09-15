# Agentic ML with Snowflake CoCo

Snowflake CoCo powers agentic ML by autonomously planning, executing, and iterating on machine learning workflows with native context awareness of your data, models, notebooks, and features on a unified platform. You can ask it to complete a single task or pursue a broader goal that requires multi-step reasoning and action. From a natural language prompt, CoCo can explore data, engineer features, train and evaluate models, debug issues, and prepare models for deployment, all within Snowflake’s governed environment.

Rather than requiring you to manually orchestrate every step, CoCo can determine what needs to happen next, write and run code, evaluate results, recover from errors, and continue iterating. You define the objective, approve key decisions, and step in when you want to steer. CoCo handles the execution.

CoCo is available in the CoCo CLI, CoCo Desktop, and CoCo in Snowsight, which is directly integrated with [Snowflake Notebooks](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-overview). Data scientists can use CoCo to automate the full ML lifecycle, including data exploration, feature engineering, model training, evaluation, deployment, monitoring, and debugging.

Looking for code?

This page shows the natural-language prompts you give to CoCo. CoCo writes and runs the actual Python code for you inside your notebook or session. To see or reuse that code, check the notebook cells CoCo generates during a session.

If you prefer to write ML code directly without CoCo, see the [Snowflake ML Python API reference](/developer-guide/snowflake-ml/snowpark-ml) and the [Snowflake ML overview](/developer-guide/snowflake-ml/overview) for hands-on examples.

Resources

Try out these quickstarts to get started:

- [Build Your First ML Model in Snowflake with Agentic ML](https://www.snowflake.com/en/developers/guides/build-your-first-ml-model-in-snowflake-with-agentic-ml/)
- [Agentic Machine Learning Best Practices with Snowflake CoCo](https://www.snowflake.com/en/developers/guides/agentic-machine-learning-best-practices-cortex-code/)

## Using the machine-learning skill

CoCo comes embedded with a rich set of ML-specific capabilities that streamline design, implementation, and optimization of end-to-end workflows in Snowflake ML. The ML skill activates automatically based on your intent. When you describe an ML task in
natural language, CoCo detects the intent, loads the ML skill, and routes to the appropriate
subskill to handle your request. To ensure that the skill is always triggered, you can also explicitly invoke it by typing `/machine-learning` before your prompt.

```
/machine-learning Train a model on the table CUSTOMER_FEATURES to predict churn
```

## Subskills

The ML skill is composed of specialized subskills. CoCo selects and routes between them
autonomously based on your goal. For example, if you train a model and then say “deploy it”,
CoCo switches from the training subskill to the deployment subskill automatically,
preserving context across the full workflow. A single conversation can span many subskills
without you needing to invoke each one explicitly.

The following table lists the available subskills.

| Subskill | Description | Example Prompt |
| --- | --- | --- |
| Model Training | Train classification, regression, forecasting, and clustering models with scikit-learn, XGBoost, LightGBM, PyTorch, or AutoGluon | *Train an XGBoost model to predict churn on CUSTOMER\_FEATURES* |
| Feature Store | Create entities, feature views, pipelines, training datasets with point-in-time correctness, and online serving | *Create a feature store with 7-day rolling spend windows* |
| Model Registry | Log, version, and deploy trained models for inference | *Register this model in the registry and deploy it* |
| Batch Inference | Score tables at scale using `mv.run()` on warehouses or `mv.run_batch()` on compute pools | *Run batch predictions on my test data using CHURN\_MODEL V2* |
| Online Inference | Deploy low-latency REST endpoints on Snowpark Container Services | *Deploy my model as a real-time inference service* |
| Distributed Training | Multi-node XGBoost, LightGBM, and PyTorch training with hyperparameter tuning | *Train XGBoost distributed across 4 GPU nodes with 20 HPO trials* |
| ML Jobs | Submit Python scripts to Snowflake compute pools for GPU or high-memory workloads | *Submit this training script to run on a GPU compute pool* |
| Pipeline Orchestration | Schedule and chain ML tasks using Snowflake Task Graphs (DAGs) | *Create a weekly pipeline: refresh features, retrain, deploy if better* |
| Experiment Tracking | Log parameters, metrics, and artifacts across training runs for comparison | *Track this experiment and log accuracy, F1, and training time* |
| Preprocessing | Scale, encode, impute, and transform features before training | *Normalize numeric features and one-hot encode categoricals* |
| Model Monitoring | Track drift, performance degradation, and set alerts on production models | *Set up drift monitoring for my fraud detection model* |
| Datasets | Create versioned, immutable data snapshots for reproducible training | *Create a versioned dataset from my training query results* |
| ML Lineage | Trace the flow from source tables to features, datasets, models, and services | *What data trained this model? Show the full lineage.* |
| Inference Logs | Query auto-captured inference data from model services | *Show me the last 100 inference requests for FRAUD\_MODEL* |
| Debug Inference | Diagnose dtype errors, OOM issues, container crashes, and service failures | *My model service is returning errors. Help me debug.* |

Expand

Show lessSee more

## Prepare data

Use CoCo to explore, clean, and transform raw data into ML-ready inputs. This is useful
when you need to understand your data before modeling or prepare features for training.

### Transform and preprocess features

Use CoCo to scale, encode, impute, and engineer features to prepare data for training.

```
Normalize numeric features and one-hot encode categoricals
```

### Save as datasets

Use CoCo to create versioned, immutable data snapshots for reproducible training with [Snowflake Datasets](/developer-guide/snowflake-ml/dataset).

```
Create a versioned dataset from my training query results as Parquet files
```

## Manage and serve features

Use CoCo to set up your [Feature Store](/developer-guide/snowflake-ml/feature-store/overview). Define entities, build feature views, generate
training datasets with point-in-time correctness, and enable online serving. This is useful when
you need reusable, production-ready features that multiple models and teams can share and reuse or serve in real time.

### Create and manage feature views

```
Create a feature store with 7-day rolling spend windows for each customer
```

### Generate training datasets

```
Generate a training dataset with point-in-time correctness using my Feature Views
```

### Serve features online

```
Enable online serving on CUSTOMER_SPEND_FEATURES for real-time inference
```

## Train and tune models

Use CoCo to train classification, regression, forecasting, and clustering models using
scikit-learn, XGBoost, LightGBM, PyTorch, or AutoGluon. This is useful when you want to build a
predictive model from your data, run distributed training at scale, or let the Auto ML skill
handle the full workflow autonomously.

For more information, see [Train models](/developer-guide/snowflake-ml/train-models) and
[Distributed training](/developer-guide/snowflake-ml/distributed-training).

### Train a model

Use CoCo to train models on your data with the framework and configuration you specify.

```
Train an XGBoost model to predict churn on CUSTOMER_FEATURES
```

### Distribute training

Use CoCo to distribute training across multiple nodes for large datasets or parallel
hyperparameter search.

```
Train XGBoost distributed across 4 GPU nodes with 20 HPO trials
```

### Submit training jobs to compute pools

Use CoCo to submit custom training scripts to Snowflake compute pools for GPU or
high-memory workloads.

```
Submit this training script to run on a GPU compute pool
```

For more information, see [Container Runtime for ML](/developer-guide/snowflake-ml/container-runtime-ml).

### Experiment tracking

Use CoCo to log parameters, metrics, and artifacts for every training run so you can
compare trials systematically.

```
Track this experiment and log accuracy, F1, and training time
```

For more information, see [Experiment Tracking](/developer-guide/snowflake-ml/experiments).

## Manage and deploy models

Use CoCo to version, register, and deploy trained models for batch or real-time
inference. This is useful when you have a trained model and need to move it to production.

For more information, see [Model Registry](/developer-guide/snowflake-ml/model-registry/overview) and
[Inference overview](/developer-guide/snowflake-ml/inference/inference-overview).

### Register and version models

Use CoCo to log models to the Snowflake Model Registry with metadata, lineage, and
deployment-ready packaging.

```
Register the best model in the registry as CHURN_MODEL V2
```

For more information, see [Model management](/developer-guide/snowflake-ml/model-registry/model-management).

### Run batch predictions

Use CoCo to score entire tables or datasets at scale using warehouses or compute pools.

```
Run batch predictions on my test data using CHURN_MODEL V2
```

For more information, see [Batch inference](/developer-guide/snowflake-ml/inference/native-batch-inference-sql).

### Deploy real-time inference endpoints

Use CoCo to deploy models as low-latency REST endpoints on Snowpark Container Services.

```
Deploy my fraud model as a real-time inference service on SPCS
```

For more information, see [Real-time inference](/developer-guide/snowflake-ml/inference/real-time-inference-rest-api).

## Operationalize ML workflows

Use CoCo to automate recurring ML workflows and manage the full pipeline lifecycle.
This is useful when you need to schedule retraining, chain tasks, or trace how models were
produced.

### Build and schedule pipelines

Use CoCo to build Snowflake Task Graphs (DAGs) that chain feature refresh, training,
evaluation, and deployment.

```
Create a weekly pipeline: refresh features, retrain, deploy if better
```

For more information, see [Create pipelines](/developer-guide/snowflake-ml/create-pipelines-deploy).

### Trace data and model lineage

Use CoCo to trace the full provenance graph from source tables through features,
datasets, models, and deployed services.

```
What data trained CHURN_MODEL V2? Show the full lineage.
```

For more information, see [ML Lineage](/developer-guide/snowflake-ml/ml-lineage).

## Monitor and observe models

Use CoCo to track production model health, analyze inference patterns, and debug
failures. This is useful when you have models in production and need to ensure they continue
performing well.

For more information, see [Model Observability](/developer-guide/snowflake-ml/model-registry/model-observability).

### Monitor drift and performance

Use CoCo to track drift, performance degradation, and set up alerts before issues
impact users.

```
Set up drift monitoring for my fraud detection model
```

### Analyze inference logs

Use CoCo to query auto-captured request and response data from model services and
analyze usage patterns.

```
Show me the last 100 inference requests for FRAUD_MODEL
```

For more information, see [Inference logs](/developer-guide/snowflake-ml/inference/auto-capture-inference-logs).

### Debug inference failures

Use CoCo to diagnose dtype mismatches, OOM issues, container crashes, and service
failures.

```
My model service is returning TypeErrors. Help me debug.
```

## Auto ML: End-to-end model exploration and optimization

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

The Auto ML skill builds a complete machine learning model from scratch. It explores the model
space across multiple frameworks (XGBoost, LightGBM, AutoGluon, and others), runs hyperparameter
optimization for each candidate, and engineers features to maximize performance. The full
workflow runs autonomously: data exploration, quality gates, feature engineering, model training,
hyperparameter tuning, and evaluation. You describe what machine learning task you want to perform and CoCo handles the
rest.

```
Build a model predicting whether a customer will churn
in the next 30 days using the CUSTOMERS table with the highest accuracy
```

```
Forecast daily order volume for the next 2 weeks from ORDERS table
```

**Supported task types:**

- **Classification**: predict a category (churn yes/no, fraud detection, lead scoring)
- **Regression**: predict a number (revenue forecast, price estimation, demand prediction)
- **Time-series forecasting**: predict future values over time (sales forecast, capacity planning)
- **Clustering**: segment data into groups (customer segmentation, anomaly grouping)

All you need to provide is:

- **Data source**: a table, view, or DataFrame
- **What to predict or analyze**: for example, “predict churn”, “forecast sales”, “segment customers”
- **Time budget**: how long you want to invest in building the model (default is 30 minutes)

CoCo infers everything else (task type, target column, evaluation metric, train/test split
strategy) and asks you to confirm before proceeding.

**How it works:**

The skill follows a 4-step workflow with built-in checkpoints:

1. **Understand and configure**: CoCo explores your data, proposes a configuration (task
   type, metric, time budget, trial plan), and waits for your approval.
2. **Quality gates**: Mandatory data quality checks (leakage detection, baseline scoring, EDA)
   before any modeling begins.
3. **Build**: CoCo works autonomously on feature engineering, model training, and
   evaluation. It reports after feature engineering and after each training trial with metrics,
   leaderboard, and overfitting checks. You can interject at any time.
4. **Deliver**: CoCo updates the experiment manifest and presents next steps (deeper
   research, training notebook, batch inference, Feature Store, monitoring, or retraining).

CoCo asks how long you want to invest (default 30 minutes). It proposes
a trial plan, tracks elapsed time, and adjusts if the budget runs low.

**What you get:**

| Artifact | Location |
| --- | --- |
| Working notebook | Your Workspace notebook (or a local `.ipynb` in CLI). Contains EDA and all experimentation cells with the full decision trail. |
| Experiment tracking | Snowflake Experiment Tracking: queryable metrics, parameters, and artifacts for every trial. |
| Manifest | `<experiment_name>_manifest.json` in the notebook’s directory. Lists all Snowflake objects created. |
| Diagnostic plots | Logged as experiment artifacts: feature importance, SHAP, confusion matrix, forecast components, and others. |

Expand

Show lessSee more
