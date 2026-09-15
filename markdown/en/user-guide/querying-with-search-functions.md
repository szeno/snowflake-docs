# Using full-text search

You can use search functions to find character data (text) and IP addresses in specified columns from one or
more tables, including fields in VARIANT, OBJECT, and ARRAY columns. This function searches the text in specified
columns or strings based on a list of given search terms. The function returns TRUE if the text matches the
specified search terms based on the search semantics.

In most cases, you call the SEARCH function by specifying it in the SELECT list or the WHERE clause of a SELECT statement.
If the function is used as a WHERE clause filter, the query returns rows when the function returns TRUE.

The SEARCH function requires no setup and no additional privileges. If you’re using a role that has the
privileges to access the data in a column, you can search for that data by using the SEARCH function.

The next sections contain more information about the SEARCH function and about optimizing query performance when you
use it:

- [Using the SEARCH function](#label-querying-with-search-functions-search)
- [Using the SEARCH\_IP function](#label-querying-with-search-functions-search-ip)
- [Optimizing queries that use the SEARCH function](#label-querying-with-search-functions-optimizing)

## Using the SEARCH function

The [SEARCH function](/sql-reference/functions/search) finds character data (text) in specified columns from one
or more tables, including fields in VARIANT, OBJECT, and ARRAY columns.

When you use the SEARCH function, a text analyzer breaks the text into *tokens*, which are discrete units of text, such
as words or numbers. A default analyzer is applied if you don’t specify one. The analyzer extracts tokens from both the
search terms and the data.

If tokens extracted from the search terms match tokens extracted from a specified column or field according to the
search semantics, the function returns TRUE. The SEARCH\_MODE function argument specifies one of the following search
modes:

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

The following example searches for the string `snow leopard` in the text `leopard` with the default SEARCH\_MODE (`'OR'`)
and the default analyzer:

Copy code

```
SELECT SEARCH('leopard', 'snow leopard');
```

```
+-----------------------------------+
| SEARCH('LEOPARD', 'SNOW LEOPARD') |
|-----------------------------------|
| True                              |
+-----------------------------------+
```

The following example searches for the string `snow leopard` in the text `lion`:

Copy code

```
SELECT SEARCH('lion', 'snow leopard');
```

```
+--------------------------------+
| SEARCH('LION', 'SNOW LEOPARD') |
|--------------------------------|
| False                          |
+--------------------------------+
```

The following example searches for the string `snow leopard` in the text `leopard` and specifies `'AND'` for the
SEARCH\_MODE argument:

Copy code

```
SELECT SEARCH('leopard', 'snow leopard', search_mode => 'AND');
```

```
+---------------------------------------------------------+
| SEARCH('LEOPARD', 'SNOW LEOPARD', SEARCH_MODE => 'AND') |
|---------------------------------------------------------|
| False                                                   |
+---------------------------------------------------------+
```

For more information about this function and additional examples, see [SEARCH](/sql-reference/functions/search).

## Using the SEARCH\_IP function

The [SEARCH\_IP function](/sql-reference/functions/search_ip) finds valid IPv4 and IPv6 addresses in specified character-string
columns from one or more tables, including fields in VARIANT, OBJECT, and ARRAY columns. The search is based on a single IP
address that you specify. If this IP address exactly matches an IP address in the specified column or field, the function
returns TRUE.

The following example searches for the IP address `10.10.10.1` in the text `192.0.2.146`:

Copy code

```
SELECT SEARCH_IP('192.0.2.146','10.10.10.1');
```

```
+---------------------------------------+
| SEARCH_IP('192.0.2.146','10.10.10.1') |
|---------------------------------------|
| False                                 |
+---------------------------------------+
```

For more information about this function and additional examples, see [SEARCH\_IP](/sql-reference/functions/search_ip).

## Optimizing queries that use the SEARCH function

To improve the performance of queries that use the function, you can optionally [enable FULL\_TEXT search optimization](/user-guide/search-optimization/enabling#label-enable-full-text-search) on a specific column or set of columns in a table. When you enable search
optimization, a new [search access path](/user-guide/search-optimization-service#label-search-optimization-service-how-it-works) is built and maintained.
