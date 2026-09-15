Categories:
:   [String & binary functions](/sql-reference/functions-string) (Full-Text Search)

# SEARCH

Searches character data (text) in specified columns from one or more tables, including fields in VARIANT, OBJECT,
and ARRAY columns. A text analyzer breaks the text into tokens, which are discrete units of text, such as words
or numbers. A default analyzer is applied if you don’t specify one.

For more information about using this function, see [Using full-text search](/user-guide/querying-with-search-functions).

## Syntax

Copy code

```
SEARCH( <search_data>, '<search_string>'
  [ , ANALYZER => '<analyzer_name>' ]
  [ , SEARCH_MODE => { 'OR' | 'AND' | 'PHRASE' | 'EXACT' } ] )
```

## Required arguments

`search_data`
:   The data you want to search, expressed as a comma-delimited list of string literals, column names, or
    [paths](/user-guide/querying-semistructured#label-traversing-semistructured-data) to fields in VARIANT columns. The search data can
    also be a single literal string, which can be useful when you are testing the function.

    You can specify the wildcard character (`*`), where `*` expands to all qualifying columns in all of the
    tables that are in scope for the function. Qualifying columns are those that have VARCHAR (text), VARIANT,
    ARRAY, and OBJECT data types. VARIANT, ARRAY, and OBJECT data is converted to text for searching.

    When you pass a wildcard to the function, you can qualify the wildcard with the name or alias for the table.
    For example, to pass in all of the columns from the table named `mytable`, specify the following:

    Copy code

    ```
    (mytable.*)
    ```

    You can also use the ILIKE and EXCLUDE keywords for filtering:

    - ILIKE filters for column names that match the specified pattern. Only one
      pattern is allowed. For example:

      Copy code

      ```
      (* ILIKE 'col1%')
      ```
    - EXCLUDE filters out column names that don’t match the specified column or columns. For example:

      Copy code

      ```
      (* EXCLUDE col1)

      (* EXCLUDE (col1, col2))
      ```

    Qualifiers are valid when you use these keywords. The following example uses the ILIKE keyword to
    filter for all of the columns that match the pattern `col1%` in the table `mytable`:

    Copy code

    ```
    (mytable.* ILIKE 'col1%')
    ```

    The ILIKE and EXCLUDE keywords can’t be combined in a single function call.

    For more information about the ILIKE and EXCLUDE keywords, see the “Parameters” section in [SELECT](/sql-reference/sql/select).

    You can search columns from more than one table when multiple tables are in scope by joining tables or using
    the [UNION](/sql-reference/operators-query#label-query-operators-union) set operator. To search all of the columns in the output of a
    join or a UNION query, you can use the unqualified `*` wildcard as follows:

    Copy code

    ```
    SELECT *
      FROM t AS T1
        JOIN t AS T2 USING (col1)
      WHERE SEARCH((*), 'string');
    ```

    To search specific columns when joining tables, you might need to qualify the column
    names (for example, `table2.colname`). You can also use a qualified `*` wildcard as follows:

    Copy code

    ```
    SELECT *
      FROM t AS T1
        JOIN t AS T2 USING (col1)
      WHERE SEARCH((T2.*), 'string');
    ```

    However, you can’t specify `*` or `table.*` more than once for the function.
    In the previous join example, you can’t specify `SEARCH((T1.*, T2.*), 'string')`. This
    syntax returns an error.

    Parentheses are required for the `search_data` argument when `*`, `table.*`,
    or multiple items are listed. For example:

    Copy code

    ```
    SEARCH((col1, col2, col3), 'string')
    SEARCH((t1.*), 'string')
    SEARCH((*), 'string')
    ```

    If parentheses aren’t used to separate multiple items, commas are parsed as separators between function arguments.

    See also [Examples of Expected Error Cases](#examples-of-expected-error-cases).

    You can search fields in VARIANT data by specifying the column name, a colon or dot, and the subfields
    separated by dots. For example: `colname:fieldname.subfieldname`. For more information about specifying
    fields in such columns, see [Traversing Semi-structured Data](/user-guide/querying-semistructured#label-traversing-semistructured-data).

`'search_string'`
:   A VARCHAR string that contains one or more search terms. This argument must be a literal string; column names
    aren’t supported. Specify one pair of single quotes around the entire string. Don’t specify quotes around
    individual terms or phrases. For example, use:

    `'blue red green'`

    Don’t use:

    `'blue' 'red' 'green'`

    The list of terms can be disjunctive or conjunctive when `OR` or `AND` is set for the SEARCH\_MODE argument.
    However, when the `'NO_OP_ANALYZER'` is used, the query string is matched exactly as it is, with no tokenization
    and no disjunctive or conjunctive semantics.

    Searches aren’t case sensitive, except when the `'NO_OP_ANALYZER'` is used, so a search for the term `'ONCE'`
    against the string `'Once upon a time'` returns TRUE.

    When `OR` or `AND` is set for the SEARCH\_MODE argument, the order of search terms doesn’t matter
    with respect to their presence in the searched data. When `PHRASE` or `EXACT` is set for the SEARCH\_MODE
    argument, the order of search terms must exactly match the searched data.

## Optional arguments

`ANALYZER => 'analyzer_name'`
:   The name of the text analyzer. The name must be enclosed in single quotes.

    The analyzer breaks the search terms (and the text from the column being searched) into tokens.
    The matching semantics (disjunctive, conjunctive, phrase, or exact) for tokens extracted from the search string
    and tokens extracted from the columns or fields being searched depends on the value of the
    [SEARCH\_MODE](/sql-reference/functions/search#label-search-mode) argument.

    The analyzer tokenizes a string by breaking it where it finds certain delimiters. These delimiters aren’t
    included in the resulting tokens, and empty tokens aren’t extracted.

    This parameter accepts one of the following values:

    - `'DEFAULT_ANALYZER'` - Breaks text into tokens based on the following delimiters:

      | Character | Unicode code | Description |
      | --- | --- | --- |
      | `` | `U+0020` | Space |
      | `[` | `U+005B` | Left square bracket |
      | `]` | `U+005D` | Right square bracket |
      | `;` | `U+003B` | Semicolon |
      | `<` | `U+003C` | Less-than sign |
      | `>` | `U+003E` | Greater-than sign |
      | `(` | `U+0028` | Left parenthesis |
      | `)` | `U+0029` | Right parenthesis |
      | `{` | `U+007B` | Left curly bracket |
      | `}` | `U+007D` | Right curly bracket |
      | `|` | `U+007C` | Vertical bar |
      | `!` | `U+0021` | Exclamation mark |
      | `,` | `U+002C` | Comma |
      | `'` | `U+0027` | Apostrophe |
      | `"` | `U+0022` | Quotation mark |
      | `*` | `U+002A` | Asterisk |
      | `&` | `U+0026` | Ampersand |
      | `?` | `U+003F` | Question mark |
      | `+` | `U+002B` | Plus sign |
      | `/` | `U+002F` | Slash |
      | `:` | `U+003A` | Colon |
      | `=` | `U+003D` | Equal sign |
      | `@` | `U+0040` | At sign |
      | `.` | `U+002E` | Period (full stop) |
      | `-` | `U+002D` | Hyphen |
      | `$` | `U+0024` | Dollar sign |
      | `%` | `U+0025` | Percent sign |
      | `\` | `U+005C` | Backslash |
      | `_` | `U+005F` | Underscore (low line) |
      | `\n` | `U+000A` | New line (line feed) |
      | `\r` | `U+000D` | Carriage return |
      | `\t` | `U+0009` | Horizontal tab |

      Expand

      Show lessSee more
    - `'UNICODE_ANALYZER'` - Tokenizes based on Unicode segmentation rules that treat spaces and certain
      punctuation characters as delimiters. These internal rules are designed for natural language searches in
      many different languages. For example, the default analyzer treats periods in IP addresses and
      apostrophes in contractions as delimiters, but the Unicode analyzer doesn’t.
      See [Using an analyzer to adjust search behavior](#label-search-function-adjust-search-behavior).

      For more information about the Unicode Text Segmentation algorithm, see <https://unicode.org/reports/tr29/>.
    - `'NO_OP_ANALYZER'` - Tokenizes neither the data nor the query string. A search term must exactly match the full text
      in a column or field, including case sensitivity; otherwise, the SEARCH function returns FALSE. Even if the query
      string looks like it contains multiple tokens — for example, `'sky blue'` — the column or field must equal the
      entire query string exactly. In this case, only `'sky blue'` is a match; `'sky'` and `'blue'` aren’t matches.

    For more information about the behavior of different analyzers, see [How search terms are tokenized](#label-how-search-terms-tokenized).

`SEARCH_MODE => { 'OR' | 'AND' | 'PHRASE' | 'EXACT' }`
:   The semantics used by the search. Set this argument to one of the following values:

    - `'OR'` - The function uses disjunctive semantics. There is a match if *any* of the tokens
      extracted from the columns or fields being searched match *any* of the tokens extracted from the search string.
      For example, if the `search_string` value is `'blue red green'`, the function returns TRUE for a row that
      contains `blue` OR `red` OR `green` in any of the columns or fields being searched.
    - `'AND'` - The function uses conjunctive semantics. There is a match if the tokens extracted from
      *at least one* of the columns or fields being searched matches *all* of the tokens extracted from the search
      string. The matching tokens must all be in one column or field; they can’t be spread across multiple columns or fields.
      For example, if the `search_string` value is `'blue red green'`, the function returns TRUE for a row that
      contains `blue` AND `red` AND `green` in at least one of the columns or fields being searched.
    - `'PHRASE'` - The function uses phrase-match semantics. There is a match if the tokens extracted from
      *at least one* of the columns or fields being searched matches *all* of the tokens extracted from the search string,
      including the order and adjacency of the tokens.

      The matching semantics are the same as conjunctive semantics, except for the following differences:

      - The order of the tokens must exactly match. For example, if the `search_string` value is `'blue,red,green'`,
        the function returns FALSE for `red,green,blue`.
      - No additional tokens can be interspersed in the search data. For example, if the `search_string` value
        is `'blue,red,green'`, the function returns FALSE for `blue,yellow,red,green`.
    - `'EXACT'` - The function uses exact-match semantics. There is a match if the tokens extracted from
      *at least one* of the columns or fields being searched exactly matches *all* of the tokens extracted
      from the search string, including the delimiters.

      The matching rules are the same as phrase-search semantics, except for the following differences:

      - The delimiter strings between the tokens must match exactly. For example, if the `search_string`
        value is `'blue,red,green'`, the function returns TRUE for a row that contains `blue,red,green`
        in at least one of the columns or fields being searched. The function returns FALSE for variations such as
        `blue%red%green` or `blue, red, green`.
      - When a delimiter is the first or last character in the `search_string` value, the delimiter
        is treated like a character for matching. Therefore, delimiters on the left and right of the first and
        last delimiter can result in a match. For example, if the `search_string` value is `'[blue]'`,
        the function returns TRUE for `foo [blue] bar`, `[[blue]]`, and `=[blue].`, but not for
        `(blue)` or `foo blue bar`.

      For all search modes, the string must be delimited by a delimiter symbol on the left and right. For example, if the
      `search_string` value is `'blue,red,green'`, the function returns TRUE for
      `-blue,red,green;`. The function returns FALSE for `darkblue,red,green` or
      `blue,red,greenish`.

      If you use the `UNICODE_ANALYZER`, exact-match semantics aren’t supported. You can use the
      `DEFAULT_ANALYZER` or the `NO_OP_ANALYZER` with exact-match semantics, but generally
      these search semantics are best suited for the `DEFAULT_ANALYZER`.

      A search that uses exact-match semantics with the `DEFAULT_ANALYZER` behaves differently
      than an equality search or a full-text searches with the `NO_OP_ANALYZER` in the following ways:

      - An equality search matches rows where the column value is exactly the same as in the predicate
        (including letter case), with no additional text surrounding the occurrence of the search string.
      - A full-text search with the `NO_OP_ANALYZER` is similar to an equality search in that it is
        case-sensitive and doesn’t allow additional text.
      - A search with exact-match semantics with the `DEFAULT_ANALYZER` tokenizes the column values. It
        allows additional tokens to the left and right of the search string occurrence as long as they are separated
        by token delimiters. The search is case-insensitive.

    Default: `'OR'`

## Returns

Returns a BOOLEAN:

- The value is TRUE if `search_string` tokens match `search_data` tokens based on the semantics specified
  in the SEARCH\_MODE argument.
- Returns NULL if either of these arguments is NULL.
- Otherwise, returns FALSE.

## Usage notes

- The SEARCH function operates only on VARCHAR, VARIANT, ARRAY, and OBJECT data. The function returns an error if the
  `search_data` argument doesn’t contain data of these data types. When the `search_data` argument includes
  data of both supported data types and unsupported data types, the function searches the data of the supported data
  types and silently ignores the data of the unsupported data types. For examples, see [Examples of expected error cases](#label-search-function-error-examples).
- You can add a FULL\_TEXT search optimization on columns that are the target of SEARCH function calls by using an ALTER TABLE
  command. For example:

  Copy code

  ```
  ALTER TABLE lines ADD SEARCH OPTIMIZATION
    ON FULL_TEXT(play, character, line);
  ```

  For more information, see [enable FULL\_TEXT search optimization](/user-guide/search-optimization/enabling#label-enable-full-text-search).

## How search terms are tokenized

The following table shows a few examples of how input search terms are split into tokens,
which depends on the rules applied by the analyzer that is used. In the table, commas
denote where the tokens are split (if they are).

| Search Term(s) | Tokens: DEFAULT\_ANALYZER | Tokens: UNICODE\_ANALYZER | NO\_OP\_ANALYZER (not split) |
| --- | --- | --- | --- |
| `10.210.158.44` | `10`, `210`, `158`, `44` | `10.210.158.44` | `10.210.158.44` |
| `192.0.2.0/24` | `192`, `0`, `2`, `24` | `192.0.2.0`, `24` | `192.0.2.0/24` |
| `high-tech` | `high`, `tech` | `high`, `tech` | `high-tech` |
| `Bob's Burgers` | `bob`, `s`, `burgers` | `bob's`, `burgers` | `Bob's Burgers` |
| `Three spaces` | `three`, `spaces` | `three`, `spaces` | `Three spaces` |
| `docs@snowflake.com` | `docs`, `snowflake`, `com` | `docs`, `snowflake.com` | `docs@snowflake.com` |
| `/opt/homebrew/README.md` | `opt`, `homebrew`, `readme`, `md` | `opt`, `homebrew`, `readme.md` | `/opt/homebrew/README.md` |

Expand

Show lessSee more

## Examples

The following examples show different ways to use the SEARCH function, starting with simple
usage and progressing to more complex use cases:

- [Matching against a literal](#label-search-function-example-literal)
- [Matching against a column reference](#label-search-function-example-column-reference)
- [WHERE clause search on one column](#label-search-function-example-where-clause-one-column)
- [WHERE clause search on multiple columns](#label-search-function-example-where-clause-multiple-columns)
- [Wildcard search on all qualifying columns in a table](#label-search-function-example-wildcard-columns)
- [Wildcard search in a SELECT list](#label-search-function-example-select-list)
- [Wildcard search on qualifying columns in joined tables](#label-search-function-example-wildcard-join)
- [Wildcard search on the output of a UNION subquery](#label-search-function-example-union-subquery)
- [Finding rows that match multiple search strings](#label-search-function-example-multiple-strings)
- [Finding rows using phrase-match and exact-match semantics](#label-search-function-example-phrase-exact)
- [Searching VARIANT and VARCHAR data in a join](#label-search-function-example-variant-varchar-join)
- [Using an analyzer to adjust search behavior](#label-search-function-adjust-search-behavior)
- [Examples of expected error cases](#label-search-function-error-examples)

To run the queries in several examples, first [create the sample data for the SEARCH function](#label-search-sample-data).

### Matching against a literal

The simplest example of the SEARCH function is a test for TRUE or FALSE on a string literal. The first
example returns TRUE because the literals for the first and second arguments match, given that the comparison
isn’t case sensitive.

Copy code

```
SELECT SEARCH('king','KING');
```

```
+-----------------------------+
| SEARCH('KING','KING')       |
|-----------------------------|
| True                        |
+-----------------------------+
```

The second example returns FALSE because the token `32` doesn’t appear in the literal `5.1.33` specified
for the first argument.

Copy code

```
SELECT SEARCH('5.1.33','32');
```

```
+-----------------------------+
| SEARCH('5.1.33','32')       |
|-----------------------------|
| False                       |
+-----------------------------+
```

### Matching against a column reference

This example uses a column in a table as the first argument. The function returns TRUE because one of
the search terms (`king`) exists in the `character` column. The list of terms is disjunctive because
the default value for the SEARCH\_MODE argument is `'OR'`. (For information about the table used
here and in some subsequent examples, see [Creating the sample data for SEARCH](#label-search-sample-data).)

Copy code

```
SELECT SEARCH(character, 'king queen'), character
  FROM lines
  WHERE line_id=4;
```

```
+---------------------------------+---------------+
| SEARCH(CHARACTER, 'KING QUEEN') | CHARACTER     |
|---------------------------------+---------------|
| True                            | KING HENRY IV |
+---------------------------------+---------------+
```

The following example is similar to the previous example, but search semantics are conjunctive because the
SEARCH\_MODE argument is set to `'AND'`. The function returns FALSE because only one of the search terms
(`king`) exists in the `character` column. The term `queen` doesn’t appear in the search data.

Copy code

```
SELECT SEARCH(character, 'king queen', SEARCH_MODE => 'AND'), character
  FROM lines
  WHERE line_id=4;
```

```
+-------------------------------------------------------+---------------+
| SEARCH(CHARACTER, 'KING QUEEN', SEARCH_MODE => 'AND') | CHARACTER     |
|-------------------------------------------------------+---------------|
| False                                                 | KING HENRY IV |
+-------------------------------------------------------+---------------+
```

### WHERE clause search on one column

The following query uses the SEARCH function to find rows that contain the word `wherefore` in the `line` column:

Copy code

```
SELECT *
  FROM lines
  WHERE SEARCH(line, 'wherefore')
  ORDER BY character LIMIT 5;
```

```
+---------+----------------------+------------+----------------+-----------+-----------------------------------------------------+
| LINE_ID | PLAY                 | SPEECH_NUM | ACT_SCENE_LINE | CHARACTER | LINE                                                |
|---------+----------------------+------------+----------------+-----------+-----------------------------------------------------|
|  100109 | Troilus and Cressida |         31 | 2.1.53         | ACHILLES  | Why, how now, Ajax! wherefore do you thus? How now, |
|   16448 | As You Like It       |          2 | 2.3.6          | ADAM      | And wherefore are you gentle, strong and valiant?   |
|   24055 | The Comedy of Errors |         14 | 5.1.41         | AEMELIA   | Be quiet, people. Wherefore throng you hither?      |
|   99330 | Troilus and Cressida |         30 | 1.1.102        | AENEAS    | How now, Prince Troilus! wherefore not afield?      |
|   92454 | The Tempest          |        150 | 2.1.343        | ALONSO    | Wherefore this ghastly looking?                     |
+---------+----------------------+------------+----------------+-----------+-----------------------------------------------------+
```

### WHERE clause search on multiple columns

The following query uses the SEARCH function to find rows that contain the word `king` in the `play` column,
the `character` column, or both columns. Parentheses are required for the first argument.

Copy code

```
SELECT play, character
  FROM lines
  WHERE SEARCH((play, character), 'king')
  ORDER BY play, character LIMIT 10;
```

```
+---------------------------+-----------------+
| PLAY                      | CHARACTER       |
|---------------------------+-----------------|
| All's Well That Ends Well | KING            |
| Hamlet                    | KING CLAUDIUS   |
| Hamlet                    | KING CLAUDIUS   |
| Henry IV Part 1           | KING HENRY IV   |
| Henry IV Part 1           | KING HENRY IV   |
| King John                 | CHATILLON       |
| King John                 | KING JOHN       |
| King Lear                 | GLOUCESTER      |
| King Lear                 | KENT            |
| Richard II                | KING RICHARD II |
+---------------------------+-----------------+
```

### Wildcard search on all qualifying columns in a table

You can use the `*` character (or `table.*`) as the first argument to the SEARCH function, as shown in this example.
The search operates on all of the qualifying columns in the table you are selecting from, which in this case is the `lines` table.

The `lines` table has four columns that have data types supported by the search function. The result consists of rows where `king`
appears in one or more of the four searched columns. For one of these columns, `act_scene_line`, the function finds no matches, but
the other three columns all have matches. The SEARCH\_MODE argument defaults to `'OR'`.

Copy code

```
SELECT play, character, line, act_scene_line
  FROM lines
  WHERE SEARCH((lines.*), 'king')
  ORDER BY act_scene_line LIMIT 10;
```

```
+-----------------+-----------------+----------------------------------------------------+----------------+
| PLAY            | CHARACTER       | LINE                                               | ACT_SCENE_LINE |
|-----------------+-----------------+----------------------------------------------------+----------------|
| Pericles        | LODOVICO        | This king unto him took a fere,                    | 1.0.21         |
| Richard II      | KING RICHARD II | Old John of Gaunt, time-honour'd Lancaster,        | 1.1.1          |
| Henry VI Part 3 | WARWICK         | I wonder how the king escaped our hands.           | 1.1.1          |
| King John       | KING JOHN       | Now, say, Chatillon, what would France with us?    | 1.1.1          |
| King Lear       | KENT            | I thought the king had more affected the Duke of   | 1.1.1          |
| Henry IV Part 1 | KING HENRY IV   | So shaken as we are, so wan with care,             | 1.1.1          |
| Henry IV Part 1 | KING HENRY IV   | Which, like the meteors of a troubled heaven,      | 1.1.10         |
| King Lear       | GLOUCESTER      | so often blushed to acknowledge him, that now I am | 1.1.10         |
| Cymbeline       | First Gentleman | Is outward sorrow, though I think the king         | 1.1.10         |
| King John       | CHATILLON       | To this fair island and the territories,           | 1.1.10         |
+-----------------+-----------------+----------------------------------------------------+----------------+
```

You can also use the ILIKE and EXCLUDE keywords for filtering. For more information about
these keywords, see [SELECT](/sql-reference/sql/select).

This search uses the ILIKE keyword to search only in columns that end with the string `line`. So, the
function searches in the `line` and `act_scene_line` columns.

Copy code

```
SELECT play, character, line, act_scene_line
  FROM lines
  WHERE SEARCH((lines.* ILIKE '%line'), 'king')
  ORDER BY act_scene_line LIMIT 10;
```

```
+-----------------+-----------------+--------------------------------------------------+----------------+
| PLAY            | CHARACTER       | LINE                                             | ACT_SCENE_LINE |
|-----------------+-----------------+--------------------------------------------------+----------------|
| Pericles        | LODOVICO        | This king unto him took a fere,                  | 1.0.21         |
| Henry VI Part 3 | WARWICK         | I wonder how the king escaped our hands.         | 1.1.1          |
| King Lear       | KENT            | I thought the king had more affected the Duke of | 1.1.1          |
| Cymbeline       | First Gentleman | Is outward sorrow, though I think the king       | 1.1.10         |
+-----------------+-----------------+--------------------------------------------------+----------------+
```

This search uses the EXCLUDE keyword so that the function doesn’t search the data in the `character` column.

Copy code

```
SELECT play, character, line, act_scene_line
  FROM lines
  WHERE SEARCH((lines.* EXCLUDE character), 'king')
  ORDER BY act_scene_line LIMIT 10;
```

```
+-----------------+-----------------+----------------------------------------------------+----------------+
| PLAY            | CHARACTER       | LINE                                               | ACT_SCENE_LINE |
|-----------------+-----------------+----------------------------------------------------+----------------|
| Pericles        | LODOVICO        | This king unto him took a fere,                    | 1.0.21         |
| Henry VI Part 3 | WARWICK         | I wonder how the king escaped our hands.           | 1.1.1          |
| King John       | KING JOHN       | Now, say, Chatillon, what would France with us?    | 1.1.1          |
| King Lear       | KENT            | I thought the king had more affected the Duke of   | 1.1.1          |
| Cymbeline       | First Gentleman | Is outward sorrow, though I think the king         | 1.1.10         |
| King Lear       | GLOUCESTER      | so often blushed to acknowledge him, that now I am | 1.1.10         |
| King John       | CHATILLON       | To this fair island and the territories,           | 1.1.10         |
+-----------------+-----------------+----------------------------------------------------+----------------+
```

### Wildcard search in a SELECT list

You can use the `*` character (or `table.*`) in a SELECT list, as shown in these examples.

The following search operates on all of the qualifying columns in the table you are selecting from, which in
this case is the `lines` table. The search returns TRUE when `king` appears in one or more of the four
searched columns. The SEARCH\_MODE argument defaults to `'OR'`.

Copy code

```
SELECT SEARCH((*), 'king') result, *
  FROM lines
  ORDER BY act_scene_line LIMIT 10;
```

```
+--------+---------+---------------------------+------------+----------------+-----------------+--------------------------------------------------------+
| RESULT | LINE_ID | PLAY                      | SPEECH_NUM | ACT_SCENE_LINE | CHARACTER       | LINE                                                   |
|--------+---------+---------------------------+------------+----------------+-----------------+--------------------------------------------------------|
| True   |   75787 | Pericles                  |        178 | 1.0.21         | LODOVICO        | This king unto him took a fere,                        |
| True   |   43494 | King John                 |          1 | 1.1.1          | KING JOHN       | Now, say, Chatillon, what would France with us?        |
| True   |   49031 | King Lear                 |          1 | 1.1.1          | KENT            | I thought the king had more affected the Duke of       |
| True   |   78407 | Richard II                |          1 | 1.1.1          | KING RICHARD II | Old John of Gaunt, time-honour'd Lancaster,            |
| False  |   67000 | A Midsummer Night's Dream |          1 | 1.1.1          | THESEUS         | Now, fair Hippolyta, our nuptial hour                  |
| True   |       4 | Henry IV Part 1           |          1 | 1.1.1          | KING HENRY IV   | So shaken as we are, so wan with care,                 |
| False  |   12664 | All's Well That Ends Well |          1 | 1.1.1          | COUNTESS        | In delivering my son from me, I bury a second husband. |
| True   |    9526 | Henry VI Part 3           |          1 | 1.1.1          | WARWICK         | I wonder how the king escaped our hands.               |
| False  |   52797 | Love's Labour's Lost      |          1 | 1.1.1          | FERDINAND       | Let fame, that all hunt after in their lives,          |
| True   |   28487 | Cymbeline                 |          3 | 1.1.10         | First Gentleman | Is outward sorrow, though I think the king             |
+--------+---------+---------------------------+------------+----------------+-----------------+--------------------------------------------------------+
```

You can also use the ILIKE and EXCLUDE keywords for filtering. For more information about
these keywords, see [SELECT](/sql-reference/sql/select).

This search uses the ILIKE keyword to search only in columns that end with the string `line`. So, the
function searches in the `line` and `act_scene_line` columns.

Copy code

```
SELECT SEARCH(* ILIKE '%line', 'king') result, play, character, line
  FROM lines
  ORDER BY act_scene_line LIMIT 10;
```

```
+--------+---------------------------+-----------------+--------------------------------------------------------+
| RESULT | PLAY                      | CHARACTER       | LINE                                                   |
|--------+---------------------------+-----------------+--------------------------------------------------------|
| True   | Pericles                  | LODOVICO        | This king unto him took a fere,                        |
| False  | King John                 | KING JOHN       | Now, say, Chatillon, what would France with us?        |
| True   | King Lear                 | KENT            | I thought the king had more affected the Duke of       |
| False  | Richard II                | KING RICHARD II | Old John of Gaunt, time-honour'd Lancaster,            |
| False  | A Midsummer Night's Dream | THESEUS         | Now, fair Hippolyta, our nuptial hour                  |
| False  | Henry IV Part 1           | KING HENRY IV   | So shaken as we are, so wan with care,                 |
| False  | All's Well That Ends Well | COUNTESS        | In delivering my son from me, I bury a second husband. |
| True   | Henry VI Part 3           | WARWICK         | I wonder how the king escaped our hands.               |
| False  | Love's Labour's Lost      | FERDINAND       | Let fame, that all hunt after in their lives,          |
| True   | Cymbeline                 | First Gentleman | Is outward sorrow, though I think the king             |
+--------+---------------------------+-----------------+--------------------------------------------------------+
```

This search uses the EXCLUDE keyword so that the function doesn’t search the data in the `play` or `line` columns.

Copy code

```
SELECT SEARCH(* EXCLUDE (play, line), 'king') result, play, character, line
  FROM lines
  ORDER BY act_scene_line LIMIT 10;
```

```
+--------+---------------------------+-----------------+--------------------------------------------------------+
| RESULT | PLAY                      | CHARACTER       | LINE                                                   |
|--------+---------------------------+-----------------+--------------------------------------------------------|
| False  | Pericles                  | LODOVICO        | This king unto him took a fere,                        |
| True   | King John                 | KING JOHN       | Now, say, Chatillon, what would France with us?        |
| False  | King Lear                 | KENT            | I thought the king had more affected the Duke of       |
| True   | Richard II                | KING RICHARD II | Old John of Gaunt, time-honour'd Lancaster,            |
| False  | A Midsummer Night's Dream | THESEUS         | Now, fair Hippolyta, our nuptial hour                  |
| True   | Henry IV Part 1           | KING HENRY IV   | So shaken as we are, so wan with care,                 |
| False  | All's Well That Ends Well | COUNTESS        | In delivering my son from me, I bury a second husband. |
| False  | Henry VI Part 3           | WARWICK         | I wonder how the king escaped our hands.               |
| False  | Love's Labour's Lost      | FERDINAND       | Let fame, that all hunt after in their lives,          |
| False  | Cymbeline                 | First Gentleman | Is outward sorrow, though I think the king             |
+--------+---------------------------+-----------------+--------------------------------------------------------+
```

### Wildcard search on qualifying columns in joined tables

This example uses two small tables that contain information about car models. Table `t1` has
two character columns, and table `t2` has three. You can create and load the tables as follows:

Copy code

```
CREATE OR REPLACE TABLE t1 (col1 INT, col2 VARCHAR(20), col3 VARCHAR(20));
INSERT INTO t1 VALUES
  (1,'Mini','Cooper'),
  (2,'Mini','Cooper S'),
  (3,'Mini','Countryman'),
  (4,'Mini','Countryman S');
CREATE OR REPLACE TABLE t2 (col1 INT, col2 VARCHAR(20), col3 VARCHAR(20), col4 VARCHAR(20));
INSERT INTO t2 VALUES
  (1,'Mini','Cooper', 'Convertible'),
  (2,'Mini','Cooper S', 'Convertible'),
  (3,'Mini','Countryman SE','ALL4'),
  (4,'Mini','Countryman S','ALL4');
```

The results of the following two queries differ, given the search over `t1.*` and `t2.*`.
Only two columns from `t1` qualify for the search, but three columns from `t2` qualify.

Copy code

```
SELECT * FROM t1 JOIN t2 USING(col1)
  WHERE SEARCH((t1.*),'s all4');
```

```
+------+------+--------------+------+--------------+-------------+
| COL1 | COL2 | COL3         | COL2 | COL3         | COL4        |
|------+------+--------------+------+--------------+-------------|
|    2 | Mini | Cooper S     | Mini | Cooper S     | Convertible |
|    4 | Mini | Countryman S | Mini | Countryman S | ALL4        |
+------+------+--------------+------+--------------+-------------+
```

Copy code

```
SELECT * FROM t1 JOIN t2 USING(col1)
  WHERE SEARCH((t2.*),'s all4');
```

```
+------+------+--------------+------+---------------+-------------+
| COL1 | COL2 | COL3         | COL2 | COL3          | COL4        |
|------+------+--------------+------+---------------+-------------|
|    2 | Mini | Cooper S     | Mini | Cooper S      | Convertible |
|    3 | Mini | Countryman   | Mini | Countryman SE | ALL4        |
|    4 | Mini | Countryman S | Mini | Countryman S  | ALL4        |
+------+------+--------------+------+---------------+-------------+
```

### Wildcard search on the output of a UNION subquery

The following example uses the same two tables as the previous example. In this case,
the search is applied to all qualifying columns from `t3`, which is the table that results
from the subquery. The subquery computes the UNION of the first three columns in `t1` and
`t2` (five rows). The search returns two matching rows from the UNION result.

Copy code

```
SELECT *
  FROM (
    SELECT col1, col2, col3 FROM t1
    UNION
    SELECT col1, col2, col3 FROM t2
    ) AS T3
  WHERE SEARCH((T3.*),'s');
```

```
+------+------+--------------+
| COL1 | COL2 | COL3         |
|------+------+--------------|
|    2 | Mini | Cooper S     |
|    4 | Mini | Countryman S |
+------+------+--------------+
```

### Finding rows that match multiple search strings

The following example uses the SEARCH\_MODE argument to specify conjunctive semantics that find
a match when both search terms occur together in the same column. To use conjunctive semantics, set the
SEARCH\_MODE argument to `'AND'`.

Copy code

```
SELECT act_scene_line, character, line
  FROM lines
  WHERE SEARCH(line, 'Rosencrantz Guildenstern', SEARCH_MODE => 'AND')
    AND act_scene_line IS NOT NULL;
```

```
+----------------+------------------+-----------------------------------------------------------+
| ACT_SCENE_LINE | CHARACTER        | LINE                                                      |
|----------------+------------------+-----------------------------------------------------------|
| 2.2.1          | KING CLAUDIUS    | Welcome, dear Rosencrantz and Guildenstern!               |
| 2.2.35         | KING CLAUDIUS    | Thanks, Rosencrantz and gentle Guildenstern.              |
| 2.2.36         | QUEEN GERTRUDE   | Thanks, Guildenstern and gentle Rosencrantz:              |
| 2.2.241        | HAMLET           | Guildenstern? Ah, Rosencrantz! Good lads, how do ye both? |
| 4.6.27         | HORATIO          | where I am. Rosencrantz and Guildenstern hold their       |
| 5.2.60         | HORATIO          | So Guildenstern and Rosencrantz go to't.                  |
| 5.2.389        | First Ambassador | That Rosencrantz and Guildenstern are dead:               |
+----------------+------------------+-----------------------------------------------------------+
```

When you use conjunctive semantics, there must be a match on both search terms in the same column. For example,
the following query returns no results because the terms `KING` and `Rosencrantz` don’t appear in the
same column in any row in the search data.

Copy code

```
SELECT act_scene_line, character, line
  FROM lines
  WHERE SEARCH(line, 'KING Rosencrantz', SEARCH_MODE => 'AND')
    AND act_scene_line IS NOT NULL;
```

```
+----------------+-----------+------+
| ACT_SCENE_LINE | CHARACTER | LINE |
|----------------+-----------+------|
+----------------+-----------+------+
```

A similar query that uses disjunctive semantics (the default) by setting the SEARCH\_MODE argument to `'OR'`
finds matches in the search data.

Copy code

```
SELECT act_scene_line, character, line
  FROM lines
  WHERE SEARCH(line, 'KING Rosencrantz', SEARCH_MODE => 'OR')
    AND act_scene_line IS NOT NULL;
```

```
+----------------+------------------+-----------------------------------------------------------+
| ACT_SCENE_LINE | CHARACTER        | LINE                                                      |
|----------------+------------------+-----------------------------------------------------------|
| 1.1.1          | WARWICK          | I wonder how the king escaped our hands.                  |
| 1.1.10         | First Gentleman  | Is outward sorrow, though I think the king                |
| 2.2.1          | KING CLAUDIUS    | Welcome, dear Rosencrantz and Guildenstern!               |
| 2.2.35         | KING CLAUDIUS    | Thanks, Rosencrantz and gentle Guildenstern.              |
| 2.2.36         | QUEEN GERTRUDE   | Thanks, Guildenstern and gentle Rosencrantz:              |
| 2.2.241        | HAMLET           | Guildenstern? Ah, Rosencrantz! Good lads, how do ye both? |
| 4.6.27         | HORATIO          | where I am. Rosencrantz and Guildenstern hold their       |
| 5.2.60         | HORATIO          | So Guildenstern and Rosencrantz go to't.                  |
| 5.2.389        | First Ambassador | That Rosencrantz and Guildenstern are dead:               |
| 1.1.1          | KENT             | I thought the king had more affected the Duke of          |
| 1.0.21         | LODOVICO         | This king unto him took a fere,                           |
+----------------+------------------+-----------------------------------------------------------+
```

### Finding rows using phrase-match and exact-match semantics

You can use phrase-match and exact-match semantics for similar but slightly different use cases:

- Use phrase-match semantics when the words and the order of the words must match exactly, but
  there can be differences in the delimiters and spacing between words. To use
  phrase-match semantics, set the SEARCH\_MODE argument to `'PHRASE'`.
- Use exact-match semantics when the words, the order of the words, the delimiters between words,
  and the spacing between words must match exactly. To use exact-match semantics, set the SEARCH\_MODE
  argument to `'EXACT'`.

The following example uses phrase-match semantics to find an exact match of text in a longer text string,
but the search text has different delimiters and extra spaces between the words:

Copy code

```
SELECT act_scene_line, character, line
  FROM lines
  WHERE SEARCH(line, 'Why - how  now:  Ajax!', SEARCH_MODE => 'PHRASE');
```

```
+----------------+-----------+-----------------------------------------------------+
| ACT_SCENE_LINE | CHARACTER | LINE                                                |
|----------------+-----------+-----------------------------------------------------|
| 2.1.53         | ACHILLES  | Why, how now, Ajax! wherefore do you thus? How now, |
+----------------+-----------+-----------------------------------------------------+
```

The following example is the same as the previous example, except that it uses exact-match semantics to find
an exact match of text in a longer text string:

Copy code

```
SELECT act_scene_line, character, line
  FROM lines
  WHERE SEARCH(line, 'Why, how now, Ajax!', SEARCH_MODE => 'EXACT');
```

```
+----------------+-----------+-----------------------------------------------------+
| ACT_SCENE_LINE | CHARACTER | LINE                                                |
|----------------+-----------+-----------------------------------------------------|
| 2.1.53         | ACHILLES  | Why, how now, Ajax! wherefore do you thus? How now, |
+----------------+-----------+-----------------------------------------------------+
```

Common use cases for phrase-match and exact-match semantics include finding email addresses, URLs, and phone
numbers. For the next examples, create a table with one row of sample data:

Copy code

```
CREATE OR REPLACE TABLE phrase_exact_search_samples (
  email VARCHAR,
  url VARCHAR,
  phone VARCHAR);

INSERT INTO phrase_exact_search_samples VALUES (
  'john.robert.doe@mycompany.com',
  'http://mycompany.com/product/id-12345.67',
  '800-555-0100');
```

The following example runs a query that uses conjunctive semantics to search the email data by setting the SEARCH\_MODE
argument to `'AND'` in the first search, phrase-match semantics in the second search, and exact-match semantics
in the third search:

Copy code

```
SELECT email AS search_data,
       SEARCH(email, 'doe.john.robert@mycompany.com', SEARCH_MODE => 'AND') AS conjunctive_search,
       SEARCH(email, 'doe.john.robert@mycompany.com', SEARCH_MODE => 'PHRASE') AS phrase_search,
       SEARCH(email, 'doe.john.robert@mycompany.com', SEARCH_MODE => 'EXACT') AS exact_search
  FROM phrase_exact_search_samples;
```

The output shows the following results:

- `AND` search returns TRUE even though the terms `john`, `robert`, and `doe` are in a different
  order in the search string and the search data.
- `PHRASE` and `EXACT` search return FALSE because the search terms don’t match the order of the
  search string.

```
+-------------------------------+--------------------+---------------+--------------+
| SEARCH_DATA                   | CONJUNCTIVE_SEARCH | PHRASE_SEARCH | EXACT_SEARCH |
|-------------------------------+--------------------+---------------+--------------|
| john.robert.doe@mycompany.com | True               | False         | False        |
+-------------------------------+--------------------+---------------+--------------+
```

The following example runs a query that uses conjunctive semantics to search the email data by setting
the SEARCH\_MODE argument to `'AND'` in the first search, phrase-match semantics in the second search, and exact-match
semantics in the third search:

Copy code

```
SELECT email AS search_data,
       SEARCH(email, 'john.doe@mycompany.com', SEARCH_MODE => 'AND') AS conjunctive_search,
       SEARCH(email, 'john.doe@mycompany.com', SEARCH_MODE => 'PHRASE') AS phrase_search,
       SEARCH(email, 'john.doe@mycompany.com', SEARCH_MODE => 'EXACT') AS exact_search
  FROM phrase_exact_search_samples;
```

The output shows the following results:

- `AND` search returns TRUE even though the additional token `robert` is interspersed in the search data.
- `PHRASE` and `EXACT` search return FALSE because these search semantics don’t find a match when
  additional tokens are interspersed in the search data.

```
+-------------------------------+--------------------+---------------+--------------+
| SEARCH_DATA                   | CONJUNCTIVE_SEARCH | PHRASE_SEARCH | EXACT_SEARCH |
|-------------------------------+--------------------+---------------+--------------|
| john.robert.doe@mycompany.com | True               | False         | False        |
+-------------------------------+--------------------+---------------+--------------+
```

The following example runs a query that uses phrase-search semantics to search the email
data in the first search and exact-match semantics in the second search:

Copy code

```
SELECT email AS search_data,
       SEARCH(email, 'john-robert-doe@mycompany.com', SEARCH_MODE => 'PHRASE') AS phrase_search,
       SEARCH(email, 'john-robert-doe@mycompany.com', SEARCH_MODE => 'EXACT') AS exact_search
  FROM phrase_exact_search_samples;
```

The output shows that the `PHRASE` search returns TRUE even though the delimiters in the email address in the
search string are hyphens instead of periods between `john`, `robert`, and `doe`. The `EXACT` search returns
FALSE because, with exact-match semantics, the delimiters in the search string must exactly match the search
data:

```
+-------------------------------+---------------+--------------+
| SEARCH_DATA                   | PHRASE_SEARCH | EXACT_SEARCH |
|-------------------------------+---------------+--------------|
| john.robert.doe@mycompany.com | True          | False        |
+-------------------------------+---------------+--------------+
```

The following example runs a query that uses phrase-search semantics to search the URL data in the first search
and exact-match semantics in the second search:

Copy code

```
SELECT url AS search_data,
       SEARCH(url, 'http://mycompany.com/product/id-12345_67', SEARCH_MODE => 'PHRASE') AS phrase_search,
       SEARCH(url, 'http://mycompany.com/product/id-12345_67', SEARCH_MODE => 'EXACT') AS exact_search
  FROM phrase_exact_search_samples;
```

The output shows that the `PHRASE` search returns TRUE even though the delimiter in the URL in the search string is an
underscore instead of a period in the product ID. The `EXACT` search returns FALSE:

```
+------------------------------------------+---------------+--------------+
| SEARCH_DATA                              | PHRASE_SEARCH | EXACT_SEARCH |
|------------------------------------------+---------------+--------------|
| http://mycompany.com/product/id-12345.67 | True          | False        |
+------------------------------------------+---------------+--------------+
```

The following example runs a query that uses phrase-search semantics to search the phone number data in the first search
and exact-match semantics in the second search:

Copy code

```
SELECT phone AS search_data,
       SEARCH(phone, '800.555.0100', SEARCH_MODE => 'PHRASE') AS phrase_search,
       SEARCH(phone, '800.555.0100', SEARCH_MODE => 'EXACT') AS exact_search
  FROM phrase_exact_search_samples;
```

The output shows that the `PHRASE` search returns TRUE even though the delimiters in the phone number in the
search string are periods instead of hyphens. The `EXACT` search returns FALSE:

```
+--------------+---------------+--------------+
| SEARCH_DATA  | PHRASE_SEARCH | EXACT_SEARCH |
|--------------+---------------+--------------|
| 800-555-0100 | True          | False        |
+--------------+---------------+--------------+
```

The following examples use the SEARCH function in a WHERE clause to query the `phrase_exact_search_samples` table.
First, insert another row into the table:

Copy code

```
INSERT INTO phrase_exact_search_samples VALUES (
  'jane.smith@mycompany.com',
  'http://mycompany.com/product/id-89012.34',
  '800-555-0199');
```

The following example searches for an exact match of the phone number `800-555-0100` in the table data:

Copy code

```
SELECT *
  FROM phrase_exact_search_samples
  WHERE SEARCH(phone, '800-555-0100', SEARCH_MODE => 'EXACT');
```

```
+-------------------------------+------------------------------------------+--------------+
| EMAIL                         | URL                                      | PHONE        |
|-------------------------------+------------------------------------------+--------------|
| john.robert.doe@mycompany.com | http://mycompany.com/product/id-12345.67 | 800-555-0100 |
+-------------------------------+------------------------------------------+--------------+
```

The following example is the same as the previous example, but it uses disjunctive semantics instead of
exact-match semantics so that any phone number that contains `800` or `555` is a match:

Copy code

```
SELECT *
  FROM phrase_exact_search_samples
  WHERE SEARCH(phone, '800-555-0100', SEARCH_MODE => 'OR');
```

```
+-------------------------------+------------------------------------------+--------------+
| EMAIL                         | URL                                      | PHONE        |
|-------------------------------+------------------------------------------+--------------|
| john.robert.doe@mycompany.com | http://mycompany.com/product/id-12345.67 | 800-555-0100 |
| jane.smith@mycompany.com      | http://mycompany.com/product/id-89012.34 | 800-555-0199 |
+-------------------------------+------------------------------------------+--------------+
```

### Searching VARIANT and VARCHAR data in a join

The following example shows a join of two tables, `car_rentals` and `car_sales`, with the search applied
to columns in both tables. The `car_sales` table contains VARIANT data. The `car_sales` table and its data
are described under [Querying Semi-structured Data](/user-guide/querying-semistructured). The following SQL statements create the
`car_rentals` table and insert data into it:

Copy code

```
CREATE OR REPLACE TABLE car_rentals(
  vehicle_make VARCHAR(30),
  dealership VARCHAR(30),
  salesperson VARCHAR(30));

INSERT INTO car_rentals VALUES
  ('Toyota', 'Tindel Toyota', 'Greg Northrup'),
  ('Honda', 'Valley View Auto Sales', 'Frank Beasley'),
  ('Tesla', 'Valley View Auto Sales', 'Arturo Sandoval');
```

Run the query:

Copy code

```
SELECT SEARCH((r.vehicle_make, r.dealership, s.src:dealership), 'Toyota Tesla')
    AS contains_toyota_tesla, r.vehicle_make, r.dealership,s.src:dealership
  FROM car_rentals r JOIN car_sales s
    ON r.SALESPERSON=s.src:salesperson.name;
```

```
+-----------------------+--------------+------------------------+--------------------------+
| CONTAINS_TOYOTA_TESLA | VEHICLE_MAKE | DEALERSHIP             | S.SRC:DEALERSHIP         |
|-----------------------+--------------+------------------------+--------------------------|
| True                  | Toyota       | Tindel Toyota          | "Tindel Toyota"          |
| False                 | Honda        | Valley View Auto Sales | "Valley View Auto Sales" |
+-----------------------+--------------+------------------------+--------------------------+
```

In this second example, against the same data, different search terms are used:

Copy code

```
SELECT SEARCH((r.vehicle_make, r.dealership, s.src:dealership), 'Toyota Honda')
    AS contains_toyota_honda, r.vehicle_make, r.dealership, s.src:dealership
  FROM car_rentals r JOIN car_sales s
    ON r.SALESPERSON =s.src:salesperson.name;
```

```
+-----------------------+--------------+------------------------+--------------------------+
| CONTAINS_TOYOTA_HONDA | VEHICLE_MAKE | DEALERSHIP             | S.SRC:DEALERSHIP         |
|-----------------------+--------------+------------------------+--------------------------|
| True                  | Toyota       | Tindel Toyota          | "Tindel Toyota"          |
| True                  | Honda        | Valley View Auto Sales | "Valley View Auto Sales" |
+-----------------------+--------------+------------------------+--------------------------+
```

### Using an analyzer to adjust search behavior

The following examples show how to adjust the behavior of the SEARCH function by specifying a
non-default analyzer: `'UNICODE_ANALYZER'` or `'NO_OP_ANALYZER'`.

The first example uses the `'NO_OP_ANALYZER'` to test whether the string `1.2.500` matches the exact contents
of the `act_scene_line` column for any row in the `lines` table. Two rows qualify for the search.

Copy code

```
SELECT line_id, act_scene_line FROM lines
  WHERE SEARCH(act_scene_line, '1.2.500', ANALYZER=>'NO_OP_ANALYZER');
```

```
+---------+----------------+
| LINE_ID | ACT_SCENE_LINE |
|---------+----------------|
|   91998 | 1.2.500        |
|  108464 | 1.2.500        |
+---------+----------------+
```

If you remove `'NO_OP_ANALYZER'` as an argument to the function for this example, the search returns a large
number of rows. The default analyzer treats `1`, `2`, and `500` as distinct tokens; therefore, the function
returns TRUE for all of the rows where `1`, `2`, or `500` exist in any order or combination.

If you change this query to include only the prefix `1.2` for the second argument, the default analyzer
returns TRUE, but the `'UNICODE_ANALYZER'` and `'NO_OP_ANALYZER'` both return FALSE. The default analyzer treats
periods in these values as delimiters, but the Unicode analyzer doesn’t.

The following two queries show another effect of using the `'UNICODE_ANALYZER'` instead of the default analyzer. The
first query, using the `'UNICODE_ANALYZER'`, returns only one row. The extra single quote in the second
argument is there to escape the single quote for the apostrophe. See [Single-quoted string constants](/sql-reference/data-types-text#label-single-quoted-string-constants).

Copy code

```
SELECT DISTINCT(play)
  FROM lines
  WHERE SEARCH(play, 'love''s', ANALYZER=>'UNICODE_ANALYZER');
```

```
+----------------------+
| PLAY                 |
|----------------------|
| Love's Labour's Lost |
+----------------------+
```

The second query, using the default analyzer, returns four rows because the default analyzer treats the apostrophe
character as a delimiter. Any string that contains the letter “s” as a token qualifies for the search.
In this example, the function returns TRUE for every string that contains an “apostrophe s” (`'s`).

Copy code

```
SELECT DISTINCT(play) FROM lines WHERE SEARCH(play, 'love''s');
```

```
+---------------------------+
| PLAY                      |
|---------------------------|
| All's Well That Ends Well |
| Love's Labour's Lost      |
| A Midsummer Night's Dream |
| The Winter's Tale         |
+---------------------------+
```

### Examples of expected error cases

The following examples show queries that return expected syntax errors.

This example fails because `5` is not a supported data type for the `search_string` argument.

Copy code

```
SELECT SEARCH(line, 5) FROM lines;
```

```
001045 (22023): SQL compilation error:
argument needs to be a string: '1'
```

This example fails because there is no column of a supported data type specified for the `search_data` argument.

Copy code

```
SELECT SEARCH(line_id, 'dream') FROM lines;
```

```
001173 (22023): SQL compilation error: error line 1 at position 7: Expected non-empty set of columns supporting full-text search.
```

This example succeeds because there is a column of a supported data type specified for the `search_data` argument. The function
ignores the `line_id` column because it is not a supported data type

Copy code

```
SELECT SEARCH((line_id, play), 'dream') FROM lines
  ORDER BY play LIMIT 5;
```

```
+----------------------------------+
| SEARCH((LINE_ID, PLAY), 'DREAM') |
|----------------------------------|
| True                             |
| True                             |
| False                            |
| False                            |
| False                            |
+----------------------------------+
```

This example fails because multiple string literals are listed for the first argument, without
parentheses, resulting in mismatched arguments:

Copy code

```
SELECT SEARCH('docs@snowflake.com', 'careers@snowflake.com', '@');
```

```
001881 (42601): SQL compilation error: Expected 1 named argument(s), found 0
```

This example fails because multiple column names are listed for the first argument, without
parentheses, resulting in too many arguments:

Copy code

```
SELECT SEARCH(play,line,'king', ANALYZER=>'UNICODE_ANALYZER') FROM lines;
```

```
000939 (22023): SQL compilation error: error line 1 at position 7
too many arguments for function [SEARCH(LINES.PLAY, LINES.LINE, 'king', 'UNICODE_ANALYZER')] expected 3, got 4
```

This example fails because a column name is not accepted as the search string argument.

Copy code

```
SELECT SEARCH(line, character) FROM lines;
```

```
001015 (22023): SQL compilation error:
argument 2 to function SEARCH needs to be constant, found 'LINES.CHARACTER'
```

### Creating the sample data for SEARCH

Some of the examples in this section query a table that contains text from Shakespeare’s plays.
Each line of text is stored in a single row of the table. Other columns identify the name of the play,
the name of the character, and so on. The `lines` table has the following structure:

Copy code

```
DESCRIBE TABLE lines;
```

```
+----------------+---------------+--------+-------+-
| name           | type          | kind   | null? |
|----------------+---------------+--------+-------+-
| LINE_ID        | NUMBER(38,0)  | COLUMN | Y     |
| PLAY           | VARCHAR(50)   | COLUMN | Y     |
| SPEECH_NUM     | NUMBER(38,0)  | COLUMN | Y     |
| ACT_SCENE_LINE | VARCHAR(10)   | COLUMN | Y     |
| CHARACTER      | VARCHAR(30)   | COLUMN | Y     |
| LINE           | VARCHAR(2000) | COLUMN | Y     |
+----------------+---------------+--------+-------+-
```

For example, a single line in this table looks like this:

Copy code

```
SELECT * FROM lines
  WHERE line_id=34230;
```

```
+---------+--------+------------+----------------+-----------+--------------------------------------------+
| LINE_ID | PLAY   | SPEECH_NUM | ACT_SCENE_LINE | CHARACTER | LINE                                       |
|---------+--------+------------+----------------+-----------+--------------------------------------------|
|   34230 | Hamlet |         19 | 3.1.64         | HAMLET    | To be, or not to be, that is the question: |
+---------+--------+------------+----------------+-----------+--------------------------------------------+
```

If you want to run the examples in this section, create this table by running the following commands:

Copy code

```
CREATE OR REPLACE TABLE lines(
  line_id INT,
  play VARCHAR(50),
  speech_num INT,
  act_scene_line VARCHAR(10),
  character VARCHAR(30),
  line VARCHAR(2000)
  );

INSERT INTO lines VALUES
  (4,'Henry IV Part 1',1,'1.1.1','KING HENRY IV','So shaken as we are, so wan with care,'),
  (13,'Henry IV Part 1',1,'1.1.10','KING HENRY IV','Which, like the meteors of a troubled heaven,'),
  (9526,'Henry VI Part 3',1,'1.1.1','WARWICK','I wonder how the king escaped our hands.'),
  (12664,'All''s Well That Ends Well',1,'1.1.1','COUNTESS','In delivering my son from me, I bury a second husband.'),
  (15742,'All''s Well That Ends Well',114,'5.3.378','KING','Your gentle hands lend us, and take our hearts.'),
  (16448,'As You Like It',2,'2.3.6','ADAM','And wherefore are you gentle, strong and valiant?'),
  (24055,'The Comedy of Errors',14,'5.1.41','AEMELIA','Be quiet, people. Wherefore throng you hither?'),
  (28487,'Cymbeline',3,'1.1.10','First Gentleman','Is outward sorrow, though I think the king'),
  (33522,'Hamlet',1,'2.2.1','KING CLAUDIUS','Welcome, dear Rosencrantz and Guildenstern!'),
  (33556,'Hamlet',5,'2.2.35','KING CLAUDIUS','Thanks, Rosencrantz and gentle Guildenstern.'),
  (33557,'Hamlet',6,'2.2.36','QUEEN GERTRUDE','Thanks, Guildenstern and gentle Rosencrantz:'),
  (33776,'Hamlet',67,'2.2.241','HAMLET','Guildenstern? Ah, Rosencrantz! Good lads, how do ye both?'),
  (34230,'Hamlet',19,'3.1.64','HAMLET','To be, or not to be, that is the question:'),
  (35672,'Hamlet',7,'4.6.27','HORATIO','where I am. Rosencrantz and Guildenstern hold their'),
  (36289,'Hamlet',14,'5.2.60','HORATIO','So Guildenstern and Rosencrantz go to''t.'),
  (36640,'Hamlet',143,'5.2.389','First Ambassador','That Rosencrantz and Guildenstern are dead:'),
  (43494,'King John',1,'1.1.1','KING JOHN','Now, say, Chatillon, what would France with us?'),
  (43503,'King John',5,'1.1.10','CHATILLON','To this fair island and the territories,'),
  (49031,'King Lear',1,'1.1.1','KENT','I thought the king had more affected the Duke of'),
  (49040,'King Lear',4,'1.1.10','GLOUCESTER','so often blushed to acknowledge him, that now I am'),
  (52797,'Love''s Labour''s Lost',1,'1.1.1','FERDINAND','Let fame, that all hunt after in their lives,'),
  (55778,'Love''s Labour''s Lost',405,'5.2.971','ADRIANO DE ARMADO','Apollo. You that way: we this way.'),
  (67000,'A Midsummer Night''s Dream',1,'1.1.1','THESEUS','Now, fair Hippolyta, our nuptial hour'),
  (69296,'A Midsummer Night''s Dream',104,'5.1.428','PUCK','And Robin shall restore amends.'),
  (75787,'Pericles',178,'1.0.21','LODOVICO','This king unto him took a fere,'),
  (78407,'Richard II',1,'1.1.1','KING RICHARD II','Old John of Gaunt, time-honour''d Lancaster,'),
  (91998,'The Tempest',108,'1.2.500','FERDINAND','Were I but where ''tis spoken.'),
  (92454,'The Tempest',150,'2.1.343','ALONSO','Wherefore this ghastly looking?'),
  (99330,'Troilus and Cressida',30,'1.1.102','AENEAS','How now, Prince Troilus! wherefore not afield?'),
  (100109,'Troilus and Cressida',31,'2.1.53','ACHILLES','Why, how now, Ajax! wherefore do you thus? How now,'),
  (108464,'The Winter''s Tale',106,'1.2.500','CAMILLO','As or by oath remove or counsel shake')
  ;
```
