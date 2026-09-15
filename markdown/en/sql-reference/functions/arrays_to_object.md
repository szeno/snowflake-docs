Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# ARRAYS\_TO\_OBJECT

Returns an [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) that contains the keys specified by one input [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) and the values
specified by another input ARRAY.

## Syntax

Copy code

```
ARRAYS_TO_OBJECT( <key_array> , <value_array> )
```

## Arguments

`key_array`
:   ARRAY of VARCHAR values that specify the keys for the new OBJECT.

`value_array`
:   ARRAY of values for the new OBJECT. This ARRAY must be the same length as `key_array`. The values in this ARRAY should
    correspond to the keys in `key_array`.

## Returns

The function returns a value of the type OBJECT. The OBJECT contains the keys and values specified by the input ARRAYs.

## Usage notes

- If any element in `key_array` is not a string, the function reports the following error:

  ```
  215002 (22000): Key supplied for ARRAYS_TO_OBJECT does not have string type
  ```
- `key_array` and `value_array` must be equal in length. Otherwise, the function reports the following error:

  ```
  215001 (22000): Key array and value array had unequal lengths in ARRAYS_TO_OBJECT
  ```
- If an element in `key_array` is NULL, that key and the corresponding value are omitted from the returned OBJECT.

  If the key is not NULL but the corresponding element in `value_array` is NULL, the key and NULL value are included in
  the returned OBJECT.
- The returned OBJECT does not necessarily preserve the original order of the key-value pairs.

- This function doesn’t support a [structured type](/sql-reference/data-types-structured) as an input argument.

## Examples

The following example returns an OBJECT that contains key-value pairs specified by two input ARRAYs:

Copy code

```
SELECT ARRAYS_TO_OBJECT(['key1', 'key2', 'key3'], [1, 2, 3]);
```

```
+-------------------------------------------------------+
| ARRAYS_TO_OBJECT(['KEY1', 'KEY2', 'KEY3'], [1, 2, 3]) |
|-------------------------------------------------------|
| {                                                     |
|   "key1": 1,                                          |
|   "key2": 2,                                          |
|   "key3": 3                                           |
| }                                                     |
+-------------------------------------------------------+
```

In the following example, the ARRAY of keys includes a NULL value. That key and the corresponding value are omitted from the
returned OBJECT.

Copy code

```
SELECT ARRAYS_TO_OBJECT(['key1', NULL, 'key3'], [1, 2, 3]);
```

```
+-----------------------------------------------------+
| ARRAYS_TO_OBJECT(['KEY1', NULL, 'KEY3'], [1, 2, 3]) |
|-----------------------------------------------------|
| {                                                   |
|   "key1": 1,                                        |
|   "key3": 3                                         |
| }                                                   |
+-----------------------------------------------------+
```

In the following example, the ARRAY of values includes a NULL value. That value and the corresponding key are included in the
returned OBJECT.

Copy code

```
SELECT ARRAYS_TO_OBJECT(['key1', 'key2', 'key3'], [1, NULL, 3]);
```

```
+----------------------------------------------------------+
| ARRAYS_TO_OBJECT(['KEY1', 'KEY2', 'KEY3'], [1, NULL, 3]) |
|----------------------------------------------------------|
| {                                                        |
|   "key1": 1,                                             |
|   "key2": null,                                          |
|   "key3": 3                                              |
| }                                                        |
+----------------------------------------------------------+
```
