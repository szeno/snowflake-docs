# July 20, 2026: Pass-through policies for dynamic tables with incremental refresh (*General availability*)

Dynamic tables that have base tables with arbitrary masking or row access policies can now maintain incremental
refresh when the policy is pass-through for the role used during refresh (that is, when the refresh role has
unrestricted access to all rows and columns regardless of the policy condition). Previously, only policies using
allow-listed functions, such as `CURRENT_ROLE()` or `IS_ROLE_IN_SESSION()`, were compatible with incremental
refresh.

For more information, see [Masking and row access policies](/user-guide/dynamic-tables/supported-queries#label-dynamic-tables-limits-incremental-refresh-features).
