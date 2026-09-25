# Administrator control and cost monitoring

Administrators manage user access and costs primarily through the compute pools
associated with Streamlit apps.

A user’s role must have the USAGE privilege on a compute pool to create and run a
Streamlit app in a workspace. In addition, the compute pool must allow the
`STREAMLIT` workload type through the `ALLOWED_SPCS_WORKLOAD_TYPES` parameter.
The default value for this parameter is `ALL`, which includes `STREAMLIT`.

Secondary roles apply to the compute pool but not to the query warehouse, which the app uses
under a single role. Grant USAGE on the query warehouse directly to the role the app runs as.

To learn more about compute pool workloads, see
[Snowpark Container Services: Working with compute pools](/developer-guide/snowpark-container-services/working-with-compute-pool).

## Disable Streamlit app execution

Administrators can restrict Streamlit app execution in Workspaces in multiple ways:

### Remove USAGE on the compute pool

Removing the USAGE privilege from a role on a compute pool prevents that role from
using that compute pool, including running Streamlit apps.

### Restrict workload types on all compute pools

Administrators can restrict Streamlit app execution while still permitting other
workloads using two account-level parameters. This affects all roles in the account.

- Exclude `STREAMLIT` from the
  [ALLOWED\_SPCS\_WORKLOAD\_TYPES](/sql-reference/parameters#label-allowed-spcs-workload-types) parameter.
- Set `STREAMLIT` as the
  [DISALLOWED\_SPCS\_WORKLOAD\_TYPES](/sql-reference/parameters#label-disallowed-spcs-workload-types)
  parameter.

Any role that has USAGE on the compute pool can still run other allowed workload
types as specified by the parameters.

## Monitor costs

Administrators can monitor consumption per compute pool. Snowflake recommends
provisioning a unique compute pool for each role to view role-level consumption. To
manage spend, administrators can apply [budgets](/user-guide/budgets) on
specific compute pools.
