# Working with privacy domains as an administrator

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

A *privacy domain* defines the possible values in a column, similar to a mathematical domain. Snowflake uses a privacy domain to determine
how much noise to introduce into results.

To gain a complete understanding of privacy domains before completing the tasks in this section, see [About privacy domains](/user-guide/diff-privacy/differential-privacy-privacy-domains).

It is best practice for a data provider to set a privacy domain for all numerical and categorical columns that an analyst might want to act
upon *before* distributing data to them.

## Choosing a privacy domain

A privacy domain defines *possible* values in a column, not necessarily *actual* values. You can narrow or expand a privacy domain as needed
so that it doesn’t contain actual values. For example, you can do either of the following:

- Define a broader list to obscure exact values. Because an analyst can view the privacy domain, you might not want to expose the exact
  contents of a column. For example, suppose a column contains a subset of zip codes. You might want to expand the privacy domain to include
  all possible zip codes, thereby obscuring whether a particular zip code is in the dataset.
- Define a narrower range to obscure the presence of an outlier value. For example, if most values are between 1 and 50, you might not want a
  value of 100 to be included in an average because the analyst could deduce the presence of 100 because the average is unusually high.

For information about how values outside a privacy domain are treated, see [Values outside a privacy domain](/user-guide/diff-privacy/differential-privacy-privacy-domains#label-diff-privacy-privacy-domains-excluded-values).

Important

Anyone with privileges to query a privacy-protected table has the ability to view the privacy domain for a column in that table, so
choose your privacy domains carefully.

While most fields should have a privacy domain, there are important exceptions. For example, unique identifier fields like user ID, email,
credit card numbers, and Social Security numbers should *not* have a privacy domain. Users can see the exact privacy domain, and you
usually don’t want an analyst to know whether a particular identifier exists in the dataset.

In contrast, privacy domains should contain the actual values for identifier fields when they’re not unique to an individual entity and
whose possible values are publicly known, such as zip codes, ICD codes in healthcare data, and NAICS codes.

## Setting a privacy domain

You define a privacy domain as either a range of values with a minimum and maximum or as an enumerated list of values. In general, the type
of privacy domain is based on the data type of the column. You cannot set a privacy domain on a column if its data type is not in the
following list.

| Data type | Privacy domain type |
| --- | --- |
| [Numeric](/sql-reference/data-types-numeric)  [Date & time](/sql-reference/data-types-datetime) | Range |
| [Strings](/sql-reference/data-types-text#label-character-datatypes) | Enumerated list |

Expand

Show lessSee more

To set, alter, or drop a privacy domain, you need the OWNERSHIP privilege on a table. You can set a privacy domain
when doing the following:

- [Creating a table](#label-diff-privacy-admin-domain-create-table).
- [Adding a new column](#label-diff-privacy-admin-domain-add-column) to an existing table.
- [Modifying an existing column](#label-diff-privacy-admin-domain-modify-column) of a table. If the existing column already has a
  privacy domain, the new domain replaces the old one.

For each of these methods, the syntax of the new privacy domain is the same.

Note

When a table is dropped, its privacy domains are also be dropped. This applies to a CREATE OR REPLACE command as well.

### Privacy domain syntax

The syntax of creating a privacy domain is:

Copy code

```
PRIVACY DOMAIN
  {
      [ BETWEEN ( <lo_value>, <hi_value> ) ]
    | [ IN ( '<value1>, '<value2>', ... ) ]
    | [ REFERENCES <table_name>( <col_name> ) ]
  }
```

#### Parameters

A single parameter must be specified.

`BETWEEN ( lo_value, hi_value )`
:   Creates a privacy domain that is the range of possible values in the column, where `lo_value` is the minimum value and
    `hi_value` is the maximum value.

`IN ( 'value1', 'value2', ... )`
:   Creates a privacy domain that is an enumerated list of the specified values.

    The `IN` parameter accepts a maximum of 50 values, each of which can contain a maximum of 100 characters. If you need to specify an
    enumerated list of greater than 50 values, use the `REFERENCES` parameter.

`REFERENCES table_name( col_name )`
:   Creates a privacy domain that is an enumerated list consisting of the values contained in the column of a table.

    The user making differentially private queries against a table with a REFERENCES privacy domain must have SELECT privileges to the table
    that contains the column referenced in the privacy domain. This means that if you share a privacy-protected table that references another,
    it is best to share the referenced table in the same share.

    The privacy domain can reference itself; however, you must be careful when using this capability. If the privacy domain references its own
    column, the enumerated list contains all *actual* values in the column, not all *possible* values in the column, which can expose private
    information. For example, if the privacy domain of a `zipcode` column references itself, then the analyst will know with absolute
    certainty whether a particular zip code is in the dataset when they view the privacy domain.

    Note

    You cannot define a privacy domain that references itself when creating the table for the first time. First create the table, then
    [set the privacy domain with a separate command](#label-diff-privacy-admin-domain-alter).

    The column being referenced can contain 16,384 unique values.

#### Set a privacy domain when creating a new table

The syntax to set a privacy domain for a column when using the [CREATE TABLE](/sql-reference/sql/create-table) command to create a table is:

Copy code

```
CREATE TABLE <table_name>
  ( <col_name> <col_type> PRIVACY DOMAIN
    {
        [ BETWEEN ( <lo_value>, <hi_value> ) ]
      | [ IN ( '<value1>', '<value2>', ... ) ]
      | [ REFERENCES <table_name>( <col_name> ) ]
    }
  )
```

For more information, see [Privacy domain syntax](#label-diff-privacy-admin-domain-syntax).

### Set a privacy domain when adding a new column

The syntax to set a privacy domain when using the [ALTER TABLE](/sql-reference/sql/alter-table) to add a new column to an existing table is:

Copy code

```
ALTER TABLE <table_name>
  ADD COLUMN <col_name> <col_type> PRIVACY DOMAIN
    {
        [ BETWEEN ( <lo_value>, <hi_value> ) ]
      | [ IN ( '<value1>', '<value2>', ... ) ]
      | [ REFERENCES <table_name>( <col_name> ) ]
    }
```

For more information, see [Privacy domain syntax](#label-diff-privacy-admin-domain-syntax).

### Set a privacy domain by modifying a column

The syntax to set a privacy domain for an existing column of a table using the [ALTER TABLE … ALTER COLUMN](/sql-reference/sql/alter-table-column) command is:

Copy code

```
ALTER TABLE <table_name>
  { ALTER | MODIFY } COLUMN <col1_name> SET PRIVACY DOMAIN
    {
        [ BETWEEN ( <lo_value>, <hi_value> ) ]
      | [ IN ( '<value1>', '<value2>', ... ) ]
      | [ REFERENCES <table_name>( <col_name> ) ]
    }
```

For more information, see [Privacy domain syntax](#label-diff-privacy-admin-domain-syntax).

## Modify a privacy domain

The syntax for modifying an existing privacy domain is identical to [creating a new privacy domain on an existing column](#label-diff-privacy-admin-domain-modify-column). An ALTER TABLE .. ALTER COLUMN … SET PRIVACY DOMAIN command replaces the old privacy
domain with the new one.

## Remove a privacy domain

The syntax for using the [ALTER TABLE … ALTER COLUMN](/sql-reference/sql/alter-table-column) command to remove a privacy domain from a column is:

Copy code

```
ALTER TABLE <table_name>
  { ALTER | MODIFY } COLUMN <col1_name> UNSET PRIVACY DOMAIN
```

## View a privacy domain

To view the privacy domains of a privacy-protected table or view, execute the [DESCRIBE TABLE](/sql-reference/sql/desc-table) or
[DESCRIBE VIEW](/sql-reference/sql/desc-view) command. The privacy domain for a column appears in the PRIVACY\_DOMAIN column of the output.

You need the SELECT privilege on a privacy-protected table to view its privacy domains.

### Interpreting the privacy domain object

A privacy domain for a column is returned as a JSON object. The `domain_type` field of the JSON object indicates whether the privacy
domain is a range of values or an enumerated list. The remaining fields in the object are dependent on the value of the `domain_type`
field.

The JSON object for a privacy domain can include the following fields:

`domain_type`
:   Indicates the type of privacy domain.

    `BETWEEN`
    :   The privacy domain is a range of the possible values that might be in the column.

    `IN`
    :   The privacy domain is an enumerated list of the possible values that might be in the column.

    `REFERENCES`
    :   The privacy domain is an enumerated list of the possible values that might be in the column. This list comes
        from the column of the same table or another table. To view the enumerated list of the privacy domain, query the contents of the
        referenced column.

`low`
:   When `domain_type = BETWEEN`, specifies the minimum value in the range of possible values.

`high`
:   When `domain_type = BETWEEN`, specifies the maximum value in the range of possible values.

`values`
:   When `domain_type = IN`, specifies the enumerated list of possible values, structured as an array.

`database`
:   When `domain_type = REFERENCES`, specifies the database that contains the column that Snowflake references to build the enumerated
    list of possible values.

`schema`
:   When `domain_type = REFERENCES`, specifies the schema that contains the column that Snowflake references to build the enumerated
    list of possible values.

`table`
:   When `domain_type = REFERENCES`, specifies the table that contains the column that Snowflake references to build the enumerated
    list of possible values.

`column`
:   When `domain_type = REFERENCES`, specifies the column that Snowflake references to build the enumerated list of possible values.
    To view the enumerated list of the privacy domain, query the contents of this column.
