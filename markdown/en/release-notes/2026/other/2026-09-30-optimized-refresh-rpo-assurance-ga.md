# Sep 30, 2026: Optimized Refresh and RPO Assurance for failover groups (*General availability*)

Optimized Refresh and RPO Assurance for failover groups are now generally available.

Optimized Refresh for failover groups makes account replication refreshes more efficient and predictable, especially for accounts that
replicate large numbers of objects. Refresh duration scales with your rate of change rather than the number of objects in the group. You
opt in per failover group by setting `OPTIMIZED_REFRESH = TRUE` on the primary failover group.

RPO Assurance provides a Recovery Point Objective (RPO) target. When you set `RPO_ASSURANCE = TRUE` on the primary failover group,
Snowflake manages continuous refreshes to keep secondary accounts in sync with the primary. For the current target, and when it is
backed by a service-level agreement (SLA), see
[SLA eligibility and coverage](/user-guide/account-replication-optimized-refresh#label-rpo-assurance-sla).

Failover groups that you have today keep running as Replication Classic by default.

For more information, see [Optimized Refresh and RPO Assurance](/user-guide/account-replication-optimized-refresh) and
[Pricing for Optimized Refresh and RPO Assurance](/user-guide/account-replication-cost#label-optimized-refresh-pricing).
