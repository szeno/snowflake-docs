# Mar 20, 2026: Block public access to internal stages with IP allowlist exceptions (*General availability*)

You can now block public access to Microsoft Azure internal stages while maintaining an allowlist of IP addresses or
CIDR blocks that are permitted to reach the internal stage. The new
SYSTEM$BLOCK\_INTERNAL\_STAGES\_PUBLIC\_ACCESS\_WITH\_EXCEPTION function extends the existing set of functions for blocking
public access to internal stages by letting you specify exceptions, rather than blocking all public IP addresses.

For more information, see [Blocking public access with IP allowlist exceptions](/user-guide/private-internal-stages-azure#label-private-internal-stage-block-public-with-exceptions) and
[SYSTEM$BLOCK\_INTERNAL\_STAGES\_PUBLIC\_ACCESS\_WITH\_EXCEPTION](/sql-reference/functions/system_block_internal_stages_public_access_with_exception).
