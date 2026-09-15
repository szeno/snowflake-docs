# Access control requirements for ML Jobs

To use Snowflake ML Jobs, users need specific access privileges assigned to their roles. This page outlines the required privileges for both setting up new environments and using existing ones.

## Setting Up a New Environment

Creating a new environment for ML Jobs requires the following privileges:

- CREATE COMPUTE POOL privilege on the account: Required to create new compute pools. Alternatively, you may use any existing compute pool.
- CREATE SCHEMA privilege on the database (optional): Needed if you want to create a new schema for organizing ML Jobs and resources. We recommend this approach to easily clean up old jobs and payload stages.

## Using an Existing Environment

For users who will be executing ML Jobs in an existing environment, the following privileges are required:

Basic Access

- USAGE privilege on the database where the ML Jobs run
- USAGE privilege on the schema where ML Jobs run
- CREATE SERVICE privilege on the schema to create and manage ML Jobs
- USAGE privilege on the compute pool to allow it to be used for ML workloads
- USAGE privilege on a stage to upload ML Job payloads for execution

Note

If you don’t have an existing stage, the ML Job creates one on your behalf using the specified `stage_name`.
This requires the CREATE STAGE privilege on the schema.

## Additional Requirements

- Data Access Privileges: Users need appropriate privileges for any data tables, warehouses, or other resources their ML workloads will access
