# Differential privacy in Snowflake Data Clean Rooms

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

To help protect the privacy of entities in your data, Snowflake Data Clean Rooms offer *differential privacy*. Differential privacy is a
math-based privacy system [[1]](#footnote-1) to provide entity-level data protection for both single queries and repeated querying of a data set.
Data providers can configure differential privacy in their clean rooms to enable strong entity-level privacy protection and low noise
levels for their data.

Differential privacy is an alternative to simple aggregation requirements, which can expose private information if adversaries generate
enough “close” queries on data that differ by one entity (known as a *differencing attack*).

Differential privacy is also a good alternative to data masking, which hides column values entirely at the cost
of preventing joins on masked rows and hiding useful data from the analyst. Differential privacy enables joins on protected columns, and
also allows analysts to view protected data, by adding enough noise to protect the privacy of protected rows, but not so much
noise that the data is unusable by the analyst.

[1]
C. Dwork and A. Roth. The Algorithmic Foundations of Differential Privacy. Foundations and Trends in Theoretical
Computer Science, 9 (3-4):211-407, 2014.

Important

Customers are responsible for configuring differential privacy tools in Snowflake Data Clean Rooms to meet their data privacy
requirements. These tools are not configured by default.

## How differential privacy works for clean rooms

Clean rooms offer their own differential privacy implementation that is different from
[Snowflake differential privacy](/user-guide/diff-privacy/differential-privacy-admin-privacy-policies), so read this document to
understand the different behavior and settings.

Differential privacy protects the privacy of *entities* in your data. Clean rooms define an entity as a unique value in a column. Clean
rooms determine which columns contain data that are likely to be sensitive; for example, a social security number or email address is
probably a sensitive entity, but a color is not. When differential privacy is applied, clean rooms might identify one or more entity
columns in each table. You cannot configure which columns are designated as entity columns.

Differential privacy in clean rooms also adds noise to numeric results associated with each entity.

Users might try to compare multiple different query results in order to reduce the noise; this is called a *differencing attack*. In order
to mitigate differencing attacks, differential privacy calculates and monitors a *privacy budget* assigned to an account. Each query has a
cost that reflects how much entity privacy is exposed by that query. This cost is determined mathematically, and depends on the query, the
data, and the previous queries from that user. If a query cost exceeds the remaining privacy budget limit, the query will fail. Otherwise, the
query can continue and the cost is added to the user’s daily privacy budget. The privacy budget is refreshed daily.

Differential privacy in clean rooms does not enforce aggregation constraints on queries, but you can
[add aggregation constraints](#label-dcr-aggregation-constraints) on your data or templates independently.

Tip

[Snowflake privacy policies](/user-guide/diff-privacy/differential-privacy-admin-privacy-policies) prevent creation of a view from
a protected table, so you cannot link in tables that have privacy polices.

## Enable and manage differential privacy in the UI

In the clean room UI, providers can set privacy settings at the template level; consumers cannot enable or modify differential privacy
settings. Standard Snowflake templates used in the clean rooms UI can have different privacy settings per template.

To use the clean room UI to enable or disable differential privacy for a template:

1. Open the **Created** tab of the **Clean Rooms** page
2. Select **Edit** or [![Three vertical dots indicating more options](/static/images/icons/vertical-more-icon.png)](/static/images/icons/vertical-more-icon.png) » **Edit** on the clean room tile (depending on whether the clean room allows you to
   run an analysis).
3. Select **Next** until you reach **Configure Analysis & Query**.
4. At the bottom of the page, expand **Privacy Settings**. Select or deselect **Differential Privacy** and provide your settings for
   that template, including privacy budget for users and query cost. You can also set threshold values to enforce minimum group sizes in
   this query.
5. To configure settings for a different template, first set values for the current template, then choose a different template in the
   template selector.

Tip

If you enable differential privacy for the Audience Overlap template, do not compute overlap statistics. Doing so will consume most of
the user’s privacy budget, leaving little or no budget to run analyses.

### Manage privacy budget in the UI

**See your remaining privacy budget**

When you run a query or view the results, you can see your total budget and the amount used in the **Privacy Settings** section.

**Set the privacy budget for other users**

In the UI, a provider can set a privacy budget, but a consumer cannot.

> 1. Edit a clean room and go to the **Configure Analysis & Query** page.
> 2. Select a template.
> 3. At the bottom of the page, expand **Privacy Settings** where you can see your privacy budget for users and query cost.

## Enable and manage differential privacy in the API

In the clean rooms API, either side can enable and configure differential privacy at the collaborator level.

All custom templates use the same differential privacy settings in a clean room. Snowflake-provided templates can be configured with
individual privacy settings in the UI.

Use the following procedures to configure differential privacy:

- `consumer.enable_templates_for_provider_run` - Turn differential privacy off or on with default values for all
  provider-run analyses.
- `consumer.set_privacy_settings` - Specify individual differential privacy settings in provider-run analyses involving custom templates.
- `provider.set_privacy_settings` - Specify individual differential privacy settings in consumer-run analyses involving custom templates.
- `provider.add_custom_sql_template` - Provide a *sensitivity* parameter to increase or decrease the epsilon (noise level) for a
  template above or below the base line epsilon set for the consumer.
- `provider.add_consumers` - Specify privacy settings per consumer. You can add the same customer multiple times with different
  privacy settings to change their privacy settings.
- `provider.suspend_account_dp_task` - Turn off differential privacy budget monitoring for all clean rooms in this account. Differential
  privacy is no longer enforced.
- `provider.resume_account_dp_task` - Turn on differential privacy budget monitoring for all clean rooms in this account. Any
  differential privacy settings will be respected.

Privacy settings for a clean room are stored in `SAMOOHA_CLEANROOM_cleanroom_ID.admin.privacy_budget`, where `APPLICATION_ID` is
a template name (NULL represents all custom templates) and PARTY\_ACCOUNT is the user it is applied to.

### Manage privacy budget in the API

**See your remaining privacy budget**

Consumers can call the `consumer.view_remaining_privacy_budget` procedure. There is no way for providers to see their remaining privacy
budget in code.

**Set the privacy budget for other users**

- **Providers** call `provider.set_privacy_settings` or `provider.add_consumers`.
- **Consumers** call `consumer.set_privacy_settings` to set budget for provider-run analyses.

### Available privacy settings

The following privacy values can be set using various privacy value setting procedures:

- `differential` (*Integer*) - 1 or 0, where 1 means that differential privacy should be enabled, and 0 means it should not.
- `epsilon` (*Float*): A number greater than zero indicating how much noise should be added to the results. Smaller values (0.1-1.0)
  provide stronger privacy protection but add more noise to the results. Default: 0.1.
- `noise_mechanism` (*String*) - The algorithm used to add noise to the results. Specify either *Laplace* or *Gaussian*.
- `privacy_budget` (*Integer*) - How much privacy budget to give this user, a number >= 0, where 0 means they cannot run a query when
  differential privacy is enabled. Default is 10.
- `threshold` (*Integer*) - Specify 1 to enforce `threshold_value` in Snowflake-provided templates, or 0 to ignore `threshold_value`.
  Default is 0. This is managed by the differential privacy toggle in the clean room UI.
- `threshold_value` (*Integer*) - Minimum number of rows that a group should have to appear in the data. Only used in specific
  Snowflake-provided templates.

## Additional privacy functionality

### Add noise to results

If you want to manually add noise to your results without implementing differential privacy, you can use the following clean room function
in your template or custom code. Note that this code requires the user to have sufficient privacy budget or it will fail; if the
differential privacy task is disabled, the user essentially has infinite budget.

Copy code

```
cleanroom.addnoise(<val>, <epsilon>, <noiserand>, [<gaussian>], [<delta>])
```

**Description:** Add calibrated noise to a numerical value to satisfy differential privacy guarantees. This function can be called only in
the context of a clean room. This does not require differential privacy to be enabled for the user or template, or the differential privacy
task to be enabled. Use this function in a template or UDP/UDTP.

**Arguments:**

- `val` *(DOUBLE)* - The original value to which noise will be added.
- `epsilon` *(DOUBLE)* - The privacy budget parameter, where smaller values (0.1-1.0) provide stronger privacy protection but add
  more noise. Value is > 0.
- `noiserand` (*DOUBLE)* - A random value between 0 and 1 that adds randomness to each result. Calculate this on the fly with a
  random value generator rather than passing in a static value.
- `gaussian` *(BOOLEAN, optional)* - When TRUE, uses Gaussian noise instead of Laplacian noise. Default is FALSE.
- `delta` *(DOUBLE, optional)* - The delta parameter for the Gaussian mechanism when `gaussian` is TRUE (smaller is better).
  Default is 0.000001.

**Returns:** A DOUBLE value representing the original value with privacy-preserving noise added.

**Recommendations:**

- Apply only to aggregates (COUNT, SUM, AVG), never to individual records.
- Consider rounding the results to avoid revealing too much precision.
- This function requires a privacy budget to run, so be aware that it will fail if the user is out of budget.
- Combine with minimum group size constraints for enhanced protection.

**Example:**

This example template adds noise to a count of distinct hashed email values, using the cleanroom-wide epsilon value.

Copy code

```
CALL samooha_by_snowflake_local_db.provider.add_custom_sql_template(
$cleanroom_name,
$template_name,
$$
SELECT
  cleanroom.addNoise(
    count(distinct p.hashed_email),  -- Value
    {{ privacy.epsilon | sqlsafe }}, -- Epsilon
    UNIFORM(0::FLOAT, 1::FLOAT, RANDOM()) -- Noiserand
    ) AS noisy_count
FROM
    IDENTIFIER({{ source_table[0] }}) p
$$);
```

### Set aggregation policies and minimum group sizes

If you want to require aggregation on your data, and specify minimum group sizes, you can either set an
[aggregation policy](/user-guide/aggregation-policies) on the source tables, or enforce aggregation in your templates.

## Managing differential privacy costs

Differential privacy [incurs costs](/user-guide/cleanrooms/cleanroom-cost) even when individual users or templates have not enabled
differential privacy, because the system checks every query to see whether differential privacy should be applied. If you want to eliminate
this cost, you can disable differential privacy for the account:

1. First, turn off differential privacy for all clean rooms using the clean rooms UI:

   1. [Sign in to the clean rooms UI.](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in)
   2. Disable differential privacy in all non-failed clean rooms, even if not shared or published:
      1. Select **Clean rooms** » **Created** » **Edit**.
      2. Select **Next** until you reach **Configure Analysis & Query**.
      3. At the bottom of the page, expand **Privacy Settings**. Deselect **Differential Privacy** if it is selected, then click
         **Next** and **Finish** to save your changes. If it is not selected, just click **Cancel** and move on to the next clean
         room.
2. Finally, suspend the differential privacy background task in your account by calling the
   [provider.suspend\_account\_dp\_task procedure](#dcr-provider-suspend-account-dp-task) in Snowsight.

Important

Enabling differential privacy in a clean room after disabling the background task automatically re-enables the task for that account.

**Some notes and troubleshooting:**

- If you forget to disable differential privacy for a clean room and suspend the background task, differential privacy might not
  function in that clean room for users who have already installed it.
- If differential privacy is enabled within a clean room prior to the clean room being installed, the installation of the clean room
  fails. In this case, you must disable differential privacy in the clean room or re-enable the task as outlined below.

**If you later want to enable differential privacy in your account,** either enable differential privacy for any clean room in the account
or call the [provider.resume\_account\_dp\_task procedure](#dcr-provider-resume-account-dp-task) in Snowsight.
