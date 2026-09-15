# Using the Snowpark XML RowTag Reader

You can activate the Snowpark XML RowTag Reader by specifying `.option("rowTag", "<rowtag>")` in `session.read.option("rowTag", "<rowtag>").xml()`. Instead of loading the entire document as a single object, this mode splits the file based on the specified `rowTag`, loads each matching element as a separate row, and splits each row into multiple columns in a Snowpark DataFrame. The Reader is especially useful for processing only selective elements in XML files or ingesting large XML files in a scalable, Snowpark-native way.

## Example

This sample XML is an example:

Copy code

```
<library>
    <book id="1">
        <title>The Art of Snowflake</title>
        <author>Jane Doe</author>
        <price>29.99</price>
        <reviews>
            <review>
                <user>tech_guru_87</user>
                <rating>5</rating>
                <comment>Very insightful and practical.</comment>
            </review>
            <review>
                <user>datawizard</user>
                <rating>4</rating>
                <comment>Great read for data engineers.</comment>
            </review>
        </reviews>
        <editions>
            <edition year="2023" format="Hardcover"/>
            <edition year="2024" format="eBook"/>
        </editions>
    </book>

    <book id="2">
        <title>XML for Data Engineers</title>
        <author>John Smith</author>
        <price>35.50</price>
        <reviews>
            <review>
                <user>xml_master</user>
                <rating>5</rating>
                <comment>Perfect for mastering XML parsing.</comment>
            </review>
        </reviews>
        <editions>
            <edition year="2022" format="Paperback"/>
        </editions>
    </book>
</library>
```

### Snowpark script

Copy code

```
df = session.read.option("rowTag", "book").xml("@mystage/books.xml")
```

This loads each `<book>` element from the XML file into its own row, with child elements (for example, `<title>` and `<author>`) automatically extracted as columns of type `VARIANT`.

### Output

| `_id` | `author` | `editions` | `price` | `reviews` | `title` |
| --- | --- | --- | --- | --- | --- |
| “2” | “John Smith” | `{ "edition": { "_format": "Paperback", "_year": "2022" } }` | “35.50” | `{ "review": { "comment": "Perfect for mastering XML parsing.", "rating": "5", "user": "xml_master" } }` | “XML for Data Engineers” |
| “1” | “Jane Doe” | `{ "edition": [ { "_format": "Hardcover", "_year": "2023" }, { "_format": "eBook", "_year": "2024" } ] }` | “29.99” | `{ "review": [ { "comment": "Very insightful and practical.", "rating": "5", "user": "tech_guru_87" }, { "comment": "Great read for data engineers.", "rating": "4", "user": "datawizard" } ] }` | “The Art of Snowflake” |

Expand

Show lessSee more

- Each XML element identified by `rowTag` becomes one row.
- Each sub-element within that tag becomes a column, stored as a `VARIANT`. Nested elements are captured as nested `VARIANT` data.
- The resulting DataFrame is flattened and columnized and behaves like any other Snowpark DataFrame.

## Getting started

1. Install the Snowpark Python package:

   Copy code

   ```
   pip install snowflake-snowpark-python
   ```
2. Upload your XML file to a Snowflake stage:

   Copy code

   ```
   PUT file:///path/to/books.xml @mystage;
   ```
3. Use Snowpark to read the XML file:

   Copy code

   ```
   df = session.read.option("rowTag", "book").xml("@mystage/books.xml")
   ```
4. Use DataFrame methods to transform or save:

   Copy code

   ```
   df.select(col("`title`"), col("`author`")).show()
   df.write.save_as_table("books_table")
   ```

## Supported options

- `rowTag` (Required): The name of the XML element to extract as a row.
- `rowValidationXSDPath` (Optional): Stage path to an XSD used to validate each rowTag fragment during load.
- `mode` (Optional): Default behavior loads without validation. When `rowValidationXSDPath` is set:
  - `PERMISSIVE`: Quarantines invalid rows in `_corrupt_record`; loads the rest.
  - `FAILFAST`: Stops at the first invalid row and raises an error.

For more information about XML options, see [snowflake.snowpark.DataFrameReader.xml](/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrameReader.xml).

## Validate XML using XSD

- To validate each `rowTag` fragment against an XSD during load, set the XSD path and choose a validation mode:

  Copy code

  ```
  df = (
  session.read
   .option("rowTag", "book")
   .option("rowValidationXSDPath", "@mystage/schema.xsd")  # validates each row element
   .option("mode", "PERMISSIVE")                         # or "FAILFAST"
   .xml("@mystage/books.xml")
  )
  ```

`PERMISSIVE`: Invalid rows are quarantined in a special `_corrupt_record` column; valid rows load normally.

- To persist the result, write the DataFrame to a table with `df.write.save_as_table("<table_name>")`. The table will include all parsed columns plus an extra `_corrupt_record` column: it is `NULL` for valid rows and contains the full XML records for invalid rows (with the other columns showing `NULL`).

  ```
  +-------------------+
  | _corrupt_record   |
  | <book id="1"> ... |
  | <book id="2"> ... |
  +-------------------+
  ```

`FAILFAST`: The read stops at the first offending row and returns an error.

## Limitations

Snowpark XML RowTag Reader has the following limitations:

- Doesn’t infer schema, and the output columns are all of type `VARIANT`.
- Only supports files stored in Snowflake stages; local files are not supported.
- Is available only in the Snowpark Python library.
