# SnowConvert AI - Elements Report

## What is an “element”?

The term “element” is used in this context to address a grammar element; that is, an element from a grammar that has a name, a syntax and a purpose within a specific language.

Usually, these elements are highlighted and quite important within the documentation of a language.

These are some examples of elements in SQL languages:

- Any DDL, such as `CREATE TABLE` and `CREATE VIEW`
- Important content of DML, such as `PARTITION BY` and `NOT NULL`
- Any DML, like `INSERT` and `DELETE`
- Some important expressions, such as `IN`, `NOT IN`, `BETWEEN` and `LIKE`
- Operators, including conditionals and arithmetic operators
- Some internal parts of queries, such as `ORDER BY`, `WHEN`, `INNER JOIN` and `TOP`.
- Important functions, such as `AVG` and `RANK`

Essentially, anything that is worth keeping track of for assessment purposes can be considered an element.

### Where can I find it?

The elements report can be found in a folder named *“reports”*, in the output folder of your conversion. The name of the file itself starts with *“Elements”* so it can easily be located.

The format of the file is **.CSV**.

### What information does it contain?

The elements report is presented in a table format, and contains the following columns:

| Column | Description |
| --- | --- |
| SessionID | The session ID of the transformation. This is a unique identifier for the transformation session. |
| Category | The element’s corresponding category. These can be DDL, DDL Content, DML, Functions & Expressions, Statement, Query, and so on. |
| Grammar Element | The name associated to the element, often the same as found in the official documentation for the language. |
| File Type | The type of the file that contains the element. For example: SQL. |
| Total Count | The total count of that particular element found during the transformation process. |
| Not Converted Count (Self) | The count of that particular element that presented issues severe enough for it to not properly transform. Usually unsupported structures or elements that had a particular transformation error.   Keep in mind that “Self” means that some of the inner contents of the element may or may not be not converted, but if the element itself did not present errors, it will not be counted towards this column. |
| Language | The programming language or SQL dialect of the source code unit. |

#### Summarization

Each individual element is summarized using a specific criteria, that may include multiple columns to form a “composite key”. The basic grouping is made using the Category, Grammar Element and File Type columns.

Following this convention, the same `SELECT` element could be summarized differently depending on the type of the file that contains it, or two elements that share the same grammar element (or name) may still be summarized independently if their category is different.
