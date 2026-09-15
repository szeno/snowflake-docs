# Understanding Snowflake Data Clean Room policies

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. Migrate to the
[Collaboration API](/user-guide/cleanrooms/overview) using the
[migration tool](/user-guide/cleanrooms/migration-tool) before the dates below.

- **2026-10-01:** New legacy clean rooms may not be created via the
  [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction).
- **2027-02-01:** The [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction)
  will no longer be accessible, and new legacy clean rooms may not be created via the
  [Provider and Consumer API](/user-guide/cleanrooms/getting-started).
- **2027-06-01:** Legacy [Provider and Consumer clean rooms](/user-guide/cleanrooms/getting-started)
  will no longer be accessible. Use the [Collaboration API](/user-guide/cleanrooms/overview)
  to create and manage clean rooms.

Clean rooms can implement data policies to control how data can be used by collaborators. These are in addition to any Snowflake table
policies set on the underlying tables linked into the clean room.

Each collaborator in a clean room can set policies on their own data. Your policies are enforced only in requests from other users;
your policies are not enforced against your own requests. For example, if your join policy allows joins against only column A, other users
are restricted to joining on column A, but you can run joins against any of your columns.

Clean room policies can be set using either the clean room API or UI.

To implement policy checks, the following must be true:

- **The data owner must set a policy in their clean room.** You set policies using either the API or the UI. Each policy type is set separately. Clean rooms natively implement column policies, row policies, and activation policies. **Clean room policies aren’t additive:** when you set a clean room policy, all previous values are deleted.

  Copy code

  ```
  -- Sets a join policy on column HASHED_EMAIL.
  CALL samooha_by_snowflake_local_db.provider.set_join_policy(
    'my_provider_cleanroom',
    ['my_db.my_sch.T1:HASHED_EMAIL']);

  -- Replaces the previous join policy. Now the only column in the join policy is AGE_BND.
  CALL samooha_by_snowflake_local_db.provider.set_join_policy(
    'my_provider_cleanroom',
    ['my_db.my_sch.T1:AGE_BAND']);
  ```
- **The template must check the policy in the appropriate place in the template.** A clean room policy is checked only if it has the
  appropriate policy filter applied to the column in the template. If you set a clean room policy to protect your data, you should examine
  the template to confirm that the template is enforcing your policies as you expect. The following template checks whether col1 is allowed
  by the data owner’s column policy:

  Copy code

  ```
  SELECT
    IDENTIFIER( {{ col1 | column_policy }} )
  FROM {{ source_table[0] }} AS c;
  ```

  The following template does not check whether `col1` has a clean room policy:

  Copy code

  ```
  SELECT
    IDENTIFIER( {{ col1 }})
  FROM {{ source_table[0] }} AS c;
  ```

  Clean rooms supports a different template filter for each policy type. However, the semantics of the filter are not checked, only whether
  the column is in the policy for that filter type. For example, in the following snippet, the join policy is checked for `col1`, even
  though the column is not being joined against. If `col1` is in the data owner’s join policy, the query can succeed; if `col1` is not
  in the data owner’s join policy, the query will be blocked.

  Copy code

  ```
  SELECT
    IDENTIFIER( {{ col1 | join_policy }})
  FROM {{ source_table[0] }} AS c;
  ```

Note

Column policy checks are carried out when the template JinjaSQL is parsed. Queries
with wildcards might not be caught using these checks, and discretion should be used when designing an analysis template. If some columns
should really never be queried, consider creating a view of your source table that eliminates these sensitive columns, and link in
that view instead.

## Snowflake policies in clean rooms

When you link tables into a clean room, any Snowflake table policies on the source tables are enforced in the linked tables in the clean
room, but these policies aren’t necessarily reported by the clean room API or UI. For instance, a
[Snowflake join policy](/user-guide/join-policies) continues to be enforced in the clean room, but that join policy is not visible
by calling `consumer.view_provider_join_policy` or `consumer.view_join_policy`. Therefore, you should either remove policies from the
underlying linked tables, create equivalent clean room policies (when they exist), or communicate the existence of these policies clearly
to your collaborators so that their queries don’t fail or behave unexpectedly (“why can’t I join on this column?”).

Any changes to Snowflake policies in the source tables are automatically propagated to the linked views in the clean room.

[Snowflake privacy policies](/user-guide/diff-privacy/differential-privacy-admin-privacy-policies) prevent creation of a view from a
protected table, so you cannot link in tables that have privacy policies.

The following policies can be applied directly into a clean room:

