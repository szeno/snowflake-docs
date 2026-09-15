# Feb 24, 2026: User-defined actions for budgets

You can now configure budgets to automatically call stored procedures at key points during a budget cycle, such as when
a spending threshold is reached or when the cycle restarts.

**Custom actions:** You can now configure a budget to automatically call a stored procedure when a spending threshold is
reached. This lets you take automated actions in response to credit consumption, such as suspending warehouses, sending
custom alerts, or logging spending events to a table.

When you define a custom action, you specify whether it triggers based on projected or actual credit consumption, then
you set the threshold percentage. You can add up to 10 custom actions per budget.

For more information, see [Custom actions for budgets](/user-guide/budgets/custom-actions).

**Cycle-start actions:** You can now configure a budget to automatically call a stored procedure when the budget cycle
restarts at the beginning of its monthly period. This lets you run automated actions at the start of each cycle, such as
re-enabling warehouses or sending notifications. Cycle-start actions are particularly useful for reversing actions that
were triggered by custom actions during the previous budget cycle.

For more information, see [Cycle-start actions for budgets](/user-guide/budgets/cycle-start-actions).
