# Create the manifest file for an app

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how to create the manifest file for an app.

## About the manifest file

The manifest file contains information that the application package
requires to create and manage a Snowflake Native App. This includes the location
of the setup script, version definitions, and configuration information
for the app.

The manifest file has the following requirements:

- The name of the manifest file must be `manifest.yml`.
- The manifest file must be uploaded to a named stage so that it is
  accessible to the application package.
- The manifest file must exist at the root of the directory structure on
  the named stage where other application files are stored.

## Version 1 and version 2 of the manifest file

Snowflake Native Apps supports two versions of the manifest file. The version is
specified using the `manifest_version` field.

`manifest_version: 1`
:   This version of the manifest file supports the current and
    legacy functionality of Snowflake Native Apps.

`manifest_version: 2`
:   This version of the manifest file provides support for additional
    features, including automated granting of privileges.

## Security considerations when using version 2 of the manifest file

When using version 2 of the manifest file, consider the following security implications:

When a provider configures an app to use
`manifest_version: 2` in the manifest file, automated granting of
privileges is enabled. By default this allows Snowflake to automatically
grant certain privileges to the app. For information on the privileges
that can be automatically granted to the app, see
[Privileges granted by automated granting of privileges](/developer-guide/native-apps/requesting-auto-privs#label-native-apps-auto-privs-supported-privs).

During installation, Snowsight displays a notification about
the privileges requested by the app. When a consumer installs an app
that uses automated granting of privileges, they agree that the app may
be granted these privileges during upgrades without requiring additional
consent.

Consumers can create feature policies that restrict the objects an app
can create. For more information on creating feature policies, see
[Use feature policies to limit the objects an app can create](/developer-guide/native-apps/ui-consumer-feature-policies).

## Specify the privileges required by an app with containers

Like other apps, the `privileges` field of the manifest file
specifies the privileges that an app with containers requests from
consumers.

The following privileges are specific to an app with containers:

- CREATE COMPUTE POOL

  This privilege is required to allow the app to create a compute pool in the consumer account. It is not required if the consumer creates
  the compute pool manually.
- BIND SERVICE ENDPOINT

  This privilege is required to allow an endpoint to be accessible outside of Snowflake.

The following example shows how to add these privileges to the `privileges` block:

Copy code

```
privileges:
- CREATE COMPUTE POOL:
  description: 'Required to allow the app to create a compute pool in the consumer account.'
- BIND SERVICE ENDPOINT:
  description: 'Required to allow endpoints to be externally accessible.'
```

## Specify the container images used by an app with containers

To specify the location of the container images used by the app with
containers, add the `images` property to the `artifacts.container_services` block.

You must include an entry for each image. The path specified includes
the name of the database, schema, and image repository. This path has
the following form:

Copy code

```
/<database>/<schema>/<image_repository>/<image_name>:tag
```

The following example shows how to specify the `images` property:

Copy code

```
artifacts
...
  container_services
    ...
    images
      - /dev_db/dev_schema/dev_repo/image1
      - /dev_db/dev_schema/dev_repo/image2
```

## Specify the user interface endpoint for an app with containers

To specify the endpoint for the user interface of the app with
containers, add the `default_web_endpoint` property to the
`artifacts` block.

The `default_web_endpoint` property is optional. If this property
is specified, the endpoint must also be defined in the service
specification file.

Note

Only one of the `default_web_endpoint` and `default_streamlit` can be specified.

This entry in the manifest file has two additional properties:

- `service`
  :   Specifies the name of the service of the user interface.
- `endpoint`
  :   Specifies the name of the endpoint.

The following example shows how to specify the `default_web_endpoint` property.

Copy code

```
default_web_endpoint:
  service: ux_schema.ux_service
  endpoint: ui
```

## Example manifest files

The following examples show typical manifest files for different types of use cases.

### Example manifest file for using automated granting of privileges

The following manifest file shows how to configure an app to use
automated granting of privileges. This example uses version 2 of the
manifest file. The `privileges` block specifies the privileges that the app requires.

Copy code

```
manifest_version: 2
version:
  name: v1
artifacts:
  readme: readme.md
  setup_script: setup.sql
privileges:
  - CREATE TABLE:
    description: "Allows the app to create tables in the consumer account"
  - CREATE WAREHOUSE:
    description: "Allows the app to create warehouses in the consumer account"
```

When the app is installed, Snowflake automatically grants the CREATE TABLE and CREATE WAREHOUSE privileges to the app.

### Example manifest file files for an app with containers

Snowflake Native Apps supports entries in the manifest file that are specific to
an app with containers. The following example manifest file
shows a typical manifest file for an app with containers:

Copy code

```
manifest_version: 2
version:
  name: v1
artifacts:
  readme: readme.md
  setup_script: setup.sql
  container_services:
    images:
      - /dev_db/dev_schema/dev_repo/image1
      - /dev_db/dev_schema/dev_repo/image2
  default_web_endpoint:
    service: ux_schema.ux_service
    endpoint: ui
privileges:
 - CREATE COMPUTE POOL:
   description: "..."
 - BIND SERVICE ENDPOINT:
   description: "...”
```
