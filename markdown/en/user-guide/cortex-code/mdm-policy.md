# Enforce CoCo policy with MDM

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Administrators can deliver CoCo policy through a Mobile Device Management (MDM) system, such as Jamf or Microsoft Intune, so that standard users can’t change or remove it. This applies to the CoCo clients, [CoCo CLI](/user-guide/cortex-code/cortex-code-cli) and [CoCo Desktop](/user-guide/cortex-code/cortex-code-desktop).

The controls on this page add to the existing permission, sandbox, and UI settings described in [Managed settings (organization policy)](/user-guide/cortex-code/managed-settings). You can deliver them in the same `managed-settings.json` file and system paths, or through an MDM profile.

## Controls

The following table lists each control and its key in `managed-settings.json` and in an MDM profile:

| Control | Managed setting | MDM key | Description |
| --- | --- | --- | --- |
| Account lock | `tenant.allowedAccounts` | `CortexAllowedAccounts` | Restricts which Snowflake accounts CoCo can connect to. Accepts glob patterns. |
| Allowed authentication methods | `auth.allowedMethods` | `CortexAllowedAuthMethods` | Restricts sign-in to the listed methods, for example `OAUTH_AUTHORIZATION_CODE`, `EXTERNALBROWSER`, `PROGRAMMATIC_ACCESS_TOKEN`, or `SNOWFLAKE`. |
| Per-account authentication methods | `auth.accounts` | `CortexAllowedAuthMethodsByAccount` | Enforces allowed authentication methods for specific Snowflake accounts. |
| Minimum client version | `required.minimumVersion` | `CortexMinimumVersion` | Blocks CoCo from starting if the installed version is older than the value. |
| Per-client minimum version | `cli.required.minimumVersion`, `desktop.required.minimumVersion` | `CortexCliMinimumVersion`, `CortexDesktopMinimumVersion` | Sets a different minimum version for CoCo CLI and CoCo Desktop. Overrides the shared `required.minimumVersion` or `CortexMinimumVersion` for that client only. If a client has no client-specific value, the shared value applies. |
| On/off switch | `enabled` | `CortexEnabled` | Turns the controls on or off. |

Expand

Show lessSee more

The controls behave the same on CLI and Desktop. Use `tenant.allowedAccounts` to restrict accounts. The older `account()` pattern in `permissions.onlyAllow` is enforced only on the CLI.

Note

The account lock checks the host that CoCo connects to, not only the [account name](/user-guide/admin-account-identifier). A connection that names an allowed account but points to another account’s host is refused. Region and [PrivateLink](/user-guide/admin-security-privatelink) hosts for an allowed account are permitted.

## Requirements

