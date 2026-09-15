# SnowConvert AI - Assessment Report

## General Summary

The purpose of this document is to provide guidance for users to understand the summary results from the SnowConvert AI conversion tools. It will guide through the different metrics returned and how these metrics can be used to determine the automation level achieved, and the amount of manual effort needed to make the output code into functionally equivalent Snowflake code.

[![image](/static/images/migrations/sc-assets/image(210).png "image")](/static/images/migrations/sc-assets/image(210).png)

Most of the concepts presented in this document are already explained on the Report’s main page. But here is some other helpful information about the most important information of the image above.

- **Total Parsing Errors**: The number of times that the conversion tool found text fragments that could not be recognized as syntactically correct elements for the source language under conversion. A parsing error could have a little or large impact. It is important to determine the number of LOC affected by parsing errors and how much they represent of the total workload. Sometimes parsing errors can occur due to encoding issues or because the workload needs some preparation.
- **Code Conversion Rate**: The conversion rate is the percentage of the total source code that was successfully converted by SnowConvert AI into functionally equivalent Snowflake code. Every time that the tool identifies not supported elements, *i.e,* fragments in the input source code that were not converted into Snowflake, this will affect the conversion rate.
- **Identified Objects**: The count of all the Top Level DDL Objects ( Table, View, Procedure, etc.. ) that the SnowConvert AI identified. If there were a parsing error on an object, it wouldn’t be an Identified Object.   
  Example: The [first objects](../../../../../technical-documentation/issues-and-troubleshooting/functional-difference/README) from line #1 to line #6. There is evidently a parsing error, so the SnowConvert AI cannot identify that as an object.

### Conversion rate modes

As mentioned before, when an element is marked as not supported (due to parsing errors or because there is no support for it in Snowflake) the conversion rate will be punished. How much of the conversion rate is punished for each not-supported element depends on the unit of code selected, two units are available: characters or lines.

#### Conversion rate using code characters

When characters of code are selected, the total amount of characters in the input source will represent the overall units to convert. So, if there are 100 characters total and there is only one not-supported element with 10 characters, the conversion rate will be **90%**. The conversion rate using characters is more precise because only the characters belonging to the not-supported elements are punished but, it is harder to manually calculate and understand.

#### Conversion rate using lines of code

When lines of code are chosen (default option), the number of lines of code in the input source code will represent the overall units to convert, and lines containing not-supported elements will be **entirely** considered as not-supported units of code. So, if the same input code with those 100 characters is split into 5 lines of code, and the not-supported element is in just one line, then the conversion rate will be **80%**; the **entire line** containing the not-supported element is considered not supported as well. The conversion rate using lines is easier to follow however, it is less accurate because entire lines of code containing not-supported elements are punished (even if there are other supported elements in that same line).

The next example shows how the conversion rate is calculated using both metrics.

### Conversion rate example

**Input source code**

Copy code

```
--Comment123
CREATE TABLE Table1(
 Prefix_Employee_Name CHAR(25),
 !ERROR_Col,
 Prefix_Employee_Sal DECIMAL(8))
```

The above code has exactly 100 code characters because whitespaces and line breaks are not considered code characters. The comment above `Table1` belongs to the table and is part of those 100 characters. This is the output code that SnowConvert AI generates for this input.

**Output source code**

Copy code

```
--Comment123
CREATE OR REPLACE TABLE Table1 (
 Prefix_Employee_Name CHAR(25)
--                              ,
-- ** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON LINE '4' COLUMN '2' OF THE SOURCE CODE STARTING AT '!'. EXPECTED 'Column Definition' GRAMMAR. LAST MATCHING TOKEN WAS ',' ON LINE '3' COLUMN '31'. FAILED TOKEN WAS '!' ON LINE '4' COLUMN '2'. CODE '15'. **
-- !ERROR_Col
           ,
 Prefix_Employee_Sal DECIMAL(8))
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"teradata"}}'
;
```

The second column of the table has a parsing error and therefore this is a not-supported element. Let’s take a look a how the conversion rate is punished using the two units available.

#### Conversion rate using code characters

Here is the breakdown of the characters in the input code

Copy code

```
--Comment123 /*12 code characters*/
CREATE TABLE Table1( /*18 code characters*/
 Prefix_Employee_Name CHAR(25), /*29 code characters*/
 !ERROR_Col, /*11 code characters*/
 Prefix_Employee_Sal DECIMAL(8)) /*30 code characters*/
```

- Total amount of code characters: 100
- Code characters in not-supported elements: 10
- **Result: 90.00%**

Note

