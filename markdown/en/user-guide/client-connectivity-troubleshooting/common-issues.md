# Common connectivity issues and resolutions

This topic outlines the steps for troubleshooting connectivity issues that are likely to be the root cause of the [common error messages](/user-guide/client-connectivity-troubleshooting/error-messages).

## Firewall or proxy SSL inspection issues

Snowflake does not support the alteration or modification of the TLS/SSL certificates for its services. Please work with your network administrator to ensure that all service endpoints returned by the [allowing the URLs](/user-guide/hostname-allowlist) function have full passthrough access through your network.

If you have unique requirements specific to your network environment security that require further discussion on this topic, contact your account team.

## OCSP and port 80 issues

All communications with Snowflake use port 443. However, OCSP certification checks are transmitted over port 80. If port 80 is not open in your network, you might experience OCSP-related issues, which can be accompanied by an error mentioning OCSP (such as [JDCB Error 5](/user-guide/client-connectivity-troubleshooting/error-messages#label-jdbc-connectivity-error-5)). In these scenarios, your organization’s system or network administrator needs to open the firewall to traffic on ports 443 and 80 and to ensure that all URLs in the [Snowflake allowlist](/user-guide/hostname-allowlist) are allowed.

Note

No customer data is transferred over unencrypted HTTP; it is strictly data related to the OCSP operations. Also, note that Snowflake does not provide or maintain the OCSP Responders. The OCSP Cache Server is an exception, which is provided and operated by Snowflake.

If the issue persists after enabling port 80, try deleting all OCSP-related temporal cache files and retry connecting based on your operating system:

- Windows: `${HOME}/AppData/Local/Snowflake/Caches`
- MacOS: `${HOME}/Library/Caches/Snowflake`
- Linux: `${HOME}/.cache/snowflake`

## Fetching large query result sets failures

At times, your client can fetch small query results but struggles with large ones because retrieving large results (over 100KB) requires clients to have full network access with certificate passthrough to all STAGE endpoints. You can frequently resolve these issues by [allowing the URLs](/user-guide/hostname-allowlist) in the Snowflake allowlist in your proxy or firewall.

## DNS configuration issues

In Private Connectivity scenarios, DNS-related settings can be misconfigured on the host or the remote DNS server. These issues are usually accompanied by error messages like “Name or service not known” or “nodename nor servname provided, or not known” (such as [JDCB Error 2](/user-guide/client-connectivity-troubleshooting/error-messages#label-jdbc-connectivity-error-2)). If you configure [AWS PrivateLink](/user-guide/admin-security-privatelink), [Azure Private Link](/user-guide/privatelink-azure), or [Google Cloud Private Service Connect](/user-guide/private-service-connect-google), your network administrator must [create and manage a DNS record for your connection URL](/user-guide/client-redirect#label-client-redirect-configuring-the-dns-cname-record). Ensure that you performed all the configuration steps associated with your provider correctly.

## Transient network issues

Sometimes your issue might be transient, which can result from the temporary unavailability of the OCSP servers, remote DNS servers, Snowflake servers, or the client temporarily being unable to reach them.

## Further troubleshooting

If your issue is not transient, or the steps above do not resolve your issue, please follow the steps in [Troubleshooting steps](/user-guide/client-connectivity-troubleshooting/troubleshooting-steps).
