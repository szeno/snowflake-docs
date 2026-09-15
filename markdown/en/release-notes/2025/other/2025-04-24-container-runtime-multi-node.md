# Apr 24, 2025: Container Runtime for ML on multi-node clusters (*Preview*)

Snowflake announces the preview of Container Runtime for ML on multi-node clusters, a new capability that allows you to scale your ML workloads across multiple compute nodes in Snowflake Notebooks.

Container Runtime for ML on multi-node clusters enables you to:

- **Scale ML workloads**: Dynamically adjust the number of nodes in your compute pool to match the resource needs of your ML tasks.
- **Run distributed training**: Train ML models on larger datasets using distributed frameworks like PyTorch, LightGBM, and XGBoost.
- **Manage cluster resources**: Easily scale up for resource-intensive tasks and scale down when fewer resources are needed.
- **Control scaling operations**: Configure asynchronous scaling, timeout thresholds, and minimum node requirements to match your workflow needs.

Key benefits of Container Runtime for ML on multi-node clusters include:

- **Improved performance**: Process larger datasets and accelerate training of complex models through parallelization.
- **Resource efficiency**: Scale resources up or down based on workload requirements without provisioning new compute pools.
- **Flexibility**: Support for synchronous or asynchronous scaling operations to match your development workflow.
- **Simplicity**: Straightforward APIs for scaling clusters and monitoring active nodes with minimal configuration.

To get started with Container Runtime for ML on multi-node clusters, see [Container Runtime on multi-node clusters](/developer-guide/snowflake-ml/container-runtime-multi-node).
