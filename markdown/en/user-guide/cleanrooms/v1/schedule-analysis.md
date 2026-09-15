# Scheduling a repeating analysis in the clean rooms UI

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. Migrate to the
[Collaboration API](/user-guide/cleanrooms/overview) using the
[migration tool](/user-guide/cleanrooms/migration-tool) before the dates below.

- **2026-10-01:** New legacy clean rooms may not be created via the
  [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction).
- **2027-02-01:** The [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction)
  will no longer be accessible, and new legacy clean rooms may not be created via the
  [Provider and Consumer API](/user-guide/cleanrooms/getting-started).
- **2027-06-01:** Legacy [Provider and Consumer clean rooms](/user-guide/cleanrooms/getting-started)
  will no longer be accessible. Use the [Collaboration API](/user-guide/cleanrooms/overview)
  to create and manage clean rooms.

Some types of analyses can be scheduled to run automatically at a regular interval. These analyses include the following:

- SQL Query template
- Audience Overlap & Segmentation template
- Custom templates created using the developer APIs

An administrator must configure the clean room environment to allow scheduled analyses before a user can schedule an analysis to repeat.

**Limitation:** Only consumers can schedule analyses.

## Enable scheduled analyses

A clean rooms account administrator must configure an account to allow scheduled analyses.

To enable scheduled analyses in a clean room account:

1. [Sign in to the clean rooms UI.](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in)
2. In the left navigation, select **Admin** » **Snowflake Admin**.
3. Select **Login to Snowflake**, and authenticate as a Snowflake user with the ACCOUNTADMIN role.
4. In the **Account Features** section, enable **Schedule Analysis Run**.

## Scheduling a repeating analysis

If an analysis template supports scheduling analyses, you can configure an analysis to repeat at a regular interval when you run it for the
first time in the clean room. When prompted to save the analysis, use the **Schedule Run** drop-down list to select an interval.

## Modify or disable a scheduled analysis

If you want to change the scheduled interval for an analysis or turn off scheduling, complete these steps:

1. [Sign in to the clean rooms UI.](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in)
2. In the left navigation, select **Analyses & Queries**.
3. Find the analysis in the list and select it.
4. Expand the **Save Analysis & Query** section, and use the **Schedule Run** drop-down list to make the change.
