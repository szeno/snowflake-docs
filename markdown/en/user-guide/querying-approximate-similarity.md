# Estimating Similarity of Two or More Sets

Snowflake uses MinHash for estimating the approximate similarity between two or more data sets. The MinHash scheme compares sets without computing the intersection or union of the sets, which enables
efficient and effective estimation.

## Overview

Typically, the Jaccard similarity coefficient (or index) is used to compare the similarity between two sets. For two sets, `A` and `B`, the Jaccard index is defined to be the ratio of the
size of their intersection and the size of their union:

> `J(A,B) = (A ∩ B) / (A ∪ B)`

However, this calculation can consume significant resources and time and, therefore, is not ideal for large data sets.

In contrast, the goal of the MinHash scheme is to estimate `J(A,B)` quickly, without computing the intersection or union.

## SQL Functions

The following [Aggregate functions](/sql-reference/functions-aggregation) are provided for estimating approximate similarity using MinHash:

- [MINHASH](/sql-reference/functions/minhash): Returns a MinHash state containing a MinHash array of length *k* (input argument).
- [MINHASH\_COMBINE](/sql-reference/functions/minhash_combine): Combines two (or more) input MinHash states into a single output MinHash state.
- [APPROXIMATE\_SIMILARITY](/sql-reference/functions/approximate_similarity) (or [APPROXIMATE\_JACCARD\_INDEX](/sql-reference/functions/approximate_jaccard_index)): Returns an estimation of the similarity (Jaccard index) of input sets based on
  their MinHash states.

## Implementation Details

As detailed in [MinHash](https://en.wikipedia.org/wiki/MinHash) (in Wikipedia):

> “Let `H` be a hash function that maps the members of `A` and `B` to distinct integer values and, for any set `S`, define `H_min(S)` to be the minimal member of `S`
> with respect to `H`, i.e. the member `s` of `S` with the minimum value of `H(s)`, as expressed in the following equation:
>
> > `H_min(S) = argmin_{s in S} (H(s))`
>
> If we apply `H_min` to both `A` and `B`, we will get the same value exactly when the element of the union `A ∪ B` with minimum hash value lies in the intersection `A ∩ B`. The probability of this being true is the above ratio, therefore:
>
> > `Pr[H_min(A) = H_min(B)] = J(A,B)`
>
> Namely, assuming randomly chosen sets `A` and `B`, the probability that `H_min(A) = H_min(B)` holds is equal to `J(A,B)`. In other words, if `X` is the random variable
> that is 1 when `H_min(A) = H_min(B)` and 0 otherwise, then `X` is an unbiased estimator of `J(A,B)`. Note that `X` has a too large variance to be a good estimator for the
> Jaccard index on its own (since it is always 0 or 1).
>
> The MinHash scheme reduces this variance by averaging together several variables constructed in the same way using `k` number of different hash functions.”

In order to achieve this, the [MINHASH](/sql-reference/functions/minhash) function initially creates `k` number of different hash functions and applies them to every element of each input set, retaining
the minimum of each one, to produce a MinHash array (also called a MinHash *state*) for each set. More specifically, for `i = 0 to k-1`, the entry `i` of the MinHash array for set
`A` (shown by `MinHash_A`) corresponds to the minimum value of hash function `H_i` applied to every element of set `A`.

Finally, an approximation for the similarity of the two sets `A` and `B` is calculated as:

> `J_apprx(A,B) = (# of entries MinHash_A and MinHash_B agree on) / k`

## Examples

In the following example, we show how this scheme and the corresponding functions can be used in order to approximate the similarity of two sets of elements.

First, create two sample tables and insert some sample data:

> Copy code
>
> ```
> CREATE OR REPLACE TABLE mhtab1(c1 NUMBER,c2 DOUBLE,c3 TEXT,c4 DATE);
> CREATE OR REPLACE TABLE mhtab2(c1 NUMBER,c2 DOUBLE,c3 TEXT,c4 DATE);
>
> INSERT INTO mhtab1 VALUES
>     (1, 1.1, 'item 1', to_date('2016-11-30')),
>     (2, 2.31, 'item 2', to_date('2016-11-30')),
>     (3, 1.1, 'item 3', to_date('2016-11-29')),
>     (4, 44.4, 'item 4', to_date('2016-11-30'));
>
> INSERT INTO mhtab2 VALUES
>     (1, 1.1, 'item 1', to_date('2016-11-30')),
>     (2, 2.31, 'item 2', to_date('2016-11-30')),
>     (3, 1.1, 'item 3', to_date('2016-11-29')),
>     (4, 44.4, 'item 4', to_date('2016-11-30')),
>     (6, 34.23, 'item 6', to_date('2016-11-29'));
> ```

Then, approximate the similarity of the two sets (tables `mhtab1` and `mhtab2`) using their MinHash states:

> Copy code
>
> ```
> SELECT APPROXIMATE_SIMILARITY(mh) FROM
>     ((SELECT MINHASH(100, *) AS mh FROM mhtab1)
>     UNION ALL
>     (SELECT MINHASH(100, *) AS mh FROM mhtab2));
>
> +----------------------------+
> | APPROXIMATE_SIMILARITY(MH) |
> |----------------------------|
> |                       0.79 |
> +----------------------------+
> ```

The similarity index of these two tables is approximated as 0.79, as opposed to the exact value 0.8 (i.e., 4/5).
