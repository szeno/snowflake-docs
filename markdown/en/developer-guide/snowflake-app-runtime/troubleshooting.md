# Troubleshoot apps

This topic describes how to fix common Snowflake App Runtime errors. To inspect
an app’s state and logs first, see
[Quick troubleshooting runbook](/developer-guide/snowflake-app-runtime/observability#label-snowflake-app-runtime-observability-runbook).

## Deploy

### Serverless compute isn’t enabled

[![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

If `snow app deploy` reports
`compute_resource SERVERLESS is not enabled for this account.`, run `snow upgrade` to
update the [Snowflake CLI](/developer-guide/snowflake-cli/installation), then
deploy again. If the error persists, serverless compute isn’t enabled for
the account. Contact your Snowflake representative.

### Serverless deploy stops while the TLS certificate is issued

[![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

On the first serverless deploy in an account, the CLI checks for the TLS
certificate that serverless endpoints share. If the certificate is missing,
the CLI starts
[SYSTEM$ISSUE\_PER\_ACCOUNT\_APP\_SERVICE\_CERTIFICATE](/sql-reference/functions/system_issue_per_account_app_service_certificate)
automatically. A full deploy or `snow app deploy --promote-only` stops, but
`--upload-only` and `--build-only` continue after a warning. Issuance can take
up to three hours. Run the stopped command again after the certificate is
ready.

If the CLI can’t check the certificate, such as when AWS PrivateLink, a proxy,
or a custom certificate authority is in the path, the deploy continues without
starting issuance. If the app URL later shows a browser warning, start issuance
manually:

Copy code

```
SELECT SYSTEM$ISSUE_PER_ACCOUNT_APP_SERVICE_CERTIFICATE();
```

Wait for issuance to finish, then run the deploy again.

### Can’t upgrade or redeploy a disabled serverless app

[![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

You can’t upgrade, redeploy, or change the configuration of a disabled
serverless app. Run `ALTER APPLICATION SERVICE ... ENABLE`, then try again. See
[Disable and enable a serverless app](/developer-guide/snowflake-app-runtime/scale-and-suspend#label-snowflake-app-runtime-scale-serverless-disable).

## Sign-in and caller’s rights

### Caller’s rights login fails on serverless compute

[![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

On serverless compute, the `Sf-Context-Current-User-Token` header holds the
caller’s complete OAuth token. Authenticate with that token alone and
`authenticator: "OAUTH"`. A token joined with the session token, as managed
compute requires, fails at login. Projects created with an older
version of the `snowflake-apps` skill might join the tokens on every backend.
See [How you use the caller token depends on the](/developer-guide/snowflake-app-runtime/query-snowflake#label-query-snowflake-callers-rights-serverless).

## Workspaces preview

[![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

### Logs pane shows Container not ready

If the dev server isn’t running yet, for example right after you select
**Preview**, the logs pane shows `Container not ready` and keeps checking. Wait
for the dev server to start.

### Preview stops restarting after crashes

If the dev server crashes three times in a row, each within 10 seconds of
starting, Snowflake stops restarting it. To start it again, edit a source file,
or select **Shutdown** and then reopen **Preview**.

### Query results differ from the deployed app

A preview has no caller identity, so caller’s rights isn’t available. Apps from
the **Next.js App** template run caller’s rights queries with the preview’s own
credentials instead. Test row access and masking policies in a deployed app.

## Next steps

- Inspect logs and events for a running app: [Monitor a Snowflake App Runtime app](/developer-guide/snowflake-app-runtime/observability).
