# Aug 16, 2026: Feature policy rules (*General availability*)

With this release, we are pleased to announce the general availability of feature policy
rules. A feature policy can carry a YAML body that conditionally blocks object creation
based on attributes of the request. For example, you can permit tables in general but
block temporary tables, or permit tasks but block serverless (no-warehouse) tasks.

[DESCRIBE FEATURE POLICY](/sql-reference/sql/desc-feature-policy) is also now generally
available. Use it to inspect a policy’s YAML body, which appears as the
`policy_definition` property.

For more information, see [Feature policy rules](/user-guide/feature-policies#label-feature-policy-rules).
