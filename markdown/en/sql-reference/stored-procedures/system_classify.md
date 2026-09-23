# SYSTEM$CLASSIFY

Classifies the specified object with the option to specify the number of rows to sample and assign the recommended
[classification tag](/user-guide/classify-intro#label-classify-classification-tags) to each column in the specified object.

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## Syntax

Copy code

```
SYSTEM$CLASSIFY( '<object_name>' ,
  { '<classification_profile>' | <options> } )
```

## Arguments

`'object_name'`
:   The name of the table, external table, view, or materialized view containing the columns to be classified. If a database and schema are
    not in use in the current session, the name must be fully-qualified.

    The name must be specified exactly as it is stored in the database. If the name contains special characters, capitalization, or blank
    spaces, the name must be enclosed first in double-quotes and then in single quotes.

`'classification_profile'`
:   Specifies a [classification profile](/user-guide/classify-auto#label-classification-auto-about-profile) in order to classify based on the criteria specified in the profile, including [AI mode](/user-guide/classify-intro#label-classify-ai-mode) when enabled on the profile.

`options`
> Specifies a JSON [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) that determines how the classification process works. One of the following:
>
> `NULL`
> :   Snowflake uses its default configuration based on the number of rows in the specified object. System tags are not set on any columns
>     in the specified object.
>
> `{}`
> :   An empty object, which is functionally equivalent to specifying `NULL`.
>
> `{'sample_count': integer}`
> :   Specifies the number of rows to sample in the specified object. Any number from `1` to `10000`, inclusive.
>
> `{'auto_tag': true}`
> :   Sets the recommended classification system tags on the columns in the specified object when the classification process is complete.
>
>     When you use this argument, call the stored procedure with the role that has the OWNERSHIP privilege on the schema.
>
> `{'sample_count': integer, 'auto_tag': true}`
> :   Classify the specified object while specifying the number of rows to sample and set the recommended system tag on each column in the
>     specified object when the classification process is complete.
>
>     When you use this argument, call the stored procedure with the role that has the OWNERSHIP privilege on the schema.
>
> `{'ai_mode': true}`
> :   [Preview Feature](/release-notes/preview-features) — Open
>
>     For details, see [AI mode](/user-guide/classify-intro#label-classify-ai-mode).
>
>     Enables [AI mode](/user-guide/classify-intro#label-classify-ai-mode) to use LLMs to identify additional semantic categories beyond those
>     identified by standard classification.
>
>     LLM usage is billed under the `AI_SENSITIVE_DATA_CLASSIFICATION` [service type](/sql-reference/service-types).
>
> `{'ai_mode': true, 'auto_tag': true}`
> :   [Preview Feature](/release-notes/preview-features) — Open
>
>     For details, see [AI mode](/user-guide/classify-intro#label-classify-ai-mode).
>
>     Classify the specified object with [AI mode](/user-guide/classify-intro#label-classify-ai-mode) enabled and set the recommended classification system tags on the columns when the
>     classification process is complete.
>
>     When you use this argument, call the stored procedure with the role that has the OWNERSHIP privilege on the schema.
>
> `{'use_all_custom_classifiers': true}`
> :   Snowflake evaluates all custom classification instances and recommends the tag associated with a custom classification instance based
>     on the classification result.
>
>     This option uses the custom classifiers that are accessible to the role in use that calls the stored procedure
>     (current role, caller’s rights). For information, see [Understanding caller’s rights and owner’s rights stored procedures](/developer-guide/stored-procedure/stored-procedures-rights).
>
> `{'custom_classifiers': ['instance_name1' [ , 'instance_name2' ... ] ]}`
> :   Specifies the custom classification instance to evaluate as a source for the recommended tag to be set on the column.
>
>     You can specify multiple instances in the list and separate each instance with a comma.

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

## Usage notes

- Snowflake-provided stored procedures utilize caller’s rights. For more details, see
  [Understanding caller’s rights and owner’s rights stored procedures](/developer-guide/stored-procedure/stored-procedures-rights).
- If you want to apply alternate system tag values, use an
  [ALTER TABLE … MODIFY COLUMN … SET TAG](/sql-reference/sql/alter-table-column) statement to update the tag value.
- To unset a Classification system tag from a column, use an ALTER TABLE … MODIFY COLUMN … UNSET TAG statement.
- To use [AI mode](/user-guide/classify-intro#label-classify-ai-mode), pass `'ai_mode': true` in the options object or specify a
  classification profile that has AI mode enabled. For limitations and billing details, see
  [Limitations and considerations](/user-guide/classify-intro#limitations-and-considerations) and
  [Cost considerations](/user-guide/classify-intro#label-classify-auto-cost).

## Examples

Classify a table:

> Copy code
>
> ```
> CALL SYSTEM$CLASSIFY('hr.tables.empl_info', null);
> ```

Classify a table and specify the number of rows to sample:

> Copy code
>
> ```
> CALL SYSTEM$CLASSIFY('hr.tables.empl_info', {'sample_count': 1000});
> ```

Classify a table and set the system tags to the columns:

> Copy code
>
> ```
> CALL SYSTEM$CLASSIFY('hr.tables.empl_info', {'auto_tag': true});
> ```

Classify a table, and specify the number of rows to sample and set the recommended system tag to each column in the table:

> Copy code
>
> ```
> CALL SYSTEM$CLASSIFY('hr.tables.empl_info', {'sample_count': 1000, 'auto_tag': true});
> ```

Classify a table based on the criteria specified in the `my_config_profile` classification profile:

> Copy code
>
> ```
> CALL SYSTEM$CLASSIFY('hr.tables.empl_info, 'my_config_profile');
> ```

Classify a table with [AI mode](/user-guide/classify-intro#label-classify-ai-mode) enabled:

> Copy code
>
> ```
> CALL SYSTEM$CLASSIFY('hr.tables.empl_info', {'ai_mode': true});
> ```

Classify a table with AI mode enabled and apply recommended system tags to columns:

> Copy code
>
> ```
> CALL SYSTEM$CLASSIFY('hr.tables.empl_info', {'ai_mode': true, 'auto_tag': true});
> ```
