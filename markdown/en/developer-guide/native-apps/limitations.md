# Understand limitations in the Snowflake Native App Framework

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic provides information about the limitations of Snowflake Native Apps.

## Known limitations

Snowflake Native Apps have the following known limitations:

- Temporary tables or stages are not supported.
- Some Streamlit features are not supported. See [Unsupported Streamlit features](/developer-guide/native-apps/adding-streamlit#label-streamlit-unsupported-features-na)
  for details.
- Running a Streamlit app on a container runtime is in preview and has additional limitations. For
  details, see [Limitations for container runtimes in an app](/developer-guide/native-apps/adding-streamlit#label-streamlit-container-limitations-na).
- Snowflake Native Apps do not support failover for business continuity. For example, adding an application
  package to a replication group or failover group is not supported.
- [Storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies) aren’t
  supported in Snowflake Native Apps.
- [Snowflake ML functions](/guides-overview-ml-functions) such as
  [Top Insights](/user-guide/ml-functions/top-insights) aren’t supported
  in Snowflake Native Apps.

## Known limitations in Snowflake Native Apps with Snowpark Container Services

Snowflake Native Apps with Snowpark Container Services have the following limitations:

- Support varies by cloud region and deployment type. For details, see [Support for private connectivity, VPS, and government regions](#label-native-apps-supported-clouds).
- Sessions used in connections from containers, for example using the Python connector, are limited
  to the application owner role. See
  [Snowpark Container Services: Additional considerations for services and jobs](/developer-guide/snowpark-container-services/spcs-execute-sql)
  for additional information.
- A maximum of 15 compute pools per application is allowed.
- [Cross-Cloud Auto-Fulfillment](/collaboration/provider-listings-auto-fulfillment) has the following
  limitation:

  - There is a 100GB limit for each file within the image repository.
- Using the LOG\_LEVEL, TRACE\_LEVEL, METRIC\_LEVEL, and LOG\_EVENT\_LEVEL properties in the
  manifest file to set the logging and trace level for
  a container is not supported. Instead, use the `spec.logExporters` property in the service specification file.

  See [`spec.logExporters` field (optional)](/developer-guide/snowpark-container-services/specification-reference#label-snowpark-containers-spec-reference-spec-logexporters) for more information.

## Support for private connectivity, VPS, and government regions

The following tables list Snowflake Native App support for private connectivity, Virtual Private Snowflake (VPS),
and government regions on the [cloud platform](/user-guide/intro-cloud-platforms) that
Snowflake supports:

**Amazon Web Services**

> |  | Amazon Web Services | AWS PrivateLink | Virtual Private Snowflake | Government regions |
> | --- | --- | --- | --- | --- |
> | Snowflake Native App Framework (without containers) | Generally available | Generally available | Generally available | Generally available |
> | Snowflake Native App Framework (with containers) | Generally available | Generally available | Generally available | Generally available |
>
> Expand
>
> Show lessSee more

**Microsoft Azure**

> |  | Microsoft Azure | Microsoft Azure Private Link | Virtual Private Snowflake | Government regions |
> | --- | --- | --- | --- | --- |
> | Snowflake Native App Framework (without containers) | Generally available | Generally available | Not yet supported | Generally available |
> | Snowflake Native App Framework (with containers) | Generally available | Generally available | Not yet supported | Not yet supported |
>
> Expand
>
> Show lessSee more

**Google Cloud**

> |  | Google Cloud | Google Cloud Private Service Connect |
> | --- | --- | --- |
> | Snowflake Native App Framework (without containers) | Generally available | Not yet supported |
> | Snowflake Native App Framework (with containers) | Generally available | Not yet supported |
>
> Expand
>
> Show lessSee more

## Limitations on Snowflake Native Apps in government regions

The following limitations apply to Snowflake Native App support for government regions:

- Providers publishing apps from government regions can
  only share listings within the same organization.
- Department of Defense (DoD) regions are not supported.
- Apps with containers are not yet supported in Azure government regions.

## Limitations on Virtual Private Snowflake (VPS)

The following limitations apply to Snowflake Native App support for Virtual Private Snowflake (VPS):

- Snowflake Native Apps and Streamlit are not enabled by default in Virtual Private Snowflake. To use
  Snowflake Native Apps or Streamlit in VPS, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).
- If Streamlit is not enabled in the VPS deployment, consumers cannot use the Python Permission SDK
  to manage privileges and references.
- Sharing an app from a VPS account to an account outside the VPS
  is only supported within the same organization. To share an app outside the current organization, contact
  [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).
- Only private listings are supported for applications published inside the VPS.
- Consumers in the VPS can
  [enable event sharing](https://other-docs.snowflake.com/en/native-apps/consumer-enable-logging#enable-event-sharing-for-an-app)
  for an app. However, log messages and trace events are not shared unless the provider has
  an event table within the VPS.
- Because the Snowflake Marketplace interface is not available in VPS, providers and consumers must
  manage listings by using SQL. For additional information, see [About managing listings using SQL](/progaccess/listing-progaccess-about).

## Known issue with AWS PrivateLink and Azure Private Link

Links in email notifications from apps do not correctly link into a private link account.
