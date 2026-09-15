# Common Vulnerabilities and Exposures (CVE) considerations

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how Snowflake applies Common Vulnerabilities and Exposures (CVE) criteria to
a Snowflake Native App.

## About the CVE for a Snowflake Native App

Common Vulnerabilities and Exposures (CVEs) are publicly disclosed information about security
vulnerabilities in software applications and systems. These vulnerabilities can potentially be
exploited, compromising the security of affected applications.

In the context of a Snowflake Native App, providers must address CVEs to ensure the secure execution of
these applications within Snowflake’s data cloud environment. This is necessary to protect the data
and operations of Snowflake customers. During the security review of a Snowflake Native App, Snowflake scans
all incoming apps for known CVEs.

Warning

It is possible that not all CVEs are detected. Also, CVEs may not present the same level of risk
or may not be actionable by Snowflake.

The purpose of Snowflake’s CVE Evaluation Criteria is to establish a set of clear and objective criteria
for evaluating and addressing known CVEs in an app submitted to Snowflake. By defining these criteria, Snowflake
prioritizes and mitigates critical security risks, while accounting for the effort required to address less
severe vulnerabilities. This policy guides the process for accepting or rejecting an app based on the CVE risk
profile.

This CVE policy applies to all incoming apps that undergo Snowflake’s security review process. It covers how
CVEs that are identified in the packages and dependencies of an app are evaluated and addressed. This policy
is enforced during the security review process, as documented in [Run the automated security scan](/developer-guide/native-apps/security-run-scan).

This process ensures that only apps that meet the defined criteria are approved for publishing and distribution to
consumers within Snowflake’s data cloud environment.

## CVE Evaluation Criteria

Snowflake uses the following three criteria to evaluate known vulnerabilities (CVEs) in
a Snowflake Native App and review each CVE:

- [The CVE has a confirmed fix](#label-native-apps-security-cve-confirmed)
- [The CVE has a high integrity impact](#label-native-apps-security-cve-impact)
- [The CVE has an EPSS score of 10 percent or higher](#label-native-apps-security-cve-epss)

By considering these three criteria, Snowflake decides which CVEs pose the most significant risks and
require immediate fixes within an app. An app is rejected if it contains any packages with a CVE that meets the criteria below or is not
appropriately remediated.

### The CVE has a confirmed fix

Snowflake provides actionable information and reports only on CVEs that have a confirmed fix according
to the National Vulnerability Database (NVD). This ensures that the identified vulnerabilities have a
known and available solution, enabling developers to address them effectively.

### The CVE has a high integrity impact

Snowflake focuses on CVEs with a high integrity impact, as defined by the Common Vulnerability Scoring
System (CVSS). A high integrity impact indicates a total loss of integrity or complete loss of protection,
allowing unauthorized modifications of data and/or data tampering without any constraints. Providers must
address these CVEs to ensure the security and reliability of our data cloud environment.

### The CVE has an EPSS score of 10 percent or higher

The Exploit Prediction Scoring System (EPSS) provides an estimate of how likely a software
vulnerability will be exploited based on factors including the age, complexity, and potential
impact of the vulnerability.

Snowflake rejects an app if it has an EPSS score of ten percent or higher. This threshold is determined
based on the analysis of data from current apps. This threshold allows Snowflake to prioritize and address
vulnerabilities that have a higher probability of being exploited, while maintaining a reasonable level of
risk tolerance.

## Additional information

The following links provide more information about the processes and policies Snowflake uses
when evaluating the CVE vulnerabilities for an app:

- [NVD Vulnerabilities](https://nvd.nist.gov/vuln)
- [Vulnerability metrics](https://nvd.nist.gov/vuln-metrics/cvss)
- [Exploited Protection Scoring System](https://nvd.nist.gov/vuln-metrics/cvss)
- [Enhancing Vulnerability Prioritization](https://arxiv.org/abs/2302.14172)
