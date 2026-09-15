# Snowpark Container Services

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

## About Snowpark Container Services

Snowflake started by providing a SQL database for querying structured and semi-structured data, but SQL alone isn’t ideal for complex computations or machine learning. To address this, Snowflake introduced [Snowpark](/developer-guide/snowpark/index), which lets developers use languages like Python, Java, and Scala to build data applications and pipelines. Snowpark translates this code into optimized SQL, combining the flexibility of modern languages with the performance and scalability of Snowflake’s SQL engine.

For more flexibility, Snowflake offers Snowpark Container Services, a managed container orchestration platform within Snowflake. You can package your application and its dependencies into an Open Container Initiative (OCI) image, which can include any programming language, framework, or library.
This enables use cases that require custom runtimes, specialized libraries, or specific software configurations. In addition, with support for advanced CPUs and GPUs, you can run compute-intensive workloads, such as ML model serving, ML model training, and advanced AI analytics. Snowflake manages the underlying infrastructure, but you have full control over the contents of your containerized environment.

As a fully managed service, Snowpark Container Services streamlines operational tasks related to running your containers. Using best practices, Snowpark Container Services handles the intricacies of container management, including security and configuration. This ensures that you can focus on developing and deploying your applications without the overhead of managing the underlying infrastructure.

Snowpark Container Services is fully integrated with Snowflake. For example, your application can easily perform these tasks:

- Connect to Snowflake and run SQL in a Snowflake virtual warehouse.
- Access data files in a Snowflake stage.
- Process data retrieved through SQL queries.

Your application can leverage your existing Snowflake configuration, including the following items:

- Network policies for network ingress
- External access integration for network egress
- Role-based access control for enabling service-to-service communications
- Event tables for logs, metrics, and events

Snowpark Container Services is also integrated with third-party tools. It lets you use third-party clients, such as Docker, to easily upload your application images to Snowflake. Seamless integration makes it easier for teams to focus on building data applications.

All these capabilities come with Snowflake platform benefits, most notably ease-of-use, security, and governance features. You also get a scalable, flexible compute layer next to the powerful Snowflake data layer without needing to move data off the platform.

## Common scenarios for using Snowpark Container Services

Your application can be deployed to Snowflake regions without concern for the underlying cloud platform (AWS, Azure, or Google Cloud). Snowpark Container Services also makes it easy for your application to access your Snowflake data. In addition, Snowflake manages the underlying compute nodes.

The following list shows the common workloads for Snowpark Container Services:

- **Batch Data Processing Jobs:** Run flexible jobs similar to stored procedures, pulling data from Snowflake or external sources, processing it, and producing results. Workloads can be distributed across multiple job instances, and graphics processing unit (GPU) support is available for computationally intensive tasks like AI and machine learning.
- **Service Functions:** Your service can provide a service function so that your queries can send batches of data to your service for processing. The query processing happens in Snowflake’s advanced query engine and your service provides custom data processing that Snowflake can scale to multiple compute nodes. For an example, see [Tutorial 1](/developer-guide/snowpark-container-services/tutorials/tutorial-1). In step 4 of this tutorial, you call the service function in a query.
- **APIs or Web UI Over Snowflake Data:** Deploy services that expose APIs or web interfaces with embedded business logic. Users interact with the service rather than raw data. Caller’s rights ensure that queries run with the correct user permissions. For an example, see [Tutorial 1](/developer-guide/snowpark-container-services/tutorials/tutorial-1). In this tutorial, the service also exposes a web UI to the internet. In step 4, you send requests to the service from a web browser.

## How does it work?

To run containerized applications in Snowpark Container Services, in addition to working with the basic Snowflake objects, such
as databases and warehouses, you work with these objects: [image repository](/developer-guide/snowpark-container-services/working-with-registry-repository),
[compute pool](/developer-guide/snowpark-container-services/working-with-compute-pool), and [service](/developer-guide/snowpark-container-services/working-with-services).

