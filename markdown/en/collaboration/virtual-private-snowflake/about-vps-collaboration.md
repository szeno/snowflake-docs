# About collaboration in VPS environments

Virtual Private Snowflake (VPS) offers the highest level of security by completely isolating your data and
resources. VPS was specifically created for organizations requiring the highest levels of security,
such as financial institutions and enterprises handling sensitive data. With such focus on security
and isolation, VPS deployments handle information collaboration differently from other Snowflake deployments.
Despite the restraints required by this isolation, VPS customers can still share data with other Snowflake users,
allowing both cooperation and data security.

## How collaboration works with VPS

Collaborative data, offered by a *data provider* and accessed by a *data consumer*, can be made
available for collaboration even if one or both parties use VPS. Snowflake Support is always
involved in this process to ensure that all security protocols are strictly followed.
The VPS environment provides strong and flexible options for securely sharing data,
maintaining the highest levels of security and compliance across all data-sharing activities.

## About VPS private listings

Private listings are shared from one provider to one consumer only. Either the provider or the
consumer, or both, use VPS. Discovery of listings can be restricted to specific users or organizations chosen by
the data provider. The VPS consumer also restricts which providers (and listings) are visible to them.
After all the processes described in this guide
are complete and reviewed by Snowflake Support, the end result is that the VPS user can
query the data through a private listing.

If you’re a data consumer in search of listings, see [Finding consumers for private listings](/collaboration/virtual-private-snowflake/vps-collaboration-for-providers#label-locating-vps-priv-listings-for-consumers).

If you’re a data provider, find more information on locating consumers who might be interested in
your listing in [Finding consumers for private listings](/collaboration/virtual-private-snowflake/vps-collaboration-for-providers#label-finding-consumers-vps-private-listings-for-providers).

## Data Collaboration: Access without Duplication

Snowflake uses a process called cross-cloud auto-fulfillment to make the data locally available
without requiring any inbound data transfer into the consumer’s Snowflake account.
Powered by Snowgrid™, Snowflake’s cross-cloud technology, auto-fulfillment connects data across
different regions and cloud providers. Snowgrid creates the seamless global network that keeps data
securely within the provider’s environment while allowing authorized users to access it from anywhere,
without duplication or movement.

For private listings, Snowgrid isolates the data, making it available exclusively to specific
consumers through a dedicated connection. This process ensures that the data remains secure and
isolated while still providing immediate, controlled access.

These private listings only become available after the provider and consumer have officially
arranged to share the data, a process described in this guide. The provider’s catalog of VPS-eligible
listings then becomes discoverable to the VPS consumer. However, these listings are not
accessible unless there is at least one active consumer.

Just as VPS environments are isolated and have globally unique identifiers, each private listing is
also isolated and has a globally unique identifier (called a *Universal Listing Locator* or *ULL*). The
ULL is often casually referred to as a *listing name*, but for private listings the listing name
is unique to the collaboration between one provider and one consumer.

### Provision of data products

VPS users can publish data to a listing if and only if this action is
explicitly allowed and correctly configured.

Note

**Snowflake Support is always involved in this process to
ensure that all security protocols are strictly followed.**

Private listings are visible within a dedicated, secure user interface, accessible exclusively
by other participating users. If those users are also in a VPS environment, they must also have
authorized this interaction.

These measures ensure that data remains isolated and secure within VPS environments and that
no data leaves or enters the VPS without strict procedures to ensure compliance and security.

Note

Currently in preview, VPS providers can publish free and limited trial listings on the Snowflake Marketplace. For more information, see [As a VPS provider, create a listing in Snowflake Marketplace](/collaboration/provider-listings-creating-publishing#label-listings-vps-provider-create-in-marketplace)

### Consumption of data products

VPS users can see and consume listings that are shared by a controlled list
of vetted data providers. The providers and their data products must be specifically
enabled for the consumers VPS, regardless of whether the provider is in a VPS or not.
To find privately shared data products, VPS users use a separate, isolated user interface
called *Private Sharing*.

This separate interface is designed to uphold the strict isolation requirements of VPS environments,
ensuring that all data interactions comply with VPS compliance and security standards. View and install
listings that are shared with you by visiting <https://app.snowflake.com/pm/pm_aws_us_west_2/#/data/shared>.
Or, if you are already signed in, in the navigation menu, select **Data sharing** » **Internal sharing**.

VPS environments have tightly controlled interactions with any external connection,
utilizing a dedicated isolated user interface (UI) that ensures the strict security and isolation
of the VPS environment. While VPS users can publish and consume data in “listings”, these actions
require specific configurations; and only listings that are explicitly enabled (allowed) for
VPS access are publishable or accessible from within this secure environment.

## Limitations

# Limitations on collaborating with Virtual Private Snowflake (VPS)

The following limitations apply to collaboration support for Virtual Private Snowflake (VPS):

- Listings that use manual fulfillment are not supported.
- Listings that use Snowflake connectors are not supported.
