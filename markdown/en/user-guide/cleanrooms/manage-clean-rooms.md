# Creating, joining, removing, and uninstalling clean rooms

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

This topic explains basic clean room actions using both the clean rooms API and the clean rooms UI.

## Create a new clean room

You must have the proper permission in a Snowflake account to be able to create a clean room. The clean room creator is called the
*provider*.

Clean rooms UIClean rooms API

The **Clean Rooms** page in the clean rooms UI lets you, as a provider, manage the lifecycle of a clean room, including creating
and sharing. If you don’t have access to the clean rooms UI, speak to a clean rooms administrator for your Snowflake account.

To create and share a clean room, do the following:

1. [Sign in to the clean rooms UI.](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in)
2. In the left navigation, select **Clean Rooms**.
3. Select **+ Clean Room**. The creation process has the following steps:
   1. Use the **Add Data** step to name the clean room and select the tables that are being shared with the consumer. The name can
      be 80 characters maximum, case-insensitive a-z, 0-9, spaces, and underscores.
   2. Use the **Specify Join Policies** step to enable identity providers enabled by your clean rooms account administrator and
      select which columns the consumer can join on.
   3. Use the **Configure Analysis & Query** step to define which templates are available in the clean room, template-specific
      configuration settings, and additional features such as activation and privacy settings.
   4. Use the **Share Clean Room** step to invite consumers to use the clean room to collaborate. You can also use the
      **Enable Run Analysis & Query** option to specify which collaborators can run analyses in the clean room.

For a full walkthrough of creating a new clean room in the clean rooms UI, try the
[clean rooms UI tutorial](/user-guide/cleanrooms/v1/tutorials/cleanroom-web-app-tutorial)

To create a new clean room in code, you must be granted the SAMOOHA\_APP\_ROLE role in your account.

Copy code

```
USE WAREHOUSE app_wh;
USE ROLE SAMOOHA_APP_ROLE;
SET cleanroom_name = 'Developer Tutorial';
CALL samooha_by_snowflake_local_db.provider.cleanroom_init(
  $cleanroom_name,
  'INTERNAL');      -- Use EXTERNAL to share outside your Snowflake org
```

After creating your clean room, you must, at minimum, perform the following steps to configure a basic clean room:

1. Import data into the clean room.
2. Set join policies on your data.
3. Specify one or more templates in the clean room.
4. Set column policies on your data for each template.
5. Set a default release directive.
6. Specify consumers to share the clean room with.
7. Publish the clean room.

For a full walkthrough of creating a new clean room in code, try the
[clean rooms code tutorial](/user-guide/cleanrooms/tutorials/cleanroom-api-tutorial-basic)

Note

There is a limit to the number of (clean rooms + collaborators) that you can create in a single account. If you create too many test
clean rooms, you might need to delete a few in order to create new clean rooms. If you need more clean rooms than your account can hold,
contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## Install (join) a clean room

If you have been invited to join a clean room, you will receive an email message with a link to install, configure, and run the clean room
in the clean rooms UI. You can follow the link and use the clean rooms UI, or install and run the clean room using the API.

Clean rooms UIClean rooms API

The **Clean Rooms** page in the clean rooms UI lets you, as a consumer, install clean rooms that have been shared with you by a provider.
To install a clean room, do the following:

1. [Sign in to the clean rooms UI.](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in)
2. In the left navigation, select **Clean Rooms**.
3. On the **Invited** tab, find the clean room and select **Join**. You should get a direct link to this page in an invitation
   email when you are added as a collaborator in the clean rooms UI.
4. Select the tables that you want to use to collaborate with the provider’s data, then select **Next**.
5. Select any identity providers available in your Clean Room environment that you need to use in this clean room.
6. Specify which columns in your table can be joined, and the corresponding columns from the provider’s data.
7. Select **Next**.
8. Provide template-specific settings for any templates assigned to the clean room.
9. Click **Finish**, and optionally run a template immediately, or schedule a repeating run of that template.

If you have been invited to join a clean room as a consumer, you can install, configure, and run the clean room in code.

To join a clean room in code, open up the account that was invited to add the clean room, and run the following code:

Copy code

```
USE WAREHOUSE app_wh;
USE ROLE SAMOOHA_APP_ROLE;
SET cleanroom_name = 'Developer Tutorial'; -- Get the actual clean room name and provider's account locator from the provider.
CALL samooha_by_snowflake_local_db.consumer.
  install_cleanroom($cleanroom_name, <PROVIDER_LOCATOR>);
```

After the clean room is installed, you must take the following steps, at minimum, to be able to run templates in that clean room:

1. Link your data.
2. Set join and column policies on your tables and for the templates that you want to run.
3. Run the template.

For a full walkthrough of joining a clean room in code, try the
[clean rooms code tutorial](/user-guide/cleanrooms/tutorials/cleanroom-api-tutorial-basic)

Note

Some clean rooms throw the following error when you try to join it:

```
Application role `SAMOOHA_BY_SNOWFLAKE.DCR_DELEGATED_CLEANROOM_ROLE` does not exist
or not authorized.
```

If you encounter this error, run the following code and try joining the clean room again:

Copy code

