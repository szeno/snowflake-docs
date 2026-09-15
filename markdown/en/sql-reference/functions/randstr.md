Categories:
:   [Data generation functions](/sql-reference/functions-data-generation)

# RANDSTR

Returns a random string of specified `length`.

## Syntax

Copy code

```
RANDSTR( <length> , <gen> )
```

## Usage notes

- Individual characters are chosen uniformly at random from the following pool of characters: 0-9, a-z, A-Z.
- The value for the generator expression, `gen`, is used as the seed for this uniform random distribution. For more information about generator expressions, see [Usage notes](/sql-reference/functions-data-generation#label-rand-dist-functions).

## Examples

Copy code

```
SELECT randstr(5, random()) FROM table(generator(rowCount => 5));

+----------------------+
| RANDSTR(5, RANDOM()) |
|----------------------|
| rM6ep                |
| nsWJ0                |
| IQi5H                |
| VBNvY                |
| wjk6y                |
+----------------------+
```

Copy code

```
SELECT randstr(5, 1234) FROM table(generator(rowCount => 5));

+------------------+
| RANDSTR(5, 1234) |
|------------------|
| E5tav            |
| E5tav            |
| E5tav            |
| E5tav            |
| E5tav            |
+------------------+
```

Copy code

```
SELECT randstr(abs(random()) % 10, random()) FROM table(generator(rowCount => 5));

+---------------------------------------+
| RANDSTR(ABS(RANDOM()) % 10, RANDOM()) |
|---------------------------------------|
| e                                     |
| iR                                    |
| qRwWl7W6                              |
|                                       |
| Yg                                    |
+---------------------------------------+
```
