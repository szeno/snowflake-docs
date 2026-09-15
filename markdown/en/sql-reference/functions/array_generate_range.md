Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# ARRAY\_GENERATE\_RANGE

Returns an [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) of integer values within a specified range (e.g. `[2, 3, 4]`).

## Syntax

Copy code

```
ARRAY_GENERATE_RANGE( <start> , <stop> [ , <step> ] )
```

## Arguments

**Required:**

`start`
:   The first number in the range of numbers to return.

    You must specify an expression that evaluates to an INTEGER value.

`stop`
:   The last number in the range. Note that this number is not included in the range of numbers returned.

    For example, `ARRAY_GENERATE_RANGE(1, 5)` returns `[1, 2, 3, 4]` (which does not include `5`).

    You must specify an expression that evaluates to an INTEGER value.

**Optional:**

`step`
:   The amount to increment or decrement each subsequent number in the array. For example:

    - `ARRAY_GENERATE_RANGE(0, 16, 5)` returns `[0, 5, 10, 15]`
    - `ARRAY_GENERATE_RANGE(0, -16, -5)` returns `[0, -5, -10, -15]`

    You can specify a positive or negative number. You cannot specify 0.

    The default value is `1`.

## Returns

An ARRAY of integers in the specified range.

If any of the arguments is NULL, the function returns NULL.

## Usage notes

- After `start`, each subsequent element increases or decreases by `step` (depending on whether `step`
  is positive or negative) up to (but not including) `stop`.

  For example:

  - `ARRAY_GENERATE_RANGE(10, 50, 10)` returns `[10, 20, 30, 40]`.
  - `ARRAY_GENERATE_RANGE(-10, -50, -10)` returns `[-10, -20, -30, -40]`.
- The function returns an empty ARRAY under any of the following conditions:

  - `start = stop`.
  - `step` is a positive number and `start > stop`.
  - `step` is a negative number and `start < stop`.

  For example:

  - `ARRAY_GENERATE_RANGE(2, 2, 4)` returns `[]`.
  - `ARRAY_GENERATE_RANGE(8, 2, 2)` returns `[]`.
  - `ARRAY_GENERATE_RANGE(2, 8, -2)` returns `[]`.

## Examples

The following example returns an ARRAY containing a range of numbers starting from 2 and ending before 5:

Copy code

```
SELECT ARRAY_GENERATE_RANGE(2, 5);
```

```
+----------------------------+
| ARRAY_GENERATE_RANGE(2, 5) |
|----------------------------|
| [                          |
|   2,                       |
|   3,                       |
|   4                        |
| ]                          |
+----------------------------+
```

The following example returns an ARRAY containing a range of numbers starting from 5 and ending before 25, increasing in value by
10:

Copy code

```
SELECT ARRAY_GENERATE_RANGE(5, 25, 10);
```

```
+---------------------------------+
| ARRAY_GENERATE_RANGE(5, 25, 10) |
|---------------------------------|
| [                               |
|   5,                            |
|   15                            |
| ]                               |
+---------------------------------+
```

The following example returns an ARRAY containing a range of numbers starting from -5 and ending before -25, decreasing in value
by -10:

Copy code

```
SELECT ARRAY_GENERATE_RANGE(-5, -25, -10);
```

```
+------------------------------------+
| ARRAY_GENERATE_RANGE(-5, -25, -10) |
|------------------------------------|
| [                                  |
|   -5,                              |
|   -15                              |
| ]                                  |
+------------------------------------+
```
