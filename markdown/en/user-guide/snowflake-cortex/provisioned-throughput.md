# Provisioned Throughput

## Overview

Use Provisioned Throughput to reserve throughput for managed inference on Snowflake Cortex.
You specify throughput size as provisioned throughput units (PTU), and Cortex allocates the required capacity for a one-month term.
You can use the PTUs in your REST API calls for a consistent end-user experience. The functionality is available for the following models in the AWS and Azure Clouds:

- Mistral Large 2
- Llama 3.1-405B
- Llama 3.1-70B
- Llama 3.1-8B
- Snowflake-Llama3.3-70B
- Snowflake-Llama3.1-405B

## Access control requirements

Users must use a role that has been granted the SNOWFLAKE.CORTEX\_USER database role with USAGE privilege on the PT ID.
For more information about this privilege, see [Privileges](#label-provisioned-provisioned-throughput-privileges).

### Privileges

The following sections describe the privileges required to create, manage, and use provisioned throughput.

#### Creating a provisioned throughput

To create a provisioned throughput, you must use a role that has been granted the account-level CREATE PROVISIONED THROUGHPUT privilege.
By default, ACCOUNTADMIN is the only role that can create the provisioned throughput.
You can use the ACCOUNTADMIN role to grant the CREATE PROVISIONED THROUGHPUT privilege to another role.

Use the following SQL command to grant the privilege to create a provisioned throughput:

Copy code

```
GRANT CREATE PROVISIONED THROUGHPUT ON ACCOUNT TO ROLE <role>
```

Provisioned Throughput is a schema-level object.
A role with the CREATE PROVISIONED THROUGHPUT privilege can create a provisioned throughput in any schema where it has the USAGE privilege.

The role that you used to create the provisioned throughput is automatically granted the OWNERSHIP privilege on the provisioned throughput.
The OWNERSHIP privilege allows you to rename or drop the provisioned throughput.

#### Giving roles the privilege to use a provisioned throughput

Grant roles with the USAGE privilege on the provisioned throughput. The USAGE privilege provides roles with ability to make REST API or SQL calls with a provisioned throughput ID.

The following SQL command grants the USAGE privilege on a provisioned throughput:

Copy code

```
GRANT USAGE ON PROVISIONED THROUGHPUT <pt_id> TO ROLE <role>
```

#### Using a provisioned throughput

A role with USE or OWNERSHIP privilege on a provisioned throughput can use the provisioned throughput for inference.
For information about the privileges required to use a provisioned throughput, see [Provisioned Throughput privileges](/user-guide/security-access-control-privileges#label-provisioned-throughput-privileges).

## Minimum Provisioned Throughput Unit requirements

Provisioned Throughput is subject to minimum and incremental PTU requirements. Each model or feature in the Minimum PTUs column shows the minimum number of PTUs that you must request. If you request fewer PTUs than the minimum, your request is rejected.

If you need more throughput than the minimum PTUs offer for the model, you need additional PTUs. The Increment PTUs column shows the PTU increments in excess of the Minimum PTUs that you can request.
Requests must specify PTUs such that the amount exceeding the minimum is a whole integer multiple of the increment; otherwise, the request is rejected.

The table below lists the available models, the minimum PTUs required for each model, and the increment requirements for additional PTUs beyond the minimum.

**Provisioned Throughput - Complete REST API**

| Model | Minimum PTUs | Increment PTUs |
| --- | --- | --- |
| Mistral Large 2 | 256 | 128 |
| Llama 3.1-405B | 512 | 256 |
| Llama 3.1-70B | 128 | 64 |
| Llama 3.1-8B | 64 | 32 |
| Snowflake-Llama3.3-70B | 128 | 64 |
| Snowflake-Llama3.1-405B | 512 | 256 |

Expand

Show lessSee more

## Determining PTU size

The PTUs required for your application depend on the workload profile.
For example, on Llama 3.1-8B, a workload with 500 requests per minute (RPM) and 500 tokens per request output has a minimum of 64 PTUs.
It delivers 960K tokens of throughput per minute. If you need more throughput, you can request additional PTUs in increments of 32.

When you’re starting out, you can use the minimum PTUs for the model and add increments as needed.

## Cost considerations

For the duration of your Provisioned Throughput term, you consume Credits per PTU per hour at the rate listed in the [Snowflake Credit Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf). You incur charges for the allocated PTUs regardless of your actual usage during the term. The term starts and ends at 8:00 a.m. PT for the dates provided in the provisioned throughput creation.

Provisioned Throughput does not renew automatically. To reserve throughput for another term, see the following section.

## Reserving throughput

This tutorial guides you through the process of reserving and using provisioned throughput in a REST API call for the Cortex COMPLETE function.

### Step 1: Create a provisioned throughput ID

To get started with provisioned throughput, use SQL to create a request with the following information:

- The cloud provider
- The model
- The number of PTUs
- The start of the term (period of the provisioned throughput’s availability)
- The end of the term (period of the provisioned throughput’s availability)

The following examples create the *my\_pt* provisioned throughput resource on AWS, specifying the model *llama3.1-8B*, allocating 64 provisioned throughput units (PTUs) from April 15, 2025, to May 15, 2025.

Copy code

```
CREATE PROVISIONED THROUGHPUT my_pt CLOUD_PROVIDER='aws', MODEL='llama3.1-8B', PTUS=64, TERM_START='2025-04-15' TERM_END='2025-05-15'
```

The provisioned throughput ID (PT ID) is in the response.

### Step 2: Open a support case to allocate the provisioned throughput

After you create an ID, create a support ticket with Snowflake Support to enable Provisioned Throughput.
In the ticket, provide your [Account identifiers](/user-guide/admin-account-identifier) and the PT ID. We recommend creating the ticket seven business days before the start of the term to ensure that the throughput is reserved when needed.

### Step 3: Check the status of the provisioned throughput

After you create the support ticket, you can check on the status of the provisioned throughput using the following command.

Copy code

```
DESCRIBE PROVISIONED THROUGHPUT my_pt
```

This command returns one of the following states:

- REQUESTED: PT request received, but capacity not allocated yet.
- APPROVED: PT is enabled and will be ACTIVE on the specified start date.
- ACTIVE: PT is now available for use.
- EXPIRED: PT is no longer available for use or was not enabled before the term start.

### Step 4: Use the Provisioned Throughput ID in your REST API calls

After the PT is in the ACTIVE state, you can use it in your [AI\_COMPLETE](/sql-reference/functions/ai_complete) REST API calls. To use the provisioned throughput in the inference request, specify the PT ID in the API call.
Using provisioned throughput in the request doesn’t change the behavior of the API.

The following example shows how to use the PT ID in a COMPLETE REST API call:

Copy code

```
curl --location 'https://some-account-identifier.snowflakecomputing.com/api/v2/cortex/inference:complete' \
--header 'X-Snowflake-Authorization-Token-Type: KEYPAIR_JWT' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--header 'Authorization: ••••••' \
--data '{
  "model": "snowflake-llama-3.1-8b",
  "messages": [
  {
      "content": "Write an essay on the benefits of provisioned throughput."
  }
  ],
  "provisioned_throughput_id": "f3a27d60-f61f-4247-8aa3-6272ea0d7a8d"
}'
```

Note

The role that you use to make the REST API call must have the USE privilege on the provisioned throughput ID.
For more information about the required privileges, see [Provisioned Throughput privileges](/user-guide/security-access-control-privileges#label-provisioned-throughput-privileges).

### Termination

The provisioned throughput stops processing inference requests after the term expires.
If you’re using Provisioned Throughput for API requests after the term expires, you must create a new Provisioned Throughput ID and use it in your requests.
