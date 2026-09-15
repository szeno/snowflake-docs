# SYSTEM$CLASSIFY\_SCHEMA

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts that are Enterprise Edition (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Schedules the tables in the specified schema to be classified with the option to specify the number of rows to sample in each table and
assign the recommended sensitive data classification [system tag](/user-guide/classify-intro#label-classify-classification-tags) to each column in the tables
stored in the specified schema.

## Syntax

Copy code

```
SYSTEM$CLASSIFY_SCHEMA( '<schema_name>' , <object> )
```

## Arguments

`schema_name`
:   The name of the schema containing the tables to be classified. If a database and schema are not in use in the current session, the name
    must be fully-qualified.

    The name must be specified exactly as it is stored in the database. If the name contains special characters, capitalization, or blank
    spaces, the name must be enclosed first in double-quotes and then in single quotes.

`object`
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
> :   Enables [AI mode](/user-guide/classify-intro#label-classify-ai-mode) to use LLMs to identify additional semantic categories beyond those
>     identified by standard classification.
>
>     LLM usage is billed under the `AI_SENSITIVE_DATA_CLASSIFICATION` [service type](/sql-reference/service-types).
>
> `{'ai_mode': true, 'auto_tag': true}`
> :   Classify the specified object with AI mode enabled and set the recommended classification system tags on the columns when the
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

The stored procedure returns a JSON object in the following format. For example:

Copy code

```
{
  "failed": [
    {
      "message": "Insufficient privileges.",
      "table_name": "t4"
    }
  ],
  "succeeded": [
    {
      "table_name": "t1"
    },
    {
      "table_name": "t2"
    },
    {
      "table_name": "t3"
    }
  ]
}
```

Where:

`failed`
:   Specifies a message that provides a reason why the table was not scheduled to be classified.

`succeeded`
:   Specifies each table that is scheduled for Data Classification.

## Usage notes

- The specified schema name can contain up to 1000 table objects. If the schema contains more than 1000 table objects, Snowflake returns an
  error message.
- Snowflake-provided stored procedures utilize caller’s rights. For more details, see
  [Understanding caller’s rights and owner’s rights stored procedures](/developer-guide/stored-procedure/stored-procedures-rights).
- If you want to apply alternate system tag values, use an
  [ALTER TABLE … MODIFY COLUMN … SET TAG](/sql-reference/sql/alter-table-column) statement to update the tag value.
- To unset a Classification system tag from a column, use an ALTER TABLE … MODIFY COLUMN … UNSET TAG statement.

Caution

When you call this stored procedure, the classification process for each table in the schema runs in parallel and consumes warehouse
resources. If you call this stored procedure many times in a short period to classify tables in schemas simultaneously,
those processes also run in parallel. Many parallel classification processes can exceed the warehouse capability, which causes the
classification process for some tables to fail. Consequently, a schema might have some of its tables classified and others not classified.

Prior to calling SYSTEM$CLASSIFY\_SCHEMA, evaluate the number of columns in each table, the number of tables in a schema, the number of
schemas that you want to classify, and the warehouse size that is in use for the session.

## Examples

Stage the classification of tables in the schema:

> Copy code
>
> ```
> CALL SYSTEM$CLASSIFY_SCHEMA('hr.tables', null);
> ```

Stage the classification of the tables in the schema and specify the number of rows to sample:

> Copy code
>
> ```
> CALL SYSTEM$CLASSIFY_SCHEMA('hr.tables', {'sample_count': 1000});
> ```

Stage the classification of the tables in the schema and set the system tags to the columns:

> Copy code
>
> ```
> CALL SYSTEM$CLASSIFY_SCHEMA('hr.tables', {'auto_tag': true});
> ```

Stage the classification of the tables in the schema, specify the number of rows to sample, and set the recommended system tag to each
column in the table:

> Copy code
>
> ```
> CALL SYSTEM$CLASSIFY_SCHEMA('hr.tables', {'sample_count': 1000, 'auto_tag': true});
> ```