```
USE ROLE ACCOUNTADMIN;
CALL SAMOOHA_BY_SNOWFLAKE.APP_SCHEMA.PREPARE_MOUNT_SCRIPT();
EXECUTE IMMEDIATE FROM @SAMOOHA_BY_SNOWFLAKE.APP_SCHEMA.MOUNT_CODE_STAGE/dcr_loader.sql;
```

## Delete a clean room that you created

After deletion, a clean room will no longer be visible to shared users the next time they open the clean rooms UI. If an analysis is in
progress when a clean room is deleted, it might not complete before the clean room is deleted.

Clean rooms UIClean rooms API

To use the clean rooms UI to delete a clean room that you created, do the following:

> 1. [Sign in to the clean rooms UI.](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in)
> 2. In the left navigation, select **Clean Rooms**.
> 3. In the clean room to delete, select *More* ([![Three vertical dots indicating more options](/static/images/icons/vertical-more-icon.png)](/static/images/icons/vertical-more-icon.png)) **> Delete**.

> - **To delete a single clean room** using the API, call
>   [provider.drop\_cleanroom](/user-guide/cleanrooms/provider#provider-drop-cleanroom).
> - **To list your created clean rooms,** call [provider.view\_cleanrooms](/user-guide/cleanrooms/provider#provider-view-cleanrooms):
>
>   Copy code
>
>   ```
>   USE ROLE SAMOOHA_APP_ROLE;
>   USE WAREHOUSE app_wh;
>
>   -- List created and published clean rooms
>   CALL samooha_by_snowflake_local_db.provider.view_cleanrooms();
>   SELECT CLEANROOM_ID AS "cleanroom_name"
>     FROM TABLE(RESULT_SCAN(last_query_id()))
>     WHERE STATE = 'CREATED' AND IS_PUBLISHED = TRUE;
>
>   -- Specify a clean room name from the list and drop it
>   CALL samooha_by_snowflake_local_db.provider.drop_cleanroom($cleanroom_name);
>   ```

For a full walkthrough of creating, configuring, using, and deleting a clean room in code, try the
[clean rooms code tutorial](/user-guide/cleanrooms/tutorials/cleanroom-api-tutorial-basic)

## Uninstall (unjoin) a clean room

You can uninstall a clean room that you installed (joined) as a consumer. This will uninstall the clean room for all users in the account.

Clean rooms UIClean rooms API

1. [Sign in to the clean rooms UI.](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in)
2. In the left navigation, select **Clean Rooms**.
3. Navigate to **Clean Rooms** » **Joined**.
4. In the clean room to uninstall, select *More* ([![Three vertical dots indicating more options](/static/images/icons/vertical-more-icon.png)](/static/images/icons/vertical-more-icon.png)) **> Leave**.

**To list your installed (joined) clean rooms**

Call [samooha\_by\_snowflake\_local\_db.consumer.view\_cleanrooms](/user-guide/cleanrooms/consumer#consumer-view-cleanrooms) and filter
rows to `IS_ALREADY_INSTALLED = TRUE`. This shows clean rooms that are installed rather than simply invitations to join.

Copy code

```
USE ROLE SAMOOHA_APP_ROLE;
USE WAREHOUSE app_wh;

CALL samooha_by_snowflake_local_db.consumer.view_cleanrooms();
SELECT CLEANROOM_ID AS "cleanroom_name"
  FROM TABLE(RESULT_SCAN(last_query_id()))
  WHERE IS_ALREADY_INSTALLED = TRUE;

CALL samooha_by_snowflake_local_db.consumer.uninstall_cleanroom($cleanroom_name);
```

**To uninstall (unjoin) a single clean room:**

Copy code

```
USE ROLE SAMOOHA_APP_ROLE;
USE WAREHOUSE app_wh;
CALL samooha_by_snowflake_local_db.consumer.
  uninstall_cleanroom($cleanroom_name).
```

For a full walkthrough of creating, configuring, using, and deleting a clean room in code, try the
[clean rooms code tutorial](/user-guide/cleanrooms/tutorials/cleanroom-api-tutorial-basic)

## Adding or removing tables from a clean room

Here is how to add or remove (*link* or *unlink*) tables from a clean room:

Clean rooms UIClean rooms API

When using the UI, only tables or views registered by an administrator can be linked into a clean room. If you don’t see a table or view as available for use in your clean room, ask your administrator to register the object in your account.

- As a provider, you choose which tables to link into the clean room in the **Add Data** step when you create or edit a clean room.
- As a consumer, you choose which tables to link the clean room in the **Add Data** step when you join or edit a clean room.

Once a table is added to a clean room, it cannot be removed from that clean room. You can, however, remove the data from the entire account. If you need to remove a table or view from a clean room, speak to your clean room administrator.

When using the clean rooms API, anyone with the REFERENCE\_USAGE privilege on a data object can register it in the account. After an object is registered, you can link it into any clean room in that account. (Only the account that registered an object can link it into a clean room.)

You cannot unlink a table or view after it has been linked into a clean room. However, you can unregister the table or view for the
entire account, making it unavailable to any clean room in that account. If you unregister a table, be sure to change any row or column
policies, or templates, that refer to that table.

[Learn how to register or unregister data objects](/user-guide/cleanrooms/register-data) to make them available for linking
into a clean room.
