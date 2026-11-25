# Start, stop, and scale an app

This topic describes how to stop and start an app and how many instances it
runs. Both depend on the app’s
[compute option](/developer-guide/snowflake-app-runtime/serverless#label-snowflake-app-runtime-serverless-compare):

- On managed compute, an app runs until you suspend it.
- On serverless compute (Public Preview), an app starts on the first request
  and stops after an idle period.

To have an app stop when nobody uses it, see
[Move an existing app to serverless compute](/developer-guide/snowflake-app-runtime/serverless#label-snowflake-app-runtime-serverless-switch).

## Stop and start an app

To stop and start an app on managed compute, suspend and resume it. Suspending
releases its compute:

Copy code

```
ALTER APPLICATION SERVICE my_db.my_schema.my_app SUSPEND;
ALTER APPLICATION SERVICE my_db.my_schema.my_app RESUME;
```

After `RESUME`, requests return errors until the app is ready. Wait until the
app is `RUNNING` before you send traffic to it. To check its state, see
[Check service status](/developer-guide/snowflake-app-runtime/observability#label-snowflake-app-runtime-observability-service-status).
If `RESUME` fails because the runtime image is blocked, upgrade to a new
package version first. See
[Snowflake App Runtime limitations](/developer-guide/snowflake-app-runtime/limitations).

Serverless apps don’t support `SUSPEND` and `RESUME`. A serverless app stops
on its own when idle and starts again on the next request. See
[Set the idle timeout for a serverless app](#label-snowflake-app-runtime-scale-idle-timeout). To take a serverless app
offline, disable it. See
[Disable and enable a serverless app](#label-snowflake-app-runtime-scale-serverless-disable).

You need `OWNERSHIP` or `OPERATE` on the service to suspend, resume, disable,
or enable it. See
[Delegate lifecycle control](/developer-guide/snowflake-app-runtime/access-control#label-snowflake-app-runtime-access-control-delegate-lifecycle).

### Set the idle timeout for a serverless app

[![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

By default, Snowflake stops a serverless app after 3600 seconds (1 hour)
without requests. To use a longer idle period, set `auto_suspend_secs` in
[`app.yml`](/developer-guide/snowflake-app-runtime/app-yml):

Copy code

```
auto_suspend_secs: 7200
```

For valid values, see
[`auto_suspend_secs`](/developer-guide/snowflake-app-runtime/app-yml#label-snowflake-apps-manifest-auto-suspend-secs).
You can’t turn off idle stopping.

Serverless apps always start on request, so you can’t set
`auto_resume: false`. A request can’t start an app that you disabled.

### Disable and enable a serverless app

[![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Disabling stops a serverless app until you enable it again. No request can
start a disabled app:

Copy code

```
ALTER APPLICATION SERVICE my_db.my_schema.my_app DISABLE;
ALTER APPLICATION SERVICE my_db.my_schema.my_app ENABLE;
```

While disabled, the app keeps its Application Service object, deployed
package, configuration, privilege grants, and endpoint URL. Enabling recreates
the serverless runtime with the same endpoint.

You can’t upgrade, redeploy, or change the configuration of a disabled app.
Enable it first.

## Scale

On managed compute, an app starts as one instance. To run more, set
`min_instances` and `max_instances` in
[`app.yml`](/developer-guide/snowflake-app-runtime/app-yml):

Copy code

```
min_instances: 2
max_instances: 5
```

- `min_instances`: fewest instances Snowflake runs while the app is up. Must
  be at least `1`. Default is `1`.
- `max_instances`: most instances Snowflake runs. Must be at least
  `min_instances` and no more than `10`. Default is `1`.

If `max_instances` is greater than `min_instances`, Snowflake adds instances
when CPU is high and removes them when CPU is low. See
[How CPU-based autoscaling works](/developer-guide/snowpark-container-services/scaling-services#label-spcs-working-with-services-enabling-autoscaling).

You pay for compute nodes, not per instance. Snowflake packs instances onto a
node and adds a node only when the existing ones are full. See
[Cost and credit usage for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/cost).

Scaling settings apply only to managed compute. For how serverless apps run,
see [Serverless compute for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/serverless).

## Changes from ALTER don’t survive deploy

You can set instance counts and other properties with
[`ALTER APPLICATION SERVICE`](/sql-reference/sql/alter-application-service)
as well. That change isn’t permanent: the next `snow app deploy` puts the
values back to what’s in `app.yml`, or to the defaults if those keys aren’t
there. There are two
[exceptions](/developer-guide/snowflake-app-runtime/app-yml#label-snowflake-apps-manifest-validation):
`compute_resource` keeps its current value when omitted, and
`execute_as_role` can’t change after the app is created. To keep a value,
put it in `app.yml`.

## Next steps

- See what your apps cost: [Cost and credit usage for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/cost).
