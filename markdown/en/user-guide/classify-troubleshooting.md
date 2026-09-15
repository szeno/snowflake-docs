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

In general, there is a delay before Snowflake tries to classify the object again. Every additional failed attempt is logged to the event
table. This delay and retry process continues until the object is fixed or removed from automatic classification.

Note

To help avoid unnecessary costs, Snowflake waits additional time to retry classification for some errors, such as timeouts. For these
timeout errors, Snowflake doesn’t retry classification until all objects are reclassified; the schedule on which objects are reclassified
is controlled by the `maximum_classification_validity_days` key of the classification profile.

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

## Tag-related error messages

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
