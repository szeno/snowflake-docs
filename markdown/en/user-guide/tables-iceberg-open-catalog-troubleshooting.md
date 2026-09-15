# Troubleshooting using Apache Iceberg™ tables with Snowflake Open Catalog in Snowflake

Note

New customers should use [Snowflake Horizon Catalog](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon)
for Apache Iceberg™ tables and multi-engine interoperability with Iceberg. Customers who
haven’t previously created a Snowflake Open Catalog account can’t sign up for their first Open
Catalog account.

Existing Snowflake Open Catalog customers can continue to use and can create additional
Open Catalog accounts if necessary.

The following scenarios can help you troubleshoot issues that might occur when using Apache Iceberg™ tables with Snowflake Open Catalog in
Snowflake.

## You can’t create a catalog integration for Open Catalog

This section describes how to troubleshoot creating a catalog integration for Open Catalog.

To troubleshoot, identify the error message you received in the SQL output when the creation of your catalog integration failed.

|  |  |
| --- | --- |
| Error | ``` SQL Execution Error: Cannot create catalog integration <catalog_integration_name> due to error: Unable to process: Unable to find warehouse <catalog_name>. Check the REST configuration and ensure the warehouse name '<catalog_name>' matches the Polaris catalog name. ``` |
| Cause | The `<open_catalog_name>` you specified for the `CATALOG_NAME` parameter in your catalog integration doesn’t match the name of any external catalog in the Open Catalog account at the `<polaris_account_url>` you specified for the `CATALOG_URI` parameter. |
| Solution | Update `<open_catalog_name>` for the `CATALOG_NAME` parameter to exactly match the name of the external catalog in Open Catalog, and try creating the catalog integration again. If you haven’t created the external catalog yet, follow the instructions in [Create a catalog](https://other-docs.snowflake.com/en/opencatalog/create-catalog).  Important  `<open_catalog_name>` is case-sensitive. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Error | ``` SQL Execution Error: User provided authentication credentials are invalid for catalog integration <catalog_integration_name> due to error: Malformed request: unauthorized_client: The client is not authorized. ``` |
| Cause | The OAuth token you specified in the catalog integration isn’t valid. |
| Solution | Ensure that the values specified for `OAUTH_CLIENT_ID` and `OAUTH_CLIENT_SECRET` in your catalog integration are valid values for an existing service connection. To validate, compare these values with the service credential values you saved when you [configured the service connection](https://other-docs.snowflake.com/en/opencatalog/configure-service-connection#configure-a-service-connection). If they don’t match, update the values to match. |

Expand

Show lessSee more

## You can’t create a Snowflake-managed table

This section describes how to troubleshoot creating a Snowflake-managed table.

To troubleshoot, identify the error message you received in the SQL output when the creation of your table failed.

|  |  |
| --- | --- |
| Error | ``` SQL Execution Error: Failed to validate CATALOG_SYNC target '<catalog_integration_name>' due to error: The Snowflake service connection associated with the Polaris catalog integration does not have the required privileges to send notifications. The minimum required privileges are TABLE_CREATE, TABLE_WRITE_PROPERTIES, TABLE_DROP, NAMESPACE_CREATE, and NAMESPACE_DROP. ``` |
| Cause | The catalog role for the external catalog you want to connect to doesn’t have the necessary privileges to send notifications to Open Catalog. |
| Solution | Update the catalog role by granting all of the following privileges to the catalog role for your external catalog:   - TABLE\_CREATE - TABLE\_WRITE\_PROPERTIES - TABLE\_DROP - NAMESPACE\_CREATE - NAMESPACE\_DROP   Where you update the catalog role depends on whether the grants it has are applied at the catalog, namespace, or table level. See the applicable procedure for your catalog role:   - [Update the privileges granted to a catalog role at the catalog level](https://other-docs.snowflake.com/en/opencatalog/secure-catalogs#update-the-privileges-granted-to-a-catalog-role-at-the-catalog-level) - [Update the privileges granted to a catalog role at the namespace level](https://other-docs.snowflake.com/en/opencatalog/secure-catalogs#update-the-privileges-granted-to-a-catalog-role-at-the-namespace-level) - [Update the privileges granted to a catalog role at the table level](https://other-docs.snowflake.com/en/opencatalog/secure-catalogs#update-the-privileges-granted-to-a-catalog-role-at-the-table-level) |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Error | ``` SQL Execution Error: Failed to access the REST endpoint of catalog integration <catalog_integration_name> with error: Unable to process: Failed to get subscoped credentials: Error assuming AWS_ROLE: User: <IAM_user_arn> is not authorized to perform: sts:AssumeRole on resource: <S3_role_arn>. Check the accessibility of the REST catalog URI or warehouse. ``` |
| Cause | The AWS IAM user for your external catalog can’t assume the role that has permission to access S3. |
| Solution | Modify the policy document in AWS to allow the IAM user for your Open Catalog account to assume the role that has permission to access your S3 bucket. To modify the policy document, you need to update the IAM role in AWS. For details, see [Retrieve the AWS IAM user for your Snowflake Open Catalog account](https://other-docs.snowflake.com/en/opencatalog/create-catalog#step-4-retrieve-the-aws-iam-user-for-your-open-catalog-account) and then [Grant the IAM user permissions to access bucket objects](https://other-docs.snowflake.com/en/opencatalog/create-catalog#step-5-grant-the-iam-user-permissions-to-access-bucket-objects).  Remember that the policy document must include the IAM user ARN and external ID for both your external volume and external catalog in Open Catalog. In the following example policy document, note the following values:   - `arn:aws:iam::111111111111:user/----0000-s` is the STORAGE\_AWS\_IAM\_USER\_ARN for the external volume. - `arn:aws:iam::222222222222:user/----0000-s` is the IAM user ARN for the external catalog in Snowflake Open Catalog. - `Iceberg_table_external_id` is the STORAGE\_AWS\_EXTERNAL\_ID for your external volume and also the external ID for your external   Catalog in Open Catalog.   Copy code  ``` {      "Version": "2012-10-17",      "Statement": [        {          "Sid": "",          "Effect": "Allow",          "Principal": {            "AWS": [                "arn:aws:iam::111111111111:user/----0000-s",                "arn:aws:iam::222222222222:user/----0000-s"             ]          },          "Action": "sts:AssumeRole",          "Condition": {            "StringEquals": {              "sts:ExternalId": "iceberg_table_external_id"            }          }        }      ]    } ``` |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Error | ``` SQL Execution Error: Failed to validate CATALOG_SYNC target '<catalog_integration_name>' due to error: The associated Polaris catalog cannot be of type INTERNAL. ``` |
| Cause | You’re attempting to sync a Snowflake-managed table to an internal catalog in Open Catalog. You can only sync a Snowflake-managed table to an external catalog in Open Catalog. |
| Solution | You can’t update an existing internal catalog to an external catalog, so you must create a new external catalog:  1. Follow the instructions in [Create a catalog](https://other-docs.snowflake.com/en/opencatalog/create-catalog) to create an external catalog in your Open Catalog account. When creating the catalog,    ensure that the **External** toggle is enabled. 2. Update `<open_catalog_name>` for the `CATALOG_NAME` parameter in your catalog integration to the name of the external    catalog you created. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Error | ``` SQL Execution Error: Failed to validate CATALOG_SYNC target '<catalog_integration_name>' due to error: SQL Execution Error: Resource on the REST endpoint of catalog integration CATINT is forbidden due to error: Forbidden: Invalid locations '[<path to metadata file>]' for identifier '<identifier>': <path to metadata file> is not in the list of allowed locations: [<list of allowed locations>]. ``` |
| Cause | The path to the metadata file for the table you want to create isn’t included in the list of allowed locations for your external cloud provider. As a result, Open Catalog can’t access the metadata file for the table. |
| Solution | Ensure that the location of the metadata file falls under the file path of the default base location for the catalog that the service admin created in Open Catalog, or that it falls under any of the additional allowed locations, if applicable. For the list of allowed locations, select the catalog in Open Catalog and refer to the **Locations** field. |

Expand

Show lessSee more

## You can’t alter an Iceberg table when specifying the CATALOG\_SYNC parameter

This section describes how to troubleshoot altering the CATALOG\_SYNC parameter.

To troubleshoot, identify the error message you received in the SQL output when your table alteration failed.

|  |  |
| --- | --- |
| Error | ``` SQL Execution Error: Failed to validate CATALOG_SYNC target '<catalog_integration_name>' due to error: The Snowflake service connection associated with the Polaris catalog integration does not have the required privileges to send notifications. The minimum required privileges are TABLE_CREATE, TABLE_WRITE_PROPERTIES, TABLE_DROP, NAMESPACE_CREATE, and NAMESPACE_DROP. ``` |
| Cause | The catalog role for the external catalog you want to connect to doesn’t have the necessary privileges to send notifications to Open Catalog. |
| Solution | Grant all of the following privileges to the catalog role for your external catalog:   - TABLE\_CREATE - TABLE\_WRITE\_PROPERTIES - TABLE\_DROP - NAMESPACE\_CREATE - NAMESPACE\_DROP   Where you update the catalog role depends on whether its grants are applied at the catalog, namespace, or table level. See the applicable procedure for your catalog role:   - [Update the privileges granted to a catalog role at the catalog level](https://other-docs.snowflake.com/en/opencatalog/secure-catalogs#update-the-privileges-granted-to-a-catalog-role-at-the-catalog-level) - [Update the privileges granted to a catalog role at the namespace level](https://other-docs.snowflake.com/en/opencatalog/secure-catalogs#update-the-privileges-granted-to-a-catalog-role-at-the-namespace-level) - [Update the privileges granted to a catalog role at the table level](https://other-docs.snowflake.com/en/opencatalog/secure-catalogs#update-the-privileges-granted-to-a-catalog-role-at-the-table-level) |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Error | ``` SQL Execution Error: Failed to access the REST endpoint of catalog integration <catalog_integration_name> with error: Unable to process: Failed to get subscoped credentials: Error assuming AWS_ROLE: User: <IAM_user_arn> is not authorized to perform: sts:AssumeRole on resource: <S3_role_arn>. Check the accessibility of the REST catalog URI or warehouse. ``` |
| Cause | The AWS IAM user for your external catalog doesn’t have permission to access S3 bucket objects. |
| Solution | Modify the policy document in AWS to allow the IAM user for your Open Catalog account to access objects in your S3 bucket. To modify the policy document, you need to update the IAM role in AWS. For details, see [Retrieve the AWS IAM user for your Polaris Open Catalog account](https://other-docs.snowflake.com/en/opencatalog/create-catalog#step-4-retrieve-the-aws-iam-user-for-your-open-catalog-account) and then [Grant the IAM user permissions to access bucket objects](https://other-docs.snowflake.com/en/opencatalog/create-catalog#step-5-grant-the-iam-user-permissions-to-access-bucket-objects).  Remember that the policy document must include the IAM user ARN and external ID for both your external volume and external catalog in Open Catalog. In the following example policy document, note the following values:   - `arn:aws:iam::111111111111:user/----0000-s` is the STORAGE\_AWS\_IAM\_USER\_ARN for the external volume - `arn:aws:iam::222222222222:user/----0000-s` is the IAM user ARN for the external catalog in Snowflake Open Catalog. - `Iceberg_table_external_id` is the STORAGE\_AWS\_EXTERNAL\_ID for your external volume and also the external ID for your   external catalog in Open Catalog.   Copy code  ``` {      "Version": "2012-10-17",      "Statement": [        {          "Sid": "",          "Effect": "Allow",          "Principal": {            "AWS": [                "arn:aws:iam::111111111111:user/----0000-s",                "arn:aws:iam::222222222222:user/----0000-s"             ]          },          "Action": "sts:AssumeRole",          "Condition": {            "StringEquals": {              "sts:ExternalId": "iceberg_table_external_id"            }          }        }      ]    } ``` |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Error | ``` SQL Execution Error: Failed to validate CATALOG_SYNC target '<catalog_integration_name>' due to error: The associated Polaris catalog cannot be of type INTERNAL. ``` |
| Cause | You’re attempting to sync a Snowflake-managed Iceberg table to a catalog integration for an internal catalog in Open Catalog. You can only sync a Snowflake-managed Iceberg table to an external catalog in Open Catalog. |
| Solution | You can’t update an existing internal catalog to an external catalog, so you must create a new external catalog:   1. Follow the instructions in [Create a catalog](https://other-docs.snowflake.com/en/opencatalog/create-catalog) to create an    external catalog in your Open Catalog account. When creating the catalog, ensure that the **External** toggle is enabled. 2. Update `open_catalog_name` for the `CATALOG_NAME` parameter in your catalog integration to the name of the external    catalog you created. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Error | ``` SQL Execution Error: Failed to validate CATALOG_SYNC target '<catalog_integration_name>' due to error: SQL Execution Error: Resource on the REST endpoint of catalog integration CATINT is forbidden due to error: Forbidden: Invalid locations '[<path to metadata file>]' for identifier '<identifier>': <path to metadata file> is not in the list of allowed locations: [<list of allowed locations>]. ``` |
| Cause | The path to the metadata file for the table you want to create isn’t included in the list of allowed locations for your external cloud provider. As a result, Open Catalog can’t access the metadata file for the table. |
| Solution | Ensure that the location of the metadata file falls under the file path of the default base location for the catalog that the service admin created in Open Catalog, or that it falls under any of the additional allowed locations, if applicable. For the list of allowed locations, select the catalog in Open Catalog and refer to the **Locations** field. |

Expand

Show lessSee more
