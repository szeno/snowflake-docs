# August 08, 2024 — RANGE BETWEEN window frames with explicit offsets — *General Availability*

With this release, we are pleased to announce the general availability of RANGE BETWEEN window frames with explicit
offsets. A range-based window frame consists of a logically computed set of rows. By using a range-based frame with
explicit offsets, such as `RANGE BETWEEN 3 PRECEDING AND 3 FOLLOWING`, you can easily compute rolling
calculations, such as moving sums and averages, over time-series data. Because of the range-based frame, these
calculations are not disrupted by gaps in the data set.

For details about using this feature, see [Window function syntax and usage](/sql-reference/functions-window-syntax#label-window-syntax-and-usage).
