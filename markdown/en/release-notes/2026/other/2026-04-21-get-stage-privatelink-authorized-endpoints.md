# Apr 21, 2026: View authorized private connectivity sources for internal stages (*General availability*)

You can now use the SYSTEM$GET\_STAGE\_PRIVATELINK\_AUTHORIZED\_ENDPOINTS
function to view the private connectivity sources that are authorized to
access the internal stage of your account. The function is supported on
Microsoft Azure and Google Cloud, and helps administrators verify which Microsoft Azure
private endpoints or Google Cloud VPC networks have been authorized through
previous calls to
[SYSTEM$AUTHORIZE\_STAGE\_PRIVATELINK\_ACCESS](/sql-reference/functions/system_authorize_stage_privatelink_access).

For more information, see
[SYSTEM$GET\_STAGE\_PRIVATELINK\_AUTHORIZED\_ENDPOINTS](/sql-reference/functions/system_get_stage_privatelink_authorized_endpoints).
