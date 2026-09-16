# File formats to unload data

This topic provides an overview of supported data file formats for unloading data.

## Supported file formats

The following file formats are supported:

> | Structured/Semi-structured | Type | Notes |
> | --- | --- | --- |
> | Structured | Delimited (CSV, TSV, etc.) | Any valid singlebyte delimiter is supported; default is comma (i.e. CSV). |
> | Semi-structured | JSON, Parquet |  |
>
> Expand
>
> Show lessSee more

File format options specify the type of data contained in a file, as well as other related characteristics about the format of the data. The file format options you can specify are different depending on the type of data you are unloading to. Snowflake provides a full set of file format option defaults.

### Semi-structured data

When unloading to JSON files, Snowflake outputs to the [NDJSON](https://github.com/ndjson/ndjson-spec) (newline delimited JSON) standard format.

## Specify file format options

Individual file format options can be specified in any of the following places:

- In the definition of a table.
- In the definition of a named stage. For more information, see [CREATE STAGE](/sql-reference/sql/create-stage).
- Directly in a [COPY INTO <location>](/sql-reference/sql/copy-into-location) command when unloading data.

In addition, to simplify data unloading, Snowflake supports creating named file formats, which are database objects that encapsulate all of the required
format information. Named file formats can then be used as input in all the same places where you can specify individual file format options, thereby
helping to streamline the data unloading process for similarly-formatted data.

Named file formats are optional, but are recommended when you plan to regularly unload similarly-formatted data.

### Create a named file format

You can create a file format using either the web interface or SQL:

> Snowsight:
> :   In the navigation menu, select **Catalog** » **Explorer**. Then select the *<db\_name>* » **File Formats**.
>
> SQL:
> :   [CREATE FILE FORMAT](/sql-reference/sql/create-file-format)

For detailed descriptions of all the file format options, see [CREATE FILE FORMAT](/sql-reference/sql/create-file-format).

#### Examples

The following example creates a named CSV file format with a specified field delimiter:

> Copy code
>
> ```
> CREATE OR REPLACE FILE FORMAT my_csv_unload_format
>   TYPE = 'CSV'
>   FIELD_DELIMITER = '|';
> ```

The following example creates a named JSON file format:

> Copy code
>
> ```
> CREATE OR REPLACE FILE FORMAT my_json_unload_format
>   TYPE = 'JSON';
> ```
