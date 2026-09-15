# Create pipelines and deploy them

## Overview

Machine learning (ML) workflows typically involve several key stages:

**Data Exploration and Preparation**: This initial phase involves understanding the raw data, cleaning it, handling missing values, and transforming it into a usable format.

**Data Engineering**: Here, raw data is transformed into features that better represent the underlying problem to the predictive models, often involving techniques like scaling, encoding, and creating new features from existing ones.

**Model Development**: In this stage, various ML models are selected, trained on the prepared data, and tuned to optimize their performance. Developed models are rigorously evaluated using appropriate metrics to assess their accuracy, fairness, and generalization capabilities.

**Model Deployment**: Production ready models are saved to a model registry and subsequently deployed for batch or real time predictions on new data.

Initial development of ML models often benefits from an agile, iterative approach, allowing data scientists to quickly experiment with different algorithms and features. However, as models mature and demonstrate value, the focus shifts to operationalization, where pipelines are hardened and automated with CI/CD (Continuous Integration/Continuous Delivery). This automation ensures that changes to code, data pipelines, or models are consistently built, tested, and deployed, leading to more reliable, efficient, and maintainable ML systems.

## Develop

Start with interactive development in a local IDE (e.g., VS Code) or an interactive notebook (Snowflake Notebook or Jupyter). Parameterize inputs (tables, stages, hyperparameters) and keep steps modular for portability. For instance, it can be helpful to have one cell/function for data preparation, another for feature engineering, another for model training, and so-on.

Snowflake provides the following tools for each stage of the machine learning lifecycle:

| Stage | Tool | Usage |
| --- | --- | --- |
| Data Exploration | Snowflake Notebooks | Develop in a managed, browser‑based notebook environment. Use Python and SQL in one place to profile datasets, visualize distributions, and iterate quickly. |
|  | Snowpark DataFrames | Work with familiar DataFrame APIs that push computation down to Snowflake. |
| Data Engineering | Snowpark DataFrames | Build reproducible transforms at warehouse scale using SQL/Python/Scala with pushdown optimization. |
|  | UDFs/UDTFs | Encapsulate custom Python logic as functions or table functions to reuse complex transforms across teams and pipelines. |
|  | Feature Store | Define, register, and serve features with point‑in‑time correctness and reuse across models. Supports consistent offline training sets and low‑latency online retrieval, reducing leakage and duplication. |
| Model Training | Snowflake Notebooks | Train ML models with familiar open source libraries like scikit-learn, XGBoost, and PyTorch in your Snowflake Notebooks. Leverage elastic scale, avoid data movement, and persist models and preprocessing in one place. |
|  | ML Jobs | Offload resource-intensive steps to specialized compute options like high-memory instances, GPU acceleration, and distributed processing from any environment, including local IDEs, notebooks, and externally hosted orchestrators. |
| Model Deployment | Model Registry | Register and version models with lineage and governance controls. Centralizes discovery and promotes safe promotion workflows, audits, and rollback. |
|  | Batch Inference | Serve registered models from Python or SQL, keeping inference close to governed data and simplifying ops with consistent registry-backed execution. |
|  | Real-time Inference | Deploy registered models to managed HTTPS endpoints with autoscaling. Eliminates serving infrastructure, offering simple, secure, low‑latency inference integrated with Snowflake auth and governance. |
|  | Model Monitoring | Create a monitor per model version to materialize inference logs and automatically refresh daily metrics, surfacing drift, performance, and statistical signals in Snowsight. Configure alerts and custom dashboards to compare versions and quickly diagnose data or pipeline issues |
| Workflow Orchestration | Scheduled Notebooks | Parameterize and configure Snowflake Notebooks to execute non-interactively on a schedule. |
|  | Task Graphs | Operationalize your ML pipeline into a Directed Acyclic Graph (DAG) and configure it to run on a schedule or by event based triggers. |
| Security and governance | RBAC, tags, masking, policies | Apply role‑based access, data classification, and masking/row policies to training data, features, and models. Ensures least‑privilege access and compliance throughout the ML lifecycle. |

Expand

Show lessSee more

## Prepare for production

### Prepare code

Before operationalizing your pipeline, prepare your code for productionization. If you started with notebooks, begin by restructuring your code into modular, reusable functions where each major step (data preparation, feature engineering, model training, evaluation) becomes a separate function with clear inputs and outputs. If you already have modular scripts, ensure each function has well-defined interfaces and responsibilities. Parameterize all configuration values like table names and hyperparameters to enable cross-environment deployment. We recommend also authoring an entrypoint script which executes the end-to-end pipeline locally for debugging and future development.

Example directory structure:

```
ml_pipeline_project/
├── README.md
├── requirements.txt
├── config/
├── src/ml_pipeline/
│   ├── utils/                     # Common utilities
│   ├── data/                      # Data preparation
│   ├── features/                  # Feature engineering
│   ├── models/                    # Model training
│   └── inference/                 # Model inference
├── scripts/
│   ├── run_pipeline.py            # Main entry point
│   └── dag.py
├── tests/
└── notebooks/
```

Example run\_pipeline.py script:

Copy code

