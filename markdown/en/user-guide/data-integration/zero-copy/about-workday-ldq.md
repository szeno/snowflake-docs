# About Workday Live Data Query for Snowflake

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Note

Workday Live Data Query for Snowflake is in Early Adopter (EA) for Workday and in Preview for Snowflake. To request access, contact your Workday account representative.

Workday Live Data Query (LDQ) gives you real-time SQL access to Workday business data from Snowflake, without any ETL pipelines or data replication. Data stays in Workday; Snowflake queries it on demand through a Python connector running in a Snowflake Notebook.

This integration is ideal for organizations that need up-to-date workforce and talent data inside Snowflake for analytics, reporting, or AI workloads, without the overhead and latency of a traditional data pipeline.

## How it works

Workday LDQ uses a Trino-over-HTTPS connection to query the Workday Unified Data Catalog directly from a Snowflake Notebook. Authentication uses JWT Bearer OAuth2, with credentials stored securely as Snowflake Secrets.

Copy code

```
Snowflake Notebook
  └── Python (workday_ldq wheel)
        └── JWT Bearer OAuth2 → Workday Token Endpoint
              └── Trino-over-HTTPS → Workday Live Data Query service
                    └── Returns rows from Workday Unified Data Catalog
```

Because the data isn’t copied into Snowflake, queries always reflect the current state of your Workday tenant.

## Available data

In EA, the integration supports Workforce and Talent objects, including:

- `worker`
- `worker_contact_data`
- `job_profile`

Support for Financials, Payroll, and Student objects is planned for general availability (GA).

## Prerequisites

Before starting, ensure you have the following from your Workday administrator:

| Item | Example |
| --- | --- |
| ISU username | `snowflake_ldq_user` |
| Client ID | `YTg4YjRk...` (base64 string) |
| Token endpoint | `https://<host>/ccx/oauth2/<tenant>/token` |
| Private key file | `private-key.pem` (RSA 2048, PEM format) |
| Workday host | `impl-services1.<tenant>.myworkday.com` |

Expand

Show lessSee more

You also need:

- `ACCOUNTADMIN` (or equivalent) role in Snowflake to complete the initial setup.
- The `ldq_python_client-*.whl` wheel file, available from the Workday Community portal.

Note

The steps in this guide use `WORKDAY_LDQ_TEST` as the base name for all Snowflake objects (for example, `WORKDAY_LDQ_TEST` database, `WORKDAY_LDQ_TEST_ROLE` role, `WORKDAY_LDQ_TEST_USER` user, `WORKDAY_LDQ_TEST_EAI` integration). Replace these with names that match your organization’s naming conventions, and substitute consistently throughout all steps.

## Setup checklist

| Order | Task | Description | Persona |
| --- | --- | --- | --- |
| 1 | [Set up Snowflake for Workday Live Data Query](/user-guide/data-integration/zero-copy/workday/snowflake-setup) | Create the Snowflake objects required for LDQ: role, user, database, schema, stage, network rule, secret, and external access integration. | Snowflake account administrator |
| 2 | [Connect to Workday and query data from Snowflake](/user-guide/data-integration/zero-copy/workday/connect-and-query) | Create a Snowflake Notebook, install the Workday connector, configure credentials, and run your first queries against Workday data. | Snowflake account administrator or data engineer |
| 3 | [Use Cortex Code with Workday data](/user-guide/data-integration/zero-copy/workday/cortex-code) | Use Cortex Code to write queries, analyze results, and build visualizations on top of Workday data. | Data engineer or analyst |

Expand

Show lessSee more

If you run into errors, see [Troubleshoot Workday Live Data Query](/user-guide/data-integration/zero-copy/workday/troubleshooting).
