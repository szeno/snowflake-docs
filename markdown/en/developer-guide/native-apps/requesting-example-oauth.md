# Example - External access using OAuth and references

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic provides an example that describes how to use references to allow providers to grant access to
an endpoint that is external to Snowflake. This example uses a OAuth2 secret and an external access
integration to allow access.

Important

This example shows the manual method using references where consumers must create integrations
themselves. For new apps, Snowflake recommends using [automated granting of privileges](/developer-guide/native-apps/requesting-auto-privs)
with [app specifications](/developer-guide/native-apps/requesting-app-specs) instead. See [Request external access](/developer-guide/native-apps/requesting-app-specs-eai)
for external access integrations and [Request OAuth connection](/developer-guide/native-apps/requesting-app-specs-sec-integ) for security integrations.

## Add references to the manifest file

To enable access to an external endpoint using OAuth, a provider can add the following entries in the manifest file:

- EXTERNAL ACCESS INTEGRATION reference with the USAGE privilege
- SECRET reference with the READ privilege

The following example manifest file shows how to define these references:

Copy code

```
manifest_version: 1
configuration:
  log_level: warn
  trace_level: off
...
references:
  - consumer_secret:
      label: "Consumer's Secret"
      description: "Needed to authenticate with xyz.com"
      privileges:
        - READ
      object_type: SECRET
      register_callback: config.register_my_secret
      configuration_callback: config.get_config_for_ref
  - consumer_external_access:
      label: "Default External Access Integration"
      description: "This is required to access xyz.com"
      privileges:
        - USAGE
      object_type: EXTERNAL ACCESS INTEGRATION
      register_callback: config.register_reference
      configuration_callback: config.get_config_for_ref
      required_at_setup: true
```

Note

These references cannot have the `multi_valued` property set to true.

References to secrets and external access objects also require a `configuration_callback` function
in the setup script. See [Add the configuration\_callback function to the setup script](#label-native-apps-refs-example-setup) for more information.

## Add the configuration\_callback function to the setup script

After adding references for the secret and external access integration, you must add the
`configuration_callback` function to the setup script. To create an external access integration or
secret, the application must be able to determine values for host port, secret type, the authorization
and token endpoint for OAuth, etc. The `configuration_callback` provides this information from
the consumer account to the application.

Snowsight runs this callback procedure to populate the configuration dialog that prompts the
user to configure the objects. The procedure needs to be granted to an app role for execution.

Note

The configuration\_callback is only supported for external access integration and secret
objects.

The callback function has the following requirements:

- The callback function must accept an argument containing a reference name. This allows the same
  callback function to handle multiple references.
- The callback function must return a well-formed JSON object. The JSON object contains the following
  properties:
  - `type`

    Indicates the type of message. Valid values are:

    - `CONFIGURATION`: Returns a payload with the configuration values for the object based on object type.
    - `ERROR`: Returns an error with the associated message that is displayed in Snowsight.
  - `payload`

    Contains the content of the response based on the value of the `type` property and the object type being configured.

The signature for the configuration callback is:

Copy code

```
CREATE OR REPLACE PROCEDURE configuration_callback_name(ref_name string)
RETURNS STRING
language <language>
as
$$
  ...
$$
```

Within the setup script, you must grant the USAGE privilege to the application roles that are used
for configuring the app so that they have permission to call the stored procedure. The following
example shows how to grant the USAGE privilege on a stored procedure:

Copy code

```
GRANT USAGE ON PROCEDURE configuration_callback_name(string)
  TO APPLICATION ROLE app_role;
```

The callback function returns a JSON object. See [JSON format for the configuration callback response](/developer-guide/native-apps/requesting-refs#label-native-apps-reference-json-format) for
more information.

The following example shows a typical callback function for handling external access and secret references.

This function does the following:

- For a reference to an external access integration, the procedure returns a JSON object containing the
  required configuration information. See [JSON format for external access integration](/developer-guide/native-apps/requesting-refs#label-native-apps-reference-json-format-eai) for more
  information.
- For a reference to a secret, the procedure returns a JSON object containing a secret configuration of
  type OAuth2. See [JSON format for secret references](/developer-guide/native-apps/requesting-refs#label-native-apps-reference-json-format-secret) for more information.

Copy code

```
  CREATE OR REPLACE PROCEDURE config.get_config_for_ref(ref_name STRING)
    RETURNS STRING
    LANGUAGE SQL
    AS
    $$
    BEGIN
      CASE (ref_name)
        WHEN 'CONSUMER_EXTERNAL_ACCESS' THEN
          RETURN '{
            "type": "CONFIGURATION",
            "payload":{
              "host_ports":["google.com"],
              "allowed_secrets" : "LIST",
              "secret_references":["CONSUMER_SECRET"]}}';
        WHEN 'CONSUMER_SECRET' THEN
          RETURN '{
            "type": "CONFIGURATION",
            "payload":{
              "type" : "OAUTH2",
              "security_integration": {
                "oauth_scopes": ["https://www.googleapis.com/auth/analytics.readonly"],
                "oauth_token_endpoint": "https://oauth2.googleapis.com/token",
                "oauth_authorization_endpoint":
                    "https://accounts.google.com/o/oauth2/auth"}}}';
  END CASE;
  RETURN '';
  END;
  $$;

GRANT USAGE ON PROCEDURE config.get_config_for_ref(string)
  TO APPLICATION ROLE app_admin;
```

## Using the Python Permission SDK for secrets and external access integrations

Python Permission SDK supports secret and external access integration objects.
However, the behavior is slightly different for these objects.

When a provider calls `permission.request_reference()`
and passes the name of a reference with an `object_type` value of `SECRET` or
`EXTERNAL ACCESS INTEGRATION`, Snowsight automatically performs
the following:

- Calls the `configuration_callback` function in the setup script.
- Validates the values returned by the `configuration_callback` function.
- Displays the configuration dialog to the consumer.

Note

If a provider configures an external access integration with the
`payload.allow_secrets` property set to `LIST`, it is not necessary to
make a separate call to request a reference for the secret. The secret configuration
is implicitly included as part of the external access integration configuration.
