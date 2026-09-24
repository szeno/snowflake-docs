# Snowflake Data Clean Rooms: Provider API reference guide

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

This page describes procedures used by clean rooms API consumers to manage their clean rooms. For coding setup instructions, see [Coding setup](/user-guide/cleanrooms/v1/developer-introduction#label-cleanrooms-coding-setup).

## Create, configure, and delete clean rooms

These procedures enable a provider to create, configure, and delete a clean room.

### view\_cleanrooms

Schema:
:   PROVIDER

**Description:** Lists all existing clean rooms that were created by this provider account.

**Arguments:** *None*

**Returns:** *(Table)* A list of clean rooms created by this provider account. Clean rooms need not be shared to, installed,
or used by consumers. Deleted clean rooms are expunged from the database, and do not appear in this list.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.view_cleanrooms();
```

### describe\_cleanroom

Schema:
:   PROVIDER

**Description:** Get a summary of information about a clean room, such as templates, join policies, column policies, and consumers.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room to get information about.

**Returns:** *(String)* A summary of clean room metadata.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.describe_cleanroom($cleanroom_name);
```

### cleanroom\_init

Schema:
:   PROVIDER

**Description:** Creates a clean room with the specified name in your account. This procedure can take a minute or more to run. The clean
room isn’t visible in the clean rooms UI or to collaborators until after you call `create_or_update_cleanroom_listing`.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Clean room name, 80 characters maximum. Valid characters: `[A-Z,a-z,0-9,_]` and spaces.
- `distribution` - (String, optional) One of the following values:
  - INTERNAL (*Default*) - Clean room is visible only to users in the same organization and does not trigger a security scan before
    [changing the default version](#label-dcr-provider-set-default-release-directive).
  - EXTERNAL - Clean room is production ready and can be shared outside the organization. The clean room triggers a security scan before
    [changing the default version](#label-dcr-provider-set-default-release-directive). If you want to change the distribution after a
    clean room is created, call `ALTER PACKAGE` as shown here:

    Copy code

    ```
    ALTER APPLICATION PACKAGE samooha_cleanroom_<CLEANROOM_ID>
      SET DISTRIBUTION = EXTERNAL;
    ```

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
-- Create an internal clean room
CALL samooha_by_snowflake_local_db.provider.cleanroom_init($cleanroom_name, 'INTERNAL');
```

### set\_default\_release\_directive

Schema:
:   PROVIDER

**Description:** Specifies the version and patch of a clean room loaded by collaborators when they start a new
browser session in the clean rooms UI, or access the clean room from the API. This must be called before the clean room can be shared with
consumers.

The clean room application creates a new version of a clean room whenever you upload or change Python code. If you want users to be served
the newest version, call this procedure with the new version number. To see the available versions and their status, or the current release directive, run the appropriate SQL command:

Copy code

```
-- See all versions, including failed versions.
SHOW VERSIONS IN APPLICATION PACKAGE SAMOOHA_CLEANROOM_<cleanroom_name>;

-- See current release directive.
SHOW RELEASE DIRECTIVES IN APPLICATION PACKAGE SAMOOHA_CLEANROOM_<cleanroom_name>;
```

Where `<cleanroom_name>` [follows this format](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names).

All clean rooms are created with the following version and patch numbers:

- **version**: V1\_0
- **patch**: 0

Note

If the clean room distribution is set to EXTERNAL, this procedure can be called only after the clean room security scan moves to an
APPROVED state. To see the security status, call `view_cleanroom_scan_status`.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Clean room name.
- `version` - (String) Version. Must always be “V1\_0”.
- `patch` - (String) Patch number loaded by the consumer. This starts at 0, and you should increment it whenever a new clean room
  version is available. You can see the available versions as described above.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.set_default_release_directive(
  $cleanroom_name,
  'V1_0', '0'
);
```

### drop\_cleanroom

Schema:
:   PROVIDER

**Description:** Delete the clean room. Collaborators who have the clean room installed can no longer access or use it. The
clean room no longer appears in the clean rooms UI the next time the browser is refreshed.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room to delete.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.drop_cleanroom($cleanroom_name);
```

### enable\_consumer\_run\_analysis

Schema:
:   PROVIDER

**Description:** Enables the consumer to run analyses in the clean room. This capability is enabled by default in all new clean rooms, so
this procedure need only be run if you have explicitly disabled consumer-run analysis for a clean room.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room in which consumer-run analyses are allowed.
- `consumer_accounts` - (Array of string) Account locators of all consumers to enable this feature for. **NOTE:** These consumers must
  already have been added to the clean room.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.enable_consumer_run_analysis(
  $cleanroom_name,
  ['<CONSUMER_ACCOUNT_LOCATOR_1>']
);
```

### disable\_consumer\_run\_analysis

Schema:
:   PROVIDER

**Description:** Prevents the specified consumers from running analyses in the specified clean room. By default, all
consumers are allowed to run an analysis in a clean room.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Clean room where consumer-run analysis is being disabled.
- `consumer_accounts` - (Array of string) Account locators of consumers that cannot run an analysis in this clean room. **NOTE:**
  These consumers must already have been added to the clean room.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.disable_consumer_run_analysis(
  $cleanroom_name,
  ['<CONSUMER_ACCOUNT_LOCATOR_1>']
);
```

### is\_consumer\_run\_enabled

Schema:
:   LIBRARY

**Description:** Checks if this clean room allows consumer-run analyses.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room to check.

**Returns:** *(String)* Whether or not this clean room allows consumer-run analyses.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.library.is_consumer_run_enabled($cleanroom_name)
```

### create\_or\_update\_cleanroom\_listing

Schema:
:   PROVIDER

**Description:** Publishes a new clean room or updates an existing clean room. You should call this method whenever you make changes to
a clean room to ensure that the changes are propagated to consumers.

When publishing a clean room for the first time, it can take up to 15 minutes for the clean room to become visible in the clean rooms UI.

If you make updates to a clean room without calling this method afterwards, there is no guarantee that the changes will
be propagated to consumers.

There is a limit to the number of clean rooms + collaborators that you can create in a single account. If you create too
many test clean rooms, you might need to delete a few in order to create new clean rooms. If you need more clean rooms
than your account can hold, contact Snowflake support.

Note

You must set the release directive at least once before calling this procedure.
For more information, see [provider.set\_default\_release\_directive](#label-dcr-provider-set-default-release-directive).

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room to publish or update.

**Returns:** *(String)* Success message.

**Error handling:**

If you get an error saying that “Cross-Cloud Auto-Fulfillment is not enabled for this account”, it means that one of the
consumers is in another cloud hosting region. You must enable Cross-Cloud Auto-Fulfillment as described in
[Managing Cross-Cloud Auto-Fulfillment in Snowflake Data Clean Rooms](/user-guide/cleanrooms/v1/enabling-laf).

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.create_or_update_cleanroom_listing(
  $cleanroom_name
);
```

## Register and unregister data

Use the following command to register and unregister databases, schemas, and objects. Tables and views must be registered before they can be
linked into the clean room. If you register a database or schema, all of the objects in that database or schema are registered.
[Learn more about registering data.](/user-guide/cleanrooms/register-data)

### register\_db

Schema:
:   PROVIDER

**Description:** Enables a database and all objects within it to be linked into individual clean rooms in this clean room environment.
This procedure grants USAGE and SELECT privileges on the database to SAMOOHA\_APP\_ROLE, which is used by the clean room environment to
access data.

You must have MANAGE GRANTS access on the database to call this procedure. Other providers in this clean room environment can then
link these objects into their own clean rooms without needing their own SELECT privilege.

Important

This procedure does not register any objects created after it was called. If new objects were added to the database and you want to
register those as well, you must call this procedure again.

**Arguments:**

- `db_name` - (String) Name of database to register.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
USE ROLE <role_with_manage_grants>;
CALL samooha_by_snowflake_local_db.provider.register_db('SAMOOHA_SAMPLE_DATABASE');
```

### register\_schema

Schema:
:   LIBRARY

**Description:** Similar to `register_db`, but operates at a schema level. You must have MANAGE GRANTS privilege on the schema to call
this procedure.

This procedure grants USAGE and SELECT privileges on the schema to SAMOOHA\_APP\_ROLE, which is used by the clean room environment to access
data.

If you want to register a managed access schema (that is, a schema created using the WITH MANAGED ACCESS parameter), use
`library.register_managed_access_schema` instead.

Important

This procedure does not register any objects created after it was called. If new objects were added to the database and you want to
register those as well, you must call this procedure again.

**Arguments:**

- `schema_name` - (Array of string) An array of one or more fully qualified schema names to register.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
USE ROLE <role_with_manage_grants>;
CALL samooha_by_snowflake_local_db.library.register_schema(['SAMOOHA_SAMPLE_DATABASE.DEMO']);
```

### register\_managed\_access\_schema

Schema:
:   LIBRARY

**Description:** Similar to `register_schema`, but registers a schema that was created using the WITH MANAGED ACCESS parameter. You must
have MANAGE GRANTS privileges on the schema to call this procedure.

This procedure grants use privileges on the managed schema to SAMOOHA\_APP\_ROLE, which is used by the clean room environment to access data.

Important

This procedure does not register any objects created after it was called. If new objects were added to the database and you want to
register those as well, you must call this procedure again.

**Arguments:**

- `schema_name` - (Array of string) An array of one or more fully qualified schema names.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
USE ROLE <role_with_manage_grants>;
CALL samooha_by_snowflake_local_db.library.register_managed_access_schema(
  ['SAMOOHA_SAMPLE_DATABASE.DEMO']
);
```

### register\_objects

Schema:
:   LIBRARY

**Description:** Grants the clean room access to tables and views of all types, making them available to be linked into the clean room by
calling `provider.link_datasets`. You can register broader groups of objects by calling `library.register_schema`,
`library.register_managed_access_schema`, or `provider.register_db`.

This procedure grants use privileges on the object to SAMOOHA\_APP\_ROLE, which is used by the clean room environment to access data.

You must have MANAGE GRANTS privilege on the object to call this procedure. This procedure cannot be used to register a database.

If you register a view that is based on an object in another database, you must also grant the native application permission to access
the source object.

**Arguments:**

- `object_names` - (array) Array of fully qualified object names. These objects can then be linked into the clean room.

**Returns:** *(String)* Success message.

**Examples**

To register a table and a view:

Copy code

```
USE ROLE <role_with_manage_grants>;
CALL samooha_by_snowflake_local_db.library.register_objects(
  [
    'SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS',
    'SAMOOHA_SAMPLE_DATABASE.INFORMATION_SCHEMA.FIELDS'
  ]
 );
```

### enable\_external\_tables\_on\_account

Schema:
:   LIBRARY

**Description:** Enable Iceberg or external tables to be used in all clean rooms in this account. Must be called by an ACCOUNTADMIN in
both the provider and consumer accounts to allow Iceberg or external tables to be linked by either account. To
limit this ability to specific clean rooms in this account, call `enable_external_tables_for_cleanroom` instead.

If successful and all security scans pass, this generates a [new patch version](/user-guide/cleanrooms/dcr-versions) of the clean
room.

**Arguments:** *None*

**Returns:** *(String)* Success message. If successful, it triggers a security scan and also provide the number of the patch
that will be generated if the security scan succeeds.

**Example:**

Copy code

```
USE ROLE ACCOUNTADMIN;
CALL samooha_by_snowflake_local_db.library.enable_external_tables_on_account();
```

### enable\_external\_tables\_for\_cleanroom

Schema:
:   PROVIDER

**Description:** Enable Iceberg or external tables to be linked into the specified clean room in this account by the provider. To allow
Iceberg and external tables for all clean rooms in this account, call `enable_external_tables_on_account` instead.

If successful, this will generate a [new patch version](/user-guide/cleanrooms/dcr-versions) of the clean room.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - The name of the clean room into which the provider can link Iceberg or external tables.

**Returns:** *(String)* Success message. If successful, it triggers a security scan and also provide the number of the patch
that will be generated if the security scan succeeds.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.enable_external_tables_for_cleanroom(
  $cleanroom_name);
```

### unregister\_db

Schema:
:   LIBRARY

**Description:** Reverses the `register_db` procedure and removes the database-level grants given to the SAMOOHA\_APP\_ROLE role and Snowflake
Data Clean Room native application. This also removes any database from the selector in the clean rooms UI.

**Arguments:**

- `db_name` - (String) Name of the database to unregister.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
USE ROLE <role_with_manage_grants>;
CALL samooha_by_snowflake_local_db.library.unregister_db('SAMOOHA_SAMPLE_DATABASE');
```

### unregister\_schema

Schema:
:   LIBRARY

**Description:** Unregisters a schema, which prevents users from linking its tables and views into the clean room.

If you want to unregister a managed access schema (that is, a schema created using the WITH MANAGED ACCESS parameter), use
`library.unregister_managed_access_schema` instead.

**Arguments:**

- `schema_name` - (array) Schemas to unregister.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
USE ROLE <role_with_manage_grants>;
CALL samooha_by_snowflake_local_db.library.unregister_schema(
  ['SAMOOHA_SAMPLE_DATABASE.DEMO']
);
```

### unregister\_managed\_access\_schema

Schema:
:   LIBRARY

**Description:** Similar to `unregister_schema`, but unregisters a schema that was created using the WITH MANAGED ACCESS parameter.

**Arguments:**

- `schema_name` - (array) Managed schemas to unregister.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
USE ROLE <role_with_manage_grants>;
CALL samooha_by_snowflake_local_db.library.unregister_managed_access_schema(['SAMOOHA_SAMPLE_DATABASE.DEMO']);
```

### unregister\_objects

Schema:
:   LIBRARY

**Description:** Revokes clean room access to tables and views of all types. Objects will no longer be available to any users in any clean
rooms managed by this account.

**Arguments:**

- `object_names` - (array) Array of fully-qualified object names for which access should be revoked.

**Returns:** *(String)* Success message.

**Examples**

To unregister a table and a view:

Copy code

```
USE ROLE <role_with_manage_grants>;
CALL samooha_by_snowflake_local_db.library.unregister_objects(
  [
    'SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS',
    'SAMOOHA_SAMPLE_DATABASE.INFORMATION_SCHEMA.FIELDS'
  ]
);
```

## Link data and tables

Use the following commands to add or remove tables and views in a clean room.

### link\_datasets

Schema:
:   PROVIDER

**Description:** Links a Snowflake table or view into the clean room. The procedure automatically makes the table accessible to the clean
room by creating a secure view of the table within the clean room, without any requirement to copy your table. The table is
linked to its source, so updates in the source appear in the secure version within the clean room.

If the dataset includes a Snowflake policy that is stored in a different database, you (or a clean rooms administrator)
must [grant your clean room access to that policy database](/user-guide/cleanrooms/register-data#label-dcr-link-views-with-external-policies) to enable linking the data
into a clean room.

Any items linked here must be registered first, at the database, schema, or object level.

Note

If a table linked into a clean room is deleted, renamed, moved, or has restrictive permissions added, the table can’t be used in the clean
room until you restore the table using the same location, name, and permissions.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room with access to the objects.
- `tables_list` - (Array of string) List of tables or views to link into the clean room. Objects must be registered before they can be
  linked in.
- `consumer_list` - (Array of string, optional) If present, allows only consumers listed here to access these objects. If absent, allows
  anyone with access to the clean room to access this data.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.link_datasets(
  $cleanroom_name,
  [
    'SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS',
    'MYDB.MYSCH.EXPOSURES'
  ]
);
```

Note

If you link a view into the clean room, and the view is based on a table in another database, you must register both the
view and the source of the view

### unlink\_datasets

Schema:
:   PROVIDER

**Description:** Removes access to the specified tables in the specified clean room for all users. Specified tables must have been linked by
the provider.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of clean room linked to these data sets.
- `tables_list` - (array) Array of table or view names to unlink from the clean room.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.unlink_datasets(
  $cleanroom_name,
  [
    'SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS',
    'MYDB.MYSCH.EXPOSURES'
  ]
);
```

### view\_provider\_datasets

Schema:
:   PROVIDER

**Description:** View all tables and views linked into the specified clean room by any provider in this account.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room.

**Returns:** Table of objects linked into the specified clean room, along with the clean room’s internal view name for each object.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.view_provider_datasets($cleanroom_name);
```

### restrict\_table\_options\_to\_consumers

Schema:
:   PROVIDER

**Description:** Controls whether a particular consumer can access a table in the clean room. This procedure is **replace only**, meaning
that it overwrites completely any values set in a previous call.

Consumers granted access through `provider.link_datasets`, `provider.restrict_table_options_to_consumers`, or any other method will lose
access to a table if it isn’t specified when calling this method.

Note

Restrictions that you create by calling this procedure might not behave as expected in the clean rooms UI. You should not call this
procedure on a clean room that can be used in the clean rooms UI.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room to restrict.
- `access_details` - (Object) A JSON object, where each field name is the fully qualified name of a table or view, and the field value is
  an array of account locators of users who can access that table or view.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.restrict_table_options_to_consumers(
  $cleanroom_name,
  {
    'DB.SCHEMA.TABLE1': ['CONSUMER_1_LOCATOR'],
    'DB.SCHEMA.TABLE2': ['CONSUMER_1_LOCATOR', 'CONSUMER_2_LOCATOR']
  }
);
```

## Manage policies

Join policies in data clean rooms are not the same as [Snowflake-wide join policies](/user-guide/join-policies). Join policies for clean
rooms are set only by using this procedure; join policies set on tables outside of clean rooms are ignored by clean rooms.

[Learn more about table policies in clean rooms.](/user-guide/cleanrooms/v1/policies)

### set\_join\_policy

Schema:
:   PROVIDER

**Description:** Specifies which columns the consumer can join on when running templates within this clean room.

Calling this function completely replaces the old policy with the new one.

Learn more about clean room policies: [Understanding Snowflake Data Clean Room policies](/user-guide/cleanrooms/v1/policies).

Important

Join policies are enforced **only** when the template applies the `join_policy` or `join_and_column_policy` JinjaSQL filters to join rows.

Note

Join policies in data clean rooms are not the same as Snowflake-wide join policies. Join policies for clean rooms are set only by using this procedure; join policies set on tables outside of clean rooms are ignored by clean rooms.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room where the join policy should be enforced.
- `table_and_col_names` - (Array of string) Fully qualified column name in the format
  `database_name.schema_name.table_or_view_name:column_name`. **Note the correct use of . versus : marks**

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.set_join_policy(
  $cleanroom_name,
  [
    'SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:HASHED_EMAIL',
    'MYDB.MYSCH.EXPOSURES:HASHED_EMAIL'
  ]
);
```

### view\_join\_policy

Schema:
:   PROVIDER

**Description:** Shows the provider join policy in the specified clean room.

Learn more about clean room policies: [Understanding Snowflake Data Clean Room policies](/user-guide/cleanrooms/v1/policies).

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room to query.

**Returns:** *(Table)* List of joinable rows on all tables or views in the clean room.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.view_join_policy($cleanroom_name);
```

### set\_column\_policy

Schema:
:   PROVIDER

**Description:** Specifies which columns of your data can be projected in templates run by other collaborators.

Calling this function completely replaces the old policy with the new one.

Don’t set a column policy on identity columns or columns that contain sensitive data, such as email addresses. You generally don’t want this sort of data to be projected.

Queries with wildcards might not be caught by using these checks, so use discretion when you design the analysis template.

Learn more about clean room policies: [Understanding Snowflake Data Clean Room policies](/user-guide/cleanrooms/v1/policies).

**Arguments:**

> - [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room.
> - `analysis_and_table_and_cols` - (Array of string) Array of columns that can be used by templates. The format for each column is:
>   `template_name:full_table_name:column_name`

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.set_column_policy(
  $cleanroom_name,
  ['prod_overlap_analysis:SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:STATUS',
   'prod_overlap_analysis:SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:AGE_BAND',
   'prod_overlap_analysis:SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:DAYS_ACTIVE']);

 -- Same example, but using a variable name for the template.
CALL samooha_by_snowflake_local_db.provider.set_column_policy(
  $cleanroom_name,
  [$template_name || ':SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:STATUS',
   $template_name || ':SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:AGE_BAND',
   $template_name || ':SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:DAYS_ACTIVE']);
```

### view\_column\_policy

Schema:
:   PROVIDER

**Description:** Shows the provider’s column policy in the designated clean room.

Learn more about clean room policies: [Understanding Snowflake Data Clean Room policies](/user-guide/cleanrooms/v1/policies).

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)*

**Returns:** *(Table)* Which columns can be used in which templates.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.view_column_policy($cleanroom_name);
```

## Manage provider templates

Use the following commands to add the templates/analyses that are supported in this clean room.

### view\_added\_templates

Schema:
:   PROVIDER

**Description:** Views the provider-added templates in the clean room. There is no method to list all templates in all clean rooms for
this provider.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Clean room to query.

**Returns:** *(Table)* - List of templates available in the specified clean room, with details about each template.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.view_added_templates($cleanroom_name);
```

### view\_template\_definition

Schema:
:   PROVIDER

**Description:** Shows information about a specific template. Consumers looking at a provider template should use
`consumer.view_template_definition`.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room with this template.
- `template_name` - (String) Name of the template to request information about.

**Returns:** *(String)* The template definition.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.view_template_definition(
  $cleanroom_name,
  $template_name);
```

### add\_templates

Schema:
:   PROVIDER

**Description:** Adds a list of templates to the clean room. This does not replace the existing template list.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room to add templates to.
- `template_names` - (Array of string) Name of the templates to add. These are Snowflake-provided templates only. To add a custom template,
  call `add_custom_sql_template`.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.add_templates(
  $cleanroom_name,
  ['my_custom_template']);
```

### clear\_template

Schema:
:   PROVIDER

**Description:** Removes a specified template from the clean room.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room.
- `template_name` - (String) Name of the template to remove from that clean room.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.clear_template(
  $cleanroom_name,
  'prod_custom_template');
```

### clear\_all\_templates

Schema:
:   PROVIDER

**Description:** Removes all the templates that have been added to the clean room.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room from which to remove all templates.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.clear_all_templates($cleanroom_name);
```

### add\_custom\_sql\_template

Schema:
:   PROVIDER

**Description:** Adds a custom JinjaSQL template into the clean room. This makes the template callable by the consumer.
[Learn how to create custom templates.](/user-guide/cleanrooms/custom-templates)

You can call this API more than once to add multiple custom templates to the clean room. The procedure overwrites any previous template with
the same name in this clean room.

If the template is used by the consumer to [activate results back to the provider](/user-guide/cleanrooms/v1/activation),
the command must meet the following requirements:

- The name of the custom template must begin with the string `activation_`. For example: `activation_custom_template`.
- The template must create a table that begins with `cleanroom.activation_data_`.
  For example: `CREATE TABLE cleanroom.activation_data_analysis_results AS ...`.
- The template must return the unique part of the table name that was created in the definition, which is the string
  appended to `cleanroom.activation_data_`. For example, for the template named `activation_data_analysis_results`, you would return
  `data_analysis_results`.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room to which this template is applied.
- `template_name` - (String) Name of the template. Must be all lowercase letters, numbers, spaces, or underscores. Activation templates must
  have a name beginning with “activation”.
- `template` - (String) The JinjaSQL template.
- `sensitivity` - (Float, optional) If differential privacy is enabled for this clean room, it controls the amount of
  differential privacy noise applied to the data returned by this template. Must be a number greater than 0. Default is 1.0. The
  differential privacy task must be running in this clean room for this argument to have any effect.
- `consumer_locators` - (Array of string, optional) An array of one or more account locators. If present, this template will be added to the
  clean room only for these accounts. You can later modify this list by calling `provider.restrict_template_options_to_consumers`. If you
  don’t specify a list of consumers, all consumers can use the custom template in the specified clean room.
- `is_obfuscated` - (Boolean, optional) If TRUE, prevents consumers from being able to view the template body. Note that you must be using
  Snowflake Enterprise Edition or higher to run an obfuscated template. If this template is used for a provider-run analysis, the consumer
  must re-approve the analysis request any time you change the `is_obfuscated` state. `is_obfuscated` cannot be used together with
  `sensitivity`.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.add_custom_sql_template(
    $cleanroom_name,
    $template_name,
    $$
SELECT
    IDENTIFIER({{ dimensions[0] | column_policy }})
FROM
    IDENTIFIER({{ my_table[0] }}) c
    INNER JOIN
    IDENTIFIER({{ source_table[0] }}) p
    ON
        IDENTIFIER({{ c.consumer_id  }}) = IDENTIFIER({{ provider_id | join_policy }})
    {% if where_clause %}
      WHERE {{ where_clause | sqlsafe | join_and_column_policy }}
    {% endif %};
    $$);
```

### add\_ui\_form\_customizations

Schema:
:   PROVIDER

**Description:** Defines a customization form for a template in a clean room when the clean room is run in the clean rooms UI. This is
useful when you let consumers choose template parameters, such as tables or columns. At a minimum, you must specify values for
`display_name`, *description*, and `methodology` in the `template_information` argument.

It is recommended to put table selection elements before column selection elements, especially when the column choosers populate based on
the table selection.

[Learn how to design user input forms for custom templates.](/user-guide/cleanrooms/demo-flows/custom-templates#label-dcr-define-user-form)

**You must update the clean room after calling this function.** If you do not call `provider.create_or_update_cleanroom_listing` after
updating the UI, collaborators will not see any updates.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - The name of the clean room that contains this template. The submitted form applies only to
  the specified template in the specified clean room.
- `template_name` - (String) Name of the template to which this UI applies. This is not the user-visible title, which is specified using the
  `template_information.display_name` field.
- `template_information` - (Dict) Meta information about the template to show in the clean rooms UI. The following properties must or can be
  defined:

  - `display_name` (**Required**): Display name of the template in the clean rooms UI.
  - `description` (**Required**): Description of the template.
  - `methodology` ( **Required**): Description of any arguments, and what the result is.
  - `warehouse_hints` *(Object)*: Recommends what type of warehouse to use to run the analysis. This is an object with the
    following fields:

    - `warehouse_size`: See *warehouse\_size* in [CREATE WAREHOUSE](/sql-reference/sql/create-warehouse) for valid values.
    - `snowpark_optimized` *(Boolean)*: Whether to use a [Snowpark-optimized warehouse](/user-guide/warehouses-snowpark-optimized) to
      process the query. For most machine learning use cases, Snowflake recommends TRUE.
  - `render_table_dropdowns` *(Object)*: Whether to show the default drop-down lists that let the user select which provider or consumer
    tables to use in the query. This is an object with the following fields:

    - `render_consumer_table_dropdown` - *(Boolean)* If TRUE, show the default consumer table selector. If FALSE, hide the
      consumer tables selector. The template can access the chosen values as a list using the `my_table` template variable. If any element
      sets `references=CONSUMER_TABLES`, this defaults to FALSE, otherwise it defaults to TRUE.
    - `render_provider_table_dropdown` - *(Boolean)* If TRUE, show the default provider table selector. If FALSE, hide the
      provider tables selector. The template can access the chosen values as a list using the `source_table` template variable. If any
      element sets `references=PROVIDER_TABLES`, this defaults to FALSE, otherwise it defaults to TRUE.
  - `activation_template_name` - *(String)* Name of an activation template in this clean room. Use the template name without any
    `cleanroom` prefix. [Learn about activation templates.](/user-guide/cleanrooms/custom-templates#label-dcr-custom-templates-activation)
  - `enabled_activations` - *(String)* Which kind of activations are enabled. Possible values: `consumer`, `provider`. No default; must be
    provided if `activation_template_name` is specified.
- `details` - (Dict, optional) Defines user-configurable input fields that pass values to the template. This is a dictionary of key - object
  pairs, each pair representing one form element. The key is a variable name available to the linked JinjaSQL template.
  The value is an object that defines the form element. If a template variable doesn’t have an equivalent form element defined here, clean
  rooms autogenerates a default form element. Each object can define the following fields:

  Copy code

  ```
  <field_name>: {
    ['display_name': <string>,]
    ['order': <number>,]
    ['description': <string>,]
    ['type': <enum>,]
    ['default': <value>,]
    ['choices': <string array>,]
    ['infoMessage': <string>,]
    ['size': <enum>,]
    ['required': <bool>,]
    ['group': <string>,]
    ['references': <array of string>,]
    ['provider_parent_table_field':  <string>,]
    ['consumer_parent_table_field': <string>]
  }
  ```

  - `display_name`: Label text for this item in the UI form.
  - `order`: 1-based order in which this element should be shown in the form. If not specified, the elements will be rendered in the
    order in which they appear in the object.
  - `description`: A description of the element purpose, shown below the label. Provide short help or examples here. If not provided,
    none is shown.
  - `type`: The type of UI element. If *references* is specified for this input field, then omit this entry (the type is determined for
    you). Supported values:

    - `any` *(Default)*: Regular text entry field.
    - `boolean`: True/False selector
    - `integer`: Use arrows to change the number
    - `multiselect`: Select multiple items from a dropdown list
    - `dropdown`: Select one item from a dropdown list
    - `date`: Date selector
  - `default`: Default value of this element
  - `choices`: *(Array of string)* List of choices for dropdown and multiselect elements
  - `infoMessage`: Informational hovertext shown next to the element. If not provided, no tooltip is provided.
  - `size`: Element size. Supported values: `XS`, `S`, `M`, `L`, `XL`
  - `required`: Whether a value is required by the user. Specify TRUE or FALSE.
  - `group`: A group name, used to group items in the UI. Use the same group name for items that should be grouped together in the UI.
    If you hide the default dropdown lists, you can use the `{{ source_table }}` and `{{ my_table}}` special arguments in the custom
    template, then define your own dropdown list that contains the desired tables. For more information about using these special
    variables when defining the custom template, see [provider.add\_custom\_sql\_template](#dcr-provider-add-custom-sql-template).
  - `references`: Populates a drop-down list with tables or columns of the specified type in the clean room. If used, `type` must be
    either `multiselect` or `dropdown`. The following string values are supported:

    - `PROVIDER_TABLES`: List all the provider’s tables in the clean room. **If specified,**
      `render_table_dropdowns.render_provider_table_dropdown` must be FALSE.
    - `PROVIDER_JOIN_POLICY`: List all columns in the provider’s join policy for the table currently selected in the
      `provider_parent_table_field` element.
    - `PROVIDER_COLUMN_POLICY`: List all columns in the provider’s column policy for the current template and the table selected in
      the `provider_parent_table_field` element.
    - `PROVIDER_ACTIVATION_POLICY`: List all columns in the provider’s activation policy.
    - `CONSUMER_TABLES`: List all the consumer tables in the clean room. **If specified,**
      `render_table_dropdowns.render_consumer_table_dropdown` must be FALSE.
    - `CONSUMER_COLUMNS`: List all columns in the consumer table specified by `consumer_parent_table_field`. You shouldn’t use consumer
      column references in provider-run templates, as the consumer might
      apply join and column policies to these columns; use `CONSUMER_JOIN_POLICY` or `CONSUMER_COLUMN_POLICY` for provider-run
      templates instead.
    - `CONSUMER_JOIN_POLICY`: List all columns in the consumer’s join policy from the table selected in the
      `consumer_parent_table_field` element.
    - `CONSUMER_COLUMN_POLICY`: List all columns in the consumer’s column policy for the current template and the table selected in the
      `consumer_parent_table_field` field.
  - `provider_parent_table_field`: The name of the UI element where the user selects a provider table; don’t provide the
    table name itself here. Use only when `references` is set to `PROVIDER_COLUMN_POLICY` or `PROVIDER_JOIN_POLICY`. To reference
    the default provider table chooser, specify `source_table` here and set `render_table_dropdowns.render_provider_table_dropdown` to TRUE.
  - `consumer_parent_table_field`: The name of the UI element where the user selects a consumer table; don’t provide the
    table name itself here. Use only when `references` is set to `CONSUMER_COLUMNS`, `CONSUMER_JOIN_POLICY`, or
    `CONSUMER_COLUMN_POLICY`. To reference the default consumer table chooser, specify `my_table` here and set
    `render_table_dropdowns.render_provider_table_dropdown` to TRUE.
- `output_config` - (Dict) Defines how to display template results graphically in the clean rooms UI. If not provided, the results are not
  displayed in a graph, only in a table. If you do not want a graph, provide an empty object `{}` for this argument. Allowed fields:

  - `measure_columns`: Names of columns containing measures and dimensions to use in the graph generated by the clean rooms UI.
  - `default_output_type`: The default format to display the results. The user will typically be able to change the display format
    in the UI if the data is in the proper format. Supported types:
    - `TABLE`: *(Default)* Tabular format
    - `BAR`: Bar chart, which is good for comparing different categories
    - `LINE`: Line chart, which is good for showing trends over time or continuous data
    - `PIE`: Pie chart, which is suitable for showing proportions or percentages

The following table shows a matrix of values that are allowed in the `details` object for values that can conflict:

| `type` | `references` | `provider_parent_table_field` | `consumer_parent_table_field` | `render_provider_table_dropdown` | `render_consumer_table_dropdown` |
| --- | --- | --- | --- | --- | --- |
| `multiselect` or `dropdown` | `PROVIDER_TABLES` | *Not allowed* | *Not allowed* | FALSE | TRUE or FALSE |
|  | `PROVIDER_JOIN_POLICY` | `source_table` | *Not allowed* | TRUE | TRUE or FALSE |
|  | `PROVIDER_JOIN_POLICY` | `{parent field name}` | *Not allowed* | TRUE or FALSE | TRUE or FALSE |
|  | `PROVIDER_COLUMN_POLICY` | `source_table` | *Not allowed* | TRUE | TRUE or FALSE |
|  | `PROVIDER_COLUMN_POLICY` | `{parent field name}` | *Not allowed* | TRUE or FALSE | TRUE or FALSE |
|  | `CONSUMER_TABLES` | *Not allowed* | *Not allowed* | TRUE or FALSE | FALSE |
|  | `CONSUMER_COLUMNS` | *Not allowed* | `my_table` or `{parent field name}` | TRUE or FALSE | TRUE |
|  | `CONSUMER_JOIN_POLICY` | *Not allowed* | `my_table` or `{parent field name}` | TRUE or FALSE | TRUE |
|  | `CONSUMER_COLUMN_POLICY` | *Not allowed* | `my_table` or `{parent field name}` | TRUE or FALSE | TRUE |
|  | `PROVIDER_ACTIVATION_POLICY` | *Not allowed* | *Not allowed* | TRUE or FALSE | TRUE or FALSE |

Expand

Show lessSee more

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
-- Specify the display name, description, and warehouse, and hide the default table dropdown lists.
-- Define the following two fields in the UI:
--   A provider table selector that shows all provider tables. Chosen tables can be accessed by the template with the variable 'a_provider_table'
--     (This dropdown list is equivalent to setting ``render_table_dropdowns.render_provider_table_dropdown: True``)
--   A column selector for the tables chosen in 'a_provider_table'. Chosen columns can be accessed by the template with the variable 'a_provider_col'

  CALL samooha_by_snowflake_local_db.provider.add_ui_form_customizations(
      $cleanroom_name,
      'prod_custom_template',
      {
          'display_name': 'Custom Analysis Template',
          'description': 'Use custom template to run a customized analysis.',
          'methodology': 'This custom template dynamically renders a form for you to fill out, which are then used to generate a customized analysis fitting your request.',
          'warehouse_hints': {
              'warehouse_size': 'xsmall',
              'snowpark_optimized': FALSE
          },
          'render_table_dropdowns': {
              'render_consumer_table_dropdown': false,
              'render_provider_table_dropdown': false
          },
          'activation_template_name': 'activation_my_template',
          'enabled_activations': ['consumer', 'provider']
      },
      {
          'a_provider_table': {
              'display_name': 'Provider table',
              'order': 3,
              'description': 'Provider table selection',
              'size': 'S',
              'group': 'Seed Audience Selection',
              'references': ['PROVIDER_TABLES'],
              'type': 'dropdown'
          },
          'a_provider_col': {
              'display_name': 'Provider column',
              'order': 4,
              'description': 'Which col do you want to count on',
              'size': 'S',
              'group': 'Seed Audience Selection',
              'references': ['PROVIDER_COLUMN_POLICY'],
              'provider_parent_table_field': 'a_provider_table',
              'type': 'dropdown'
          }
      },
      {
          'measure_columns': ['col1', 'col2'],
          'default_output_type': 'PIE'
      }
  );
```

### restrict\_template\_options\_to\_consumers

Schema:
:   PROVIDER

**Description:** Controls which users can access a given template in a given clean room. This procedure overrides any access list specified
previously by any other procedure for a clean room/template pair.

Note

Restrictions that you create by calling this procedure might not behave as expected in the clean rooms UI. You should not call this
procedure on a clean room that can be used in the clean rooms UI.

**Arguments:**

> - [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - The name of the clean room.
> - `access_details` - (JSON object) The name of a template and the users who can access that template in that clean room. If a template is
>   specified, only users listed here can access that template in that clean room. This is an object with one child object per template in
>   the following format: `'{template_name': ['user1_locator','user2_locator','userN_locator']}`

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.restrict_template_options_to_consumers(
  $cleanroom_name,
  {
      'prod_template_1': ['CONSUMER_1_LOCATOR', 'CONSUMER_2_LOCATOR']
  }
);
```

## Consumer-defined templates

The following APIs allow you to approve or reject a request from a consumer to add a template to the clean room. A consumer-defined template
is added to a clean room only if the provider approves the consumer’s request to add it. For more information, see
[Consumer-written custom templates](/user-guide/cleanrooms/demo-flows/custom-templates#label-dcr-consumer-written-templates).

### list\_pending\_template\_requests

Schema:
:   PROVIDER

**Description:** Lists all unapproved requests from consumers who want to add a consumer-defined template to a clean room. This includes
pending, approved, and rejected requests. Use this procedure to check for pending requests and approve them
(`provider.approve_template_request`) or reject them (`provider.reject_template_request`).

This will fail until all consumers that the clean room is shared with have installed the clean room.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - View consumer requests to add a template to this clean room.

**Returns:** A table with the following values, among others:

- `request_id` - (String) ID of the request, needed to accept or reject the request.
- `consumer_locator` - (String) Account locator of the person making the request.
- `template_name` - (String) Name of the consumer-provided template.
- `template_definition` - (String) Full definition of the consumer-proposed template.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.list_pending_template_requests($cleanroom_name);
```

### list\_template\_requests

Schema:
:   PROVIDER

**Description:** Lists all requests from consumers who want to add a consumer-defined template to a clean room. This includes pending,
approved, and rejected requests. Use this to check for pending requests and approve them (`provider.approve_template_request`) or reject
them (`provider.reject_template_request`) .

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - View consumer requests to add a template to this clean room.

**Returns:** A table with the following values, among others:

- `request_id` - (String) ID of the request, needed to accept or reject the request.
- `consumer_identifier` - (String) Account locator of the person making the request.
- `template_name` - (String) Name of the consumer-provided template.
- `template_definition` - (String) Full definition of the consumer-proposed template.
- `status` - (String) Status of the request: PENDING, APPROVED, REJECTED.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.list_template_requests($cleanroom_name);
```

### approve\_template\_request

Schema:
:   PROVIDER

**Description:** Approves a request to add a template to the clean room.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room the user wants to add the template to.
- `request_id` - (String) ID of the request to approve. Call `provider.list_template_requests` to see request IDs.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.approve_template_request(
  $cleanroom_name,
  '815324e5-54f2-4039-b5fb-bb0613846a5b'
);
```

### approve\_multiple\_template\_requests

Schema:
:   PROVIDER

**Description:** Approves multiple consumer requests to add a template to a clean room. All requests must be for a single clean room.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - The name of the clean room to which this request applies.
- `request_ids` - (Array of strings) The IDs of all template requests to approve. To obtain a request ID, call
  `provider.list_template_requests`.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.approve_multiple_template_requests(
  $cleanroom_name,
  [
    'cfd538e2-3a17-48e3-9773-14275e7d2cc9',
    '2982fb0a-02b7-496b-b1c1-56e6578f5eac'
  ]
);
```

### reject\_template\_request

Schema:
:   PROVIDER

**Description:** Rejects a request to add a template to a clean room.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room the user wants to add the template to.
- `request_id` - (String) ID of the request to reject. Call `provider.list_template_requests` to see request IDs.
- `reason_for_rejection` - (String) Reason for rejecting the request.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.reject_template_request(
  $cleanroom_name,
  'cfd538e2-3a17-48e3-9773-14275e7d2cc9',
  'Failed security assessment');
```

### reject\_multiple\_template\_requests

Schema:
:   PROVIDER

**Description:** Rejects multiple consumer requests to add a template to a clean room. All requests must be for the same clean room.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room to which this request applies.
- `rejected_templates` - (array of objects) An array of objects with the following fields, one per rejection:
  - `request_id` - (string) ID of the request to reject. To obtain a request ID, call `provider.list_template_requests`.
  - `reason_for_rejection` - (string) A free-text description of why the request is being rejected.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.reject_multiple_template_requests($cleanroom_name,
  [
    OBJECT_CONSTRUCT('request_id', '815324e5-54f2-4039-b5fb-bb0613846a5b', 'reason_for_rejection', 'Failed security assessment'),
    OBJECT_CONSTRUCT('request_id', '2982fb0a-02b7-496b-b1c1-56e6578f5eac', 'reason_for_rejection', 'Some other reason')
  ]
);
```

## Template chains

Use the following commands to create and manage [template chains](/user-guide/cleanrooms/developer-template-chains).

### add\_template\_chain

Schema:
:   PROVIDER

**Description:** Creates a new template chain. Templates must exist before being added to the template chain. After a template chain is
created, it cannot be modified, but you can create a new template chain with the same name to overwrite the old one.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room where the template chain should be added.
- `template_chain_name` - (String) Name of the template chain.
- `templates` - (Array of objects) - Array of objects, one per template. The object can contain the following fields:
  - `template_name` (String) - Specifies the template being added to the template chain. The template must already be added to the clean
    room by calling `provider.add_template_chain`.
  - `cache_results` (Boolean) - Determines whether the results of the template are temporarily saved so other templates in the template
    chain can access them. To cache results, specify TRUE.
  - `output_table_name` (String) - When `cache_results` = TRUE, specifies the name of the Snowflake table where template results are stored.
  - `jinja_output_table_param` (String) - When `cache_results` = TRUE, specifies the name of the Jinja parameter that other templates must
    include to accept the results that are stored in `output_table_name`.
  - `cache_expiration_hours` (integer) - When `cache_results` = TRUE, specifies the number of hours before the results in the cache are
    dropped. When the cache expires, the next time the template chain is executed, the cache is refreshed with the results of the template.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.add_template_chain(
  $cleanroom_name,
  'my_chain',
  [
    {
      'template_name': 'crosswalk',
      'cache_results': True,
      'output_table_name': 'crosswalk',
      'jinja_output_table_param': 'crosswalk_table_name',
      'cache_expiration_hours': 2190
    },
    {
      'template_name': 'transaction_insights',
      'cache_results': False
    }
  ]
);
```

### view\_added\_template\_chains

Schema:
:   PROVIDER

**Description:** Lists the template chains in the specified clean room.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room.

**Returns:** *(Table)* Description of all template chains added to this clean room.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.view_added_template_chains($cleanroom_name);
```

### view\_template\_chain\_definition

Schema:
:   PROVIDER

**Description:** Returns the definition of a template chain.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room associated with this template chain.
- `template_chain_name` - (String) Name of the template chain associated with this clean room.

**Returns:** *(Table)* Description of the specified template chain.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.view_template_chain_definition(
  $cleanroom_name,
  'my_chain');
```

### clear\_template\_chain

Schema:
:   PROVIDER

**Description:** Deletes a specified template chain from a specified clean room. The chain is not stored anywhere, so if you want to
recreate the chain, you must recreate it from scratch.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - The clean room that is assigned this template chain.
- `template_chain_name` - (String) The template chain to remove from this clean room.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.clear_template_chain($cleanroom_name, 'my_chain');
```

## Activation

*Activation* means exporting results to a provider, a consumer, or a third party.
[Read more about activation](/user-guide/cleanrooms/v1/activation).

### set\_activation\_policy

Schema:
:   PROVIDER

**Description:** Defines which provider columns can be used within an activation template. Only columns listed in an activation policy can
be activated from the provider’s data set. Not setting an activation policy prevents any provider data from being activated.

Calling this procedure wipes out any previous activation policy set by the provider.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room where activation should be allowed.
- `columns` - (Array of string) Only columns listed here can be used in an activation template in this clean room. Column name format is
  `template_name:fully_qualified_table_name:column_name`. **Note the proper usage of dot . and colon : markers.**

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.set_activation_policy('my_cleanroom', [
    'prod_overlap_analysis:SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:HASHED_EMAIL',
    'prod_overlap_analysis:SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:REGION_CODE' ]);
```

### view\_activation\_policy

Schema:
:   PROVIDER

**Description:** Shows the provider’s activation policy in the specified clean room.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - The name of the clean room to report on.

**Returns:** *(Table)* The provider’s activation policy in the specified clean room.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.view_activation_policy($cleanroom_name);
```

### request\_provider\_activation\_consent

Schema:
:   PROVIDER

**Description:** Sends a request to the consumer to allow the provider to run a specified template and push the results to the provider’s
Snowflake account. In the background, it adds a template to the list of provider-activation templates in the clean room. Once a template is
designated as an activation template, it can be used only in activation requests.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Clean room that contains the activation template.
- `template_name` - (String) Name of the activation template to request approval for. This template must have been added to the clean room
  in a previous call. The template name must start with “[activation](#activation)”.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.request_provider_activation_consent(
    $cleanroom_name, 'activation_my_activation_template');
```

### update\_activation\_warehouse

Schema:
:   PROVIDER

**Description:** Specify what size warehouse should be used when decrypting results to the output table in a provider activation. The
warehouse used for decryption is DCR\_ACTIVATION\_WAREHOUSE. The provider pays for this warehouse.

**Arguments:**

- `size` - (String) Warehouse size. Choose one of the WAREHOUSE\_SIZE values from the [CREATE WAREHOUSE](/sql-reference/sql/create-warehouse) command.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.update_activation_warehouse('LARGE');
```

### setup\_provider\_activation\_share\_mount\_task

Schema:
:   PROVIDER

**Description:** Enables provider activation when the provider does not have the clean room UI installed on their account.

Call this after adding consumers with `provider.add_consumers`. It is called only when you are implementing provider activation
and you (the provider) do not have the clean room UI installed. (Whether or not the consumer has the UI installed does not matter.)

This starts a thread to asynchronously mount consumer shares needed for provider activation. Rather than mount the shares synchronously and
block your code, this code mounts the share asynchronously and rechecks for new collaborators periodically. You need to call this only
once, and can add additional collaborators later without needing to call this procedure again.

**Arguments:**

- `frequency_minutes` - (Integer) How often to recheck for new consumers in this clean room, in order to mount shares for them as well. A
  recommended value is 15.

**Returns:** *(String)* A success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.setup_provider_activation_share_mount_task(15);
```

### dcr\_health.provider\_run\_provider\_activation\_history

**Description:** Returns a history of provider activation requests for the specified clean room. Provider activation requests initiated by
both the provider and consumer are shown. This procedure provides extra information to help debug problems with provider activation.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room in which the activation was requested. You
  must be a provider or consumer in this clean room.

**Returns:** *(Table)* - A list of activation requests with information about each, including the template and segment name, the status,
the consumer’s account locator, and any error message returned by the request.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.dcr_health.provider_run_provider_activation_history(
  $cleanroom_name);
```

### view\_external\_activation\_history

Schema:
:   LIBRARY

**Description:** View the history of activation requests in the current account.

**Arguments:** *None*

**Returns:** A table with the details and status of activation requests.

**Example**:

Copy code

```
CALL samooha_by_snowflake_local_db.library.view_external_activation_history();
```

## Running analyses as a provider

[Learn how to run a provider analysis.](/user-guide/cleanrooms/demo-flows/provider-run-analysis)

### enable\_provider\_run\_analysis

Schema:
:   PROVIDER

**Description:** Enables the provider (clean room creator) to run analyses in a specified clean room. This is disabled by default. The
consumer must then call `consumer.enable_templates_for_provider_run` to enable provider-run analyses for specific templates in the clean
room. After that, the provider can run an analysis by calling `provider.submit_analysis_request`.

[Learn more about provider-run analyses.](/user-guide/cleanrooms/demo-flows/provider-run-analysis)

Important

This procedure must be called **after** `provider.add_consumers`, and before a consumer installs a clean room. If this is changed
after a consumer has already installed their clean room, then the consumer must reinstall the clean room to reflect the new configuration.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room that should enable provider-run analysis.
- `consumer_accounts` - (Array of string) Account locators of all consumer accounts that have added data to this clean room.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.enable_provider_run_analysis(
  $cleanroom_name,
  ['<CONSUMER_ACCOUNT_LOCATOR>']
);
```

### disable\_provider\_run\_analysis

Schema:
:   PROVIDER

**Description:** Prevents the provider (clean room creator) from running an analysis in the clean room (this is disabled by default).

Important

You must call this procedure **after** calling `provider.add_consumers`, and before a consumer installs a clean room. If the run
analysis setting is changed after a consumer has installed a clean room, then the consumer must reinstall the clean room to implement the
new setting.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room where provider-run analysis should be
  disabled.
- `consumer_account_locator` - (String) Same list of consumer account names passed to `provider.enable_provider_run_analysis`.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.disable_provider_run_analysis(
  $cleanroom_name,
  ['<CONSUMER_ACCOUNT_LOCATOR>']);
```

### is\_provider\_run\_enabled

Schema:
:   LIBRARY

**Description:** Checks if this clean room allows provider-run analyses.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room to check.

**Returns:** *(String)* Whether or not this clean room allows provider-run analyses.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.library.is_provider_run_enabled($cleanroom_name)
```

### is\_request\_back\_share\_mounted

Schema:
:   PROVIDER

**Description:** Checks whether messages can be propagated from the specified consumer to the provider in the specified clean room. If a
back share has not been mounted for this consumer in this clean room, messages such as provider-run request approvals aren’t propagated
from the consumer to the provider (though they will be queued on the consumer side).

Call `provider.mount_request_logs_for_all_consumers` to set up back sharing with this consumer. If you called
`provider.mount_request_logs_for_all_consumers` previously and `is_request_back_share_mounted` fails, it’s likely that you added this
consumer to this clean room after you last called `provider.mount_request_logs_for_all_consumers`.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room to check.
- `consumer_account` - (String) Account locator of the consumer.

**Returns:** SUCCESS if back sharing is enabled for the specified consumer in the specified clean room. Throws an error otherwise.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.library.is_request_back_share_mounted(
  $cleanroom_name,
  $consumer_locator);
```

### view\_warehouse\_sizes\_for\_template

Schema:
:   PROVIDER

**Description:** View the list of warehouse sizes and types available to use in provider-run analyses with a given template. The consumer
must first populate the list in their call to `consumer.enable_templates_for_provider_run`.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room.
- `template_name` - (String) Name of the template that the provider wants to run.
- `consumer_account` - (String) Account locator of the consumer who will approve the provider-run request.

**Returns:** A table of permitted warehouse sizes and types. Supported warehouse type and size strings are those used by the WAREHOUSE\_TYPE
and WAREHOUSE\_SIZE properties in the [CREATE WAREHOUSE](/sql-reference/sql/create-warehouse) command.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.PROVIDER.VIEW_WAREHOUSE_SIZES_FOR_TEMPLATE(
  $cleanroom_name,
  $template_name,
  $consumer_account_loc);
```

### submit\_analysis\_request

Schema:
:   PROVIDER

**Description:** Submits an analysis to run in the clean room. All of the following conditions
must be met before calling this procedure:

- The provider must have [enabled provider-run analyses](#dcr-provider-enable-provider-run-analysis) in this clean room.
- The consumer must have [approved provider-run analyses](#dcr-consumer-enable-templates-for-provider-run) for the specified template.
- All [join](#dcr-consumer-set-join-policy)) and [column](#dcr-consumer-set-column-policy)) policies on the consumer data and the template
  must be respected.

The template runs within the clean room and the results are stored securely inside the clean room. Results are encrypted so only the
provider can see the results.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room where the template should run.
- `consumer_account_locator` - *(String)* Account locator of the consumer in this clean room who has allowed provider-run analyses by
  calling `consumer.enable_templates_for_provider_run`.
- `template_name` - *(String)* Name of the template to run.
- `provider_tables` - *(Array of String)* List of provider tables to expose to the template. This list will populate the `source_table` array variable.
- `consumer_tables` - *(Array of String)* List of consumer tables to expose to the template. This list will populate the `my_table` array variable.
- `analysis_arguments` - *(JSON object)* Pass in any arguments required by the template as key-value pairs.
  The following fields are required only if the consumer specifies a set of allowed warehouse types and sizes. Call `provider.view_warehouse_sizes_for_template` to see if the consumer has specified required warehouse size and type.
  - `warehouse_type` *(String, required only if the consumer specifies a range of permitted types)* - A warehouse type that the consumer allows for provider-run analyses with the specified template. [See the list of supported types](/user-guide/cleanrooms/consumer#label-dcr-consumer-set-provider-run-configuration). If the consumer has not specified a preference, the default is STANDARD.
  - `warehouse_size` *(String, required only if the consumer specifies a range of permitted sizes)* - A warehouse size that the consumer allows for provider-run analyses with the specified template. [See the list of supported types](/user-guide/cleanrooms/consumer#label-dcr-consumer-set-provider-run-configuration). If the consumer has not specified a preference, the default is X-SMALL.

**Returns:** *(String)* A request ID that is used to check the status of the request and also to access the results. **Save this ID**
because you will need it to see the analysis results.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.submit_analysis_request(
  $cleanroom_name,
  '<CONSUMER_ACCOUNT>',
  'prod_overlap_analysis',
  ['SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS'],
  ['SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS'],
  object_construct(
    'dimensions', ['c.REGION_CODE'],
    'measure_type', ['AVG'],
    'measure_column', ['c.DAYS_ACTIVE'],
    'warehouse_type', 'STANDARD',        -- If this type and size pair were not listed by view_warehouse_sizes_for_template,
    'warehouse_size', 'LARGE'            -- the request will automatically fail.
  )
);
```

### check\_analysis\_status

Schema:
:   PROVIDER

**Description:** The provider calls this procedure to check the status of the provider analysis request. There can be a significant delay
before you can start seeing the status of a request. When an analysis is marked as complete, call `provider.get_analysis_result` to see
the results.

All consumers in the clean room must have their request logs mounted before you can call check\_analysis\_status. This is done once per
consumer per clean room by calling `provider.mount_request_logs_for_all_consumers`.

You can see your list of analysis requests by running this SQL command, where `cleanroom_name` is your clean room name, with spaces
replaced by underscores.

Copy code

```
SELECT * FROM SAMOOHA_CLEANROOM_<cleanroom_name>.ADMIN.PROVIDER_ANALYSIS_REQUESTS;
```

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room where the request was made.
- `request_id` - (String) ID of the request, returned by `provider.submit_analysis_request`.
- `consumer_account_locator` - (String) Account locator of the consumer to whom the request was sent.

**Returns:** *(String)* Status of the request, where `COMPLETED` means a successful completion of the analysis. Possible statuses:

- IN-PROGRESS: The analysis is in progress.
- PENDING: Indicates one of the following cases:

  - The request is still propagating, which can take a few minutes. Try again in a few minutes.
  - The user has not approved the request by calling `consumer.enable_templates_for_provider_run`. Try again in a few minutes.
  - You have not mounted the request logs for this consumer. Call `provider.is_request_back_share_mounted`; if that procedure not return
    SUCCESS, call `provider.mount_request_logs_for_all_consumers`.
- COMPLETED: The analysis is complete. You can call `provider.get_analysis_result`.

**Errors:**

If you see an error “ResultSet is empty or not prepared”, this can indicate that at request logs were not mounted for at least one consumer
in this clean room. Call `provider.mount_request_logs_for_all_consumers` to mount request logs for all consumers.

**Example:**

Copy code

```
-- It can take up to 2 minutes for this to pick up the request ID after the initial request
CALL samooha_by_snowflake_local_db.provider.check_analysis_status(
  $cleanroom_name,
  $request_id,
  '<CONSUMER_ACCOUNT>'
);
```

### get\_analysis\_result

Schema:
:   PROVIDER

**Description:** Get the results for a provider-run analysis. Do not call `get_analysis_result` until `provider.check_analysis_status`
returns COMPLETED. Analysis results persist in the clean room indefinitely.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room for which the request was sent.
- `request_id` - (String) ID of the request, returned by `submit_analysis_request`.
- `consumer_account_locator` - (String) Account locator of the consumer passed in to `submit_analysis_request`.

**Returns:** *(Table)* Query results.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.get_analysis_result(
    $cleanroom_name,
    $request_id,
    $locator
);
```

## Manage clean room sharing

Use the following commands to manage sharing a clean room with consumers.

### view\_consumers

Schema:
:   PROVIDER

**Description:** Lists the consumers who are granted access to the clean room. It does not show whether a consumer has installed the clean
room.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - The clean room of interest.

**Returns:** *(Table)* - List of consumer accounts that can access the clean room.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.view_consumers($cleanroom_name);
```

### add\_consumers

Schema:
:   PROVIDER

**Description:** Grants the specified users access to the specified clean room. The clean room can be accessed both through
the clean rooms UI and the API. This doesn’t overwrite the consumer lists from previous calls. Clean room access is granted to a specific
user, not an entire account. The consumer account must be in the same Snowflake region as the provider to be able to access a clean room.
You can check your region by calling `select current_region();`

You can see the current list of consumers by calling `provider.view_consumers`.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room to share with the specified users. Users can install the clean room using either the
  clean rooms API or UI.
- `consumer_account_locators` - (String) A comma-delimited list of consumer account locators, as returned by
  [CURRENT\_ACCOUNT](/sql-reference/functions/current_account). This list should include the same number of entries, in the same order, as contained in
  `consumer_account_names`.
- `consumer_account_names` - (String) A comma-delimited list of
  [consumer data sharing account IDs](/user-guide/admin-account-identifier#label-account-name-data-sharing) for the consumer in the format
  `org_name.account_name` *Org name* can be retrieved by calling [CURRENT\_ORGANIZATION\_NAME](/sql-reference/functions/current_organization_name).
  *Account name* can be retrieved by calling [CURRENT\_ACCOUNT\_NAME](/sql-reference/functions/current_account_name). This list should include the same number
  of items, in the same order, as listed in `consumer_account_locators`.
- `enable_differential_privacy_tasks` - (Boolean, optional) TRUE to enforce differential privacy in all queries by the listed
  users in this clean room. This is a simple way to enable differential privacy with default values for the listed users. To specify
  advanced settings, provide the `privacy_settings` argument instead. The differential privacy task must be running in this clean room to
  enable differential privacy. Default is FALSE.
- `privacy_settings` - (String, optional) If present, applies privacy settings to custom templates when used by any of the users in
  `consumer_account_names`. This is a string version of an object with a single NULL key and a value that specifies various privacy
  settings. Do not specify both `enable_differential_privacy_tasks` and `privacy_settings`. The differential privacy task must be running
  in this clean room to enable differential privacy. [See the available fields for this object.](/user-guide/cleanrooms/differential-privacy#label-dcr-available-privacy-settings)

**Returns:** Success message. Note that the procedure does not validate user locators or account names, so success
indicates only that the submitted locators have been added to the database for this clean room.

**Examples:**

Copy code

```
-- Add consumer without differential privacy.
CALL samooha_by_snowflake_local_db.provider.add_consumers($cleanroom_name,
  'LOCATOR1,LOCATOR2',
  'ORG1.NAME1,ORG2.NAME2');

-- Add consumer and turn on differential privacy for all their queries.
CALL samooha_by_snowflake_local_db.provider.add_consumers($cleanroom_name,
  'LOCATOR1',
  'ORGNAME.ACCOUNTNAME',
  '{
    "null": {
        "threshold_value": 5000,
        "differential": 1,
        "privacy_budget": 10,
        "epsilon": 0.1,
        "noise_mechanism": "Laplace"
    }
  }'
);
```

### remove\_consumers

Schema:
:   PROVIDER

**Description:** Removes account access to a given clean room. This method blocks access by all users in the provided accounts.

You can see the current list of consumers by calling `provider.view_consumers`.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - The ID of the clean room (not the user-friendly name).
- `cleanroom_account_locators` - (String) A comma-delimited list of user account locators. All users in the account will lose access to the
  clean room.

**Returns:** *(String)* - Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.remove_consumers(
  $cleanroom_name,
  'locator1,locator2,locator3'
);
```

### set\_cleanroom\_ui\_accessibility

Schema:
:   PROVIDER

**Description:** Shows or hides the clean room in the clean rooms UI to all users logged in to this provider account.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - The name of the clean room.
- `visibility_status` - (String) One of the following case-sensitive values:
  - HIDDEN - Hides the clean room in the clean rooms UI from all users in the current provider account. The clean room is still accessible
    for API calls.
  - EDITABLE - Makes the clean room visible in the clean rooms UI.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.set_cleanroom_ui_accessibility(
  $cleanroom_name,
  'HIDDEN'
);
```

## Cross-cloud collaboration

Enable a clean room to be shared with a consumer on another cloud region. [Learn more.](/user-guide/cleanrooms/v1/enabling-laf)

### enable\_laf\_on\_account

Schema:
:   LIBRARY

**Description:** Enables Cross-Cloud Auto-Fulfillment on the current account. Running this procedure requires the ACCOUNTADMIN role.

Important

You must first enable Cross-Cloud Auto-Fulfillment for the account by calling
[SYSTEM$ENABLE\_GLOBAL\_DATA\_SHARING\_FOR\_ACCOUNT](/sql-reference/functions/system_enable_global_data_sharing_for_account).

[Learn more about auto-fulfillment](/collaboration/provider-listings-auto-fulfillment) and
[managing auto-fulfillment privileges](/collaboration/provider-listings-auto-fulfillment-manage-privileges).

**Arguments:** *None*

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
USE ROLE ACCOUNTADMIN;
CALL samooha_by_snowflake_local_db.library.enable_laf_on_account();
```

### disable\_laf\_on\_account

Schema:
:   LIBRARY

**Description:** Disables Cross-Cloud Auto-Fulfillment on the current account. Running this procedure requires the ACCOUNTADMIN role.

Important

You must first call [SYSTEM$ENABLE\_GLOBAL\_DATA\_SHARING\_FOR\_ACCOUNT](/sql-reference/functions/system_enable_global_data_sharing_for_account) before you can disable Cross-Cloud
Auto-Fulfillment on an account.

[Learn more about auto-fulfillment](/collaboration/provider-listings-auto-fulfillment) and
[managing auto-fulfillment privileges](/collaboration/provider-listings-auto-fulfillment-manage-privileges).

**Arguments:** *None*

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
USE ROLE ACCOUNTADMIN;
CALL samooha_by_snowflake_local_db.library.disable_laf_on_account();
```

### is\_laf\_enabled\_on\_account

Schema:
:   LIBRARY

**Description:** Returns whether Cross-Cloud Auto-Fulfillment is enabled for this account.

**Arguments:** *None*

**Returns:** TRUE if Cross-Cloud Auto-Fulfillment is enabled for this account, FALSE otherwise.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.library.is_laf_enabled_on_account();
```

### set\_laf\_dcr\_refresh\_schedule

Schema:
:   PROVIDER

**Description:** Sets the refresh interval for [clean room data](/user-guide/cleanrooms/v1/enabling-laf#label-dcr-laf-refresh-rates) between the provider and the consumer
when they are located on different cloud regions. This data includes provider datasets, provider run requests, clean room policies, and clean room metadata. If you need an immediate refresh, you can call [SYSTEM$TRIGGER\_LISTING\_REFRESH](/sql-reference/functions/system_trigger_listing_refresh).

**Arguments:**

- `schedule` - (Int) Interval, in minutes, between refreshes. The minimum allowed value is 10.

**Returns:** *(String)* - Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.set_laf_dcr_refresh_schedule(10);
```

## Use Python in a clean room

### load\_python\_into\_cleanroom

Schema:
:   PROVIDER

**Description:** Loads custom Python code into the clean room. Code loaded into the clean room using this procedure is not visible
to consumers. The uploaded code can be called by your Jinja template. Although your code can include multiple function definitions, only
one function is exposed for a template to call.

If you want to load multiple callable Python packages into a clean room in a single patch, call `prepare_python_for_cleanroom` instead.

[Learn how to upload and use Python code in a clean room.](/user-guide/cleanrooms/demo-flows/custom-code)

This procedure increments the patch number of your clean room and triggers a security scan. You must wait for the scan status to be APPROVED
before you can share the latest version with collaborators. This step does not report syntax errors in the code, which are thrown at run
time.

This procedure is overloaded, and has two signatures that differ in the data type of the fifth argument, which determines whether you are
uploading the code inline or loading it from a file on a stage:

Inline uploadLink from stage

**Signature**

`load_python_into_cleanroom` has the following signature for inline code upload. Pass your code string into the `code` argument.

Copy code

```
(cleanroom_name String, function_name String, arguments Array, packages Array, rettype String, handler String, code String)
```

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room where the script should be loaded.
- `function_name` - (String) Name that a template uses to call the function specified by `handler`.
  The template must qualify the function name with the `cleanroom` namespace. For example: `cleanroom.my_func(val1, val2)`.
- `arguments` - (Array of space-delimited string pairs) An array of arguments required by function `function_name`. Each element
  is a space-delimited `'name data_type'` pair that specifies the argument name and its Snowflake SQL data type. For
  example: `['size INT', 'start_date DATE']`.
- `packages` - (Array of string) List of any Python package names used by the code. Clean rooms natively supports all the packages
  [in this list](https://repo.anaconda.com/pkgs/snowflake/) or the [Snowpark API](https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/snowpark/index).
  If you need a package not listed there, you must use [Snowpark Container Services in a clean room.](/user-guide/cleanrooms/demo-flows/snowpark#label-dcr-snowpark-spcs)
- `ret_type` - (String) SQL data type of the value returned by the function `handler`.
  ([See some equivalent Python and SQL types](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-java-data-type-mappings). Snowflake
  [SQL type synonyms](/sql-reference/intro-summary-data-types) are accepted, such as STRING for VARCHAR.) For a UDF, the return
  type is a single SQL type. For a UDTF, the return type is a TABLE function with `column_name {SQL column type}` pairs. For
  example:
  `TABLE (item_name STRING, total FLOAT)`
- `handler` - (String) The function called in your code when a template calls `function_name`. For a UDF this
  should be the function name itself; for a UDTF, this should be the name of the class that implements the UDTF.
- `code` - (String) Your Python code as a string. This should be a [Python UDF](/developer-guide/udf/python/udf-python-designing).

**Signature**

Upload your code to a Snowflake stage, and then provide the stage location to the clean room API. You must use the stage enabled for your
specific clean room by calling `provider.get_stage_for_python_files`.

`load_python_into_cleanroom` has the following signature to upload code into the clean room from a stage.

Copy code

```
(cleanroom_name String, function_name String, arguments Array, packages Array, imports Array, rettype String, handler String)
```

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room where the script should be loaded.
- `function_name` - (String) Name that a template uses to call the function specified by `handler`.
  The template must qualify the function name with the `cleanroom` namespace. For example: `cleanroom.my_func(val1, val2)`.
- `arguments` - (Array of space-delimited string pairs) An array of arguments required by function `function_name`. Each element
  is a space-delimited `'name data_type'` pair that specifies the argument name and its Snowflake SQL data type. For
  example: `['size INT', 'start_date DATE']`.
- `packages` - (Array of string) List of any Python package names used by the code. Clean rooms natively supports all the packages
  [in this list](https://repo.anaconda.com/pkgs/snowflake/) or the [Snowpark API](https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/snowpark/index).
- `imports` - (Array of string) List of files to import from the stage. Each file address is relative to the stage to where you
  uploaded the code, for example: `['/my_func.py']`. Find the clean room stage by calling `provider.get_stage_for_python_files`.
- `ret_type` - (String) SQL data type of the value returned by the function `handler`.
  ([See some equivalent Python and SQL types](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-java-data-type-mappings). Snowflake
  [SQL type synonyms](/sql-reference/intro-summary-data-types) are accepted, such as STRING for VARCHAR.) For a UDF, the return
  type is a single SQL type. For a UDTF, the return type is a TABLE function with `column_name {SQL column type}` pairs. For
  example:
  `TABLE (item_name STRING, total FLOAT)`
- `handler` - (String) The function called in your code when a template calls `function_name`. For a UDF this
  should be the function name itself; for a UDTF, this should be the name of the class that implements the UDTF.

**Returns:** *(String)* Success message if the upload succ

**Examples:**

Copy code

```
-- Inline UDF

CALL samooha_by_snowflake_local_db.provider.load_python_into_cleanroom(
    $cleanroom_name,
    'assign_group',                      -- Name of the UDF.
    ['data STRING', 'index INTEGER'],    -- Arguments of the UDF, along with their type.
    ['pandas', 'numpy'],                 -- Packages UDF will use.
    'INTEGER',                           -- Return type of UDF.
    'main',                              -- Handler.
    $$
import pandas as pd
import numpy as np

def main(data, index):
    df = pd.DataFrame(data)  # you can do something with df but this is just an example
    return np.random.randint(1, 100)
    $$
);
```

Copy code

```
-- Upload from stage

CALL samooha_by_snowflake_local_db.provider.load_python_into_cleanroom(
    $cleanroom_name,
    'myfunc',                            -- Name of the UDF.
    ['data STRING', 'index INTEGER'],    -- Arguments of the UDF.
    ['numpy', 'pandas'],                 -- Packages UDF will use.
    ['/assign_group.py'],                -- Python file to import from a stage.
    'INTEGER',                           -- Return type of UDF.
    'assign_group.main'                  -- Handler, scoped to file name.
);
```

### prepare\_python\_for\_cleanroom

Schema:
:   PROVIDER

**Description:** Loads custom Python code into the clean room as part of a bulk code upload flow. Call this procedure multiple times to
upload multiple packages, then call `load_prepared_python_into_cleanroom` to trigger the upload to the specified clean room, flush the
pool of prepared code, and generate a new clean room patch.

Uploaded code can be called by your Jinja template. To upload only a single Python bundle, you can call `load_python_into_cleanroom`
instead.

[Learn how to upload and use Python code in a clean room.](/user-guide/cleanrooms/demo-flows/custom-code)

You can either pass code directly into this procedure using the `code` parameter, or pass in the name of a file in a stage that contains
the code using the `imports` parameter.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room where the script should be loaded.
- `function_name` - (String) Name that a template uses to call the function specified by `handler`.
  The template must qualify the function name with the `cleanroom` namespace. For example: `cleanroom.my_func(val1, val2)`.
- `arguments` - (Array of space-delimited string pairs) An array of arguments required by function `function_name`. Each element is a
  space-delimited `'name data_type'` pair that specifies the argument name and its Snowflake SQL data type. For example:
  `['size INT', 'start_date DATE']`.
- `packages` - (Array of string) List of any Python package names used by the code. Clean rooms natively supports all the packages
  [in this list](https://repo.anaconda.com/pkgs/snowflake/) or the
  [Snowpark API](https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/snowpark/index). If you need a package not
  listed there, you must use
  [Snowpark Container Services in a clean room.](/user-guide/cleanrooms/demo-flows/snowpark#label-dcr-snowpark-spcs)
- `imports` - (Array of string) List of Python source files, when importing your source from a stage. Each file address is relative to
  the stage to where you uploaded the code, for example: `['/my_func.py']`. Find the clean room stage by calling
  `provider.get_stage_for_python_files`. If you are providing code inline by using the `code` parameter, provide an empty array.
- `rettype` - (String) SQL data type of the value returned by the function `handler`.
  ([See some equivalent Python and SQL types](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-java-data-type-mappings). Snowflake
  [SQL type synonyms](/sql-reference/intro-summary-data-types) are accepted, such as STRING for VARCHAR.) For a UDF, the return
  type is a single SQL type. For a UDTF, the return type is a TABLE function with `<column name> <SQL column type>` pairs. For
  example:
  `TABLE (item_name STRING, total FLOAT)`
- `handler` - (String) The function called in your code when a template calls `function_name`. For a UDF this
  should be the function name itself; for a UDTF, this should be the name of the class that implements the UDTF.
- `code` - (String) Your Python code as a string. This should be a [Python UDF](/developer-guide/udf/python/udf-python-designing)
  or UDTF. If you are uploading the code from a stage, this should be an empty string.

**Returns:** *(String)* Summary of the upload request, including the patch number before the code is added to the clean room.

**Example:**

This example loads two simple Python procedures into a clean room and triggers only a single patch generation.

Copy code

```
CALL samooha_by_snowflake_local_db.provider.prepare_python_for_cleanroom(
    $cleanroom_name,
    'get_next_status',  -- Name of the UDF. Can be different from the handler.
    ['status VARCHAR'], -- Arguments of the UDF, specified as (variable name, SQL type).
    ['numpy'],          -- Packages needed by UDF.
    [],                 -- When providing the code inline, this is an empty array.
    'VARCHAR',          -- Return type of UDF.
    'get_next_status',  -- Handler.
    $$
import numpy as np
def get_next_status(status):
  """Return the next higher status, or a random status
  if no matching status found or at the top of the list."""

  statuses = ['MEMBER', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND']
  try:
    return statuses[statuses.index(status.upper()) + 1]
  except:
    return 'NO MATCH'
    $$
);

 CALL samooha_by_snowflake_local_db.provider.prepare_python_for_cleanroom(
    $cleanroom_name,
    'hello_world',  -- Name of the UDF.
    [],
    [],
    [],
    'VARCHAR',
    'hello_world',
    $$
import numpy as np
def hello_world():
  return 'Hello world!'
    $$
);

CALL samooha_by_snowflake_local_db.provider.load_prepared_python_into_cleanroom($cleanroom_name);
```

### load\_prepared\_python\_into\_cleanroom

Schema:
:   PROVIDER

**Description:** Takes all code staged using previous calls to `prepare_python_for_cleanroom`, runs a security scan on the code and, if the scan passes, uploads the code to the clean room and generates a new clean room patch. To serve this version of the clean room to users, you must then update the clean room’s release directive to the patch number returned by this procedure by calling
`set_default_release_directive`. Whether or not the call succeeds, it flushes the pool of Python code stored in previous calls to `prepare_python_for_cleanroom`. This step does not report syntax errors, which are only reported when you try to run your code.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room where you want to upload Python code.

**Returns:** *(String)* If successful, returns the new patch number created. Update the clean room’s release directive to the patch number returned by this procedure by calling `set_default_release_directive`.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.load_prepared_python_into_cleanroom($cleanroom_name);
```

### get\_stage\_for\_python\_files

Schema:
:   PROVIDER

**Description:** Returns the stage path where Python files should be uploaded, if you plan to use code files uploaded to a stage rather than
inline code definitions to define custom Python code in a clean room. The stage does not exist, and can’t be examined, until after files
are uploaded by calling `provider.load_python_into_cleanroom`.

[Learn how to upload and use Python code in a clean room.](/user-guide/cleanrooms/demo-flows/custom-code)

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room where you want to upload files.

**Returns:** *(String)* The path where you should upload code files. Use this for the *imports* argument in
`provider.load_python_into_cleanroom`.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.get_stage_for_python_files($cleanroom_name);
```

### view\_cleanroom\_scan\_status

Schema:
:   PROVIDER

**Description:** Reports the threat scan status for a clean room with DISTRIBUTION set to EXTERNAL. The scan needs to be marked as
“APPROVED” before you can set or change the default release directive. Scan status needs to be checked only with EXTERNAL clean rooms.

A scan is run after any action that generates a new patch version; most commonly this is either after you first publish the clean room, or
after you upload Python into the clean room. Snowflake Data Clean Rooms uses the
[Snowflake Native App security scan framework](/developer-guide/native-apps/security-run-scan).

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room to check the status of.

**Returns:** *(String)* The scan status. The following values are possible:

- `NOT_REVIEWED` - The scan is in progress.
- `APPROVED` - The scan passed.
- `REJECTED` - The scan failed; a new clean room version won’t be published. Try to find the problems in your code and
  retry the last action.
- `MANUAL_REVIEW` - The scan requires manual review by Snowflake. This might take a few days, so check again periodically.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.view_cleanroom_scan_status($cleanroom_name);
```

## Request logs

Use the following commands to manage consumer request logs. Request logs enable the consumer to send messages to the provider, and must be
mounted to enable functionality such as consumer custom template requests, consumer approval of provider-run requests, and Cross-Cloud
Auto-Fulfillment.

### mount\_request\_logs\_for\_all\_consumers

Schema:
:   PROVIDER

**Description:** Gives providers access to requests from the consumer. You must mount request logs to support various functionality,
including consumer custom template requests, consumer approval of provider-run requests, and Cross-Cloud Auto-Fulfillment.

This mounts request logs only for consumers that have already installed the specified clean room; if a consumer installs a clean room after
the provider calls this procedure, the provider must call this procedure again.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room to mount request logs for.

**Returns:** *(Table)* A table of consumers, with the request log mount status for each. If a consumer was granted access to a clean room
but hasn’t yet installed the clean room, the status is described as pending, and you should call `mount_request_logs_for_all_consumers`
again after they have installed the clean room.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.mount_request_logs_for_all_consumers($cleanroom_name);
```

### view\_request\_mount\_status\_for\_all\_consumers

Schema:
:   PROVIDER

**Description:** Shows the mount status of request logs for all consumers in the specified clean room. Only consumers that were included in
a call to `provider.mount_request_logs_for_all_consumers` are shown. Request logs enable messages to be passed from the consumer to the
provider.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room.

**Returns:** *(Table)* - A table of consumers and the request log mount status of each consumer.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.view_request_mount_status_for_all_consumers($cleanroom_name);
```

### view\_request\_logs

Schema:
:   PROVIDER

**Description:** Shows the request logs sent by consumers in this clean room. Only requests from consumers who were included in a previous
successful call to `mount_request_logs_for_all_consumers` are shown.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room to review request logs for.

**Returns:** *(Table)* The requests sent by the consumer to the provider in the specified clean room.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.view_request_logs($cleanroom_name);
```

## Differential privacy

These commands control differential privacy at the user level or provider account level. [Learn more about differential privacy.](/user-guide/cleanrooms/differential-privacy)

### set\_privacy\_settings

Schema:
:   PROVIDER

**Description:** Set (or reset) privacy settings enforced when the specified consumer runs a custom template. This
overwrites all existing settings for this consumer.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room.
- `consumer_account_locator` - (String) Account locator of one or more consumers, in a comma-delimited list.
- `privacy_settings` - (Object) A JSON object that specifies differential privacy settings for one or more templates. Settings are applied
  to all templates run by the specified consumer. [See the available fields for this object.](/user-guide/cleanrooms/differential-privacy#label-dcr-available-privacy-settings)

**Returns:** Success message.

**Example:**

Copy code

```
-- Enforce differential privacy on queries by this consumer
-- with the settings provided.
CALL samooha_by_snowflake_local_db.provider.set_privacy_settings(
  $cleanroom_name,
  $consumer_locator,
  { 'differential': 1,
    'epsilon': 0.1,
    'privacy_budget': 3 });
```

### is\_dp\_enabled\_on\_account

Schema:
:   PROVIDER

**Description:** Describes whether or not differential privacy is enabled for this account.

**Arguments:** *None*

**Returns:** TRUE if differential privacy is enabled for this account, FALSE otherwise.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.is_dp_enabled_on_account();
```

### suspend\_account\_dp\_task

Schema:
:   PROVIDER

**Description:** Disables the task that monitors and enforces differential privacy budgets. This is used to control the
[costs associated with differential privacy in your account](/user-guide/cleanrooms/cleanroom-cost). If the differential privacy task is
disabled, noise will still be added to queries by users, templates, or clean rooms where differential privacy is specified, but budget
limits will not be enforced and you will not incur costs from differential privacy.
[Learn more about managing differential privacy.](/user-guide/cleanrooms/differential-privacy)

**Arguments:** *None*

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.suspend_account_dp_task();
```

### resume\_account\_dp\_task

Schema:
:   PROVIDER

**Description:** Resumes the differential privacy task listener in the current account, and differential privacy budgets will be enforced.
Any differential privacy values previously set (such as sensitivity or associated users) are retained.

**Arguments:** *None*

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.resume_account_dp_task();
```

## Snowpark Container Services commands

These procedures enable you to [use Snowpark Container Services inside a clean room](/user-guide/cleanrooms/demo-flows/snowpark#label-dcr-snowpark-spcs).

### load\_service\_into\_cleanroom

Schema:
:   PROVIDER

**Description:** Creates or updates a container service in a clean room. Calling this procedure updates the clean room patch number, so you
must call `provider.set_default_release_directive` after calling this procedure. You must call this procedure every time you create or
update the service. The client must then call `consumer.start_or_update_service` to see any updates.

[Learn about using Snowpark Container Services in a clean room.](/user-guide/cleanrooms/demo-flows/snowpark#label-dcr-snowpark-spcs)

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room.
- `service_spec` - (String) A YAML specification for the service, rooted at the `spec` element.
- `service_config` - (String) A YAML format configuration for the service. The following properties are supported:
  - `default_service_options` - An optional array of service-level default values. These values can be overridden by the consumer when
    they create their service. The following child properties are supported:

    - `min_instances` *(Integer, optional)*
    - `max_instances` *(Integer, optional)*
    - `allow_monitoring` *(Boolean, optional)* - If TRUE, allows the consumer to see service logs. Default is FALSE.
  - `functions` - An array of functions exposed by the service. Each function definition maps to the
    [SPCS service function definition](/sql-reference/sql/create-function-spcs). See that documentation to learn the details of each
    element. The following child properties are supported:

    - `name`
    - `args`
    - `returns`
    - `endpoint`
    - `path`
    - `max_batch_rows` (*optional*)
    - `context_headers` (*optional*)

**Returns:** (*String*) Success message, if successful. Throws an error if not successful.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.load_service_into_cleanroom(
    $cleanroom_name,
    $$
    spec:
      containers:
      - name: lal
        image: /dcr_spcs/repos/lal_example/lal_service_image:latest
        env:
          SERVER_PORT: 8000
        readinessProbe:
          port: 8000
          path: /healthcheck
      endpoints:
      - name: lalendpoint
        port: 8000
        public: false
    $$,
    $$
    default_service_options:
      min_instances: 1
      max_instances: 1
      allow_monitoring: true

    functions:
      - name: train
        args: PROVIDER_TABLE VARCHAR, PROVIDER_JOIN_COL VARCHAR, CONSUMER_TABLE VARCHAR, CONSUMER_JOIN_COL VARCHAR, DIMENSIONS ARRAY, FILTER VARCHAR
        returns: VARCHAR
        endpoint: lalendpoint
        path: /train
      - name: score
        args: PROVIDER_TABLE VARCHAR, PROVIDER_JOIN_COL VARCHAR, CONSUMER_TABLE VARCHAR, CONSUMER_JOIN_COL VARCHAR, DIMENSIONS ARRAY
        returns: VARCHAR
        endpoint: lalendpoint
        path: /score
      - name: score_batch
        args: ID VARCHAR, FEATURES ARRAY
        returns: VARIANT
        max_batch_rows: 1000
        endpoint: lalendpoint
        path: /scorebatch
$$);
```

## Environment management

Use the following commands to generally assist in leveraging clean room functionality and supported flows.

### manage\_datastats\_task\_on\_account

Schema:
:   PROVIDER

**Description:** Enables or disables the background task that computes clean room statistics. The task is running by default, but you can
disable it to reduce your costs. To manage the task, all collaborators must call the appropriate `provider` or `consumer` version of this
procedure with the same value.

**Arguments:**

- `enable` - (Boolean) TRUE to enable the task, FALSE to disable the task.

**Returns:** Success message.

**Example:**

Copy code

```
-- Disable the task in this account.
CALL samooha_by_snowflake_local_db.provider.manage_datastats_task_on_account(FALSE);
```

### enable\_local\_db\_auto\_upgrades

Schema:
:   LIBRARY

**Description:** Enables the task that automatically upgrades the Snowflake Data Clean Rooms environment when new procedures or
functionality is released (The task is `samooha_by_snowflake_local_db.admin.expected_version_task`. ) Call this procedure to automate
upgrades, rather than calling `library.apply_patch` with each new release.

Although you might reduce cost by disabling this task, we recommend that you leave it running to ensure that you have the latest version of
the clean rooms environment on your system.

**Arguments:** *None*

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.library.enable_local_db_auto_upgrades();
```

### disable\_local\_db\_auto\_upgrades

Schema:
:   LIBRARY

**Description:** Disables the task that automatically upgrades the Snowflake
Data Clean Rooms environment when new versions are released. If you disable auto upgrades, you must call
`library.apply_patch` with each [new release](/release-notes/new-features#label-new-features-features).

**Arguments:** *None*

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.library.disable_local_db_auto_upgrades();
```

### apply\_patch

Schema:
:   LIBRARY

**Description:** Updates your clean rooms environment, enabling new features and fixes in your environment. Call this when a new version of
the clean rooms environment has been released. (This typically occurs weekly; see clean rooms entries in
[Recent feature updates](/release-notes/new-features#label-new-features-features).) This procedure updates [samooha\_by\_snowflake\_local\_db](/user-guide/cleanrooms/v1/installation-details).

You can automate patch updates by calling `library.enable_local_db_auto_upgrades`. We recommend enabling auto-updates.

**Arguments:** *None*

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.library.apply_patch();
```

### patch\_cleanroom

Schema:
:   PROVIDER

**Description:** Updates the specified clean room to the latest version, enabling new features and fixes for that clean room. Typically you
call this only when Snowflake Support tells you to call it.

The provider should call `library.patch_cleanroom` before the consumer calls `library.patch_cleanroom`. Otherwise, there is no patch to
apply.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* : Name of the clean room to patch.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.patch_cleanroom($cleanroom_name);
```

### dcr\_health.dcr\_tasks\_health\_check

**Description:** Shows information about running or recently stopped clean room tasks.

**Arguments:** *None*

**Returns:** *(Table)* Information about clean room tasks, including the schedule, warehouse name, and warehouse size.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.dcr_health.dcr_tasks_health_check();
```
