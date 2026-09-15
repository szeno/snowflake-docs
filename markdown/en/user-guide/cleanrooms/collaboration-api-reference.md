# Snowflake Data Clean Rooms Collaboration API

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

## Introduction

This is the reference page for the Snowflake Data Clean Rooms Collaboration API. This API uses the COLLABORATION and REGISTRY
schemas.

Note

You should disable secondary roles in your environment when using the Collaboration API:

Copy code

```
USE SECONDARY ROLES NONE;
```

To learn how to set up your development environment, see [Setting up your environment](/user-guide/cleanrooms/developer-guide#label-cleanrooms-developer-setup).

To learn how to manage access to the Collaboration API procedures, see [Use DCR privileges to manage account, object, and procedure privileges](/user-guide/cleanrooms/manage-access#label-dcr-collab-about-rbac-roles).

### Metadata cheat sheet

Here is how to find some commonly sought information about a collaboration:

| To learn this… | Call this |
| --- | --- |
| What collaborations can I join? | VIEW\_COLLABORATIONS - Look for collaborations where the `collaboration_name` column is NULL. |
| Which collaborations have I joined? | VIEW\_COLLABORATIONS - Look for collaborations where the `collaboration_name` column is not NULL, which can mean either that you have created or joined the collaboration. |
| Which collaborations do I own? | VIEW\_COLLABORATIONS - Look in the `owner_account` column. |
| What is the status of all collaborators in a collaboration? | GET\_STATUS |
| What is my join or creation status in a collaboration? | GET\_STATUS or VIEW\_COLLABORATIONS |
| Who owns a given collaboration? | GET\_STATUS - Look for OWNER in the `roles` column. |
| What is my collaboration role in a given collaboration? | GET\_STATUS - Look in the `roles` column. |
| What collaboration roles are assigned in a given collaboration? | GET\_STATUS - Look in the `roles` column. |
| What is the spec in a given collaboration? | VIEW\_COLLABORATIONS - Look in the `collaboration_spec` column. |
| How do I edit an existing collaboration? | The collaboration owner can call [EDIT](#label-dcr-collaboration-edit-reference) to add or remove collaborators, change collaborator roles, or re-share resources that are already registered or linked in the collaboration. All collaborators (including the owner) can share new resources into the collaboration by calling [LINK\_DATA\_OFFERING](#label-dcr-collaboration-link-data-offering-reference) (data offerings) or [ADD\_TEMPLATE\_REQUEST](#label-dcr-collaboration-add-template-request-reference) (templates). |
| Is the spec up to date? | There is no way to tell if a given spec has changes in progress, but you can call VIEW\_COLLABORATIONS to see when the latest updates were applied. |
| What pending update requests do I have? | `VIEW_UPDATE_REQUESTS`. Look for rows where STATUS = PENDING\_MY\_APPROVAL. |
| Show me the spec for a given collaboration | REVIEW returns the collaboration spec. If you have already called REVIEW or joined the collaboration, call the following SQL command with your collaboration name as indicated:  Copy code  ``` CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.   VIEW_COLLABORATIONS() ->>     SELECT "COLLABORATION_SPEC" FROM $1       WHERE "SOURCE_NAME" = <collaboration name>; ``` |

Expand

Show lessSee more

## Template procedures

### REGISTER\_TEMPLATE

Schema:
:   REGISTRY

Registers a template to enable it to be used in a collaboration. Every template registered must have a unique
name-version combination for all templates in all registries in your account. To remove a template that you registered, call [REGISTRY.UNREGISTER\_TEMPLATE](#label-dcr-collaboration-unregister-template-reference).

#### Syntax

Copy code

```
REGISTER_TEMPLATE( ['<registry_name>' ,] <template_spec> )
```

#### Arguments

`registry_name` *(Optional)*
:   Name of a [custom registry](/user-guide/cleanrooms/registries) in which to register this template. If not specified, registers the template in the default account registry.

`template_spec`
:   [Template definition](/user-guide/cleanrooms/spec-template#label-dcr-collaboration-template-yaml) in YAML format, as a string.

#### Returns

A template ID to use in the collaboration specification.

#### Examples

Register a template in the default registry:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.REGISTER_TEMPLATE(
  $$
  api_version: 2.0.0
  spec_type: template
  name: my_test_template
  version: 2026_01_12_V1
  type: sql_analysis
  description: A test template
  template:
    SELECT * FROM IDENTIFIER({{ source_table[0] }}) LIMIT 10;
$$);
```

Register a template in a custom registry:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.REGISTER_TEMPLATE(
  'my_custom_registry',
  $$
  api_version: 2.0.0
  spec_type: template
  name: my_test_template
  version: 2026_01_12_V1
  type: sql_analysis
  description: A test template
  template:
    SELECT * FROM IDENTIFIER({{ source_table[0] }}) LIMIT 10;
$$);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling the following procedures.

To register objects in the default registry:

- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('REGISTER TEMPLATE', '{role name}')`

To register items in a custom registry:

- You have read and write privileges on any custom registry that you created yourself.
- To access a custom registry created by another user, you need `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('REGISTER', 'REGISTRY', 'MY_REGISTRY', '{role name}')`.

---

### VIEW\_REGISTERED\_TEMPLATES

Schema:
:   REGISTRY

Lists all templates that you have registered. To register a template, call REGISTRY.REGISTER\_TEMPLATE.

#### Syntax

Copy code

```
VIEW_REGISTERED_TEMPLATES()
VIEW_REGISTERED_TEMPLATES( [ '<registry_name>' ] )
```

#### Arguments

`registry_name` *(Optional)*
:   An ARRAY of registry names to scope the read. Use `'default'` (case-insensitive) to include the built-in registry alongside custom ones. Inaccessible or non-existent registries in the array are silently skipped. If not specified, lists templates from all registries you have access to.

    Example: `['default', 'my_registry', 'other_reg']`

#### Returns

A table that lists the details of all templates that you have registered in this account. The table includes the following columns:

- `TEMPLATE_ID`: ID of the template.
- `NAME`: Template name.
- `VERSION`: Template version.
- `TEMPLATE_SPEC`: Full YAML specification of the template.
- `REGISTRY`: Registry the template is registered in.
- `CREATED_ON`: Timestamp when the template was created.

#### Examples

List templates from all registries:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.VIEW_REGISTERED_TEMPLATES();
```

List templates from the default registry only:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.VIEW_REGISTERED_TEMPLATES(['default']);
```

List templates from specific registries:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.VIEW_REGISTERED_TEMPLATES(
  ['default', 'my_custom_registry']
);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling one of the following procedures.

To see items in the default registry:

- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('VIEW REGISTERED TEMPLATES', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`

To see items in a custom registry:

- You have read and write privileges on any custom registry that you created yourself.
- To access a custom registry created by another user, you need `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('READ', 'REGISTRY', 'MY_REGISTRY', '{role name}')`.

---

### UNREGISTER\_TEMPLATE

Schema:
:   REGISTRY

Unregisters a template that you previously registered, removing it from the registry. To find the ID of a template that you registered, call [REGISTRY.VIEW\_REGISTERED\_TEMPLATES](#label-dcr-collaboration-view-registered-templates-reference).

You can’t unregister a template that is currently used in a collaboration. If the template is linked to one or more collaborations, the procedure fails and returns an error that lists those collaborations; remove the template from each of them before you unregister it.

#### Syntax

Copy code

```
UNREGISTER_TEMPLATE( '<template_id>' )
```

#### Arguments

`template_id`
:   The ID of the template to unregister, as returned by [REGISTRY.REGISTER\_TEMPLATE](#label-dcr-collaboration-register-template-reference) or [REGISTRY.VIEW\_REGISTERED\_TEMPLATES](#label-dcr-collaboration-view-registered-templates-reference). A template ID has the form `{name}_{version}`.

#### Returns

A table with a status message confirming that the template was unregistered.

#### Example

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.UNREGISTER_TEMPLATE('my_test_template_2026_01_12_V1');
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling the following procedures.

To unregister a template in the default registry:

- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('REGISTER TEMPLATE', '{role name}')`

To unregister items in a custom registry:

- You have read and write privileges on any custom registry that you created yourself.
- To access a custom registry created by another user, you need `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('REGISTER', 'REGISTRY', 'MY_REGISTRY', '{role name}')`.

---

### ADD\_TEMPLATE\_REQUEST

Schema:
:   COLLABORATION

Sends a request to link a template to an existing collaboration. If the sender is affected by the request, the sender automatically approves the request; all other affected collaborators must approve the request for the change to be applied. All collaborators need to call this procedure to link a template to an existing collaboration, even the collaboration owner.

To add additional template sharers, you can call this procedure again with their aliases. Each call adds the users listed in `share_with` to the existing list of sharers.

To see the status of the request, call VIEW\_UPDATE\_REQUESTS.

[See the link template flow.](/user-guide/cleanrooms/resources-templates#label-dcr-collaboration-add-template-post-creation)

#### Syntax

Copy code

```
ADD_TEMPLATE_REQUEST( <collaboration_name>, <template_id>, <share_with> )
```

#### Arguments

`collaboration_name`
:   Name of the collaboration to link the template to.

`template_id`
:   ID of the template to link to the collaboration. Register the template to get this value.

`share_with`
:   Array of *aliases* of analysis runners to share this template with. Collaborators listed here will be added in addition to any other collaborators associated with this template. All collaborators listed here must be analysis runners or the procedure will fail without sharing this template with anyone.

#### Returns

A string success message.

#### Example

Copy code

```
-- Ask to link the template only for Collaborator3 in this collaboration.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.ADD_TEMPLATE_REQUEST(
  $collaboration_name,
  $template_alias,
  ['Collaborator3']
);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling the following procedures:

- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('UPDATE', 'COLLABORATION', '{collaboration name}', '{role name}')`
- Either of the following privileges:

  - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges that must be manually granted to the role.
  - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges that must be manually granted to the role.
- If the template is in a custom registry, you must also have `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE( 'READ', '{registry name}', '{role name}')`

---

### REMOVE\_TEMPLATE

Schema:
:   COLLABORATION

Asynchronous request to remove a template from a given collaboration for specified collaborators. Only the collaborator that registered the
template can remove a template. No approval is needed from anyone else to remove a template that you have registered. When a template is
removed for a collaborator, that collaborator can’t see or use the template.

#### Syntax

Copy code

```
REMOVE_TEMPLATE( <collaboration_name>, <template_id>, <remove_for> )
```

#### Arguments

`collaboration_name`
:   Name of the collaboration to remove the template from.

`template_id`
:   ID of the template to remove from the collaboration.

`remove_for`
:   Array of one or more *aliases* of analysis runners in this collaboration that should no longer be able to see or use this template.

#### Returns

A string success message. To see if a template has been removed for a collaborator, view the collaboration specification.

#### Example

Copy code

```
-- Prevent collaborator_1234 from using the specified template
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.REMOVE_TEMPLATE(
  $collaboration_name,
  $template_id,
  ['collaborator_1234']
);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling the following procedures:

- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('UPDATE', 'COLLABORATION', '{collaboration name}', '{role name}')`
- Either of the following privileges:

  - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges that must be manually granted to the role.
  - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges that must be manually granted to the role.
- If the template is in a custom registry, or references a code spec in a custom registry, you must also have `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE( 'READ', '{registry name}', '{role name}')`

---

### VIEW\_TEMPLATES

Schema:
:   COLLABORATION

Shows all templates that you can run, or that you have submitted, to the specified collaboration.

#### Syntax

Copy code

```
VIEW_TEMPLATES( <collaboration_name> )
```

#### Arguments

`collaboration_name`
:   Name of the collaboration. You must review or join this collaboration before you can list its templates.

#### Returns

A table that lists information about templates that you can run in this collaboration, including templates that you have registered. The
table includes the following columns:

- `template_id`: The template ID. Pass this into the `template` field or `template_id` parameter of your RUN command.
- `template_spec`: The [template specification](/user-guide/cleanrooms/resources-templates#label-dcr-collaboration-add-templates-to-collaboration) for this template, which
  includes the full [JinjaSQL](/user-guide/cleanrooms/custom-templates) for this template.
- `parameters`: A description of all the arguments accepted by this template, in JSON format. The information about each parameter
  includes the name, default value, template-provider-written description, and whether it is required. Pass values for these parameters
  into your RUN command.
- `shared_by`: The collaborator that registered this template.
- `shared_with`: The collaborators that this template is shared with.

#### Example

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.VIEW_TEMPLATES(
  $collaboration_name
);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling one of the following procedures:

- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('VIEW TEMPLATES', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('READ', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`

---

### ENABLE\_TEMPLATE\_AUTO\_APPROVAL

Deprecated Feature

This procedure is deprecated. Use [SET\_CONFIGURATION](#label-dcr-collaboration-set-configuration-reference) with `TEMPLATE_AUTO_APPROVAL` set to `true` instead.

Schema:
:   COLLABORATION

Causes all template update requests sent by other collaborators to be approved automatically. Requests will still appear in the request log.
This affects only requests sent after auto-approval was enabled.

#### Syntax

Copy code

```
ENABLE_TEMPLATE_AUTO_APPROVAL( <collaboration_name> )
```

#### Arguments

`collaboration_name`
:   Name of the collaboration.

#### Returns

A string success message.

#### Example

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.ENABLE_TEMPLATE_AUTO_APPROVAL(
  $collaboration_name
);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling one of the following procedures:

- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('MANAGE TEMPLATE AUTO APPROVAL', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('UPDATE', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`

---

### DISABLE\_TEMPLATE\_AUTO\_APPROVAL

Deprecated Feature

This procedure is deprecated. Use [SET\_CONFIGURATION](#label-dcr-collaboration-set-configuration-reference) with `TEMPLATE_AUTO_APPROVAL` set to `false` instead.

Schema:
:   COLLABORATION

Disables automatic approval for template requests raised by other collaborators. All future requests must be approved manually by calling APPROVE\_UPDATE\_REQUEST.

#### Syntax

Copy code

```
DISABLE_TEMPLATE_AUTO_APPROVAL( <collaboration_name> )
```

#### Arguments

`collaboration_name`
:   Name of the collaboration.

#### Returns

A string success message.

#### Example

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.DISABLE_TEMPLATE_AUTO_APPROVAL(
  $collaboration_name
);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling one of the following procedures:

- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('MANAGE TEMPLATE AUTO APPROVAL', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('UPDATE', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`

## Data offering procedures

### REGISTER\_DATA\_OFFERING

Schema:
:   REGISTRY

Registers a data offering so that it can be linked to a collaboration definition. To remove a registered data offering, call [REGISTRY.UNREGISTER\_DATA\_OFFERING](#label-dcr-collaboration-unregister-data-offering-reference). You can’t overwrite an existing data offering, but you can register a new one with the same name and a new version. Creating a new version of a data offering doesn’t remove any earlier versions.

Every data offering must have a unique name-version combination for all data offerings in all registries in your account.

If you want to share this table with others in the collaboration, include the table in the collaboration specification before the collaboration is created.

You must have the REFERENCE\_USAGE privilege with GRANT OPTION on any data that you share in a collaboration. If you do not, you will get a “missing reference usage grant” error when you try to join the collaboration or register the object. [Learn how to handle this issue.](/user-guide/cleanrooms/v2/troubleshooting#label-dcr-database-missing-reference-usage-error)

#### Syntax

Copy code

```
REGISTER_DATA_OFFERING( ['<registry_name>' ,] <data_offering_spec> )
```

#### Arguments

`registry_name` *(Optional)*
:   Name of a [custom registry](/user-guide/cleanrooms/registries) in which to register this data offering. If not specified, registers the data offering in the default account registry.

`data_offering_spec`
:   A [data offering definition](/user-guide/cleanrooms/spec-data-offering#label-dcr-collaboration-data-yaml) in YAML format that describes this data offering.

#### Returns

The data offering ID to use in a collaboration’s `data_offerings.id` field.

#### Examples

Register a data offering in the default registry:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.REGISTER_DATA_OFFERING(
    $$
    api_version: 2.0.0
    spec_type: data_offering
    version: v1
    name: customers
    datasets:
     - alias: customers_1
       data_object_fqn: SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS
       allowed_analyses: template_only
       schema_and_template_policies:
         hashed_email:
           category: join_custom
         status:
           category: passthrough
    $$
  );
```

Register a data offering in a custom registry:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.REGISTER_DATA_OFFERING(
    'my_custom_registry',
    $$
    api_version: 2.0.0
    spec_type: data_offering
    version: v1
    name: customers
    datasets:
     - alias: customers_1
       data_object_fqn: SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS
       allowed_analyses: template_only
       schema_and_template_policies:
         hashed_email:
           category: join_custom
         status:
           category: passthrough
    $$
  );
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling the following procedures.

To register a data offering in the default registry:

- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('REGISTER DATA OFFERING', '{role name}')`

To register items in a custom registry:

- You have read and write privileges on any custom registry that you created yourself.
- To access a custom registry created by another user, you need `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('REGISTER', 'REGISTRY', 'MY_REGISTRY', '{role name}')`.

---

### LINK\_DATA\_OFFERING

Schema:
:   COLLABORATION

A data provider runs this procedure to update an existing collaboration by making the specified data offering available to the specified analysis runners. This is an asynchronous procedure; analysis runners should call VIEW\_DATA\_OFFERINGS to see when the data offering is available to be used.

This procedure is *additive*, meaning that the collaborators you specify are added to the existing list of data offering sharers.

If you want to use this table but not make it visible to other collaborators, call LINK\_LOCAL\_DATA\_OFFERING instead of LINK\_DATA\_OFFERING.

Important

LINK\_DATA\_OFFERING can currently only be called by the role that created or joined the collaboration.

You cannot have an active secondary role when you run this procedure. Run the following SQL code to disable any secondary roles:

Copy code

```
USE SECONDARY ROLES NONE;
```

This procedure is atomic: all of the following conditions must be met for this procedure to succeed. If the link attempt fails for any one collaborator, it fails for all of them.

- All of the specified collaborators must be analysis runners.
- This data offering must not already be shared with any of the specified analysis runners.
- This procedure can be run only by a user with the data provider collaboration role who has joined the collaboration.

You must have the REFERENCE\_USAGE privilege with GRANT OPTION on any data that you wish to share. If you don’t, you’ll get a “missing reference usage grant” error when you try to join the collaboration. [Learn how to handle this issue.](/user-guide/cleanrooms/v2/troubleshooting#label-dcr-database-missing-reference-usage-error)

#### Syntax

Copy code

```
LINK_DATA_OFFERING( <collaboration_name>, <data_offering_id>, <share_with> )
```

#### Arguments

`collaboration_name`
:   Name of the collaboration.

`data_offering_id`
:   ID of the dataset to share, generated when it was registered. The data offering must be visible to you when you call VIEW\_DATA\_OFFERINGS or VIEW\_REGISTERED\_DATA\_OFFERINGS to be able to link it.

`share_with`
:   Array of string aliases of analysis runners to share this dataset with. Collaborators listed here will be added in addition to any other collaborators associated with this data offering. All collaborators listed here must be analysis runners that you are a data provider for, or the procedure will fail without sharing data with anyone.

#### Returns

A string success message.

#### Example

This example allows collaborator `alice` to use the specified data offering in the specified collaboration.

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.LINK_DATA_OFFERING(
  $collaboration_name,
  $my_data_id,
  ['alice']
);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling one of the following procedures:

- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges that must be manually granted to the role.
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges that must be manually granted to the role.

If the data offering is in a custom registry, you must also have `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE( 'READ', '{registry name}', '{role name}')`.

---

### UNLINK\_DATA\_OFFERING

Schema:
:   COLLABORATION

A data provider runs this procedure to remove access to a data offering from specified analysis runners in an existing collaboration. This is an asynchronous procedure; analysis runners should call VIEW\_COLLABORATIONS to confirm the data offering has been removed.

#### Syntax

Copy code

```
UNLINK_DATA_OFFERING( <collaboration_name>, <data_offering_id>, <remove_for> )
```

#### Arguments

`collaboration_name`
:   Name of the collaboration.

`data_offering_id`
:   ID of the dataset to unlink, generated when it was registered.

`remove_for`
:   Array of string aliases of one or more analysis runners to remove access for. All collaborators listed here must be analysis runners that currently have access to this data offering.

#### Returns

A string success message.

#### Example

Copy code

```
-- Remove data offering access for specific analysis runners in this collaboration.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.UNLINK_DATA_OFFERING(
  $collaboration_name,
  $data_offering_id,
  ['AnalysisRunner_1', 'AnalysisRunner_2']
);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling one of the following procedures:

- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`

---

### LINK\_LOCAL\_DATA\_OFFERING

Schema:
:   COLLABORATION

Use this procedure to link your own data into a collaboration if you are using Snowflake Standard Edition. You must first register your data offerings by calling REGISTER\_DATA\_OFFERING. These offerings will not be visible to any other collaborator, and template policies will not be enforced. Tables submitted here propagate the `my_table` array in the template.

For more information, see [Run an analysis with your own data when you use Standard Edition](/user-guide/cleanrooms/demo-flows/basic-multiparty-collab#label-dcr-using-local-data).

#### Syntax

Copy code

```
LINK_LOCAL_DATA_OFFERING( <collaboration_name>, <data_offering_id> )
```

#### Arguments

`collaboration_name`
:   Name of the collaboration.

`data_offering_id`
:   ID of the dataset, generated when you registered it. Also visible in VIEW\_REGISTERED\_DATA\_OFFERINGS and VIEW\_DATA\_OFFERINGS (to you only).

#### Returns

A string success message.

#### Example

This example links a registered data offering for use only by the current account, without exposing it to the rest of the collaborators.

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.LINK_LOCAL_DATA_OFFERING(
  $collaboration_name,
  $my_private_data_offering_id
);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling one of the following procedures:

- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('LINK LOCAL DATA OFFERINGS', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('UPDATE', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`

---

### UNLINK\_LOCAL\_DATA\_OFFERING

Schema:
:   COLLABORATION

Use this procedure to unlink your own local data from a collaboration. After unlinking, the data offering will no longer be available to use in analyses within this collaboration. For more information about local data offerings, see [Run an analysis with your own data when you use Standard Edition](/user-guide/cleanrooms/demo-flows/basic-multiparty-collab#label-dcr-using-local-data).

#### Syntax

Copy code

```
UNLINK_LOCAL_DATA_OFFERING( <collaboration_name>, <data_offering_id> )
```

#### Arguments

`collaboration_name`
:   Name of the collaboration.

`data_offering_id`
:   ID of the dataset to unlink, generated when you registered it. Also visible in VIEW\_REGISTERED\_DATA\_OFFERINGS and VIEW\_DATA\_OFFERINGS (to you only).

#### Returns

A string success message.

#### Example

Copy code

```
-- Unlink a local data offering from a collaboration.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.UNLINK_LOCAL_DATA_OFFERING(
  $collaboration_name,
  $my_private_data_offering_id
);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling one of the following procedures:

- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('UNLINK LOCAL DATA OFFERINGS', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('UPDATE', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`

---

### VIEW\_REGISTERED\_DATA\_OFFERINGS

Schema:
:   REGISTRY

Lists all data offerings that you have registered. To view data offerings in a collaboration linked by others, call COLLABORATION.VIEW\_DATA\_OFFERINGS.

#### Syntax

Copy code

```
VIEW_REGISTERED_DATA_OFFERINGS()
VIEW_REGISTERED_DATA_OFFERINGS( [ '<registry_name>' ] )
```

#### Arguments

`registry_name` *(Optional)*
:   An ARRAY of registry names to scope the read. Use `'default'` (case-insensitive) to include the built-in registry alongside custom ones. Inaccessible or non-existent registries in the array are silently skipped. If not specified, lists data offerings from all registries you have access to.

    Example: `['default', 'my_registry', 'other_reg']`

#### Returns

A table that lists the details of all data offerings that you have registered in this account. The table includes the following columns:

- `DATA_OFFERING_ID`: ID of the data offering.
- `NAME`: Data offering name.
- `VERSION`: Data offering version.
- `DATA_OFFERING_SPEC`: Full YAML specification of the data offering.
- `REGISTRY`: Registry the data offering is registered in.
- `CREATED_ON`: Timestamp when the data offering was created.

#### Examples

List data offerings from all registries:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.VIEW_REGISTERED_DATA_OFFERINGS();
```

List data offerings from the default registry only:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.VIEW_REGISTERED_DATA_OFFERINGS(['default']);
```

List data offerings from specific registries:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.VIEW_REGISTERED_DATA_OFFERINGS(
  ['default', 'my_custom_registry']
);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling one of the following procedures.

To see items in the default registry:

- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('VIEW REGISTERED DATA OFFERINGS', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`

To see items in a custom registry:

- You have read and write privileges on any custom registry that you created yourself.
- To access a custom registry created by another user, you need `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('READ', 'REGISTRY', 'MY_REGISTRY', '{role name}')`.

---

### UNREGISTER\_DATA\_OFFERING

Schema:
:   REGISTRY

Unregisters a data offering that you previously registered, removing it from the registry. To find the ID of a data offering that you registered, call [REGISTRY.VIEW\_REGISTERED\_DATA\_OFFERINGS](#label-dcr-collaboration-view-registered-data-offerings-reference).

You can’t unregister a data offering that is currently used in a collaboration. If the data offering is linked to one or more collaborations, the procedure fails and returns an error that lists those collaborations; remove the data offering from each of them before you unregister it.

#### Syntax

Copy code

```
UNREGISTER_DATA_OFFERING( '<data_offering_id>' )
```

#### Arguments

`data_offering_id`
:   The ID of the data offering to unregister, as returned by [REGISTRY.REGISTER\_DATA\_OFFERING](#label-dcr-collaboration-register-data-offering-reference) or [REGISTRY.VIEW\_REGISTERED\_DATA\_OFFERINGS](#label-dcr-collaboration-view-registered-data-offerings-reference). A data offering ID has the form `{name}_{version}`.

#### Returns

A table with a status message confirming that the data offering was unregistered.

#### Example

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.UNREGISTER_DATA_OFFERING('customers_v1');
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling the following procedures.

To unregister a data offering in the default registry:

- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('REGISTER DATA OFFERING', '{role name}')`

To unregister items in a custom registry:

- You have read and write privileges on any custom registry that you created yourself.
- To access a custom registry created by another user, you need `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('REGISTER', 'REGISTRY', 'MY_REGISTRY', '{role name}')`.

---

### VIEW\_DATA\_OFFERINGS

Schema:
:   COLLABORATION

Lists all data offerings present in a specified collaboration that you can access as an analysis runner, or that you have linked yourself. To see only data offerings that you registered, call REGISTRY.VIEW\_REGISTERED\_DATA\_OFFERINGS.

You can see data offerings from collaborator X only after X has joined the collaboration.

#### Syntax

Copy code

```
VIEW_DATA_OFFERINGS( <collaboration_name> )
```

#### Arguments

`collaboration_name`
:   Name of the collaboration to explore.

#### Returns

Information about all data offerings in the specified collaboration. The table includes the
following columns:

- `template_view_name`: The fully qualified view name used to reference offerings when calling RUN to query using a template. Pass this
  name into the `source_tables` field in the RUN spec.
- `template_join_columns`: Names of columns in this table that can be used in joins in template-based queries.
- `analysis_allowed_columns`: Names of columns in this table that can be projected in template-based queries.
- `activation_allowed_columns`: Names of columns in this table that can be activated.
- `freeform_sql_view_name`: The fully qualified view name used in free-form SQL queries, when the dataset supports
  [free-form SQL queries](/user-guide/cleanrooms/free-form-sql). This cell is empty if the dataset doesn’t offer free-form SQL
  queries.
- `freeform_sql_column_policies`: A JSON representation of all [free-form column policies](/user-guide/cleanrooms/spec-data-offering#label-dcr-freeform-sql-policies-field)
  in this collaboration, keyed by policy type.
- `shared_by`: The collaborator that linked this data offering.
- `shared_with`: Who can use the data in an analysis. If this value is `LOCAL`, this is a local dataset that isn’t shared with any
  collaborators except for the party that hosts the data.
- `data_offering_id`: The unique ID of this data offering, generated when it was registered.

#### Example

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.VIEW_DATA_OFFERINGS(
  $collaboration_name
);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling one of the following procedures:

- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('VIEW DATA OFFERINGS', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('READ', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`

## Code spec procedures

These procedures manage code specs, which define Python functions, stored procedures, or ML Jobs
that can be called from collaboration templates. For more information, see
[Code specs](/user-guide/cleanrooms/resources-code-specs).

### REGISTER\_CODE\_SPEC

Schema:
:   REGISTRY

Registers a code spec. This stores the code in the clean rooms environment in the REGISTRY.CODE\_SPECS table. After a code spec is registered, it can be used by a template.

Every code spec registered must have a unique name-version combination across all registries in your account.

#### Syntax

Copy code

```
REGISTER_CODE_SPEC( ['<registry_name>' ,] <code_spec> )
```

#### Arguments

`registry_name` *(Optional)*
:   Name of a [custom registry](/user-guide/cleanrooms/registries) in which to register this code spec. If not specified, registers the code spec in the default account registry.

`code_spec`
:   Code specification in YAML format, as a string.

#### Returns

The generated code spec ID.

#### Examples

Register a code spec in the default registry:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.REGISTER_CODE_SPEC(
  $$
  api_version: 2.0.0
  spec_type: code_spec
  name: custom_udf
  version: v1
  description: Custom UDF for data normalization

  functions:
    - name: normalize_value
      type: UDF
      language: PYTHON
      runtime_version: "3.10"
      handler: normalize
      arguments:
        - name: value
          type: FLOAT
        - name: min_val
          type: FLOAT
        - name: max_val
          type: FLOAT
      returns: FLOAT
      code_body: |
        def normalize(value, min_val, max_val):
            if max_val == min_val:
                return 0.0
            return (value - min_val) / (max_val - min_val)
  $$
);
```

Register a code spec in a custom registry:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.REGISTER_CODE_SPEC(
  'my_custom_registry',
  $$
  api_version: 2.0.0
  spec_type: code_spec
  name: custom_udf
  version: v1
  description: Custom UDF for data normalization

  functions:
    - name: normalize_value
      type: UDF
      language: PYTHON
      runtime_version: "3.10"
      handler: normalize
      arguments:
        - name: value
          type: FLOAT
        - name: min_val
          type: FLOAT
        - name: max_val
          type: FLOAT
      returns: FLOAT
      code_body: |
        def normalize(value, min_val, max_val):
            if max_val == min_val:
                return 0.0
            return (value - min_val) / (max_val - min_val)
  $$
);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling the following procedures.

To register objects in the default registry:

- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('REGISTER CODE SPEC', '{role name}')`

To register items in a custom registry:

- You have read and write privileges on any custom registry that you created yourself.
- To access a custom registry created by another user, you need `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('REGISTER', 'REGISTRY', 'MY_REGISTRY', '{role name}')`.

---

### VIEW\_REGISTERED\_CODE\_SPECS

Schema:
:   REGISTRY

Lists all code specs registered by this role in the local account registry.

#### Syntax

Copy code

```
VIEW_REGISTERED_CODE_SPECS()
VIEW_REGISTERED_CODE_SPECS( [ '<registry_name>' ] )
```

#### Arguments

`registry_name` *(Optional)*
:   An ARRAY of registry names to scope the read. Use `'default'` (case-insensitive) to include the built-in registry alongside custom ones. Inaccessible or non-existent registries in the array are silently skipped. If not specified, lists code specs from all registries you have access to.

    Example: `['default', 'my_registry', 'other_reg']`

#### Returns

A table that lists the details of all code specs that you have registered in this account. The table includes the following columns:

- `CODE_SPEC_ID`: ID of the code spec.
- `NAME`: Code spec name.
- `VERSION`: Code spec version.
- `CODE_SPEC`: Full YAML code specification.
- `REGISTRY`: Registry the code spec is registered in.
- `CREATED_ON`: Timestamp when the code spec was registered.

#### Examples

List code specs from all registries:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.VIEW_REGISTERED_CODE_SPECS();
```

List code specs from the default registry only:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.VIEW_REGISTERED_CODE_SPECS(['default']);
```

List code specs from specific registries:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.VIEW_REGISTERED_CODE_SPECS(
  ['default', 'my_custom_registry']
);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling one of the following procedures.

To see items in the default registry:

- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('VIEW REGISTERED CODE SPECS', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`

To see items in a custom registry:

- You have read and write privileges on any custom registry that you created yourself.
- To access a custom registry created by another user, you need `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('READ', 'REGISTRY', 'MY_REGISTRY', '{role name}')`.

---

### VIEW\_CODE\_SPECS

Schema:
:   COLLABORATION

Returns all code specs that are referenced by any template that you created or can run in the specified collaboration.

#### Syntax

Copy code

```
VIEW_CODE_SPECS( <collaboration_name> )
```

#### Arguments

`collaboration_name`
:   Name of the collaboration.

#### Returns

A table that lists the code specs available in the specified collaboration. The table includes the following columns:

- `code_spec_id`: ID of this code spec.
- `code_spec`: Full YAML code specification.
- `shared_by`: Collaborator alias that shared the code spec.

#### Example

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.VIEW_CODE_SPECS(
  $collaboration_id
);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling one of the following procedures:

- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('VIEW CODE SPECS', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('READ', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`

## Update request procedures

These procedures are used to manage collaboration update requests that require approval, such as
the [link template flow.](/user-guide/cleanrooms/resources-templates#label-dcr-collaboration-add-template-post-creation)

### VIEW\_UPDATE\_REQUESTS

Schema:
:   COLLABORATION

See all update requests that you have created or that you can approve or deny, in the specified collaboration. This includes all collaboration changes such as adding data offerings, templates, and code packages. This procedure shows the status of the update.
It can take a few seconds for an update request to appear in the request list, so you might not see a request that you just sent a moment ago.

[See the link template flow.](/user-guide/cleanrooms/resources-templates#label-dcr-collaboration-add-template-post-creation)

#### Syntax

Copy code

```
VIEW_UPDATE_REQUESTS( <collaboration_name> )
```

#### Arguments

`collaboration_name`
:   Name of the collaboration.

#### Returns

A table of update requests sent in this collaboration. Information includes:

- `id`: ID of the request. Use this to approve or deny a request.
- `type`: Type of request. The following values are supported:

  - Add Template
  - Link Data Offering
  - Unlink Data Offering
  - Remove Template
  - Edit Collaboration
- `status`: Current status of the request. The following statuses can be reported:

  - REQUESTED: The request has been submitted.
  - PENDING\_MY\_APPROVAL: The request is awaiting your approval or rejection.
  - PENDING\_PARTNER\_APPROVAL: You have approved the request, but the request still needs to be approved by one or more other collaborators.
  - REJECTED: Someone in the collaboration rejected this request.
  - APPROVED: All required approvers have approved the request.
  - COMPLETED: The update action has been completed and changes applied to the collaboration. For templates that include a code spec, you
    should still [check the upgrade state](/user-guide/cleanrooms/resources-code-specs) to see when the code spec is ready to be called.
  - FAILED: The update action has failed. See the `DETAILS` column for failure details. For an Edit Collaboration request, this status is also used when only some of the requested operations could be applied; the `details` column reports the status of each individual operation.
- `approval_log`: Log of all approvals and rejections of the request. If the request is rejected, the reason given by the rejecting party is also provided here.
- `details`: Details specific to the request type, such as the template name and whom it is shared with for an ‘Add Template’ request. For an ‘Edit Collaboration’ request, this column contains operation-wise payloads that report the outcome of each individual operation in the edit.
- `spec`: The details of the resource being updated, such as the template specification for an ‘Add Template’ request or the collaboration specification for an ‘Edit Collaboration’ request.
- `updated_on`: The timestamp when the last action was taken on this request (for example, an approval or rejection).

#### Details column contents

The `details` column contains a JSON payload whose fields depend on the request type. The following table lists the fields included for each type. Unless noted otherwise, `failure_reason` is included only when the status is `FAILED`.

| Request type | Fields in `details` |
| --- | --- |
| Add Template | `template_id`, `share_with`, `code_specs` (only when the template has code specs), `requested_by`, `failure_reason` |
| Remove Template | `template_id`, `remove_for`, `requested_by`, `failure_reason` |
| Link Data Offering | `data_offering_id`, `share_with`, `requested_by`, `failure_reason` |
| Unlink Data Offering | `data_offering_id`, `remove_for`, `requested_by`, `failure_reason` |
| Edit Collaboration | `operations` (one entry per operation, each with `operation_type`, operation-specific fields, a per-operation `status`, and `failure_reason` when it fails), `requested_by`, `failure_reason` |

Expand

Show lessSee more

#### Example

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.VIEW_UPDATE_REQUESTS(
  $collaboration_name
);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling one of the following procedures:

- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('VIEW UPDATE REQUESTS', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('UPDATE', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('READ', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`

---

### APPROVE\_UPDATE\_REQUEST

Schema:
:   COLLABORATION

Approves a collaboration update request. See your list of pending requests by calling VIEW\_UPDATE\_REQUESTS. Once you approve a request, you cannot reject it later.

All affected collaborators must approve a request before the change is actually applied to the collaboration.

[See the link template flow.](/user-guide/cleanrooms/resources-templates#label-dcr-collaboration-add-template-post-creation)

#### Syntax

Copy code

```
APPROVE_UPDATE_REQUEST( <collaboration_name>, <request_id> )
```

#### Arguments

`collaboration_name`
:   Name of the collaboration.

`request_id`
:   ID of the request.

#### Returns

A string success message.

#### Example

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.APPROVE_UPDATE_REQUEST(
  $collaboration_name,
  $request_id
);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling one of the following procedures:

- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('MANAGE UPDATE REQUEST', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('UPDATE', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`

---

### REJECT\_UPDATE\_REQUEST

Schema:
:   COLLABORATION

Rejects a collaboration update request. A single rejection prevents the change from being applied to the collaboration. You cannot approve a request after rejecting it.

#### Syntax

Copy code

```
REJECT_UPDATE_REQUEST( <collaboration_name>, <request_id>, <reason> )
```

#### Arguments

`collaboration_name`
:   Name of the collaboration.

`request_id`
:   ID of the request.

`reason`
:   A human-readable description of why the request was rejected. The argument is required, but you can submit an empty string.

#### Returns

A string success message.

#### Example

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.REJECT_UPDATE_REQUEST(
  $collaboration_name,
  'request_1324f934457',
  'Needs more cowbell'
);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling one of the following procedures:

- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('MANAGE UPDATE REQUEST', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('UPDATE', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`

## Collaboration management procedures

### INITIALIZE

Schema:
:   COLLABORATION

The owner calls this to create a collaboration and, optionally, join the collaboration. If `auto_join_warehouse` is FALSE, you must call JOIN separately to make the collaboration available to other collaborators. You must use the same role to call INITIALIZE and then JOIN.

Submitting a collaboration definition with the same `name` value as an existing collaboration throws an error.

It takes some time to create and join a collaboration, so you must call GET\_STATUS to learn when the collaboration has been joined.

#### Syntax

Copy code

```
INITIALIZE( <collaboration_spec> [, '<auto_join_warehouse>'] )
```

#### Arguments

`collaboration_spec`
:   [Collaboration definition](/user-guide/cleanrooms/spec-collaboration#label-dcr-collaboration-spec-yaml) in YAML format, as a string.

`auto_join_warehouse` *(Optional)*
:   String that specifies a warehouse name as a valid Snowflake identifier. If specified, the collaboration will be created and joined using
    this warehouse. If not specified, the current warehouse will be used to create the collaboration, and you must call JOIN to join the
    collaboration. An XS warehouse is recommended.

#### Returns

A table with the following columns:

- `collaboration_name`: The name of the collaboration. Use this in any procedures that require you to specify a collaboration.
- `message`: Information about the initialize request.
- `auto_join_task`: If `auto_join_warehouse` was specified, indicates whether the auto-join task was created.

#### Examples

The following example creates a collaboration where Alice is the owner and can run an analysis using data provided
by Bob.

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.INITIALIZE(
  $$
  api_version: 2.0.0
  spec_type: collaboration
  name: basic_collaboration
  owner: alice
  collaborator_identifier_aliases:
    alice: corp_id.account_id
    bob: corp2_id.account2_id
  analysis_runners:
    alice:
      data_providers:
        bob:
          data_offerings:
          - id: bob_data_v1
      templates:
      - id: alice_test_template_2026_01_12_V1
  $$,
  'APP_WH'
);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling the following procedure:

- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`

  If providing the `auto-join-warehouse` parameter and using a role other than SAMOOHA\_APP\_ROLE, the role must also be granted the
  EXECUTE TASK account-level privilege.

See [GRANT\_PRIVILEGE\_ON\_ACCOUNT\_TO\_ROLE](#label-dcr-grant-privilege-on-account-to-role) for additional required role permissions.

---

### EDIT

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Schema:
:   COLLABORATION

Called by the owner to edit an existing collaboration in place. The owner submits the full, target [collaboration specification](/user-guide/cleanrooms/spec-collaboration#label-dcr-collaboration-spec-yaml); the procedure compares it to the current specification and applies the differences as a single bulk update request. Only the collaboration owner can call this procedure.

The changes are not applied immediately. EDIT creates one update request that must be approved by all affected collaborators before any change takes effect. Track the request by calling [VIEW\_UPDATE\_REQUESTS](#label-dcr-collaboration-view-update-requests-reference), where it appears with the type `Edit Collaboration`.

#### Supported changes

EDIT supports the following changes:

- Add a new collaborator as an analysis runner or a data provider.
- Remove an existing collaborator. Removal can be partial (from specific components) or complete (from the entire collaboration).
- Change a collaborator’s role (for example, update a data provider to an analysis runner, or the reverse).
- Share an already-registered template with an analysis runner, or remove a shared template.
- Share an already-linked data offering from a data provider with an analysis runner, or unlink a shared data offering.

The following fields cannot be changed with EDIT:

- `name`
- `description`
- `owner`
- `activation_destinations`

You cannot rename an existing alias in `collaborator_identifier_aliases` or remap it to a different account. However, `collaborator_identifier_aliases` is updated automatically as collaborators are added or removed.

The `api_version` and `spec_type` fields are immutable and cannot be changed for an existing collaboration.

Note

EDIT works alongside the existing post-creation flows. You can still
[link a data offering](#label-dcr-collaboration-link-data-offering-reference) with LINK\_DATA\_OFFERING,
[add a template](#label-dcr-collaboration-add-template-request-reference) with ADD\_TEMPLATE\_REQUEST,
[remove a template](#label-dcr-collaboration-remove-template-reference) with REMOVE\_TEMPLATE, and
[unlink a data offering](#label-dcr-collaboration-unlink-data-offering-reference) with UNLINK\_DATA\_OFFERING.

#### Syntax

Copy code

```
EDIT( <collaboration_name>, <target_collaboration_spec> )
```

#### Arguments

`collaboration_name`
:   Name of the collaboration to edit.

`target_collaboration_spec`
:   The full, target [collaboration definition](/user-guide/cleanrooms/spec-collaboration#label-dcr-collaboration-spec-yaml) in YAML format, as a string. This is the target state of the collaboration, not a partial diff. The procedure validates the specification, compares it to the current specification, and derives the set of changes to apply. If the submitted specification is identical to the current one, or if it would produce an invalid collaboration topology, the procedure returns an error.

#### Returns

A string message confirming that the update request has been submitted. Use [VIEW\_UPDATE\_REQUESTS](#label-dcr-collaboration-view-update-requests-reference) to track the status of the request and to see the operation-wise payloads in the `details` column.

#### Usage notes

- Approvers can only approve or reject the entire request; partial approval of individual changes is not supported.
- You can only add a collaborator in a different cloud region from the owner if the collaboration was originally created as a cross-cloud collaboration. If the collaboration wasn’t initially set up for [Cross-Cloud Auto-Fulfillment](/user-guide/cleanrooms/laf#label-dcr-collab-enabling-laf), every collaborator added with EDIT must be in the same region as the owner. Conversely, removing the last cross-region collaborator does not cause the collaboration to start supporting [external tables](/user-guide/cleanrooms/laf#label-dcr-collab-laf-limitations).
- When the edit adds a new collaborator, the collaboration tracks that collaborator through the `INVITED`, `REVIEWING`, `JOINING`, and `JOINED` states. The update request moves directly to `APPROVED` once the existing collaborators approve it; the new collaborator’s review and join operations do not change the request status. Affected collaborators can review any newly shared resources by calling [VIEW\_DATA\_OFFERINGS](#label-dcr-collaboration-view-data-offerings-reference), [VIEW\_TEMPLATES](#label-dcr-collaboration-view-templates-reference), and [VIEW\_CODE\_SPECS](#label-dcr-collaboration-view-code-specs-reference).

#### Example

The following example adds a new collaborator, `carol`, to an existing collaboration as an analysis runner who can use Bob’s data offering and an existing template. The owner submits the complete updated specification, including the new analysis runner and alias.

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.EDIT(
  'basic_collaboration',
  $$
  api_version: 2.0.0
  spec_type: collaboration
  name: basic_collaboration
  owner: alice
  collaborator_identifier_aliases:
    alice: corp_id.account_id
    bob: corp2_id.account2_id
    carol: corp3_id.account3_id
  analysis_runners:
    alice:
      data_providers:
        bob:
          data_offerings:
          - id: bob_data_v1
      templates:
      - id: alice_test_template_2026_01_12_V1
    carol:
      data_providers:
        bob:
          data_offerings:
          - id: bob_data_v1
      templates:
      - id: alice_test_template_2026_01_12_V1
  $$
);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling the following procedure:

- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('UPDATE', 'COLLABORATION', '{collaboration name}', '{role name}')`

---

### TEARDOWN

Schema:
:   COLLABORATION

Called by the owner to delete a collaboration for all parties.

**You must call this procedure twice.** Call it once, then call GET\_STATUS until it returns `LOCAL_DROP_PENDING`, then call this procedure again.

Tearing down a collaboration doesn’t finish cleanup in the other collaborators’ accounts. All other collaborators see their status change to
`LOCAL_DROP_PENDING` and must call [LEAVE](#label-dcr-collaboration-leave-reference) to remove the clean room application and collaboration
metadata from their account.

Note

This procedure can be called only on a collaboration that you have created and joined. If you have created but not yet joined the
collaboration, you must join it before you can tear it down.

#### Syntax

Copy code

```
TEARDOWN( <collaboration_name> )
```

#### Arguments

`collaboration_name`
:   Name of the collaboration to delete.

#### Returns

A string success message.

#### Example

Copy code

```
-- Start the process.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.TEARDOWN($collaboration_name);

-- Call until it returns LOCAL_DROP_PENDING.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.GET_STATUS($collaboration_name);

-- Final call.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.TEARDOWN($collaboration_name);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling one of the following procedures:

- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`

See [GRANT\_PRIVILEGE\_ON\_ACCOUNT\_TO\_ROLE](#label-dcr-grant-privilege-on-account-to-role) for additional required role permissions.

---

### GET\_STATUS

Schema:
:   COLLABORATION

Shows information about all collaborators in a given collaboration.

When running an asynchronous operation such as creating or joining a collaboration, you must check the status to know when the last operation was complete before you can perform additional actions on that collaboration, such as running analyses. This procedure can be called by any collaborator invited to a collaboration.

Collaboration owners can see the following status pathway:

- CREATING » CREATED » INSTALLING » IN\_REVIEW (or INSTALLATION\_FAILED) » JOINING » JOINED (or JOIN\_FAILED)

Non-owners will see the following status pathway:

- INSTALLING » IN\_REVIEW (or INSTALLATION\_FAILED) » JOINING » JOINED (or JOIN\_FAILED)

If the collaboration involves accounts in different regions, you might also see a `REPLICATING` status while the collaboration listing replicates to your region. For details, see [Cross-region replication delays](/user-guide/cleanrooms/v2/troubleshooting#label-dcr-collaboration-replication-delays).

#### Syntax

Copy code

```
GET_STATUS( <collaboration_name> )
```

#### Arguments

`collaboration_name`
:   Name of the collaboration to see the status of. You can see a list of your collaborations by calling
    COLLABORATION.VIEW\_COLLABORATIONS. You must be invited to, or have joined, a collaboration before you can call GET\_STATUS on it.

#### Returns

A table that shows the details about the latest join attempt for all collaborators in the specified collaboration. The table includes the following columns:

- `updated_on`: Timestamp when the status was reported by the system.
- `collaborator_account`: Data sharing account ID of this collaborator.
- `collaborator_name`: The collaborator’s alias, as declared in the collaboration specification.
- `roles`: The actual and potential roles for this collaborator. Values include `owner`, `data_provider`, `analysis_runner`.
- `status`: Status at the updated time. The following values are supported, and show the status of the named collaborator in the specified collaboration.

  - `CREATING`: Collaboration creation has started.
  - `CREATE_FAILED`: Collaboration creation failed.
  - `CREATE_TIMED_OUT`: Collaboration creation timed out.
  - `INSTALLING`: Installing the application package and preparing the collaboration details for review.
  - `REPLICATING`: The collaboration listing is still replicating to your region, so the REVIEW or JOIN operation you called couldn’t finish yet. Call GET\_STATUS again to check whether replication has finished. For details, see [Cross-region replication delays](/user-guide/cleanrooms/v2/troubleshooting#label-dcr-collaboration-replication-delays).
  - `CREATED`: Collaboration has been created and is ready to operate on. If a previous JOIN failed because the listing was still replicating, this status signals that replication has finished and you can call JOIN again.
  - `IN_REVIEW`: The collaboration is in review.
  - `INSTALLATION_FAILED`: Installation failed; application package not installed, and can’t be reviewed.
  - `INVITED`: Participant has been invited. If a previous REVIEW failed because the listing was still replicating, this status signals that replication has finished and you can call REVIEW again.
  - `JOINING`: Join process has started.
  - `JOIN_FAILED`: Join process failed.
  - `JOINED`: Successfully joined the collaboration. You can start to use the collaboration.
  - `LEAVING`: Leave process has started.
  - `LEAVE_FAILED`: Leave process failed.
  - `LEFT`: Successfully left the collaboration.
  - `LOCAL_DROP_PENDING`: The collaboration is ready to be cleaned up in your account, either because you requested to leave it, or because the owner tore down the collaboration. Complete the process by calling LEAVE, or TEARDOWN if you’re the owner.
  - `DROPPING`: Drop process has started.
  - `DROPPED`: Successfully dropped.
  - `DROP_FAILED`: Drop process failed.
- `details`: Additional details about the current status, if available.
- `region`: The cloud region of this collaborator.

#### Example

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.GET_STATUS(
  $collaboration_name
);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling one of the following procedures:

- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('GET STATUS', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('READ', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`

---

### ENABLE\_EXTERNAL\_TABLE\_ANALYSIS\_FOR\_COLLABORATION

Schema:
:   ADMIN

Enables external and Apache Iceberg™ tables to be used to run an analysis in your account. An analysis runner must call this before running any analysis that includes external or Iceberg tables. This procedure is called once per collaboration, not once per analysis.

#### Syntax

Copy code

```
ENABLE_EXTERNAL_TABLE_ANALYSIS_FOR_COLLABORATION( <collaboration_name> )
```

#### Arguments

`collaboration_name`
:   Name of the collaboration.

#### Returns

A table with a `MESSAGE` column containing a success message.

#### Example

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.ADMIN.ENABLE_EXTERNAL_TABLE_ANALYSIS_FOR_COLLABORATION(
  $collaboration_name
);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted the MANAGE FIREWALL CONFIGURATION privilege to call this procedure.

---

### VIEW\_COLLABORATIONS

Schema:
:   COLLABORATION

View information about collaborations that you have created, can review, or have joined.

#### Syntax

Copy code

```
VIEW_COLLABORATIONS()
```

#### Arguments

*None*

#### Returns

A table that lists details of all collaborations that you can access. The table includes the following columns:

- `source_name`: The name of the collaboration, as specified by the `name` value in the collaboration specification.
- `collaboration_name`: The name of the installed collaboration. This is NULL until the collaboration is installed by calling JOIN (owners) or REVIEW (non-owners).
- `owner_account`: Data sharing ID of the account that created the collaboration.
- `updated_on`: When the collaboration was last updated.
- `collaboration_spec`: The specification for this collaboration in YAML format. This shows the latest version of the collaboration, including any resources linked or removed after the collaboration was created. However, there might be update requests that are in progress that will be linked soon, such as new or removed templates or data offerings.

#### Examples

View all collaborations:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.VIEW_COLLABORATIONS();
```

View the specification for a given collaboration by name:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.VIEW_COLLABORATIONS() ->>
SELECT "COLLABORATION_SPEC" FROM $1 WHERE "SOURCE_NAME" = $collaboration_name;
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling one of the following procedures:

- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('READ', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('RUN', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('VIEW COLLABORATIONS', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`

---

### REVIEW

Schema:
:   COLLABORATION

Provides details about a collaboration to which you have been invited. Call COLLABORATION.VIEW\_COLLABORATIONS to see which
collaborations you have been invited to and not yet joined. All collaborators except the owner must call this
procedure before calling JOIN. You cannot call this procedure on a collaboration that you have joined. You must use the same role to call REVIEW and JOIN. If your account is on a different cloud hosting region than the owner, you might need to call this procedure several times until it returns a successful response.

This procedure installs the underlying application in your account.

**Important notes:**

- Owners cannot call REVIEW on their own collaborations.
- Everyone except the owner must call REVIEW before calling JOIN.
- After you have joined a collaboration, you cannot call REVIEW again.

#### Syntax

Copy code

```
REVIEW( <source_name>, <owner_account> )
REVIEW( <source_name>, <owner_account>, <collaboration_name> )
```

#### Arguments

`source_name`
:   Name of the collaboration you have been invited to join. You can see a list of your collaborations by calling
    COLLABORATION.VIEW\_COLLABORATIONS.

`owner_account`
:   [Data Sharing Account Identifier](/user-guide/admin-account-identifier#label-account-name-data-sharing) of the owner. This can be found in the response to COLLABORATION.VIEW\_COLLABORATIONS.

`collaboration_name` *(Optional)*
:   Name to assign to the collaboration when it’s installed in your account. Use this name in later procedures that require you to specify a collaboration. If not specified, the collaboration name defaults to `source_name`.

#### Returns

Table of information about the collaboration, including the collaboration ID, owner, and the collaboration specification.

If your account is on a [different cloud hosting region](/user-guide/cleanrooms/laf#label-dcr-collab-enabling-laf) than the collaboration owner’s, REVIEW might return a message saying that additional setup steps are still being performed. If you get this message, continue calling REVIEW until it returns the information table about the collaboration.

#### Example

Copy code

```
-- View the collaboration for your own usage.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.REVIEW(
  $collaboration_name,
  'org1.account1234'
);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling one of the following procedures:

- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('REVIEW COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`

See [GRANT\_PRIVILEGE\_ON\_ACCOUNT\_TO\_ROLE](#label-dcr-grant-privilege-on-account-to-role) for additional required role permissions.

---

### JOIN

Schema:
:   COLLABORATION

Asynchronous method to join a specified collaboration. Note that you can access only the resources listed in the collaboration at the time that you join. This procedure takes some time to run.

You need the REGISTER DATA OFFERING account privilege to join any collaboration in which you can activate data (that is, you are an analysis runner and the collaboration specification includes an `activation_destinations` field). See the [access management API reference guide](#label-dcr-collaboration-access-management-api).

You cannot have an active secondary role when you run this procedure. Run the following SQL code to disable any secondary roles:

Copy code

```
USE SECONDARY ROLES NONE;
```

Everyone except the collaboration creator must call COLLABORATION.REVIEW before calling this procedure.

This procedure is asynchronous; call GET\_STATUS to determine when you have successfully joined the collaboration.

Anyone who submits a resource to the collaboration or wants to run a template in the collaboration must join the collaboration first. The collaboration creator joins automatically when calling INITIALIZE (unless `auto_join_warehouse` is set to FALSE).

#### Syntax

Copy code

```
JOIN( <collaboration_name> )
```

#### Arguments

`collaboration_name`
:   Name of the collaboration to join. This is the local name assigned when you called COLLABORATION.REVIEW (which defaults to the `source_name` unless you specified a different `collaboration_name`). You can see a list of your collaborations by calling
    COLLABORATION.VIEW\_COLLABORATIONS. If you have been invited to join multiple collaborations with the same name, this defaults to
    the last one that you called COLLABORATION.REVIEW on.

#### Returns

A string success message. If you get an error about a missing reference usage grant, see the [Troubleshooting guide](/user-guide/cleanrooms/v2/troubleshooting#label-dcr-database-missing-reference-usage-error).

#### Example

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.JOIN(
  $collaboration_name
);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling one of the following procedures:

- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`

See [GRANT\_PRIVILEGE\_ON\_ACCOUNT\_TO\_ROLE](#label-dcr-grant-privilege-on-account-to-role) for additional required role permissions.

---

### LEAVE

Schema:
:   COLLABORATION

Leaves a collaboration that you have joined. You cannot rejoin a collaboration after you have left it.

**You must call this procedure twice.** Call it once, then call GET\_STATUS until it returns `LOCAL_DROP_PENDING`, then call this procedure again.

#### Syntax

Copy code

```
LEAVE( <collaboration_name> )
```

#### Arguments

`collaboration_name`
:   Name of the collaboration to leave.

#### Returns

A string success message.

#### Example

Copy code

```
-- Start the process.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.LEAVE($collaboration_name);

-- Call until it returns LOCAL_DROP_PENDING.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.GET_STATUS($collaboration_name);

-- Final call.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.LEAVE($collaboration_name);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling one of the following procedures:

- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`

See [GRANT\_PRIVILEGE\_ON\_ACCOUNT\_TO\_ROLE](#label-dcr-grant-privilege-on-account-to-role) for additional required role permissions.

---

### GET\_CONFIGURATION

Schema:
:   COLLABORATION

Returns the current configuration settings for a collaboration. You must have joined the collaboration before calling this procedure.

#### Syntax

Copy code

```
GET_CONFIGURATION( <collaboration_name> )
```

#### Arguments

`collaboration_name`
:   Name of the collaboration.

#### Returns

A table with the following columns:

| Column | Description |
| --- | --- |
| CONFIGURATION | The name of the configuration setting. |
| VALUE | The current value of the configuration. |
| STATUS | Whether the value is `ACTIVE` or `PENDING` (a change has been requested but not yet applied). |

Expand

Show lessSee more

##### Supported configurations

| Configuration name | Description |
| --- | --- |
| TEMPLATE\_AUTO\_APPROVAL | Whether template update requests from other collaborators are automatically approved. Values: `true` or `false`. Default: `false`. |
| ALLOW\_ML\_JOBS\_MONITORING | Whether collaborators can retrieve ML Jobs container logs using the `get_logs` action. Values: `true` or `false`. Default: `true`. Only the collaboration owner can change this value. |

Expand

Show lessSee more

#### Example

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.GET_CONFIGURATION(
  $collaboration_name
);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling one of the following procedures:

- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('MANAGE TEMPLATE AUTO APPROVAL', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('READ', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`

---

### SET\_CONFIGURATION

Schema:
:   COLLABORATION

Sets a configuration value for a collaboration. The change is asynchronous: call GET\_CONFIGURATION to check when the new value has been applied. You must have joined the collaboration before calling this procedure.

Use this procedure to manage template auto-approval instead of the deprecated ENABLE\_TEMPLATE\_AUTO\_APPROVAL and DISABLE\_TEMPLATE\_AUTO\_APPROVAL procedures. Setting `TEMPLATE_AUTO_APPROVAL` to `true` enables automatic approval, and setting it to `false` disables it.

#### Syntax

Copy code

```
SET_CONFIGURATION( <collaboration_name>, <config_name>, <value> )
```

#### Arguments

`collaboration_name`
:   Name of the collaboration.

`config_name`
:   Name of the configuration to set. See GET\_CONFIGURATION for supported configuration names.

`value`
:   The new value for the configuration. Must be a valid value for the specified configuration name.

#### Returns

A string message confirming the request has been accepted.

#### Example

Copy code

```
-- Enable automatic approval of template requests
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.SET_CONFIGURATION(
  $collaboration_name,
  'TEMPLATE_AUTO_APPROVAL',
  'true'
);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling one of the following procedures:

- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('MANAGE TEMPLATE AUTO APPROVAL', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('UPDATE', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`

## Running analyses and activations

### RUN

Schema:
:   COLLABORATION

Runs an analysis in the data clean room. You can pass in run details either as individual parameters, or by passing in an [analysis YAML specification string](/user-guide/cleanrooms/spec-analysis#label-dcr-collaboration-analysis-yaml).

Read the [consumer.run\_analysis](/user-guide/cleanrooms/consumer#dcr-consumer-run-analysis) reference for background about running a template in a data clean room.

There are two versions of this procedure: one that takes the run arguments as a single YAML-formatted string, and one that takes the arguments as individual parameters.

#### Syntax

**YAML argument syntax:**

Copy code

```
RUN( <collaboration_name>, <analysis_spec> )
```

**Explicit parameters syntax:**

Copy code

```
RUN( <collaboration_name>, <template_id>, <template_view_names>, <local_template_view_names>, <arguments> )
```

#### Arguments

`collaboration_name`
:   Name of the collaboration in which to run this analysis.

`analysis_spec`
:   [Analysis definition](/user-guide/cleanrooms/spec-analysis#label-dcr-collaboration-analysis-yaml) in YAML format as a string, describing the template, tables, and template values to use in this analysis. Used with the YAML argument syntax.

`template_id`
:   ID of the template to run.

`template_view_names`
:   Array of string names of source tables to use in the analysis. Use table names returned by VIEW\_DATA\_OFFERINGS in the `template_view_name` column. The format for each entry is `user_alias.data_offering_id.dataset_alias`

    Don’t include datasets that the template author [preset in the template](/user-guide/cleanrooms/custom-templates#label-dcr-template-preset-tables) (preview); those are
    supplied by the template. Pass an empty array if the template pins every dataset it reads.

`local_template_view_names`
:   Array of string IDs of your own tables to use in the analysis. You must link these tables first by calling LINK\_LOCAL\_DATA\_OFFERING.

`arguments`
:   JSON object that contains named arguments used by the template, where each key is a template argument name, and the value is the value of that argument.

    `preset_tables` is a reserved argument name. Snowflake rejects a RUN call that passes `preset_tables` in `arguments`.

#### Returns

Analysis results in table format.

#### Examples

Pass by parameter example:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.RUN(
  $collaboration_name,
  $template_name,
  ['Provider.data_offering_1_2026_01_12_v0.test_dataset'], -- Tables to pass to source_tables variable.
  [],
  {} -- Template takes no parameters.
);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling one of the following procedures:

- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('RUN', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`

---

### RUN\_ML\_JOB\_ACTION

Schema:
:   COLLABORATION

Monitors and manages a running or completed ML Job in a collaboration. Returns status, logs, or
results depending on the action specified. For a conceptual overview of ML Jobs, see
[ML Jobs in Data Clean Rooms](/user-guide/cleanrooms/ml-jobs).

#### Syntax

Copy code

```
RUN_ML_JOB_ACTION( <collaboration_name>, <ml_job_action_spec> )
```

#### Arguments

`collaboration_name`
:   Name of the collaboration that contains the running or completed ML Job.

`ml_job_action_spec`
:   An ML job action definition in YAML format as a string. Contains the following fields:

    - `api_version`: Must be `2.0.0`.
    - `spec_type`: Must be `ml_job_action`.
    - `job_id`: The job ID returned by [RUN](#label-dcr-collaboration-run-reference) when the ML Job was started.
    - `action`: The action to perform. Case-insensitive. See [Actions](#run_ml_job_action-actions) below.

#### Actions

The `action` field is case-insensitive. Valid actions are:

`get_status`
:   Returns the current execution status of the job. Possible values: `PENDING`, `RUNNING`,
    `DONE`, `FAILED`. Poll this action to know when the job completes.

`get_logs`
:   Returns the container’s stdout/stderr output. Use this to monitor progress, debug errors, or
    view script print statements. Only available if `allow_monitoring` is `true` in the code
    spec **and** the collaboration owner has not disabled `ALLOW_ML_JOBS_MONITORING`.

`get_result`
:   Returns the job’s return value after completion. For scripts that write to cleanroom tables
    rather than returning data directly, this returns NULL. Check `get_status` first to confirm
    the job is `DONE` before calling `get_result`.

#### Returns

Action-dependent result. `get_status` returns a status string; `get_logs` returns container
output as text; `get_result` returns the job’s return value or NULL.

#### Examples

Copy code

```
-- Check job status.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.RUN_ML_JOB_ACTION(
    'my_collaboration',
    $$
    api_version: 2.0.0
    spec_type: ml_job_action
    job_id: <job_id>
    action: get_status
    $$
);

-- Check container logs for progress.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.RUN_ML_JOB_ACTION(
    'my_collaboration',
    $$
    api_version: 2.0.0
    spec_type: ml_job_action
    job_id: <job_id>
    action: get_logs
    $$
);

-- Get the result once the job completes.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.RUN_ML_JOB_ACTION(
    'my_collaboration',
    $$
    api_version: 2.0.0
    spec_type: ml_job_action
    job_id: <job_id>
    action: get_result
    $$
);
```

Note

The collaboration owner can disable log access by setting the `ALLOW_ML_JOBS_MONITORING` configuration to `false`
using [SET\_CONFIGURATION](#label-dcr-collaboration-set-configuration-reference). It is `true` (enabled) by default. When disabled,
`get_logs` returns an error, but `get_status` and `get_result` still work.

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling one of the following procedures:

- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('RUN ML JOB ACTION', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`

---

### VIEW\_ACTIVITY\_HISTORY

Schema:
:   COLLABORATION

Returns a table of template-run activity records for a collaboration. What each caller can see depends on their activity and the resources they contribute to the collaboration. For a conceptual overview, see [Monitor analysis activity in collaborations](/user-guide/cleanrooms/activity-history).

Activity history is automatically available in every collaboration created after the feature release.

#### Syntax

Copy code

```
VIEW_ACTIVITY_HISTORY( <collaboration_name> )
```

#### Arguments

`collaboration_name`
:   Name of the collaboration to return activity for.

#### Returns

A table containing activity records that the caller is permitted to see.

The table includes the following columns:

- `ACTIVITY_ID`: Unique identifier for the activity record. Also added as a Query Tag into the underlying query so callers can correlate an entry with [account-level query history](https://docs.snowflake.com/en/sql-reference/account-usage/query_history).
- `ANALYSIS_RUNNER_ALIAS`: Alias of the collaborator that ran the analysis.
- `START_TS`: Timestamp when the run started.
- `TOTAL_DURATION`: Total run duration, in milliseconds.
- `STATUS`: `SUCCESS` or `ERROR`. For activation template runs, `SUCCESS` reflects only that the template query executed successfully - failures during the export of activation results are not surfaced.
- `FAILURE_REASON`: Populated when `STATUS` is `ERROR`. The analysis runner sees the full error message. Other accounts see a redacted message.
- `ACTIVITY_TYPE`: The type of activity. Currently always `RUN`.
- `ACTIVITY_INFO`: A `VARIANT` column whose contents depend on what the caller contributed to the collaboration. Possible sub-keys:
  - `data_offering_ids`: IDs of the data offerings referenced by the run. Visible if the caller provided data offerings.
  - `request_parameters.template_id`: ID of the template used.
  - `request_parameters.source_tables`: Tables passed to the `source_tables` argument of `RUN`. Visible if the caller provided the relevant data offerings.
  - `request_parameters.local_tables`: Tables passed to the `local_tables` argument of `RUN`. Visible only to the analysis runner.
  - `request_parameters.arguments`: Template arguments passed to `RUN`. Visible only to the analysis runner.
  - `request_parameters.activation_destination`: Activation destination for the run, if any.

#### Example

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.VIEW_ACTIVITY_HISTORY(
  $collaboration_name
);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling one of the following procedures:

- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('VIEW ACTIVITY HISTORY', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`

---

### VIEW\_ACTIVATIONS

Schema:
:   COLLABORATION

Shows the activation status of any analysis run that either you triggered to send to a collaborator, or activations that a collaborator triggered to send to you. Activation requests to send data to yourself are not listed.

For more information about activation, see [Implementing activation](/user-guide/cleanrooms/activation#label-dcr-collaboration-activating-results).

#### Syntax

Copy code

```
VIEW_ACTIVATIONS( <collaboration_name> )
```

#### Arguments

`collaboration_name`
:   Name of the collaboration.

#### Returns

A table containing details for each activation. The table includes the following columns:

- `updated_on`: Time when the status was last updated.
- `segment_name`: An arbitrary string assigned by the analysis runner to identify this activation. For more information, see [Activating query results](/user-guide/cleanrooms/activation).
- `batch_id`: Batch ID of this activation request. For more information, see [Viewing provider and consumer activation results](/user-guide/cleanrooms/v1/activation#label-cleanrooms-provider-consumer-view-results).
- `template_id`: Template used to produce this activation data.
- `shared_by`: The collaborator that ran the analysis.
- `shared_with`: The collaborator that should receive the analysis data.
- `status`: Status of the activation. The following values are supported:

  - `PENDING`: Activation was requested, but is waiting to be processed.
  - `REPLICATING`: Activation data is being replicated to the destination region.
  - `SHARED`: Activation data is ready to be processed. Call PROCESS\_ACTIVATION to send the results to your account.
  - `FAILED`: Activation processing failed. See information in the `details` column.
  - `PROCESSED`: Activation results have been sent to the account specified in the activation request.
- `details`: Failure details, if the activation failed.

#### Example

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.VIEW_ACTIVATIONS(
  $collaboration_name
);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling one of the following procedures:

- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('VIEW ACTIVATIONS', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('RUN', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`

---

### PROCESS\_ACTIVATION

Schema:
:   COLLABORATION

If the analysis runner is sending data to another collaborator’s account, that collaborator should call PROCESS\_ACTIVATION to import the activation data into their account. The collaborator should call
VIEW\_ACTIVATIONS and wait until the output shows that the activation status for a given segment is `SHARED` before calling PROCESS\_ACTIVATION.

For more information, see [Implementing activation](/user-guide/cleanrooms/activation#label-dcr-collaboration-activating-results).

#### Syntax

Copy code

```
PROCESS_ACTIVATION( <collaboration_name> [, <segment_name> | <array_of_batch_ids> ] )
```

#### Arguments

`collaboration_name`
:   Name of the collaboration.

`segment_name` *(Optional)*
:   String name of a specific activation segment to process.

`batch_ids` *(Optional)*
:   String array of batch IDs of activations to process. This value is returned by VIEW\_ACTIVATIONS. If not included, the request will process all pending
    activations in the designated collaboration for the caller.

#### Returns

The table name where the user can retrieve the results, and the segment name specified for the results. See [Implementing activation](/user-guide/cleanrooms/activation#label-dcr-collaboration-activating-results) to learn how to read results.

#### Example

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.PROCESS_ACTIVATION(
  $collaboration_name
);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling one of the following procedures:

- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('PROCESS ACTIVATION', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`

## Registry management procedures

This section contains procedures used to register objects. For more information:

- [Registries](/user-guide/cleanrooms/registries)
- [Adding resources to a collaboration](/user-guide/cleanrooms/overview#label-dcr-collaboration-add-resources)

### CREATE\_REGISTRY

Schema:
:   REGISTRY

Creates a custom registry to organize resources such as templates and data offerings. A custom registry can store resources of a single type, designated when you create the registry.

Use custom registries to group related resources separately from the default local registry. Add resources to this registry using the optional registry name parameter.

#### Syntax

Copy code

```
CREATE_REGISTRY( '<registry_name>', <registry_type> )
```

#### Arguments

`registry_name`
:   Name of the registry to create. Must be a unique name across all registries in the account.

`registry_type`
:   The type of resources this registry will contain. Supported values: `TEMPLATE`, `DATA OFFERING`.

#### Returns

A string success message.

#### Example

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.CREATE_REGISTRY(
  'my_custom_registry',
  'TEMPLATE'
);
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling the following procedure:

- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE REGISTRY', '{role name}')`

---

### VIEW\_REGISTRIES

Schema:
:   REGISTRY

Lists all registries that you have access to, including the default local registry and any custom registries.

#### Syntax

Copy code

```
VIEW_REGISTRIES()
```

#### Arguments

None.

#### Returns

A table with a row for each registry that you can access.

#### Example

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.VIEW_REGISTRIES();
```

#### Access requirements

If you’re not using the SAMOOHA\_APP\_ROLE role, you must use a role that was granted privileges by calling one of the following procedures:

- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('VIEW REGISTRIES', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE REGISTRY', '{role name}')`

For a custom registry to be visible to VIEW\_REGISTRIES, you must also have READ or REGISTER privileges, granted by one of the following procedure calls:

- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('READ', 'REGISTRY', '{registry name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('REGISTER', 'REGISTRY', '{registry name}', '{role name}')`

## Access management procedures

The SAMOOHA\_APP\_ROLE role grants access to all Data Clean Room Collaboration API procedures. However, if an administrator wants to grant more granular privileges to specific roles, you can create a role and grant it specific privileges with the procedures described in this section. Learn more about managing access to Collaboration API: [The Access Management Documentation](/user-guide/cleanrooms/manage-access).

The following procedures are used to manage fine-grained access to the Snowflake Data Clean Room Collaboration API:

- [GRANT\_PRIVILEGE\_ON\_OBJECT\_TO\_ROLE](#label-grant-privilege-on-object-to-role)
- [GRANT\_PRIVILEGE\_ON\_ACCOUNT\_TO\_ROLE](#label-dcr-grant-privilege-on-account-to-role)

### GRANT\_PRIVILEGE\_ON\_OBJECT\_TO\_ROLE

Schema:
:   ADMIN

Grants a specified role the privilege to call specific procedures on a specific object.

You can call this procedure multiple times to grant multiple
permissions to the same role. Run this procedure using the role that owns the object.

#### Syntax

Copy code

```
GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE(
  '<privilege>',
  '<object_type>',
  '<object_name>',
  '<account_role_name>'
);
```

#### Arguments

`'privilege'`
:   What permission this role should be granted. See the table below to learn which privileges are available for which objects.

`'object_type'`
:   The type of object that this role is being granted permissions on. Supported values:

    - `COLLABORATION`
    - `REGISTRY`

`'object_name'`
:   The ID of the object, as specified in the object’s specification.

`'account_role_name'`
:   The role being granted.

The following privilege and object type combinations are supported:

**Compound privileges**

The following compound privileges grant access to multiple procedures at once:

| Privilege | Object type | Procedures enabled |
| --- | --- | --- |
| `READ` | `COLLABORATION` | VIEW\_COLLABORATIONS, GET\_STATUS, GET\_CONFIGURATION, VIEW\_CODE\_SPECS, VIEW\_DATA\_OFFERINGS, VIEW\_UPDATE\_REQUESTS, VIEW\_TEMPLATES |
| `RUN` | `COLLABORATION` | RUN, VIEW\_ACTIVATIONS, VIEW\_COLLABORATIONS |
| `UPDATE` | `COLLABORATION` | EDIT, LINK\_LOCAL\_DATA\_OFFERING, UNLINK\_LOCAL\_DATA\_OFFERING, ADD\_TEMPLATE\_REQUEST, REMOVE\_TEMPLATE, APPROVE\_UPDATE\_REQUEST, REJECT\_UPDATE\_REQUEST, ENABLE\_TEMPLATE\_AUTO\_APPROVAL, DISABLE\_TEMPLATE\_AUTO\_APPROVAL, SET\_CONFIGURATION, VIEW\_UPDATE\_REQUESTS |
| `READ` | `REGISTRY` | View resources registered in a [custom registry](/user-guide/cleanrooms/registries). |
| `REGISTER` | `REGISTRY` | View or register resources such as templates and data offerings in a [custom registry](/user-guide/cleanrooms/registries). |

Expand

Show lessSee more

**Fine-grained privileges**

The following fine-grained privileges grant access to individual procedures on a specific collaboration:

| Privilege | Procedures enabled |
| --- | --- |
| `GET STATUS` | GET\_STATUS |
| `VIEW DATA OFFERINGS` | VIEW\_DATA\_OFFERINGS |
| `VIEW TEMPLATES` | VIEW\_TEMPLATES |
| `VIEW CODE SPECS` | VIEW\_CODE\_SPECS |
| `VIEW UPDATE REQUESTS` | VIEW\_UPDATE\_REQUESTS |
| `VIEW ACTIVATIONS` | VIEW\_ACTIVATIONS |
| `VIEW ACTIVITY HISTORY` | VIEW\_ACTIVITY\_HISTORY |
| `ADD TEMPLATE REQUEST` | ADD\_TEMPLATE\_REQUEST |
| `REMOVE TEMPLATE` | REMOVE\_TEMPLATE |
| `MANAGE UPDATE REQUEST` | APPROVE\_UPDATE\_REQUEST, REJECT\_UPDATE\_REQUEST |
| `MANAGE TEMPLATE AUTO APPROVAL` | ENABLE\_TEMPLATE\_AUTO\_APPROVAL, DISABLE\_TEMPLATE\_AUTO\_APPROVAL, GET\_CONFIGURATION, SET\_CONFIGURATION |
| `LINK LOCAL DATA OFFERINGS` | LINK\_LOCAL\_DATA\_OFFERING |
| `UNLINK LOCAL DATA OFFERINGS` | UNLINK\_LOCAL\_DATA\_OFFERING |
| `PROCESS ACTIVATION` | PROCESS\_ACTIVATION |

Expand

Show lessSee more

#### Returns

A table with a `MESSAGE` column containing a success message.

#### Example

This example creates a role for analysts to use to run analyses in a collaboration named `my_collaboration` and assigns it to a user.

Copy code

```
USE ROLE role_that_created_this_collaboration;

CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.ADMIN.GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE(
  'RUN',
  'COLLABORATION',
  $collaboration_name,
  'collaborator_analyst_role'
);
GRANT ROLE collaborator_analyst_role to USER alexander_hamilton;
```

#### Access requirements

You must use the same role that created the object to call GRANT\_PRIVILEGE\_ON\_OBJECT\_TO\_ROLE on that object.

- **For collaborations,** any role with CREATE COLLABORATION or JOIN COLLABORATION can call GRANT\_PRIVILEGE\_ON\_OBJECT\_TO\_ROLE on any collaboration.
- **For registries,** only the role that created the registry can call GRANT\_PRIVILEGE\_ON\_OBJECT\_TO\_ROLE on that registry.

---

### GRANT\_PRIVILEGE\_ON\_ACCOUNT\_TO\_ROLE

Schema:
:   ADMIN

Grants account-level privileges to a role. This procedure enables anyone using that role to call the procedures listed for that privilege.

#### Syntax

Copy code

```
GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE( '<privilege>', '<account_role_name>' );
```

#### Arguments

`'privilege'`
:   The privilege to grant this role. The following string values are supported:

    - `JOIN COLLABORATION`: Grants permission to run COLLABORATION.JOIN as well as the following procedures on the joined collaboration:

      - ADMIN.GRANT\_PRIVILEGE\_ON\_ACCOUNT\_TO\_ROLE
      - ADMIN.GRANT\_PRIVILEGE\_ON\_OBJECT\_TO\_ROLE
      - ADMIN.REVOKE\_PRIVILEGE\_ON\_OBJECT\_FROM\_ROLE
      - COLLABORATION.ADD\_TEMPLATE\_REQUEST
      - COLLABORATION.APPROVE\_UPDATE\_REQUEST
      - COLLABORATION.ENABLE\_TEMPLATE\_AUTO\_APPROVAL
      - COLLABORATION.DISABLE\_TEMPLATE\_AUTO\_APPROVAL
      - COLLABORATION.REMOVE\_TEMPLATE
      - COLLABORATION.GET\_STATUS
      - COLLABORATION.LEAVE
      - COLLABORATION.LINK\_DATA\_OFFERING
      - COLLABORATION.LINK\_LOCAL\_DATA\_OFFERING
      - COLLABORATION.PROCESS\_ACTIVATION
      - COLLABORATION.REJECT\_UPDATE\_REQUEST
      - COLLABORATION.REVIEW
      - COLLABORATION.RUN
      - COLLABORATION.TEARDOWN
      - COLLABORATION.UNLINK\_DATA\_OFFERING
      - COLLABORATION.UNLINK\_LOCAL\_DATA\_OFFERING
      - COLLABORATION.VIEW\_ACTIVATIONS
      - COLLABORATION.VIEW\_CODE\_SPECS
      - COLLABORATION.VIEW\_COLLABORATIONS
      - COLLABORATION.VIEW\_DATA\_OFFERINGS
      - COLLABORATION.VIEW\_TEMPLATES
      - COLLABORATION.VIEW\_UPDATE\_REQUESTS
      - REGISTRY.VIEW\_REGISTRIES
      - REGISTRY.VIEW\_REGISTERED\_CODE\_SPECS
      - REGISTRY.VIEW\_REGISTERED\_DATA\_OFFERINGS
      - REGISTRY.VIEW\_REGISTERED\_TEMPLATES

      This privilege requires the following account-level privileges to be granted to the role manually:

      - APPLY ROW ACCESS POLICY ON ACCOUNT
      - CREATE APPLICATION ON ACCOUNT
      - CREATE DATABASE ON ACCOUNT
      - CREATE LISTING ON ACCOUNT
      - CREATE SHARE ON ACCOUNT
      - IMPORT SHARE ON ACCOUNT
      - MANAGE SHARE TARGET ON ACCOUNT
    - `CREATE COLLABORATION`: Grants permission to run COLLABORATION.INITIALIZE, plus all procedures allowed by `JOIN COLLABORATION`
      for the joined collaboration. Requires the following account-level privileges to be granted manually to the role:

      - APPLY ROW ACCESS POLICY
      - CREATE APPLICATION
      - CREATE DATABASE
      - CREATE LISTING
      - CREATE SHARE
      - IMPORT SHARE
      - MANAGE SHARE TARGET
      - EXECUTE TASK (if using auto-join in the INITIALIZE procedure)
    - `VIEW COLLABORATIONS`: Grants permission to run COLLABORATION.VIEW\_COLLABORATIONS. Requires the following privileges to be granted manually to the role:

      - IMPORT SHARE ON ACCOUNT
    - `REGISTER DATA OFFERING`: Grants permission to run REGISTRY.REGISTER\_DATA\_OFFERING and REGISTRY.UNREGISTER\_DATA\_OFFERING. This permission is required for any analysis runner to join a collaboration that implements activation.
    - `VIEW REGISTERED DATA OFFERINGS`: Grants permission to run REGISTRY.VIEW\_REGISTERED\_DATA\_OFFERINGS.
    - `REGISTER TEMPLATE`: Grants permission to run REGISTRY.REGISTER\_TEMPLATE and REGISTRY.UNREGISTER\_TEMPLATE.
    - `VIEW REGISTERED TEMPLATES`: Grants permission to run REGISTRY.VIEW\_REGISTERED\_TEMPLATES.
    - `REGISTER CODE SPEC`: Grants permission to run REGISTRY.REGISTER\_CODE\_SPEC.
    - `VIEW REGISTERED CODE SPECS`: Grants permission to run REGISTRY.VIEW\_REGISTERED\_CODE\_SPECS.
    - `CREATE REGISTRY`: Grants permission to run REGISTRY.CREATE\_REGISTRY, REGISTRY.VIEW\_REGISTRIES, and also the ability to read from custom registries that you have created.
    - `REVIEW COLLABORATION`: Grants permission to run COLLABORATION.REVIEW.
    - `VIEW REGISTRIES`: Grants permission to run REGISTRY.VIEW\_REGISTRIES.
    - `VIEW DCR STATUS`: Grants permission to view the overall status of Data Clean Rooms in the account.

`'account_role_name'`
:   The name of an account-level role.

#### Returns

A table with a `MESSAGE` column containing a success message.

#### Example

Copy code

```
USE ROLE ACCOUNTADMIN;
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.ADMIN.GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE(
  'REGISTER DATA OFFERING',
  'COLLABORATOR_ANALYST_ROLE'
);
```

#### Access requirements

You need the ACCOUNTADMIN role, or a role with the MANAGE GRANTS global privilege, to run this procedure.
