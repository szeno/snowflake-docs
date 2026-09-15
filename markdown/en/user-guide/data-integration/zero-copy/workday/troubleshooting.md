# Troubleshoot Workday Live Data Query

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

This topic describes common errors you might encounter when setting up or using Workday Live Data Query (LDQ) from Snowflake, along with their causes and fixes.

## HTTP 404: queries fail after a successful connection

**Symptom:** The connection succeeds, but subsequent queries fail with an HTTP 404 error.

**Cause:** The port number in the connection configuration is incorrect.

**Fix:** Confirm that `"wd.port": "443"` is set in your `DataServiceConfig` dictionary. See [Connect to Workday and query data from Snowflake](/user-guide/data-integration/zero-copy/workday/connect-and-query).

---

## HTTP 400: authentication request rejected

**Symptom:** The authentication request is rejected by the Workday Authorization Server.

**Cause:** The ISU username in `DataServiceConfig` doesn’t match the ISU registered in Workday.

**Fix:** Verify that `wd.authn.isu` in your `DataServiceConfig` exactly matches the username shown in the **View Integration System User** task in Workday. This value is case-sensitive.

---

## HTTP 401: authentication fails at the token endpoint

**Symptom:** Authentication fails at the token endpoint.

**Cause:** The Client ID in your configuration doesn’t match the one generated in Workday.

**Fix:** Confirm that `wd.authn.clientId` matches the value on the **Register API Client** page in Workday.

---

## Access token request failed: network error

**Symptom:** Python raises a connection error before authentication completes.

**Cause:** The notebook can’t reach the Workday token endpoint. Either the EAI isn’t attached or the network rule is misconfigured.

**Fix:**

1. Confirm the external access integration is attached to the notebook. See [Connect to Workday and query data from Snowflake](/user-guide/data-integration/zero-copy/workday/connect-and-query).
2. Verify the network rule `VALUE_LIST` includes the correct hostname and port (`host:443`).
3. Confirm the EAI has `ENABLED = TRUE`.
4. Confirm that `ALLOWED_AUTHENTICATION_SECRETS` in the EAI includes `WORKDAY_LDQ_TEST.LIVEDATA.WORKDAY_PRIVATE_KEY`. Without this, `_snowflake.get_generic_secret_string()` also fails. See [Set up Snowflake for Workday Live Data Query](/user-guide/data-integration/zero-copy/workday/snowflake-setup).

---

## Failed to obtain access token: 404

**Symptom:** The connector reaches the server, but the token endpoint path returns a 404.

**Cause:** The token endpoint URL is incorrect, typically because of a wrong tenant ID or environment name.

**Fix:** Double-check `wd.authn.accessTokenEndpoint`. The expected format is:

Copy code

```
https://<host>/ccx/oauth2/<tenant>/token
```

Confirm the tenant name matches your Workday tenant exactly.

---

## Failed to obtain access token: 401 (cryptographic failure)

**Symptom:** The token request reaches Workday but authentication is rejected with a cryptographic error.

**Cause:** The private key in use doesn’t match the public key registered in Workday’s API Client.

**Fix:**

1. Confirm that the Snowflake Secret `WORKDAY_LDQ_TEST.LIVEDATA.WORKDAY_PRIVATE_KEY` contains the private key that corresponds to the public key registered in Workday’s API Client.
2. If keys have been rotated or regenerated, recreate the secret with the new private key content and re-register the API Client in Workday with the corresponding public key.

---

## `ModuleNotFoundError: No module named 'workday_ldq'`

**Symptom:** The import fails after a notebook restart.

**Cause:** The wheel is installed per-session and doesn’t persist across notebook restarts.

**Fix:** Re-run the `pip install` cell (Step 3 of [Connect to Workday and query data from Snowflake](/user-guide/data-integration/zero-copy/workday/connect-and-query)) after every notebook restart. Keeping it as the very first cell ensures it always runs first.

---

## `Exception: No secret found` or `PermissionError` when retrieving the secret

**Symptom:** The temporary UDF in the notebook setup fails with a secret-related error.

**Cause:** One of the following:

- The secret name is incorrect, or the secret doesn’t exist in `WORKDAY_LDQ_TEST.LIVEDATA`.
- The secret isn’t listed in `ALLOWED_AUTHENTICATION_SECRETS` on the EAI.
- The EAI isn’t attached to the notebook.

**Fix:**

1. Verify the secret exists by running the following in a Snowflake Worksheet:

   Copy code

   ```
   SHOW SECRETS IN SCHEMA WORKDAY_LDQ_TEST.LIVEDATA;
   ```
2. Confirm the EAI includes the secret and is attached to the notebook. See [Set up Snowflake for Workday Live Data Query](/user-guide/data-integration/zero-copy/workday/snowflake-setup) and [Connect to Workday and query data from Snowflake](/user-guide/data-integration/zero-copy/workday/connect-and-query).
3. Ensure the secret name in the `secrets` parameter of the `@udf` decorator matches the fully qualified name exactly (for example, `'WORKDAY_LDQ_TEST.LIVEDATA.WORKDAY_PRIVATE_KEY'`).

---

## Queries return no rows or table not found

**Symptom:** `SELECT COUNT(*) FROM workday_core.public.worker` returns `0` or a “table not found” error.

**Cause:** The ISU doesn’t have the correct security group permissions in Workday, or the Workday tenant hasn’t provisioned the Workday Data Cloud environment.

**Fix:**

1. Confirm the ISU belongs to an **Integration System Security Group (Unconstrained)** in Workday.
2. Confirm the ISU’s security group has **View Only** permission on the required Workday catalog domains.
3. Confirm that **Activate Pending Security Policy Changes** was run in Workday after setting up permissions.
4. Run `SHOW SCHEMAS` or `SHOW TABLES` through the connector to verify what’s accessible to the ISU.
