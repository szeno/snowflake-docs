# Feb 25, 2026: Joining logical tables that contain ranges of values in a semantic view (*Preview*)

You can use a *range join* when you want to join a table with another table that defines a range of possible values in the
first table. For example, suppose that one table represents sales orders and has a column with the timestamp when the order
was placed. Suppose that another table represents fiscal quarters and contains the distinct ranges of time that represent
these quarters. You can create a semantic view that joins the two tables so that the row for an order includes the fiscal
quarter in which the order was placed.

Support for range joins is in [Preview](/release-notes/preview-features).

For information, see [Joining logical tables that contain ranges of values](/user-guide/views-semantic/sql#label-semantic-views-custom-range-joins).
