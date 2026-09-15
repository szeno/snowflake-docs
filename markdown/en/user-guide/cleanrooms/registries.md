# Registries

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

## Overview

To use a resource such as a template or data offering in a collaboration, you must first register it in a registry. A registry is an account-level container designed to store these resources. Once registered, any resource in the registry can be linked to a collaboration by any user in your account who has both access to the registry and the necessary linking permissions for that specific collaboration. Notably, registries are independent of specific collaborations; a registered resource can be linked to any number of collaborations, or none at all, within that account.

Each Snowflake account supports a default registry. You can create additional custom registries for your account. Custom registries are a
good way to group and manage access to your resources. For example, you could create a custom registry for sales data and another for
expenditure data, then grant access to these registries to the appropriate users via [DCR privileges and custom RBAC roles](/user-guide/cleanrooms/manage-access).

## Registry rules

Here are the main rules about registries:

- Registries are account-level objects. Users can see and access only registries in their own account. However, when a resource in a
  registry is linked into a collaboration, the resource is visible to anyone who can access it according to the spec. Access to the containing registry isn’t required.
- Each custom registry supports a single resource type (template, data offering, and so on). The resource type is specified when you create the
  registry. The default registry supports any resource type.
- There is no limit to how many custom registries you can create in an account.
- When you register a resource, you can use the optional registry name parameter to specify a custom registry. If you don’t specify a
  custom registry, the resource is registered in the default registry for the account.
- You can remove a template or data offering that you registered by calling [UNREGISTER\_TEMPLATE](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-unregister-template-reference)
  or [UNREGISTER\_DATA\_OFFERING](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-unregister-data-offering-reference), as long as the resource isn’t currently linked to a
  collaboration. Code specs can’t be unregistered; to update code, register a new version instead.
- All users have access to the default registry in an account. Custom registries, however, are initially private to the creator, and
  additional users must be granted access explicitly by calling `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE`.
- An account can have multiple registries that store the same resource type.
- Registries don’t have a maximum number of resources.
- A resource must have a unique name across all registries in that account for resources of that type. For example, you can have a template
  named `sales` and a data offering named `sales` in the same account, but not two templates named `sales` in either the same or
  different registries in the same account. The resource name is defined as the highest-level `name` value in the spec.
- If two different accounts link resources with the same name and type to a collaboration, that is allowed. The collaboration specification will show
  identically named resources, but the system will know which resource is intended — the resource with that name is used from the account
  that linked the resource to the collaboration.

## Example

This example creates a custom registry, registers a template in it, and grants read access to that registry to a new role. Users
with that role can link templates in that registry into a collaboration.

Copy code

```
-- Create a custom registry that can hold templates.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.CREATE_REGISTRY(
  'SALES',
  'TEMPLATE'
);

CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.REGISTER_TEMPLATE(
'SALES',
$$
api_version: 2.0.0
spec_type: template
name: alice_only_template
version: v1
type: sql_analysis
description: Joins two tables on hashed email and counts matches grouped by status.
template:
  SELECT t1.status, COUNT(*)
    FROM IDENTIFIER( {{ source_table[0] }} ) AS t1
    JOIN IDENTIFIER( {{ source_table[1] }} ) AS t2
    ON t1.hashed_email_b64_encoded = t2.hashed_email_b64_encoded
    GROUP BY t1.status;
$$
);

-- Create a role and grant it access to the registry.
CREATE ROLE MARKETING_USERS;
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.ADMIN.GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE(
  'READ',
  'REGISTRY',
  'SALES',
  'MARKETING_USERS'
);

-- Grant access to the registry for a user by assigning the role.
GRANT ROLE MARKETING_USERS to USER willy_loman;
```
