# Using SQL to automatically generate object descriptions

The Cortex Powered Object Descriptions feature allows you to use the
[Snowflake Cortex COMPLETE function](/sql-reference/functions/complete-snowflake-cortex) to automatically generate descriptions for
tables, views, and columns. This feature leverages Snowflake-hosted large language models (LLMs) to evaluate object metadata and, if
desired, sample data to generate a description.

This topic describes how to use a stored procedure to generate descriptions programmatically. For
information about using Snowsight to generate the descriptions, see [Generate descriptions with Snowflake Cortex](/user-guide/ui-snowsight-cortex-descriptions).

## Generating a description

The [AI\_GENERATE\_TABLE\_DESC](/sql-reference/stored-procedures/ai_generate_table_desc) stored procedure automatically generates a description for a table or
view. It can also generate descriptions for the columns of that table or view.

The AI\_GENERATE\_TABLE\_DESC stored procedure accepts two arguments:

- The name of the table or view that you want to generate a description for.
- An optional configuration object that allows you to do the following:
  - Generate descriptions for the columns of the specified table or view.
  - Use sample data from the table or view to potentially improve the accuracy of the column descriptions.

Example: Generate a table description
:   Copy code

    ```
    CALL AI_GENERATE_TABLE_DESC( 'my_table');
    ```

Example: Generate table and column descriptions without using sample data
:   Copy code

    ```
    CALL AI_GENERATE_TABLE_DESC(
      'mydb.sch1.hr_data',
      {
        'describe_columns': true,
        'use_table_data': false
      });
    ```

Example: Generate view and column descriptions using sample data to improve accuracy
:   Copy code

    ```
    CALL AI_GENERATE_TABLE_DESC(
      'mydb.sch1.v1',
      {
        'describe_columns': true,
        'use_table_data': true
      });
    ```

For the complete syntax of the stored procedure, see [AI\_GENERATE\_TABLE\_DESC](/sql-reference/stored-procedures/ai_generate_table_desc).

## Working with the response

The AI\_GENERATE\_TABLE\_DESC stored procedure returns a JSON object that contains the generated descriptions along with general
information about the table and columns. Within this object, the `description` field contains the generated description.

Suppose you created the following table:

Copy code

```
CREATE OR REPLACE TABLE mydb.sch1.hr_data (fname VARCHAR, age INTEGER);

INSERT INTO hr_data (fname, age)
    VALUES
        ('Thomas',    44),
        ('Katherine', 29),
        ('Lisa',      29);
```

Given this table, the following is an example of the JSON object returned by AI\_GENERATE\_TABLE\_DESC:

```
{
  "COLUMNS": [
    {
      "database_name": "mydb",
      "description": "The first name of the employee.",
      "name": "FNAME",
      "schema_name": "sch1",
      "table_name": "hr_data"
    },
    {
      "database_name": "mydb",
      "description": "A column holding data of type DecimalType representing age values.",
      "name": "AGE",
      "schema_name": "sch1",
      "table_name": "hr_data"
    }
  ],
  "TABLE": [
    {
      "database_name": "mydb",
      "description": " The table contains records of employee data, specifically demographic information. Each record includes an employee's age and name.",
      "name": "hr_data",
      "schema_name": "sch1"
    }
  ]
}
```

