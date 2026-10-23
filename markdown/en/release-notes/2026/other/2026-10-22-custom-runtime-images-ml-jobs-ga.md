# October 22, 2026: Custom runtime images for ML Jobs (*General availability*)

Custom runtime images for ML Jobs are now generally available. You can build, validate, and register your own custom
container images as Custom Runtime Environments (CREs), and then reference them when you submit ML Jobs on Container
Runtime by using the `runtime_environment="cre@<name>"` format. Custom runtime images let you include specific
packages, meet compliance and security requirements, integrate with existing CI/CD pipelines, and ensure
reproducibility across environments.

Custom runtime images for Snowflake Notebooks remain in preview.

For more information, see [Custom runtime images](/developer-guide/snowflake-ml/custom-runtime-images).
