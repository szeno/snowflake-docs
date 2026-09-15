# Uninstalling the Snowflake Data Clean Rooms environment

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

To completely uninstall the clean room environment from your account, you must use the ACCOUNTADMIN role in the Snowflake account where the
clean room application is installed. This deletes the clean room environment for all users in your account.

Important

This procedure completely uninstalls the entire environment for your account, not just individual clean rooms.

Before uninstalling, you must remove all clean rooms and collaborations from your account. The steps depend on which types of clean rooms
you have.

To uninstall the clean room environment for your account:

1. Remove all existing clean rooms and collaborations. Complete the steps that apply to your environment:

   **If you have Collaboration Data Clean Rooms:**

   1. [Tear down all collaborations that you created as an owner.](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-teardown-reference)
   2. [Leave all collaborations that you joined as a collaborator.](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-leave-reference)

   **If you have legacy Provider and Consumer clean rooms:**

   1. [Delete all the clean rooms that you created as a provider.](/user-guide/cleanrooms/manage-clean-rooms#label-dcr-single-cleanroom-delete)
   2. [Uninstall all the clean rooms that you installed (joined) as a consumer.](/user-guide/cleanrooms/manage-clean-rooms#label-dcr-single-cleanroom-unjoin)

   If you have both types, complete all four steps above.
2. [Download the cleanroom uninstall notebook file](/static/samples/clean-rooms/UNINSTALL_COLLAB_DCR.ipynb) and
   [import it into Snowsight](/user-guide/ui-snowsight/notebooks-create) in the account where you want to delete the clean rooms
   environment. You must be able to run the notebook by using the ACCOUNTADMIN role.
3. If you want to delete your organization from Snowflake Data Clean Rooms, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).
