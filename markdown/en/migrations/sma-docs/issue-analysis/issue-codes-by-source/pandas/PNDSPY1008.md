# PNDSPY1008

**Message** `pandas.core.series.Series.hist` has a partial mapping, Snowpark pandas doesn’t yet support the `bins` parameter with types other than `int`.

**Category** Warning

## Description

This issue appears when the SMA identifies a [pandas.core.series.Series.hist](https://pandas.pydata.org/docs/reference/api/pandas.Series.hist.html) usage.
Snowpark pandas doesn’t yet support the `bins` parameter with types other than `int`.

## Scenario

An unsupported use of `pandas.core.series.Series.hist`.

### Input

The following example shows an unsupported use of `pandas.core.series.Series.hist`.

Copy code

```
import pandas as pd

data = pd.Series([[1.2, -0.5, 0.3, 2.1, -2.2, 1.7, 0.0, -1.1, 2.5, -2.8]])
custom_bins = [-3, -2, -1, 0, 1, 2, 3]
data.hist(bins=custom_bins)
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()
```

### Output

The SMA adds the EWI `PNDSPY1008` to the output code to indicate that in one scenario it isn’t supported in Snowpark pandas.

Copy code

```
from snowflake.snowpark.modin import plugin
import modin.pandas as pd

data = pd.Series([[1.2, -0.5, 0.3, 2.1, -2.2, 1.7, 0.0, -1.1, 2.5, -2.8]])
custom_bins = [-3, -2, -1, 0, 1, 2, 3]
#EWI: PNDSPY1008 => pandas.core.series.Series.hist has a partial mapping, Snowpark pandas doesn't yet support the `bins` parameter with types other than `int`.
data.hist(bins=custom_bins)
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()
```

## Recommended fix

This requires a manual change using the numpy [digitize](https://numpy.org/doc/stable/reference/generated/numpy.digitize.html) function. To use `digitize`, import numpy and replace `pd.Series` with `np.array`. Then count the frequencies for each bin and create labels for the custom bins. Finally, use `plt.bar` to plot the histogram with custom labels.
Here is the previous output code with the fix:

Copy code

```
from snowflake.snowpark.modin import plugin
import modin.pandas as pd
import numpy as np

data = np.array([[1.2, -0.5, 0.3, 2.1, -2.2, 1.7, 0.0, -1.1, 2.5, -2.8]])
custom_bins = [-3, -2, -1, 0, 1, 2, 3]
bin_indices = np.digitize(data, custom_bins, right=False)

counts = [np.sum(bin_indices == i) for i in range(1, len(custom_bins))]

bin_labels = [f"({custom_bins[i - 1]}, {custom_bins[i]})" for i in range(1, len(custom_bins))]

plt.bar(bin_labels, counts, edgecolor='black', alpha=0.7)
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()
```
