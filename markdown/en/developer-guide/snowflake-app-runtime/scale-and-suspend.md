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

### Auto-suspend

`auto_suspend_secs` in `app.yml` sets how many idle seconds pass before
Snowflake suspends the app. It defaults to `0`, which turns auto-suspend off.
`auto_resume`, which defaults to `true`, resumes a suspended app on its next
request.

Setting a nonzero value isn’t recommended: when a suspended app resumes,
requests return errors until it’s ready. The same happens after you run
`SUSPEND`, so after `RESUME`, wait until the app is `RUNNING` before you send
traffic to it.

If you set a value earlier, remove it from `app.yml` and redeploy. For an app
you don’t deploy from `app.yml`, run:

Copy code

```
ALTER APPLICATION SERVICE my_db.my_schema.my_app UNSET AUTO_SUSPEND_SECS;
```

## Changes from ALTER don’t survive deploy

You can set instance counts and other properties with
[`ALTER APPLICATION SERVICE`](/sql-reference/sql/alter-application-service)
as well. That change isn’t permanent: the next `snow app deploy` puts the
values back to what’s in `app.yml`, or to the defaults if those keys aren’t
there. To keep a value, put it in `app.yml`.
