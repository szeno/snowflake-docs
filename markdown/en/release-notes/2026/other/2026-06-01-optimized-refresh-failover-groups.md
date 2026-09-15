# Jun 1, 2026: Optimized refresh for failover groups (*Public Preview*)

Optimized refresh is a new refresh mode for failover groups, now available in public preview. It makes account replication refreshes more efficient and predictable, and is especially valuable for customers who replicate a very large number of objects. You opt in per failover group by setting `OPTIMIZED_REFRESH = TRUE` on the primary failover group. The mode works with the same failover group SQL surface you already use, and replication, failover, and failback semantics are unchanged.

Optimized refresh also introduces a new, simplified pricing model that is primarily based on the volume of data changes that get replicated, making your replication costs easier to forecast.

For more information, see [Optimized refresh for failover groups](/user-guide/account-replication-config#label-optimized-refresh) and [Pricing for optimized refresh](/user-guide/account-replication-cost#label-optimized-refresh-pricing).