```
import argparse
from ml_pipeline.utils.config_loader import load_config
from ml_pipeline.data.ingestion import load_raw_data
from ml_pipeline.data.validation import validate_data_quality
from ml_pipeline.features.transformers import create_features
from ml_pipeline.models.training import train_model
from ml_pipeline.models.evaluation import evaluate_model
from ml_pipeline.models.registry import register_model

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Config file path")
    parser.add_argument("--env", default="dev", help="Environment (dev/prod)")
    args = parser.parse_args()

    # Load configuration
    config = load_config(args.config, args.env)

    # Execute pipeline stages
    raw_data = load_raw_data(config.data.source_table)
    validate_data_quality(raw_data, config.data.quality_checks)
    features = create_features(raw_data, config.features.transformations)
    model = train_model(features, config.model.hyperparameters)
    metrics = evaluate_model(model, features, config.model.eval_metrics)
    register_model(model, metrics, config.model.registry_name)

if __name__ == "__main__":
    main()
```

### Migrating from Notebooks to ML Jobs

Most code written in Snowflake Notebooks will work in ML Jobs with no code changes necessary. The few aspects to be aware of are:

**Runtime APIs**

Certain distributed ML APIs are only available inside the Container Runtime, and attempting to import them outside the Container Runtime environment will fail. These APIs are available inside ML Jobs, but need to be imported inside the ML Job payload.

Copy code

```
# Attempting to import distributed runtime APIs in local/external
# environments will fail!
from snowflake.ml.modeling.distributors.xgboost import XGBEstimator

from snowflake.ml.jobs import remote

@remote(...)
def my_remote_function(...):
  # Move imports *inside* your ML Job payloads
  from snowflake.ml.modeling.distributors.xgboost import XGBEstimator  # This works!
  ...

job = my_remote_function()  # Start ML Job
job.wait()  # Wait for job to complete
```

**Cluster Scaling**

The `scale_cluster()` API only works inside Notebooks and will not work inside ML Jobs. Instead, specify the desired cluster size at job submission time. See [Snowflake Multi-Node ML Jobs](/developer-guide/snowflake-ml/ml-jobs/distributed-ml-jobs) for more information.

Copy code

```
from snowflake.ml.jobs import remote

@remote(..., target_instances=4)
def my_remote_function(...):
  # 4-node cluster will be provisioned for distributed processing
  # inside this job. The cluster will be automatically cleaned up on
  # job termination.
```

### Pipeline orchestration

Once you’ve prepared your end-to-end pipeline, operationalize your pipeline using an orchestrator like Snowflake Task Graphs, Scheduled Notebooks, or external orchestrators like Airflow. Using an orchestration framework provides several key advantages:

- Fault tolerance and reliability through automatic retries and failure isolation
- Observability with run history, real-time status, and alerts
- Scheduling and coordination for complex dependency graphs and various triggers
- Operational hygiene with version control integration and configuration management

Snowflake ML is compatible with most orchestration frameworks including Airflow, Dagster, and Prefect. If you already have an existing workflow/DAG setup, we recommend simply integrating your existing workflows with Snowflake ML features and offloading compute or data intensive steps to ML Jobs or UDFs. If you do not have an existing DAG setup, you can use Snowflake Task Graphs for a Snowflake native solution.

To set up orchestration with a DAG on Snowflake, follow these high-level steps:

1. Prepare your local pipeline code according to [Prepare for production](#label-create-pipelines-prepare-code)
2. Create a new `dag.py` file (or any other name) to hold your DAG definition
3. Implement the DAG form of your pipeline according to this guide
4. Run the `dag.py` script to deploy the Task Graph into your Snowflake account

Tip

Running a Task Graph script does not necessarily execute the graph; a basic Task Graph script simply defines and deploys the Task Graph. The Task Graph must be separately triggered to execute, either manually or on a schedule.

### Separating development and production

We recommend parameterizing your DAG script to support isolating your development (DEV) and production (PROD) environments. You can use Snowflake connection management, application specific configurations, or any combination of the two to achieve this. The level of isolation needed depends on your governance requirements, but generally we recommend using separate databases for DEV and PROD, where the PROD database is protected by RBAC policies which limit accessibility to administrators and specialized service accounts.

### CI/CD

You can automate validation and deployment of your pipelines using CI/CD pipelines such as Azure Pipelines and GitHub Actions. In general, we recommend testing in a DEV or STAGING environment before deploying to PROD. Best practice is to configure your source control repository with merge gates which validate code changes in DEV before merging into your production branch. Changes to the production branch can be deployed to PROD continuously (i.e. for every change) or on some regular cadence (daily/weekly). Best practice is to run a final validation of the production branch’s state in a DEV or STAGING environment before deploying changes to PROD. Use platform features like GitHub Actions Deployments and Environments to define and configure connections to each deployment environment. Configure your CI/CD pipeline to push your changes into the deployment environment, including:

- (Optional) Building libraries and modules as Python packages and pushing them into a proprietary package feed
- (Optional) Uploading files into a Snowflake Stage

  This is most commonly required when you utilize `snowflake.ml.jobs.submit_from_stage()` in your pipeline

  Alternatively, you can use Snowflake’s GitHub integration to directly track your GitHub repository as a Snowflake Stage
- Running `dag.py` to deploy the Task Graph in the configured environment
- (Optional) Trigger and monitor execution of the newly deployed Task Graph to verify validity

## Additional Resources

- [E2E Task Graph Quickstart](https://quickstarts.snowflake.com/guide/e2e-task-graph/)
