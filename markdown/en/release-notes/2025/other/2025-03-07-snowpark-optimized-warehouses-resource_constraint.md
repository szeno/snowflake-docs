# Mar 07, 2025: RESOURCE\_CONSTRAINT clause for Snowpark-optimized warehouses (*General availability*)

You can now specify the memory and CPU architecture for
[Snowpark-optimized warehouses](/user-guide/warehouses-snowpark-optimized).
You can use the RESOURCE\_CONSTRAINT clause with the CREATE WAREHOUSE and ALTER WAREHOUSE commands.
This feature was previously in public preview.

Important

The RESOURCE\_CONSTRAINT clause is generally available for 16 GB and 256 GB memory sizes.
The 1 TB sizes, which you specify with the RESOURCE\_CONSTRAINT parameters `MEMORY_64X`
and `MEMORY_64X_x86`, are still in preview. Also, the 1 TB sizes are currently available
for the Amazon Web Services (AWS) cloud provider, not for Microsoft Azure and Google Cloud Platform (GCP).

For more information, see [Configuration options for Snowpark-optimized warehouses](/user-guide/warehouses-snowpark-optimized#label-snowpark-resource-constraints), [CREATE WAREHOUSE](/sql-reference/sql/create-warehouse), and [ALTER WAREHOUSE](/sql-reference/sql/alter-warehouse).
