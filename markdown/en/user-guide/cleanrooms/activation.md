# Activating query results

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

## Overview of activation

A collaborator can send template results outside the clean room in a process called *activation*.
The template must support activation, and each data provider must approve activation at the column level in their data offering specification.

Activation is implemented using a dedicated activation template. An activation template doesn’t return results to the query runner, but
instead writes them to a results table in the target user’s account.

Note

Activating results to another Snowflake account requires Snowflake Enterprise Edition or higher.

## Implementing activation

Here are the steps to implement activation:

1. You must use a role that has the [REGISTER DATA OFFERING privilege](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-access-management-api) to join any collaboration where you are an
   analysis runner and the collaboration specification includes an `activation_destinations` field.
2. Ensure that all specifications are properly configured:

   Data offering specCollaboration specAnalysis spec

   The [data offering specification](/user-guide/cleanrooms/spec-data-offering#label-dcr-collaboration-data-yaml) for the table with the activated column must set
   `activation_allowed: TRUE` for that column:

   Copy code

   ```
   api_version: 2.0.0
   spec_type: data_offering
   name: 2025_orders
   version: 2025_01_01_v1
   description: Activating Cleveland sales results for 2025

   datasets:
     - alias: customers
       data_object_fqn: db1.schema1.orders
       allowed_analyses: template_only
       object_class: custom
       schema_and_template_policies:
         email:
           category: join_standard
           column_type: hashed_email_sha256
           activation_allowed: TRUE
         purchase_amount:
           category: passthrough
           activation_allowed: TRUE
   ```

   The [collaboration specification](/user-guide/cleanrooms/spec-collaboration#label-dcr-collaboration-spec-yaml) must provide `activation_destinations` values for the
   analysis runner. The data offering specification further limits activation to designated analysis runners and templates.

   Copy code

   ```
   api_version: 2.0.0
   spec_type: collaboration
   name: simple_activation_collaboration
   description: Demonstrates a basic activation

   collaborator_identifier_aliases:
     advertiser_1: some_complex_identifier
     publisher_1: another_complex_identifier

   owner: publisher_1

   analysis_runners:
     advertiser_1:
       data_providers:
         advertiser_1:
           data_offerings:
             - id: customer_list
         publisher_1:
           data_offerings:
             - id: user1.2025_orders.sales
       templates:
         - id: activation_template_v0
       activation_destinations:
         snowflake_collaborators:
           - publisher_1
   ...
   ```

   The [analysis specification](/user-guide/cleanrooms/spec-analysis#label-dcr-collaboration-analysis-yaml) must include an `activation` section with
   `snowflake_collaborator` and `segment_name` values, and call an
   [activation template](/user-guide/cleanrooms/custom-templates#label-dcr-custom-templates-activation). You can’t activate results by running
   a standard analysis template.

   Copy code

   ```
   api_version: 2.0.0
   spec_type: analysis
   name: my_analysis
   description: Description of the analysis
   template: my_activation_template
   template_configuration:
     view_mappings:
       source_tables:
         - alias1.schema1.table1
         - alias2.schema2.table2
     arguments:
       join_column: ip_address
       advertiser_activation_column: purchase_amount
       publisher_activation_column: device_type
     activation:
       snowflake_collaborator: publisher_1
       segment_name: q1_2025
   ```
3. You must use an [activation template](/user-guide/cleanrooms/custom-templates#label-dcr-custom-templates-activation). This template saves results to an internal table.
   All projected columns from this template are activated.

   Any column in the template with the `activation_policy` filter applied must have `activation_allowed: TRUE`
   in the data offering specification.

   Note

   If a template doesn’t apply the `activation_policy` filter to a column, the column can be activated whether or not
   `activation_allowed: TRUE` is set for that column in the data offering spec.

   The following example shows a template with the activation policy applied to two columns supplied
   by the analysis runner:

   Copy code

   ```
   BEGIN
     CREATE OR REPLACE TABLE cleanroom.activation_data_analysis_results AS
       SELECT count(*) AS ITEM_COUNT, c.status, c.age_band
       FROM IDENTIFIER({{ my_table[0] }}) AS c
       JOIN IDENTIFIER({{ source_table[0] }}) AS p
       ON {{ c_join_col | sqlsafe | activation_policy }} = {{ p_join_col | sqlsafe | activation_policy }}
       GROUP BY c.status, c.age_band
       ORDER BY c.age_band;
     RETURN 'analysis_results';
   END;
   ```

   Note

   This example writes to a fixed results table name. To run multiple activations against the same clean room concurrently, use a template that
   generates a unique results table name for each run; otherwise the concurrent `CREATE OR REPLACE TABLE` statements collide and runs fail. See
   [Running activations concurrently](/user-guide/cleanrooms/custom-templates#label-dcr-custom-templates-activation-concurrency).
4. The analysis runner calls RUN to run the analysis and activate the results.

   - **If activating to yourself**, results are available immediately in the caller’s account.
   - **If activating to another collaborator:**
     1. The collaborator calls VIEW\_ACTIVATIONS until it returns a status of SHARED.
        Activating to another account can take considerable time for large result sets, as the data must be shared to the
        collaborator’s account. Cross-cloud collaborators will also experience additional delays due to replication frequency settings.
     2. When the status of the activation is SHARED, the collaborator calls PROCESS\_ACTIVATION to send the results to their account.
        The response to PROCESS\_ACTIVATION includes the table and segment names. This sets the activation status to PROCESSED.
5. The analysis runner can read results as described in the next section.

## Reading the activation results

When activation is complete, as described in the previous section, results are stored in the
`collaboration_name.activation.segment_records` table in your account.

The table has the following schema:

| Column | Description |
| --- | --- |
| BATCH\_ID | UID for the batch job that was processed. |
| SEGMENT\_NAME | Name for the activation payload. |
| TEMPLATE\_ID | ID of the template used for activation. |
| SHARED\_BY | Name of the collaborator who activated the data. |
| UPDATED\_ON | Timestamp of when the batch was processed successfully. |
| RECORDS | Payload of activated IDs and attributes from the activation template. |

Expand

Show lessSee more

Note

If a collaborator leaves the clean room, they lose access to the application, including the table that contains the activated results.

To retrieve the activation results, run the following SQL command, optionally filtering by segment name:

Copy code

```
SELECT *
  FROM <collaboration_name>.activation.segment_records
    [WHERE segment_name = '<segment_name>'];
```
