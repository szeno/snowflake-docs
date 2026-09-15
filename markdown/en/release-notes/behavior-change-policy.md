# Behavior change policy

The behavior change release process at Snowflake lets Snowflake users control a bundle of product or feature
changes that may affect existing functionality for at least eight weeks before the changes are generally enabled across
all Snowflake accounts. During this period of time, account administrators can selectively disable or enable
each bundle of behavior changes. New behavior change bundles are introduced on a monthly basis.

## Introduction

To provide the best experience and value to our customers, Snowflake is continually improving and enhancing our service offerings.
As part of these ongoing efforts, Snowflake must sometimes make changes to products or features that may affect existing functionality.
To minimize the impact of these behavior changes on production accounts, and to ensure consistent, timely customer communication,
behavior changes are typically released on a monthly basis as bundles introduced in designated regularly-scheduled weekly releases.
As a general rule, one month elapses between the start of each of these releases. Once a new bundle is released, account administrators
can enable or disable the bundle for their accounts for eight weeks before the behavior changes in the bundle become generally enabled
for all accounts.

## Monthly behavior change bundles

**Snowflake releases behavior changes in monthly behavior change bundles, with each behavior change bundle typically containing multiple behavior changes.**

Details about each behavior change are published to the [Snowflake Documentation site](/release-notes/behavior-changes) and email notifications of
behavior change releases are sent to the [Product Notification contact](/user-guide/ui-snowsight-contacts#label-snowsight-admin-contacts) and a mailing list of users
who are authorized to submit support cases.
If Snowflake identifies specific customers who are likely to be directly affected by the behavior changes,
Snowflake Customer Support may also send email notifications to the designated support contacts for those customers.
Behavior change bundles are named by the year and the ordinal number of the bundle within the year. For example, bundle 2023\_03 would be
the third behavior change bundle released in the year 2023.

For information about current and past behavior change releases, refer to the [Behavior change announcements](/release-notes/behavior-changes).

## Testing period

**For at least four weeks following release, account administrators can opt in to a behavior change bundle..**

The first four-week period after a behavior change bundle is released is called the **Testing Period**.
During this time, the behavior changes in the bundle are disabled by default.
Account administrators can [enable the entire behavior change bundle](/release-notes/bcr-bundles/managing-behavior-change-releases),
but cannot enable or disable individual changes in the bundle.
To test the changes during this period, Snowflake recommends enabling the bundle in one or more accounts dedicated to development or
quality assurance purposes.
If more time is required to test the changes in the bundle and to mitigate
their impact on a production account, the account administrator can proactively disable the entire bundle in the account prior to the
beginning of the Opt-out Period.

## Opt-out period

**For at least four weeks following the end of the Testing Period, account administrators can opt out of a behavior change bundle.**

The next four-week period is the Opt-out Period. At the beginning of the **Opt-out Period**, the behavior change bundle status changes
from disabled by default to enabled by default. If the behavior change bundle status was explicitly modified at any point during the previous Testing Period,
it will remain in its specified state.
As with the Testing Period, individual changes cannot be disabled, but account administrators can disable the entire behavior change bundle at any time.

## Generally enabled

**After these 8 weeks, the behavior changes in the bundle are generally enabled.**

After the Testing and Opt-Out periods, the bundle is generally enabled and the behavior change release process is complete. The behavior change bundle is fully released, meaning all the changes in the bundle are now in effect in production for all accounts across all deployments.

At this point, you can no longer disable the behavior changes from your accounts.

## Enabling and disabling behavior change bundles

As described above, account administrators can enable or disable behavior change bundles any time during the Testing or Opt-Out periods.
To learn how to check the status of a behavior change bundle for an account, enable a bundle, or disable a bundle, refer to
[Behavior Change Management](/release-notes/bcr-bundles/managing-behavior-change-releases).
When an account administrator (or a Snowflake representative) explicitly enables or disables a behavior change bundle for an account,
Snowflake will not override or reverse that setting. However, at the end of the Opt-out Period, behavior change bundles become
generally enabled and are in production for all accounts.

## Multiple behavior change release processes overlap

New behavior change bundles are typically released on a monthly basis, and take at least eight weeks to complete.
Therefore, only two behavior change bundles may be available for your Snowflake account at any given time,
with each behavior change bundle in different periods of the release process.
Specifically, the Opt-out Period of a bundle will overlap with the Testing Period of the next bundle.
In some instances, Snowflake may postpone or cancel the release of a new behavior change bundle in a given month,
resulting in the two available behavior change bundles to exist for longer than the normal 8 week period.

![Behavior Change Releases Overlap](/static/images/behavior-change-bundles-overlap.png)

## Impact score

BCRs are ranked from highest to lowest potential technical impact. While we recommend testing higher-ranked BCRs first, the actual impact depends on how you use our services.

> For example:

- A high-ranked BCR might not affect you if you don’t use that feature.
- A lower-ranked BCR might be more disruptive based on your specific usage.

Use this ranking as a general guide, but prioritize testing based on both the BCR’s rank and its relevance to your account.

Impact Score [LOW]:
:   This signifies minimal change to existing structures or processes.
    An example would be adding a new column to a current view or table, which would not disrupt existing queries or functionality.

Impact Score [MEDIUM]:
:   Indicates minor changes, primarily aimed at increasing awareness or requiring slight adjustments from users.

Impact Score [HIGH]:
:   Represents major changes that necessitate substantial adjustments from users.
    These changes often have a high impact due to significant alterations to use cases and workloads.
