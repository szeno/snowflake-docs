# Use Snowsight to set up data quality checks

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic describes how to use [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) to set up data quality checks. You can use the following strategies to set up data
quality checks:

- Use AI to intelligently suggest data quality checks based on characteristics of your data and usage patterns.
  See [Set up quality checks using Cortex Data Quality](#label-data-quality-ui-setup-cortex).
- Manually define the expected values to be returned by a data metric function (DMF). See [Set up quality checks manually](#label-data-quality-ui-setup-manual).

For an introduction to concepts of data quality checks, see [Core concepts of data quality checks](/user-guide/data-quality-intro#label-data-quality-core-concepts).

## Set up quality checks using Cortex Data Quality

Cortex Data Quality uses AI to suggest data quality checks based on characteristics of your metadata. If you accept
the suggestions, Snowflake checks your data for quality issues at regular intervals to identify problems.

Cortex Data Quality leverages the [Snowflake Cortex AI\_COMPLETE function](/sql-reference/functions/ai_complete) to
intelligently suggest data quality checks. Because it runs securely inside Snowflake Cortex, your enterprise data and metadata always stay
inside Snowflake. Cortex Data Quality also fully respects Snowflake access control and provides suggestions that are based only
on the data that you can access.

To use Cortex Data Quality to set up data quality checks, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Explorer**, and then select the object.
3. Select the **Data Quality** tab.
4. Select **Monitoring**.
5. Do one of the following:

   - **If this is the first time you are setting up quality checks**, select **Get started**.
   - **If you are setting up additional quality checks**, select **Add quality check**, and then select **Suggested quality checks**.
6. Review the suggested data quality checks. To change the criteria that determine whether data passes a quality check, edit the contents
   of the **What should the result be?** column.
7. Select the quality checks that you want to implement, and then select **Apply**.

For more information about Cortex Data Quality, see [More about Cortex Data Quality](#label-data-quality-ui-setup-cortex-more).

## Set up quality checks manually

To create data quality checks based on your knowledge of your data, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Explorer**, and then select the object.
3. Select the **Data Quality** tab.
4. Select **Monitoring**.
5. Do one of the following:

   - **If this is the first time you are setting up quality checks**, select **Start manually**.
   - **If you are setting up additional quality checks**, select **Add quality check**, and then select **Build checks manually**.
6. In the **Set up a quality check** dialog, select the type of check that you want to create.
7. Configure the criteria that determine if data passes the quality check, and then select **Save**.

Tip

If you want to enable anomaly detection so that Snowflake can automatically detect data quality issues based on the historical volume and
freshness of your data, either use [Cortex Data Quality](#label-data-quality-ui-setup-cortex) and accept its suggestions for anomaly
detection or [set up anomaly detection manually](/user-guide/data-quality-anomaly).

## Adjust how often quality checks run

The schedule of a table or view determines how often the DMF that is powering the data quality check runs. The schedule can be based on time
or on updates to the table.

Note

You can’t use Snowsight to adjust the schedule until you have added at least one quality check. You can use an ALTER <object>
command to set the schedule for a table or view at any time.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Explorer**, and then select the object.
3. Select the **Data Quality** tab.
4. Select **Monitoring**.
5. Select **Settings**.
6. Specify how often you want to run the DMF:
   - To run the DMF at a regular interval of one day or less, select **Interval-based timing** and select the interval from the drop-down
     list.
   - To run the DMF on a custom schedule, select **Select schedule** and set the schedule.
   - To run the DMF whenever there is a DML change to the table (for example, when a row is added), select
     **Trigger-based execution**.

## More about Cortex Data Quality

The following sections provide additional information about Cortex Data Quality.

### Required LLMs

Cortex Data Quality won’t work unless the [CORTEX\_MODELS\_ALLOWLIST](/sql-reference/parameters#label-cortex-models-allowlist) account parameter allows the `mistral-7b` and
`llama3.1-8b` models within the account. By default, both models are allowed. For more information about setting this parameter, see
[Account-level allowlist parameter](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-allowlist).

### Access control requirements

Administrators with the ACCOUNTADMIN role have all the privileges that they need to use Cortex to suggest data quality checks.

Other users must have the following privileges and roles:

- OWNERSHIP privilege on the table
- EXECUTE DATA METRIC FUNCTION privilege on the account
- SNOWFLAKE.DATA\_METRIC\_USER database role
- SNOWFLAKE.CORTEX\_USER database role

#### Limit access

By default, the CORTEX\_USER database role is granted to the PUBLIC role, which means every user has it. If you don’t want all users to be
able to use Snowflake Cortex features, you can revoke this database role from the PUBLIC role and then grant
it to specific roles.

To stop users from using Cortex to suggest quality checks, revoke the CORTEX\_USER database role from the PUBLIC role by
running the following commands. Be sure to use the ACCOUNTADMIN role.

Copy code

```
USE ROLE ACCOUNTADMIN;

REVOKE DATABASE ROLE SNOWFLAKE.CORTEX_USER
  FROM ROLE PUBLIC;
```

You can now selectively provide access by granting the CORTEX\_USER database role to specific roles. In the following example, use the
ACCOUNTADMIN role and grant the user `some_user` the CORTEX\_USER database role through the account role `cortex_access_role`, which you
create for this purpose.

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE ROLE cortex_access_role;
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE cortex_access_role;

GRANT ROLE cortex_access_role TO USER some_user;
```

You can also grant the CORTEX\_USER database role to existing roles.

### Cost considerations

The cost of using Cortex Data Quality consists of the following:

- Costs associated with the [COMPLETE (SNOWFLAKE.CORTEX)](/sql-reference/functions/complete-snowflake-cortex) function. These charges appear on a bill as
  AI-Services, which includes all uses of Snowflake Cortex.
- Compute cost of the default warehouse that runs Snowsight.

### Legal notices

Cortex Data Quality leverages third-party models and/or services, as previously described on this page.

The data classification of inputs and outputs are as set forth in the following table.

| Input data classification | Output data classification | Designation |
| --- | --- | --- |
| Usage Data | Usage Data | Preview AI Features. [[1]](#footnote-1) |

Expand

Show lessSee more

[1]
Represents the defined term used in the AI Terms and Acceptable Use Policy.

For additional information about the use of AI, see [Snowflake AI and ML](/guides-overview-ai-features).
