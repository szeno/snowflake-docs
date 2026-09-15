# <code className=”samp”><em>custom\_classifier</em></code>!ADD\_REGEX

[Enterprise Edition Feature](/user-guide/intro-editions)

Sensitive data classification requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

See also:
:   [Using custom classifiers to implement custom semantic categories](/user-guide/classify-custom-using)

Adds categories and a regular expression to the custom classifier, while optionally specifying a regular expression for the column name and
a comment.

## Syntax

Copy code

```
<custom_classifier>!ADD_REGEX(
  SEMANTIC_CATEGORY => '<custom_category>' ,
  PRIVACY_CATEGORY => { 'IDENTIFIER' | 'QUASI-IDENTIFIER' | 'SENSITIVE' } ,
  VALUE_REGEX => '<regular_expression>' ,
  [ COL_NAME_REGEX => <regular_expression> ] ,
  [ DESCRIPTION => <string> ] ,
  [ THRESHOLD => <number> ]
)
```

## Arguments

**Required:**

`SEMANTIC_CATEGORY => custom_category`
:   Specifies the name of the custom category (that is, type of information).

`PRIVACY_CATEGORY => { 'IDENTIFIER' | 'QUASI-IDENTIFIER' | 'SENSITIVE' }`
:   Specifies the sensitivity of the data, and can be one of the following values: `'IDENTIFIER'`, `'QUASI_IDENTIFIER'`, or
    `'SENSITIVE'`.

`VALUE_REGEX => regular_expression`
:   Specifies the regular expression to match the values in a column.

    You can test the syntax of the regular expression by calling the [REGEXP\_LIKE](/sql-reference/functions/regexp_like) function.

**Optional:**

`COL_NAME_REGEX => regular_expression`
:   Specifies the regular expression to match the name of the column that you want to classify.

`DESCRIPTION => string`
:   Specifies a comment describing the custom category or the custom classifier that implements it.

`THRESHOLD => number`
:   Specifies the threshold value for the scoring rule. For more information, see [Threshold for custom categories](/user-guide/classify-custom#label-classify-custom-threshold).

    The acceptable range is greater than `0.0` and less than or equal to `1.0`.

    Default: `0.8`.

## Output

Returns a status message indicating the association of the category with the custom classifier in this format:
`classifier_name:category_name`.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Instance role | Object | Notes |
| --- | --- | --- |
| `custom_classifier`!PRIVACY\_USER | The custom classification instance. | The account role that calls this method must be granted this instance role on the custom classifier.  By default, the account role used to create the instance can call this method. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Calling this method multiple times gives an additive result for the number of regular expressions associated with the instance.
- Call each method in a separate SQL statement (no method chaining).
- All regular expression searches for classification purposes are case-insensitive.
- Test the regular expression before adding a regular expression to the custom classification instance. For example,
  use the [[ NOT ] REGEXP](/sql-reference/functions/regexp) function to make sure that only values that match the regex are returned in the result:

  Copy code

  ```
  SELECT <col_to_classify>
  FROM <table_with_col_to_classify>
  WHERE <col_to_classify> REGEXP('<regex>');
  ```

  For details, see [String functions (regular expressions)](/sql-reference/functions-regexp).

## Examples

Add categories and a regular expression to the `medical_codes` instance:

Copy code

```
CALL internal_ids!ADD_REGEX(
  SEMANTIC_CATEGORY => 'EMPLOYEE_ID',
  PRIVACY_CATEGORY => 'IDENTIFIER',
  VALUE_REGEX => '^[0-9]{6}$',
  COL_NAME_REGEX => 'EMP.*ID.*',
  DESCRIPTION => 'Add a regex to identify employee IDs in a column',
  THRESHOLD => 0.8
);
```

Returns:

```
+---------------+
|   ADD_REGEX   |
+---------------+
| EMPLOYEE_ID   |
+---------------+
```

Create a custom classifier that uses the default threshold and doesn’t use a regular expression to match column names:

Copy code

```
CALL medical_codes!ADD_REGEX(
  SEMANTIC_CATEGORY => 'ICD_10_CODES',
  PRIVACY_CATEGORY => 'IDENTIFIER',
  VALUE_REGEX => '[A-TV-Z][0-9][0-9AB]\.?[0-9A-TV-Z]{0,4}'
);
```
