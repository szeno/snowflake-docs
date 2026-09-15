# Snowflake Data Clean Rooms operational costs

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

If you need an introduction to how costs are incurred in Snowflake, refer to [Understanding overall cost](/user-guide/cost-understanding-overall).

Important

You incur charges for Snowflake Data Clean Room operations in accordance with your contract with Snowflake.

The operational costs associated with using Snowflake Data Clean Rooms can be categorized into costs associated with *ongoing operations*
and *user-initiated operations*.

**Ongoing operations**

Ongoing operations are required to support functionality of the data clean room application and features. These operations include processes and tasks that support automatic upgrades, auto-join during initialization and [legacy provider & consumer clean rooms ongoing operations](/user-guide/cleanrooms/v1/cleanroom-cost#label-dcr-v1-ongoing-operations).

**User-initiated operations**

User-initiated operations occur during clean room management actions or while executing workloads within a clean room. A *workload* is the
process of executing any specific use case (analytics or activation) within the clean room through a user-initiated query. The cost of
executing a workload depends on the time required for the workload to complete within the warehouse specified by the user. Here are
some examples of user-initiated clean room management operations:

- **Analysis & Activation Queries:** This encompasses run procedures used when running specific use case workloads within the clean room by users.
- **Data registration:** This encompasses stored procedures required to enable objects to be used within a clean room by users.
- **Creating and editing a clean room:** This encompasses stored procedures required for setting up a clean room environment, adding data and template code.
- **Joining and editing a clean room:** This encompasses stored procedures required for joining a clean room environment, adding data and template code.

Note

Some user-initiated operations result in actions taken by the Secure Collaboration Orchestrator (SCO)
to orchestrate the clean room across collaborators. Currently, costs associated with these actions
are not charged back, though they may be in the future.

## View your usage cost

### Warehouse costs

To see the cost incurred by a warehouse, sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
In the navigation menu, select **Admin** » **Cost management** » **Consumption**, and then select a warehouse.

### Task costs

To see the cost incurred by serverless tasks, run the following SQL command:

Copy code

```
SELECT * FROM snowflake.account_usage.serverless_task_history;
```
