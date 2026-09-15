Categories:
:   [String & binary functions](/sql-reference/functions-string) (Matching/Comparison)

# JAROWINKLER\_SIMILARITY

Computes the [Jaro-Winkler similarity](https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance) between two input strings.
The function returns an integer between 0 and 100, where 0 indicates no similarity and 100 indicates an exact match.

Note

- The similarity computation is case-insensitive.
- The computation is sensitive to all formatting characters, including white space characters.
- The default [scaling factor](https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance#Jaro%E2%80%93Winkler_Similarity)
  of 0.1 is used for the computation.

## Syntax

Copy code

```
JAROWINKLER_SIMILARITY( <string_expr1> , <string_expr2> )
```

## Arguments

**Required:**

`string_expr1`, `string_expr2`
:   The input strings.

## Usage notes

- When the function compares short strings, the execution time is proportional to the product of the lengths of the input strings.
- When the function compares long strings, the execution time is proportional to the length of the longer string.

## Collation details

No impact.
In languages where the alphabet contains digraphs or trigraphs (such as “Dz” and “Dzs” in Hungarian), each character in each digraph and trigraph is treated as an independent character, not as part of a single multi-character letter.

The result is based solely on the characters in the strings, not on the collation specifications of the strings.

## Examples

The following example computes the similarity between the strings in the columns `s` and `t` in the table `ed`.

Copy code

```
SELECT s, t, JAROWINKLER_SIMILARITY(s, t), JAROWINKLER_SIMILARITY(t, s) FROM ed;

----------------+-----------------+------------------------------+------------------------------+
      S         |        T        | JAROWINKLER_SIMILARITY(S, T) | JAROWINKLER_SIMILARITY(T, S) |
----------------+-----------------+------------------------------+------------------------------+
                |                 | 0                            | 0                            |
 Gute nacht     | Ich weis nicht  | 56                           | 56                           |
 Ich weiß nicht | Ich wei? nicht  | 98                           | 98                           |
 Ich weiß nicht | Ich weiss nicht | 97                           | 97                           |
 Ich weiß nicht | [NULL]          | [NULL]                       | [NULL]                       |
 Snowflake      | Oracle          | 61                           | 61                           |
 święta         | swieta          | 77                           | 77                           |
 [NULL]         |                 | [NULL]                       | [NULL]                       |
 [NULL]         | [NULL]          | [NULL]                       | [NULL]                       |
----------------+-----------------+------------------------------+------------------------------+
```
