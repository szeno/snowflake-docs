# Scale and suspend Snowflake App Runtime apps

An app starts as one instance and keeps running until you stop it. You can
scale up to more instances, or scale down to zero.

## Scale to more than one instance

In [`app.yml`](/developer-guide/snowflake-app-runtime/app-yml):

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

These fields don’t take an app to zero. Suspend it instead.

## Scale to zero

Suspend the app to stop it and release compute:

Copy code

```
ALTER APPLICATION SERVICE my_db.my_schema.my_app SUSPEND;
ALTER APPLICATION SERVICE my_db.my_schema.my_app RESUME;
```

You need `OWNERSHIP` or `OPERATE` on the service. See
[Delegate lifecycle control](/developer-guide/snowflake-app-runtime/access-control#label-snowflake-app-runtime-access-control-delegate-lifecycle).

To check whether the app is `RUNNING` or `SUSPENDED`, see
[Check service status](/developer-guide/snowflake-app-runtime/observability#label-snowflake-app-runtime-observability-service-status).
If `RESUME` fails because the runtime image is blocked, upgrade to a new
package version first. See
[Snowflake App Runtime limitations](/developer-guide/snowflake-app-runtime/limitations).

You can also set an idle window in `app.yml`:

Copy code

```
auto_suspend_secs: 900
auto_resume: true
```

- `auto_suspend_secs`: idle seconds before Snowflake can auto-suspend the
  app. `0` (the default) disables it. The minimum non-zero value is `300`.
- `auto_resume`: resume on the next request. Default is `true`.

To stop the app yourself, run `SUSPEND`.

## Changes from ALTER don’t survive deploy

You can set instance counts and auto-suspend with
[`ALTER APPLICATION SERVICE`](/sql-reference/sql/alter-application-service)
as well. That change isn’t permanent: the next `snow app deploy` puts the
values back to what’s in `app.yml`, or to the defaults if those keys aren’t
there. To keep a value, put it in `app.yml`.
