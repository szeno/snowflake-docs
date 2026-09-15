# Build a data processing pipeline using a directory table

Build a data processing pipeline by combining a directory table,
which tracks and stores file-level metadata on a stage, with other Snowflake objects
such as streams and tasks.

A [stream](/user-guide/streams-intro) records data manipulation language (DML) changes made to a directory table,
table, external table, or the underlying tables in a view. A [task](/user-guide/tasks-intro) executes a single action,
which can be a SQL command or an extensive [user-defined function (UDF)](/developer-guide/udf/udf-overview).
You can schedule a task to run periodically, or run a task on demand.

## Example: Create a simple pipeline to process PDFs

This example builds a simple data processing pipeline that does the following:

1. Detects PDF files added to a stage.
2. Extracts data from the files.
3. Inserts the data into a Snowflake table.

The pipeline uses a stream to detect changes to a directory table on the stage,
and a task that executes a UDF to extract data from the files.

The following diagram summarizes how the example pipeline works:

![A simple data processing pipeline that uses a stream to track changes to a directory table.](/static/images/data-lake-dirtable-pipeline.png)

### Step 1: Create a stage with a directory table enabled

Create an internal stage with a directory table enabled.
The example statement sets the `ENCRYPTION` type to `SNOWFLAKE_SSE` to
[enable unstructured data access on the stage](/user-guide/unstructured-intro#label-file-url-server-side-encryption).

Copy code

```
CREATE OR REPLACE STAGE my_pdf_stage
  ENCRYPTION = ( TYPE = 'SNOWFLAKE_SSE')
  DIRECTORY = ( ENABLE = TRUE);
```

### Step 2: Create a stream on the directory table

Create a stream on the directory table by specifying the stage that the directory table belongs to.
The stream will track changes to the directory table. In step 5 of this example, we use this stream to construct a task.

Copy code

```
CREATE STREAM my_pdf_stream ON STAGE my_pdf_stage;
```

### Step 3: Create a user-defined function to parse PDFs

Create a UDF that extracts data from PDF files. The task that you create in a later step will call this UDF to process
newly-added files on the stage.

The following example statement creates a Python UDF named `PDF_PARSE` that processes PDF files containing product review data.
The UDF extracts form field data using the [PyPDF2](https://pypi.org/project/PyPDF2/) library.
It returns a dictionary that contains the form names and values as key-value pairs.

Note

The UDF reads dynamically-specified files using the `SnowflakeFile` class. To learn more about `SnowflakeFile`,
see [Reading a dynamically-specified file with `SnowflakeFile`](/developer-guide/udf/python/udf-python-examples#label-reading-file-from-python-udf-snowflakefile).

Copy code

```
CREATE OR REPLACE FUNCTION PDF_PARSE(file_path string)
  RETURNS VARIANT
  LANGUAGE PYTHON
  RUNTIME_VERSION = '3.8'
  HANDLER = 'parse_pdf_fields'
  PACKAGES=('typing-extensions','PyPDF2','snowflake-snowpark-python')
AS
$$
from pathlib import Path
import PyPDF2 as pypdf
from io import BytesIO
from snowflake.snowpark.files import SnowflakeFile

def parse_pdf_fields(file_path):
    with SnowflakeFile.open(file_path, 'rb') as f:
        buffer = BytesIO(f.readall())
    reader = pypdf.PdfFileReader(buffer)
    fields = reader.getFields()
    field_dict = {}
    for k, v in fields.items():
        if "/V" in v.keys():
            field_dict[v["/T"]] = v["/V"].replace("/", "") if v["/V"].startswith("/") else v["/V"]

    return field_dict
$$;
```

### Step 4: Create a table to store the file contents

Next, create a table where each row stores information about a file on the
stage in columns named `file_name` and `file_data`. The task that you create in a later step
will load data into this table.

Copy code

```
CREATE OR REPLACE TABLE prod_reviews (
  file_name varchar,
  file_data variant
);
```

### Step 5: Create a task

Create a scheduled task that checks the stream for new files on the stage and inserts the file data into the `prod_reviews` table.

The following statement creates a scheduled task using the stream created previously.
The task uses the [SYSTEM$STREAM\_HAS\_DATA](/sql-reference/functions/system_stream_has_data) function
to check whether the stream contains change data capture (CDC) records.

Copy code

```
CREATE OR REPLACE TASK load_new_file_data
  WAREHOUSE = 'MY_WAREHOUSE'
  SCHEDULE = '1 minute'
  COMMENT = 'Process new files on the stage and insert their data into the prod_reviews table.'
  WHEN
  SYSTEM$STREAM_HAS_DATA('my_pdf_stream')
  AS
  INSERT INTO prod_reviews (
    SELECT relative_path as file_name,
    PDF_PARSE(build_scoped_file_url('@my_pdf_stage', relative_path)) as file_data
    FROM my_pdf_stream
    WHERE METADATA$ACTION='INSERT'
  );
```

### Step 6: Run the task to test the pipeline

To check that the pipeline works, you can add files to the stage, manually execute the task, and then query the `product_reviews` table.

Start by adding some PDF files to the `my_pdf_stage` stage, and then refresh the stage.

Note

This example uses [PUT](/sql-reference/sql/put) commands, which you can’t run from a worksheet in the Snowflake web interface.
To upload files with Snowsight, see [Upload files onto a named internal stage](/user-guide/data-load-local-file-system-stage-ui#label-snowsight-stage-upload-files-internal).

Copy code

```
PUT file:///my/file/path/prod_review1.pdf @my_pdf_stage AUTO_COMPRESS = FALSE;
PUT file:///my/file/path/prod_review2.pdf @my_pdf_stage AUTO_COMPRESS = FALSE;

ALTER STAGE my_pdf_stage REFRESH;
```

You can query the stream to verify that it has recorded the two PDF files that we added to the stage.

Copy code

```
SELECT * FROM my_pdf_stream;
```

Now, execute the task to process the PDF files and update the `product_reviews` table.

Copy code

```
EXECUTE TASK load_new_file_data;
+----------------------------------------------------------+
| status                                                   |
|----------------------------------------------------------|
| Task LOAD_NEW_FILE_DATA is scheduled to run immediately. |
+----------------------------------------------------------+
1 Row(s) produced. Time Elapsed: 0.178s
```

Query the `product_reviews` table to see that the task has added a row for each PDF file.

Copy code

```
select * from prod_reviews;
+------------------+----------------------------------+
| FILE_NAME        | FILE_DATA                        |
|------------------+----------------------------------|
| prod_review1.pdf | {                                |
|                  |   "FirstName": "John",           |
|                  |   "LastName": "Johnson",         |
|                  |   "Middle Name": "Michael",      |
|                  |   "Product": "Tennis Shoes",     |
|                  |   "Purchase Date": "03/15/2022", |
|                  |   "Recommend": "Yes"             |
|                  | }                                |
| prod_review2.pdf | {                                |
|                  |   "FirstName": "Emily",          |
|                  |   "LastName": "Smith",           |
|                  |   "Middle Name": "Ann",          |
|                  |   "Product": "Red Skateboard",   |
|                  |   "Purchase Date": "01/10/2023", |
|                  |   "Recommend": "MayBe"           |
|                  | }                                |
+------------------+----------------------------------+
```

Finally, you can create a view that parses the objects in the `FILE_DATA` column into separate columns.
You can then query the view to analyze and work with the file contents.

Copy code

```
CREATE OR REPLACE VIEW prod_review_info_v
  AS
  WITH file_data
  AS (
      SELECT
        file_name
        , parse_json(file_data) AS file_data
      FROM prod_reviews
  )
  SELECT
      file_name
      , file_data:FirstName::varchar AS first_name
      , file_data:LastName::varchar AS last_name
      , file_data:"Middle Name"::varchar AS middle_name
      , file_data:Product::varchar AS product
      , file_data:"Purchase Date"::date AS purchase_date
      , file_data:Recommend::varchar AS recommended
      , build_scoped_file_url(@my_pdf_stage, file_name) AS scoped_review_url
  FROM file_data;

SELECT * FROM prod_review_info_v;

+------------------+------------+-----------+-------------+----------------+---------------+-------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| FILE_NAME        | FIRST_NAME | LAST_NAME | MIDDLE_NAME | PRODUCT        | PURCHASE_DATE | RECOMMENDED | SCOPED_REVIEW_URL                                                                                                                                                                                                                                                                                                                                                                                                              |
|------------------+------------+-----------+-------------+----------------+---------------+-------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| prod_review1.pdf | John       | Johnson   | Michael     | Tennis Shoes   | 2022-03-15    | Yes         | https://mydeployment.us-west-2.aws.privatelink.snowflakecomputing.com/api/files/01aefcdc-0000-6f92-0000-012900fdc73e/1275606224902/RZ4s%2bJLa6iHmLouHA79b94tg%2f3SDA%2bOQX01pAYo%2bl6gAxiLK8FGB%2bv8L2QSB51tWP%2fBemAbpFd%2btKfEgKibhCXN2QdMCNraOcC1uLdR7XV40JRIrB4gDYkpHxx3HpCSlKkqXeuBll%2fyZW9Dc6ZEtwF19GbnEBR9FwiUgyqWjqSf4KTmgWKv5gFCpxwqsQgofJs%2fqINOy%2bOaRPa%2b65gcnPpY2Dc1tGkJGC%2fT110Iw30cKuMGZ2HU%3d              |
| prod_review2.pdf | Emily      | Smith     | Ann         | Red Skateboard | 2023-01-10    | MayBe       | https://mydeployment.us-west-2.aws.privatelink.snowflakecomputing.com/api/files/01aefcdc-0000-6f92-0000-012900fdc73e/1275606224902/g3glgIbGik3VOmgcnltZxVNQed8%2fSBehlXbgdZBZqS1iAEsFPd8pkUNB1DSQEHoHfHcWLsaLblAdSpPIZm7wDwaHGvbeRbLit6nvE%2be2LHOsPR1UEJrNn83o%2fZyq4kVCIgKeSfMeGH2Gmrvi82JW%2fDOyZJITgCEZzpvWGC9Rmnr1A8vux47uZj9MYjdiN2Hho3uL9ExeFVo8FUtR%2fHkdCJKIzCRidD5oP55m9p2ml2yHOkDJW50%3d                            |
+------------------+------------+-----------+-------------+----------------+---------------+-------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```
