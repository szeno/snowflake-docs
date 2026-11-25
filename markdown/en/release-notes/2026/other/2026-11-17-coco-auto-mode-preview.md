# Nov 17, 2026: Auto mode in Snowflake CoCo (*Preview*)

Auto mode is now available in preview for CoCo CLI, CoCo Desktop, and CoCo in Snowsight. Auto mode is an approval mode between default approvals and bypass mode. CoCo runs routine actions, such as
reading files, editing files in your workspace, and running read-only SQL, without a prompt. An LLM classifier checks
each remaining action against your requests, and CoCo asks you only when an action looks risky or doesn’t match your
intent.

For more information, see the following topics:

- [Auto mode in Cortex Code CLI](/user-guide/cortex-code/security#label-cortex-code-cli-auto-mode)
- [Auto mode in Cortex Code Desktop](/user-guide/cortex-code/cortex-code-desktop/permission-modes#label-cortex-code-desktop-auto-mode)
- [Auto mode in Cortex Code Snowsight](/user-guide/cortex-code/cortex-code-snowsight/coco-mode#label-coco-mode-auto-mode)
