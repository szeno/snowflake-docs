# Git repository replication

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Database and share replication are available to all accounts.
- Replication of other account objects & failover/failback require Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic provides information about Snowflake support for replicating Git repository objects.

Before you get started, we recommend that you be familiar with Snowflake support for Git repositories.
For more information, see [Using a Git repository in Snowflake](/developer-guide/git/git-overview).

## Considerations for replicating Git repository clones

To replicate any Git repository objects that you’ve integrated with Snowflake,
you specify the database or schema that contains the Git repository object
in a replication group or a failover group. You don’t have to perform any
separate step to enable replication for Git repository clones.

The secrets from the primary system are replicated to the secondary system.

On the secondary system, you can read from the repository. However, you can’t commit, fetch from, or push to
the remote `origin` server from the secondary system. After you promote the secondary system to be the primary
by failing over, you can perform these other operations on the Git repository.

Snowflake supports replication for Git repository clones up to 5 GB in size. Larger repositories currently aren’t supported.
