# Set up key-pair authentication for Openflow - BYOC Deployments

Feature — Generally Available

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

This topic describes how to set up a Snowflake service user for key-pair authentication with an
Openflow connector.

[Snowflake Managed Token](/user-guide/data-integration/openflow/about#label-openflow-snowflake-managed-token)
(the `SNOWFLAKE_MANAGED` authentication strategy) is the default and recommended way for a connector
to authenticate to Snowflake, for both Openflow - Snowflake Deployments and Openflow - BYOC Deployments. It requires no service
user, no key pair, and no secrets management of any kind. The runtime’s execute-as role handles
authentication automatically.

Use this topic only if you’re deploying a connector in Openflow - BYOC Deployments and you’ve set the
connector’s **Snowflake Authentication Strategy** parameter to `KEY_PAIR` instead. Under `KEY_PAIR`,
you grant the runtime’s execute-as role to a Snowflake service user, rather than letting the runtime
reach that role automatically through a managed token.

## Create a Snowflake service user

Key-pair authentication is available only for Openflow - BYOC Deployments, and is not required for the
default `SNOWFLAKE_MANAGED` authentication strategy. Skip this section unless you set the
connector’s **Snowflake Authentication Strategy** parameter to `KEY_PAIR`.

1. Create a Snowflake user with the type as [SERVICE](/sql-reference/sql/create-user#label-user-type-property), and grant it the
   execute-as role you already configured for this runtime, so the service user has the same
   privileges the runtime would otherwise use automatically under `SNOWFLAKE_MANAGED`:

   Copy code

   ```
   CREATE USER <username> TYPE=SERVICE COMMENT='Service user for automated access of Openflow';
   GRANT ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL TO USER <username>;
   ```
2. Create a pair of secure keys (public and private). Store the private key for the user in a file
   to supply to the connector’s configuration. Assign the public key to the Snowflake service user:

   Copy code

   ```
   ALTER USER <username> SET RSA_PUBLIC_KEY = '<public_key>';
   ```

   For more information, see [Key-pair authentication and key-pair rotation](/user-guide/key-pair-auth).
3. Store the private key so the connector can reference it, using the method that matches your
   connector’s generation (gen 1 or gen 2):

   **For a gen 2 connector**, create a Snowflake secret to hold the private key, grant the execute-as
   role `READ` on it, and reference the secret directly in the connector’s configuration:

   Copy code

   ```
   CREATE SECRET <secret_name>
     TYPE = GENERIC_STRING
     SECRET_STRING = '<private_key>';

   GRANT READ ON SECRET <secret_name> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   ```

   **For a gen 1 connector**, configure a secrets manager supported by Openflow, for example, AWS,
   Azure, or HashiCorp, and store the public and private keys in the secret store:

   1. Once the secrets manager is configured, determine how you will authenticate to it. On AWS, use
      the EC2 instance role associated with Openflow, so that no other secrets need to be persisted.
   2. In Openflow, configure a Parameter Provider associated with this secrets manager, from the hamburger menu in the upper right.
      Navigate to **Controller Settings** » **Parameter Provider** and then fetch your parameter values.

   At this point, all credentials can be referenced with the associated parameter paths and no sensitive values need to be persisted within Openflow.

   Note

   You can also paste the private key value directly into the parameter context instead of using a
   secrets manager, but you’re then responsible for safeguarding the private key according to the
   security policies of your organization.

When using `KEY_PAIR`, you must also set the connector’s **Snowflake Account Identifier** and
**Snowflake Connection Strategy** parameters. Both are left blank or ignored under
`SNOWFLAKE_MANAGED`.

## Next steps

Return to your connector’s setup page to continue configuring the connector’s parameters.
