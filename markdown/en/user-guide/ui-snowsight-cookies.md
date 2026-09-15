# Cookies in the Snowflake web interface

Snowflake uses cookies and similar technologies to recognize you when you visit Snowflake web applications and product websites.
This documentation explains what these technologies are, why Snowflake uses them, and your rights to control Snowflake’s
use of these technologies.

Cookies set by the website owner (in this case, Snowflake) are called *first-party cookies*. Cookies set by parties other than the
website owner are called *third-party cookies*. Third-party cookies enable third party features or functionality to be provided on or
through the website, such as interactive video content for listings on the Snowflake Marketplace.

Snowflake uses different types of first-party and third-party cookies for different reasons. Cookies are categorized as necessary, performance, functional, or targeting:

Necessary Cookies:
:   Strictly necessary to provide you with the services available through Snowflake sites and to use some of its features.

Performance Cookies:
:   Allow Snowflake to count visits and traffic sources to measure and improve the performance of Snowsight. All information
    collected by these cookies is aggregated.

Functional Cookies:
:   Enable Snowsight to provide enhanced functionality and personalization. These cookies might be set by Snowflake, or by
    third-party providers whose services Snowflake has added to Snowsight pages. If you do not allow these cookies, some or all of
    these services may not function properly.

Targeting Cookies:
:   Used to track online activity for a more personalized experience, such as by offering relevant content or advertisements.

## Cookies used by Snowflake

This table details the specific cookies used by Snowflake. Cookies labeled **Necessary** are required for technical reasons, while
other cookies are used to track users and enhance the product experience. Third parties serve cookies through the web interface for
analytics, improving user experience, and other purposes.

| Cookie Name | Domain | Type | Purpose |
| --- | --- | --- | --- |
| `user-<encoded_string>` | `apps-api.<string>.<string>.<string>.snowflake.com` | Necessary | Used for user authentication in Snowsight. |
| `csrf-<token>` | `apps-api.<string>.<string>.<string>.snowflake.com` | Necessary | Used to carry the cross-site request forgery (CSRF) security token between the server and the client in Snowsight. |
| `oauth-nonce-<8-bit-value>` | `app.snowflake.com` | Necessary | Used to prevent OAuth CSRF attacks. |
| `snowflakeContext` | `app.snowflake.com` | Necessary | Used to determine the active customer account. |
| `__dd_s` | `app.snowflake.com` | Necessary | Used for support and SLA management. |
| `S8_SESSION_<username>__<accountUrl>` | `apps-api.<string>.<string>.<string>.snowflake.com` | Necessary | Used for user authentication. |
| `snowflake_deployment` | `app.snowflake.com` | Necessary | Used for randomized deployment of asset retrieval to support content delivery network (CDN) functionality. |
| `__stripe_mid` | `app.snowflake.com` | Necessary | Used for Stripe fraud prevention if using payment processing functionality. |
| `docai_version` | `app.snowflake.com` | Necessary | Used for blue/green deployment of updates to applications. |
| `PREF*`, `VSC*`, `VISITOR_INFO1_LIVE*`, `NID`, `remote_sid*` | `app.snowflake.com` | Necessary | Used for YouTube’s privacy-enhanced mode if you select or play a YouTube video, such as on the Snowflake Marketplace. This mode does not store personally-identifiable cookie information for playbacks of embedded videos. |

Expand

Show lessSee more

## Manage cookies used by Snowflake

You can control and manage cookies by setting or amending your web browser controls to accept or refuse all cookies. Follow the guidance
provided by your web browser for more details.

Snowflake interprets the use of a **Do Not Track** signal as an objection to the placement of **Targeting** cookies.

Note

Due to a lack of standardization in **Do Not Track** settings, this setting might not work with Snowflake.

Snowflake does not currently provide functionality for end-user cookie consent management, but Snowflake is compatible with many existing
third-party solutions that provide this functionality. You can work with your internal IT teams or consult with your Snowflake implementation
partners to identify the right cookie solution for your organization’s needs.

If you choose to reject cookies, you can still use Snowsight. Your access to some functionality and
areas of the web interface might be restricted.

## More information about Snowflake, cookies, and tracking technology

If you have questions about Snowflake’s use of cookies or other technologies, email `privacy@snowflake.com`
