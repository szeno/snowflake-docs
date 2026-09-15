# SnowConvert AI - SQL Conversion Summary

## Code Conversion Rate

Note

This field applies to Oracle and SQLServer

The conversion rate is the percentage of the total source code that was successfully converted by SnowConvert AI into functionally equivalent Snowflake code. Every time that SnowConvert AI identifies not supported elements, *i.e,* fragments in the input source code that were not converted into Snowflake, this will affect the conversion rate. You can read more about the different conversion rate modes and how they are calculated by SnowConvert AI [here](../assessment-report/README#conversion-rate-modes).

### CSV Associated Field Names

Note

The CSV field associated is going to depend on the conversion rate mode used.

- **Code Conversion Rate:**
  - SqlLoCConversionRate
  - SqlCharacterConversionRate

## Lines of Code

Note

This field applies only to Teradata reports.

Represents the number of lines of code found in the SQL files. This counting includes comments but does not include empty lines or lines with only whitespaces unless they are inside block comments or strings. Lines of code that were not recognized are counted as well.

### Samples

Copy code

```
SELECT 123 FROM my_table;
```

**Expected Lines of Code:** 1

Copy code

```
SELECT 123
FROM my_table;
```

**Expected lines of code:** 2

Copy code

```
SELECT 123
FROM my_table;

Unrecognized statement
```

**Expected lines of code:** 3

Copy code

```
SELECT '123

abc' FROM my_table;
```

**Expected lines of code: 3**

**Explanation:** In this case, we have an empty line inside a string. Since this is part of the selected string, is considered part of the code and is counted as a line of code.

Copy code

```
invalid '

' code
```

**Expected lines of code: 3**

**Explanation:** In this case, even if the code was not recognized, there was still a string containing the empty line. Such cases will count the empty line of code as well.

Copy code

```
-- Hello world
```

**Expected Lines of Code:** 1

Copy code

```
/* hello

world */
```

**Expected Lines of Code:** 3

**Explanation:** In this case, the second line is part of the block comment in the example, so this is counted as one line of code as well.

#### CSV Associated Field Names

- SqlLinesOfCode

## LOC Conversion Percentage

Note

This field applies only to Teradata reports.

This is the percentage of fully converted lines divided by the total lines of code. Unrecognized Lines of code count as not converted. Comments count as converted.

Elements that contain an EWI with medium severity or higher will count as not converted. These elements may include more than one line depending on how the input code was formatted.

### Formula

Copy code

```
sql_converted_lines_of_code / sql_total_lines_of_code
```

#### Samples

Copy code

```
CREATE TABLE t1
(
col1 INTEGER
);
```

**Expected LOC Conversion Percentage:** 100%

**Explanation:** The entire table is supported. Because of this, the conversion rate is 100%.

Copy code

```
CREATE TABLE t1
(
NOT A VALID ELEMENT
);
```

**Expected LOC Conversion Percentage:** 75%

**Explanation:** In this case, the third line is unrecognized. The other 3 lines are identified and converted properly, causing a conversion rate of 75%.

Copy code

```
CREATE TABLE t1 (
NOT A VALID ELEMENT );
```

**Expected LOC Conversion Percentage:** 50%

**Explanation:** Even though this is the same code as Sample 2, the format of the code is different. In this case, the first line is considered converted, and the second line has an unrecognized part, causing the line to be counted as not supported. Because of this, the conversion rate is 50%.

Copy code

```
CREATE TABLE t1 (
  col1 INTEGER
);

SELECT CAST (123 AS INTERVAL DAY(4));
```

**Expected LOC Conversion Percentage:** 75%

**Explanation:** In this case, the 3 lines of the `CREATE TABLE` are supported, but the `SELECT` has a `CAST` to `INTERVAL` which is not supported, causing line 5 to be counted as unsupported.

Copy code

```
-- Hello world
Unrecognized statement
```

**Expected LOC Conversion Percentage:** 50%

**Explanation:** In this case, the first line comment is considered as converted and the second line, an unrecognized element, is not supported, causing a 50% conversion rate.

#### CSV Associated Field Names

- SqlLoCConversionRate

## Unrecognized Lines of Code

Note

This field applies only to Teradata reports.

This is the number of lines of code that had an element that was not recognized.

Copy code

```
Unrecognized Element
```

**Unrecognized Lines of Code:** 1

Copy code

```
invalid '

' something
```

**Unrecognized Lines of Code:** 3

**Explanation:** In this case, there is a string that starts at line 1 and ends at line 3. However, the entire block of code was not recognized, causing the 3 lines to be counted as unrecognized lines of code.

### CSV Associated Field Names

- SqlUnrecognizedElementsLOC
