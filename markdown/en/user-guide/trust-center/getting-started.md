# Getting started with the Trust Center

You can use the Trust Center to check for common security risks in your Snowflake account, and get recommendations
on how to remediate those risks.

## Enable the CIS Benchmarks scanner package

Complete the following steps to enable the [CIS Benchmarks scanner package](/user-guide/trust-center/overview#label-cis-benchmarks-scanner-package):

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role with the `SNOWFLAKE.TRUST_CENTER_ADMIN` application role granted to it.

   For more information about granting this role, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
3. In the navigation menu, select **Governance & security** » **Trust Center**.
4. Select a warehouse.
5. Select **Scanner Packages**.
6. Select **CIS Benchmarks**.
7. Select **Enable** and then **Continue**.

After you enable the scanner package, you can
[enable or disable individual scanners in the scanner package](/user-guide/trust-center/using-the-trust-center#label-trust-center-enable-disable-scanner). You can also
[change the schedule of individual scanners in the scanner package](/user-guide/trust-center/using-the-trust-center#label-trust-center-change-scanner-schedule).

## Enable the Threat Intelligence scanner package

Complete the following steps to enable the [Threat Intelligence scanner package](/user-guide/trust-center/overview#label-threat-intelligence-scanner-package):

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role with the `SNOWFLAKE.TRUST_CENTER_ADMIN` application role granted to it.

   For more information about granting this role, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
3. In the navigation menu, select **Governance & security** » **Trust Center**.
4. Select a warehouse.
5. Select **Scanner Packages**.
6. Select **Threat Intelligence**.
7. Select **Enable** and then **Continue**.

After you enable the scanner package, you can
[enable or disable individual scanners in the scanner package](/user-guide/trust-center/using-the-trust-center#label-trust-center-enable-disable-scanner). You can also
[change the schedule of individual scanners in the scanner package](/user-guide/trust-center/using-the-trust-center#label-trust-center-change-scanner-schedule).

## Enable the AI Security scanner package

If you use Snowflake AI features, such as [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents),
[Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork), or
[Cortex Code](/user-guide/cortex-code/cortex-code), Snowflake recommends that you enable the **AI Security**
scanner package to monitor AI-related configurations and usage in your account.

Complete the following steps to enable the [AI Security scanner package](/user-guide/trust-center/overview#label-ai-security-scanner-package):

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role with the `SNOWFLAKE.TRUST_CENTER_ADMIN` application role granted to it.

   For more information about granting this role, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
3. In the navigation menu, select **Governance & security** » **Trust Center**.
4. Select a warehouse.
5. Select **Scanner Packages**.
6. Select **AI Security**.
7. Select **Enable** and then **Continue**.

After you enable the scanner package, you can
[enable or disable individual scanners in the scanner package](/user-guide/trust-center/using-the-trust-center#label-trust-center-enable-disable-scanner). You can also
[change the schedule of individual scanners in the scanner package](/user-guide/trust-center/using-the-trust-center#label-trust-center-change-scanner-schedule).

After the package runs, you can monitor AI agents, runtime guardrail status, and AI-related violations and
detections from the [View the AI Security tab](/user-guide/trust-center/using-the-trust-center#label-trust-center-ai-security-tab).

## Ensure multi-factor authentication (MFA) is enforced for all human users using password-based authentication

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role with the `SNOWFLAKE.TRUST_CENTER_ADMIN` application role granted to it.

   For more information about granting this role, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
3. In the navigation menu, select **Governance & security** » **Trust Center**.
4. Ensure you have [enabled the CIS Benchmarks scanner package](#label-trust-center-enable-cis-benchmarks-scanner-package).
5. Select **Violations**.
6. Above the list of violations, select **Search**.
7. In the **Search** box, enter `multi-factor authentication`.
8. Under the **Violation** column, select
   `Ensure multi-factor authentication (MFA) is turned on for all human users with password-based authentication`.

   A side panel opens.
9. In the side panel, select **Remediation**, and follow the guidance.

## Find over-privileged roles

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role with the `SNOWFLAKE.TRUST_CENTER_ADMIN` application role granted to it.

   For more information about granting this role, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
3. In the navigation menu, select **Governance & security** » **Trust Center**.
4. Ensure you have [enabled the CIS Benchmarks scanner package](#label-trust-center-enable-cis-benchmarks-scanner-package).
5. Select **Violations**.
6. Above the list of violations, select **Search**.
7. In the **Search** box, enter `snowflake tasks`.
8. Under the **Violation** column, select
   `Ensure that Snowflake tasks do not run with the ACCOUNTADMIN or SECURITYADMIN role privileges`.

   A side panel opens.
9. In the side panel, select **Remediation**, and follow the guidance.

## Ensure the number of users with the ACCOUNTADMIN and SECURITYADMIN system roles is limited

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role with the `SNOWFLAKE.TRUST_CENTER_ADMIN` application role granted to it.

   For more information about granting this role, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
3. In the navigation menu, select **Governance & security** » **Trust Center**.
4. Ensure you have [enabled the CIS Benchmarks scanner package](#label-trust-center-enable-cis-benchmarks-scanner-package).
5. Select **Violations**.
6. Above the list of violations, select **Search**.
7. In the **Search** box, enter `limit the number of users`.
8. Under the **Violation** column, select
   `Limit the number of users with ACCOUNTADMIN and SECURITYADMIN`.

   A side panel opens.
9. In the side panel, select **Remediation**, and follow the guidance.

## Find users who have not logged in for 90 days

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role with the `SNOWFLAKE.TRUST_CENTER_ADMIN` application role granted to it.

   For more information about granting this role, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
3. In the navigation menu, select **Governance & security** » **Trust Center**.
4. Ensure you have [enabled the CIS Benchmarks scanner package](#label-trust-center-enable-cis-benchmarks-scanner-package).
5. Select **Violations**.
6. Above the list of violations, select **Search**.
7. In the **Search** box, enter `did not log in`.
8. Under the **Violation** column, select
   `Ensure that users who did not log in for 90 days are disabled`.

   A side panel opens.
9. In the side panel, select **Remediation**, and follow the guidance.

## Find risky users and mitigate authentication risks

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role with the `SNOWFLAKE.TRUST_CENTER_ADMIN` application role granted to it.

   For more information about granting this role, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
3. In the navigation menu, select **Governance & security** » **Trust Center**.
4. Ensure you have [enabled the Threat Intelligence scanner package](#label-trust-center-enable-threat-intelligence-scanner-package).
5. Select **Violations**.
6. Above the list of violations, select **Search**.
7. In the **Search** box, enter `Ensure that every user is subject to an authentication policy`.
8. Under the **Violation** column, select
   `Ensure that every user is subject to an authentication policy that requires MFA enrollment`.

   A side panel opens.
9. In the side panel, select **Remediation**, and follow the guidance.

For more information, see the following resources:

- [How Organizations Can Use Snowflake To Move Beyond A Password-Only Sign-in Process (Whitepaper)](https://www.snowflake.com/en/resources/white-paper/best-practices-to-mitigate-the-risk-of-credential-compromise/)
- [Best Practices to Mitigate the Risk of Credential Compromise (Video)](https://youtu.be/XT16HYfaRzg?si=lojzoYbxpioxJcCF)

## Next steps

- [Using the Trust Center](/user-guide/trust-center/using-the-trust-center)
