Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_INSTANCE\_FAMILY\_PLACEMENT\_GROUPS

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Returns the list of placement groups supported for the specified
[instance family](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pools-instance-family-table)
for [Snowpark Container Services compute pool nodes](/developer-guide/snowpark-container-services/working-with-compute-pool).

## Syntax

Copy code

```
SYSTEM$GET_INSTANCE_FAMILY_PLACEMENT_GROUPS( '<instance_family>' )
```

## Arguments

`'instance_family'`
:   Instance family.

## Returns

Returns a VARCHAR value that contains the supported placement groups
formatted as a JSON array.

## Usage notes

- The returned list of placement group names is specific to your Snowflake account and the specified
  instance family. For more information, see [Compute pool placement](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pool-placement-group).
- Results don’t guarantee capacity. You might still run into insufficient capacity errors in a placement
  group even if an instance family is supported there.

## Examples

The following function returns the supported placement groups for the `GPU_NV_L` instance family:

Copy code

```
SELECT SYSTEM$GET_INSTANCE_FAMILY_PLACEMENT_GROUPS('GPU_NV_L');
```

Example output:

```
+--------------------------------------------------------------+
| SYSTEM$GET_INSTANCE_FAMILY_PLACEMENT_GROUPS('GPU_NV_L')      |
|--------------------------------------------------------------|
| ["A","B","C","D"]                                            |
+--------------------------------------------------------------+
```

The `GPU_NV_L` instance family is available in the following placement
groups: `A`, `B`, `C` and `D`.
