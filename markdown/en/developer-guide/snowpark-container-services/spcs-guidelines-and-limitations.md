# Snowpark Container Services: Guidelines and limitations

- **General limitations:** If you encounter any issues with these limitations, contact your account representative.

  - You can create up to 5000 services in your Snowflake account.
  - Each service can have up to 100 endpoints (see [spec.endpoints](/developer-guide/snowpark-container-services/specification-reference#label-spcs-spec-ref-spec-endpoints)).
  - Each service can have up to 20 containers (see [spec.containers](/developer-guide/snowpark-container-services/specification-reference#label-spcs-spec-ref-spec-containers)).
  - Each service can have up to 50 secrets (see [containers.secrets](/developer-guide/snowpark-container-services/specification-reference#label-spcs-spec-ref-containers-secrets)).
  - Each service can have up to 20 volumes (see [spec.volumes](/developer-guide/snowpark-container-services/specification-reference#label-snowpark-containers-spec-volume)).
  - The following limitations apply when you enable internet access (see [Configure service egress](/developer-guide/snowpark-container-services/service-network-communications#label-working-with-services-jobs-egress)) using external access integrations (EAIs).

    - Each service can support up to 10 EAIs (see [CREATE SERVICE](/sql-reference/sql/create-service) and [ALTER SERVICE](/sql-reference/sql/alter-service)).
    - Each EAI can have up to 100 host names.
  - When accessing the public endpoint from the internet, you might find that username/password authentication works, but SSO results in a blank page or the error: “OAuth client integration with the given client ID is not found.”. For information about addressing this issue, see [Ingress and SSO considerations](/developer-guide/snowpark-container-services/service-network-communications#label-additional-considerations-ingress-sso).
- **Image platform requirements:** Currently, Snowpark Container Services requires linux/amd64 platform images.
- **Service containers are not privileged:** Service containers do not run as privileged, and therefore cannot change
  the configuration of the hardware on the host and can change only limited OS configurations. Service containers can only
  perform operating system configurations that a normal user (that is, a user who doesn’t require root) can do.
- **Renaming the database and schema:**

  - Do not rename databases and schemas where you already created a service. Renaming is effectively moving a service to another
    database and schema, which is not supported. For example:

    - Database and schema information that Snowflake provided to the running service containers will continue to refer to the
      old names.
    - New logs that services ingest in the event table will continue to refer to the old database and schema names.
    - The service function will continue to reference the service in the old database and schema, and when you invoke the service
      function, it will fail.
  - A service specification can reference objects such as Snowflake stages and image repositories. If you rename database or
    schema names where these objects reside, you need to manually update the database and schema names of the referenced objects
    in the service specification.
- **Transferring ownership of parent schema or database:**

  The ownership of the parent database/schema can be transferred to a different role. But the ownership of services inside the database/schema is not transferred to the new role because services run as service owner roles and that does not change. As a result, the services could lose permissions on objects inside the schema, such as image repositories and Snowflake stages in the same schema.

  If ownership transfer of parent schema/database is required, consider re-creating the services.
- **Dropping and un-dropping a database and schema:**

  - When you drop the parent database or schema, services are deleted asynchronously. This means that a service might continue
    to run for some time before internal processes remove it.
  - If you attempt to un-drop a previously deleted database or schema, there is no guarantee that services will be restored.
- **Ownership transfer of services:** [Ownership transfer](/sql-reference/sql/grant-ownership) or future ownership transfer for services, including job services, isn’t supported.
- **Ownership transfer of service functions:**

  The ownership of a service function can be transferred different role. If the new owner role doesn’t have USAGE privilege on the service, function invocations will fail. You need to grant USAGE privilege to the new function owner role.
- **Replication:** When dealing with replication in Snowflake, note the following:

  - Snowpark Container Services objects, such as services, compute pools, and repositories, cannot be replicated.
  - If you create a repository within a database, the entire database cannot be replicated. In cases where the database contains
    other resources, such as services or compute pools, the database replication process will succeed, but these
    individual objects within the database will not be replicated.
- **Job services timeout:** Snowpark Container Services job services runs synchronously by default. If a statement times out, the job service is canceled. The
  default statement timeout is two days. Customers can change the timeout by setting the parameter STATEMENT\_TIMEOUT\_IN\_SECONDS
  using ALTER SESSION.

  Copy code

  ```
  ALTER SESSION SET statement_timeout_in_seconds=<time>
  ```

  Set it before running the EXECUTE JOB SERVICE command. You can run job services asynchronously, by specifying `ASYNC=true`, to avoid job services from being interrupted by a statement timeout.
- **File staging commands support in Google Cloud:** To use the PUT, GET, LIST, or REMOVE command with Snowflake client libraries on Google Cloud, update your clients to at least the following versions.

  | Client | Version |
  | --- | --- |
  | Go Snowflake Driver | 1.14.1 |
  | Snowflake Connector for Python | 3.16.0 |
  | .NET driver | 4.6.0 |
  | Node.js Driver | 2.1.3 |
  | JDBC Driver | 3.25.1 |
  | ODBC Driver | 3.10.0 |

  Expand

  Show lessSee more
