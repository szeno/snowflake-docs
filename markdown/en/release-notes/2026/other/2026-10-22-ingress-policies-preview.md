# Oct 22, 2026: Ingress policies (*Preview*)

We are introducing ingress policies in preview. An ingress policy admits or blocks a request by combining several conditions in one policy. This preview includes the following capabilities:

- **Combined admission rules.** Evaluate network origin, authentication method, client, geolocation, PrivateLink ID, and endpoint path in one policy. Combine the conditions with `AND`, `OR`, and `NOT`, then allow or block the request. For example, allow drivers from the corporate network and block a specific application, or allow single sign-on only from approved countries.
- **Difference from network and authentication policies.** A network policy controls network locations and private connectivity. An authentication policy controls authentication methods, clients, security integrations, and multi-factor authentication. An ingress policy makes one allow-or-block decision from several of these signals together, including geolocation and endpoint path. Snowflake evaluates each policy on its own. A request is admitted only when every applicable policy allows it.
- **Login and subsequent requests.** Snowflake evaluates the policy when a user logs in and again on every subsequent authenticated request through drivers and APIs, so a policy change can affect existing sessions.
- **Account and user scope.** Attach a policy to the account as a baseline, or to an individual user. A user-level policy overrides the account-level policy for that user.

For more information, see [Ingress policies](/user-guide/ingress-policies).
