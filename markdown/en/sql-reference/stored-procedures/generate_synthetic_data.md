# GENERATE\_SYNTHETIC\_DATA

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

The procedure generates synthetic data from one or more tables, based on data from input tables, and returns a table that contains metrics
about the generated data, such as the coefficient of difference (similarity) between the source data and the generated data.

This stored procedure uses the [caller’s rights](/developer-guide/stored-procedure/stored-procedures-rights) to generate the output table.

Read the [requirements](/user-guide/synthetic-data#label-synthetic-data-requirements) for running this procedure. If any requirements are not met, the request
will fail before it starts generating data.

[Learn more about synthetic data usage](/user-guide/synthetic-data).

## Syntax

Copy code

```
SNOWFLAKE.DATA_PRIVACY.GENERATE_SYNTHETIC_DATA(<configuration_object>)
```

## Arguments

`configuration_object`
:   An [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) that specifies the details of the request. You can use an
    [OBJECT constant](/sql-reference/data-types-semistructured#label-object-constant) to specify this object.

    The OBJECT value has the following structure:

    Copy code

    ```
    {
      'datasets': [
        {
          'input_table': '<input_table_name>',
          'output_table' : '<output_table_name>',
          'columns': {
            '<column_name>': {
              <property_name>: <property_value>
            }
            , ...
          }
        }
        , ...
      ],
      'similarity_filter': <boolean>,
      'replace_output_tables': <boolean>,
      'consistency_secret': <session_scoped_reference_string>
    }
    ```

    The OBJECT value contains the following key-value pairs:

    `datasets`
    :   An [array](/sql-reference/data-types-semistructured#label-data-type-array) specifying the data to generate. Each element in the array is an OBJECT
        value that defines a single input-output table pair. You can specify a maximum of five table pairs.

        A child OBJECT value representing a single input-output table pair has the following properties:

        `input_table`
        :   The fully-qualified name of the input table from which to generate synthetic data.
            If the table does not exist or cannot be accessed, Snowflake returns an error message. See
            [Using synthetic data in Snowflake](/user-guide/synthetic-data) for more input table requirements.

            If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
            Identifiers enclosed in double quotes are also case-sensitive.

            For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

        `output_table`
        :   The fully-qualified name of the output table to store the synthetic data generated from `input_table`. The generated table will
            have the same permissions and policies as if the user had called CREATE TABLE with default values. If the table already exists and
            `replace_output_tables=TRUE`, the existing table will be overwritten.

            In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
            entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
            case-sensitive.

            For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

        `columns`
        :   (*Optional*) An OBJECT value specifying additional properties for specific columns. Each field in the OBJECT defines
            properties for a single column. You do not need to define properties for all columns, or any columns at all. For each
            field:

            - The key is the column name. Properties in the value should be applied to this column.
            - The value is an OBJECT value containing any of the following key-value pairs:
              - `join_key`: BOOLEAN, where TRUE indicates that this is a join key column. This cannot be used in a column labeled
                `categorical`. Column must be a string, numeric, or Boolean value. [Learn about join keys.](/user-guide/synthetic-data#label-sdg-join-keys)

                Default: FALSE.
              - `categorical`: BOOLEAN, used to specify whether the column is a categorical string. Set to TRUE to enable the output to
                mark the data as non-sensitive, and able to be used in the output. Set to FALSE to redact values from the output.
                If not specified, will be determined by examining the data. Can be specified only for STRING columns. If set to TRUE, you cannot
                specify the `replace` or `join_key` fields for this column

                Default: Inferred based on the column data.
              - `replace`: Specifies an output format for **STRING** values. Can be used only on categorical string columns. The only values
                that can be used with `join_key` columns are `uuid` and `email`. Cannot be used when `categorical` is TRUE. If specified,
                you must provide a value for `consistency_secret`. The following values are supported:

                **`replace` values**

                | Value | Description |
                | --- | --- |
                | `uuid` | A UUID. Example: `88d99a35-c4be-4022-b06a-41fb4629b46d` |
                | `name` | A first and last name in US locale style. Example: `George Washington` |
                | `first_name` | A first name in US locale style. Example: `George` |
                | `last_name` | A last name in US locale style. Example: `Washington` |
                | `address` | An abbreviated address in US locale style. Example: `1600 Pennsylvania Ave` |
                | `full_address` | A detailed street address in US locale style. Example: `1600 Pennsylvania Ave NW, Washington DC 20500` |
                | `email` | An email address. Example: `bdbQ6OPBS5ScOdJx8bVpFw@example.com` |
                | `phone` | A US-style 10-digit phone number in US locale style. Example: `212-555-1234` |
                | `ssn` | A US-style Social Security number. Example: `123-45-6789` |

                Expand

                Show lessSee more

                Default:

                - For `join_key` columns, `uuid`
                - For non-join-key columns, the value will be redacted.

    `similarity_filter`
    :   (Optional) Specifies whether to use a similarity filter when creating the synthetic data. Set this to TRUE to use the built-in privacy
        filter to remove rows from the target table that are too similar to rows in the input table. If FALSE, each output table will have the
        same number of rows as its input table; if TRUE, an output table might have fewer rows than its input table. If TRUE, synthetic data
        generation will fail if you have NULL values in any non-string columns.

        Default: FALSE

        For more information, see [Enhancing privacy](/user-guide/synthetic-data#label-sdg-privacy-filter).

    `replace_output_tables`
    :   (*Optional*) Specifies whether to overwrite the output synthetic data table when creating the synthetic data. Set this to TRUE to
        overwrite the output table.

        Default: FALSE

    `consistency_secret`
    :   Session-scoped reference STRING for a [symmetric key SECRET](/sql-reference/sql/create-secret#label-symmetric-secret). Required if either of the following
        conditions are met, (otherwise you can omit this field):

        - If you want consistency for join keys across multiple runs.
        - If `columns.replace` or `columns.join_key = TRUE` are specified on any column, and this procedure is run in an
          [owner’s rights stored procedure](/developer-guide/stored-procedure/stored-procedures-rights).

        If you provide a secret, the procedure generates consistent values for STRING join keys across multiple runs that reuse the same
        consistency secret. If you provide a secret, you must have the READ or OWNERSHIP privilege on this secret.

        If you don’t provide a secret, join keys are consistent between tables in the same run, but not across multiple runs.
        [Learn more about consistency.](/user-guide/synthetic-data#label-sdg-key-consistency)

        Default: No consistency

## Output

| Column Name | Data Type | Description |
| --- | --- | --- |
| `created_on` | TIMESTAMP | Time the synthetic data was generated. |
| `table_name` | VARCHAR | Name of the synthetic table. |
| `table_schema` | VARCHAR | Schema name of the synthetic table. |
| `table_database` | VARCHAR | Database name of the synthetic table. |
| `columns` | VARCHAR | A pair of columns in the synthetic table. |
| `source_table_id` | NUMBER | Internal/system-generated identifier of the input table. |
| `source_table_name` | VARCHAR | Name of the input table. |
| `source_table_schema` | VARCHAR | Schema name of the input table. |
| `source_table_database` | VARCHAR | Database name of the input table. |
| `source_columns` | VARCHAR | Names of the source columns. |
| `metric_type` | ENUM | `correlation_coefficient_difference` - Calculated as the absolute value of the correlation coefficient between two non-join columns in the source table and the same two columns in the generated data.  Currently, `correlation_coefficient_difference` is the only supported metric. This is the difference between the correlation coefficient of every combination of columns in the input table and the same coefficient in the generated data. Each row represents the correlation coefficient difference between one combination of columns. The column name pair is found in these columns: `columns` and `source_columns`. |
| `metric_value` | NUMBER | Value of the metric. |

Expand

Show lessSee more

## Access control requirements

To generate synthetic data, you must use a role with each the following grants:

- USAGE on the warehouse that you want to use for queries.
- SELECT on the input table from which you want to generate synthetic data.
- USAGE on the database and schema that contain the input table, and on the database that contains the output table.
- CREATE TABLE on the schema that contains the output table.
- OWNERSHIP on the output tables. The simplest way to do this is by granting OWNERSHIP to the schema where the output table is
  generated. (However, if someone has applied a FUTURE GRANT on this schema, table ownership will be silently overridden – that is,
  `GRANT OWNERSHIP ON FUTURE TABLES IN SCHEMA db.my_schema TO ROLE some_role` will automatically grant OWNERSHIP to `some_role` on any
  new tables created in schema `my_schema`.)

All users can access the SNOWFLAKE.DATA\_PRIVACY.GENERATE\_SYNTHETIC\_DATA stored procedure. Access is made available using the
SNOWFLAKE.CORE\_VIEWER database role, which is granted to the PUBLIC role.

## Usage notes

- The JSON key values must be lowercase.
- You must [accept the Anaconda terms and conditions](/developer-guide/udf/python/udf-python-packages#label-accept-anaconda-terms) in your Snowflake account in order to enable this
  feature.
- For additional requirements, see [Requirements](/user-guide/synthetic-data#label-synthetic-data-requirements).
- Any timestamps earlier than `1677-09-21 00:12:43.145224193` or later than `2262-04-11 23:47:16.854775807` in the source data are
  coerced to `1677-09-21 00:12:43.145224193` or `2262-04-11 23:47:16.854775807` respectively when generating synthetic data.

## Examples

This example generates synthetic data from an input table containing medical information (blood type, gender, age, and ethnicity). The
response shows the closeness in data between the source and generated tables. The generated synthetic data table is not shown.

**Two columns designated as join keys**

Copy code

```
CALL SNOWFLAKE.DATA_PRIVACY.GENERATE_SYNTHETIC_DATA({
    'datasets':[
        {
          'input_table': 'syndata_db.sch.faker_source_t',
          'output_table': 'syndata_db.sch.faker_synthetic_t',
          'columns': { 'blood_type': {'join_key': TRUE} , 'ethnicity': {'join_key': TRUE}}
        }
      ]
  });
```

**No columns designated as join keys**

Copy code

```
CALL SNOWFLAKE.DATA_PRIVACY.GENERATE_SYNTHETIC_DATA({
  'datasets':[
      {
        'input_table': 'syndata_db.sch.faker_source_t',
        'output_table': 'syndata_db.sch.faker_synthetic_t'
      }
    ]
});
```

**Use consistency key to generate consistent values across multiple runs**

Copy code

```
CREATE OR REPLACE SECRET my_db.public.my_consistency_secret
  TYPE = SYMMETRIC_KEY
  ALGORITHM = GENERIC;

CALL SNOWFLAKE.DATA_PRIVACY.GENERATE_SYNTHETIC_DATA({
  'datasets':[
      {
        'input_table': 'CLINICAL_DB.PUBLIC.BASE_TABLE',
        'output_table': 'my_db.public.test_syndata',
        'columns': { 'patient_id': {'join_key': TRUE, 'replace': 'uuid'}}
      }
    ],
    'consistency_secret': SYSTEM$REFERENCE('SECRET', 'MY_CONSISTENCY_SECRET', 'SESSION', 'READ')::STRING,
    'replace_output_tables': TRUE
});
```

**Output from calling the function**

```
+---------------------------+-------------------+--------------+----------------+------------------------+-------------------+---------------------+-----------------------+------------------------+------------------------------------+----------------+
| CREATED_ON                | TABLE_NAME        | TABLE_SCHEMA | TABLE_DATABASE | COLUMNS                | SOURCE_TABLE_NAME | SOURCE_TABLE_SCHEMA | SOURCE_TABLE_DATABASE | SOURCE_COLUMNS         | METRIC_TYPE                        | METRIC_VALUE   |
+---------------------------+-------------------+--------------+----------------+------------------------+-------------------+---------------------+-----------------------+------------------------+------------------------------------+----------------+
| 2024-07-30 09:53:28.439 Z | faker_synthetic_t | sch          | syndata_db     | "BLOOD_TYPE,GENDER"    | faker_source_t    | sch                 | syndata_db            | "BLOOD_TYPE,GENDER"    | CORRELATION_COEFFICIENT_DIFFERENCE | 0.02430214616  |
| 2024-07-30 09:53:28.439 Z | faker_synthetic_t | sch          | syndata_db     | "BLOOD_TYPE,AGE"       | faker_source_t    | sch                 | syndata_db            | "BLOOD_TYPE,AGE"       | CORRELATION_COEFFICIENT_DIFFERENCE | 0.001919343586 |
| 2024-07-30 09:53:28.439 Z | faker_synthetic_t | sch          | syndata_db     | "BLOOD_TYPE,ETHNICITY" | faker_source_t    | sch                 | syndata_db            | "BLOOD_TYPE,ETHNICITY" | CORRELATION_COEFFICIENT_DIFFERENCE | 0.003720197046 |
| 2024-07-30 09:53:28.439 Z | faker_synthetic_t | sch          | syndata_db     | "GENDER,AGE"           | faker_source_t    | sch                 | syndata_db            | "GENDER,AGE"           | CORRELATION_COEFFICIENT_DIFFERENCE | 0.004348586645 |
| 2024-07-30 09:53:28.439 Z | faker_synthetic_t | sch          | syndata_db     | "GENDER,ETHNICITY"     | faker_source_t    | sch                 | syndata_db            | "GENDER,ETHNICITY"     | CORRELATION_COEFFICIENT_DIFFERENCE | 0.001171535243 |
| 2024-07-30 09:53:28.439 Z | faker_synthetic_t | sch          | syndata_db     | "AGE,ETHNICITY"        | faker_source_t    | sch                 | syndata_db            | "AGE,ETHNICITY"        | CORRELATION_COEFFICIENT_DIFFERENCE | 0.004265938158 |
+---------------------------+-------------------+--------------+----------------+------------------------+-------------------+---------------------+-----------------------+------------------------+------------------------------------+----------------+
```
