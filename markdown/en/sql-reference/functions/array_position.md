Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# ARRAY\_POSITION

Returns the index of the first occurrence of an element in an array.

## Syntax

Copy code

```
ARRAY_POSITION( <value_expr> , <array> )
```

## Arguments

`value_expr`
:   Value to find in `array`.

    - If `array` is a [semi-structured ARRAY](/sql-reference/data-types-semistructured#label-data-type-array), `value_expr` must evaluate to a
      [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant).
    - If `array` is a [structured ARRAY](/sql-reference/data-types-structured), `value_expr` must evaluate
      to a type that is [comparable](/sql-reference/data-types-structured#label-structured-types-compare-struct-struct) to the type of the ARRAY.

`array`
:   The ARRAY to search.

## Returns

The function returns an INTEGER specifying the position of `value_expr` in `array`.

## Usage notes

- The return value is 0-based, not 1-based. In other words, if the `value_expr` matches the first element in the array,
  this function returns 0, not 1.
- If the value is not contained in the ARRAY, the function returns NULL.
- If you specify NULL for `value_expr`, the function returns the position of the first NULL in the array.

## Examples

The examples below show how to use this function:

> Copy code
>
> ```
> SELECT ARRAY_POSITION('hello'::variant, array_construct('hello', 'hi'));
> +------------------------------------------------------------------+
> | ARRAY_POSITION('HELLO'::VARIANT, ARRAY_CONSTRUCT('HELLO', 'HI')) |
> |------------------------------------------------------------------|
> |                                                                0 |
> +------------------------------------------------------------------+
> ```
>
> Copy code
>
> ```
> SELECT ARRAY_POSITION('hi'::variant, array_construct('hello', 'hi'));
> +---------------------------------------------------------------+
> | ARRAY_POSITION('HI'::VARIANT, ARRAY_CONSTRUCT('HELLO', 'HI')) |
> |---------------------------------------------------------------|
> |                                                             1 |
> +---------------------------------------------------------------+
> ```
>
> Copy code
>
> ```
> SELECT ARRAY_POSITION('hello'::variant, array_construct('hola', 'bonjour'));
> +----------------------------------------------------------------------+
> | ARRAY_POSITION('HELLO'::VARIANT, ARRAY_CONSTRUCT('HOLA', 'BONJOUR')) |
> |----------------------------------------------------------------------|
> |                                                                 NULL |
> +----------------------------------------------------------------------+
> ```
