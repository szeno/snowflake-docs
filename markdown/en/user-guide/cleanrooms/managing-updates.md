# Managing clean room environment updates

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

This topic describes manging updates by the administrator of a Snowflake Data Clean Room. For information about installing the clean room environment
in your Snowflake account, see [Installing the Snowflake Data Clean Rooms environment](/user-guide/cleanrooms/installing-dcr).

Important

If you’re on version 12.3 or earlier, automatic updates may have stopped working and you must manually update your API environment. Follow these instructions to [re-run the mount procedure](/user-guide/cleanrooms/v2/troubleshooting#label-dcr-troubleshooting-versions-12-3-remount).
Afterward, [re-enable automatic upgrades](#label-dcr-automatic-api-updates) to get new updates automatically.

## Updating the clean rooms environment

Snowflake Data Clean Rooms updates their binaries weekly to support new features, procedures, and UI updates. You can find release notes for
significant new releases in the [feature updates section](/release-notes/new-features#label-new-features-features) of the Snowflake release notes page (search
for “clean rooms”).

### Clean rooms API updates

A clean rooms administrator can either enable automatic API updates (recommended) or update the API environment manually for each new
release, as described next.

#### Automatic API updates

A clean rooms API administrator can enable clean rooms updates to be installed automatically upon release by running the following SQL commands once in their account:

Copy code

```
USE ROLE SAMOOHA_APP_ROLE;
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.library.enable_local_db_auto_upgrades();
```

Clean rooms API users in that account will see the updates shortly when they are rolled out, without needing to log out.

#### Manual API updates

We recommend enabling automatic clean room updates for your account. But if you prefer to update your account’s API environment manually, you can do so by running the following SQL commands each time you want to update the environment:

Copy code

```
USE ROLE SAMOOHA_APP_ROLE;
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.library.apply_patch();
```

You can find your release number by running the following SQL command:

Copy code

```
SELECT * FROM SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.ADMIN.VERSION;
```

Note

Delaying updates for multiple releases can result in longer `apply_patch` execution times, because the patch must apply
each skipped version sequentially. To minimize update times, apply patches regularly or enable automatic updates.
