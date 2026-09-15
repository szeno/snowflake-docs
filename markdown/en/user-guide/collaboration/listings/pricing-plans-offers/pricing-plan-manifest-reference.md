# Pricing plan manifest reference

Creating Snowflake pricing plans programmatically requires a manifest, written in YAML (<https://yaml.org/spec/>). Use the information provided here to learn about the parameters available in the pricing plan manifest.

## Pricing plan manifest

Copy code

```
#
# Pricing plan manifest
#
pricing_plan_display_name: <pricing_plan_name>
currency: <three_letter_currency_code>
pricing_model: <pricing_plan_pricing_model>
usage_details:
  free_units: <number_of_free_monthly_queries>
  free_unit_kind: <free_unit_kind>
  usage_unit_price: <price_per_unit>
  usage_unit_kind: <usage_unit_kind>
  max_fee: <maximum_fee_per_month>
billing_events:
   class: <class_name>
   display_name: <billing_event_display_name>
   billing_quantity: <price_per_unit>
   billing_unit: <display_units>
   description: <description_for_the_billing_event>
compute_pool_surcharge:
   surcharge_type: <surcharge_type>
   compute_pool_rates:
    - identifier_type: <compute_pool_type>
      identifier_name: <compute_pool_name>
      surcharge_price: <price_per_credit>
      description: <compute_pool_rate_description>
    - identifier_type: <compute_pool_type>
      identifier_name: <compute_pool_name>
      surcharge_price: <price_per_credit>
      description: <compute_pool_rate_description>
base_fee: <monthly_fixed_fee>
billing_duration: <billing_duration_in_months>
sales_motion: <pricing_plan_type>
comment: <a_note_visible_only_to_the_provider>
metadata:
  description: <pricing_plan_description>
  price_prefix: <pricing_plan_prefix>
  pricing_unit: <%sf-web-interface%_pricing_plan_pricing_unit>
  button_text: <%sf-web-interface%_button_text>
  index: <%sf-web-interface%_pricing_plan_index>
  value_propositions: <pricing_plan_value_proposition>
visibility: <pricing_plan_visibility>
#
# Default offer fields
#
contract_type: <pricing plan contract type>
contract_duration_months: <pricing plan contract duration>
```

## Pricing plan parameters

The parameters within the pricing plan manifest allow you to create pricing plans that meet your specific business requirements. Required and optional parameters are identified.

pricing\_plan\_display\_name
:   Required. String. The pricing plan name that is visible to providers and consumers.

currency
:   Required. String. The three-letter currency code for the pricing plan. The default is USD.

pricing\_model
:   Required. String. The pricing model for the pricing plan. The available values are FLAT\_FEE and USAGE\_BASED. For more information about pricing models, see [Paid Listings Pricing Models](https://other-docs.snowflake.com/collaboration/provider-listings-pricing-model).

usage\_details
:   Optional. Defines pricing plan usage limitations. You can specify the following optional parameters.

    `free_units``free_unit_kind``usage_unit_price``usage_unit_kind``max_fee`

    Long. The number of queries a consumer can make without incurring a monthly usage fee.

    String. The free unit type. The accepted value is QUERY.

    Double. The price per unit kind.

    String. The usage unit type. The accepted value is QUERY.

    Double. The maximum fee a consumer can be charged monthly. The accepted value is QUERY.

billing\_events
:   Optional. Defines consumer billing events. You can specify the following optional parameters.

    `class``display_name``billing_quantity``billing_unit``description`

    String. The billing class name.

    String. The billing event name.

    Double. The price per unit.

    String. The billing unit to display.

    String. The billing event description.

compute\_pool\_surcharge
:   Optional. Defines rates for compute pool use. You can specify the following optional parameters.

    `surcharge_type``compute_pool_rates`

    String. The compute pool surcharge type. The accepted values are HOUR or CREDIT.

    String. Defines the rates charged for compute pool access. You can specify the following parameters.

    `identifier_type``identifier_name``surcharge_price``description`

    String. The compute pool identifier type. The accepted value is COMPUTE\_POOL\_NAME.

    String. The compute pool identifier name. This value must be identical to the name of the compute pool being used in the app.

    Double. The price per compute pool credit when the value is CREDIT, or the price per compute hour when the value is HOUR. When a compute node is started or resumed, a minimum of 5 minutes worth of Snowflake credits are consumed. After a compute node is started or resumed, virtual warehouses and compute nodes are charged on a per second basis, rounded up to the nearest whole second.

    String. The compute pool description.

base\_fee
:   Required. Double. The pricing plan monthly fixed fee.

billing\_duration
:   Required. Long. The pricing plan duration in months.

sales\_motion
:   Required. String. The pricing plan type. The accepted values are SELF\_SERVE and TALK\_TO\_SALES.

comment
:   Optional. String. Pricing plan information that is visible only to a provider.

metadata
:   Optional. Provides additional pricing plan information. You can specify the following optional parameters.

    `description``price_prefix``pricing_unit``button_text``index``value_propositions`

    String. A description of the pricing plan.

    String. The prefix for pricing plan pricing.

    String. The pricing plan pricing unit to display in Snowsight.

    String. The text to display on the Snowsight pricing plan button.

    String. The pricing plan index displayed in Snowsight.

    String. The pricing plan value proposition.

visibility
:   Required. String. Defines pricing plan visibility. The accepted values are VISIBLE and HIDDEN.

contract\_type
:   Required. String. The pricing plan contract type. The accepted values are SUBSCRIPTION and LIMITED\_TIME.

contract\_duration\_months
:   Required. Long. The pricing plan contract duration in months.

## Examples

The following example defines a flat-fee, self-serve pricing plan.

Copy code

```
display_name: Default pricing plan display name
currency: USD
pricing_model: FLAT_FEE
base_fee: 100.0
billing_duration_months: 1
sales_motion: SELF_SERVE
comment: Comment for the pricing plan
metadata:
  description: Pricing plan description
  price: $100 / unit
  button_text: Buy Now
  value_propositions:
    - val 1
    - val 2
visibility: VISIBLE
contract_type: LIMITED_TIME
contract_duration_months: 12
state: PUBLISHED
```
