Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_CLASSIFICATION\_RESULT

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the classification result of the specified object.

## Syntax

Copy code

```
SELECT SYSTEM$GET_CLASSIFICATION_RESULT( '<object_name>' )
```

## Arguments

`object_name`
:   The name of the table, external table, view, or materialized view containing the columns to be classified. If a database and schema are
    not in use in the current session, the name must be fully-qualified.

    The name must be specified exactly as it is stored in the database. If the name contains special characters, capitalization, or blank
    spaces, the name must be enclosed first in double-quotes and then in single quotes.

## Returns

Returns a JSON object in the following format. For example:

Copy code

```
{
  "classification_profile_config": {
    "classification_profile_name": "db1.sch.sensitive_data_detection_profile"
  },
  "classification_result": {
    "col1_name": {
      "alternates": [],
      "recommendation": {
        "confidence": "HIGH",
        "coverage": 1,
        "details": [],
        "privacy_category": "QUASI_IDENTIFIER",
        "semantic_category": "DATE_OF_BIRTH",
        "tags": [
          {
            "tag_applied": true,
            "tag_name": "snowflake.core.semantic_category",
            "tag_value": "DATE_OF_BIRTH"
          },
          {
            "tag_applied": true,
            "tag_name": "snowflake.core.privacy_category",
            "tag_value": "QUASI_IDENTIFIER"
          }
        ]
      },
      "valid_value_ratio": 1
    }
  }
}
```

**Possible fields**:

`classification_profile_config`
:   If automatic classification is configured, contains the fully qualified name of the configuration profile that was used to generate the
    classification results.

`classification_result`
:   Provides details about each column that was classified.

`object_path_results`
:   When a column contains semi-structured data with sensitive fields, the `object_path_results` key lists the fields that were
    classified into a native or custom semantic category. For more information, see [View classification results for JSON columns](/user-guide/classify-results#label-classify-results-json).

`alternates`
:   Provides information about each tag and value to consider other than the recommended tag.

`recommendation`
:   Provides information about each tag and value as the primary choice based on the classification process.

These values can appear in both the alternates and recommendation:

> `classifier_name`
> :   The fully-qualified name of the custom classification instance that was used to tag the classified column.
>
>     This field only appears when using a custom classification instance as the source of the tag to set on a column.
>
> `confidence`
> :   Provides one of the following values: `HIGH`, `MEDIUM`, or `LOW`. This value indicates the relative confidence that Snowflake
>     has based upon the column sampling process and how the column data aligns with how Snowflake classifies data.
>
> `coverage`
> :   Provides the percent of sampled cell values that match the rules for a particular category.
>
> `details`
> :   Provides fields and values related to geography-specific classification. The `semantic_category` field contains the
>     [semantic subcategory](/user-guide/classify-native#label-classify-native-subcategories) for a locale.
>
> `privacy_category`
> :   Provides the privacy category.
>
>     The possible values are `IDENTIFIER`, `QUASI-IDENTIFIER` and `SENSITIVE`.
>
> `semantic_category`
> :   Provides the semantic category. For a list of native semantic categories, see [Native semantic categories of sensitive data classification](/user-guide/classify-native).
>
>     If the value is `MULTIPLE`, then sensitive data was found in semi-structured data. Inspect the `object_path_results` field
>     of the results object for a detailed breakdown of which native and custom semantic categories were found during classification. For more information, see [View classification results for JSON columns](/user-guide/classify-results#label-classify-results-json).
>
> `tags`
> :   Provides information about the tags that were applied to the column as a result of the classification process.
>
> `valid_value_ratio`
> :   Provides the ratio of how many values in the sample size are valid.
>
>     - For structured data, invalid values include NULL, an empty string, and a string with more than 256 characters.
>     - For semi-structured data, invalid values include NULL and an empty string.

## Examples

Return the sensitive data classification result for a table:

> Copy code
>
> ```
> SELECT SYSTEM$GET_CLASSIFICATION_RESULT('hr.tables.empl_info');
> ```
