Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$CLIENT\_VERSION\_INFO

Returns version information for Snowflake clients and drivers.

See also:
:   [Client versions & support policy](/release-notes/requirements)

## Syntax

Copy code

```
SYSTEM$CLIENT_VERSION_INFO()
```

## Arguments

None

## Returns

Return a string containing a JSON array of objects. Each object contains information about a specific client and driver, such as SnowSQL, the JDBC driver, and so on.

Each JSON object contains the following name/value pairs:

Copy code

```
{
  "clientId": "DOTNETDriver",
  "clientAppId": ".NET",
  "minimumSupportedVersion": "2.0.9",
  "minimumNearingEndOfSupportVersion": "2.0.11",
  "recommendedVersion": "2.1.5",
  "deprecatedVersions": [],
  "_customSupportedVersions_": []
},
```

Where:

> `clientId`
> :   Internal ID of the client or driver. Possible values include:
>
>     - `DOTNETDriver`
>     - `GO`
>     - `JDBC`
>     - `JSDriver`
>     - `ODBC`
>     - `PHP_PDO`
>     - `PythonConnector`
>     - `SnowSQL`
>     - `SQLAPI`
>
> `clientAppId`
> :   Name of the client or driver. Possible values include:
>
>     - `.NET`
>     - `GO`
>     - `JDBC`
>     - `JavaScript`
>     - `ODBC`
>     - `PDO`
>     - `PythonConnector`
>     - `SnowSQL`
>     - `SQLAPI`
>
> `minimumSupportedVersion`
> :   Oldest version of the client or driver officially supported.
>
> `minimumNearingEndOfSupportVersion`
> :   Version of the client or driver that reaches end-of-support (EOS) at the start of the next quarter.
>
> `recommendedVersion`
> :   Current version of the client or driver.
>
> `deprecatedVersions`, `_customSupportedVersions_`
> :   Internal use only.

## Usage notes

