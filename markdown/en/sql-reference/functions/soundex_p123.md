Categories:
:   [String & binary functions](/sql-reference/functions-string)

# SOUNDEX\_P123

Returns a string that contains a phonetic representation of the input string, and retains the Soundex code number for the second
letter when the first and second letters use the same number.

This function is similar to the [SOUNDEX](/sql-reference/functions/soundex) function except for cases in which the first and second letters of the input string
use the same Soundex code number. In those cases, the SOUNDEX function ignores the number for the second letter, while the
SOUNDEX\_P123 function preserves the number for the second letter. This variant of the Soundex algorithm is used by some database
systems (e.g. Teradata).

For example, for the input string `Pfister`, the first two letters (`P` and `f`) are adjacent and share the same Soundex
code number (`1`).

- `SOUNDEX('Pfister')` ignores the Soundex code number for the second letter (`1`) and returns `P236`.
- `SOUNDEX_P123('Pfister')` preserves the Soundex code number for the second letter and returns `P123`.

See also:
:   [SOUNDEX](/sql-reference/functions/soundex)

## Syntax

Copy code

```
SOUNDEX_P123( <varchar_expr> )
```

## Arguments

`varchar_expr`
:   The string for which a representation of the pronunciation is returned. The string should use the Latin or Unicode character set.

## Returns

The returned value is a VARCHAR that contains the phonetic representation of the input string. In other words, the return value
is a string (not a sound) that represents the pronunciation (not the spelling) of the input string.

As mentioned earlier, if the first and second letters use the same Soundex code, the function retains the Soundex code number for
the second letter.

For additional information, see [Returns](/sql-reference/functions/soundex#label-soundex-return-value) in the documentation for the [SOUNDEX](/sql-reference/functions/soundex) function.

## Usage notes

See [Usage notes](/sql-reference/functions/soundex#label-soundex-usage-notes) in the documentation for the [SOUNDEX](/sql-reference/functions/soundex) function.

## Examples

The following example demonstrates the differences in the return values of the [SOUNDEX](/sql-reference/functions/soundex) function and the SOUNDEX\_P123
function:

> Copy code
>
> ```
> SELECT SOUNDEX('Pfister'),
>        SOUNDEX_P123('Pfister'),
>        SOUNDEX('LLoyd'),
>        SOUNDEX_P123('Lloyd');
> +--------------------+-------------------------+------------------+-----------------------+
> | SOUNDEX('Pfister') | SOUNDEX_P123('Pfister') | SOUNDEX('Lloyd') | SOUNDEX_P123('Lloyd') |
> |--------------------+-------------------------+------------------+-----------------------|
> | P236               | P123                    | L300             | L430                  |
> +--------------------+-------------------------+------------------+-----------------------+
> ```
