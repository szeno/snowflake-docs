# Privileges required to create and use a Streamlit app

Within Streamlit in Snowflake, a Streamlit app is a securable object that adheres to the
[Snowflake access control framework](/user-guide/security-access-control-overview).
Streamlit apps use a permission model that is based on owner’s rights. For more information, see [Understanding owner’s rights and Streamlit in Snowflake apps](/developer-guide/streamlit/object-management/owners-rights).
You can also configure a container-runtime app to use restricted caller’s rights (Preview). For more information, see
[Restricted caller’s rights and Streamlit in Snowflake](/developer-guide/streamlit/features/restricted-callers-rights).

The app owner and the owner of the schema containing the Streamlit app can determine which roles have
permission to use the app. Users can interact with the app and can see anything displayed by
the Streamlit app. Users have the same view of the app as the owner does except that they can’t access
the edit mode.

For more information, see [Share a Streamlit app](/developer-guide/streamlit/app-development/managing-your-app#label-streamlit-sharing).

## Privileges required to create a Streamlit app

To create a Streamlit app, if your role does not own the objects in the following table,
then your role must have the listed
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) on those objects:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE STREAMLIT | Schema where you create the Streamlit object |  |
| READ | Stage from which you copy the Streamlit app source files |  |
| USAGE | Warehouse used by the Streamlit app |  |
| USAGE | Compute pool used by the Streamlit app | This privilege is only required if your app uses a container runtime. |
| USAGE | External access integrations used by the Streamlit app | This privilege is only required if your app uses external access integrations. For container runtimes, this privilege is required to install packages from external package indexes like PyPI. |
| USAGE | Secrets used by the Streamlit app | This privilege is only required if your app uses secrets and only applies to warehouse runtimes. |
| CREATE STAGE | Schema where you create the Streamlit object | This privilege is only required to create Streamlit objects with the ROOT\_LOCATION parameter. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

Use the [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) command to grant these privileges to a role. The following
example shows how to grant the necessary privileges to create container-runtime apps:

Copy code

```
GRANT USAGE ON DATABASE streamlit_db TO ROLE streamlit_developer;
GRANT USAGE ON SCHEMA streamlit_db.apps TO ROLE streamlit_developer;
GRANT CREATE STREAMLIT ON SCHEMA streamlit_db.apps TO ROLE streamlit_developer;
GRANT USAGE ON COMPUTE_POOL streamlit_compute_pool TO ROLE streamlit_developer;
GRANT USAGE ON INTEGRATION python_package_index TO ROLE streamlit_developer;
GRANT USAGE ON WAREHOUSE streamlit_wh TO ROLE streamlit_developer;
```

If a future grant is defined on the database or schema, ensure that the user creates the Streamlit app using the role defined
in the future grant.

## Privileges required to view a Streamlit app

To view a Streamlit app, you must have a Snowflake account and be signed in. Additionally,
you must use a role that is granted the USAGE privilege on the following objects:

- The database that contains the Streamlit app
- The schema that contains the Streamlit app
- The Streamlit app

In most cases, when the app owner shares a Streamlit app with another role, the USAGE privilege is
automatically granted to the new role. However, if a Streamlit app is created in a schema with
MANAGED ACCESS, the USAGE privilege must be manually granted to the new role.

The schema owner or a user with the role with the MANAGE GRANTS privilege must grant the USAGE
privilege using the [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) command as shown in this example:

Copy code

```
GRANT USAGE ON DATABASE streamlit_db TO ROLE streamlit_viewer;
GRANT USAGE ON SCHEMA streamlit_db.streamlit_schema TO ROLE streamlit_viewer;
GRANT USAGE ON STREAMLIT streamlit_db.streamlit_schema.streamlit_app TO ROLE streamlit_viewer;
```

The schema owner or a user with the role with the MANAGE GRANTS privilege can grant the USAGE
privilege to view all future Streamlit apps created in the schema as shown in this example:

Copy code

```
GRANT USAGE ON FUTURE STREAMLITS IN SCHEMA streamlit_db.streamlit_schema TO ROLE streamlit_viewer;
```
