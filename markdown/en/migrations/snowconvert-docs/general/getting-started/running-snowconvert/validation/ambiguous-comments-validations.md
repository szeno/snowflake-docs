# SnowConvert AI - Ambiguous Comments Validation

## Description

This validation step verifies if the entry code has a sequence of characters that may create ambiguous comments (`/*/`)

If the entry code has an ambiguous comment, the following warning is displayed:

[![Ambiguous Comment Validation Failed](/static/images/migrations/sc-assets/image(449).png "image")](/static/images/migrations/sc-assets/image(449).png)

Also, in the ScopeValidation report, you will find information about the failed file(s).

[![ScopeValidation.csv](/static/images/migrations/sc-assets/image(450).png "image")](/static/images/migrations/sc-assets/image(450).png)

### Why is it ambiguous?

Block comments on SQL start with `/*` and end with `*/` . When the character sequence `/*/` is used, depending on the source language, it can start a nesting inside the block comment, or finish the whole block.

Here is an example of valid statements using `/*/`

Copy code

```
select col1,
  /*Some comment/*/ */*/
  col2,
  col3
from
  table1;
```

Copy code

```
select col1,
  /*Some comment/*/
  col2,
  col3
from
  table1;
```

Copy code

```
select col1,
  /*Some comment/*/ */*/
  col2,
  col3
from
  table1;
```

Copy code

```
select col1,
  /*Some comment/*/
  col2,
  col3
from
  table1;
```

As you can see, the comment behaves differently in Teradata and SQL Server than in Oracle and Snowflake. Even on Teradata, there is another treatment for bteq and other scripting languages.

### Solving the ambiguity

In Snowflake, if you encounter the /\*/ sequence in your code, it typically ends a block comment. However, if you’re using it differently in your source code, make sure to adjust it accordingly.
