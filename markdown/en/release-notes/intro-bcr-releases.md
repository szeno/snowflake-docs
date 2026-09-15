# About Behavior Changes

Each month (except for November and December), Snowflake selects one of the weekly full releases for the month to introduce behavior changes.
The weekly release selected for the behavior changes varies, but is typically the 4th or 5th release after the previous behavior change release.

A behavior change is defined as any change to existing behavior that returns different results from before and may impact customer code or
workloads.

## Behavior Change Bundles

Behavior changes are provided in bundles that utilize the following naming convention:

`YYYY_NN`

Where `YYYY` is the year and `NN` is the ordinal number of the release within the year. For example, `2022_06` would be the 6th behavior
change bundle introduced in 2022.

For more details about working with behavior change bundles, see [Behavior change management](/release-notes/bcr-bundles/managing-behavior-change-releases).

## Bundle Lifecycle

The behavior change bundle lifecycle consists of the following two periods:

Testing period (1st month):
:   The bundle is introduced **Disabled by Default**. During this period, you can choose to *enable* the bundle in
    one or more accounts. Typically, you would choose accounts designated for development or QA (quality assurance) so that you can test the
    changes without impacting your production accounts.

Opt-out period (2nd month):
:   The bundle moves from **Disabled by Default** to **Enabled by Default**. During this period, you can choose to
    *disable* the bundle in your accounts. This allows you to postpone the changes in the bundle, typically for production accounts, while
    making any necessary adjustments to mitigate the impact of the changes.

You may choose to explicitly enable or disable the behavior change bundle anytime during these two periods. Once explicitly set, the bundle is
changed from its default state and Snowflake does not override the setting for the above periods.
For example, if you disable a bundle during the testing period, we do not enable it at the beginning of the opt-out period.

At the end of the opt-out period, Snowflake enables the behavior changes in the bundle across all accounts, at which time the bundle is considered
**Generally Enabled**. From this time onwards, any overrides are cleared and you are unable to explicitly enable or disable the bundle.

## Behavior Change Documentation

A release that contains behavior change bundles includes the following documentation (in addition to the *Release Notes* for the
release):

- Summary of each bundle in the release.
- Detailed descriptions of the behavior changes in each bundle.
