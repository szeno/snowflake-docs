# Examples and Quickstarts

This topic contains several examples and quickstarts for common use cases for model logging and model inference in
Snowflake ML. You can use these examples as a starting point for your own use case.

## Beginner Quickstart

Getting started with Snowflake ML: train an xgboost regression model, log to model registry, and run inference in a
Warehouse.

[Quickstart](https://quickstarts.snowflake.com/guide/intro_to_machine_learning_with_snowpark_ml_for_python/)

## xgboost model, CPU inference in Snowpark Container Services

This code illustrates the key steps in deploying an XGBoost model in Snowpark Container Services (SPCS), then using the deployed model for inference.

For more information, see [Deploy models for real-time inference (REST API)](/developer-guide/snowflake-ml/inference/real-time-inference-rest-api).

## Log a pipeline with custom preprocessing and model training

This example illustrates how to:

- Perform feature engineering.
- Train a pipeline with custom preprocessing steps and an xgboost forecasting model.
- Run hyperparameter optimization.
- Log the optimum pipeline.
- Run inference in a warehouse or in Snowpark Container Services (SPCS).

[Example Notebook](https://github.com/rajshah4/snowflake-notebooks/blob/main/Forecasting_ChicagoBus/Snowpark_Forecasting_Bus_FeatureStore.ipynb)

## Getting Started with Model Serving in Snowpark Container Services

This example illustrates how to:

- Train, register, and version a model using the Snowflake Model Registry.
- Deploy a model as a service in Snowpark Container Services.
- Access the deployed model endpoint using REST API with both Key-Pair and Programmatic Access Token (PAT) authentication.

[Quickstart](https://quickstarts.snowflake.com/guide/snowpark-container-services-model-serving-guide/)

## Large scale open source embeddings model, GPU inference

This example uses Snowflake Notebooks on Container Runtime to train a large-scale embeddings model from the Hugging Face
`sentence_transformer` library and run large scale predictions using GPUs on Snowpark Container Services (SPCS).

[Quickstart](https://quickstarts.snowflake.com/guide/scale-embeddings-with-snowflake-notebooks-on-container-runtime/)

## Complete pipeline with distributed PyTorch recommender model, GPU inference

This example shows how to build an end-to-end distributed Pytorch recommender model using GPUs, deploying the model for GPU inference on Snowpark Container Services (SPCS).

[Quickstart](https://quickstarts.snowflake.com/guide/getting-started-with-running-distributed-pytorch-models-on-snowflake/)

## Bring an existing model trained externally (eg. AWS Sagemaker/Azure ML/GCP Vertex AI) to Snowflake

These examples show how to bring your existing model in AWS Sagemaker, Azure ML, or GCP Vertex AI to Snowflake (see [blog post](https://medium.com/snowflake/integrating-machine-learning-models-with-snowpark-ml-a-guide-for-azureml-and-sagemaker-users-735292843a7b) for more details).

- AWS and Azure ML [Quickstart](https://quickstarts.snowflake.com/guide/deploying_models_from_azureml_and_sagemaker_to_snowparkml/)
- GCP Vertex AI [Quickstart](https://quickstarts.snowflake.com/guide/getting_started_with_snowpark_for_machine_learning_on_vertexai/)

## Bring an MLFlow PyFunc model to Snowflake

This example shows how to log an MLFlow PyFunc model in the Snowflake Model Registry and run inference.

[Example](/developer-guide/snowflake-ml/model-registry/built-in-models/mlflow)

## Log a partitioned forecasting model for training and inference

This example shows how to log a forecasting model for running partitioned training and inference in Snowflake.

[Quickstart](https://quickstarts.snowflake.com/guide/partitioned-ml-model/)

## Log many models as a collection for running partitioned inference at scale

This example shows how to log thousands of models as a custom partitioned model for running distributed, partitioned inference.

[Quickstart](https://quickstarts.snowflake.com/guide/many-model-inference-in-snowflake/)
