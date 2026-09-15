# SnowConvert AI - General Conversion Settings

## File encoding settings

This setting in SnowConvert AI determines how the tool reads and interprets the text within your source files. Choosing the correct encoding is important to ensure that all characters, especially accented letters, symbols, or text from various languages, are processed correctly during conversion. By default SnowConvert AI uses `UTF-8`.

[![image](/static/images/migrations/sc-assets/image(402).png "image")](/static/images/migrations/sc-assets/image(402).png)

**Manually Selecting an Encoding**

You can choose to override this automatic process by selecting a specific encoding from the dropdown menu. If you select an encoding manually (even if you select `UTF-8` explicitly), SnowConvert AI will use *only* that chosen encoding to read the files.

**Available Encoding Options**

The dropdown list allows you to force SnowConvert AI to use one of these specific encodings:

| Code Page | Name | Display Name |
| --- | --- | --- |
| 1200 | utf-16 | Unicode |
| 1201D | unicodeFFFE | Unicode (Big endian) |
| 12000 | utf-32 | Unicode (UTF-32) |
| 12001 | utf-32BE | Unicode (UTF-32 Big endian) |
| 20127 | us-ascii | US-ASCII |
| 28591 | iso-8859-1 | Western European (ISO) |
| 65000 | utf-7 | Unicode (UTF-7). *Not available in .NET 5* |
| 65001 | utf-8 | Unicode (UTF-8). ***Default encoding*** |

**Understanding `System Default (Preview)`**

When selecting the **`System Default (Preview)`** , SnowConvert AI uses a flexible approach:

1. It first tries to automatically detect the specific character encoding of each input file.
2. If auto-detection doesn’t identify the encoding, SnowConvert AI proceeds using `UTF-8`, which handles a very wide range of characters and is common for modern files.
3. As a fallback, if the `UTF-8` interpretation fails because it finds characters that aren’t valid in UTF-8, SnowConvert AI will then attempt to use your computer’s default system encoding.

It’s marked “Preview” because this behavior is experimental. System defaults can vary significantly between different computers and operating systems, potentially leading to inconsistent results or unsupported encodings.

**Recommendation**

If you encounter errors related to text interpretation or see garbled characters in your results, manually selecting the correct encoding is the best solution. If you know your files use a specific format (like `Western European`), select that. If you’re unsure but suspect encoding issues, explicitly selecting `UTF-8` is often a good starting point as it’s the most common standard for modern files.

## Materialized views conversion settings

On this page, you will find the necessary options to customize the parameters for translating Materialized Views (or join indexes in Teradata) to Dynamic Tables during your conversion.

[![image](/static/images/migrations/sc-assets/Screenshot2024-05-30at8.54.16AM.png "image")](/static/images/migrations/sc-assets/Screenshot2024-05-30at8.54.16AM.png)

[![image](/static/images/migrations/sc-assets/Screenshot2024-05-30at8.54.26AM.png "image")](/static/images/migrations/sc-assets/Screenshot2024-05-30at8.54.26AM.png)

To preserve the full functionality of Materialized Views, or Teradata’s Join Indexes, SnowConvert AI generates Dynamic Tables instead of creating a one-to-one Materialized View or transforming a Join Index into a Materialized View. This approach is necessary because Snowflake lacks certain configuration options available in other systems’ Materialized Views.

For further details on the limitations of Snowflake’s Materialized Views, please refer to [Materialized Views Limitations](https://docs.snowflake.com/en/user-guide/views-materialized#label-limitations-on-creating-materialized-views).

### Transformation

The settings defined here will apply to every instance of a Dynamic Table generated during the conversion process.

Dynamic Table Conversion Settings:

- **Target Lag**: This setting specifies the maximum allowable time for the dynamic table’s content to lag behind updates in the base table. For example, setting this to 5 minutes ensures that the data in the dynamic table is no more than 5 minutes behind the base table’s updates.
- **Warehouse**: This setting specifies the name of the Warehouse that supplies the computing resources for refreshing the dynamic table. You must have the USAGE privilege on this warehouse to create the dynamic table. By default, SnowConvert AI will use a placeholder value.

For more information, please refer to the Snowflake Dynamic Table [documentation](https://docs.snowflake.com/en/sql-reference/sql/create-dynamic-table).

## **Next steps for Amazon Redshift databases**

For Amazon Redshift databases, you can use SnowConvert AI to complete the following tasks after conversion:

- [Deployment](../../../user-guide/deployment)
- [Data migration](../../../user-guide/data-migration)
