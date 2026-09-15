# Private connectivity for inbound network traffic

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Your connection to Snowflake can be routed over the public Internet or through a private IP address associated with the cloud platform that
hosts your Snowflake account. By using your cloud platform’s private connectivity solution to create private endpoints, you can harden your
security posture so that inbound network traffic uses private connectivity when accessing the following features:

- [To the Snowflake Service](#label-private-connect-snowflake-service)
- [To Snowsight](#label-private-connect-ui)
- [To Streamlit in Snowflake](#label-private-connect-streamlit)
- [To internal stages](#label-private-connect-internal-stages)
- [To Snowflake-managed storage volumes](#label-private-connect-managed-volumes)
- [To Snowpark Container Services](#label-private-connect-spcs)
- [To Snowflake CoWork](#label-private-connect-si)

## To the Snowflake Service

When the routing is through a private IP address *from your VPC or VNET to the Snowflake VPC or VNet*, that is *private
connectivity to the Snowflake Service*. These connections use [AWS PrivateLink](/user-guide/admin-security-privatelink),
[Azure Private Link](/user-guide/privatelink-azure), or
[Google Cloud Private Service Connect](/user-guide/private-service-connect-google). The service depends on the cloud platform that
hosts your Snowflake account.

## To Snowsight

To use private connectivity to access Snowsight, see [Configuring private connectivity for Snowsight](/user-guide/ui-snowsight-gs#label-ui-snowsight-config-private-connectivity).

After private connectivity is configured, users can [sign in using private connectivity](/user-guide/ui-snowsight-gs#label-ui-snowsight-gs-private-connectivity).

## To Streamlit in Snowflake

To access Streamlit in Snowflake with AWS PrivateLink, Azure Private Link, or Google Cloud Private Service Connect, see [Private connectivity for Streamlit in Snowflake](/developer-guide/streamlit/object-management/privatelink).

## To internal stages

You can use private connectivity to connect to Snowflake internal stages. For information, see the following:

- [AWS VPC interface endpoints for internal stages](/user-guide/private-internal-stages-aws)
- [Azure private endpoints for internal stages](/user-guide/private-internal-stages-azure)
- [Google Private Service Connect endpoints for internal stages](/user-guide/private-internal-stages-gcp)

## To Snowflake-managed storage volumes

You can use private connectivity to connect to Snowflake-managed storage volumes for Apache Iceberg tables. For information, see
the following:

- [AWS VPC interface endpoints for Snowflake-managed storage volumes](/user-guide/private-managed-volumes-aws)
- [Azure private endpoints for Snowflake-managed storage volumes](/user-guide/private-managed-volumes-azure)

## To Snowpark Container Services

You can use private connectivity to connect to Snowpark Container Services. For information, see [Inbound connectivity](/developer-guide/snowpark-container-services/private-connectivity#label-spcs-private-connectivity-inbound).

## To Snowflake CoWork

You can use private connectivity to connect to Snowflake CoWork. For information, see [Configure Snowflake CoWork with private connectivity](/user-guide/snowflake-cortex/snowflake-cowork/deploy-agents#label-snowflake-cowork-configure-privatelink).
