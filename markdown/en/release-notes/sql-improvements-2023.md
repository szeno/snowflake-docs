# 2023 SQL improvements

The following SQL improvements were introduced in 2023:

| Date released | Improvement | Impact |
| --- | --- | --- |
| August 2023 | New [ARRAY\_MIN](/sql-reference/functions/array_min), [ARRAY\_MAX](/sql-reference/functions/array_max), and [ARRAY\_SORT](/sql-reference/functions/array_sort) functions. | You can now easily select the array elements with the lowest value and the highest value.  You can easily get a sorted array of elements. |
| August 2023 | New ILIKE and REPLACE parameters in the [SELECT](/sql-reference/sql/select) command. | You can now select all columns that match a pattern containing SQL wildcards.  When selecting all columns, you can replace the value of specific columns with expressions. |
| July 2023 | New ALL keyword in the [GROUP BY](/sql-reference/constructs/group-by) construct. | You can group results by all non-aggregate columns in the SELECT list without having to specify each column by name. |
| February 2023 | Support for bankers’ rounding ([rounding half to even](https://en.wikipedia.org/wiki/Rounding#Rounding_half_to_even)) in the [ROUND](/sql-reference/functions/round) function. | You can now use bankers’ rounding when rounding values. |
| January 2023 | New [MIN\_BY](/sql-reference/functions/min_by) and [MAX\_BY](/sql-reference/functions/max_by) functions. | You can find the row containing the minimum or maximum value in a column and retrieve the value from a different column. |

Expand

Show lessSee more
