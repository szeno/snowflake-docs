Categories:
:   [Geospatial functions](/sql-reference/functions-geospatial)

# H3\_LATLNG\_TO\_CELL\_STRING

Returns the [H3](/sql-reference/data-types-geospatial#label-data-types-geospatial-h3) cell ID in hexadecimal format (as a VARCHAR value) for a given latitude,
longitude, and resolution.

See also:
:   [H3\_LATLNG\_TO\_CELL](/sql-reference/functions/h3_latlng_to_cell)

## Syntax

Copy code

```
H3_LATLNG_TO_CELL_STRING( <latitude> , <longitude> , <target_resolution> )
```

## Arguments

`latitude`
:   A FLOAT that represents the latitude.

    Values outside the standard latitude range are wrapped to the range [-90, 90].

`longitude`
:   A FLOAT that represents the longitude.

    Values outside the standard longitude range are wrapped to the range [-180, 180].

`target_resolution`
:   An INTEGER between 0 and 15 (inclusive) that specifies the H3 [resolution](https://h3geo.org/docs/core-library/restable) that you want to use for the returned H3 cell.

    Specifying any other INTEGER value results in an error.

## Returns

Returns a VARCHAR value that corresponds to the hexadecimal H3 cell ID for the given location and resolution.

## Usage notes

- Specifying NaN or Inf values for any input argument results in an error.

## Examples

The following example returns the hexadecimal H3 cell ID for the Brandenburg Gate at resolution 8.

Copy code

```
SELECT H3_LATLNG_TO_CELL_STRING(52.516262, 13.377704, 8);
```

```
+---------------------------------------------------+
| H3_LATLNG_TO_CELL_STRING(52.516262, 13.377704, 8) |
|---------------------------------------------------|
|  881F1D4887FFFFF                                  |
+---------------------------------------------------+
```

The following example specifies a `longitude` value (`373.377704`) that is outside of the traditional longitude range
(-180 to 180). The function interprets this value as `13.377704` (373.377704 modulo 180).

Copy code

```
SELECT H3_LATLNG_TO_CELL_STRING(52.516262, 373.377704, 8);
```

```
+---------------------------------------------------+
| H3_LATLNG_TO_CELL_STRING(52.516262, 13.377704, 8) |
|---------------------------------------------------|
|  881F1D4887FFFFF                                  |
+---------------------------------------------------+
```

The following example demonstrates that you cannot specify a resolution outside of 0 through 15.

Copy code

```
SELECT H3_LATLNG_TO_CELL_STRING(52.516262, 373.377704, 18);
```

```
100410 (P0000): Invalid H3 resolution value: 18. Resolution must be between 0 (coarsest) and 15 (finest).
```
