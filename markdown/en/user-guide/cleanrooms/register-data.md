# Registering data

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

This topic describes how to register data so that it can be linked into a Snowflake Data Clean Room.

## Supported objects

The following object types can be linked into clean rooms:

- Tables
- [External tables†](#label-cleanrooms-external-iceberg-tables)
- [Apache Iceberg™† tables](#label-cleanrooms-external-iceberg-tables)
- Dynamic tables
- Views
- Materialized views
- Secure views. The owner of a secure view must be the SAMOOHA\_APP\_ROLE role.

Note

†External and Iceberg tables [must be enabled](#label-cleanrooms-external-iceberg-tables) before they can be used in a clean room.

## Registering data objects

Before users can link data into a Snowflake Data Clean Room, the data must first be *registered*. Registering data grants USAGE and SELECT privileges
on the object to SAMOOHA\_APP\_ROLE, which is used by the clean room environment to access data. If you register a database or schema, all
of the child objects are registered as well. You must have MANAGE GRANTS privilege on an object to be able to link it.

You can register databases, schemas, and objects using the clean rooms UI or the
Clean rooms API. Using the Clean rooms UI is simpler, but requires that you have the ACCOUNTADMIN role.
Using the developer APIs, you can register any object on which you have the MANAGE GRANTS privilege without using the ACCOUNTADMIN role.

**Usage notes**

- Registering a database or schema does not register objects added *after* the registration. You must either register
  the new object individually or use the Clean rooms UI to navigate to **Admin > Snowflake Admin > Database Registration** and
  select **Resync**.
- You can link only data registered by your account. That is, a provider can’t link data registered by the
  consumer and a consumer can’t link data registered by the provider. Once data is linked into a clean room, it can be accessed by anyone
  with access to the clean room, subject to the linking party’s settings (such as join and column policies).
- There are special considerations when [registering tables or views with Snowflake policies applied to them](#label-dcr-link-views-with-external-policies).
- See how to [register external and Apache Iceberg tables](#label-cleanrooms-external-iceberg-limitations).
- When registering a secure view, you must also separately register the database that is the source for that secure view.
- The following instructions show how to register non-external or Iceberg tables:

Clean rooms UIClean rooms API

You must be able to use the ACCOUNTADMIN role to register objects using the clean rooms UI.

Follow these steps to register a database, schema, or object using the Clean rooms UI:

1. [Sign in to the Clean rooms UI](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in) as an account administrator and then take one of the following
   steps:

   - If using a managed account, select **Admin > My Account**.
   - If using a Snowflake account, select **Admin > Snowflake Admin** and sign in to Snowflake as a user with the
     ACCOUNTADMIN role.
2. Select **Admin > Snowflake Admin**.
3. Select **Log in to Snowflake**, and authenticate as a user with the ACCOUNTADMIN role.
4. To enable external or Iceberg tables in the account, enable the **External & Iceberg Tables** toggle.
5. In the **Access management for Snowflake objects** section, select **Edit**, and then select the database, schema, or object to
   make its data linkable by users in this account.
6. Select **Save**.

Use the Clean rooms API to register databases, schemas, and objects programmatically. You need MANAGE GRANTS privilege on an
object to register it.

External and Iceberg tables are [registered differently than other object types](#label-cleanrooms-external-iceberg-tables).

The following procedures are available to register or unregister objects:

| Object type | Register | Unregister |
| --- | --- | --- |
| Database | - `provider.register_db` (for providers) - `consumer.register_db` (for consumers) | `library.unregister_db` |
| Schema | `library.register_schema` | `library.unregister_schema` |
| Managed access schema | `library.register_managed_access_schema` | `library.unregister_managed_access_schema` |
| Any other supported object type | `library.register_objects` | `library.unregister_objects` |

Expand

Show lessSee more

**Example:**

Copy code

```
USE ROLE <ROLE-WITH-MANAGE-GRANTS-PRIVILEGE>
CALL samooha_by_snowflake_local_db.library.register_schema(['MY_DB.MY_SCHEMA']);
```

### Registering tables or views that have Snowflake policies applied

If you want to link in data that has a Snowflake policy applied, and the Snowflake policy is stored in a *different* database than the
source data, you must grant reference usage on the policy database to clean rooms. You can do this either once
per account, or once per clean room.

#### Grant reference usage once per account

To grant reference usage to a database once per account, and have it granted automatically for each clean room, grant reference usage to
SAMOOHA\_APP\_ROLE by running the following SQL command. Replace the database placeholder with your database name.

Copy code

```
GRANT REFERENCE_USAGE ON DATABASE <database_name>
  TO ROLE SAMOOHA_APP_ROLE
  WITH GRANT OPTION;
```

#### Grant reference usage once per clean room

If you prefer to grant reference usage to a database per clean room rather than to all clean rooms in the account, run the following SQL
command. Replace the database name and [clean room ID](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) placeholders with the appropriate values:

Copy code

```
GRANT REFERENCE_USAGE ON DATABASE <database_name>
  TO SHARE IN APPLICATION PACKAGE SAMOOHA_CLEANROOM_<clean_room_ID>;
```

## Unregistering data objects

Once a table is linked into a clean room, it cannot be removed. However, you can unregister the object in the account, which will remove
access by any clean rooms in that account.

If you want to remove data from a clean room or account, don’t simply delete the underlying object; this will cause the clean room
to fail. Instead, use one of the following techniques to unregister the object.

Clean rooms UIClean rooms API

When you unregister an object from an account, you should also update any clean rooms you created that used this data.

Queries by any collaborators that depend on deleted data will fail the next time they are run.

To unregister an object in an account:

1. [Sign in to the Clean rooms UI](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in) as an account administrator and then take one of the following
   steps:

   - If using a managed account, select **Admin > My Account**.
   - If using a Snowflake account, select **Admin > Snowflake Admin** and sign in to Snowflake as a user with the
     ACCOUNTADMIN role.
2. Select **Admin > Snowflake Admin**.
3. Select **Log in to Snowflake**, and authenticate as a user with the ACCOUNTADMIN role.
4. To enable external or Iceberg tables in the account, enable the **External & Iceberg Tables** toggle.
5. In the **Access management for Snowflake objects** section, select **Edit**, and then deselect the database, schema, or object to
   make its data unavailable to users in this account.
6. Select **Save**.
7. Update any clean rooms you created that depend on this data.

In the API, call the appropriate procedure to unregister an object from an account:

- `library.unregister_db`
- `library.unregister_schema`
- `library.unregister_managed_access_schema`
- `library.unregister_objects`

## Enabling external and Apache Iceberg™ tables

To allow external tables and Iceberg tables to be linked into a clean room, the account must first be configured to enable use of
external and Iceberg tables. After external and Iceberg tables are enabled, they can be registered, linked, and used the same as any other
tables.

The process for enabling external and Iceberg tables varies, depending on whether you are managing the clean room using the Clean rooms UI
or the Clean rooms API.

### External and Iceberg table requirements

- **Both the provider and consumer accounts must enable external and Iceberg tables** to allow full usage of a clean room that
  links in external or Iceberg tables.
- **Providers must always enable external tables and Iceberg tables when sharing a clean room with a managed account.** This is because
  managed accounts always use external tables.
- **If the provider and consumer are in different regions,** only the consumer can link external or Iceberg tables into a clean room.

Clean rooms UIClean rooms API

The Clean rooms UI controls external and Iceberg tables at the account level.

Warning

If the consumer account has not enabled this feature, consumers will be blocked from joining any clean rooms that link in external or
Iceberg tables, or will be prevented from editing (but can still run) any already joined clean rooms that link in either type of table.

A DCR administrator in both the provider and consumer accounts must take the following steps:

1. [Sign in to the Clean rooms UI](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in) as an account administrator and then take one of the following
   steps:

   - If using a managed account, select **Admin > My Account**.
   - If using a Snowflake account, select **Admin > Snowflake Admin** and sign in to Snowflake as a user with the
     ACCOUNTADMIN role.
2. Enable the **External & Iceberg Tables** toggle. This enables the feature in both UI-created and API-created clean rooms.
3. External and Iceberg tables are now selectable in the administrator’s
   **Access management for Snowflake objects** panel, where they can be selected to make them available to
   clean rooms, the same as any other objects.

In code, you must enable external and Iceberg tables at **both** the account level **and also** for each clean room that links in
external or Iceberg tables. If you have enabled external and Iceberg tables in the Clean rooms UI, you do not need to enable them in
code (you don’t need to take the steps listed here).

Warning

If only one account has enabled this feature for their account or clean room and linked in an external or Iceberg table, the other
account will be able to run existing templates, but won’t be able to modify the clean room in any way until external and Iceberg
tables are allowed in both that account and clean room.

To enable and use external or Iceberg tables for new clean rooms in code:

1. A user with the ACCOUNTADMIN role first enables external and Iceberg tables for the entire clean room environment in both
   the provider and consumer accounts:

   > Copy code
   >
   > ```
   > USE ROLE ACCOUNTADMIN;
   > CALL samooha_by_snowflake_local_db.library.enable_external_tables_on_account();
   > ```
   >
   > Note
   >
   > Existing clean rooms created with the Clean rooms UI are not affected by this method.
   > To update existing clean rooms created using the Clean rooms UI you must either enable them in code individually, as shown in
   > the next steps, or else enable clean rooms using the Clean rooms UI, which enables the feature for all
   > existing clean rooms.
2. A **provider** enables external and Iceberg tables for their clean room. Note that this triggers a security scan which, if successful,
   generates a new clean room version, so you will need to update the default release directive.

   Copy code

   ```
   USE ROLE SAMOOHA_APP_ROLE;
   CALL samooha_by_snowflake_local_db.provider.enable_external_tables_for_cleanroom(
     $cleanroom_name);

   -- Call until scan is complete.
   CALL samooha_by_snowflake_local_db.provider.view_cleanroom_scan_status($cleanroom_name);

   -- When scan is successful, update with patch version mentioned in return value from enable_external_tables_for_cleanroom.
   CALL samooha_by_snowflake_local_db.provider.set_default_release_directive($cleanroom_name, 'V1_0', '<PATCH_VERSION>');
   ```
3. A **consumer** must also enable use of external and Iceberg tables in the same clean room:

   Copy code

   ```
   USE ROLE SAMOOHA_APP_ROLE;
   CALL samooha_by_snowflake_local_db.consumer.enable_external_tables_for_cleanroom(
     $cleanroom_name);
   ```

After external and Iceberg tables have been enabled for a clean room, collaborators can register and link these tables the same way as
any other table.
