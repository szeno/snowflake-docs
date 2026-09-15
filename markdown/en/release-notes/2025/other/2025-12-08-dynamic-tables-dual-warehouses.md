# Dec 08, 2025: Dynamic tables: Support for dual warehouses

Dynamic tables support dual warehouses to optimize performance and cost for different types of refresh operations. You can specify a dedicated
warehouse for [initializations and reinitializations](/user-guide/dynamic-tables/overview#label-dynamic-tables-initialization), which are typically more resource-intensive,
while you use another warehouse for all other refreshes.

For more information, see [Choose and size warehouses for dynamic tables](/user-guide/dynamic-tables/warehouse-selection).
