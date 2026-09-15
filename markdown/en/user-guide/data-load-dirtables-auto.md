# Automated directory table metadata refreshes

You can automatically refresh the metadata for a directory table on an internal or external stage.

The refresh operation synchronizes the metadata with the latest set of associated files in storage, and occurs
in response to the following types of changes:

> - New files in the path are added to the table metadata.
> - Files in the path are updated in the table metadata.
> - Files no longer in the path are removed from the table metadata.

## Internal stages

[Preview Feature](/release-notes/preview-features) — Open

Preview support for this feature is only available to Snowflake accounts hosted on Amazon Web Services (AWS).

Automatically refreshing the directory table on an internal stage
synchronizes the metadata with the latest set of associated files in the internal named stage and path when the following occur:

> - New files in the path are added to the table metadata.
> - Changes to files in the path are updated in the table metadata.
> - Files no longer in the path are removed from the table metadata.

### Create an internal named stage with a directory table enabled

Create an internal named stage with a directory table enabled by using the [CREATE STAGE](/sql-reference/sql/create-stage) command. Snowflake reads
your staged data files into the directory table metadata.

Copy code

```
CREATE STAGE my_int_stage
  DIRECTORY = (
    ENABLE = TRUE
    AUTO_REFRESH = TRUE
  );
```

## External stages

You can automatically refresh the metadata for a directory table by using the following event notification services:

- **Amazon S3:** [Amazon SQS (Simple Queue Service)](https://aws.amazon.com/sqs/)
- **Google Cloud Storage:** [Google Cloud Pub/Sub](https://cloud.google.com/storage/docs/reporting-changes)
- **Microsoft Azure:** [Microsoft Azure Event Grid](https://azure.microsoft.com/en-us/services/event-grid/)

To set up automated refreshes, see the topic for the cloud storage service where your files are located:

- [Refresh directory tables automatically for Amazon S3](/user-guide/data-load-dirtables-auto-s3)
- [Refresh directory tables automatically for Google Cloud Storage](/user-guide/data-load-dirtables-auto-gcs)
- [Refresh directory tables automatically for Azure Blob Storage](/user-guide/data-load-dirtables-auto-azure)

### Cross-cloud support

Snowflake supports cross-cloud, cross-region automated directory table refreshes for external stages.

The following table shows the cross-cloud options that Snowflake supports for automated directory table refreshes,
based on the [cloud platform](/user-guide/intro-cloud-platforms) that hosts your Snowflake account.

|  | Amazon S3 | Google Cloud Storage | Microsoft Azure Blob storage | Microsoft Data Lake Storage Gen2 | Microsoft Azure General-purpose v2 |
| --- | --- | --- | --- | --- | --- |
| Accounts hosted on AWS | ✔ | ✔ | ✔ | ✔ | ✔ |
| Accounts hosted on GCP | ✔ | ✔ | ✔ | ✔ | ✔ |
| Accounts hosted on Azure | ✔ | ✔ | ✔ | ✔ | ✔ |

Expand

Show lessSee more

## Considerations

- Automated refreshes are event-based and provide better performance than manual refreshes for large or fast-growing stages.
- Automated refreshes for internal stages is currently available for accounts hosted on AWS. Snowflake
  doesn’t support refreshing the directory table metadata on an internal stage when your account is hosted on Google Cloud or Azure.

**Next Topics:**

- [Refresh directory tables automatically for Amazon S3](/user-guide/data-load-dirtables-auto-s3)
- [Refresh directory tables automatically for Google Cloud Storage](/user-guide/data-load-dirtables-auto-gcs)
- [Refresh directory tables automatically for Azure Blob Storage](/user-guide/data-load-dirtables-auto-azure)
