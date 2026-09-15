# Configure Egress Cost Optimizer

If you’re a provider, you can use Cross-Cloud Auto-Fulfillment (auto-fulfillment) for a listing to automatically replicate your data product to other Snowflake regions without having to manually replicate data.

This section describes how to authorize multi-region sharing and enable and disable Egress Cost Optimizer (ECO) for your organization.

## Authorize multi-region sharing egress cost optimization

ECO must be authorized before it can be used. You can enable ECO initially from the [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) **Home** page, or later using the **Settings**.

To initially authorize ECO, do the following:

Snowsight

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user who has been granted the ORGADMIN privilege.
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select the **Home** tab.
4. Click **Get Started**.
5. Click **Authorize**.

   **Why this is important**

   Egress Cost Optimizer is a feature of Cross-Cloud Auto-Fulfillment that helps you reduce
   egress costs by up to 80% when sharing the same data to multiple regions.

   **Enable Egress Cost Optimizer**
   By opting to use Egress Cost Optimizer, you enable Snowflake to intelligently
   route your data to minimize egress costs. You also authorize the associated Snowflake Third-party

   [Sub-processors](https://www.snowflake.com/en/legal/privacy/snowflake-sub-processors/)
   to process your data in the cloud regions described in our Documentation.
   Your data is always secure with end-to-end encryption in transit and at rest with no impact to query latency when processed through
   Egress Cost Optimizer.

   **Once Authorized**
   The optimizations will be enabled for all accounts in your organization.
   The account administrators can disable it.

## Enabling Egress Cost Optimizer

You can enable or disable ECO at the account level. Where an auto-fulfillment schedule is set, ECO will be enabled on all the listings in a database that follow the account schedule.

### Enable or disable ECO for an entire account

SnowsightSQL

After ECO is authorized at the organization level, enable or disable ECO for an account by doing the following:

> 1. In the navigation menu, select **Marketplace** » **Provider Studio**.
> 2. Select the **Settings** tab.
> 3. In the **Cross-Cloud Auto-Fulfillment** pane, click the toggle next to **Egress Cost Optimizer** to enable or disable ECO.

You can enable egress cost optimization by executing the [ALTER ACCOUNT](/sql-reference/sql/alter-account) command to set the ENABLE\_EGRESS\_COST\_OPTIMIZER parameter to TRUE:

Copy code

```
ALTER ACCOUNT SET ENABLE_EGRESS_COST_OPTIMIZER=TRUE;
```

To disable egress cost optimization, set the ENABLE\_EGRESS\_COST\_OPTIMIZER parameter to FALSE:

Copy code

```
ALTER ACCOUNT SET ENABLE_EGRESS_COST_OPTIMIZER=FALSE;
```

For more information see [ALTER ACCOUNT](/sql-reference/sql/alter-account).

# Limitations of ECO

- Incremental data ingestion is required for the cloud cache to be fully used by the egress cost optimizer.
- The cloud cache is only used by the egress cost optimizer for refreshes made by auto-fulfillment.
- Egress cost optimizer will only use the cloud cache if the overall egress costs for all listings on the same database are getting optimized. The optimizer algorithm measures the size of the listings at a database level and not at a table level.
- ECO is not supported for listings that include a [Cortex Knowledge Extension (CKE)](/user-guide/snowflake-cortex/cortex-knowledge-extensions/cke-overview).

  Providers should be aware of the cost implications for replication with listings that have a CKE.

  If a CKE is added to a listing that has ECO enabled, ECO will be automatically turned off, and the provider will be notified by email. With ECO turned off, costs associated with the listing can increase.

  Similarly, if a CKE is added to a listing that’s part of a replication group, then ECO will be turned off for all listings within that replication group. An email notification will be sent to the provider indicating that the ECO was turned off.
