# About Openflow - Snowflake Deployments

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow - Snowflake Deployment runs on [Snowpark Container Services (SPCS)](/developer-guide/snowpark-container-services/overview) and
provides a streamlined and integrated solution for data integration and connectivity across interoperable storage like Iceberg and Snowflake native storage.
As a fully self-contained service within Snowflake, it’s easy to deploy and manage, offering a convenient and cost-effective environment for running your data flows.
A key advantage is its native integration with Snowflake’s security model, which allows seamless authentication, authorization, and network security, and simplified operations.

Although customers can have both BYOC and Snowflake Deployments, the following are use cases that are well-suited to Snowflake Deployments:

- Incorporating full-fidelity data in the bronze layer: Landing raw data from various sources directly into Snowflake and using Openflow Snowflake Deployments to extract and load.
- Enriching data: Running pipelines to enrich tables that already exist inside Snowflake.
- From ingest to insight in one place: Building applications where the entire data lifecycle (ingest, process and serve) happens within the Snowflake ecosystem.
- Transforming raw data to insights with AI: Ingesting unstructured data and then, for instance, using Snowflake CoWork to search and understand it better, all in concert with users’ other structured data.
- Employing reverse ETL: Closing the loop on insight generation by sharing with external operational systems via APIs, messaging infrastructure, and more.

## Understanding execute-as roles and External Access Integrations

Openflow - Snowflake Deployments must be able to interact with data sources and destinations
that are typically outside Snowflake. In addition, these deployments must also be able
to communicate with and access Snowflake itself.
Execute-as roles and external access integrations provide this support.

### What is an execute-as role?

An execute-as role is a Snowflake role bound to a specific Openflow runtime. Connectors that use `SNOWFLAKE_MANAGED` authentication run with this role’s privileges (or those of a child role granted to it). The execute-as role is used for the following tasks:

- Grant access to external access integrations (EAIs).
  These EAIs specify rules that allow the runtime
  to access the data sources and destinations from within Snowflake itself.
- Grant access to Snowflake resources.
- Grant access to resources that are connector-specific.

Because execute-as roles are linked to Openflow session tokens, you don’t need
to create separate service users and key pairs for authentication to Snowflake.

### What is an External Access Integration (EAI) within Openflow?

An [External access integration](/developer-guide/external-network-access/external-network-access-overview) (EAI)
is a Snowflake object designed to provide secure access to external resources,
like source systems from which Openflow connectors pull external data.
Openflow Snowflake Deployments use EAIs and network rules together to define the
endpoints an Openflow connector can read from or write to.

Data engineers define and configure EAIs and execute-as roles specific to a given connector and its underlying runtime.

## Typical Openflow - Snowflake Deployment workflow

The following sections describe Openflow - Snowflake Deployment concepts and workflows.

| User persona | Task |
| --- | --- |
| Snowflake administrator | - Configures core Snowflake and external access integrations.   See [Set up Openflow - Snowflake Deployment - Task overview](/user-guide/data-integration/openflow/setup-openflow-spcs).   - Creates a set of deployments in Snowflake.   The Openflow UI is used to manage deployments and runtime creation and maintenance. The Openflow UI allows users to create, upgrade, and delete runtimes in all deployments. |
| Data engineer (pipeline author, responsible for data ingestion) | - Works with a Snowflake administrator to configure required allow-listed domains so   that Openflow - Snowflake Deployment can access the external data sources. - Creates execute-as roles, external integrations, and other objects that can later be used by runtimes. - Uses the runtime canvas to build completely new flows or to configure deployed connectors.   Creates a completely new flow or uses an existing connector as-is or as a starting point to customize.  Connectors are a simple way to solve for a specific integration use case, and less technical users can deploy them without assistance from a data engineer. |
| Data engineer (pipeline operator) | Configures flow parameters and runs the flow. |
| Data engineer (responsible for transformation to silver and gold layers) | Responsible for transforming data from the bronze layer that was populated by the pipeline to silver and gold layers for analytics. |
| Business user | Makes use of gold layer objects for analytics. |

Expand

Show lessSee more

## Deployment and runtime hierarchy

Openflow separates management from execution:

- The **control plane** is the layer you use to create, upgrade, and observe deployments and runtimes through the Openflow UI or APIs. On Openflow - Snowflake Deployments, Snowflake operates the control plane.
- A **deployment** is the data plane container for your runtimes. Each deployment is backed by a [compute pool](/developer-guide/snowpark-container-services/working-with-compute-pool). An account can have multiple Openflow - Snowflake Deployments to separate workloads by project, team, or environment. See [Create deployment](/user-guide/data-integration/openflow/setup-openflow-spcs-deployment).
- A **runtime** hosts your data flows within a deployment. Each deployment can host multiple runtimes, and each runtime has its own execute-as role and network access configuration. See [Create runtime](/user-guide/data-integration/openflow/setup-openflow-spcs-create-runtime).

For definitions of all Openflow components, see [Openflow components](/user-guide/data-integration/openflow/about#label-openflow-components).

## Limitations

- Users with a default role of ACCOUNTADMIN can’t login to Openflow - Snowflake Deployment runtimes and will get an error message when attempting to do so.
- Snowflake account suspension for payment, billing, trial expiration or any other reason impacting the organization or account-status can affect Openflow - Snowflake Deployments. Once suspended, even if an account is reactivated, existing deployments will show as **Not Reporting** and are not recoverable. For details, see [Effect of Snowflake account suspension on Openflow Snowflake Deployments](/user-guide/data-integration/openflow/manage#label-openflow-recover-after-account-suspension).
- Customers requiring private connectivity will need to configure [outbound PrivateLink](/user-guide/private-connectivity-outbound).
  PrivateLink is available to [Business Critical Edition](/user-guide/intro-editions#label-snowflake-editions-business-critical) only.

### Next steps

[Set up Openflow - Snowflake Deployment - Task overview](/user-guide/data-integration/openflow/setup-openflow-spcs)