Notice there are 11 characters in the 4th line but only 10 are marked as not supported. This is because of how the parsing recovery mechanism works. When the parser encounters an error, it will consider all the following characters, until the next delimiter character, in this case the comma (‘,’), as part of the error. That means that the amount of not-supported characters in any input code can greatly depend on the type of parsing errors. In some cases, the parser will be able to recover close to where the actual error is, but sadly in other cases, a lot of code can be swallowed by the error.

#### Conversion rate using lines of code

The conversion rate using lines of code as units is much simpler to calculate.

- Total amount of lines of code: 5
- Lines of code with not-supported elements: 1
- **Result: 80%**

#### LOC conversion rate depends on how the code is formatted

When using lines of code as the unit, the conversion rate will greatly depend on how the input code is formatted. For example, the following two code samples are equivalent but in the first case all the code is put into the same line and in the second case the code is split into 5 lines of code

Copy code

```
SELECT col1, !error_col FROM table1;
```
```
SELECT
   col1,
   !error_col
 FROM
    table1;
```

Notice that the second column that is being referenced in the SELECT has an error because it starts with an invalid character. In the first case, since the whole code is in the same line, the conversion rate will be 0%. But in the second case, since the code is split, only one line of code is punished and therefore the conversion rate will be 80%.

### Conversion rate differences

Conversion results of a migration may differ depending on the operating system.

This occurs because most of the time, Microsoft Windows uses CRLF line-breaking in their files. This format uses the characters `\r\n`, but UNIX OS only `\n`(LF).   
Due to that format difference, when our code processor is reading the input files, it will count the CRLF format as two characters and just one in LF files. These counting differences generate different results in the conversion rates, specifically, in string expressions present in your code.

To avoid this problem, you can use Visual Studio Code or similar tools to change the line-breaking format.

## File and Object-Level Breakdown

### SQL - Files

| File | Conversion Rate | Lines of Code | Total Object Quantity | Parsing Errors |
| --- | --- | --- | --- | --- |
| SQL | 42% | 20 | 2 | 3 |

Expand

Show lessSee more

In this section, you’ll get the overall assessment summary information for all the SQL Files

- **Code Conversion Rate**: This is an estimation of the conversion rate based on the characters of the given SQL Files.
- **Line of Code**: The count for the lines of code of the given SQL Files.
- **Total Object Quantity**: The count of total identified objects of the given SQL Files.
- **Parsing Errors**: The count of total parsing errors of the given SQL Files.

Warning

The Unrecognized objects will be counted also a parsing errors of the SQL Files section

Warning

The Code conversion rate may differ from Identified conversion rate because this is also considering the unrecognized objects.

### SQL - Identified Objects

| Object | Conversion Rate | Lines of Code | Total Object Quantity | Parsing Errors |
| --- | --- | --- | --- | --- |
| Tables | 67% | 5 | 1 | 1 |
| Views | 57% | 7 | 1 | 1 |
| Procedures | - | 0 | 0 | 0 |
| Functions | N/A | N/A | N/A | N/A |

Expand

Show lessSee more

Note

If N/A is listed in the table above, it means that the object type is not supported in Snowflake, most likely due to architectural reasons. These objects are commented out in the generated code, and they do not punish the conversion rate.

Note

If the Conversion Rate field has a “-”, it means that the current set of files you have migrated didn’t contain any instance of the specified object.

In this section, you’ll get the assessment information for all the identified objects divided by the DDL objects like Tables, Views, Procedures, etc.

Warning

If there is a code where the parser couldn’t handle it, the entire object will be accounted as *Unrecognized Object,* and therefore it wouldn’t show here

- **Code Conversion Rate**: This is an estimation of the conversion rate based on the characters for the identified objects like Table, View, Procedure, etc.
- **Line of Code**: The count for the lines of code of each type of identified object.
- **Total Object Quantity**: The count for each type of identified object.
- **Parsing Errors**: The count for the parsing errors that occurred inside each type of identified object.

Example: For the 2 tables that we have in the [source code](../../../../../technical-documentation/issues-and-troubleshooting/functional-difference/README), one is an unrecognized object and one is successfully identified. The conversion rate of that table of 5 lines of code is 75% due to 1 parsing error.

## Issues Breakdown

[![Issues Breakdown table](/static/images/migrations/sc-assets/image(291).png)](/static/images/migrations/sc-assets/image(291).png)

In this page, you will get the number of unique issues and the list of issues ordered by severity in descending sort.‌

For example, for the given source code, we have 2 critical issues related to parsing errors and one medium severity issue related to the *Not supported function.*

Note

Only errors with Medium/High/Critical severity will affect the current conversion rate. Warnings are just informative.
