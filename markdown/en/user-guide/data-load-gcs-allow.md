# Allow access to Google Cloud Storage

If your Google Cloud organization enforces a
[domain restriction constraint](https://cloud.google.com/resource-manager/docs/organization-policy/restricting-domains),
a Google Cloud administrator must allow the
Google Workspace customer ID in the domain restriction so that the Snowflake service account can access your storage.

Important

If your Google Cloud organization was created on or after May 3, 2024, Google Cloud enforces a
[domain restriction constraint](https://cloud.google.com/resource-manager/docs/organization-policy/restricting-domains)
in project organization policies. The default constraint lists your domain as the only allowed value.

To allow the Snowflake service account access to your storage, you must
[update the domain restriction](/user-guide/data-load-gcs-allow).

## Retrieve the Google Workspace customer ID

Before you can update an organization policy, you must retrieve the
Google Workspace customer ID associated with the Snowflake service account.

Call the [SYSTEM$GET\_SNOWFLAKE\_PLATFORM\_INFO](/sql-reference/functions/system_get_snowflake_platform_info) function:

Copy code

```
SELECT SYSTEM$GET_SNOWFLAKE_PLATFORM_INFO();
```

The function returns the project ID and Google Workspace customer ID (`snowflake-customer-directory-id`) for the Snowflake service account.

Example output:

```
{
  "snowflake-project-id":["preprod-deployment1-a12b"],
  "snowflake-customer-directory-id":["A01bcd2ef"]
}
```

## Update the allow list for a domain constraint

To update the allow list for your domain constraint, you must update your organization policy. Specifically,
you must add the Google Workspace customer ID for the Snowflake service account to the `allowed_values`
list in the constraint.

For instructions, see
[Setting the organization policy](https://cloud.google.com/resource-manager/docs/organization-policy/restricting-domains#setting_the_organization_policy)
in the Google Cloud documentation.
