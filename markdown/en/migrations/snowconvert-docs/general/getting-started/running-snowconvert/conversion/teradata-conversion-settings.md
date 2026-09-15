# SnowConvert AI - Teradata Conversion Settings

## General Conversion Settings

### General Result Settings

[![General Result Settings sub-page](/static/images/migrations/sc-assets/image(531).png "image")](/static/images/migrations/sc-assets/image(531).png)

1. **Comment objects with missing dependencies:** Flag to indicate if the user wants to comment on nodes that have missing dependencies.
2. **Generate XML-tags for SQL statements in Stored Procedures:** Flag to indicate whether the SQL statements SELECT, INSERT, CREATE, DELETE, UPDATE, DROP, MERGE in Stored Procedures will be tagged on the converted code. This feature is used for easy statement identification on the migrated code. Wrapping these statements within these XML-like tags allows for other programs to quickly find and extract them. The decorated code looks like this:

   Copy code

   ```
   //<SQL_DELETE
   EXEC(DELETE FROM SB_EDP_SANDBOX_LAB.PUBLIC.USER_LIST,[])
   //SQL_DELETE!>
   ```
3. **Separate Period Data-type definitions and usages into begin and end Data-Time fields:** This flag is used to indicate that the tool should migrate any use of the PERIOD datatype as two separate DATETIME fields that will hold the original period begin and end values, anytime a period field or function is migrated using this flag SSC-EWI-TD0053 will be added to warn about this change.

   Input Code:

   Copy code

   ```
   CREATE TABLE myTable(
      col1 PERIOD(DATE),
      col2 VARCHAR(50),
      col3 PERIOD(TIMESTAMP)
   );
   ```

   Output Code:

   Copy code

   ```
   CREATE OR REPLACE TABLE myTable (
      col1 VARCHAR(24) !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!,
      col2 VARCHAR(50),
      col3 VARCHAR(58) !!!RESOLVE EWI!!! /*** SSC-EWI-TD0053 - SNOWFLAKE DOES NOT SUPPORT THE PERIOD DATATYPE, ALL PERIODS ARE HANDLED AS VARCHAR INSTEAD ***/!!!
   )
   COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
   ;
   ```
