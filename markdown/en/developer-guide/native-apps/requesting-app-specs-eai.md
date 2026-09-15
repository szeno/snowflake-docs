# Request external access

This topic describes how to configure a Snowflake Native App to use app specifications
to request access to an external access integration (EAI) in the consumer
account. An EAI allows an app to connect to an endpoint that is external to
Snowflake.

## Access to external endpoints from an app

To access an external endpoint, an app must create a network rule and an
EAI, which uses network rules to restrict access to specific
external network locations. Network rules define the external endpoints that an
app can access.

To configure an app to use an EAI, follow these steps:

- To request privileges from the consumer to create an EAI, use
  [automated granting of privileges](/developer-guide/native-apps/requesting-auto-privs).
- Add an EAI to an app.
- Use [application specifications](/developer-guide/native-apps/requesting-app-specs) to request permissions from the consumer to connect to
  an external endpoint.

Note

A single app specification applies to all of the EAIs created by the app.
Providers can create multiple app specifications for an app; however, this is not required.

## App specification workflow for an EAI

1. Providers configure [automated granting of privileges](/developer-guide/native-apps/requesting-auto-privs) for the app.
   This allows consumers to give permission to an app to create the EAI.

   > Note
   >
   > App specifications require that `manifest_version: 2` be set in the manifest file.
2. Providers add the
   [CREATE EXTERNAL ACCESS INTEGRATION privilege](#label-native-apps-app-spec-add-eai-priv) to the
   manifest file.
3. Providers add SQL statements to the setup script to create the following objects:

   - [Network rule](/sql-reference/sql/create-network-rule)
   - [External access integration](/sql-reference/sql/create-external-access-integration)
   - [App specification](/sql-reference/sql/alter-application-set-app-spec)

   The setup script creates the app specification and other objects when the app is installed or
   upgraded or at runtime.
4. When configuring the app, consumers review and approve the host ports and external services. For more
   information on how consumers view and approve app specifications, see [Approve app specifications](/developer-guide/native-apps/ui-consumer-app-spec).

## App specification definition for an EAI

The app specification definition for an EAI contains the following entries:

- `HOST_PORTS`: A list of host ports defined in the network rule that the app requires.
- `PRIVATE_HOST_PORTS`: A list of private host ports that allow private connectivity to
  resources outside Snowflake.

Note

Endpoints and ports mentioned in the application specification and those referenced in the [network rule value list](/sql-reference/sql/create-network-rule) must match.

## Set the version of the manifest file

To enable automated granting of privileges for an app, set the version at the beginning of the
manifest file as shown in the following example:

Copy code

```
manifest_version: 2
```

## Add the CREATE EXTERNAL ACCESS INTEGRATION privilege to the manifest file

The CREATE EXTERNAL ACCESS INTEGRATION privilege allows the app to create an external
access integration during installation or upgrade.

- To configure an app to request the
  CREATE EXTERNAL ACCESS INTEGRATION privilege, add the following code to the
  `privileges` section of the manifest file:

  Copy code

  ```
  manifest_version: 2
  ...
  privileges:
    - CREATE EXTERNAL ACCESS INTEGRATION:
     description: "Allows the app to create an EAI to connect to an external service."
  ...
  ```

If you set the `manifest_version` to 2 in the manifest file, Snowflake
automatically grants the CREATE EXTERNAL ACCESS INTEGRATION privilege to the app
during installation or upgrade.

## Add a network rule and an EAI to the setup script

EAIs are the Snowflake objects that enable access to specific external network
locations and contain a list of network rules that specify the external
locations that an app can access.

- To create a network rule for an app, add the
  [CREATE NETWORK RULE](/sql-reference/sql/create-network-rule) command to the setup script as
  shown in the following example:

  Copy code

  ```
  CREATE OR REPLACE NETWORK RULE setup.my_network_rule
  TYPE = HOST_PORT
  VALUE_LIST = ( 'example.com' )
  MODE = EGRESS;
  ```

The `HOST_PORT` and `VALUE_LIST` properties indicate that the network rule must point to a
valid domain, port, or range of ports. When an app is installed or upgraded,
consumers grant permission for the app to use these domains or ports.

## Create an EAI

- To create an EAI for an app, add the
  [CREATE EXTERNAL ACCESS INTEGRATION](/sql-reference/sql/create-external-access-integration) command to the
  setup script, as shown in the following example:

  Copy code

  ```
  CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION my_app_prefix_eai_rule
    ALLOWED_NETWORK_RULES = (setup.my_network_rule)
    ENABLED = TRUE;
  ```

Note

This command creates an EAI in the consumer account. However, it is not usable
until the consumer approves the app specifications that allow external access
to the requested host ports.

For more information, see [Approve app specifications](/developer-guide/native-apps/ui-consumer-app-spec).

## Creating a user-defined function to access the external endpoint

After the EAI is created, the setup script can create user-defined
functions and stored procedures that use it to connect to the endpoints defined in the
network rule.

The following example shows a user-defined function that uses the
`my_app_prefix_eai_rule` EAI:

Copy code

```
CREATE OR REPLACE FUNCTION setup.EXTERNAL_ACCESS_UDF(hostname STRING)
  RETURNS STRING
  LANGUAGE JAVA
  HANDLER='TestHostNameLookup.compute'
  EXTERNAL_ACCESS_INTEGRATIONS = (my_app_prefix_eai_rule)
  AS
  '
      import java.net.InetAddress;
      import java.net.UnknownHostException;
      class TestHostNameLookup {{
          public static String compute(String hostname) throws Exception {{
              InetAddress addr = null;
              try {
                  addr = InetAddress.getByName(hostname);
              } catch(UnknownHostException ex) {
                  return "Hostname lookup failed";
              }
              return "Hostname lookup successful";
          }
      }
';
GRANT USAGE ON FUNCTION setup.EXTERNAL_ACCESS_UDF(STRING)
  TO APPLICATION ROLE app_public;
```

This function sets the value of the EXTERNAL\_ACCESS\_INTEGRATIONS to the EAI
created previously.

This function uses the `InetAddress` Java package to look up the hostname passed to
the procedure. The hostname provided must match one of the values provided in the `VALUE_LIST`
property of the network rules used by the EAI.

## Creating an app specification for an EAI

The following example shows how to create an app specification for an EAI:

Copy code

```
ALTER APPLICATION SET SPECIFICATION eai_app_spec
  TYPE = EXTERNAL_ACCESS
  LABEL = 'Connection to an external API'
  DESCRIPTION = 'Access an API that exists outside Snowflake'
  HOST_PORTS = ('example.com')
```

This command creates an app specification named `eai_app_spec`.

## Approve the app specification in the consumer account

After the provider configures the app to create the network rule, EAI, and
app specification, consumers can view the app specification and approve or
decline it as appropriate when configuring the app. For more information, see
[Approve app specifications](/developer-guide/native-apps/ui-consumer-app-spec).
