# Jan 23, 2026: Malicious IP Protection updates

These updates enhance Malicious IP Protection to provide visibility of blocked login attempts and the option to disable blocking for IP
addresses that are categorized as low-risk.

View blocked login attempts:
:   You can now use the new LOGIN\_DETAILS column in the Account Usage [LOGIN\_HISTORY view](/sql-reference/account-usage/login_history) to see details of
    network access attempts that the Malicious IP Protection service has blocked.

Manage opt-out for low-risk categories:
:   If you determine that blocking certain low-risk categories blocks legitimate users, you can opt out of blocking for specific
    categories by using the new [SYSTEM$OPT\_OUT\_MALICIOUS\_IP\_PROTECTION\_BY\_CATEGORY](/sql-reference/functions/system_opt_out_malicious_ip_protection_by_category) function.

For more information, see [Malicious IP Protection](/user-guide/malicious-ip-protection).
