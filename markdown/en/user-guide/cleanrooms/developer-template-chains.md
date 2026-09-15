# Using the developer APIs to execute templates sequentially

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

Complex analyses might require that multiple templates be executed in a specific order, sometimes using the output of one template as the
input of another. A provider can create a *template chain* to define a sequence of templates to be executed in a particular order. When
defining this template chain, the provider can specify whether the results of a particular template will be available to subsequent
templates in the chain.

A clean room user executes a template chain to perform an analysis that runs the templates in the chain in their predefined order.

## About intermediary results

If a provider wants the results of one template to be available to subsequent templates in the template chain, they can create a cache for
the template’s results. Each template with a cache also has an expiration time for that cache.

If a provider specifies that a template has a cache, the first time a user executes the template chain, the results of that template are
stored in a table within the clean room. This underlying table is only accessible to the clean room itself. The next time a user executes
the template chain, Snowflake Data Clean Rooms checks whether the cache has expired before executing the template. The template with the
cached results does not execute again unless the cache has expired.

Subsequent templates in the template chain can use the cache as input by including the appropriate Jinja parameter in the template.

## Define a template chain

A provider uses the `provider.add_template_chain` command to create a template chain. The templates that the provider wants to add
to the new template chain must exist before creating the template chain.

The `provider.add_template_chain` command accepts the following arguments:

- Name of a clean room (string).
- Name of the template chain (string).
- Templates in the template chain (array of JSON objects).

For an example of using the `provider.add_template_chain` command to create a template chain, see
[Example](#label-dev-api-template-chain-example).

### Adding templates to the template chain

The provider defines which templates are part of a template chain by passing an array of JSON objects into
`provider.add_template_chain`, where each JSON object represents a template. The order of the JSON objects determines the order in
which the templates are executed.

The JSON object for a template can include the following fields:

`template_name` (string)
:   Specifies the template being added to the template chain. The template must already exist.

    This field is required.

`cache_results` (boolean)
:   Determines whether the results of the template are [cached](#label-dev-api-template-chain-cache) so other templates in the template
    chain can access them. To cache results, specify TRUE.

    This field is required. If TRUE, the `output_table_name` and `cache_expiration_hours` fields are also required.

`output_table_name` (string)
:   When `cache_results = TRUE`, specifies the name of the Snowflake table where template results are stored.

    This field is required if `cache_results = TRUE`.

`jinja_output_table_param` (string)
:   When `cache_results = TRUE`, specifies the name of the Jinja parameter that other templates must include to accept the results that
    are stored in `output_table_name`.

    This field is optional.

`cache_expiration_hours` (integer)
:   When `cache_results = TRUE`, specifies the number of hours before the results in the cache are dropped. When the cache expires, then
    next time the template chain is executed the cache is refreshed with the results of the template.

    This field is required if `cache_results = TRUE`.

### Example

In this example, the provider wants to:

- Create a template chain `insights_chain` in the clean room `collab_clean_room`.
- Define the template chain so the `crosswalk` template executes before the `transaction_insights` template.
- Cache the results of the `crosswalk` template so they can be used as input to the `transaction_insights` template.

Copy code

```
CALL samooha_by_snowflake_local_db.provider.add_template_chain(
  'collab_clean_room',
  'insights_chain',
  [
    {
      'template_name': 'crosswalk',
      'cache_results': True,
      'output_table_name': 'crosswalk',
      'jinja_output_table_param': 'crosswalk_table_name',
      'cache_expiration_hours': 2190
    },
    {
      'template_name': 'transaction_insights',
      'cache_results': False
    }
  ]
);
```

For more information about each JSON object, see [Adding templates to the template chain](#label-dev-api-template-chain-templates).

## Execute a template chain

A clean room user runs the `consumer.run_analysis` command to execute a template chain, which is the same command used to execute a
single template. Executing the template chain runs each template in the chain in their predefined order to get the final result.

The `consumer.run_analysis` command accepts arguments that it passes to the Jinja templates in the template chain. You can determine
what arguments are expected by the templates in the chain by executing the `consumer.get_arguments_from_template_chain` command.

The arguments passed to `consumer.run_analysis` can be specific to a particular template in the chain or can be arguments for every
template in the chain.

Universal arguments
:   If you want to pass an argument to every template in the template chain, the syntax is the same as using `consumer.run_analysis` to
    run a single template. For example, the following command passes the value of the `where_clause` argument to all templates in the
    template chain:

    Copy code

    ```
    CALL samooha_by_snowflake_local_db.consumer.run_analysis(
      'collab_clean_room',
      'insights_chain',
      ['MY_CONSUMER_DB.C_SCHEMA.CONVERSIONS'],
      ['PROVIDER_DB.P_SCHEMA.EXPOSURES'],
      object_construct(
        'where_clause', 'p.EMAIL=c.EMAIL'
      )
    );
    ```

Template-specific arguments
:   If you want to pass an argument to a specific template, add another `object_construct` as a child of the top-level
    `object_construct` with the name of the template as the field name. For example, the following command passes the value of the
    `dimensions` argument to the `crosswalk_template` template only:

    Copy code

    ```
    CALL samooha_by_snowflake_local_db.consumer.run_analysis(
      'collab_clean_room',
      'insights_chain',
      ['MY_CONSUMER_DB.C_SCHEMA.CONVERSIONS'],
      ['PROVIDER_DB.P_SCHEMA.EXPOSURES'],
      object_construct(
        'where_clause', 'p.EMAIL=c.EMAIL',
        'crosswalk_template', object_construct(
          'dimensions', ['p.CAMPAIGN']
        )
      )
    );
    ```

## Template chain commands

You can use the following commands to work with template chains:

| Command | Description |
| --- | --- |
| `provider.add_template_chain` | Creates a new template chain. |
| `provider.view_added_template_chains`  `consumer.view_added_template_chains` | Returns all template chains that have been added to the clean room. |
| `provider.view_template_chain_definition`  `consumer.view_template_chain_definition` | Returns the definition of a template chain. |
| `provider.clear_template_chain` | Drops a template chain from the clean room. |
| `provider.clear_all_template_chains` | Drops all template chains from the clean room. |
| `consumer.get_arguments_from_template_chain` | Returns the expected arguments for all of the templates in the template chain. |

Expand

Show lessSee more

For more information about these commands, see the following:

- [Snowflake Data Clean Rooms: Provider API reference guide](/user-guide/cleanrooms/provider)
- [Snowflake Data Clean Rooms: Consumer API reference guide](/user-guide/cleanrooms/consumer).
