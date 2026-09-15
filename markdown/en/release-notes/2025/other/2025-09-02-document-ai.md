# Sep 02, 2025: Document AI models in the model registry

Document AI now stores any published or trained models within the [Snowflake Model Registry](/developer-guide/snowflake-ml/model-registry/overview).

You can now copy the Document AI models between databases or schemas in the same account or between different accounts in the same organization,
to easily manage and control model releases with versioning and role-based access control (RBAC). The model registry serves as the control plane
for deploying Document AI model versions safely and efficiently across environments.

This feature is available to accounts in AWS and Microsoft Azure. Google Cloud is not supported.

Note

New Document AI models are automatically integrated into the model registry; existing models must be manually integrated.

- To manually integrate an existing model into the model registry, when prompted, select **Start** on the integration banner in the UI.

For more information, see [Document AI: CREATE MODEL privilege required to create, publish, and train model builds](/release-notes/bcr-bundles/un-bundled/bcr-1904).
