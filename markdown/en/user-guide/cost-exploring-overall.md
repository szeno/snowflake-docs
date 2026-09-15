# Exploring overall cost

You can explore historical cost using Snowsight, or by writing queries against views in the
[ACCOUNT\_USAGE](/sql-reference/account-usage) and [ORGANIZATION\_USAGE](/sql-reference/organization-usage) schemas.
Snowsight allows you to quickly and easily obtain information about cost from a visual dashboard. Queries against the usage
views allow you to drill down into cost data and can help generate custom reports and dashboards.

If you need an introduction to how costs are incurred in Snowflake, refer to [Understanding overall cost](/user-guide/cost-understanding-overall).

To obtain a billing statement that contains information about historical usage, see [Access a billing usage statement](/user-guide/billing-usage-statement).

## Viewing costs using Snowsight

Snowsight provides multiple pages that allow you to explore the historical cost of using Snowflake. For details on using these
pages to view overall costs, see:

- [Overview of organization-level costs](#label-cost-exploring-organization-overview)
- [Overview of account-level costs](#label-cost-exploring-account-overview)
- [Drilling down into incurred costs](#label-cost-exploring-consumption-page)

Note

Keep the following in mind when viewing costs in Snowsight:

- It can take up to 72 hours for cost information to become available in Snowsight.
- Information is shown in the UTC time zone, not your local time zone.

### Overview of organization-level costs

The **Organization Overview** page provides insights into how your organization is spending the capacity commitment made in the current
contract. For example, it shows you the remaining balance of the contract, the accumulated cost of Snowflake usage since the start of the
contract, and the monthly spend for the organization.

It also gives you an overview of how much each account in the organization has spent.

Note

The **Organization Overview** page is not available in the following cases:

- The organization uses On Demand accounts rather than a capacity commitment with a contract.
- The organization signed a contract through a Snowflake reseller.

To access an overview of incurred costs at the organization level:

1. Sign in to the [organization account](/user-guide/organization-accounts) or an [ORGADMIN-enabled account](/user-guide/organization-administrators#label-enabling-orgadmin-role-for-account).
2. Switch to a role with [access to cost-related features](/user-guide/cost-access-control).
3. In the navigation menu, select **Admin** » **Cost management**.
4. Select a warehouse to use to view the usage data. Snowflake recommends using an X-Small warehouse for this purpose.
5. Select **Organization Overview**.

The **Account Spend Summary** tile has a **View All** option to expand the contents of the tile to include all of the accounts in the
organization, not just the accounts that have spent the most. To display the SQL query used to populate this tile, select
**View All** » **View query** ([![View query button.](/static/images/snowsight/icons/view-query-icon.png)](/static/images/snowsight/icons/view-query-icon.png)) .

### Overview of account-level costs

The **Account Overview** page provides high-level insights into the cost of using Snowflake and is
the starting point for optimizing your spend. The page summarizes spend, surfaces unexpected
spikes, and recommends ways to save, all in one place.

For a full walkthrough of the page, the tiles it contains, and the privileges required to view
each tile, see [Account Overview](/user-guide/cost-account-overview).

Note

Customers who signed a contract through a Snowflake reseller cannot see the price of a credit or
usage in a currency.

### Drilling down into incurred costs

You can use the **Consumption** page to drill down into the overall cost of using Snowflake for
any given day, week, or month.

To use Snowsight to drill down into the overall cost:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role with [access to cost-related features](/user-guide/cost-access-control).
3. In the navigation menu, select **Admin** » **Cost management**.
4. Select a warehouse to use to view the usage data. Snowflake recommends using an X-Small warehouse for this purpose.
5. Select **Consumption**.
6. Select **All Usage Types** from the drop-down list.

This totals the cost of compute, storage, and data transfer resources and displays them in a bar graph using the organization’s currency.
The total cost of these resources during the selected time period appears above the bar graph.

To isolate the cost of compute, storage, or data transfer, adjust your selection in the **All Usage Types** filter.

#### Usage notes

Keep the following in mind when accessing the **Consumption** page:

- It can take up to 72 hours for cost information to become available in Snowsight.
- To access all of the features on the **Consumption** page, the account administrator must also have
  the ORGADMIN role. For example, if a user has the ACCOUNTADMIN role, but does *not* have the ORGADMIN role, they can only view costs
  for the current account. The **Account** filter that would allow them to switch to a different account does not appear.
- If the usage details fail to load with a message indicating that **The result set is too large to display**, you
  must use the filters to select a shorter date range or otherwise filter the results.
- Compute costs do not include queries executed on a warehouse by the SYSTEM user as part of a user-defined
  [task](/user-guide/tasks-intro).

## Querying data for overall cost

Snowflake provides two schemas, [ORGANIZATION\_USAGE](/sql-reference/organization-usage) and
[ACCOUNT\_USAGE](/sql-reference/account-usage), that contain data related to usage and cost. The ORGANIZATION\_USAGE schema provides
cost information for all of the accounts in the organization while the ACCOUNT\_USAGE schema provides similar information for a single
account. Views in these schemas provide granular, analytics-ready usage data to build custom reports or dashboards.

The following query combines data from the USAGE\_IN\_CURRENCY view in the ORGANIZATION\_USAGE schema in order to gain insight into the
overall cost of using Snowflake.

Query: Total usage costs in dollars for the organization, broken down by account
:   Copy code

    ```
    SELECT account_name,
      ROUND(SUM(usage_in_currency), 2) as usage_in_currency
    FROM snowflake.organization_usage.usage_in_currency_daily
    WHERE usage_date > DATEADD(month,-1,CURRENT_TIMESTAMP())
    GROUP BY 1
    ORDER BY 2 desc;
    ```

**Next Topics**

- [Exploring compute cost](/user-guide/cost-exploring-compute)
- [Exploring storage cost](/user-guide/cost-exploring-data-storage)
- [Exploring data transfer cost](/user-guide/cost-exploring-data-transfer)