Snowflake offers an [OCIv2](https://github.com/opencontainers/distribution-spec/blob/main/spec.md)
compliant *image registry* service for storing your images. This service enables Open Container Initiative (OCI) clients, such as Docker CLI, to upload your application images to a *repository* (a storage unit) in your
Snowflake account. You create a repository using the [CREATE IMAGE REPOSITORY](/sql-reference/sql/create-image-repository) command. For more information, see
[Working with an image registry and repository](/developer-guide/snowpark-container-services/working-with-registry-repository).

After you upload your application image to a repository, you can run your application by creating a
[long-running service or executing a job service](/developer-guide/snowpark-container-services/working-with-services).

- **Service:** A service is long-running and, as with a web service, you explicitly stop it when it is no longer needed. If a service container
  exits for whatever reason, Snowflake restarts that container. To create a service, such as a full stack web application,
  use the [CREATE SERVICE](/sql-reference/sql/create-service) command.
- **Job service:** A job service has a finite lifespan, similar to a stored procedure.
  When all containers exit, the job service is done. Snowflake doesn’t restart any job service containers. To start a job service, such as training a machine learning model with GPUs, use the
  [EXECUTE JOB SERVICE](/sql-reference/sql/execute-job-service) command.

Your services, including job services, run in a *compute pool*, which is a collection of one or more virtual machine (VM) nodes. You first
create a compute pool by using the [CREATE COMPUTE POOL](/sql-reference/sql/create-compute-pool) command, and then specify the compute pool when
you create a service or a job service. The required information to create a compute pool includes the machine type, the minimum number of nodes to
launch the compute pool with, and the maximum number of nodes the compute pool can scale to. Some of the supported machine types
provide GPU. For more information, see [Working with compute pools](/developer-guide/snowpark-container-services/working-with-compute-pool).

After you create a service, users in the same Snowflake account that created the service can use the service, if they have the appropriate permissions. For more information, see [Using a service](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating).

Note

The Snowpark Container Services documentation primarily uses SQL commands and functions in explanations of concepts and in examples. Snowflake also provides other interfaces, including [Python APIs](/developer-guide/snowflake-python-api/snowflake-python-overview), [REST APIs](/developer-guide/snowflake-rest-api/snowflake-rest-api), and the [Snowflake CLI](/developer-guide/snowflake-cli/index) command-line tool for most operations.

## Available regions and considerations

Snowpark Container Services is in all [regions](/user-guide/intro-regions) except the following:

- Snowpark Container Services supports [public sector (government) workloads](/user-guide/intro-regions#label-us-gov-regions) in the AWS US East (Commercial Gov - N. Virginia) region and is not available in other AWS or Azure government regions.
- Currently, Snowpark Container Services in the GCP Dammam region uses the global endpoints for Google Cloud APIs.

## What’s next?

If you’re new to Snowpark Container Services, we suggest that you first explore the tutorials and then continue with other
topics to learn more and create your own containerized applications. The following topics provide more information:

- **Tutorials:** These [introductory tutorials](/developer-guide/snowpark-container-services/overview-tutorials) provide step-by-step instructions for you to explore
  Snowpark Container Services. After initial exploration, you can continue with
  [advanced tutorials](/developer-guide/snowpark-container-services/overview-advanced-tutorials).
- **Service specification reference:** This reference explains the [YAML syntax](/developer-guide/snowpark-container-services/specification-reference) to
  create a service specification.
- **Working with services and job services:** These topics provide details about the Snowpark Container Services components that you use
  in developing services and job services:

  - [Working with an image registry and repository](/developer-guide/snowpark-container-services/working-with-registry-repository)
  - [Working with compute pools](/developer-guide/snowpark-container-services/working-with-compute-pool)
  - [Working with services](/developer-guide/snowpark-container-services/working-with-services)
  - [Troubleshooting](/developer-guide/snowpark-container-services/troubleshooting)
- **Reference:** Snowpark Container Services provides the following SQL commands and functions:

  - SQL commands: [Snowpark Container Services commands](/sql-reference/commands-snowpark-container-services) and [CREATE FUNCTION (Snowpark Container Services)](/sql-reference/sql/create-function-spcs)
  - SQL functions:
    - System function: [SYSTEM$GET\_SERVICE\_LOGS](/sql-reference/functions/system_get_service_logs)
    - Scalar functions: [Snowpark Container Services functions](/sql-reference/functions-spcs)
    - Table-valued functions:
      - [GET\_JOB\_HISTORY](/sql-reference/functions/get_job_history)
      - [SPCS\_GET\_LOGS](/sql-reference/functions/spcs_get_logs)
      - [SPCS\_GET\_EVENTS](/sql-reference/functions/spcs_get_events)
      - [SPCS\_GET\_METRICS](/sql-reference/functions/spcs_get_metrics)
- **Billing:** This topic explains the costs associated with using Snowpark Container Services:

  - [Snowpark Container Services costs](/developer-guide/snowpark-container-services/accounts-orgs-usage-views)