- macOS: CoCo CLI 1.1.89 or later, CoCo Desktop 1.21.4 or later.
- Windows: CoCo Desktop 1.21.6 or later. CoCo CLI 1.1.104 or later; CoCo CLI 1.2.0 or later to embed `managed-settings.json` (see [Option 2](#label-cortex-code-mdm-embed)).

## Deploy on macOS

Deliver a configuration profile with a Managed Client (forced preferences) payload for the preference domain `com.snowflake.coco`. Use the MDM keys from [Controls](#label-cortex-code-mdm-controls). The following profile sets the same policy as the `managed-settings.json` example later on this page:

Copy code

```
<key>CortexEnabled</key>
<true/>
<key>CortexAllowedAccounts</key>
<array>
  <string>acme-prod</string>
  <string>acme-analytics</string>
</array>
<key>CortexAllowedAuthMethods</key>
<array>
  <string>OAUTH_AUTHORIZATION_CODE</string>
  <string>EXTERNALBROWSER</string>
</array>
<key>CortexAllowedAuthMethodsByAccount</key>
<string>{"acme-prod": ["EXTERNALBROWSER"]}</string>
<key>CortexMinimumVersion</key>
<string>1.1.89</string>
```

macOS delivers these keys as forced preferences. The Managed Client payload writes them to the `/Library/Managed Preferences/` directory, which [System Integrity Protection](https://support.apple.com/en-us/102149) protects, and marks them forced (`CFPreferencesAppValueIsForced`). Forced values take precedence over any value in the user’s or computer’s own preferences, so deleting or editing CoCo’s local preferences has no effect.

On a supervised device enrolled through [Automated Device Enrollment](https://support.apple.com/guide/deployment/automated-device-enrollment-management-dep73069dd57/web) with MDM profile removal disallowed, the profile can’t be removed and macOS continuously reasserts the forced values. Even a user with root or sudo access can’t override the policy. Removing the profile requires booting to Recovery and disabling System Integrity Protection, after which the device re-enrolls if it is still assigned in Apple Business Manager.

## Deploy on Windows

Deliver machine policy under `HKLM\Software\Policies\Microsoft\CortexCode` through Group Policy or Intune, using the ADMX template. CoCo reads only the machine hive, so standard users can’t add or weaken policy.

CoCo reads the following registry values:

| Value | Type |
| --- | --- |
| `CortexEnabled` | REG\_DWORD (1 on, 0 off) |
| `CortexAllowedAccounts` | REG\_SZ (JSON array) |
| `CortexAllowedAuthMethods` | REG\_SZ (JSON array) |
| `CortexAllowedAuthMethodsByAccount` | REG\_SZ (JSON object) |
| `CortexMinimumVersion` | REG\_SZ |
| `CortexCliMinimumVersion` | REG\_SZ |
| `CortexDesktopMinimumVersion` | REG\_SZ |
| `CortexManagedSettingsBase64` | REG\_SZ (base64) |
| `CortexManagedSettingsBase64Enabled` | REG\_DWORD (1 on, 0 off) |

Expand

Show lessSee more

Example `.reg` file for testing:

```
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\Software\Policies\Microsoft\CortexCode]
"CortexEnabled"=dword:00000001
"CortexAllowedAccounts"="[\"acme-prod\",\"acme-analytics\"]"
"CortexAllowedAuthMethods"="[\"OAUTH_AUTHORIZATION_CODE\",\"EXTERNALBROWSER\"]"
"CortexAllowedAuthMethodsByAccount"="{\"acme-prod\":[\"EXTERNALBROWSER\"]}"
"CortexMinimumVersion"="1.1.104"
```

## Deploy with managed-settings.json

Place `managed-settings.json` in the system location for your platform:

- macOS: `/Library/Application Support/Cortex/managed-settings.json`
- Windows: `%ProgramData%\Cortex\managed-settings.json`

`managed-settings.json` must be writable only by administrators. On macOS it must be owned by root and must not be group-writable or world-writable. On Windows, CoCo checks the access control list on `managed-settings.json` and its folder. If these checks fail, CoCo ignores `managed-settings.json`.

The following `managed-settings.json` sets the same policy as the macOS profile example:

Copy code

```
{
  "version": "1.0",
  "enabled": true,
  "tenant": {
    "allowedAccounts": ["acme-prod", "acme-analytics"]
  },
  "auth": {
    "allowedMethods": ["OAUTH_AUTHORIZATION_CODE", "EXTERNALBROWSER"],
    "accounts": {
      "acme-prod": { "allowedMethods": ["EXTERNALBROWSER"] }
    }
  },
  "required": {
    "minimumVersion": "1.1.89"
  }
}
```

## Scope controls by account or client

### Per-account authentication

Use `auth.accounts` or `CortexAllowedAuthMethodsByAccount` to set different methods for different accounts. For example, require browser SSO for production and allow any method for development:

Copy code

```
"auth": {
  "allowedMethods": ["OAUTH_AUTHORIZATION_CODE", "EXTERNALBROWSER"],
  "accounts": {
    "acme-prod": { "allowedMethods": ["EXTERNALBROWSER"] },
    "acme-dev": { "allowedMethods": [] }
  }
}
```

Matching rules:

- A matching account entry replaces the global list for that account.
- An empty list means any method is allowed for that account.
- Accounts with no entry use the global list.
- Account names are matched case-insensitively and support globs. An exact match takes priority over a glob.
- Per-account scope applies to authentication methods only.

### Per-client minimum version

To set a different minimum version for each client, use `cli.required.minimumVersion` and `desktop.required.minimumVersion` in `managed-settings.json`, or `CortexCliMinimumVersion` and `CortexDesktopMinimumVersion` in MDM. A client-specific value overrides the shared value for that client only.

## How CoCo resolves policy

CoCo resolves each control separately, in this order:

1. MDM profile
2. `managed-settings.json`
3. Default

Within a source, a client-specific minimum version overrides the shared minimum version, and a matching per-account entry overrides the global authentication list. User settings in `settings.json` can’t set or weaken these controls.

If a managed policy is present but malformed, unreadable, or fails validation, CoCo denies connections until the policy is fixed.

## Turn off the controls

Set `enabled` to `false` in `managed-settings.json`, or set `CortexEnabled` to `false` in the macOS profile or to `0` in the Windows registry. Use the same channel that you used to deploy the controls.

## Verify the policy

Run `cortex managed-settings` to print the active policy, its source, and any validation errors.

## How MDM and managed-settings.json interact

You can deploy an MDM profile, a `managed-settings.json` file, or both. When both set the same control, the MDM value wins. The following table compares the two methods:

| Method | Who can change it | Platforms |
| --- | --- | --- |
| MDM profile | Your MDM administrator. Standard (non-administrator) users can’t change or remove it. On a supervised Mac, even a local administrator or root user can’t. On other devices, a local administrator can edit it. See [Keep policy applied](#label-cortex-code-mdm-keep-policy-applied). | macOS, Windows |
| `managed-settings.json` | Any user with administrator or root access on the device. | macOS, Windows |

Expand

Show lessSee more

### Keep policy applied

On a supervised Mac, an MDM profile can be changed only through your MDM, and even root can’t remove it (see [Deploy on macOS](#label-cortex-code-mdm-deploy-macos)). On Windows and on Macs that aren’t supervised, a user with local administrator or root access can edit or remove an MDM profile or a `managed-settings.json` file.

Where users can edit or remove the policy, configure it to be restored automatically:

- On Windows, Intune reapplies the policy with [Config Refresh](https://learn.microsoft.com/en-us/intune/intune-service/remote-actions/pause-config-refresh), or with a remediation script that rewrites a changed value or a deleted `managed-settings.json` file.
- On a Mac that isn’t supervised, the MDM reinstalls a removed [configuration profile](https://support.apple.com/guide/deployment/intro-to-device-management-profiles-depc0aadd3fe/web) at its next check-in.

Automatic reapplication corrects tampering on a schedule. It doesn’t prevent the edit, and there is a short window before the next refresh, so pair it with endpoint detection and response (EDR) monitoring to alert on changes.

### Option 1: Deploy both

Deliver the controls in the MDM profile and deploy `managed-settings.json` for everything else, such as permissions, [sandbox](/user-guide/cortex-code/sandbox), and MCP rules. The controls in the profile are tamper-resistant. Settings that exist only in `managed-settings.json` are not, because any user with root or administrator access can edit it.

### Option 2: Embed managed-settings.json in the MDM profile

You can embed the entire `managed-settings.json` in the MDM profile (macOS) or registry policy (Windows) so that every setting is tamper-resistant. On Windows, the embedded value has the same tamper resistance as other registry policy; see [Keep policy applied](#label-cortex-code-mdm-keep-policy-applied).

1. Encode `managed-settings.json`: `cortex managed-settings encode /path/to/managed-settings.json`
2. Set the output as the value of `CortexManagedSettingsBase64`. On Windows, set it as a REG\_SZ value under `HKLM\Software\Policies\Microsoft\CortexCode`.
3. Optional: Set `CortexManagedSettingsBase64Enabled` to `false` (`0` on Windows) to turn off the embedded policy without removing it.

The following example shows the macOS profile key. Deliver the value as `<string>`, not `<data>`:

Copy code

```
<key>CortexManagedSettingsBase64</key>
<string>OUTPUT_OF_ENCODE_COMMAND</string>
```

The following example shows the Windows registry value:

```
[HKEY_LOCAL_MACHINE\Software\Policies\Microsoft\CortexCode]
"CortexManagedSettingsBase64"="OUTPUT_OF_ENCODE_COMMAND"
```

A value that is invalid or larger than 256 KB causes CoCo to deny connections.

Note

CoCo CLI on Windows reads the embedded value from version 1.2.0. Until a 1.2.x release reaches the stable channel, it is available only to users who install from the beta channel (`$env:CORTEX_CHANNEL="beta"` before running `install.ps1`). On earlier CLI versions, use Option 1 (deploy `managed-settings.json` alongside the registry policy).

## Limitations

- Changes take effect the next time CoCo starts. Restart the CLI or fully quit and reopen Desktop.
- On non-English editions of Windows, the permission check can skip `managed-settings.json`. Use Group Policy or Intune on those devices. A `managed-settings.json` embedded in registry policy (Option 2) isn’t affected.
