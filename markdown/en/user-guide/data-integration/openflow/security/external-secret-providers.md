# Use external secret providers with Openflow

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Openflow can expose string secrets from AWS Secrets Manager, Azure Key Vault, or Google Cloud Secret
Manager as parameters that gen 2 and gen 1 connectors can consume.

Before you configure Openflow, set up and verify an external secret provider in Snowflake:

- [AWS Secrets Manager](/user-guide/external-secret-providers-aws)
- [Azure Key Vault](/user-guide/external-secret-providers-azure)
- [Google Cloud Secret Manager](/user-guide/external-secret-providers-gcp)

For information about how external secret providers work, their access model, and the SQL functions
that list and fetch secrets, see [External secret providers](/user-guide/external-secret-providers).

## Grant Openflow access to an integration

Grant `USAGE` on each external secret provider integration to the
[execute-as role](/user-guide/data-integration/openflow/setup-openflow-spcs-create-rr#label-create-runtime-role):

Copy code

```
GRANT USAGE ON INTEGRATION MY_EXTERNAL_SECRET_PROVIDER_INTEGRATION
  TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
```

Openflow automatically discovers the integrations that are visible to this role.

## Use external secrets in connectors

External secrets become Openflow parameters through the Snowflake Parameter Provider. The workflow
differs by [Openflow connector generation](/user-guide/data-integration/openflow/gen2/openflow-generations).

### Gen 2 connectors

When you configure a connector property that accepts a secret, the Openflow UI displays the resolved
secrets in a dropdown. Select the expected secret for the property.

### Gen 1 connectors

The Snowflake Parameter Provider organizes the parameters created from each external secret into a
parameter group. When you run **Fetch**, each parameter group becomes a generated Parameter Context.
To make the parameters available to a gen 1 connector, configure Parameter Context inheritance on
the connector’s process group:

1. In the Runtime UI, open **Controller Settings** > **Parameter Providers** in the top-right menu.
2. On the **Snowflake Parameter Provider**, open the three-dot menu and select **Fetch**.
3. Go back to the canvas.
4. Right-click on the process group for the gen 1 connector, go into Configure, and configure its Parameter Context inheritance.
5. Add the generated Parameter Context for the required external secret as an inherited Parameter
   Context.

The **Fetch** action creates or updates the Parameter Contexts that correspond to the external
secrets. Repeat **Fetch** after you add or rotate external secrets when you need refreshed values.

## Parameter mapping

This mapping determines the generated Parameter Context and parameter names for gen 1 connectors.

Each external secret maps as follows:

- **Group name**: `EXTERNAL_<integration_name>.<secret_name>`.
- **Plaintext value**: One parameter whose name is the secret name.
- **JSON object value**: One string parameter for each scalar, non-null top-level property.
- **Not exposed as parameters**: Nested objects, arrays, and null properties.

Don’t use `EXTERNAL_` as the prefix of a Snowflake database name where you add native Snowflake Secrets.
The provider groups native Snowflake secrets separately by using `<database_name>.<schema_name>`. The
`EXTERNAL_` prefix is reserved for external secret parameter groups.

### Plaintext example

For a secret named `my_api_token` in an integration named `my_secrets_int`, the Snowflake Parameter
Provider creates the group `EXTERNAL_my_secrets_int.my_api_token` with a parameter named
`my_api_token`.

### JSON example

For a secret named `service_config` in `my_secrets_int` with this JSON value:

Copy code

```
{
  "username": "<username>",
  "host": "<host>",
  "port": "<port>",
  "options": { "ssl": true },
  "tags": ["example"],
  "notes": null
}
```

The Snowflake Parameter Provider creates the group `EXTERNAL_my_secrets_int.service_config` with
the parameters `username`, `host`, and `port`. It doesn’t expose `options`, `tags`, or `notes` as
parameters.

## Filter integrations and secrets

To limit the external parameters available to Openflow beyond what the execute-as role can access, you can
go to the Runtime UI, open **Controller Settings** > **Parameter Providers** in the top-right menu,
select the **Snowflake Parameter Provider**, and configure these properties:

- **Integration Name Pattern** filters external secret provider integrations by name.
- **Secret Name Pattern** filters external secrets by name.

## Operational considerations

- Resolving one external parameter currently lists and fetches every secret visible through the
  referenced integration. Grant `USAGE` to the execute-as role only on the integrations that its
  connectors require. If needed, use **Integration Name Pattern** and **Secret Name Pattern** to further limit
  the integrations and secrets that the provider processes.
- For gen 2 connectors, stop and start the connector after adding or rotating a secret to apply the
  new value.
- For gen 1 connectors, run **Fetch** after adding or rotating a secret when you need the refreshed
  value to be used by referencing components.

## Troubleshoot Openflow configuration

Use the provider-specific setup topic to troubleshoot integration verification, cloud trust, or
provider permissions. For Openflow-specific issues, check the following:

| Symptom | Remedy |
| --- | --- |
| Integration isn’t discovered | Confirm that the execute-as role has `USAGE` on the integration and that the integration matches **Integration Name Pattern**. |
| Secret isn’t exposed as a parameter | Confirm that the secret matches **Secret Name Pattern** and that its value uses a supported mapping described on this page. |
| Gen 1 value is stale or its Parameter Context is missing | Run **Fetch** and confirm that the generated Parameter Context is inherited by the connector. |

Expand

Show lessSee more
