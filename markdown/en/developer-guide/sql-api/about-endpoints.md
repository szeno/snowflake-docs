# About the SQL API endpoints

The SQL API is available at `https://account_identifier.snowflakecomputing.com/api`, where `account_identifier` is
your [account identifier](/user-guide/admin-account-identifier).

## Using the SQL API over private connectivity

You can call the SQL API over AWS PrivateLink, Azure Private Link, or Google Cloud Private Service Connect instead of the
public internet. To do so, substitute your account’s private connectivity URL for the standard account URL in all SQL
API requests, including the base URL and the `statementHandle` URLs.

To determine the private connectivity URL for your account, run [SYSTEM$GET\_PRIVATELINK\_CONFIG](/sql-reference/functions/system_get_privatelink_config)
as the `ACCOUNTADMIN` role and use the returned `privatelink-account-url` value.

Before you can use private connectivity, you must configure it for your account. For instructions, see:

- [AWS PrivateLink and Snowflake](/user-guide/admin-security-privatelink) (AWS)
- [Azure Private Link and Snowflake](/user-guide/privatelink-azure) (Azure)
- [Google Cloud Private Service Connect and Snowflake](/user-guide/private-service-connect-google) (Google Cloud)

Beginning with Snowflake version 6.3, the API consists of the `/api/v2/statements/` resource and provides the following endpoints:

| Endpoint | Description |
| --- | --- |
| `/api/v2/statements/` | Use this endpoint to [submit SQL statements for execution](/developer-guide/sql-api/submitting-requests). |
| `/api/v2/statements/statementHandle` | Use this endpoint to [check the status of the execution of a statement](/developer-guide/sql-api/handling-responses#label-sql-api-checking-statement-status). (`statementHandle` is a unique identifier for the statement submitted for execution.) |
| `/api/v2/statements/statementHandle/cancel` | Use this endpoint to [cancel the execution of a statement](/developer-guide/sql-api/cancelling-requests). |

Expand

Show lessSee more

These endpoints include the new method of retrieving results, which was introduced in Snowflake version 5.40. However, when sending a request to these new endpoints, you do not need to set the format field to `jsonv2` in the `resultSetMetaData` field. If the format field is set in the request, the SQL API ignores the field.

The new version of the SQL API also removes concurrency limits, enabling you to retrieve query results from multiple threads.

You can use development tools and libraries for REST APIs (e.g. Postman) to send requests and handle responses.
