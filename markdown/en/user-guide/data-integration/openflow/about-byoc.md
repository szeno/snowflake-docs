# About Openflow: BYOC deployments

Feature — Generally Available

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC *is* Openflow and contains all the benefits of Openflow, but within your existing cloud.

## Typical BYOC workflow

| User persona | Task |
| --- | --- |
| AWS cloud engineer/administrator | Creates a set of deployments in their AWS cloud account.  The Openflow UI is used to manage deployments and runtime creation and maintenance. The Openflow UI allows users to create, upgrade, and delete runtimes in all deployments.  Snowflake sign-ins are used to authenticate to Openflow, and roles and privileges are used to control access to Openflow deployments and runtimes. |
| Data engineer (pipeline author, responsible for data ingestion) | Uses the runtime canvas to build completely new flows or to configure deployed connectors.  Creates a completely new flow or uses an existing connector as-is or as a starting point to customize. Populates data in the bronze layer within your Snowflake account (or other target system).  Connectors are a simple way to solve for a specific integration use case, and less technical users can deploy them without necessarily needing a data engineer. |
| Data engineer (pipeline operator) | Configures the flow parameters and runs the flow. |
| Data engineer (responsible for transformation to silver and gold layers) | Responsible for transforming data from the bronze layer that was populated by the pipeline to silver and gold layers for analytics. |
| Business user | Makes use of gold layer objects for analytics. |

Expand

Show lessSee more

## Limitations

- As described in the [Snowflake Openflow BYOC terms](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/openflow-terms/),
  securing Openflow BYOC is a shared responsibility model.
- Openflow authorization uses roles and their associated privileges that are directly granted to the user.
  Currently, Openflow does not support authorization when the role is attached to another role within the user’s role hierarchy.
- Openflow BYOC deployments obtain all container images from the Snowflake System Image Registry.
  Sourcing Openflow images from a customer-owned AWS ECR repository is not supported.
- The EKS cluster name is derived from the generated Openflow deployment key and is not configurable.
- AWS CloudFormation stack tags are applied to the AWS-level resources created for the deployment, but
  not to Kubernetes-level objects inside the EKS cluster. For details, see
  [BYOC deployment customization and tagging behavior](/user-guide/data-integration/openflow/setup-openflow-byoc#label-openflow-byoc-customization-tagging).

## Next steps

[Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc)
