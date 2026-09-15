# Manage Postgres instances with Terraform

You can use the [Snowflake Terraform provider](/user-guide/terraform) to create, update, and
destroy Snowflake Postgres instances using infrastructure as code. The provider includes a
`snowflake_postgres_instance` resource for managing the full instance lifecycle.

For complete provider documentation including all available attributes and data sources, see
the [Terraform Registry documentation](https://registry.terraform.io/providers/snowflakedb/snowflake/latest/docs/resources/postgres_instance).

Note

The `snowflake_postgres_instance` resource is currently a preview feature in the Terraform
provider. To use it, add `"snowflake_postgres_instance_resource"` to the
`preview_features_enabled` list in your provider configuration. The resource schema may change
in future provider releases. This doesn’t affect the Snowflake Postgres feature itself, which
is generally available.

## Provider configuration

Configure the Snowflake provider with `preview_features_enabled` to use the Postgres instance
resource:

Copy code

```
terraform {
  required_providers {
    snowflake = {
      source  = "snowflakedb/snowflake"
      version = "~> 2.18"
    }
  }
}

provider "snowflake" {
  organization_name        = "my_organization"
  account_name             = "my_account"
  user                     = "my_user"
  authenticator            = "PROGRAMMATIC_ACCESS_TOKEN"
  token                    = file("/path/to/token")
  preview_features_enabled = ["snowflake_postgres_instance_resource"]
}
```

## Create an instance

The following example creates a minimal Postgres instance:

Copy code

```
resource "snowflake_postgres_instance" "my_instance" {
  name                     = "my_postgres_instance"
  compute_family           = "BURST_S"
  storage_size_gb          = 10
  authentication_authority = "POSTGRES"
  postgres_version         = 18

  timeouts {
    create = "30m"
    update = "30m"
    delete = "30m"
  }
}
```

Postgres instance operations can take several minutes. Always include a `timeouts` block with
values of at least 10 minutes for create, update, and delete. For instances with high availability
enabled, you may need even more time.

## Create an instance with a network policy

A common workflow is to create a network rule and network policy in the same Terraform
configuration, then reference the policy in the Postgres instance. Terraform handles the
dependency ordering automatically.

Postgres network rules require `type = "IPV4"` with `mode = "POSTGRES_INGRESS"`:

Copy code

```
resource "snowflake_network_rule" "pg_ingress" {
  name       = "pg_ingress_rule"
  database   = "my_database"
  schema     = "public"
  type       = "IPV4"
  mode       = "POSTGRES_INGRESS"
  value_list = ["203.0.113.0/24"]
  comment    = "Allow office network for Postgres"
}

resource "snowflake_network_policy" "pg_policy" {
  name    = "pg_network_policy"
  allowed_network_rule_list = [
    snowflake_network_rule.pg_ingress.fully_qualified_name
  ]
}

resource "snowflake_postgres_instance" "my_instance" {
  name                     = "my_postgres_instance"
  compute_family           = "STANDARD_M"
  storage_size_gb          = 10
  authentication_authority = "POSTGRES_OR_SNOWFLAKE"
  postgres_version         = 18
  network_policy           = snowflake_network_policy.pg_policy.name

  timeouts {
    create = "30m"
    update = "30m"
    delete = "30m"
  }
}
```

Caution

Don’t use `type = "HOST_PORT"` with `mode = "INGRESS"` for Postgres network rules. Postgres
ingress requires `type = "IPV4"` with `mode = "POSTGRES_INGRESS"`.

## Get connection details

After creating an instance, you can retrieve the connection hostname from the resource’s
computed attributes:

Copy code

```
output "postgres_host" {
  value = snowflake_postgres_instance.my_instance.describe_output[0].host
}

output "postgres_state" {
  value = snowflake_postgres_instance.my_instance.describe_output[0].state
}
```

The port is always 5432 unless you’re using
[connection pooling](/user-guide/snowflake-postgres/postgres-connection-pooling), which uses
port 5431. Credentials aren’t available through Terraform and must be
configured separately:

- For instances with `authentication_authority = "POSTGRES"`: reset credentials through
  Snowsight or the Snowflake CLI.
- For instances with `authentication_authority = "POSTGRES_OR_SNOWFLAKE"`: generate an
  access token using [GENERATE\_POSTGRES\_ACCESS\_TOKEN\_FOR\_USER](/sql-reference/functions/generate_postgres_access_token_for_user)
  after configuring a role mapping.

For more information about connecting, see [Connecting to Snowflake Postgres](/user-guide/snowflake-postgres/connecting-to-snowflakepg).

## Async operations

Some changes to Postgres instances, including compute family changes, version upgrades, and
enabling high availability, complete asynchronously after Terraform reports success. The
instance remains available during these operations.

To check whether a background operation has completed, run:

Copy code

```
DESCRIBE POSTGRES INSTANCE my_instance;
```

When the `operations` field is empty (`{}`), all background operations have finished.

Note

Running `terraform plan` immediately after an apply that triggered an async operation won’t
show drift, even though the change hasn’t completed in Snowflake yet. If your pipeline
depends on the change being live, add a verification step outside Terraform.

## Import an existing instance

To bring an existing Postgres instance under Terraform management:

Copy code

```
terraform import snowflake_postgres_instance.my_instance '"MY_INSTANCE_NAME"'
```

The name must be wrapped in single quotes containing double quotes (the outer quotes are for the
shell, the inner quotes are the Snowflake identifier format).

## Limitations

- **Credentials**: there’s no way to set or retrieve Postgres credentials through Terraform.
  Credential setup requires a separate step in Snowsight or SQL.
- **Scope**: not all Snowflake Postgres features are configurable through Terraform. See [Managing instances](/user-guide/snowflake-postgres/managing-instances) for additional features for managing Postgres instances.