4. **Set encoding of the input files:** Check [General Conversion Settings](general-conversion-settings) for more details.
5. **Disable use of COLLATE for Case Specification**: This flag indicates whether to use COLLATE or UPPER to preserve Case Specification functionality, e.g. CASESPECIFIC or NOT CASESPECIFIC. By default, COLLATE will be used to emulate the case insensitive comparisons (NOT CASESPECIFIC), when turning on this flag SnowConvert will modify queries to use the UPPER function for case insensitive comparisons instead. To learn more about how Case Specification is handled by SnowConvert AI check [here](../../../../translation-references/teradata/session-modes).

   When the “Iceberg tables in Snowflake Horizon Catalog” option is selected in the [Table translation](#table-translation) setting, this setting will be enforced, this is done since Iceberg Tables do not support collation at the column level.

Note

To review the Settings that apply to all supported languages, go to the following [article](general-conversion-settings).

### Session Mode Settings

This settings sub-page is used to indicate the Session Mode of the input code.

[![Session Mode Settings sub-page](/static/images/migrations/sc-assets/image(532).png "image")](/static/images/migrations/sc-assets/image(532).png)

SnowConvert AI handles Teradata code in both TERA and ANSI modes. Currently, this is limited to the default case specification of character data and how it affects comparisons. By default, the Session Mode is TERA.

You can learn more about how SnowConvert AI handles and converts code depending on the session mode, check here.

## DB Objects Names Settings

[![DB Objects Names Settings page](/static/images/migrations/sc-assets/image(407).png "image")](/static/images/migrations/sc-assets/image(407).png)

1. **Schema:** The string value specifies the custom schema name to apply. If not specified, the original database name will be used. Example: DB1.**myCustomSchema**.Table1.
2. **Database:** The string value specifies the custom database name to apply. Example: **MyCustomDB**.PUBLIC.Table1.
3. **Default:** None of the above settings will be used in the object names.

## Prepare Code Settings

[![Prepare Code Settings page](/static/images/migrations/sc-assets/image(408).png "image")](/static/images/migrations/sc-assets/image(408).png)

### **Description**

**Prepare my code:** Flag to indicate whether the input code should be processed before parsing and transformation. This can be useful to improve the parsing process. By default, it’s set to FALSE.

Splits the input code top-level objects into multiple files. The containing folders would be organized as follows:

Copy code

```
└───A new folder named ''[input_folder_name]_Processed''
    └───Top-level object type
        └───Schema name
```

### **Example**

#### **Input**

Copy code

```
├───in
│       DDL_Macros.sql
│       DDL_Procedures.sql
│       DDL_Tables.sql
```

#### **Output**

Assume that the name of the files is the name of the top-level objects in the input files.

Copy code

```
├───in_Processed
    ├───macro
    │   └───MY_DATABASE
    │           MY_FIRST_MACRO.sql
    │           ANOTHER_MACRO.sql
    │
    ├───procedure
    │   └───MY_DATABASE
    │           A_PROCEDURE.sql
    │           ANOTHER_PROCEDURE.sql
    │           YET_ANOTHER_PROCEDURE.sql
    │
    └───table
        └───MY_DATABASE
                MY_TABLE.sql
                ADDITIONAL_TABLE.sql
                THIRD_TABLE.sql
```

Inside the “schema name” folder, there should be as many files as top-level objects in the input code. Also, it is possible to have copies of some files when multiple same-type top-level objects have the same name. In this case, the file names will be enumerated in ascending order.

[![](/static/images/migrations/sc-assets/image(541).png "image")](/static/images/migrations/sc-assets/image(541).png)

Only files with the “.sql”, “.ddl” and “.dml” extensions will be considered for splitting. Other kinds of files like “.bteq” scripts will be copied into the preprocessed folder and will be categorized depending on the script extension but they won’t be modified by the Split Task.

### Requirements

To identify top-level objects, a tag must be included in a comment before their declaration. Our [Extraction](../../code-extraction/teradata) scripts generate these tags.

The tag should follow the next format:

Copy code

```
<sc-top_level_object_type>top_level_object_name</sc-top_level_object_type>
```

You can follow the next example:

Copy code

```
/* <sc-table> MY_DATABASE.MY_TABLE</sc-table> */
CREATE TABLE "MY_DATABASE"."MY_TABLE" (
    "MY_COLUMN" INTEGER
) ;
```

## Format Conversion Settings

[![Format Conversion Settings page](/static/images/migrations/sc-assets/image(409).png "image")](/static/images/migrations/sc-assets/image(409).png)

1. **Character to Number default scale:** An integer value for the CHARACTER to Approximate Number transformation (Default: 10).
2. **Default TIMESTAMP format:** String value for the TIMESTAMP format (Default: “YYYY/MM/DD HH:MI:SS.FF6”).
3. **Default DATE format:** String value for the DATE format (Default: “YYYY/MM/DD”).
4. **Source TIMEZONE:** String value for the TIMEZONE format (Default: “GMT-5”).
5. **Default TIME format:** String value for the TIME format (Default: “HH:MI:SS.FF6”).

## Target Language for BTEQ, Procedures/Macros

[![BTEQ Target Language Settings page](/static/images/migrations/sc-assets/image(410).png "image")](/static/images/migrations/sc-assets/image(410).png)

Specifies the target language to convert Bteq and Mload script files. Currently supported values are **SnowScript** and **Python**. The default value is set to **Python**.

[![Procedures/Macros Target Language Settings page](/static/images/migrations/sc-assets/image(411).png "image")](/static/images/migrations/sc-assets/image(411).png)

String value specifying the target language to convert Stored procedures and Macros. Currently supported are: **SnowScript** and **JavaScript**. The default value is set to **SnowScript**.

**Reset Settings:** The reset settings option appears on every page. If you’ve made changes, you can reset SnowConvert AI to its original default settings.

## Table translation

Used to specify the type of tables that SnowConvert AI will output for table transformations, currently:

1. Snowflake-native tables
2. [Iceberg tables in Snowflake Horizon Catalog](../../../../translation-references/teradata/sql-translation-reference/Iceberg-tables-transformations)

Default is Snowflake-native tables.

The selected table type will be generated unless the source table is considered not compatible, the following criteria is applied for incompatible tables generation:

| Table type | Not compatible tables |
| --- | --- |
| Iceberg tables in Snowflake Horizon Catalog | Temporary tables (VOLATILE) |

Expand

Show lessSee more

Any table not compatible with the specified table type will not be affected by the setting and transformed to its default table type.
