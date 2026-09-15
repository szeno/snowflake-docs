# Amazon Virtual Private Cloud ID for external stage, external function, and external volume

As part of Snowflake’s continued commitment to enhance control over data leaving Snowflake,
we are migrating our egress control points to a new Amazon Virtual Private Cloud (VPC).
This will result in a change to the Amazon VPC ID used by Snowflake when
making outbound connections for external functions, external stages, and external volumes.

Note

Customers using [Amazon S3-compatible storage](/user-guide/data-load-s3-compatible-storage)
should confirm if they have any policies that may be affected by this change, and update their policies accordingly.

Customers who filter traffic coming into their API Gateways or S3 stages based on the published VPC ID,
will need to update their policies to include the new VPC ID.

To obtain the full list of VPC IDs that need to be allowlisted, customers should
run the [SYSTEM$GET\_SNOWFLAKE\_PLATFORM\_INFO](/sql-reference/functions/system_get_snowflake_platform_info) function.

## Behavior change

Before the change:
:   The output of [SYSTEM$GET\_SNOWFLAKE\_PLATFORM\_INFO](/sql-reference/functions/system_get_snowflake_platform_info) does not contain the `snowflake-egress-vpc-ids` property.

After the change:
:   The output of the SYSTEM$GET\_SNOWFLAKE\_PLATFORM\_INFO function contains a new property `snowflake-egress-vpc-ids` which includes
    `id`, `expires`, and `purpose` child properties.

The output of the function resembles:

```
{
  "snowflake-vpc-id": ["<existing VPC ID>"],
  "snowflake-egress-vpc-ids": [
    {
      "id": "<existing VPC ID>",
      "expires": "2025-03-01T00:00:00",
      "purpose": "generic"
    },
    {
      "id": "<new VPC ID>",
      "expires": "2025-03-01T00:00:00",
      "purpose": "generic"
    }
  ]
}
```

Customers should examine the `id` field within the `snowflake-egress-vpc-ids`
property and note `id` values marked as `"purpose":"generic"`.
`generic` IDs are VPC IDs which will need to be allowlisted to support core Snowflake functionality.

This change becomes effective during the week of February 24 2025.

Note

The function returns a list of VPC IDs: the currently used VPC ID and new VPC ID(s).
VPC IDs from `snowflake-vpc-id` will be duplicated in `snowflake-egress-vpc-ids` but marked as `"purpose":"generic"`.
All VPC IDs with the generic purpose must be allowlisted in the policies.

The `expires` property specifies the date and time until which the associated VPC ID is guaranteed to remain valid.
Customers should update any automation or processes to query the function before the
expiration date to ensure they have the latest information about the current VPC IDs.

Output VPC IDs are stable and their expiration dates are automatically updated and extended.

While Snowflake may need to change VPC IDs in the future, there are no plans to change before March 31, 2025.
This information is primarily for future reference.

The following changes must be made to continue to access the following Snowflake features:

External stage and volumes:
:   Follow the instructions in [Allowing the Virtual Private Cloud IDs](/user-guide/data-load-s3-allow) to specify VPC IDs for external stages or external volumes.

