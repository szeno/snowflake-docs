# Planning a data load

This topic provides best practices, general guidelines, and important considerations for planning a data load.

## Dedicating separate warehouses to load and query operations

Loading large data sets can affect query performance. We recommend dedicating separate warehouses for loading and querying operations to optimize performance for each.

The number of data files that can be processed in parallel is determined by the amount of compute resources in a warehouse. If you follow the file sizing guidelines described in [Preparing your data files](/user-guide/data-load-considerations-prepare), a data load requires minimal resources. Splitting larger data files allows the load to scale linearly. Unless you are bulk loading a large number of files concurrently (i.e. hundreds or thousands of files), a smaller warehouse (Small, Medium, Large) is generally sufficient. Using a larger warehouse (X-Large, 2X-Large, etc.) will consume more credits and may not result in any performance increase.
