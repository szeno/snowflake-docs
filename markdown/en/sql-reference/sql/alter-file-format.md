# ALTER FILE FORMAT

Modifies the properties for an existing file format object. Currently the only actions that are supported are renaming the file format, changing
the file format options (based on the type), and adding/changing a comment. To make any other changes, you must drop the file format and then
recreate it.

See also:
:   [CREATE FILE FORMAT](/sql-reference/sql/create-file-format) , [DROP FILE FORMAT](/sql-reference/sql/drop-file-format) , [SHOW FILE FORMATS](/sql-reference/sql/show-file-formats) , [DESCRIBE FILE FORMAT](/sql-reference/sql/desc-file-format)

## Syntax

Copy code

```
ALTER FILE FORMAT [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER FILE FORMAT [ IF EXISTS ] <name> SET { [ formatTypeOptions ] [ COMMENT = '<string_literal>' ] }
```

Where:

> Copy code
>
> ```
> formatTypeOptions ::=
> -- If TYPE = CSV
>      COMPRESSION = AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE
>      RECORD_DELIMITER = '<string>' | NONE
>      FIELD_DELIMITER = '<string>' | NONE
>      MULTI_LINE = TRUE | FALSE
>      FILE_EXTENSION = '<string>'
>      PARSE_HEADER = TRUE | FALSE
>      SKIP_HEADER = <integer>
>      SKIP_BLANK_LINES = TRUE | FALSE
>      DATE_FORMAT = '<string>' | AUTO
>      TIME_FORMAT = '<string>' | AUTO
>      TIMESTAMP_FORMAT = '<string>' | AUTO
>      BINARY_FORMAT = HEX | BASE64 | UTF8
>      ESCAPE = '<character>' | NONE
>      ESCAPE_UNENCLOSED_FIELD = '<character>' | NONE
>      TRIM_SPACE = TRUE | FALSE
>      FIELD_OPTIONALLY_ENCLOSED_BY = '<character>' | NONE
>      NULL_IF = ( '<string>' [ , '<string>' ... ] )
>      ERROR_ON_COLUMN_COUNT_MISMATCH = TRUE | FALSE
>      REPLACE_INVALID_CHARACTERS = TRUE | FALSE
>      EMPTY_FIELD_AS_NULL = TRUE | FALSE
>      SKIP_BYTE_ORDER_MARK = TRUE | FALSE
>      ENCODING = '<string>' | UTF8
> -- If TYPE = JSON
>      COMPRESSION = AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE
>      DATE_FORMAT = '<string>' | AUTO
>      TIME_FORMAT = '<string>' | AUTO
>      TIMESTAMP_FORMAT = '<string>' | AUTO
>      BINARY_FORMAT = HEX | BASE64 | UTF8
>      TRIM_SPACE = TRUE | FALSE
>      MULTI_LINE = TRUE | FALSE
>      NULL_IF = ( '<string>' [ , '<string>' ... ] )
>      FILE_EXTENSION = '<string>'
>      ENABLE_OCTAL = TRUE | FALSE
>      ALLOW_DUPLICATE = TRUE | FALSE
>      STRIP_OUTER_ARRAY = TRUE | FALSE
>      STRIP_NULL_VALUES = TRUE | FALSE
>      REPLACE_INVALID_CHARACTERS = TRUE | FALSE
>      IGNORE_UTF8_ERRORS = TRUE | FALSE
>      SKIP_BYTE_ORDER_MARK = TRUE | FALSE
> -- If TYPE = AVRO
>      COMPRESSION = AUTO | GZIP | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE
>      TRIM_SPACE = TRUE | FALSE
>      REPLACE_INVALID_CHARACTERS = TRUE | FALSE
>      NULL_IF = ( '<string>' [ , '<string>' ... ] )
> -- If TYPE = ORC
>      TRIM_SPACE = TRUE | FALSE
>      REPLACE_INVALID_CHARACTERS = TRUE | FALSE
>      NULL_IF = ( '<string>' [ , '<string>' ... ] )
> -- If TYPE = PARQUET
>      COMPRESSION = AUTO | LZO | SNAPPY | NONE
>      SNAPPY_COMPRESSION = TRUE | FALSE
>      BINARY_AS_TEXT = TRUE | FALSE
>      USE_LOGICAL_TYPE = TRUE | FALSE
>      TRIM_SPACE = TRUE | FALSE
>      USE_VECTORIZED_SCANNER = TRUE | FALSE
>      REPLACE_INVALID_CHARACTERS = TRUE | FALSE
>      NULL_IF = ( '<string>' [ , '<string>' ... ] )
> -- If TYPE = XML
>      COMPRESSION = AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE
>      IGNORE_UTF8_ERRORS = TRUE | FALSE
>      PRESERVE_SPACE = TRUE | FALSE
>      STRIP_OUTER_ELEMENT = TRUE | FALSE
>      DISABLE_AUTO_CONVERT = TRUE | FALSE
>      REPLACE_INVALID_CHARACTERS = TRUE | FALSE
>      SKIP_BYTE_ORDER_MARK = TRUE | FALSE
> ```

## Parameters

`name`
:   Specifies the identifier for the file format to alter. If the identifier contains spaces or special characters, the entire string must be
    enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`RENAME TO new_name`
:   Specifies the new identifier for the file format; must be unique for the schema.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

    You can move the object to a different database and/or schema while optionally renaming the object. To do so, specify
    a qualified `new_name` value that includes the new database and/or schema name in the form
    `db_name.schema_name.object_name` or `schema_name.object_name`, respectively.

    Note

    - The destination database and/or schema must already exist. In addition, an object with the same name cannot already
      exist in the new location; otherwise, the statement returns an error.
    - Moving an object to a managed access schema is prohibited unless the object owner (that is, the role that has
      the OWNERSHIP privilege on the object) also owns the target schema.

    When an object is renamed, other objects that reference it must be updated with the new name.