- [Join policies](#join-policies)

### Join policies

Set a join policy to indicate which columns in your data can be joined on by *any* template in the clean room. (Snowflake join policies, in
contrast, specify which columns *must* be joined on.) Join policies apply to all templates in the clean room.

A column cannot be in both a join policy and a column policy, but a column can be in both a join policy and an activation policy.

## Implementing a join policy

Clean room join policies are enforced against a column if the template applies the `join_policy` or `join_and_column_policy`
filter to the column.

If a template checks a join policy for a column, and the clean room has no join policies set, or the column is not in the join policy, the
query will be blocked.

The following code shows how to set join policies as a provider or a consumer. Remember that policies are only enforced against queries
run by another account.

Copy code

```
-- Set join policies on two columns in a clean room where you are a provider.
CALL samooha_by_snowflake_local_db.provider.set_join_policy(
  'my_provider_cleanroom',
  ['SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:HASHED_EMAIL', 'MYDB.MYSCH.EXPOSURES:HASHED_EMAIL']);

-- Set join policies on two columns in a clean room where you are a consumer.
CALL samooha_by_snowflake_local_db.consumer.set_join_policy(
  'my_consumer_cleanroom',
  ['SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:HASHED_EMAIL', 'MYDB.MYSCH.EXPOSURES:HASHED_EMAIL']);
```

The following procedures are used to view or manage join policies in code:

- `consumer.set_join_policy`
- `consumer.view_provider_join_policy`
- `consumer.view_join_policy`
- `provider.view_join_policy`
- `provider.set_join_policy`

### Column policies

Set a column policy to indicate which of your columns can be projected in analysis results from a *specific* template. Column policies are
applied to specific templates in a specific clean room.

A column cannot be in both a join and a column policy. A column can be in both an activation and a column policy.

## Implementing a column policy

Clean room column policies are enforced against a column only if the template uses the `column_policy` or `join_and_column_policy`
filter.

If a clean room checks a column policy for a column, and the column is not in the column policy, or the clean room has no column policies,
the query will be blocked.

The following code shows how to set column policies for three columns when accessed by the `prod_overlap_analysis` template. The example
shows how to set the policy both as a provider and a consumer. Remember that policies are only enforced against queries
run by another account.

Copy code

```
-- Set column policy check on prod_overlap_analysis template in a clean room where
-- you are a provider.
call samooha_by_snowflake_local_db.provider.set_column_policy(
  'my_provider_cleanroom',
  ['prod_overlap_analysis:SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:STATUS',
   'prod_overlap_analysis:SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:AGE_BAND',
   'prod_overlap_analysis:SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:DAYS_ACTIVE']);

-- Set column policy check on prod_overlap_analysis template in a clean room where
-- you are a consumer.
call samooha_by_snowflake_local_db.consumer.set_column_policy(
  'my_consumer_cleanroom',
  ['prod_overlap_analysis:SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:STATUS',
   'prod_overlap_analysis:SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:AGE_BAND',
   'prod_overlap_analysis:SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:DAYS_ACTIVE']);
```

The following procedures are used to view or manage column policies in code:

- `consumer.set_column_policy`
- `consumer.view_column_policy`
- `consumer.view_provider_column_policy`
- `provider.set_column_policy`
- `provider.view_column_policy`

### Activation policies

Set an activation policy to indicate which of your columns can be activated by an activation template. Activation saves query results to
a table in the Snowflake account of the provider or consumer, or to a third-party activation connector.

A column can be part of an activation policy as well as any other policy.

## Implementing an activation policy

Activation policies can be set in the clean rooms UI if the template allows activation.

Activation policies are set for a specific column in a specific template.

Activation policies are enforced against a column only if the template applies the `activation_policy` filter to the column.

The following code demonstrates setting an activation policy to allow the HASHED\_EMAIL and REGION\_CODE columns to be activated in a clean
room. This policy affects all users and all activation templates in the clean room. There are equivalent procedures for providers and
consumers in a clean room. Call the procedure that reflects your role in the clean room.

Copy code

```
-- Set activation policy check on prod_overlap_analysis template in a clean room where you are a provider
call samooha_by_snowflake_local_db.provider.set_activation_policy('my_cleanroom', [
    'prod_overlap_analysis:SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:HASHED_EMAIL',
    'prod_overlap_analysis:SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:REGION_CODE' ]);

-- Set activation policy check on prod_overlap_analysis template in a clean room where you are a consumer
call samooha_by_snowflake_local_db.consumer.set_activation_policy('my_cleanroom', [
    'prod_overlap_analysis:SAMOOHA_SAMPLE_DATABASE_NAME.DEMO.CUSTOMERS:HASHED_EMAIL',
    'prod_overlap_analysis:SAMOOHA_SAMPLE_DATABASE_NAME.DEMO.CUSTOMERS:REGION_CODE' ]);
```

The following template checks that the value passed into `col1` by the caller is in the caller’s activation policy. If the activation policy was set as shown previously, that means the only columns that can be activated are `HASHED_EMAIL` and `REGION_CODE`.

Copy code

```
BEGIN
  CREATE OR REPLACE TABLE cleanroom.activation_data_analysis_results AS
    SELECT {{ col1 | sqlsafe | activation_policy }}
    FROM IDENTIFIER({{ my_table[0] }}) AS c
    RETURN 'analysis_results';
END;
```

The following procedures are used to manage activation policies in code:

- `consumer.set_activation_policy`
- `provider.set_activation_policy`

### Aggregation policies

Aggregation policies require that all queries against a table contain aggregations (GROUP BY, COUNT, and other functions), and also specify
a minimum number of rows per result group, or the group will be omitted from the results.

Clean rooms do not have their own implementation of aggregation policies; to apply aggregation constraints on your linked data, either
apply an [aggregation policy](/user-guide/aggregation-policies) on the source table, or implement aggregation constraints in your
template.

Some Snowflake-provided templates use the `threshold` and `threshold_value` parameters set for a user or template. These values can be
modified in the clean rooms UI, or by calling `provider.add_consumers` or `provider/consumer.set_privacy`. If set for a consumer, you
can [access these values in your template](/user-guide/cleanrooms/v1/custom-templates#label-dcr-v1-snowflake-defined-variables).
