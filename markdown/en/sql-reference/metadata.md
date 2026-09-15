# Metadata fields in Snowflake

The data contained in metadata fields may be processed outside of your Snowflake Region. It is your responsibility to ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered into any metadata field when using the Snowflake Service.

When creating an object in Snowflake, metadata fields may be captured. The most common metadata fields are:

- Object definitions, such as a policy, an external function, or a view definition.
- Object properties, such as an object name or an object comment.
- Listing and profile fields, such as listing and organization descriptions.

Attention

For objects defined through SQL, metadata fields are usually populated by any fields entered as part of [CREATE <object>](/sql-reference/sql/create),
and [ALTER <object>](/sql-reference/sql/alter), or method call statements for a given object. Creating or manipulating objects in other languages,
such as Python, may also populate metadata fields based on the object’s definitions and properties.

When using these commands, ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other
regulated data populates any metadata fields.

In addition to the above fields, the following table sets forth additional potential metadata fields in the Snowflake Service. Metadata is
“Usage Data” as defined in our [Terms of Service](https://www.snowflake.com/legal/terms-of-service/) or other agreement between you and
Snowflake covering use of the Snowflake Service.

Snowflake updates this table regularly as new features and services are added. If you have questions about how Snowflake tracks data or
about sensitive information in the actual query text please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

|  |  |  |
| --- | --- | --- |
| Additional Metadata | Query literals | [Query Data in Snowflake](/guides-overview-queries)  [QUERY\_HISTORY view](/sql-reference/account-usage/query_history) |
|  | Manifests | [Snowflake Native App manifest file](/developer-guide/native-apps/manifest-overview)  [Listing manifest reference](/progaccess/listing-manifest-reference) |
|  | Snowpark Container Services specification file | [Service specification reference](/developer-guide/snowpark-container-services/specification-reference) |
|  | Listing information, manifest file, and profiles | [Listing fields](/collaboration/provider-listings-reference)  [Listing manifest reference](/progaccess/listing-manifest-reference)  [Provider profile fields](/collaboration/provider-profiles-managing#label-configuring-metadata-for-provider-profile) |
|  | Custom instructions for Snowflake Copilot | [Using Snowflake Copilot](/user-guide/snowflake-copilot) |
|  | Generic error messages from ML functions | [ML Functions](/guides-overview-ml-functions) |
|  | Semantic models and semantic views | [Cortex Analyst semantic models](/user-guide/views-semantic/sql)  [Semantic views](/user-guide/views-semantic/overview) |
|  | Experiment run parameters, metrics, and artifacts | [Snowflake Experiments](/developer-guide/snowflake-ml/experiments) |

Expand

Show lessSee more