`SET ...`
:   Specifies the options/properties to set for the file format:

    `FILE_FORMAT = ( ... )`
    :   Modifies the format-specific options for the file format. For more details, see
        [Format Type Options](#label-alter-file-format-formattypeoptions) (in this topic).

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites the existing comment for the file format.

## Format type options (`formatTypeOptions`)

Depending on the file format type specified (`TYPE = ...`), you can include one or more of the following format-specific options (separated
by blank spaces, commas, or new lines):

# TYPE = CSV

`COMPRESSION = AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE`
:   Use:
    :   Data loading, data unloading, and external tables

    Definition:
    :   - When loading data, specifies the current compression algorithm for the data file. Snowflake uses this option to detect how an already-compressed data file was compressed so that the compressed data in the file can be extracted for loading.
        - When unloading data, compresses the data file using the specified compression algorithm.

    Values:
    :   | Supported Values | Notes |
        | --- | --- |
        | `AUTO` | When loading data, compression algorithm detected automatically, except for Brotli-compressed files, which cannot currently be detected automatically. When unloading data, files are automatically compressed using the default, which is gzip. |
        | `GZIP` |  |
        | `BZ2` |  |
        | `BROTLI` | Must be specified when loading/unloading Brotli-compressed files. |
        | `ZSTD` | Zstandard v0.8 (and higher) is supported. |
        | `DEFLATE` | Deflate-compressed files (with zlib header, RFC1950). |
        | `RAW_DEFLATE` | Raw Deflate-compressed files (without header, RFC1951). |
        | `NONE` | When loading data, indicates that the files have not been compressed. When unloading data, specifies that the unloaded files are not compressed. |

        Expand

        Show lessSee more

    Default:
    :   `AUTO`

`RECORD_DELIMITER = 'string' | NONE`
:   Use:
    :   Data loading, data unloading, and external tables

    Definition:
    :   One or more singlebyte or multibyte characters that separate records in an input file (data loading) or unloaded file (data unloading). Accepts common escape sequences or the following singlebyte or multibyte characters:

        Singlebyte characters:
        :   Octal values (prefixed by `\\`) or hex values (prefixed by `0x` or `\x`). For example, for records delimited by the circumflex accent (`^`) character, specify the octal (`\\136`) or hex (`0x5e`) value.

        Multibyte characters:
        :   Hex values (prefixed by `\x`). For example, for records delimited by the cent (`¢`) character, specify the hex (`\xC2\xA2`) value.

            The delimiter for RECORD\_DELIMITER or FIELD\_DELIMITER cannot be a substring of the delimiter for the other file format option (For example, `FIELD_DELIMITER = 'aa' RECORD_DELIMITER = 'aabb'`).

        The specified delimiter must be a valid UTF-8 character and not a random sequence of bytes. Also note that the delimiter is limited to a maximum of 20 characters.

        Also accepts a value of `NONE`.

    Default:
    :   Data loading:
        :   New line character. Note that “new line” is logical such that `\r\n` will be understood as a new line for files on a Windows platform.

        Data unloading:
        :   New line character (`\n`).

`FIELD_DELIMITER = 'string' | NONE`
:   Use:
    :   Data loading, data unloading, and external tables

    Definition:
    :   One or more singlebyte or multibyte characters that separate fields in an input file (data loading) or unloaded file (data unloading). Accepts common escape sequences or the following singlebyte or multibyte characters:

        Singlebyte characters:
        :   Octal values (prefixed by `\\`) or hex values (prefixed by `0x` or `\x`). For example, for records delimited by the circumflex accent (`^`) character, specify the octal (`\\136`) or hex (`0x5e`) value.

        Multibyte characters:
        :   Hex values (prefixed by `\x`). For example, for records delimited by the cent (`¢`) character, specify the hex (`\xC2\xA2`) value.

            The delimiter for RECORD\_DELIMITER or FIELD\_DELIMITER cannot be a substring of the delimiter for the other file format option (For example, `FIELD_DELIMITER = 'aa' RECORD_DELIMITER = 'aabb'`).

            > Note
            >
            > For non-ASCII characters, you must use the hex byte sequence value to get a deterministic behavior.

        The specified delimiter must be a valid UTF-8 character and not a random sequence of bytes. Also note that the delimiter is limited to a maximum of 20 characters.

        Also accepts a value of `NONE`.

    Default:
    :   comma (`,`)

`MULTI_LINE = TRUE | FALSE`
:   Use:
    :   Data loading and external tables

    Definition:
    :   Boolean that specifies whether multiple lines are allowed. If MULTI\_LINE is set to `FALSE` and the specified record delimiter is present within a CSV field, the record containing the field will be interpreted as an error.

    Default:
    :   `TRUE`

    Note

    If you are loading large uncompressed CSV files (greater than 128MB) that follow the RFC4180 specification, Snowflake supports parallel scanning of these CSV files when MULTI\_LINE is set to `FALSE`, COMPRESSION is set to `NONE`, and ON\_ERROR is set to `ABORT_STATEMENT` or `CONTINUE`.

`FILE_EXTENSION = 'string' | NONE`
:   Use:
    :   Data unloading only

    Definition:
    :   Specifies the extension for files unloaded to a stage. Accepts any extension. The user is responsible for specifying a file extension that can be read by any desired software or services.

    Default:
    :   null, meaning the file extension is determined by the format type: `.csv[compression]`, where `compression` is the extension added by the compression method, if `COMPRESSION` is set.

    Note

    If the `SINGLE` copy option is `TRUE`, then the COPY command unloads a file without a file extension by default. To specify a file extension, provide a file name and extension in the
    `internal_location` or `external_location` path (For example, `copy into @stage/data.csv`).

`PARSE_HEADER = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether to use the first row headers in the data files to determine column names.

    This file format option is applied to the following actions only:

    > - Automatically detecting column definitions by using the INFER\_SCHEMA function.
    > - Loading CSV data into separate columns by using the INFER\_SCHEMA function and MATCH\_BY\_COLUMN\_NAME copy option.

    If the option is set to TRUE, the first row headers will be used to determine column names. The default value FALSE will return column names as c\*, where \* is the position of the column.

    Note

    - This option isn’t supported for external tables.
    - The SKIP\_HEADER option isn’t supported if you set `PARSE_HEADER = TRUE`.

    Default:
    :   `FALSE`

`SKIP_HEADER = integer`
:   Use:
    :   Data loading and external tables

    Definition:
    :   Number of lines at the start of the file to skip.

    Note that SKIP\_HEADER does not use the RECORD\_DELIMITER or FIELD\_DELIMITER values to determine what a header line is; rather, it simply skips the specified number of CRLF (Carriage Return, Line Feed)-delimited lines in the file. RECORD\_DELIMITER and FIELD\_DELIMITER are then used to determine the rows of data to load.

    Default:
    :   `0`

`SKIP_BLANK_LINES = TRUE | FALSE`
:   Use:
    :   Data loading and external tables

    Definition:
    :   Boolean that specifies to skip any blank lines encountered in the data files; otherwise, blank lines produce an end-of-record error (default behavior).

    Default:
    :   `FALSE`

`DATE_FORMAT = 'string' | AUTO`
:   Use:
    :   Data loading and unloading

    Definition:
    :   Defines the format of date values in the data files (data loading) or table (data unloading). If a value is not specified or is `AUTO`, the value for the [DATE\_INPUT\_FORMAT](/sql-reference/parameters#label-date-input-format) (data loading) or [DATE\_OUTPUT\_FORMAT](/sql-reference/parameters#label-date-output-format) (data unloading) parameter is used.

    Default:
    :   `AUTO`

`TIME_FORMAT = 'string' | AUTO`
:   Use:
    :   Data loading and unloading

    Definition:
    :   Defines the format of time values in the data files (data loading) or table (data unloading). If a value is not specified or is `AUTO`, the value for the [TIME\_INPUT\_FORMAT](/sql-reference/parameters#label-time-input-format) (data loading) or [TIME\_OUTPUT\_FORMAT](/sql-reference/parameters#label-time-output-format) (data unloading) parameter is used.

    Default:
    :   `AUTO`

`TIMESTAMP_FORMAT = string' | AUTO`
:   Use:
    :   Data loading and unloading

    Definition:
    :   Defines the format of timestamp values in the data files (data loading) or table (data unloading). If a value is not specified or is `AUTO`, the value for the [TIMESTAMP\_INPUT\_FORMAT](/sql-reference/parameters#label-timestamp-input-format) (data loading) or [TIMESTAMP\_OUTPUT\_FORMAT](/sql-reference/parameters#label-timestamp-output-format) (data unloading) parameter is used.

    Default:
    :   `AUTO`

`BINARY_FORMAT = HEX | BASE64 | UTF8`
:   Use:
    :   Data loading and unloading

    Definition:
    :   Defines the encoding format for binary input or output. The option can be used when loading data into or unloading data from binary columns in a table.

    Default:
    :   `HEX`

`ESCAPE = 'character' | NONE`
:   Use:
    :   Data loading and unloading

    Definition:
    :   A singlebyte character string used as the escape character for enclosed or unenclosed field values. An escape character invokes an alternative interpretation on subsequent characters in a character sequence. You can use the ESCAPE character to interpret instances of the `FIELD_OPTIONALLY_ENCLOSED_BY` character in the data as literals.

        Accepts common escape sequences, octal values, or hex values.

    Loading data:
    :   Specifies the escape character for enclosed fields only. Specify the character used to enclose fields by setting `FIELD_OPTIONALLY_ENCLOSED_BY`.

        Note

        This file format option supports singlebyte characters only. Note that UTF-8 character encoding represents high-order ASCII characters
        as multibyte characters. If your data file is encoded with the UTF-8 character set, you cannot specify a high-order ASCII character as
        the option value.

        In addition, if you specify a high-order ASCII character, we recommend that you set the `ENCODING = 'string'` file format
        option as the character encoding for your data files to ensure the character is interpreted correctly.

    Unloading data:
    :   If this option is set, it overrides the escape character set for `ESCAPE_UNENCLOSED_FIELD`.

    Default:
    :   `NONE`

`ESCAPE_UNENCLOSED_FIELD = 'character' | NONE`
:   Use:
    :   Data loading, data unloading, and external tables

    Definition:
    :   A singlebyte character string used as the escape character for unenclosed field values only. An escape character invokes an alternative interpretation on subsequent characters in a character sequence. You can use the ESCAPE character to interpret instances of the `FIELD_DELIMITER` or `RECORD_DELIMITER` characters in the data as literals. The escape character can also be used to escape instances of itself in the data.

        Accepts common escape sequences, octal values, or hex values.

    Loading data:
    :   Specifies the escape character for unenclosed fields only.

        Note

        - The default value is `\\`. If a row in a data file ends in the backslash (`\`) character, this character escapes the newline or
          carriage return character specified for the `RECORD_DELIMITER` file format option. As a result, the load operation treats
          this row and the next row as a single row of data. To avoid this issue, set the value to `NONE`.
        - This file format option supports singlebyte characters only. Note that UTF-8 character encoding represents high-order ASCII characters
          as multibyte characters. If your data file is encoded with the UTF-8 character set, you cannot specify a high-order ASCII character as
          the option value.

          In addition, if you specify a high-order ASCII character, we recommend that you set the `ENCODING = 'string'` file format
          option as the character encoding for your data files to ensure the character is interpreted correctly.

    Unloading data:
    :   If `ESCAPE` is set, the escape character set for that file format option overrides this option.

    Default:
    :   backslash (`\\`)

`TRIM_SPACE = TRUE | FALSE`
:   Use:
    :   Data loading and external tables

    Definition:
    :   Boolean that specifies whether to remove white space from fields.

        For example, if your external database software encloses fields in quotes, but inserts a leading space, Snowflake reads the leading space rather than the opening quotation character as the beginning of the
        field (i.e. the quotation marks are interpreted as part of the string of field data). Set this option to `TRUE` to remove undesirable spaces during the data load.

        As another example, if leading or trailing spaces surround quotes that enclose strings, you can remove the surrounding spaces using this option and the quote character using the
        `FIELD_OPTIONALLY_ENCLOSED_BY` option. Note that any spaces within the quotes are preserved. For example, assuming `FIELD_DELIMITER = '|'` and `FIELD_OPTIONALLY_ENCLOSED_BY = '"'`:

        Copy code

        ```
        |"Hello world"|    /* loads as */  >Hello world<
        |" Hello world "|  /* loads as */  > Hello world <
        | "Hello world" |  /* loads as */  >Hello world<
        ```

        (the brackets in this example are not loaded; they are used to demarcate the beginning and end of the loaded strings)

    Default:
    :   `FALSE`

`FIELD_OPTIONALLY_ENCLOSED_BY = 'character' | NONE`
:   Use:
    :   Data loading, data unloading, and external tables

    Definition:
    :   Character used to enclose strings. Value can be `NONE`, single quote character (`'`), or double quote character (`"`). To use the single quote character, use the octal or hex representation (`0x27`) or the double single-quoted escape (`''`).

        Data unloading only:
        :   When a field in the source table contains this character, Snowflake escapes it using the same character for unloading. For example, if the value is the double quote character and a field contains the string `A "B" C`, Snowflake escapes the double quotes for unloading as follows:

            `A ""B"" C`

    Default:
    :   `NONE`

`NULL_IF = ( 'string1' [ , 'string2' , ... ] )`
:   Use:
    :   Data loading, data unloading, and external tables

    Definition:
    :   String used to convert to and from SQL NULL:

        - When loading data, Snowflake replaces these values in the data load source with SQL NULL. To specify more than one string, enclose
          the list of strings in parentheses and use commas to separate each value.

          Note that Snowflake converts all instances of the value to NULL, regardless of the data type. For example, if `2` is specified as
          a value, all instances of `2` as either a string or number are converted.

          For example:

          `NULL_IF = ('\N', 'NULL', 'NUL', '')`

          Note that this option can include empty strings.
        - When unloading data, Snowflake converts SQL NULL values to the first value in the list.

    Default:
    :   `\N` (that is, NULL, which assumes the `ESCAPE_UNENCLOSED_FIELD` value is `\\`)

`ERROR_ON_COLUMN_COUNT_MISMATCH = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether to generate a parsing error if the number of delimited columns (i.e. fields) in an input file does not match the number of columns in the corresponding table.

        If set to `FALSE`, an error is not generated and the load continues. If the file is successfully loaded:

        - If the input file contains records with more fields than columns in the table, the matching fields are loaded in order of occurrence in the file and the remaining fields are not loaded.
        - If the input file contains records with fewer fields than columns in the table, the non-matching columns in the table are loaded with NULL values.

        This option assumes all the records within the input file are the same length (i.e. a file containing records of varying length return an error regardless of the value specified for this parameter).

    Default:
    :   `TRUE`

    Note

    When [transforming data during loading](/user-guide/data-load-transform) (i.e. using a query as the source for the COPY command), this option is ignored. There is no requirement for your data files to have
    the same number and ordering of columns as your target table.

`REPLACE_INVALID_CHARACTERS = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (`�`).

    If set to `TRUE`, Snowflake replaces invalid UTF-8 characters with the Unicode replacement character.

    If set to `FALSE`, the load operation produces an error when invalid UTF-8 character encoding is detected.

    Default:
    :   `FALSE`

`EMPTY_FIELD_AS_NULL = TRUE | FALSE`
:   Use:
    :   Data loading, data unloading, and external tables

    Definition:
    :   - When loading data, specifies whether to insert SQL NULL for empty fields in an input file, which are represented by two successive delimiters (For example, `,,`).

          If set to `FALSE`, Snowflake attempts to cast an empty field to the corresponding column type. An empty string is inserted into columns of type STRING. For other column types, the COPY command produces an error.
        - When unloading data, this option is used in combination with `FIELD_OPTIONALLY_ENCLOSED_BY`. When `FIELD_OPTIONALLY_ENCLOSED_BY = NONE`, setting `EMPTY_FIELD_AS_NULL = FALSE` specifies to unload empty strings in tables to empty string values without quotes enclosing the field values.

          If set to `TRUE`, `FIELD_OPTIONALLY_ENCLOSED_BY` must specify a character to enclose strings.

    Default:
    :   `TRUE`

`SKIP_BYTE_ORDER_MARK = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether to skip the BOM (byte order mark), if present in a data file. A BOM is a character code at the beginning of a data file that defines the byte order and encoding form.

        If set to `FALSE`, Snowflake recognizes any BOM in data files, which could result in the BOM either causing an error or being merged into the first column in the table.

    Default:
    :   `TRUE`

`ENCODING = 'string'`
:   Use:
    :   Data loading and external tables

    Definition:
    :   String (constant) that specifies the character set of the source data when loading data into a table.

        | Character Set | `ENCODING` Value | Supported Languages | Notes |
        | --- | --- | --- | --- |
        | Big5 | `BIG5` | Traditional Chinese |  |
        | EUC-JP | `EUCJP` | Japanese |  |
        | EUC-KR | `EUCKR` | Korean |  |
        | GB18030 | `GB18030` | Chinese |  |
        | IBM420 | `IBM420` | Arabic |  |
        | IBM424 | `IBM424` | Hebrew |  |
        | IBM949 | `IBM949` | Korean |  |
        | ISO-2022-CN | `ISO2022CN` | Simplified Chinese |  |
        | ISO-2022-JP | `ISO2022JP` | Japanese |  |
        | ISO-2022-KR | `ISO2022KR` | Korean |  |
        | ISO-8859-1 | `ISO88591` | Danish, Dutch, English, French, German, Italian, Norwegian, Portuguese, Swedish |  |
        | ISO-8859-2 | `ISO88592` | Czech, Hungarian, Polish, Romanian |  |
        | ISO-8859-5 | `ISO88595` | Russian |  |
        | ISO-8859-6 | `ISO88596` | Arabic |  |
        | ISO-8859-7 | `ISO88597` | Greek |  |
        | ISO-8859-8 | `ISO88598` | Hebrew |  |
        | ISO-8859-9 | `ISO88599` | Turkish |  |
        | ISO-8859-15 | `ISO885915` | Danish, Dutch, English, French, German, Italian, Norwegian, Portuguese, Swedish | Identical to ISO-8859-1 except for 8 characters, including the Euro currency symbol. |
        | KOI8-R | `KOI8R` | Russian |  |
        | Shift\_JIS | `SHIFTJIS` | Japanese |  |
        | UTF-8 | `UTF8` | All languages | For loading data from delimited files (CSV, TSV, etc.), UTF-8 is the default.     For loading data from all other supported file formats (JSON, Avro, etc.), as well as unloading data, UTF-8 is the only supported character set. |
        | UTF-16 | `UTF16` | All languages |  |
        | UTF-16BE | `UTF16BE` | All languages |  |
        | UTF-16LE | `UTF16LE` | All languages |  |
        | UTF-32 | `UTF32` | All languages |  |
        | UTF-32BE | `UTF32BE` | All languages |  |
        | UTF-32LE | `UTF32LE` | All languages |  |
        | windows-874 | `WINDOWS874` | Thai |  |
        | windows-949 | `WINDOWS949` | Korean |  |
        | windows-1250 | `WINDOWS1250` | Czech, Hungarian, Polish, Romanian |  |
        | windows-1251 | `WINDOWS1251` | Russian |  |
        | windows-1252 | `WINDOWS1252` | Danish, Dutch, English, French, German, Italian, Norwegian, Portuguese, Swedish |  |
        | windows-1253 | `WINDOWS1253` | Greek |  |
        | windows-1254 | `WINDOWS1254` | Turkish |  |
        | windows-1255 | `WINDOWS1255` | Hebrew |  |
        | windows-1256 | `WINDOWS1256` | Arabic |  |

        Expand

        Show lessSee more

    Default:
    :   `UTF8`

    Note

    Snowflake stores all data internally in the UTF-8 character set. The data is converted into UTF-8 before it is loaded into Snowflake.

## TYPE = JSON

`COMPRESSION = AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE`
:   Use:
    :   Data loading and external tables

    Definition:
    :   - When loading data, specifies the current compression algorithm for the data file. Snowflake uses this option to detect how an already-compressed data file was compressed so that the compressed data in the file can be extracted for loading.
        - When unloading data, compresses the data file using the specified compression algorithm.

    Values:
    :   | Supported Values | Notes |
        | --- | --- |
        | `AUTO` | When loading data, compression algorithm detected automatically, except for Brotli-compressed files, which cannot currently be detected automatically. When unloading data, files are automatically compressed using the default, which is gzip. |
        | `GZIP` |  |
        | `BZ2` |  |
        | `BROTLI` | Must be specified if loading/unloading Brotli-compressed files. |
        | `ZSTD` | Zstandard v0.8 (and higher) is supported. |
        | `DEFLATE` | Deflate-compressed files (with zlib header, RFC1950). |
        | `RAW_DEFLATE` | Raw Deflate-compressed files (without header, RFC1951). |
        | `NONE` | When loading data, indicates that the files have not been compressed. When unloading data, specifies that the unloaded files are not compressed. |

        Expand

        Show lessSee more

    Default:
    :   `AUTO`

`DATE_FORMAT = 'string' | AUTO`
:   Use:
    :   Data loading only

    Definition:
    :   Defines the format of date string values in the data files. If a value is not specified or is `AUTO`, the value for the [DATE\_INPUT\_FORMAT](/sql-reference/parameters#label-date-input-format) parameter is used.

        This file format option is applied to the following actions only:

        - Loading JSON data into separate columns using the MATCH\_BY\_COLUMN\_NAME copy option.
        - Loading JSON data into separate columns by specifying a query in the COPY statement (i.e. COPY transformation).

    Default:
    :   `AUTO`

`TIME_FORMAT = 'string' | AUTO`
:   Use:
    :   Data loading only

    Definition:
    :   Defines the format of time string values in the data files. If a value is not specified or is `AUTO`, the value for the [TIME\_INPUT\_FORMAT](/sql-reference/parameters#label-time-input-format) parameter is used.

        This file format option is applied to the following actions only:

        - Loading JSON data into separate columns using the MATCH\_BY\_COLUMN\_NAME copy option.
        - Loading JSON data into separate columns by specifying a query in the COPY statement (i.e. COPY transformation).

    Default:
    :   `AUTO`

`TIMESTAMP_FORMAT = string' | AUTO`
:   Use:
    :   Data loading only

    Definition:
    :   Defines the format of timestamp string values in the data files. If a value is not specified or is `AUTO`, the value for the [TIMESTAMP\_INPUT\_FORMAT](/sql-reference/parameters#label-timestamp-input-format) parameter is used.

        This file format option is applied to the following actions only:

        - Loading JSON data into separate columns using the MATCH\_BY\_COLUMN\_NAME copy option.
        - Loading JSON data into separate columns by specifying a query in the COPY statement (i.e. COPY transformation).

    Default:
    :   `AUTO`

`BINARY_FORMAT = HEX | BASE64 | UTF8`
:   Use:
    :   Data loading only

    Definition:
    :   Defines the encoding format for binary string values in the data files. The option can be used when loading data into binary columns in a table.

        This file format option is applied to the following actions only:

        - Loading JSON data into separate columns using the MATCH\_BY\_COLUMN\_NAME copy option.
        - Loading JSON data into separate columns by specifying a query in the COPY statement (i.e. COPY transformation).

    Default:
    :   `HEX`

`TRIM_SPACE = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether to remove leading and trailing white space from strings.

        For example, if your external database software encloses fields in quotes, but inserts a leading space, Snowflake reads the leading space rather than the opening quotation character as the beginning of the
        field (i.e. the quotation marks are interpreted as part of the string of field data). Set this option to `TRUE` to remove undesirable spaces during the data load.

        This file format option is applied to the following actions only when loading JSON data into separate columns using the
        MATCH\_BY\_COLUMN\_NAME copy option.

    Default:
    :   `FALSE`

`MULTI_LINE = TRUE | FALSE`
:   Use: Data loading and external tables

    Definition:
    :   Boolean that specifies whether multiple lines are allowed. If MULTI\_LINE is set to `FALSE` and a new line is present within a JSON record, the record containing the new line will be interpreted as an error.

    Default:
    :   `TRUE`

`NULL_IF = ( 'string1' [ , 'string2' , ... ] )`
:   Use:
    :   Data loading only

    Definition:
    :   String used to convert to and from SQL NULL. Snowflake replaces these strings in the data load source with SQL NULL. To
        specify more than one string, enclose the list of strings in parentheses and use commas to separate each value.

        This file format option is applied to the following actions only when loading JSON data into separate columns using the
        MATCH\_BY\_COLUMN\_NAME copy option.

        Note that Snowflake converts all instances of the value to NULL, regardless of the data type. For example, if `2` is specified as a
        value, all instances of `2` as either a string or number are converted.

        For example:

        `NULL_IF = ('\N', 'NULL', 'NUL', '')`

        Note that this option can include empty strings.

    Default:
    :   `\N` (that is, NULL)

`FILE_EXTENSION = 'string' | NONE`
:   Use:
    :   Data unloading only

    Definition:
    :   Specifies the extension for files unloaded to a stage. Accepts any extension. The user is responsible for specifying a file extension that can be read by any desired software or services.

    Default:
    :   null, meaning the file extension is determined by the format type: `.json[compression]`, where `compression` is the extension added by the compression method, if `COMPRESSION` is set.

`ENABLE_OCTAL = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that enables parsing of octal numbers.

    Default:
    :   `FALSE`

`ALLOW_DUPLICATE = TRUE | FALSE`
:   Use:
    :   Data loading and external tables

    Definition:
    :   Boolean that specifies to allow duplicate object field names (only the last one will be preserved).

    Default:
    :   `FALSE`

`STRIP_OUTER_ARRAY = TRUE | FALSE`
:   Use:
    :   Data loading and external tables

    Definition:
    :   Boolean that instructs the JSON parser to remove outer brackets (i.e. `[ ]`).

    Default:
    :   `FALSE`

`STRIP_NULL_VALUES = TRUE | FALSE`
:   Use:
    :   Data loading and external tables

    Definition:
    :   Boolean that instructs the JSON parser to remove object fields or array elements containing `null` values. For example, when set to `TRUE`:

        | Before | After |
        | --- | --- |
        | `[null]` | `[]` |
        | `[null,null,3]` | `[,,3]` |
        | `{"a":null,"b":null,"c":123}` | `{"c":123}` |
        | `{"a":[1,null,2],"b":{"x":null,"y":88}}` | `{"a":[1,,2],"b":{"y":88}}` |

        Expand

        Show lessSee more

    Default:
    :   `FALSE`

`REPLACE_INVALID_CHARACTERS = TRUE | FALSE`
:   Use:
    :   Data loading and external table

    Definition:
    :   Boolean that specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (`�`). This
        option performs a one-to-one character replacement.

    Values:
    :   If set to `TRUE`, Snowflake replaces invalid UTF-8 characters with the Unicode replacement character.

        If set to `FALSE`, the load operation produces an error when invalid UTF-8 character encoding is detected.

    Default:
    :   `FALSE`

`IGNORE_UTF8_ERRORS = TRUE | FALSE`
:   Use:
    :   Data loading and external table

    Definition:
    :   Boolean that specifies whether UTF-8 encoding errors produce error conditions. It is an alternative syntax for `REPLACE_INVALID_CHARACTERS`.

    Values:
    :   If set to `TRUE`, any invalid UTF-8 sequences are silently replaced with the Unicode character `U+FFFD` (i.e. “replacement character”).

        If set to `FALSE`, the load operation produces an error when invalid UTF-8 character encoding is detected.

    Default:
    :   `FALSE`

`SKIP_BYTE_ORDER_MARK = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether to skip the BOM (byte order mark), if present in a data file. A BOM is a character code at the beginning of a data file that defines the byte order and encoding form.

        If set to `FALSE`, Snowflake recognizes any BOM in data files, which could result in the BOM either causing an error or being merged into the first column in the table.

    Default:
    :   `TRUE`

## TYPE = AVRO

`COMPRESSION = AUTO | GZIP | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE`
:   Use:
    :   Data loading only

    Definition:
    :   - When loading data, specifies the current compression algorithm for the data file. Snowflake uses this option to detect how an already-compressed data file was compressed so that the compressed data in the file can be extracted for loading.
        - When unloading data, compresses the data file using the specified compression algorithm.

    Values:
    :   | Supported Values | Notes |
        | --- | --- |
        | `AUTO` | When loading data, compression algorithm detected automatically, except for Brotli-compressed files, which cannot currently be detected automatically. When unloading data, files are automatically compressed using the default, which is gzip. |
        | `GZIP` |  |
        | `BROTLI` | Must be specified if loading/unloading Brotli-compressed files. |
        | `ZSTD` | Zstandard v0.8 (and higher) is supported. |
        | `DEFLATE` | Deflate-compressed files (with zlib header, RFC1950). |
        | `RAW_DEFLATE` | Raw Deflate-compressed files (without header, RFC1951). |
        | `NONE` | When loading data, indicates that the files have not been compressed. When unloading data, specifies that the unloaded files are not compressed. |

        Expand

        Show lessSee more

    Default:
    :   `AUTO`.

Note

We recommend that you use the default `AUTO` option because it will determine both the file and codec compression. Specifying a compression option refers to the compression of files, not the compression of blocks (codecs).

`TRIM_SPACE = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether to remove leading and trailing white space from strings.

        For example, if your external database software encloses fields in quotes, but inserts a leading space, Snowflake reads the leading space rather than the opening quotation character as the beginning of the
        field (i.e. the quotation marks are interpreted as part of the string of field data). Set this option to `TRUE` to remove undesirable spaces during the data load.

        This file format option is applied to the following actions only when loading Avro data into separate columns using the
        MATCH\_BY\_COLUMN\_NAME copy option.

    Default:
    :   `FALSE`

`REPLACE_INVALID_CHARACTERS = TRUE | FALSE`
:   Use:
    :   Data loading and external table

    Definition:
    :   Boolean that specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (`�`). This
        option performs a one-to-one character replacement.

    Values:
    :   If set to `TRUE`, Snowflake replaces invalid UTF-8 characters with the Unicode replacement character.

        If set to `FALSE`, the load operation produces an error when invalid UTF-8 character encoding is detected.

    Default:
    :   `FALSE`

`NULL_IF = ( 'string1' [ , 'string2' , ... ] )`
:   Use:
    :   Data loading only

    Definition:
    :   String used to convert to and from SQL NULL. Snowflake replaces these strings in the data load source with SQL NULL. To
        specify more than one string, enclose the list of strings in parentheses and use commas to separate each value.

        This file format option is applied to the following actions only when loading Avro data into separate columns using the
        MATCH\_BY\_COLUMN\_NAME copy option.

        Note that Snowflake converts all instances of the value to NULL, regardless of the data type. For example, if `2` is specified as a
        value, all instances of `2` as either a string or number are converted.

        For example:

        `NULL_IF = ('\N', 'NULL', 'NUL', '')`

        Note that this option can include empty strings.

    Default:
    :   `\N` (that is, NULL)

## TYPE = ORC

`TRIM_SPACE = TRUE | FALSE`
:   Use:
    :   Data loading and external tables

    Definition:
    :   Boolean that specifies whether to remove leading and trailing white space from strings.

        For example, if your external database software encloses fields in quotes, but inserts a leading space, Snowflake reads the leading space rather than the opening quotation character as the beginning of the
        field (i.e. the quotation marks are interpreted as part of the string of field data). Set this option to `TRUE` to remove undesirable spaces during the data load.

        This file format option is applied to the following actions only when loading Orc data into separate columns using the
        MATCH\_BY\_COLUMN\_NAME copy option.

    Default:
    :   `FALSE`

`REPLACE_INVALID_CHARACTERS = TRUE | FALSE`
:   Use:
    :   Data loading and external table

    Definition:
    :   Boolean that specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (`�`). This
        option performs a one-to-one character replacement.

    Values:
    :   If set to `TRUE`, Snowflake replaces invalid UTF-8 characters with the Unicode replacement character.

        If set to `FALSE`, the load operation produces an error when invalid UTF-8 character encoding is detected.

    Default:
    :   `FALSE`

`NULL_IF = ( 'string1' [ , 'string2' , ... ] )`
:   Use:
    :   Data loading and external tables

    Definition:
    :   String used to convert to and from SQL NULL. Snowflake replaces these strings in the data load source with SQL NULL. To
        specify more than one string, enclose the list of strings in parentheses and use commas to separate each value.

        This file format option is applied to the following actions only when loading Orc data into separate columns using the
        MATCH\_BY\_COLUMN\_NAME copy option.

        Note that Snowflake converts all instances of the value to NULL, regardless of the data type. For example, if `2` is specified as a
        value, all instances of `2` as either a string or number are converted.

        For example:

        `NULL_IF = ('\N', 'NULL', 'NUL', '')`

        Note that this option can include empty strings.

    Default:
    :   `\N` (that is, NULL)

## TYPE = PARQUET

`COMPRESSION = AUTO | LZO | SNAPPY | NONE`
:   Use:
    :   Data unloading and external tables

    Definition:

    - When unloading data, specifies the compression algorith for columns in the Parquet files.

    Values:
    :   | Supported Values | Notes |
        | --- | --- |
        | `AUTO` | When loading data, compression algorithm detected automatically. Supports the following compression algorithms: Brotli, gzip, Lempel-Ziv-Oberhumer (LZO), LZ4, Snappy, or Zstandard v0.8 (and higher).    When unloading data, unloaded files are compressed using the [Snappy](https://google.github.io/snappy/) compression algorithm by default. |
        | `LZO` | When unloading data, files are compressed using the Snappy algorithm by default. If unloading data to LZO-compressed files, specify this value. |
        | `SNAPPY` | When unloading data, files are compressed using the Snappy algorithm by default. You can optionally specify this value. |
        | `NONE` | When loading data, indicates that the files have not been compressed. When unloading data, specifies that the unloaded files are not compressed. |

        Expand

        Show lessSee more

    Default:
    :   `AUTO`

`SNAPPY_COMPRESSION = TRUE | FALSE`
:   Use:
    :   Data unloading only

        | Supported Values | Notes |
        | --- | --- |
        | `AUTO` | Unloaded files are compressed using the [Snappy](https://google.github.io/snappy/) compression algorithm by default. |
        | `SNAPPY` | May be specified if unloading Snappy-compressed files. |
        | `NONE` | When loading data, indicates that the files have not been compressed. When unloading data, specifies that the unloaded files are not compressed. |

        Expand

        Show lessSee more

    Definition:
    :   Boolean that specifies whether unloaded file(s) are compressed using the SNAPPY algorithm.

    Note

    Deprecated. Use `COMPRESSION = SNAPPY` instead.

    Limitations:
    :   Only supported for data unloading operations.

    Default:
    :   `TRUE`

`BINARY_AS_TEXT = TRUE | FALSE`
:   Use:
    :   Data loading and external tables

    Definition:
    :   Boolean that specifies whether to interpret columns with no defined logical data type as UTF-8 text. When set to `FALSE`, Snowflake interprets these columns as binary data.

    Default:
    :   `TRUE`

    Note

    Snowflake recommends that you set BINARY\_AS\_TEXT to FALSE to avoid any potential conversion issues.

`TRIM_SPACE = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether to remove leading and trailing white space from strings.

        For example, if your external database software encloses fields in quotes, but inserts a leading space, Snowflake reads the leading space rather than the opening quotation character as the beginning of the
        field (i.e. the quotation marks are interpreted as part of the string of field data). Set this option to `TRUE` to remove undesirable spaces during the data load.

        This file format option is applied to the following actions only when loading Parquet data into separate columns using the
        MATCH\_BY\_COLUMN\_NAME copy option.

    Default:
    :   `FALSE`

`USE_LOGICAL_TYPE = TRUE | FALSE`
:   Use:
    :   Data loading, data querying in staged files, and schema detection.

    Definition:
    :   Boolean that specifies whether to use Parquet logical types. With this file format option, Snowflake can interpret Parquet logical types during data loading. For more information, see [Parquet Logical Type Definitions](https://github.com/apache/parquet-format/blob/master/LogicalTypes.md). To enable Parquet logical types, set USE\_LOGICAL\_TYPE as TRUE when you create a new file format option.

    Limitations:
    :   Not supported for data unloading.

`USE_VECTORIZED_SCANNER = TRUE | FALSE`
:   Use:
    :   Data loading and data querying in staged files

    Definition:
    :   Boolean that specifies whether to use a vectorized scanner for loading Parquet files.

    Default:
    :   `FALSE`. In a future BCR, the default value will be `TRUE`.

    Using the vectorized scanner can significantly reduce the latency for loading Parquet files, because this scanner is well suited for the columnar format of a [Parquet](https://parquet.apache.org/docs/file-format/) file. The scanner only downloads relevant sections of the Parquet file into memory, such as the subset of selected columns.

    If `USE_VECTORIZED_SCANNER` is set to `TRUE`, the vectorized scanner has the following behaviors:

    > - The `BINARY_AS_TEXT` option is always treated as `FALSE` and the `USE_LOGICAL_TYPE` option is always treated as `TRUE`, no matter what the actual value is being set to.
    > - The vectorized scanner supports Parquet map types. The output of scanning a map type is as follows:
    >
    > > Copy code
    > >
    > > ```
    > > "my_map":
    > >   {
    > > "k1": "v1",
    > > "k2": "v2"
    > >   }
    > > ```
    >
    > - The vectorized scanner shows `NULL` values in the output, as the following example demonstrates:
    >
    > > Copy code
    > >
    > > ```
    > > "person":
    > >  {
    > >   "name": "Adam",
    > >   "nickname": null,
    > >   "age": 34,
    > >   "phone_numbers":
    > >   [
    > >  "1234567890",
    > >  "0987654321",
    > >  null,
    > >  "6781234590"
    > >   ]
    > >   }
    > > ```
    >
    > - The vectorized scanner handles Time and Timestamp as follows:
    >
    > > | Parquet | Snowflake vectorized scanner |
    > > | --- | --- |
    > > | TimeType(isAdjustedToUtc=True/False, unit=MILLIS/MICROS/NANOS) | TIME |
    > > | TimestampType(isAdjustedToUtc=True, unit=MILLIS/MICROS/NANOS) | TIMESTAMP\_LTZ |
    > > | TimestampType(isAdjustedToUtc=False, unit=MILLIS/MICROS/NANOS) | TIMESTAMP\_NTZ |
    > > | INT96 | TIMESTAMP\_LTZ |
    > >
    > > Expand
    > >
    > > Show lessSee more

    If `USE_VECTORIZED_SCANNER` is set to `FALSE`, the scanner has the following behaviors:

    > - This option does not support Parquet maps. The output of scanning a map type is as follows:
    >
    > > Copy code
    > >
    > > ```
    > > "my_map":
    > >  {
    > >   "key_value":
    > >   [
    > > {
    > >        "key": "k1",
    > >        "value": "v1"
    > >    },
    > >    {
    > >        "key": "k2",
    > >        "value": "v2"
    > >    }
    > >  ]
    > >   }
    > > ```
    >
    > - This option does not explicitly show `NULL` values in the scan output, as the following example demonstrates:
    >
    > > Copy code
    > >
    > > ```
    > > "person":
    > >  {
    > >   "name": "Adam",
    > >   "age": 34
    > >   "phone_numbers":
    > >   [
    > > "1234567890",
    > > "0987654321",
    > > "6781234590"
    > >   ]
    > >  }
    > > ```
    >
    > - This option handles Time and Timestamp as follows:
    >
    > > | Parquet | When USE\_LOGICAL\_TYPE = TRUE | When USE\_LOGICAL\_TYPE = FALSE |
    > > | --- | --- | --- |
    > > | TimeType(isAdjustedToUtc=True/False, unit=MILLIS/MICROS) | TIME | - TIME (If ConvertedType present) - INTEGER (If ConvertedType not present) |
    > > | TimeType(isAdjustedToUtc=True/False, unit=NANOS) | TIME | INTEGER |
    > > | TimestampType(isAdjustedToUtc=True, unit=MILLIS/MICROS) | TIMESTAMP\_LTZ | TIMESTAMP\_NTZ |
    > > | TimestampType(isAdjustedToUtc=True, unit=NANOS) | TIMESTAMP\_LTZ | INTEGER |
    > > | TimestampType(isAdjustedToUtc=False, unit=MILLIS/MICROS) | TIMESTAMP\_NTZ | - TIMESTAMP\_LTZ (If ConvertedType present) - INTEGER (If ConvertedType not present) |
    > > | TimestampType(isAdjustedToUtc=False, unit=NANOS) | TIMESTAMP\_NTZ | INTEGER |
    > > | INT96 | TIMESTAMP\_NTZ | TIMESTAMP\_NTZ |
    > >
    > > Expand
    > >
    > > Show lessSee more

`REPLACE_INVALID_CHARACTERS = TRUE | FALSE`
:   Use:
    :   Data loading and external table

    Definition:
    :   Boolean that specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (`�`). This
        option performs a one-to-one character replacement.

    Values:
    :   If set to `TRUE`, Snowflake replaces invalid UTF-8 characters with the Unicode replacement character.

        If set to `FALSE`, the load operation produces an error when invalid UTF-8 character encoding is detected.

    Default:
    :   `FALSE`

`NULL_IF = ( 'string1' [ , 'string2' , ... ] )`
:   Use:
    :   Data loading only

    Definition:
    :   String used to convert to and from SQL NULL. Snowflake replaces these strings in the data load source with SQL NULL. To
        specify more than one string, enclose the list of strings in parentheses and use commas to separate each value.

        This file format option is applied to the following actions only when loading Parquet data into separate columns using the
        MATCH\_BY\_COLUMN\_NAME copy option.

        Note that Snowflake converts all instances of the value to NULL, regardless of the data type. For example, if `2` is specified as a
        value, all instances of `2` as either a string or number are converted.

        For example:

        `NULL_IF = ('\N', 'NULL', 'NUL', '')`

        Note that this option can include empty strings.

    Default:
    :   `\N` (that is, NULL)

## TYPE = XML

`COMPRESSION = AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE`
:   Use:
    :   Data loading only

    Definition:
    :   - When loading data, specifies the current compression algorithm for the data file. Snowflake uses this option to detect how an already-compressed data file was compressed so that the compressed data in the file can be extracted for loading.
        - When unloading data, compresses the data file using the specified compression algorithm.

    Values:
    :   | Supported Values | Notes |
        | --- | --- |
        | `AUTO` | When loading data, compression algorithm detected automatically, except for Brotli-compressed files, which cannot currently be detected automatically. When unloading data, files are automatically compressed using the default, which is gzip. |
        | `GZIP` |  |
        | `BZ2` |  |
        | `BROTLI` | Must be specified if loading/unloading Brotli-compressed files. |
        | `ZSTD` | Zstandard v0.8 (and higher) is supported. |
        | `DEFLATE` | Deflate-compressed files (with zlib header, RFC1950). |
        | `RAW_DEFLATE` | Raw Deflate-compressed files (without header, RFC1951). |
        | `NONE` | When loading data, indicates that the files have not been compressed. When unloading data, specifies that the unloaded files are not compressed. |

        Expand

        Show lessSee more

    Default:
    :   `AUTO`

`IGNORE_UTF8_ERRORS = TRUE | FALSE`
:   Use:
    :   Data loading and external table

    Definition:
    :   Boolean that specifies whether UTF-8 encoding errors produce error conditions. It is an alternative syntax for `REPLACE_INVALID_CHARACTERS`.

    Values:
    :   If set to `TRUE`, any invalid UTF-8 sequences are silently replaced with the Unicode character `U+FFFD` (i.e. “replacement character”).

        If set to `FALSE`, the load operation produces an error when invalid UTF-8 character encoding is detected.

    Default:
    :   `FALSE`

`PRESERVE_SPACE = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether the XML parser preserves leading and trailing spaces in element content.

    Default:
    :   `FALSE`

`STRIP_OUTER_ELEMENT = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether the XML parser strips out the outer XML element, exposing 2nd level elements as separate documents.

    Default:
    :   `FALSE`

`DISABLE_AUTO_CONVERT = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether the XML parser disables automatic conversion of numeric and Boolean values from text to native representation.

    Default:
    :   `FALSE`

`REPLACE_INVALID_CHARACTERS = TRUE | FALSE`
:   Use:
    :   Data loading and external table

    Definition:
    :   Boolean that specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (`�`). This
        option performs a one-to-one character replacement.

    Values:
    :   If set to `TRUE`, Snowflake replaces invalid UTF-8 characters with the Unicode replacement character.

        If set to `FALSE`, the load operation produces an error when invalid UTF-8 character encoding is detected.

    Default:
    :   `FALSE`

`SKIP_BYTE_ORDER_MARK = TRUE | FALSE`
:   Use:
    :   Data loading only

    Definition:
    :   Boolean that specifies whether to skip any BOM (byte order mark) present in an input file. A BOM is a character code at the beginning of a data file that defines the byte order and encoding form.

        If set to `FALSE`, Snowflake recognizes any BOM in data files, which could result in the BOM either causing an error or being merged into the first column in the table.

    Default:
    :   `TRUE`

## Usage notes

- ALTER FILE FORMAT does not support the following actions:

  - Changing the type (CSV, JSON, etc.) for the file format.
  - Unsetting any format options (i.e. resetting the options to the defaults for the type).
  - Unsetting (i.e. removing) a comment.

  To make any of these changes, you must recreate the file format.

## Examples

Rename file format `my_format` to `my_new_format`:

> Copy code
>
> ```
> ALTER FILE FORMAT IF EXISTS my_format RENAME TO my_new_format;
> ```

Specify comma (`,`) as the field delimiter for `my_format` (created in the [CREATE FILE FORMAT](/sql-reference/sql/create-file-format) examples):

> Copy code
>
> ```
> ALTER FILE FORMAT my_format SET FIELD_DELIMITER=',';
> ```
