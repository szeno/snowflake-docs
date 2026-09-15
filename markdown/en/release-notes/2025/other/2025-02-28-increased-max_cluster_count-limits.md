# Feb 28, 2025: Increased max\_cluster\_count limits for multi-cluster warehouses

You now have more flexibility when specifying upper limits for the MAX\_CLUSTER\_COUNT property
in [Multi-cluster warehouses](/user-guide/warehouses-multicluster).

The upper limit for MAX\_CLUSTER\_COUNT is no longer restricted to 10. Instead, the upper limit
varies depending on the warehouse size.
Currently, you must use a SQL command, not Snowsight, to specify an upper limit higher than 10.

The scaling policies for multi-cluster warehouses now can increase or decrease the capacity
of a warehouse by more than one cluster at a time.

For more information, see [Upper limit on number of clusters for a multi-cluster warehouse](/user-guide/warehouses-multicluster#label-max-cluster-size-limit-per-warehouse-size).
