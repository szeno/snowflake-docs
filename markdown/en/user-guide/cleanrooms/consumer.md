# Snowflake Data Clean Rooms: Consumer API reference guide

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

This page describes procedures used by clean rooms API consumers to manage their clean rooms. For coding setup instructions, see [Coding setup](/user-guide/cleanrooms/v1/developer-introduction#label-cleanrooms-coding-setup).

## Manage role access

### grant\_run\_on\_cleanrooms\_to\_role

Schema:
:   CONSUMER

**Description:** Grants the specified role permission to run a subset of procedures on the specified clean rooms. Clean rooms must be
*installed* in this account, not *created* by this account. (That is, only clean rooms for which you are a consumer.)

To grant limited use to your clean rooms, grant users the specified role rather than SAMOOHA\_APP\_ROLE.
For more information about role access, see [Grant limited API access (run roles)](/user-guide/cleanrooms/manage-dcr-users#label-dcr-grant-limited-access).

The following procedures can be run using a role specified here:

- consumer.view\_added\_templates
- consumer.view\_added\_template\_chains
- consumer.get\_arguments\_from\_template
- consumer.view\_column\_policy
- consumer.view\_consumer\_datasets
- consumer.view\_join\_policy
- consumer.view\_provider\_column\_policy
- consumer.view\_provider\_datasets
- consumer.view\_provider\_join\_policy
- consumer.view\_remaining\_privacy\_budget
- consumer.run\_analysis
- consumer.view\_provider\_activation\_policy
- consumer.view\_activation\_policy
- consumer.run\_activation

**Arguments:**

- [cleanroom\_names](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(Array of strings)* - Names of all the clean rooms on which to grant limited access to the specified role.
- `run_role_name` - (String) Name of a role that has limited permissions on the specified clean rooms. You must create the role
  before calling this procedure.

**Returns:** *(String)* - Success message.

**Example:**

Copy code

```
CREATE ROLE MARKETING_ANALYST_ROLE;
CALL samooha_by_snowflake_local_db.consumer.grant_run_on_cleanrooms_to_role(
  ['overlap_cleanroom', 'market_share_cleanroom'],
  'MARKETING_ANALYST_ROLE'
);
```

### revoke\_run\_on\_cleanrooms\_from\_role

Schema:
:   CONSUMER

**Description:** Revokes permissions from the specified roles on the specified clean rooms. If the user has access to a
non-revoked role, or has the SAMOOHA\_APP\_ROLE, they can still run clean room procedures in the specified clean rooms.

**Arguments:**

- [cleanroom\_names](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(Array of strings)* - Names of one or more clean rooms in this account.
- `run_role_name` - (String) Name of role that should no longer have limited permissions on the specified clean rooms in this
  account.

**Returns:** *(String)* - Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.revoke_run_on_cleanrooms_from_role(
  ['overlap_cleanroom', 'market_share_cleanroom'],
  'TEMP_USERS_ROLE'
);
```

## Install a clean room

Procedures to install or uninstall a clean room.

### install\_cleanroom

Schema:
:   CONSUMER

**Description:** Installs (joins) the clean room created by the specified provider. Calling this multiple times clears out the
existing clean room each time; if you interrupt a second installation before it’s complete, the clean room becomes corrupted, and you will
need to complete this procedure to make the clean room usable.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room to install.
- `provider_account_locator` - (String) Account locator of the provider who created this clean room.

**Returns:** *(String)* Success message.

**Error handling:**

If you get an error saying that “Cross-Cloud Auto-Fulfillment is not enabled for this account”, it means
that the provider is in another cloud hosting region. You must enable Cross-Cloud Auto-Fulfillment as described in
[Managing Cross-Cloud Auto-Fulfillment in Snowflake Data Clean Rooms](/user-guide/cleanrooms/v1/enabling-laf).

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.install_cleanroom(
  $cleanroom_name,
  $provider_locator);
```

### is\_enabled

Schema:
:   CONSUMER

**Description:** There can be a short delay after clean room installation before it is ready to use. You might call this procedure to
confirm whether or not the clean room is ready for use after installation.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of clean room to check the status of.

**Returns:** *(Boolean)* Whether or not the specified clean room is installed and ready to use.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.is_enabled($cleanroom_name);
```

### uninstall\_cleanroom

Schema:
:   CONSUMER

**Description:** Uninstalls the clean room on the consumer account. This removes all databases associated with the clean room, including
the shared clean room database. The clean room can always be installed again by calling `consumer.install_cleanroom`.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of clean room to uninstall.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.uninstall_cleanroom($cleanroom_name);
```

## Cross-cloud collaboration

Install a clean room created on another cloud region. [Learn more.](/user-guide/cleanrooms/v1/enabling-laf)

### enable\_laf\_on\_account

Schema:
:   LIBRARY

**Description:** Enables Cross-Cloud Auto-Fulfillment on the current account. Requires ACCOUNTADMIN role.

Important

You must first enable Cross-Cloud Auto-Fulfillment for your account by calling
[SYSTEM$ENABLE\_GLOBAL\_DATA\_SHARING\_FOR\_ACCOUNT](/sql-reference/functions/system_enable_global_data_sharing_for_account).

[Learn more about auto-fulfillment](/collaboration/provider-listings-auto-fulfillment)
and [managing auto-fulfillment privileges](/collaboration/provider-listings-auto-fulfillment-manage-privileges).

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

**Description:** Disables Cross-Cloud Auto-Fulfillment on the current account. Requires ACCOUNTADMIN role.

Important

You must call [SYSTEM$ENABLE\_GLOBAL\_DATA\_SHARING\_FOR\_ACCOUNT](/sql-reference/functions/system_enable_global_data_sharing_for_account) before calling this
procedure.

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

### is\_laf\_enabled\_for\_cleanroom

Schema:
:   CONSUMER

**Description:** Describes whether or not cross-cloud auto-fulfillment has been enabled for this clean room. Cross-cloud auto-fulfillment
[must be configured by an account administrator](/user-guide/cleanrooms/v1/enabling-laf).

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room.

**Returns:** Whether or not cross-cloud auto-fulfillment has been enabled for this clean room.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.is_laf_enabled_for_cleanroom($cleanroom_name);
```

### request\_laf\_cleanroom

Schema:
:   CONSUMER

**Description:** Sets up prerequisites for installing a clean room created on another cloud region. Calling `consumer.install_cleanroom`
before calling this procedure fails. This procedure returns the current status each time you call. Call periodically until
the status is FULFILLED, then call `consumer.install_cleanroom`. It can take up to 10 minutes until the status is FULFILLED.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - The name of the cross-region clean room that will be installed.
- `provider_locator` - (String) Account locator of the provider that created this clean room.

**Returns:** *(String)* Status message of the request. Continue calling until status is FULFILLED.

**Example:**

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.consumer.request_laf_cleanroom(
  $cleanroom_name,$provider_locator);
```

### setup\_cleanroom\_request\_share\_for\_laf

Schema:
:   CONSUMER

**Description:** Enables cross-cloud request sharing with a specified provider for a specific clean room. This is required for cross-region clean rooms to have full functionality, including request logs, consumer template requests, and provider-run analyses.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Clean room name.
- `provider_account_name` - (String) [Data sharing account identifier](/user-guide/admin-account-identifier#label-account-name-data-sharing) of the provider.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.setup_cleanroom_request_share_for_laf(
      $cleanroom_name, $provider_account_name);
```

### setup\_activation\_share\_to\_laf\_consumer

Schema:
:   CONSUMER

**Description:** Enables provider activation between a provider and a consumer on different cloud regions.

**Arguments:**

- `provider_account` - (String) One or more comma-delimited provider [Data sharing account identifiers](/user-guide/admin-account-identifier#label-account-name-data-sharing).

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.setup_activation_share_to_laf_consumer(
  'org1.locator1,org2.locator2'
);
```

## Provider-run analysis

For more information about provider-run analysis, see [Provider-run analyses](/user-guide/cleanrooms/demo-flows/provider-run-analysis).

### is\_provider\_run\_enabled

Schema:
:   LIBRARY

**Description:** Checks if this clean room allows provider-run analyses. The consumer must still grant explicit permission by
calling `consumer.enable_templates_for_provider_run` before providers can run an analysis in this clean room.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Clean room name.

**Returns:** *(String)* Description of whether or not the clean room supports provider-run analyses.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.library.is_provider_run_enabled($cleanroom_name)
```

### approve\_template

Schema:
:   CONSUMER

**Description:** Approves a single template for provider-run analysis in a given clean room. The clean room provider typically communicates
with you beforehand to ask permission to run a specific template in a clean room. Be sure to set join and column policies on a template
before you approve it for provider-run analysis:

- A clean room **without** a consumer join policy means that the provider can join on all consumer columns.
- A clean room **without** a consumer column policy means that the provider can project all consumer columns.
- A clean room **with** a consumer column policy that **doesn’t include this approved template** means that the provider cannot project any
  consumer columns when using this template.

`consumer.approve_template` grants the provider permission to run the specified template in the specified clean room as many times as they want. Any provider calls to `provider.submit_analysis_request` are against the last approved version of the template; if the provider later modifies the template, the last approved version will be run when `provider.submit_analysis_request` is called.

If you want to approve multiple templates at once, you can call `provider.enable_templates_for_provider_run`.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room with the template to approve.
- `template_name` - (String) Name of the template that the provider can run, in the specified clean room.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.approve_template(
  $cleanroom_name,
  $template_name);
```

### enable\_templates\_for\_provider\_run

Schema:
:   CONSUMER

**Description:** Grants permission to the provider to run one or more specified templates in the requested clean room. The provider must
enable provider-run analysis in a clean room before the consumer can call this procedure. This is a multi-template version of
`consumer.approve_template`, and has all the same requirements and restrictions.

`consumer.enable_templates_for_provider_run` grants the provider permission to run the specified templates in the specified clean room as
many times as they want. Any provider calls to `provider.submit_analysis_request` are against the last approved version of the template;
if the provider later modifies the template, the last approved version will be run when `provider.submit_analysis_request` is called.

Providers run enabled templates in the consumer’s account, with the usage billed to the consumer. If you want to limit the warehouse type or
sizes allowed to a provider when running a given template, call `set_provider_run_configuration`.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - The name of the clean room where the provider can run analyses.
- `template_names` - (Array of strings) An array of names of one or more templates in the clean room that the provider can run.
- `enable_differential_privacy` - (Boolean) If TRUE, enable differential privacy for all templates listed in `template_names`.
  Differential privacy can be enabled for these templates only if differential privacy is enabled for the clean room itself. You can check
  differential privacy status for a clean room by calling `consumer.is_dp_enabled`. You can customize the privacy settings by calling
  `consumer.set_privacy_settings`. [Learn more.](/user-guide/cleanrooms/differential-privacy)
- `template_configuration` - (Object, optional) An optional object to specify additional settings for each template in `template_names`.
  This object contains key-value pairs, where the key is the template name (from `template_names`) and the value is an object that sets
  limitations on how the provider can use this template. **If you do not provide a template configuration**, ‘ALL’ is the default for all
  properties for all templates in `template_names`. **If you do provide a template configuration**, you must provide a configuration for
  every template listed in `template_names`, and define all properties for that template’s configuration. You can also set the permissible
  values for a template by calling `consumer.set_provider_run_configuration`.

  The following properties are supported:

  - `warehouse_type` (*String*) - A permitted warehouse type that the provider can use with this template. Allowed values:

    - ALL - Allow any warehouse type.
    - STANDARD - Allow only a standard warehouse.
    - SNOWPARK-OPTIMIZED - Allow only a Snowpark-optimized warehouse.
  - `warehouse_size` (*Array of strings*) - One or more permitted warehouse sizes that can be used with this warehouse type and template.
    Allowed values are those defined for [WAREHOUSE\_SIZE](/sql-reference/sql/create-warehouse) or their synonyms (for example, either
    XLARGE or X-LARGE). Specify ‘ALL’ to allow any warehouse size.

**Returns:** *(String)* Success message.

**Examples:**

Copy code

```
-- Simple example
CALL samooha_by_snowflake_local_db.consumer.enable_templates_for_provider_run(
  $cleanroom_name,
  ['prod_overlap_analysis'],
  FALSE);

-- Specify what types of warehouse the provider can use to run these templates.
CALL samooha_by_snowflake_local_db.CONSUMER.enable_templates_for_provider_run(
  $cleanroom_name,
  ['template1', 'template2', 'template3'],
  TRUE,
  {
    'template1': {'warehouse_type': 'ALL', 'warehouse_size': ['MEDIUM', 'LARGE']},
    'template2': {'warehouse_type': 'SNOWPARK-OPTIMIZED', 'warehouse_size': ['MEDIUM', 'XLARGE']},
    'template3': {'warehouse_type': 'STANDARD', 'warehouse_size': ['MEDIUM', 'XLARGE']}
  });
```

### set\_provider\_run\_configuration

Schema:
:   CONSUMER

**Description:** Applies settings to a template that control how a provider can run a specified template in the clean room. If the consumer
does not provide a configuration for a template, then default values are applied. A provider cannot run a template until a consumer approves
the template for provider-run analyses by calling `consumer.approve_template`.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room. If the template is not present in this
  clean room, the procedure throws an error. The template doesn’t need to be approved for provider-run analysis yet, but the provider won’t
  be able to run the template until the consumer approves it.
- `template_configuration` - (Object) An object that provides limits on how a provider can run a specific template in this clean room.
  Provider-run analyses are run in the consumer’s account, and billed to the consumer, so the consumer can set limitations on what
  warehouses can be used for a given template. The configuration object has this form:

  Copy code

  ```
  {
    <template_name>: {
      'warehouse_type': '<warehouse_type>',
      'warehouse_size': '<warehouse_size>'
    }
  }
  ```

  You must provide all of the following values:

  - `template_name` - The object key is the template name. The configuration is applied to this template. This template must be
    present in the clean room.
  - `warehouse_type` (*String*) - Which warehouse type the provider can use to run this template. Allowed values:
    - ALL - (*Default*) Allow any warehouse type.
    - STANDARD - Allow only a standard warehouse.
    - SNOWPARK-OPTIMIZED - Allow only a Snowpark-optimized warehouse.
      XLARGE or X-LARGE) is supported.
    - ALL - (*Default*) Any warehouse size allowed.
    - Any size defined for [WAREHOUSE\_SIZE](/sql-reference/sql/create-warehouse), or their synonyms (for example, either
      XLARGE or X-LARGE) is supported.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.set_provider_run_configuration(
  $cleanroom_name,
  {
    'some_template': {
      'warehouse_type': 'STANDARD',
      'warehouse_size': ['MEDIUM', 'LARGE']
    }
  }
);
```

## Register and unregister data

Use the following procedures to register and unregister databases, schemas, and objects. Tables and views must be registered before they can
be linked into the clean room. If you register a database or schema, all of the objects in that database or schema are registered.
For more information about registering data, see [Registering data](/user-guide/cleanrooms/register-data).

### register\_db

Schema:
:   CONSUMER

**Description:** Register a database in an account to be able to link any objects from that database into a clean room in that account.
For more fine-grained control you can call `register_schema`, `register_managed_access_schema`, or `register_object` instead. Objects added
to the database after it has been registered might not be linkable, in which case you should re-register the database (or register the
object itself).

You must have MANAGE GRANTS privileges on the database to run this procedure.

**Arguments:**

- `db_name` - (String) Name of database to register in this account.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
USE ROLE <ROLE_WITH_MANAGE_GRANTS>;
CALL samooha_by_snowflake_local_db.consumer.register_db('SAMOOHA_SAMPLE_DATABASE');
```

### register\_schema

Schema:
:   LIBRARY

**Description:** Register a schema in an account to be able to link any objects from that schema into a clean room in that account.
For more fine-grained control you can call `register_object` instead. Objects added to the schema after it has been registered might not be linkable, in which case you should re-register the schema (or register the object itself).

If you want to register a managed access schema (that is, a schema created with the WITH MANAGED ACCESS parameter), use `library.register_managed_access_schema` instead.

**Arguments:**

- `schema_names` - (Array of strings) Array of fully qualified schemas to register.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
USE ROLE <ROLE_WITH_MANAGE_GRANTS>;
CALL samooha_by_snowflake_local_db.library.register_schema(
  ['SAMOOHA_SAMPLE_DATABASE.DEMO']
);
```

### register\_managed\_access\_schema

Schema:
:   LIBRARY

**Description:** Register a managed access schema in an account to be able to link any objects from that schema into a clean room in that
account. For more fine-grained control you can call `register_object` instead. Objects added to the schema after it has been registered
might not be linkable, in which case you should re-register the schema (or register the object itself).

**Arguments:**

- `schema_names` - (Array of strings) Array of fully qualified managed schemas to register.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
USE ROLE <ROLE_WITH_MANAGE_GRANTS>;
CALL samooha_by_snowflake_local_db.library.register_managed_access_schema(
  ['SAMOOHA_SAMPLE_DATABASE.DEMO']
);
```

### register\_objects

Schema:
:   LIBRARY

**Description:** Grants the clean room access to tables and views of all types, making them available to be linked into the clean room by
calling `consumer.link_datasets`. You can register broader groups of objects by calling `library.register_schema`,
`library.register_managed_access_schema`, or `consumer.register_db`. You must have MANAGE GRANTS privileges on the database to run this procedure.

**Arguments:**

- `object_names` - (Array) Array of fully qualified object names. These objects can then be linked into the clean room.

**Returns:** *(String)* Success message.

**Examples**

To register a table and a view:

Copy code

```
USE ROLE <ROLE_WITH_MANAGE_GRANTS>;
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

**Arguments:** *None*

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
USE ROLE ACCOUNTADMIN;
CALL samooha_by_snowflake_local_db.library.enable_external_tables_on_account();
```

### enable\_external\_tables\_for\_cleanroom

Schema:
:   CONSUMER

**Description:** Enable Iceberg or external tables to be linked into the specified clean room in this account by the consumer. To allow
Iceberg and external tables for all clean rooms in this account, call `enable_external_tables_on_account` instead.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - The name of the clean room into which the provider can link Iceberg tables or external tables.

**Returns:** *(String)* Success message. If successful, it triggers a security scan and also provides the number of the patch
that is generated if the security scan succeeds.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.provider.enable_external_tables_for_cleanroom(
  $cleanroom_name);
```

### unregister\_db

Schema:
:   LIBRARY

**Description:** Removes the database-level grants given to the SAMOOHA\_APP\_ROLE role and Snowflake Data Clean Room native application. Any
data in this database that is linked into a clean room will no longer be accessible in this account. You must have MANAGE GRANTS privileges
on the database to run this procedure.

**Arguments:**

- `db_name` - (String) Name of the database to unregister.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
USE ROLE <ROLE_WITH_MANAGE_GRANTS>;
CALL samooha_by_snowflake_local_db.library.unregister_db('SAMOOHA_SAMPLE_DATABASE');
```

### unregister\_schema

Schema:
:   LIBRARY

**Description:** Unregisters one or more schemas, which prevents users from linking their tables and views into the clean room.

If you want to unregister a managed access schema (that is, a schema created with the WITH MANAGED ACCESS parameter), use `library.unregister_managed_access_schema` instead. You must have MANAGE GRANTS privileges on the database to run this procedure.

**Arguments:**

- `schema_names` - (Array of strings) Fully qualified names of schemas to unregister.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
USE ROLE <ROLE_WITH_MANAGE_GRANTS>;
CALL samooha_by_snowflake_local_db.library.unregister_schema(
  ['SAMOOHA_SAMPLE_DATABASE.PUBLIC', 'MY_DB.MY_SCH']
);
```

### unregister\_managed\_access\_schema

Schema:
:   LIBRARY

**Description:** Unregisters one or more managed access schemas, which prevents users from linking their tables and views into the clean
room.

**Arguments:**

- `schema_names` - (Array of strings) Fully qualified names of schemas to unregister.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.library.unregister_managed_access_schema(
  ['SAMOOHA_SAMPLE_DATABASE.DEMO']
);
```

### unregister\_objects

Schema:
:   LIBRARY

**Description:** Revokes clean room access to tables and views of all types. Objects are no longer available to any users in any clean
rooms managed by this account.

**Arguments:**

- `object_names` - (Array) Array of fully qualified object names to revoke access to.

**Returns:** *(String)* Success message.

**Examples**

To unregister a table and a view:

Copy code

```
USE ROLE <ROLE_WITH_MANAGE_GRANTS>;
CALL samooha_by_snowflake_local_db.library.unregister_objects(
  ['SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS','MY_DB.MY_SCH.MY_VIEW']
);
```

## Link and unlink datasets

After a dataset is registered, you can link tables or views from that dataset into a specific clean room. You can
also unlink a table or view from a specific clean room to remove access to that data from the clean room.

### link\_datasets

Schema:
:   CONSUMER

**Description:** Link a table or view into the clean room, giving templates within that clean room access to the table,
according to any join and column policies that you specify.

If the dataset includes a Snowflake policy that is stored in a different database, you (or a clean rooms administrator)
must [grant your clean room access to that policy database](/user-guide/cleanrooms/register-data#label-dcr-link-views-with-external-policies) to be able to link the data
into a clean room.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room to link data into.
- `full_tables` - (Array of strings) List of fully qualified table or view names to expose to the clean room. These objects must first be
  registered (made available to the clean room environment) with the appropriate [registration method](#cleanroom-consumer-library-register-objects).

Note

If a table linked into a clean room is deleted, renamed, moved, or has restrictive permissions added, the table will no longer be usable in the clean
room unless you restore the old table with the same location, name, and permissions.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.link_datasets(
  $cleanroom_name,
  ['SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS', 'MY_DB.MY_SCH.EXPOSURES']
);
```

### unlink\_datasets

Schema:
:   CONSUMER

**Description:** Removes access to the specified tables or views in the specified clean room for all users. This works only for
data that you have linked into the clean room.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room for which access should be removed.
- `tables_list` - (Array of strings) List of fully qualified table or view names for which access should be blocked.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.unlink_datasets(
  $cleanroom_name,
  ['SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS', 'MYDB.MYSCH.EXPOSURES']);
```

### view\_consumer\_datasets

Schema:
:   CONSUMER

**Description:** View all tables and views linked into the specified clean room by any consumer.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room.

**Returns:** Table of objects linked into the specified clean room, along with the clean room’s internal view name for each object.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.view_consumer_datasets($cleanroom_name);
```

## Manage and view policies

[Manage policies](/user-guide/cleanrooms/v1/policies) on your data in a clean room that you have installed.

### set\_join\_policy

Schema:
:   CONSUMER

**Description:** Specifies which columns other users can join on when they run a template in the specified clean room.

Calling this function completely replaces the old policy with the new one.

Queries with wildcards might circumvent a join policy, so use discretion when you design your analysis template.

Learn more about clean room policies: [Understanding Snowflake Data Clean Room policies](/user-guide/cleanrooms/v1/policies).

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room where the join policy is applied.
- `table_col_names` - (String array) Fully qualified names of columns that can be joined, in the format `{database name}.{schema name}:{column name}`

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.set_join_policy(
  $cleanroom_name,
  ['SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:HASHED_EMAIL', 'MYDB.MYSCH.EXPOSURES:HASHED_EMAIL']
);
```

### view\_join\_policy

Schema:
:   CONSUMER

**Description:** Shows the column policy for your data in this clean room.

Learn more about clean room policies: [Understanding Snowflake Data Clean Room policies](/user-guide/cleanrooms/v1/policies).

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)*

**Returns:** *The join policy (table)*

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.view_join_policy($cleanroom_name);
```

### view\_provider\_join\_policy

Schema:
:   CONSUMER

**Description:** Shows which provider columns the consumer can join on in the specified clean room.

Learn more about clean room policies: [Understanding Snowflake Data Clean Room policies](/user-guide/cleanrooms/v1/policies).

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)*

**Returns:** *(Table)* The join policy.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.view_provider_join_policy($cleanroom_name);
```

### set\_column\_policy

Schema:
:   CONSUMER

**Description:** Specifies which columns of your data can be projected in templates run by other collaborators.

Calling this function completely replaces the old policy with the new one.

Don’t set a column policy on identity columns or sensitive columns like email because you generally don’t want this sort of data to be projected.

Queries with wildcards might not be caught by using these checks, so use discretion when you design the analysis template.

Learn more about clean room policies: [Understanding Snowflake Data Clean Room policies](/user-guide/cleanrooms/v1/policies).

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room where the column policy is applied.
- `analysis_table_cols` - (String array) Fully qualified names of columns that can be projected, in the format `{database name}.{schema name}:{column name}`

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.set_column_policy(
  $cleanroom_name,
  ['prod_overlap_analysis:SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:STATUS',
   'prod_overlap_analysis:SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:AGE_BAND',
   'prod_overlap_analysis:SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:DAYS_ACTIVE'
  ]
);
```

### view\_column\_policy

Schema:
:   CONSUMER

**Description:** Shows your column policy in the specified clean room. To see the provider’s column policy, call
`consumer.view_provider_column_policy`.

Learn more about clean room policies: [Understanding Snowflake Data Clean Room policies](/user-guide/cleanrooms/v1/policies).

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room to describe.

**Returns:** *(Table)* Information about all consumer column policies in the clean room.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.view_column_policy($cleanroom_name);
```

### view\_provider\_column\_policy

Schema:
:   CONSUMER

**Description:** Shows the provider’s column policy.

Learn more about clean room policies: [Understanding Snowflake Data Clean Room policies](/user-guide/cleanrooms/v1/policies).

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)*

**Returns:** *The column policy (table)*

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.view_provider_column_policy($cleanroom_name);
```

## Templates

The following procedures allow users to work with templates in the clean room.

### view\_template\_definition

Schema:
:   CONSUMER

**Description:** View the raw JinjaSQL of the specified template. If a template [was obscured](#dcr-provider-add-custom-sql-template) by applying the `is_obfuscated` argument, you can’t see the template source code.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room that holds the template.
- `template_name` - (String) Name of the template to view.

**Returns:** *(String)* The template definition.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.view_template_definition(
  $cleanroom_name,
  'prod_overlap_analysis');
```

### get\_arguments\_from\_template

Schema:
:   CONSUMER

**Description:** Get a list of arguments used by the template. You can pass values for these argument into the template when you call
`consumer.run_analysis`.

**Arguments:**

> - [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room that has the template.
> - `template_name` - (String) Name of the template to return arguments for.

**Returns:** *(Table)* Argument list and specification.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.get_arguments_from_template(
  $cleanroom_name,
  'prod_overlap_analysis');
```

## Template chains

The following procedures allow users to work with [template chains](/user-guide/cleanrooms/developer-template-chains) in the clean room.

### view\_added\_template\_chains

Schema:
:   CONSUMER

**Description:** List all template chains defined in a given clean room.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room to list template chains for.

**Returns:** *(Table)* Information about any template chains in the specified clean room.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.view_added_template_chains(
  $cleanroom_name);
```

### view\_template\_chain\_definition

Schema:
:   CONSUMER

**Description:** Returns the attributes of a specified template chain.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room with the template chain to describe.
- `template_chain_name` - (String) Name of the template chain to describe.

**Returns:** *(String)* The definition of the specified template chain.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.view_template_chain_definition(
  $cleanroom_name,
  'insights_chain');
```

## Consumer-run analyses

The following procedure runs an analysis or activation based on the specified template.

### run\_analysis

Schema:
:   CONSUMER

**Description:** Runs an analysis by using a template or template chain and returns the results table.

Important

- If [differential privacy](/user-guide/cleanrooms/differential-privacy) is enabled, the query can fail if you have reached your
  budget limit for this template.
- If a template [was obscured](#dcr-provider-add-custom-sql-template) by applying the `is_obfuscated` argument, you must use
  Snowflake Enterprise Edition or higher to be able to run the template.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room in which to run the analysis.
- `template_name` - (String) Name of the template or template chain to run in the clean room. This template must have been added to the
  clean room by the provider or consumer.
- `consumer_tables` - (Array of strings) Array of fully qualified consumer table names. These are assigned to the `my_table` template
  variable.
  These tables must already be linked into the clean room. See available tables by calling `consumer.view_consumer_datasets`.
- `provider_tables` - (Array of strings) Array of fully qualified provider table names. These are assigned to the `source_table`
  template variable. These tables must have been linked into the clean room. See available tables by calling
  `consumer.view_provider_datasets`.
- `analysis_arguments` - (Object) An object with key-value pairs passed to the template. The template can access
  the variable by key name. If you pass in `{'age': 20}`, the template accesses the value as `{{age}}`. Pass in an empty object if no
  values are required. To see which values are required, examine the template in question by calling `consumer.view_template_definition`.
  Examine the template to determine whether you need to fully qualify any column names used. If the table is aliased as `p` or `c` in
  the template, use *lowercase* `p` and `c` table aliases for column names.

  This object has one optional reserved value:

  - `epsilon` *(Float, optional)* - Specifies the
    [epsilon value for differential privacy](https://www.google.com/search?q=differential+privacy+epsilon&oq=differential+privacy+epsilon),
    if differential privacy is enabled for this clean room. Default is 0.1.
- `use_cache` - (Boolean, optional) Whether or not to use cached results for the same query. Default is FALSE.

**Returns:** *(Table)* Query results.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.run_analysis(
  $cleanroom_name,
  'prod_overlap_analysis',
  ['DB1.MYDATA.CONVERSIONS'],  -- Consumer tables
  ['MYDB.MYSCH.EXPOSURES'],    -- Provider tables
  object_construct(
    'max_age', 30
  )
);
```

## Activation

The following procedures manage [activation](/user-guide/cleanrooms/v1/activation), or the saving of results to a consumer’s or
provider’s Snowflake account. You can’t activate data to third-party accounts by using the API.

### view\_activation\_policy

Schema:
:   CONSUMER

**Description:** Shows the consumer’s activation policy in the specified clean room.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - The name of the clean room to report on.

**Returns:** *(Table)* The consumer’s activation policy in the specified clean room.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.view_activation_policy($cleanroom_name);
```

### view\_external\_activation\_history

Schema:
:   LIBRARY

**Description:** View the history of activation requests in the current account.

**Arguments:** *None*

**Returns:** A table with the details and status of activation requests.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.library.view_external_activation_history();
```

### set\_activation\_policy

Schema:
:   CONSUMER

**Description:** Indicates which columns should be allowed to be activated.

Your activation policies are enforced only on queries by other users; your activation policies are not enforced in your own queries.

Calling this function completely replaces the old policy with the new one.

Learn more about clean room policies: [Understanding Snowflake Data Clean Room policies](/user-guide/cleanrooms/v1/policies).

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room in which to set the activation policy.
- `columns` - (Array) Name of columns of your own data that can be activated, in the format `{template name}:{database name}.{schema name}.{table name}:column_name`.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.set_activation_policy(
  $cleanroom_name,
  [
    'prod_overlap_analysis:SAMOOHA_SAMPLE_DATABASE_NAME.DEMO.CUSTOMERS:HASHED_EMAIL',
    'prod_overlap_analysis:SAMOOHA_SAMPLE_DATABASE_NAME.DEMO.CUSTOMERS:REGION_CODE' ]);
```

### approve\_provider\_activation\_consent

Schema:
:   CONSUMER

**Description:** Approves a provider’s request to allow provider activation, which is the ability to push results to the provider’s
Snowflake account.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room where the provider is requesting to run a template.
- `activation_template_name` - (String) Name of the activation template that the provider wants to run.

**Returns:** *(String)* Success message. This procedure fails if the provider has not called `provider.request_provider_activation_consent`
in this clean room with the specified template.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.approve_provider_activation_consent(
  $cleanroom_name,
  'activation_my_template');
```

### run\_activation

Schema:
:   CONSUMER

**Description:** Runs a template that pushes results back to the consumer’s or provider’s Snowflake account. The
`consumer_direct_activation` argument determines whether this is a consumer or provider activation.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room in which to run the activation.
- `segment_name` - (String) Arbitrary string used to label rows that are generated by this activation run. Each activation run adds new rows to an
  existing results table. Provide a unique string in this field each time you call this procedure to be able to filter results to a
  specific run.
- `template_name` - (String) Name of the activation template to call.
- `consumer_tables` - (Array of strings) Array of fully qualified consumer table names to pass to the template.
- `provider_tables` - (Array of strings) Array of fully qualified provider table names to pass to the template.
- `activation_arguments` - (Object) Key-value set of arguments to pass to the template.
- `consumer_direct_activation` - (Boolean, optional) TRUE to push results back to the consumer account, FALSE to send results to the
  provider. Default is FALSE.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
-- Run a consumer activation, as specified by the final TRUE argument.
SET segment_name = 'my_activation_segment';
CALL samooha_by_snowflake_local_db.consumer.run_activation(
  $cleanroom_name,
  $segment_name,
  $template_name,
  ['SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS'],
  ['SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS'],
  object_construct(
    'c_join_col', 'c.hashed_email',
    'p_join_col', 'p.hashed_email'
  ),
  TRUE);
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

## Consumer-defined templates

The following APIs allow you to add consumer-defined templates to a clean room. For more information, see [consumer-written templates](/user-guide/cleanrooms/demo-flows/custom-templates#label-dcr-consumer-written-templates).

### create\_template\_request

Schema:
:   CONSUMER

**Description**: Sends a request to the provider of a clean room, asking them to approve a custom template so it can be added to the clean
room. See [Consumer-written custom templates](/user-guide/cleanrooms/demo-flows/custom-templates#label-dcr-consumer-written-templates).

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room where the template is added.
- `template_name` - (String) Name of the template to add. Must be all lowercase letters, numbers, spaces, or underscores. Activation
  template names must start with “activation”.
- `template_definition` - (String) The JinjaSQL template. [Learn the template syntax.](/user-guide/cleanrooms/custom-templates)

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.create_template_request(
  $cleanroom_name,
  $template_name,
  $$
  SELECT
      identifier({{ dimensions[0] | column_policy }})
  FROM
      identifier({{ my_table[0] }}) c
    INNER JOIN
      identifier({{ source_table[0] }}) p
        ON
          c.identifier({{ consumer_id  }}) = p.identifier({{ provider_id | join_policy }})
        {% if where_clause %} where {{ where_clause | sqlsafe | join_and_column_policy }} {% endif %};
  $$);
```

### get\_sql\_jinja

Schema:
:   CONSUMER

**Description:** Evaluates a JinjaSQL template to a SQL statement. This procedure is used when developing custom templates, to see how the
template is rendered after processing with a given set of parameters.

This procedure can process only standard [JinjaSQL](https://github.com/sripathikrishnan/jinjasql) statements; it can’t process clean room
extensions to JinjaSQL such as `join_policy` or `column_policy`.

**Arguments:**

- `template_string` - (String) The JinjaSQL code to process. Only standard JinjaSQL is supported.
- `arguments` - (Object) An object where field names correspond to variables that are used in the template.

**Returns:** *(String)* The SQL statement generated by the submitted template with the provided variable values.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.get_sql_jinja(
$$
SELECT COUNT(*), IDENTIFIER({{ group_by_col }})
  FROM IDENTIFIER({{ my_table | sqlsafe }})
  INNER JOIN IDENTIFIER({{ source_table | sqlsafe }})
  ON IDENTIFIER({{ consumer_join_col }}) = IDENTIFIER({{ provider_join_col }})
  GROUP BY IDENTIFIER({{ group_by_col }});
$$,
object_construct(
'group_by_col', 'city',
'consumer_join_col', 'hashed_email',
'provider_join_col', 'hashed_email',
'my_table', 'mydb.mysch.t1',
'source_table', 'mydb.mysch.t2'));
```

**Response:**

Copy code

```
SELECT COUNT(*), IDENTIFIER('city')
  FROM IDENTIFIER(mydb.mysch.t1)
  INNER JOIN IDENTIFIER(mydb.mysch.t2)
  ON IDENTIFIER('hashed_email') = IDENTIFIER('hashed_email')
  GROUP BY IDENTIFIER('city');
```

### generate\_python\_request\_template

Schema:
:   CONSUMER

**Description:** Generates a consumer clean room template that includes custom Python code. The generated template includes your Python code
and a placeholder for your JinjaSQL template. Pass your final template to `consumer.create_template_request`.

For more information about consumer-defined templates, see [Consumer-written custom templates](/user-guide/cleanrooms/demo-flows/custom-templates#label-dcr-consumer-written-templates).

**Arguments:**

- `function_name` - (String) The function name that is used by a template to call your function.
- `arguments` - (Array of String pairs) An array of arguments required by function `function_name`. Each element is a space-delimited pair
  that gives the argument name and its Snowflake SQL data type. For example: `['size INT', 'start_date DATE']`.
- `packages` - (Array of strings) Array of package names required for your Python code. If none, specify an empty array.
  [See the full list of supported packages.](https://repo.anaconda.com/pkgs/snowflake/) Example: `['pandas','numpy']`.
- `imports` - Not supported: Do not use
- `rettype` - (String) The Snowflake SQL return type of your function. Examples: INTEGER, VARCHAR.
- `handler` - (String) The name of the main handler function in your Python code. Typically this is `'main'`.
- `code` - (String) Your Python code implementation. If you include an import and your designated handler is defined in an import, this
  can be an empty string.

**Returns:** *(String)* Returns your Python UDF with a placeholder for your JinjaSQL template. You must escape any nested *$$* or
single-quote marks *‘* correctly before passing your template string into `consumer.create_template_request`. Read
[Consumer-submitted code](/user-guide/cleanrooms/demo-flows/custom-code#label-dcr-consumer-submitted-code).

**Example:**

Call the helper function with a trivial Python example:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.CONSUMER.GENERATE_PYTHON_REQUEST_TEMPLATE(
  'my_func',                         -- SQL should use this name to call your function.
  ['data VARIANT', 'index INTEGER'], -- Arguments and types for the function.
  ['pandas', 'numpy'],               -- Standard libraries used.
  [],                                -- Reserved.
  'INTEGER',                         -- SQL return type.
  'main',                            -- Standard main handler.
  $$
  import pandas as pd
  import numpy as np

  def main(data, index):
      df = pd.DataFrame(data)  # you can do something with df but this is just an example
      return np.random.randint(1, 100)
      $$
  );
```

The following example shows the generated code. Replace `<INSERT SQL TEMPLATE HERE>` with your template JinjaSQL code.

```
BEGIN

-- First define the Python UDF
CREATE OR REPLACE FUNCTION CLEANROOM.my_func(data VARIANT, index INTEGER)
RETURNS INTEGER
LANGUAGE PYTHON
RUNTIME_VERSION = 3.10
PACKAGES = ('pandas', 'numpy')

HANDLER = 'main'
AS $$
import pandas as pd
import numpy as np

def main(data, index):
    df = pd.DataFrame(data)  # you can do something with df but this is just an example
    return np.random.randint(1, 100)
    $$;

-- Then define and run the SQL query
LET SQL_TEXT varchar := $$<INSERT SQL TEMPLATE HERE>$$;

-- Run the query and return the result
LET RES resultset := (EXECUTE IMMEDIATE :SQL_TEXT);
RETURN TABLE(RES);

END;
```

### list\_template\_requests

Schema:
:   CONSUMER

**Description:** Shows all requests that the consumer has made to add a template to a clean room.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - The clean room to list template requests for.

**Returns:** A table with the following columns:

- `request_id` - ID of the request, generated by the clean rooms system.
- `provider_identifier` - Provider’s account locator.
- `template_name` - Template name that the consumer provided in the request.
- `template_definition` - Source code of the template that the consumer asked to add to the clean room.
- `request_status` - Status of the request: PENDING, APPROVED, or REJECTED.
- `reason` - If the request status is REJECTED, the provider should give a reason for the rejection here.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.list_template_requests($cleanroom_name);
```

## Clean room metadata getter methods

The following methods show relevant properties of the clean room:

### describe\_cleanroom

Schema:
:   CONSUMER

**Description:** Provides a summary of key information about the specified clean room, including templates, datasets, and policies.
If a template [was obscured](#dcr-provider-add-custom-sql-template) by applying the `is_obfuscated` argument, you must use Snowflake
Enterprise Edition or higher to be able to see the template name.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room to describe.

**Returns:** *(String)* Description of the clean room.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.describe_cleanroom($cleanroom_name);
```

### view\_provider\_datasets

Schema:
:   CONSUMER

**Description:** Lists all datasets that the provider added to the clean room.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room.

**Returns:** *(Table)* A table of datasets added by the provider. Use the table name returned here in your queries.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.view_provider_datasets($cleanroom_name);
```

### view\_added\_templates

Schema:
:   CONSUMER

**Description:** Lists all templates in the clean room. If a template [was obscured](#dcr-provider-add-custom-sql-template) by
applying the `is_obfuscated` argument, you must use Snowflake Enterprise Edition or higher to be able to view the template.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room.

**Returns:** A list of templates in this clean room, and the source code for each (unless the template was obscured by the provider).

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.view_added_templates($cleanroom_name);
```

### is\_consumer\_run\_enabled

Schema:
:   LIBRARY

**Description:** Checks whether consumer-run analysis is enabled for the specified clean room. This is enabled by default, but a clean room
provider can disable it.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room.

**Returns:** *(String)* Whether or not the clean room allows consumer-run analyses.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.library.is_consumer_run_enabled($cleanroom_name);
```

### view\_cleanrooms

Schema:
:   CONSUMER

**Description:** Lists all clean rooms that are joined (installed) or that are joinable by this account. To see only installed clean rooms,
run `consumer.view_installed_cleanrooms`. To see clean rooms created by this account, call `provider.view_cleanrooms`.

**Arguments:** *None*

**Returns:** *(Table)* All installed or invited clean rooms for this account.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.view_cleanrooms();
```

### view\_installed\_cleanrooms

Schema:
:   CONSUMER

**Description:** Lists all clean rooms that are installed (joined) in this account. To see both joined and unjoined clean rooms, call
`consumer.view_cleanrooms`. To see all clean rooms created by this account, call `provider.view_cleanrooms`.

**Arguments:** *None*

**Returns:** (*Table*) The clean rooms installed in this account.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.view_installed_cleanrooms();
```

## Differential privacy

These procedures control [differential privacy](/user-guide/cleanrooms/differential-privacy) in the clean room. You can also specify differential privacy at the template level when you call `consumer.enable_templates_for_provider_run`.

### is\_dp\_enabled

Schema:
:   CONSUMER

**Description:** Checks whether differential privacy is enabled in the clean room. The clean room must be installed to check this value.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)*

**Returns:** *(Boolean)* Whether or not the clean room has differential privacy enabled.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.is_dp_enabled($cleanroom_name);
```

### view\_remaining\_privacy\_budget

Schema:
:   CONSUMER

**Description:** Views the privacy budget remaining that can be used to make queries from the clean room. After the budget is exhausted, further calls to `run_analysis` aren’t allowed until the budget is reset. The budget resets daily.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* Name of the clean room. The clean room must be installed for this
  procedure to succeed.

**Returns:** *(Float)* The remaining privacy budget.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.view_remaining_privacy_budget($cleanroom_name);
```

### set\_privacy\_settings

Schema:
:   CONSUMER

**Description:** Sets privacy settings for provider-run analyses (including activation) that use custom templates. This procedure
overwrites all previously set values. Each time you call this method it erases all previous configuration settings.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room where these settings should be applied.
- `privacy_settings` - (String) A string JSON object that specifies privacy settings when custom templates are run by a provider. Here is
  the syntax of the object:

  Copy code

  ```
  '{
    "null" : <template_config>
  }'
  ```

  `template_config` is an object with differential privacy and aggregation settings. See
  :   [Available privacy settings](/user-guide/cleanrooms/differential-privacy#label-dcr-available-privacy-settings) to see what fields you can provide in this object.

**Example:**

Copy code

```
-- Apply differential privacy for provider-run analysis using all custom templates.
CALL samooha_by_snowflake_local_db.consumer.set_privacy_settings(
  $cleanroom_name,
  PARSE_JSON('{
    "null":{ "differential": 1, "epsilon": 0.1, "privacy_budget": 3 }
    }')
  );
```

**Returns:** *(String)* Success message.

## Snowpark Container Services procedures

[Read more about using Snowpark Container Services in your clean rooms.](/user-guide/cleanrooms/demo-flows/machine-learning)

### start\_or\_update\_service

Schema:
:   CONSUMER

**Description:** Creates and starts the latest version of Snowpark Container Services that is defined by the provider in this clean room.
Any time the provider calls `provider.load_service_into_cleanroom` to create or update a container, the consumer must call
`consumer.start_or_update_service` to update the service.

The consumer must define and start the pool before calling this procedure.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room where the container should be loaded.
- `compute_pool_name` - (String) The name of a compute pool that is defined by the consumer in this clean room. The pool must already be created, and
  the clean room must have privileges to access to the pool.
- `service_options` - (Object, optional) An object specifying parameters for this service. The following properties are supported:
  - `query_warehouse` - (*String, optional*) Name of the warehouse to use for this service. Doesn’t need to be the same warehouse as the one
    running the clean room.
  - `min_instances` - (*Integer, optional*) Minimum number of instances to use for this service.
  - `max_instances` - (*Integer, optional*) Maximum number of instances to use for this service.

**Returns:** (*Table*) Results of the load, if successful. Throws an error if not successful.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.start_or_update_service(
  $cleanroom_name,
  'dcr_lal_pool',
  object_construct(
        'query_warehouse', 'app_wh',
        'min_instances', '1',
        'max_instances', '1'
));
```

## Environment management

Use the following methods to assist in general clean room functionality.

### set\_cleanroom\_ui\_accessibility

Schema:
:   CONSUMER

**Description:** Shows or hides clean rooms in the clean rooms UI for consumers in the current account.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - The name of the clean room.
- `visibility_status` - (String) One of the following case-sensitive values:
  - HIDDEN - Hides the specified clean room in the clean rooms UI from all users in the current consumer account. The clean room will
    still be accessible using API calls.
  - EDITABLE - Makes the clean room visible in the clean rooms UI.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.set_cleanroom_ui_accessibility(
  $cleanroom_name,
  'HIDDEN');
```

### manage\_datastats\_task\_on\_account

Schema:
:   CONSUMER

**Description:** Enables or disables the background task that computes clean room statistics. The task is running by default, but you can
disable it to reduce your costs.

Important

To manage this task, all collaborators must call the appropriate `provider` or `consumer` version of this
procedure with the same value.

**Arguments:**

- `enable` - (Boolean) TRUE to enable the task, FALSE to disable the task.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
-- Disable the task in this account.
CALL samooha_by_snowflake_local_db.consumer.manage_datastats_task_on_account(FALSE);
```

### enable\_local\_db\_auto\_upgrades

Schema:
:   LIBRARY

**Description:** Enables the task that automatically upgrades the Snowflake Data Clean Rooms environment when new procedures or
functionality is released (The task is `samooha_by_snowflake_local_db.admin.expected_version_task`.) Call this procedure to automate
upgrades, rather than calling `library.apply_patch` with each new release.

Although you might reduce cost by disabling this task, we recommend that you leave it running to ensure that you have the latest version of
the clean rooms environment on your system.

**Arguments:** *None*

**Returns:** *(String)* Success or failure message.

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

**Returns:** *(String)* Success or failure message.

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
[Recent feature updates](/release-notes/new-features#label-new-features-features).) This procedure updates
[SAMOOHA\_BY\_SNOWFLAKE\_LOCAL\_DB](/user-guide/cleanrooms/v1/installation-details).

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
:   CONSUMER

**Description:** Updates the specified clean room to the latest version, enabling new features and fixes for that clean room. Typically you
call this only when Snowflake Support tells you to call it.

The provider should call `library.patch_cleanroom` before the consumer calls `library.patch_cleanroom`; otherwise, there is no patch to
apply.

**Arguments:**

- [cleanroom\_name](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-about-clean-room-names) *(String)* - Name of the clean room to patch.

**Returns:** *(String)* Success message.

**Example:**

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.patch_cleanroom($cleanroom_name);
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
