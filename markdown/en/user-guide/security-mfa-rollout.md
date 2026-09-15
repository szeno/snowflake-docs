# Planning for the deprecation of single-factor password sign-ins

To improve the security posture of all of its customers, Snowflake is rolling out changes to require multi-factor authentication (MFA) for
all human users using passwords, and disallow passwords for all service users. These service users must switch to a stronger authentication
method that doesn’t require interaction with a person. This topic describes how single-factor passwords will be deprecated so you can plan
accordingly.

Important

Snowflake provides a tool that guides you through the process of implementing strong authentication for all users, so you are ready for
the deprecation of single-factor passwords. For more information, see [Strong Authentication Hub](/user-guide/strong-authentication-hub).

The phases described in this topic don’t apply to reader accounts, trial accounts, or Snowflake Postgres. You can continue to sign in to
these types of accounts with a single-factor password.

## Human users vs. service users

User objects in Snowflake don’t always correspond to human users. There are users who sign in to Snowflake without human interaction — for
example, an application or service. These users are considered *service users*.

Administrators use the `TYPE` parameter of a user object to define whether a user is a human user or a service user.

- For human users, `TYPE=PERSON`. If you don’t set the `TYPE` parameter or set it to NULL, the user is treated as a human user.
- For service users, `TYPE=SERVICE`.

  Note

  The `LEGACY_SERVICE` user type helps customers transition service users to using a secure form of authentication. Setting
  a user’s type to `LEGACY_SERVICE` temporarily allows the user to authenticate with a password even though it’s an application or
  service. The rollout described in this topic involves the gradual deprecation of this user type.

The distinction between a human user and a service user is important because this rollout affects these two types of users differently.
To harden the security posture for both types of users, the enforcement of strong authentication consists of the following:

- All *human users* who use password authentication will be required to use a second factor of authentication.
- All *legacy service users* who currently use password authentication will be required to migrate to a more secure authentication method.

## Enforcement timeline

The following table provides the timeline for the enforcement of strong authentication methods.

| Estimated date | Affected users | Phase |
| --- | --- | --- |
| Sep. 2025 - Jan. 2026 | - Human users | [Mandatory MFA for all Snowsight users](#label-security-mfa-milestone-human-snowsight) |
| May 2026 - Jul. 2026 | - Human users - Legacy service users | [Strong authentication for NEW users](#label-security-mfa-milestone-new-users) |
| Aug. 2026 - Oct. 2026 | - Human users - Legacy service users | [Strong authentication for ALL users](#label-security-mfa-milestone-all-users) |

Expand

Show lessSee more

To learn how to implement strong authentication to meet these deadlines, see [Strong Authentication Hub](/user-guide/strong-authentication-hub).

### Phase 1: Mandatory MFA for all *Snowsight* users (new and existing)

Phase 1 is implemented using Snowflake’s established behavior change release process. In this process, Snowflake releases a
*behavior change bundle* each month. Because changes will be included in a behavior change bundle, enforcement of the new restrictions
coincide with the lifecycle of the bundle.

For more information about the lifecycle of behavior change bundles so you can plan for the enforcement of this phase, see
[Behavior change policy](/release-notes/behavior-change-policy).

**2025\_06 bundle (September 2025 - January 2026)** [[1]](#footnote-1)

| Objective | New behavior |
| --- | --- |
| Mandatory MFA for all Snowsight users | Human users must authenticate with a second factor when using a password to access Snowsight, with no exceptions.  Keep in mind the following:   - This phase affects Snowsight only. Human users can continue to use a single-factor password to access the Snowflake   service from business intelligence (BI) and similar tools, even after they use Snowsight to enroll in MFA. You can choose to   enforce MFA for these other tools; users who are already enrolled in MFA and use MFA outside Snowsight will continue to use   MFA. - Authentication policies that implemented optional MFA enrollment for Snowsight are overridden. - Because users authenticating with Snowflake OAuth use the Snowsight login interface, they must be enrolled in MFA. - Single sign-on users are not impacted by this change and can continue to access Snowsight with no changes. - Legacy service users (`TYPE=LEGACY_SERVICE`) are not impacted by this change and can continue to access   Snowsight with a single-factor password. |

Expand

Show lessSee more

For detailed information about how the changes in this bundle affect password and SSO authentication for your users, see [Upcoming Multi-Factor Authentication (MFA) enforcement for Snowsight logins with single-factor passwords](https://community.snowflake.com/s/article/Upcoming-MFA-enforcement-for-Snowsight-logins) (Knowledge Base article).

[1]
These dates are estimated, and are dependent on the release and lifecycle of the bundle. To understand this lifecycle, see [Monthly behavior change bundles](/release-notes/behavior-change-policy#label-behavior-change-bundles).

### Phase 2: Strong authentication for *new* users

Phase 2 will be enforced in accounts on a rolling basis during a three-month period. You’ll receive a notification with the enforcement
date for your account.

**May 2026 - July 2026** [[2]](#footnote-2)

| Objective | New behavior |
| --- | --- |
| Mandatory MFA for all new human users | All human users that are created *after* this phase is enforced must use a second factor when authenticating with a password, including those using BI tools or similar.  Human users who existed *before* the phase is enforced are not affected. These password users can continue to use BI tools or similar (anything but Snowsight) without a second factor of authentication until the next phase.  For example, suppose this phase is enforced on May 15, 2026. All human users created on or after this date must use a second factor of authentication regardless of the surface. Human users who existed before this date can continue to use password-only authentication for BI tools, but not Snowsight. |
| No new legacy service users | All non-human users created after the phase is enforced must be of type `SERVICE`, which prevents them from using a password. The `LEGACY_SERVICE` type is no longer available when creating a new user object. In addition, administrators cannot change the type of an existing user to `LEGACY_SERVICE`.  For example, suppose this phase is enforced on May 15, 2026. After this date, `TYPE=LEGACY_SERVICE` is an invalid option when executing a CREATE USER or ALTER USER command. |

Expand

Show lessSee more

[2]
These dates don’t correspond to a behavior change bundle, but are subject to change.

### Phase 3: Strong authentication for all users

Phase 3 will be enforced in accounts on a rolling basis during a three-month period. You’ll receive a notification with the enforcement
date for your account.

**August 2026 - October 2026** [[3]](#footnote-3)

| Objective | New behavior |
| --- | --- |
| Mandatory MFA for all human users | When this phase is enforced, all new and existing human users must use a second factor when authenticating with a password, with no exceptions. |
| No legacy service users | When this phase is enforced, all non-human users are blocked from using a password to authenticate.  The `LEGACY_SERVICE` user type is fully deprecated. All existing user objects with `TYPE=LEGACY_SERVICE` are migrated to `TYPE=SERVICE`, which prevents them from using a password. |

Expand

Show lessSee more

To learn how to implement strong authentication to meet the requirements of this phase, see [Strong Authentication Hub](/user-guide/strong-authentication-hub).

[3]
These dates don’t correspond to a behavior change bundle, but are subject to change.
