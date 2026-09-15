# July 21, 2026: Improved Google Cloud Storage query performance for credential-vended Iceberg tables

You can now set the `VENDED_CREDENTIAL_STORAGE_REGION` parameter on Google Cloud Storage-backed
externally managed Iceberg tables that use catalog-vended credentials. Setting this parameter to
your Google Cloud Storage bucket’s region can significantly improve query latency.

The parameter can be set at the table, schema, or database level:

Copy code

```
ALTER TABLE <table_name>
  SET VENDED_CREDENTIAL_STORAGE_REGION = '<gcs_region>';
```

To use this feature, contact Snowflake Support to enable it for your account.

For more information, see
[Use catalog-vended credentials for Iceberg tables](/user-guide/tables-iceberg-configure-catalog-integration-vended-credentials).
