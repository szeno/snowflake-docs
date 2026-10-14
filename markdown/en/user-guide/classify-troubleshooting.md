# Troubleshooting sensitive data classification

[Enterprise Edition Feature](/user-guide/intro-editions)

Sensitive data classification requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## View classification errors in the Trust Center

You can see which objects failed classification and read the error message for each object in the Snowsight without using SQL.
Complete the following steps:

1. In the navigation menu, select **Governance & security** » **Trust Center**.
2. Select the **Data Security** tab.
3. Select the **Dashboard** tab.
4. Select the **Classification errors** tile.

For the full workflow, see [Classification errors](/user-guide/classify-ui-trust-center#label-classify-trust-center-classification-errors) in [Use the Trust Center to set up sensitive data classification](/user-guide/classify-ui-trust-center).

## Why a table might not be classified, and how to find errors

A table might not get classified for several reasons. The simplest check is whether Snowflake can query the table: run a query against it
(for example, `SELECT * FROM my_table`). If a table can’t be queried, it can’t be classified.

Other failures can include tagging or privilege issues, data format problems, or restrictions on secure objects or certain views. When
classification fails, you can find details in these places:

- **Trust Center**: Use the **Classification errors** tile as described in [View classification errors in the Trust Center](#label-classify-troubleshooting-trust-center-errors).
- **Event table**: Snowflake logs an event to an
  [event table](/developer-guide/logging-tracing/event-table-setting-up). By default, the event is logged to the account-level event
  table. If you have an event table defined for the failed object’s database, then the event is logged there instead.
- **SQL**: Query the event table with the examples in [Listing general errors](#label-classify-troubleshooting-listing-general) and
  [Listing object-level classification errors](#label-classify-troubleshooting-listing-object). For known tag-related failure codes, see
  [Tag-related error messages](#label-classify-troubleshooting-error-message-examples).
- **Account Usage**: Query the `ERROR_MESSAGE` column of the
  [DATA\_CLASSIFICATION\_LATEST view](/sql-reference/account-usage/data_classification_latest) for the most recent error per table.

Note

By default, retryable classification failures are logged to the event table after three consecutive failed attempts. The
[DATA\_CLASSIFICATION\_LATEST view](/sql-reference/account-usage/data_classification_latest) also reports errors after three consecutive failures, except for timeouts,
which appear after the first failure. Non-retryable failures, such as timeouts, are logged to the event table on their first occurrence.

## How Snowflake retries a failed object

Snowflake retries automatic classification on its standard schedule until an object fails three consecutive times. After three
failures, Snowflake reduces the retry frequency to no more than once every 22 hours to prevent continuous retries on persistent errors.
Subsequent failed attempts are logged to the event table when logging is enabled.

Note

Non-retryable failures, such as timeouts, don’t follow the 22-hour interval. To help avoid unnecessary costs, Snowflake retries these
objects only after the interval set by `maximum_classification_validity_days` in the classification profile has elapsed since the last
failure.

If you want to prevent classification events from being logged, set the [ENABLE\_AUTOMATIC\_SENSITIVE\_DATA\_CLASSIFICATION\_LOG](/sql-reference/parameters#label-enable-automatic-sensitive-data-classification-log) account
parameter to FALSE.

## Listing general errors

The following query returns general errors related to sensitive data classification from the event table:

Copy code

```
SELECT
  record_type,
  record:severity_text::string log_level,
  parse_json(value) error_message
  FROM <event_db>.<event_schema>.<event_table>
  WHERE record_type='LOG' and scope:name ='snow.automatic_sensitive_data_classification'
  ORDER BY log_level;
```

For a subset of the possible error messages returned by this query, see [Tag-related error messages](#label-classify-troubleshooting-error-message-examples).

## Listing object-level classification errors

The following query against the event table returns errors related to the classification of a specific object. For example, it returns
errors that occurred when Snowflake tried to classify a specific table.

Copy code

```
SELECT
  RECORD_ATTRIBUTES:"object_name"::string AS object_name,
  parse_json(value):"error_message" error_message,
  PARSE_JSON(VALUE):"profile_name" classification_profile_name,
  timestamp,
  FROM <event_db>.<event_schema>.<event_table>
  WHERE record_type='LOG'
    AND scope:name ='snow.automatic_sensitive_data_classification'
    AND RECORD_ATTRIBUTES:"event_type" = 'CLASSIFICATION_ERROR'
  ORDER BY TIMESTAMP DESC;
```

Important

Always filter on the `event_type` attribute, as this example does, rather than on the presence of the `error_message` payload key.
Classification emits two unrelated event types, and both of them use an `error_message` key:

- `CLASSIFICATION_ERROR` for classification failures. The payload is one of the messages described in
  [Classification error messages](#label-classify-troubleshooting-classification-error-messages).
- `TAGGING_ERROR` for failures applying user-defined tags. The payload is structured JSON, not one of those messages. For details, see
  [Tag-related error messages](#label-classify-troubleshooting-error-message-examples).

For example, the following query returns only `TAGGING_ERROR` events:

Copy code

```
SELECT
  RECORD_ATTRIBUTES:"object_name"::string AS object_name,
  PARSE_JSON(VALUE):"error_message" AS error_message,
  timestamp
  FROM <event_db>.<event_schema>.<event_table>
  WHERE record_type = 'LOG'
    AND scope:name = 'snow.automatic_sensitive_data_classification'
    AND RECORD_ATTRIBUTES:"event_type" = 'TAGGING_ERROR'
  ORDER BY timestamp DESC;
```

## Classification error messages

Classification error details appear in `CLASSIFICATION_ERROR` events and in the `ERROR_MESSAGE` column of the
[DATA\_CLASSIFICATION\_LATEST](/sql-reference/account-usage/data_classification_latest) view. The messages available in the event table can
differ from those in the view.

Each message includes its originating Snowflake error code in parentheses when the code is available. For example,
`Failed to classify due to timeout while reading the data (000630).` Because this standard error code provides the most specific details about the issue, review it before taking
corrective action.

For descriptions and causes of specific error messages, see
[Data Classification Latest Error Messages](/sql-reference/account-usage/data_classification_latest#label-data-classification-latest-error-messages) in the
[DATA\_CLASSIFICATION\_LATEST](/sql-reference/account-usage/data_classification_latest) documentation.

The following table lists solutions for messages reported by both the view and the event table:

| Message | Solution |
| --- | --- |
| `Failed to classify the view due to a SQL compilation error` | Repair the view definition, then recreate the view. |
| `Failed to classify due to data format issues` | Correct the offending values, or cast them to a valid type. |
| `Failed to classify the secure object` | Check the appended error code for the cause. Commonly, the secure view references an object that was dropped. |
| `Failed to classify the external table as it was marked invalid` | Refresh or recreate the external table. |
| `Failed to classify 'Iceberg External Table' as it has been deprecated` | Migrate the table to [Apache Iceberg™ tables](/user-guide/tables-iceberg). |
| `Failed to classify as the data in the table was inaccessible` | Repair the storage integration, the stage, or the cloud IAM role that Snowflake uses to read the data. |
| `Failed to classify as one or more column(s) are mapped to multiple masking policies` | Resolve the conflict so that each column maps to a single masking policy. |
| `Failed to classify due to timeout while reading the data` | You can’t fix this error yourself. Contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support). |
| `Failed to classify` | Check the appended error code and the event table for details. If you can’t resolve the error, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) with the error code. |

Expand

Show lessSee more

The event table can also report `Failed to classify due to an invalid custom classifier configuration`. This message indicates an
invalid regular expression, a missing category, or an invalid score in a custom classifier. Correct the custom classifier configuration.
The `DATA_CLASSIFICATION_LATEST` view can instead report this failure as `Failed to classify`.

## Tag-related error messages

Snowflake emits `TAGGING_ERROR` events when it can’t apply user-defined tags to a classified column. Unlike
[Classification Error Messages](#label-classify-troubleshooting-classification-error-messages), `TAGGING_ERROR` payloads are structured
JSON.

|  |  |
| --- | --- |
| Error | ``` "failure_reason":"NO_TAGGING_PRIVILEGE" ``` |
| Cause | The role that was used for sensitive data classification does not have the correct privileges to set tags. |
| Solution | Grant the necessary privileges to the role used for sensitive data classification. For more information, see [Tag privileges](/user-guide/object-tagging/work#label-object-tags-privileges). |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Error | ``` "failure_reason":"MANUALLY_APPLIED_VALUE_PRESENT" ``` |
| Cause | Another tag is manually set on the column. |
| Solution | Determine whether you want to keep the tag that was manually set on the column. If not, unset the tag before classifying the table using automatic classification or the SYSTEM$CLASSIFY stored procedure. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Error | ``` "failure_reason":"TAG_NOT_ACCESSIBLE_OR_AUTHORIZED" ``` |
| Cause | The role that was used for classification cannot access the tag. |
| Solution | - If the tag does not exist, create the tag. - If the tag exists, grant privileges on the tag, or the database and schema that contains the tag, to the role that was used to   classify the database or schema. |

Expand

Show lessSee more

For more information about event table messages, see [Viewing log messages](/developer-guide/logging-tracing/logging-accessing-messages).
