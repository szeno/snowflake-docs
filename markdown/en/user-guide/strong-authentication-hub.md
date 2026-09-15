# Strong Authentication Hub

The Strong Authentication Hub is a user interface that helps you implement strong authentication for all of your users. It is an essential
tool for meeting the deadlines associated with the [deprecation of single-factor passwords](/user-guide/security-mfa-rollout).

The hub identifies users who don’t meet Snowflake requirements for strong authentication and provides step-by-step instructions to bring
these users into conformance.

## What is the Strong Authentication Hub?

The Strong Authentication Hub helps your account conform to Snowflake’s strong authentication requirements by providing the following
capabilities:

Provide visibility
:   Gives you clarity on your account’s readiness for the multi-factor authentication (MFA) enforcement and the deprecation of
    `LEGACY_SERVICE` users, with a clear path to ensure 100% compliance before enforcement deadlines.

Identify risks
:   Identifies specific authentication issues and at-risk users, including:

    - Users who have logged in using only a password via specific applications (for example, Power BI) within the last 90 days.
    - Users who have a password but aren’t enrolled in MFA, and who have not logged in in the past 90 days.
    - Service users (`TYPE=LEGACY_SERVICE`) that need to migrate to stronger authentication methods and be converted to `TYPE=SERVICE`
      users.
    - Users who have logged in using a strong authentication method like federated authentication with single sign-on, but still have a
      password that is not protected by MFA. If a malicious actor obtained the password, they could sign in and enable MFA for themselves.

Manage remediation
:   Provides progress tracking, step-by-step remediation guidance, and the ability to prioritize by issue type or by individual user.

Manage enforcement timelines
:   Displays the rollout timeline for enforcement phases and allows you to extend enforcement dates if needed.

## Access the hub and remediate users

To meet the requirement for strong authentication, every human user who uses a password must be enrolled in MFA and
every service user must use an authentication method that is stronger than a password. Use the Strong Authentication Hub to find users who
don’t meet these requirements and bring them into conformance.

Note

Results and violations displayed in the hub are based on Trust Center scanner results that update periodically. Changes you make to
remediate users might not be reflected immediately.

To access the Strong Authentication Hub and remediate users:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role with the [required access control privileges](#label-strong-auth-hub-access-control).
3. In the navigation menu, select **Governance & security** » **Trust Center**.
4. Select the **Overview** tab.
5. In the **Strong authentication** section, use the **Strong authentication progress** tile to determine whether you have users who
   aren’t ready for the enforcement of strong authentication.
6. If you have users who need to be migrated to a stronger authentication method, select **View hub**.
7. Find the **Prioritize your remediation efforts** section and do one of the following:

   - If you choose to prioritize by issue, select **By issue**, and then select the card that corresponds to the problem that you want to
     remediate.
   - If you choose to prioritize by user, select **By user**, and then select the user that you want to remediate.
8. In the side panel, follow the instructions on how to migrate users to a strong authentication method that meets Snowflake requirements.

## Access control requirements

To use the Strong Authentication Hub, you need the following privileges/roles:

| Task | Required privilege/role | Notes |
| --- | --- | --- |
| View the hub | One of the following application roles:   - `SNOWFLAKE.TRUST_CENTER_ADMIN` application role. - `SNOWFLAKE.TRUST_CENTER_VIEWER` application role. | The ACCOUNTADMIN role meets this requirement. |
| Extend enforcement dates | MODIFY privilege on the account. | The ACCOUNTADMIN role meets this requirement. |

Expand

Show lessSee more
