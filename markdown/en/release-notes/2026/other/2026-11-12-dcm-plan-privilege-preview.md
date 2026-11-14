# Nov 12, 2026: DCM Projects PLAN privilege (*Preview*)

With this Public Preview release, you can grant the PLAN privilege on a DCM project to let a role run `EXECUTE DCM PROJECT ... PLAN` and `EXECUTE DCM PROJECT ... PLAN DELTA` without holding OWNERSHIP of the project. The DCM project privileges form a hierarchy in the order READ, MONITOR, PLAN, OWNERSHIP, where each privilege includes all operations of the privileges before it.

PLAN runs with the privileges of the DCM project owner role. A role with PLAN can therefore retrieve the metadata (DDL) of objects that the owner role can read, even if the role can’t access those objects with its own privileges.

For more information, see [PLAN privilege](/user-guide/dcm-projects/dcm-projects-use#label-dcm-projects-plan-privilege).
