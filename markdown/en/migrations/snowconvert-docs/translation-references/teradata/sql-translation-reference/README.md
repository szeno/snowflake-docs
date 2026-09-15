# Teradata - SQL Translation Reference

This section provides information about how Teradata SQL Syntax is translated to Snowflake.

Use this as a guide to understand how the transformed code might look when migrating from [**Teradata**](https://docs.teradata.com/) to [**Snowflake**](https://docs.snowflake.net/manuals/index.html). SQL has a similar syntax between dialects, but each dialect can extend or add new functionalities.

For this reason, when running SQL in one environment (such as Teradata) vs. another (such as Snowflake), there are many statements that require transformation or even removal. These transformations are performed.

Browse through the following pages to find more information about specific topics.

- [Analytic](analytic), compare Teradata Analytics statements and their equivalents in Snowflake.
- [Data Types](data-types), compare Teradata data types and their equivalents in Snowflake.
- [DDL](ddl-teradata), explore the translation of the Data Definition Language.
- [CREATE TYPE](teradata-create-type), translation of Teradata UDT definitions to Snowflake `CREATE TYPE`.
- [DML](dml-teradata), explore the translation of the Data Manipulation Language.
- [Built-in Functions](teradata-built-in-functions), compare functions included in the runtime of both languages.