For more information about each JSON field, see [Returns](/sql-reference/stored-procedures/ai_generate_table_desc#label-ai-generate-table-desc-returns).

## Set generated descriptions as comments

To set a generated description as a comment on a table, view, or column, you must manually execute a SQL statement that includes the
SET COMMENT parameter. For example, to save a generated description for a table `t1`, execute
`ALTER TABLE t1 SET COMMENT = 'ai generated description';`.

You can write custom code to automatically generate and save descriptions. For examples of stored procedures that do this, see
[Examples](#label-sql-object-descriptions-example).

## Access control requirements

Users must have the following privileges and roles to call the AI\_GENERATE\_TABLE\_DESC stored procedure:

- SELECT privilege on the table or view.
- SNOWFLAKE.CORTEX\_USER database role.

## Availability of the feature

Your region must support the LLM used by Snowflake Cortex (like Mistral-7b and Llama 3.1-8b) to generate the descriptions. Check the
[availability of the COMPLETE function](/user-guide/snowflake-cortex/aisql-regional-availability#label-cortex-llm-availability). If the COMPLETE function is not supported in your region, you
must enable [cross-region inference](/user-guide/snowflake-cortex/cross-region-inference) to use the feature.

## Using sample data

When generating a description for a column, you can rely only on metadata, or you can choose to use sample data to
improve the Snowflake Cortex Powered Description. Sample data refers to data within a particular column that is evaluated when you
use Snowflake Cortex to generate descriptions. If you choose to use sample data, Snowflake uses a portion of the sample data to generate the
description, which leads to more accurate descriptions. Sample data is not stored by Snowflake as Usage Data.

## Cost considerations

Generating descriptions incurs the following costs:

- Credits consumed by the warehouse in use.
- Credits charged for the use of Snowflake Cortex with smaller LLMs like Mistral-7b and Llama 3.1-8b. These charges appear on a bill as
  AI-Services, which includes all uses of Snowflake Cortex.

## Limitations

You cannot generate column descriptions for objects with more than 5,000 columns.

## Legal Notices

This feature relies on the COMPLETE function to generate a recommended object description. When the user initiates the description
generation, Usage Data may be collected through the COMPLETE function.

The generated description is not retained by Snowflake until it is saved by the user.

For additional information about the use of AI, see [Snowflake AI and ML](/guides-overview-ai-features).

## Examples

The following examples create and call a stored procedure to generate object descriptions:

- [Example: Generate descriptions and set them as comments](#example-generate-descriptions-and-set-them-as-comments)
- [Example: Generate descriptions and save them to a catalog table](#example-generate-descriptions-and-save-them-to-a-catalog-table)

### Example: Generate descriptions and set them as comments

**Step 1: Create a stored procedure**

The following stored procedure does the following:

- Automatically generates descriptions for all tables (and their columns) in a schema.
- Sets these descriptions as comments on the tables and columns.

Copy code

```
CREATE OR REPLACE PROCEDURE DESCRIBE_TABLES_SET_COMMENT (database_name STRING, schema_name STRING,
  set_table_comment BOOLEAN,
  set_column_comment BOOLEAN)
  RETURNS STRING
  LANGUAGE PYTHON
  RUNTIME_VERSION = '3.10'
  PACKAGES=('snowflake-snowpark-python','joblib')
  HANDLER = 'main'
AS
$$
import json
from joblib import Parallel, delayed
import multiprocessing

def generate_descr(session, database_name, schema_name, table, set_table_comment, set_column_comment):
  table_name =  table['TABLE_NAME']
  async_job = session.sql(f"CALL AI_GENERATE_TABLE_DESC( '{database_name}.{schema_name}.{table_name}',{{'describe_columns': true, 'use_table_data': true}})").collect_nowait()
  result = async_job.result()
  output = json.loads(result[0][0])
  columns_ret = output["COLUMNS"]
  table_ret = output["TABLE"][0]

  table_description = table_ret["description"]
  table_name = table_ret["name"]
  database_name = table_ret["database_name"]
  schema_name = table_ret["schema_name"]

  if (set_table_comment):
      table_description = table_description.replace("'", "\\'")
      session.sql(f"""ALTER TABLE {database_name}.{schema_name}.{table_name} SET COMMENT = '{table_description}'""").collect()

  for column in columns_ret:
      column_description = column["description"];
      column_name = column["name"];
      if not column_name.isupper():
        column_name = '"' + column_name + '"'

      if (set_column_comment):
          column_description = column_description.replace("'", "\\'")
          session.sql(f"""ALTER TABLE  {database_name}.{schema_name}.{table_name} MODIFY COLUMN {column_name}  COMMENT '{column_description}'""").collect()

  return 'Success';

def main(session, database_name, schema_name, set_table_comment, set_column_comment):

    schema_name = schema_name.upper()
    database_name = database_name.upper()
    tablenames = session.sql(f"""SELECT table_name
                      FROM {database_name}.information_schema.tables
                      WHERE table_schema = '{schema_name}'
                      AND table_type = 'BASE TABLE'""").collect()
    try:
        Parallel(n_jobs=multiprocessing.cpu_count(), backend="threading")(
                delayed(generate_descr)(
                    session,
                    database_name,
                    schema_name,
                    table,
                    set_table_comment,
                    set_column_comment,
                ) for table in tablenames
            )
        return 'Success'
    except Exception as e:
        # Catch and return the error message
        return f"An error occurred: {str(e)}"
$$;
```

**Step 2: Call the stored procedure**

Assuming your schema is named `my_db.sch1`, call the stored procedure as follows to generate descriptions for both tables and columns:

Copy code

```
CALL describe_tables_set_comment('my_db', 'sch1', true, true);
```

You can run a DESC TABLE command to verify that the generated descriptions were set as comments on a table.

### Example: Generate descriptions and save them to a catalog table

**Step 1: Create a stored procedure**

The following stored procedure does the following:

- Automatically generates descriptions for all tables (and their columns) in a schema.
- Populates a catalog table, where each row represents a table or column with its generated description.

Copy code

```
CREATE OR REPLACE PROCEDURE DESCRIBE_TABLES_SET_CATALOG (database_name string, schema_name string, catalog_table string)
  RETURNS STRING
  LANGUAGE PYTHON
  RUNTIME_VERSION = '3.10'
  PACKAGES=('snowflake-snowpark-python','joblib')
  HANDLER = 'main'
AS
$$
import json
from joblib import Parallel, delayed
import multiprocessing

def generate_descr(session, database_name, schema_name, table, catalog_table):
    table_name =  table['TABLE_NAME']
    async_job = session.sql(f"CALL AI_GENERATE_TABLE_DESC( '{database_name}.{schema_name}.{table_name}',{{'describe_columns': true, 'use_table_data': true}})").collect_nowait()
    result = async_job.result()
    output = json.loads(result[0][0])
    columns_ret = output["COLUMNS"]
    table_ret = output["TABLE"][0]

    table_description = table_ret["description"]
    table_description = table_description.replace("'", "\\'")
    table_name = table_ret["name"]
    database_name = table_ret["database_name"]
    schema_name = table_ret["schema_name"]

    session.sql(f"""INSERT INTO {catalog_table} (domain, description, name, database_name, schema_name, table_name)
                          VALUES ('TABLE', '{table_description}', '{table_name}', '{database_name}', '{schema_name}', null)""").collect()

    for column in columns_ret:
        column_description = column["description"];
        column_description = column_description.replace("'", "\\'")
        column_name = column["name"];
        if not column_name.isupper():
            column_name = '"' + column_name + '"'
        session.sql(f"""INSERT INTO {catalog_table} (domain, description, name, database_name, schema_name, table_name)
                          VALUES ('COLUMN', '{column_description}', '{column_name}', '{database_name}', '{schema_name}', '{table_name}')""").collect()

    return 'Success';

def main(session, database_name, schema_name, catalog_table):

    schema_name = schema_name.upper()
    database_name = database_name.upper()
    catalog_table_upper = catalog_table.upper()
    tablenames = session.sql(f"""SELECT table_name
                      FROM {database_name}.information_schema.tables
                      WHERE table_schema = '{schema_name}'
                      AND table_type = 'BASE TABLE'
                      AND table_name !='{catalog_table_upper}'""").collect()
    try:
        Parallel(n_jobs=multiprocessing.cpu_count(), backend="threading")(
                delayed(generate_descr)(
                    session,
                    database_name,
                    schema_name,
                    table,
                    catalog_table,
                ) for table in tablenames
            )
        return 'Success'
    except Exception as e:
        # Catch and return the error message
        return f"An error occurred: {str(e)}"
$$;
```

**Step 2: Create the catalog table to populate**

Use the following code to create the catalog table where table and column descriptions are stored.

Copy code

```
CREATE OR REPLACE TABLE catalog_table (
  domain VARCHAR,
  description VARCHAR,
  name VARCHAR,
  database_name VARCHAR,
  schema_name VARCHAR,
  table_name VARCHAR
  );
```

**Step 3: Call the stored procedures**

Assuming your schema is named `my_db.sch1`, call the stored procedure as follows:

Copy code

```
CALL describe_tables_set_catalog('my_db', 'sch1', 'catalog_table');
```
