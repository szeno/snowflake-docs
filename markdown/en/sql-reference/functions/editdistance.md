Categories:
:   [String & binary functions](/sql-reference/functions-string) (Matching/Comparison)

# EDITDISTANCE

Computes the Levenshtein distance between two input strings. It is the number
of single-character insertions, deletions, or substitutions needed to convert
one string to another.

Note

Unlike some other metrics (for example, Damerau-Levenshtein distance), character
transpositions aren’t considered.

## Syntax

Copy code

```
EDITDISTANCE( <string_expr1> , <string_expr2> [ , <max_distance> ] )
```

## Arguments

**Required:**

`string_expr1`, `string_expr2`
:   The input strings.

**Optional:**

`max_distance`
:   Integer expression that specifies the maximum distance to compute.

    When the distance between the strings exceeds this number, the function stops computing the distance and just returns the
    maximum distance.

    Specifying this argument has the same effect as calling
    `LEAST( EDITDISTANCE( string_expr1, string_expr2 ), max_distance )`.

    If you specify a negative number (that is, `-n`), the function uses `0` as the maximum distance and returns `0`.

## Usage notes

- The execution time of the EDITDISTANCE function is proportional to the product of the lengths of the input strings.
- For better performance, Snowflake recommends using input strings not longer than 4096 characters.

  Input strings longer than 128 MB might result in an error.

  You can also use the optional `max_distance` argument to set an upper bound for the distance computed.

## Collation details

No impact.
In languages where the alphabet contains digraphs or trigraphs (such as “Dz” and “Dzs” in Hungarian), each character in each digraph and trigraph is treated as an independent character, not as part of a single multi-character letter.

The result is based solely on the characters in the strings, not on the collation specifications of the strings.

## Examples

The following example computes the distance between the strings in the columns `s` and `t` in the table `ed`.

The last two columns use the `max_distance` argument to specify the maximum distance to compute:

- When `max_distance` is `3`, the function returns `3` if the distance between the strings is greater than or equal to
  3 (as shown below).
- If `max_distance` is a negative number (for example, `-1`, as shown below), the function uses `0` as the maximum distance
  and returns `0`.

Copy code

```
SELECT s,
       t,
       EDITDISTANCE(s, t),
       EDITDISTANCE(t, s),
       EDITDISTANCE(s, t, 3),
       EDITDISTANCE(s, t, -1)
  FROM ed;
```

```
+----------------+-----------------+--------------------+--------------------+-----------------------+------------------------+
|      S         |        T        | EDITDISTANCE(S, T) | EDITDISTANCE(T, S) | EDITDISTANCE(S, T, 3) | EDITDISTANCE(S, T, -1) |
|----------------+-----------------+--------------------+--------------------+-----------------------+------------------------|
|                |                 | 0                  | 0                  | 0                     | 0                      |
| Gute nacht     | Ich weis nicht  | 8                  | 8                  | 3                     | 0                      |
| Ich weiß nicht | Ich wei? nicht  | 1                  | 1                  | 1                     | 0                      |
| Ich weiß nicht | Ich weiss nicht | 2                  | 2                  | 2                     | 0                      |
| Ich weiß nicht | [NULL]          | [NULL]             | [NULL]             | [NULL]                | [NULL]                 |
| Snowflake      | Oracle          | 7                  | 7                  | 3                     | 0                      |
| święta         | swieta          | 2                  | 2                  | 2                     | 0                      |
| [NULL]         |                 | [NULL]             | [NULL]             | [NULL]                | [NULL]                 |
| [NULL]         | [NULL]          | [NULL]             | [NULL]             | [NULL]                | [NULL]                 |
+----------------+-----------------+--------------------+--------------------+-----------------------+------------------------+
```

The next example returns `FALSE` if the distance between two strings is at least 2. Because `max_distance` is
specified as `2`, the function stops calculating the distance once the distance is determined to be at least 2. (The actual
distance between the input strings is 6.)

Copy code

```
SELECT EDITDISTANCE('future', 'past', 2) < 2;
```

```
+---------------------------------------+
| EDITDISTANCE('FUTURE', 'PAST', 2) < 2 |
|---------------------------------------|
| False                                 |
+---------------------------------------+
```
