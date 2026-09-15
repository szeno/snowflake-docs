# Offer manifest reference

Creating Snowflake offers programmatically requires a manifest, written in YAML (<https://yaml.org/spec/>). Use the information provided here to learn about the parameters available in the offer manifest.

## Offer manifest

Copy code

```
#
# Offer manifest
#
access_start_date_preference: <preferred_offer_start_date>
comment: <offer_comments>
contract_type: <contract_type>
contract_duration_months: <the_contract_duration_in_months>
invoice_end_time: <invoice_end_date_and_time>
invoice_start_date_preference: <preferred_invoice_start_date>
invoice_start_time: <invoice_start_time>
is_default: <is_a_default_offer_included_with_the_pricing_plane>
offer_display_name: <offer_display_name>
offer_expiration_time: <offer_expiration_time>
payment_terms:
  payment_type: <pricing_plan_payment_method>
  installment_schedule: <pricing_plan_installment_schedule>
  allowed_payment_methods: <allowed_payment_methods>
pricing_plan_name: <the_pricing_plan_name>
access_end_time: <listing_access_end_time>
access_start_time: <listing_access_start_time>
discount: <the_offer_discount>
target_consumer: <offer_target_consumer>
terms_of_service:
  type: <terms_of_service_type>
  custom_link: <link_to_custom_terms_of_service>
additional_information: <additional_offer_information>
attachments:
  - attachment_path: <stage_path_to_pdf>
```

## Offer parameters

The parameters within the offer manifest allow you to create offers that meet your specific business requirements. Required and optional parameters are identified.

access\_start\_date\_preference
:   Required. String. The preferred offer start date. Accepted values are SPECIFIC\_DATE or OFFER\_ACCEPTED\_DATE.

comment
:   Optional. String. Comments about the offer that are only visible to providers.

contract\_type
:   Required. String. The contract type. Accepted values are SUBSCRIPTION or LIMITED\_TIME.

contract\_duration\_months
:   Required. Long. The contract duration in months.

invoice\_end\_time
:   Required. Long. Invoice end date and time in milliseconds since Unix epoch.

invoice\_start\_date\_preference
:   Required. String. The preferred invoice start date. Accepted values include the following:

    - `OFFER_ACCEPTED_DATE`: Use with flat-fee plans.
    - `SPECIFIC_DATE`: Use with flat-fee plans or (less commonly) with usage-based plans.
    - `FIRST_DAY_NEXT_MONTH`: Use with flat fee plans or with new usage-based plans.
    - `TWO_DAYS_AFTER_OFFER_ACCEPTED_DATE`: Use when allowing a consumer to accept a new usage-based plan that replaces an existing
      usage-based plan. In this case, it can take up to 2 days for the new usage-based pricing plan to take effect.

invoice\_start\_time
:   Required. Long. The time the invoice was created.

is\_default
:   Required. Boolean. When TRUE, specifies that a default offer is included with the pricing plan. The default is FALSE.

offer\_display\_name
:   Optional. String. The offer name visible to consumers.

offer\_expiration\_time
:   Optional. Long. The offer expiration time.

payment\_terms
:   Required. Provides additional pricing plan parameters. You can specify the following parameters.

    `payment_type``installment_schedule``allowed_payment_methods`

    String. The pricing plan payment types. Accepted values are INVOICE and CREDIT\_CARD.

    String. The pricing plan installment schedule.

    List. The allowed pricing plan payment methods. Accepted values are INVOICE and CREDIT\_CARD.

pricing\_plan\_name
:   Required. String. The pricing plan name.

access\_end\_time
:   Required. Long. The time the consumer loses access to a trial listing.

access\_start\_time
:   Required. Long. The time a consumer can access a listing.

discount
:   Optional. Double. The offer discount.

target\_consumer
:   Optional. String. The target consumer for the offer. The format is `organization_name.account_name`.

terms\_of\_service
:   Required. Provides additional pricing plan terms of service. You can specify the following parameters.

    `type``custom_link`

    String. The terms of service type. Accepted values are CUSTOM, DEFAULT, and OFFLINE.

    String. A link to custom terms of service.

additional\_information
:   Optional. Additional offer information.

attachments
:   Optional. List. PDF files to attach to a private offer. Consumers can download these files when viewing the offer. You can specify the following field.

    `attachment_path`

    String. The path to a PDF file in the listing stage. Must follow the format `offers/<offer_name>/attachments/<filename>.pdf`.

    Each offer supports up to 5 PDF attachments, with a maximum size of 5 MB per file. The total size of all attachments across all offers in a listing cannot exceed 50 MB.

## Examples

The following example defines a limited-time offer that’s tied to a PRICING\_PLAN\_V2 pricing plan.

Copy code

```
version: V2
contract_type: LIMITED_TIME
contract_duration_months: 12
display_name: OFFER_V2
is_default: true
payment_terms:
  payment_type: FULL
state: PUBLISHED
sales_motion: SELF_SERVE
pricing_plan_details:
  type: DEFAULT
  name: PRICING_PLAN_V2
metadata:
  description: sample-description
  price: 100
  button_text: button-text
  value_propositions:
    - val 1
    - val 2
```
