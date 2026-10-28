# Oct 27, 2026: Continuous and bulk file loading with CoCo (*General availability*)

Describe the files that you want to load, and CoCo builds the load for you: a Snowpipe pipeline that loads new files from cloud storage within minutes of their arrival, or a one-time `COPY INTO` for files that are already in place. Both capabilities load into standard Snowflake tables or Snowflake-managed Apache Iceberg™ tables. They’re now generally available in CoCo CLI, CoCo Desktop, and CoCo in Snowsight.

For continuous ingestion from Amazon S3, Microsoft Azure Blob Storage, or Google Cloud Storage, CoCo infers the schema, then sets up and validates the pipeline. Choose the setup that fits how you manage cloud access:

- **Let Snowflake handle cloud setup for Amazon S3:** Approve one temporary access request, and Snowflake creates the IAM role, bucket notifications, and Snowflake objects. You don’t need to provide long-lived AWS access keys. This option isn’t available in AWS GovCloud or China deployments.
- **Infrastructure as code:** Generate Terraform for the complete pipeline on any supported cloud.
- **Reuse or hand off:** Keep your existing storage integration, or give generated deployment files to your cloud team.

For one-time loads from a stage, cloud storage, or your computer, CoCo chooses the file format options, creates a table or uses an existing one, and loads the files on your warehouse.

For more information, see [Set up continuous file ingestion with CoCo](/user-guide/data-load-snowpipe-auto-coco) and [Bulk load files with CoCo](/user-guide/data-load-bulk-coco).
