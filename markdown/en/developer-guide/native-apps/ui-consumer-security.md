# Consumer security best practices for an app with containers

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic provides security guidelines for consumers when running a Snowflake Native App.

## Consumer security best practices

Consumers have a shared responsibility for ensuring the security of their data and the safe
use of a Snowflake Native App with Snowpark Container Services. The following best practices help to ensure the security of an app:

- Review the app’s listing, documentation, and security certification before installing the app.
- Grant the minimum privileges required for an app.
- Grant access only to the specific tables and views that the app requires to function correctly.
- Periodically review and modify the privileges to ensure that the minimum required privileges
  are granted to the app.
- Immediately report any suspected security incidents to Snowflake and the app provider.
- Ensure the secure configuration of the consumer network environment and access controls.
- Review [network controls](/developer-guide/native-apps/security-na-spcs#label-native-apps-security-spcs-network-isolation),
  [network configurations](/developer-guide/snowpark-container-services/service-network-communications#label-working-with-services-jobs-ingress),
  and [limitations of Snowpark Container Services](/developer-guide/snowpark-container-services/spcs-guidelines-and-limitations)
  and ensure only trusted endpoints are accessible to an app.
- Regularly update and patch systems and software to maintain a secure posture.
- Educate users on the secure use of apps with containers and the importance of data protection.

## Mitigate data exfiltration risks

Despite the security features of a Snowflake Native App, Snowflake cannot guarantee the security of
a third-party app. Consumers are responsible for ensuring the security of their data.

Snowflake recommends the following policies as part of a comprehensive security program to mitigate
data exfiltration and other security risks. This is important when using an app with containers
provided by third parties that implement services and ingress.

- Carefully review app listings, documentation, and security certifications before deploying apps.
- Ensure security controls outlined in Snowflake documentation are appropriate for your use case and
  environment.
- Configure app privileges and access controls to use only the minimum privileges required
  by an app.
- Regularly review and adjust privileges to maintain this principle and disable unused features.
- Use a modern, up-to-date browser with security features, for example the latest versions of
  Chrome, Firefox, or Safari.
- Ensure that your browser settings are configured to block pop-ups and protect against potential
  vulnerabilities.
- Ensure that network rule configurations conform to the expected behavior of the app. When a Snowflake Account URL is
  added to an external access integration, communication is not limited to a specific account. Traffic can be routed to different
  accounts based on access methods. Consumers should avoid adding account URLs if possible communication with other Snowflake accounts
  is unacceptable.