- If you prefer not to process JSON, you can use the [PARSE\_JSON](/sql-reference/functions/parse_json) and [LATERAL FLATTEN](/user-guide/lateral-join-using#label-lateral-flatten-example) function to convert the JSON to columnar output.
- You can also use the WHERE clause to return the information for a specific client or driver (`clientId`).

## Examples

The following example retrieves the version information for all Snowflake clients and drivers. Note that the output has been manually formatted for better readability.

Copy code

```
SELECT SYSTEM$CLIENT_VERSION_INFO();
```

```
[
  {
    "clientId": "DOTNETDriver",
    "clientAppId": ".NET",
    "minimumSupportedVersion": "2.0.9",
    "minimumNearingEndOfSupportVersion": "2.0.11",
    "recommendedVersion": "2.1.5",
    "deprecatedVersions": [],
    "_customSupportedVersions_": []
  },
  {
    "clientId": "GO",
    "clientAppId": "Go",
    "minimumSupportedVersion": "1.6.6",
    "minimumNearingEndOfSupportVersion": "1.6.9",
    "recommendedVersion": "1.7.1",
    "deprecatedVersions": [],
    "_customSupportedVersions_": [
      "1.1.5"
    ]
  },
  {
    "clientId": "JDBC",
    "clientAppId": "JDBC",
    "minimumSupportedVersion": "3.13.14",
    "minimumNearingEndOfSupportVersion": "3.13.18",
    "recommendedVersion": "3.14.4",
    "deprecatedVersions": [],
    "_customSupportedVersions_": []
  },
  {
    "clientId": "JSDriver",
    "clientAppId": "JavaScript",
    "minimumSupportedVersion": "1.6.6",
    "minimumNearingEndOfSupportVersion": "1.6.9",
    "recommendedVersion": "1.9.2",
    "deprecatedVersions": [],
    "_customSupportedVersions_": []
  },
  {
    "clientId": "ODBC",
    "clientAppId": "ODBC",
    "minimumSupportedVersion": "2.24.5",
    "minimumNearingEndOfSupportVersion": "2.24.7",
    "recommendedVersion": "3.1.4",
    "deprecatedVersions": [],
    "_customSupportedVersions_": []
  },
  {
    "clientId": "PHP_PDO",
    "clientAppId": "PDO",
    "minimumSupportedVersion": "1.2.0",
    "minimumNearingEndOfSupportVersion": "1.2.1",
    "recommendedVersion": "2.0.1",
    "deprecatedVersions": [],
    "_customSupportedVersions_": []
  },
  {
    "clientId": "PythonConnector",
    "clientAppId": "PythonConnector",
    "minimumSupportedVersion": "2.7.3",
    "minimumNearingEndOfSupportVersion": "2.7.7",
    "recommendedVersion": "3.6.0",
    "deprecatedVersions": [],
    "_customSupportedVersions_": []
  },
  {
    "clientId": "SnowSQL",
    "clientAppId": "SnowSQL",
    "minimumSupportedVersion": "1.2.21",
    "minimumNearingEndOfSupportVersion": "1.2.21",
    "recommendedVersion": "1.2.31",
    "deprecatedVersions": [],
    "_customSupportedVersions_": []
  },
  {
    "clientId": "SQLAPI",
    "clientAppId": "SQLAPI",
    "minimumSupportedVersion": "1.0.0",
    "minimumNearingEndOfSupportVersion": "",
    "recommendedVersion": "",
    "deprecatedVersions": [],
    "_customSupportedVersions_": []
  }
]
```

The following example returns the version information for all clients as a rowset:

Copy code

```
WITH output AS (
  SELECT
    PARSE_JSON(SYSTEM$CLIENT_VERSION_INFO()) a
)
SELECT
    value:clientAppId::STRING AS client_app_id,
    value:minimumSupportedVersion::STRING AS minimum_version,
    value:minimumNearingEndOfSupportVersion::STRING AS near_end_of_support_version,
    value:recommendedVersion::STRING AS recommended_version
  FROM output r,
    LATERAL FLATTEN(INPUT => r.a, MODE =>'array');
```

```
+-----------------+-----------------+-----------------------------+---------------------+
| CLIENT_APP_ID   | MINIMUM_VERSION | NEAR_END_OF_SUPPORT_VERSION | RECOMMENDED_VERSION |
|-----------------+-----------------+-----------------------------+---------------------|
| .NET            | 2.0.9           | 2.0.11                      | 2.1.5               |
| Go              | 1.6.6           | 1.6.9                       | 1.7.1               |
| JDBC            | 3.13.14         | 3.13.18                     | 3.14.4              |
| JavaScript      | 1.6.6           | 1.6.9                       | 1.9.2               |
| ODBC            | 2.23.5          | 2.24.7                      | 3.1.4               |
| PDO             | 1.2.0           | 1.2.1                       | 2.0.1               |
| PythonConnector | 2.7.3           | 2.7.7                       | 3.6.0               |
| SnowSQL         | 1.2.21          | 1.2.21                      | 1.2.31              |
| SQLAPI          | 1.0.0           |                             |                     |
+-----------------+-----------------+-----------------------------+---------------------+
```

The following example returns the version information for the JDBC driver as a rowset:

Copy code

```
WITH output AS (
  SELECT
    PARSE_JSON(SYSTEM$CLIENT_VERSION_INFO()) a
)
SELECT
    value:clientId::STRING AS client_id,
    value:minimumSupportedVersion::STRING AS minimum_version,
    value:minimumNearingEndOfSupportVersion::STRING AS near_end_of_support_version,
    value:recommendedVersion::STRING AS recommended_version
  FROM output r,
    LATERAL FLATTEN(INPUT => r.a, MODE =>'array')
  WHERE client_id = 'JDBC';
```

```
+-----------+-----------------+-----------------------------+---------------------+
| CLIENT_ID | MINIMUM_VERSION | NEAR_END_OF_SUPPORT_VERSION | RECOMMENDED_VERSION |
|-----------+-----------------+-----------------------------+---------------------|
| JDBC      | 3.13.14         | 3.13.18                     | 3.14.4              |
+-----------+-----------------+-----------------------------+---------------------+
```
