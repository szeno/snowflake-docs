# Update billing contact information

Snowflake customers can manage billing contact information for their account directly in Snowsight.

## Required Role

- To manage billing contact information, you must use the [Organization Administrator](/user-guide/organization-administrators)
  (**ORGADMIN**) role.

## Billing contact management restrictions

The fields you can edit vary based on whether your account uses an **On-Demand** or **Capacity** payment model.

| Customer Type | Editable Fields |
| --- | --- |
| **On-Demand, Self-Service (ODSS)** | Can edit billing contact details and billing email addresses. |
| **Capacity** | **Email only.** |

Expand

Show lessSee more

## Marketplace account restrictions

Customers with Snowflake Marketplace accounts have specific limitations when editing information on the **Contacts** tab.

| Customer Type | Editable Fields |
| --- | --- |
| **Marketplace Provider (ODSS)** | **Email only.** Name and address fields cannot be updated via Snowsight. |
| **Marketplace Consumer (ODSS)** | **Country and Email only.** |
| **Non-ODSS Marketplace** | **Email only.** |

Expand

Show lessSee more

## Edit billing contact information

To edit your Snowflake billing contact information:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Admin** » **Billing**.
3. On the **Billing and Payments** page, select the **Contacts** tab.
4. Find the field that you want to edit, and select [![Pencil icon](/static/images/snowsight/icons/pencil-icon.svg)](/static/images/snowsight/icons/pencil-icon.svg).
5. Type your updated information.

   If you are updating email addresses, you can update multiple email addresses at the same time. The list can be comma-separated or
   space-separated. For example, `updated-usage@snowflake.com, existing-usage@snowflake.com`.

   Tip

   Snowsight might suggest information that matches existing addresses when you update address information. You can accept
   (select) or ignore such suggestions.
6. Update other fields, as necessary.
7. Select **Save** to save all updates.

### Receiving notification of changes

Snowflake notifies customers who update billing information about the change by sending an email message to the current email addresses
shown in the **Usage emails** and **Invoices emails** fields on the **Billing communication** card. If a customer changes the email address
in a specific email address field, Snowflake sends an email message to both the previous and current email addresses entered in that field.

Snowflake sends notification emails to customers about successful and unsuccessful update attempts. Unsuccessful update attempts also
generate a banner in Snowsight, which remains visible for up to 35 days or until the next update attempt.

## Usage notes

- Updates to billing contact information might take several minutes to process.
- Pending updates appear as **In-progress** in Snowsight.
