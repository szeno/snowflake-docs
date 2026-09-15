# Snowflake Terraform provider

[HashiCorp Terraform](https://www.terraform.io/) is an open-source Infrastructure as Code (IaC) tool that allows you to dynamically build, change, and version infrastructure resources. You use the [Terraform language](https://developer.hashicorp.com/terraform/language) to create configuration files that describe the configuration you want. Terraform compares your configuration to the current state and then generates a plan to create new resources or update and delete existing resources. The plan runs as a directed acyclic graph (DAG), which allows Terraform to understand and handle dependencies between resources.

The [Snowflake Terraform provider](https://registry.terraform.io/providers/snowflakedb/snowflake/latest) enables you to establish a consistent workflow to manage Snowflake resources like warehouses, databases, schemas, tables, roles, grants, and more.

After you [install Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli#install-terraform), see the following resources to get started using the Snowflake provider.

| Resource | Description |
| --- | --- |
| [Snowflake provider documentation](https://registry.terraform.io/providers/snowflakedb/snowflake/latest/docs) | Guides and reference documentation in the [Terraform Registry](https://registry.terraform.io/) for the Snowflake provider. Documentation includes the [resource blocks](https://developer.hashicorp.com/terraform/language/resources/syntax) that describe objects in Snowflake (for example, `snowflake_database`*) and the [data sources](https://developer.hashicorp.com/terraform/language/data-sources) that you can use to name and dynamically fetch configuration state from Snowflake objects (for example, `snowflake_users`*). |
| [terraform-provider-snowflake](https://github.com/snowflakedb/terraform-provider-snowflake) | The GitHub project where you can do the following:   - Stay up to date on feature developments and status, including the [project roadmap](https://github.com/snowflakedb/terraform-provider-snowflake/blob/main/ROADMAP.md) and [issues](https://github.com/snowflakedb/terraform-provider-snowflake/issues). - Get support from the community in [discussion forums](https://github.com/snowflakedb/terraform-provider-snowflake/discussions). Snowflake Support and subject matter experts participate actively in the GitHub community and make a best effort to resolve issues. Snowflake provides official support as detailed below in [Officially supported versions](#label-terraform-support). - Review supplementary documentation and source code. - Review the [change log](https://github.com/snowflakedb/terraform-provider-snowflake/blob/main/CHANGELOG.md) and [migration guide](https://github.com/snowflakedb/terraform-provider-snowflake/blob/main/MIGRATION_GUIDE.md) to follow releases. |
| [Terraforming Snowflake](https://quickstarts.snowflake.com/guide/terraforming_snowflake/#0) | This Quickstart tutorial from Snowflake Labs guides you through creating a Terraform project in GitHub that uses the Snowflake provider to create a demo database and warehouse. |

Expand

Show lessSee more

## Versioning and preview features

The Snowflake Terraform provider follows semantic versioning. Major version releases include breaking changes. We announce these well in advance on GitHub. Minor version releases may sometimes include unexpected changes, depending on the configuration or environment. We balance the occasional one-time inconvenience for some users against the overall benefits these updates bring to the community.

### New features and fixes

- Generally, we introduce new features and fixes in the latest minor version. This is due to the resource-intensive development process and the need for extensive regression testing.
- If we discover a security vulnerability, we consider backporting critical fixes to earlier versions on a case-by-case basis.
- We assess BCRs introduced by underlying Snowflake features for impacts to the provider. The [migration guide](https://github.com/snowflakedb/terraform-provider-snowflake/blob/main/MIGRATION_GUIDE.md) provides information about how to manage potential breaking changes. We prioritize BCR fixes in each latest version release of the provider and recommend updating your version of the provider regularly.

### Preview features

Some resources and data sources are labeled “preview features” with each release.

- Please consider these features to be preview features in the provider, regardless of their state in Snowflake.
- Preview features are disabled by default. You must add the relevant feature name to the *preview\_features\_enabled* field in the provider configuration. The GitHub repository always contains a list of preview features.
- Each preview feature will be reworked and marked as a stable feature in future releases. Please expect that preview features might introduce breaking changes, even when the provider’s major version number does not change.
- Preview features, much like other Snowflake preview features, do not receive official Snowflake Support. However, the Product and Engineering teams can offer help.

## Officially supported versions

- Snowflake offers official support only for the latest version. When a new version is released, it immediately becomes the officially supported version. You can submit a case for official support of a Terraform provider issue using the processes described in [Contacting Snowflake Support](/user-guide/contacting-support). This support channel is limited to issues directly related to the Snowflake Terraform provider. For third-party issues, please contact the associated third-party provider support team.
- Official Snowflake Support began exclusively with version 2.0.0 and later. All other versions, including major versions earlier than 2.0.0, are not officially supported.
- Although the latest version of the provider is the only officially supported version, we make a best effort to support resolution of issues with earlier versions. After assessing the issue, Snowflake Support may at its discretion require an update to the latest version to support the troubleshooting process. Upgrading to the latest version will be the most likely resolution to issues.
