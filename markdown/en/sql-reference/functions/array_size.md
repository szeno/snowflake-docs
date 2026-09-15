Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# ARRAY\_SIZE

Returns the size of the input array.

A variation of ARRAY\_SIZE takes a VARIANT value as input. If the VARIANT value contains an array, the size of the array is returned; otherwise, NULL is returned if the value is not an array.

## Syntax

Copy code

```
ARRAY_SIZE( <array> )

ARRAY_SIZE( <variant> )
```

## Returns

The data type of the returned value is `INTEGER`.

## Usage notes

- Takes an ARRAY value as input and returns the size of the array (i.e. the largest index + 1).

  If the array is a [sparse](/sql-reference/data-types-semistructured#label-sparse-arrays) array, this means that the size includes the undefined elements as
  well as the defined elements.
- A NULL argument returns NULL as a result.

## Examples

Here is a simple example:

> Copy code
>
> ```
> SELECT ARRAY_SIZE(ARRAY_CONSTRUCT(1, 2, 3)) AS SIZE;
> +------+
> | SIZE |
> |------|
> |    3 |
> +------+
> ```

Here is a slightly more complex example, this time using VARIANT data type:

> Copy code
>
> ```
> CREATE OR replace TABLE colors (v variant);
>
> INSERT INTO
>    colors
>    SELECT
>       parse_json(column1) AS v
>    FROM
>    VALUES
>      ('[{r:255,g:12,b:0},{r:0,g:255,b:0},{r:0,g:0,b:255}]'),
>      ('[{r:255,g:128,b:0},{r:128,g:255,b:0},{r:0,g:255,b:128},{r:0,g:128,b:255},{r:128,g:0,b:255},{r:255,g:0,b:128}]')
>     v;
> ```
>
> Retrieve the size for each array in the VARIANT column:
>
> Copy code
>
> ```
> SELECT ARRAY_SIZE(v) from colors;
> +---------------+
> | ARRAY_SIZE(V) |
> |---------------|
> |             3 |
> |             6 |
> +---------------+
> ```
>
> Retrieve the last element of each array in the VARIANT column:
>
> Copy code
>
> ```
> SELECT GET(v, ARRAY_SIZE(v)-1) FROM colors;
> +-------------------------+
> | GET(V, ARRAY_SIZE(V)-1) |
> |-------------------------|
> | {                       |
> |   "b": 255,             |
> |   "g": 0,               |
> |   "r": 0                |
> | }                       |
> | {                       |
> |   "b": 128,             |
> |   "g": 0,               |
> |   "r": 255              |
> | }                       |
> +-------------------------+
> ```