External functions:
:   Follow the instructions in [Secure your Amazon API Gateway endpoint](/sql-reference/external-functions-creating-aws-ui-proxy-service#label-secure-your-proxy-service-endpoint-aws) to specify VPC IDs for external functions.

## Timeline

Stage one:
:   Starting the week of February 24, 2025, [SYSTEM$GET\_SNOWFLAKE\_PLATFORM\_INFO](/sql-reference/functions/system_get_snowflake_platform_info)
    function will be updated across all AWS deployments to include the new egress VPC IDs under the
    `snowflake-egress-vpc-ids` element. Customers can begin updating their S3 and API Gateway policies to allowlist these new VPC IDs.

Stage two:
:   Starting the week of June 9, 2025 (previously May 24, 2025), Snowflake will start a gradual
    transition to using the new VPCs for external stages, external functions, and external volumes.
    Customers must ensure their S3 and API Gateway policy updates are completed by this date.

Stage three:
:   Starting the week of February 15, 2026, old VPC-IDs will no longer be available.
    If you encounter any issues while connecting, update to the new VPC-ID for external stages, external functions, and external volumes.

    Additionally, you must ensure their S3 and API Gateway policies are updated with the new VPC-ID.

For any issues, or concerns, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## Frequently asked questions

### How can I find S3 buckets for external stages that can be impacted by this change?

Using the ACCOUNTADMIN role, execute the following query to identify the external stages that are affected by the change:

Copy code

```
USE ROLE ACCOUNTADMIN;

SELECT stage_url, stage_region, stage_owner, stage_catalog, stage_schema
  FROM SNOWFLAKE.ACCOUNT_USAGE.STAGES
  WHERE STARTSWITH(stage_url, 's3')
    AND stage_url IS NOT NULL
    AND deleted IS NULL;
```

### How can I find API Gateways that can be impacted by this change?

Using the ACCOUNTADMIN role, execute the following query to identify the S3 gateways that are affected by the change:

Copy code

```
USE ROLE ACCOUNTADMIN;

SELECT function_name, function_definition, function_owner, function_catalog, function_schema
  FROM SNOWFLAKE.ACCOUNT_USAGE.FUNCTIONS
  WHERE function_language = 'EXTERNAL'
    AND function_definition ILIKE '%.execute-api.%.amazonaws.com%'
    AND deleted IS NULL;
```

### How can I find S3 buckets for external volume that can be impacted by this change?

Using the ACCOUNTADMIN role, execute the following query to identify the S3 buckets that are affected by the change:

Copy code

```
use role accountadmin;

DECLARE
res1 RESULTSET;
res2 RESULTSET;
sql_vol VARCHAR;
rpt VARIANT;
rpt_int VARIANT;
BEGIN
  rpt := object_construct();
  sql_vol := 'SELECT PROPERTY, VALUE:"NAME"::VARCHAR as NAME, VALUE:"STORAGE_ALLOWED_LOCATIONS"::VARCHAR as S3_PATH FROM (
SELECT PARSE_JSON(T."property_value") AS VALUE, T."property" as PROPERTY
FROM TABLE(RESULT_SCAN(last_query_id())) T
WHERE T."property_type" = \'String\'
AND T."property" != \'ACTIVE\'
AND VALUE:"STORAGE_PROVIDER"=\'S3\')
;';
  show external volumes;
  LET c1 CURSOR FOR SELECT * FROM TABLE(RESULT_SCAN(last_query_id()));
  OPEN c1;
  FOR record IN c1 DO
    res1 := (execute immediate 'describe external volume ' || record."name");
    res2 := (execute immediate :sql_vol);
    rpt_int := object_construct();
    let c2 CURSOR for res2;
    open c2;
    for inner_record in c2 do
        rpt_int := object_insert( rpt_int, inner_record.NAME, inner_record.S3_PATH);
    end for;

    rpt := object_insert( rpt, record."name", rpt_int );
  END FOR;
  RETURN rpt;
END;
```

### How can I find AWS policies that may contain the current Snowflake VPC ID?

To identify policies potentially affected by the change, use the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

1. Run [SYSTEM$GET\_SNOWFLAKE\_PLATFORM\_INFO](/sql-reference/functions/system_get_snowflake_platform_info) command and note VPC ID returned in snowflake-vpc-id.
2. Run the following script to list the ARNs of IAM policies and the API IDs of API Gateways that contain resource policies with the current Snowflake VPC ID. Please note, running the script may take time.
3. Review the listed policies and determine which ones need to be updated to include additional VPC ID(s), as per the instructions above.

Copy code

```
SNOWFLAKE_VPC_ID="<VPC ID returned in snowflake-vpc-id>"

# List ARNs of IAM policies that contain the current Snowflake VPC ID.
aws iam list-policies --scope Local --query 'Policies[*].Arn' --output text | tr '\t' '\n' | while read -r policy_arn; do
  version_id=$(aws iam get-policy --policy-arn "${policy_arn}" --query 'Policy.DefaultVersionId' --output text)
  aws iam get-policy-version --policy-arn "${policy_arn}" --version-id "${version_id}" | grep -q "${SNOWFLAKE_VPC_ID}" && echo "${policy_arn}"
done

# List API IDs of API Gateways that contain resource policies with the current Snowflake VPC ID.
aws apigateway get-rest-apis --query 'items[*].id' --output text --profile | tr '\t' '\n' | while read -r api_id; do
  aws apigateway get-rest-api --rest-api-id "${api_id}" --query 'policy' --output text | grep -q "${SNOWFLAKE_VPC_ID}" && echo "${api_id}"
done
```

Ref: 1910
