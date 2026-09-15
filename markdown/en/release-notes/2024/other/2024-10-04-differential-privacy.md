# October 04, 2024 — Differential Privacy — *General Availability*

With this release, we are pleased to announce the general availability of differential privacy in Snowflake.

Differential privacy is a widely recognized standard for data privacy that limits the risk that someone could leak sensitive information
from a sensitive dataset, even if they are carrying out a targeted privacy attack. Data providers implement differential privacy by
assigning privacy policies to their sensitive tables and views. As analysts query the protected data, Snowflake uses rigorous mathematics to
ensure that they cannot identify individuals and entities in the dataset to an unacceptable degree of certainty.

Data owners can now change the default settings of a privacy budget, and analysts and data owners can call a system function to estimate how
many more queries can be run before reaching the limit of a privacy budget.

For more information, see [Differential privacy in Snowflake](/user-guide/diff-privacy/differential-privacy-overview).
