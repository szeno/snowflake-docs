# Serverless compute

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

With serverless compute, a Snowflake App Runtime app runs only while people use
it. Snowflake starts the app when a request arrives and stops it after an idle
period, so you don’t pay to keep it running between uses. You opt in per app by
setting `compute_resource: SERVERLESS` in
[`app.yml`](/developer-guide/snowflake-app-runtime/app-yml).

Serverless compute suits apps that people open at different times: a dashboard
checked each morning, an approval tool used through the week, or a report
used at month end. It supports Node.js and
[Python](/developer-guide/snowflake-app-runtime/build-python-app) apps.

## How serverless compute works

![Animated example of a serverless app that starts on a request, serves it, fills an idle timer while no requests arrive, and scales to zero when the timer ends.](/static/images/screens/snowflake-app-runtime-serverless-idle-cycle.gif)

1. A request arrives and Snowflake starts the app. The request waits, then gets
   its response when the app is up.
2. The app serves requests while people use it.
3. When no requests arrive for the idle period, 3600 seconds (1 hour) by
   default, Snowflake stops the app. To change the idle period, see
   [Set the idle timeout for a serverless app](/developer-guide/snowflake-app-runtime/scale-and-suspend#label-snowflake-app-runtime-scale-idle-timeout).
4. The next request starts the app again.

The Application Service, its deployed package, its configuration, and its URL
persist across these cycles. Only the running container stops and starts.

Requests arrive over HTTPS on the account’s `snowflake.app` domain. Snowflake
terminates TLS and authenticates the user before it forwards the request to the
app. See [Runtime environment for Snowflake App Runtime apps](/developer-guide/snowflake-app-runtime/runtime-environment).

## What a serverless app gets

- **A URL you choose.** Set `url_prefix` to name the app’s address:
  `<url_prefix>-apps.<org>-<account>.<region>.<cloud>.snowflake.app`. The
  address stays the same across redeploys. See
  [URL prefix](/developer-guide/snowflake-app-runtime/app-yml#label-snowflake-app-runtime-app-yml-serverless-url).
- **Per-app cost.** Each serverless app has its own
  [credit usage](/developer-guide/snowflake-app-runtime/cost#label-snowflake-app-runtime-cost-per-app).
- **Fixed size.** The app runs as one instance with 2 vCPU and 4 GiB of
  memory. Test your busiest apps under realistic load before you move them.
- **Disable and enable.** Use `DISABLE` and `ENABLE` to take the app offline
  and bring it back. See
  [Disable and enable a serverless app](/developer-guide/snowflake-app-runtime/scale-and-suspend#label-snowflake-app-runtime-scale-serverless-disable).
- **Caller’s rights.** Requests carry the caller token alone. See
  [Query Snowflake from a Snowflake App Runtime app](/developer-guide/snowflake-app-runtime/query-snowflake).
- **Logs.** Event tables receive the app’s logs. See
  [Monitor a Snowflake App Runtime app](/developer-guide/snowflake-app-runtime/observability).

For the full list of limits, see
[Serverless compute limitations](/developer-guide/snowflake-app-runtime/limitations#label-snowflake-app-runtime-limitations-serverless).

## Create a serverless app

Serverless compute must be enabled for your account. If it isn’t, contact
your Snowflake representative. See
[Serverless compute isn’t enabled](/developer-guide/snowflake-app-runtime/troubleshooting#label-snowflake-app-runtime-troubleshooting-serverless-not-enabled).

1. Use the latest version of
   [Snowflake CLI](/developer-guide/snowflake-cli/installation).
2. In an [`app.yml`](/developer-guide/snowflake-app-runtime/app-yml)
   manifest, set `compute_resource: SERVERLESS`. Optionally, set `url_prefix`
   to choose the app’s URL. If your project still uses `snowflake.yml`,
   [migrate to `app.yml`](/developer-guide/snowflake-app-runtime/migrate-to-app-yml)
   first.

   Copy code

   ```
   version: 2
   name: MY_APP
   compute_resource: SERVERLESS
   url_prefix: my-app
   ```

   Without `url_prefix`, Snowflake generates the name for you. Either way, the
   address stays the same across redeploys and disable-and-enable cycles.
3. Deploy the project:

   Copy code

   ```
   snow app deploy
   ```

   To check the resolved manifest first, run `snow app validate`.

   The first serverless deploy in an account can stop while Snowflake issues
   the TLS certificate, which can take up to three hours. See
   [Serverless deploy stops while the TLS certificate is issued](/developer-guide/snowflake-app-runtime/troubleshooting#label-snowflake-app-runtime-troubleshooting-serverless-certificate).

You can also build and deploy a serverless app from
[Snowsight Workspaces](/developer-guide/snowflake-app-runtime/workspaces).

## Move an existing app to serverless compute

You can’t convert an existing Application Service to serverless. Instead,
deploy a new service on serverless compute, move users to it, and then retire
the old service.

Before you start, check that the app doesn’t depend on in-memory or local
state. See [Design for ephemeral compute](#label-snowflake-app-runtime-serverless-state-caching).

1. In `app.yml`, add a
   [named target](/developer-guide/snowflake-app-runtime/deploy-targets#label-deploy-targets-serverless)
   with a new `name` and `compute_resource: SERVERLESS`. Keep the existing
   target so the current service stays unchanged:

   Copy code

   ```
   default_target: managed

   targets:
     managed:
       name: SALES_DASHBOARD
     serverless:
       name: SALES_DASHBOARD_SERVERLESS
       compute_resource: SERVERLESS
       url_prefix: sales-dashboard
   ```

   For the serverless fields, see
   [compute\_resource](/developer-guide/snowflake-app-runtime/app-yml#label-snowflake-app-runtime-app-yml-compute-resource).
2. Deploy the new target:

   Copy code

   ```
   snow app deploy --target serverless
   ```
3. Open the new app and verify that it works:

   Copy code

   ```
   snow app open --target serverless
   ```
4. Grant access to the new service. Grants on the old service don’t carry
   over. Grant `USAGE` on the new Application Service to each role that uses
   the app:

   Copy code

   ```
   GRANT USAGE ON APPLICATION SERVICE <database>.<schema>.SALES_DASHBOARD_SERVERLESS TO ROLE ANALYST;
   ```

   For other privileges and patterns, see
   [Share a Snowflake App Runtime app](/developer-guide/snowflake-app-runtime/access-control).
5. Update links, bookmarks, and docs to point to the new URL.
6. Set `default_target: serverless` in `app.yml`. This step is required so
   that later deploys go to the new service and not the old one:

   Copy code

   ```
   default_target: serverless
   ```
7. Keep the old service running while people move to the new URL. Its URL
   works only while the service exists, so dropping it breaks old links and
   bookmarks. To send visitors on, deploy a version of the old app that
   redirects to the new URL.

## Design for ephemeral compute

Design your app so it can serve requests after starting with an empty cache.
When a serverless app stops, in-process caches and files written to its local
filesystem don’t persist. The next request starts a new runtime.

Check for data held in module-level variables, in-memory caches, or local
files. Store anything the app must retain in durable storage.

Choose a caching strategy based on what must persist across a restart:

**In-process memory:** Use it for disposable data that the app can fetch or
calculate again on a cache miss. Don’t depend on it for durable state.

**Local disk:** Use `/tmp` for disposable scratch files, not as the source of
truth.

**Snowflake query result reuse:** For repeated SQL queries, consider
Snowflake’s built-in [result reuse](/user-guide/querying-persisted-results)
before adding an application cache. Reuse depends on the query, underlying
data, privileges, and other conditions; identical SQL alone doesn’t
guarantee it.

**Snowflake tables:** Use a table when cached data must persist across
restarts. Consider [hybrid tables](/user-guide/tables-hybrid) for low-latency
primary-key lookups, subject to their
[availability and limitations](/user-guide/tables-hybrid-limitations).
Define when entries expire and how the app refreshes them.

If you cache caller’s rights query results, preserve user isolation. Reading a
stored result doesn’t rerun the original query’s authorization checks.
Restrict who can read the cache and verify that each user is authorized to
receive the cached data. See
[Stateless design and session isolation](/developer-guide/snowflake-app-runtime/secure-development#label-snowflake-app-runtime-secure-development-stateless).

## Serverless and managed compute

An app without `compute_resource` runs on managed compute, which is generally
available. You set the compute option when you create the app and can’t change
it later.

| Feature | Serverless compute | Managed compute |
| --- | --- | --- |
| Status | Public Preview, opt in with `compute_resource: SERVERLESS` | Generally available, the default |
| Start and stop | Starts on the first request and stops after an idle period | Always on until you suspend the app |
| Requests while stopped | The request waits while the app starts, then gets its response | Requests fail with an error until the app finishes resuming |
| URL | `<url_prefix>-apps.<org>-<account>.<region>.<cloud>.snowflake.app` | `<id>-<org>-<account>-<region>.snowflakecomputing.app` |
| Cost attribution | Each app has its own [credit usage](/developer-guide/snowflake-app-runtime/cost#label-snowflake-app-runtime-cost-per-app) | Credits are reported for the account’s compute, not for each app |
| Observability | Event-table logs only | Event-table logs, metrics, and lifecycle events |

Expand

Show lessSee more

## Next steps

- Change how long a serverless app stays idle before it stops: [Set the idle timeout](/developer-guide/snowflake-app-runtime/scale-and-suspend#label-snowflake-app-runtime-scale-idle-timeout).
- Build a Python app, which runs on serverless compute: [Build a Python app for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/build-python-app).
