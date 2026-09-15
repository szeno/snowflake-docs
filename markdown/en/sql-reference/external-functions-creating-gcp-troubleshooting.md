# Troubleshooting external functions for GCP

This topic provides troubleshooting information for external functions for GCP.

# Platform-independent Runtime Issues

## Data Type Return Values Do Not Match Expected Return Values

When passing arguments to or from an external function, ensure that the data types are appropriate. If the value
sent can’t fit into the data type being received, the value might be truncated or corrupted in some other way.

For more details, see [Ensure that arguments to the external function correspond to arguments parsed by the remote service](/sql-reference/external-functions-best-practices#label-external-functions-general-ensure-arguments-correspond).

## Error: Row numbers out of order

Possible Causes:
:   The row numbers you return within each batch should be monotonically ascending integers starting at 0. The input row numbers must also
    follow this rule, and each output row should match the corresponding input row. For example, the output in output row 0 should
    correspond to the input in input row 0.

Possible Solutions:
:   Ensure that the row numbers you return are the same as the row numbers you received, and that each output value uses the row number of
    the corresponding input. If this doesn’t work, then the input row numbers may not be correct or you did not return the rows in the
    correct order.

    Next, ensure that the output row numbers start from 0, increase by 1, and are in order.

For more information about data input and output formats, see [Remote service input and output data formats](/sql-reference/external-functions-data-format#label-external-functions-data-format).

## Error: “Error parsing JSON: Invalid response”

Possible Causes:
:   The most likely cause is that the JSON returned by the remote service (e.g. AWS Lambda function) is not constructed correctly.

Possible Solutions:
:   Ensure that the external function returns an array of arrays, with one inner array returned for each input row received. Review the
    description of the output format at [Data format received by Snowflake](/sql-reference/external-functions-data-format#label-format-of-data-to-snowflake).

## Error: Format of the returned value is not JSON

Possible Causes:
:   Your return value includes double quotes inside the value.

Possible Solutions:
:   Although JSON strings are delimited by double quotes, the string itself should not start and end with a quotation mark in most cases.
    If the embedded double quotes are incorrect, remove them.

## Error: Function received the wrong number of rows

Possible Causes:
:   The remote service tried to return more or fewer rows than it received. Even though the function is nominally scalar, it might receive
    multiple rows in the `body` field of the `event` parameter, and should return exactly as many rows as it received.

Possible Solution(s):
:   Ensure that the remote service returns one row for each row that it receives.

## GCP-specific issues

### Error: Request fails with ‘{“message”:”Audiences in jwt are not allowed”,”code”:403}’

Possible Causes:
:   The value in the API integration’s `google_audience` field is not allowed.

Possible Solutions:
:   - Verify that the API Integration’s `google_audience` value matches the managed service name of your API, which should be
      recorded in the `Managed Service Identifier` field in your tracking worksheet.
    - If you added an **x-google-audiences** field to the **securityDefinitions** section of your API config file, make sure that
      the value in **x-google-audiences** matches the value in the `google_audience` field of the API integration.

For more information about authenticating with Google, see the Google service account
[authentication documentation](https://cloud.google.com/api-gateway/docs/authenticate-service-account#configure_auth).

### Error: Request fails with ‘{“message”:”Jwt is missing”,”code”:401}’

Possible Causes:
:   - The value of the **x-google-issuer** field in the **securityDefinitions** field in the configuration file
      might not match the value of the **API\_GCP\_SERVICE\_ACCOUNT** for the API integration, as recorded in your tracking worksheet.
    - The value in **x-google-issuer** might contain extra whitespace.

Possible Solutions:
:   - Update the **x-google-issuer** to match the **API\_GCP\_SERVICE\_ACCOUNT**.
    - Remove unneeded whitespace.

### Error: Request fails with ’403 forbidden’

Possible Causes:
:   The service account using the config does not have the appropriate permissions on the backend.

Possible Solutions:
:   Update the service account’s permissions.
