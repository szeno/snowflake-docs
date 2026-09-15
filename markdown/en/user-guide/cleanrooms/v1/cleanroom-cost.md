# Snowflake Data Clean Rooms operational costs

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

If you need an introduction to how costs are incurred in Snowflake, refer to [Understanding overall cost](/user-guide/cost-understanding-overall).

Important

You incur charges for Snowflake Data Clean Room operations in accordance with your contract with Snowflake.

The operational costs associated with using Snowflake Data Clean Rooms can be categorized into costs associated with *ongoing operations*
and *user-initiated operations*.

## Ongoing operations

Ongoing operations are required to support functionality of the data clean room application and features. Here are some examples of ongoing operations required for product functionality:

- **Differential Privacy:** Enabled on the provider’s account to support enforcement of differential privacy. This operation prevents
  consumers from being able to increase their daily query budget by altering or resetting their current differential privacy
  budget usage. In order to provide the highest fidelity for this enforcement, this operation needs to validate the consumer’s true
  remaining daily budget every minute. This operation is set up when a user enables differential privacy in a clean room. You can control
  this cost by [disabling the differential privacy task](#dcr-provider-diff-privacy-functions).
- **Template Scans:** Snowflake scans custom templates to highlight deviations from best practices in custom template code logic. Clean
  room providers can then take necessary actions to address these findings by updating or disabling custom templates within their clean
  rooms. This operation is enabled when you install the Snowflake Data Clean Room application.
- **Activation:** Required to support activation use cases from the clean room to any preferred destination. For clean rooms that support
  activation, Snowflake monitors the status of incoming shares or API calls to ensure successful processing and near real-time availability
  of data (subject to end destination processing time). This operation is set up when your account is enabled as an activation partner in
  the **Profiles & Features** section of the clean rooms UI.
- **Clean rooms UI metadata:** Snowflake maintains the most up-to-date clean room metadata to ensure that clean rooms UI users are
  operating on the most current state of the clean room. This operation is enabled when you install the Snowflake Data Clean Room
  application.
- **Automated Data Stats:** Snowflake maintains a daily refresh of your table stats and data overlap stats between your linked tables and
  your collaborator’s linked tables. This operation is enabled when you install the Snowflake Data Clean Room application.

## User-initiated operations

User-initiated operations occur during clean room management actions or while executing workloads within a clean room. A *workload* is the
process of executing any specific use case (analytics or activation) within the clean room through a user-initiated query. The cost of
executing a workload depends on the time required for the workload to complete within the warehouse specified by the user. Here are
some examples of user-initiated clean room management operations:

- **Data registration:** This encompasses stored procedures required to enable objects to be used within a clean room by users.
- **Creating and editing a clean room:** This encompasses stored procedures required for setting up a clean room environment,
  adding data and template code, and setting respective data policies.
- **Installing and editing a clean room:** This encompasses stored procedures required for installing a clean room environment,
  adding data, and setting respective data policies.
- **Identity Hub:** This encompasses any calls to identity providers used by the clean room.
- **Statistics:** Each clean room account runs a daily task to generate clean room data statistics. Credit consumption is dependent on the
  dataset size linked into the clean room. To disable this task, the provider must run
  `CALL samooha_by_snowflake_local_db.provider.manage_datastats_task_on_account(false);`, and all consumers in all clean rooms in the
  provider’s account must run `CALL samooha_by_snowflake_local_db.consumer.manage_datastats_task_on_account(false)`;

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
