# agent-github-test

## Receipt subtotal (`receipt_totals.py`)

`calculate_subtotal(items)` computes the sum of `unit_price * quantity` over all items with exact `Decimal` arithmetic and returns the total rounded to exactly two decimal places using `ROUND_HALF_UP`.

### Input contract

- `items`: a `list` of `dict` objects; each item must contain:
  - `unit_price`: `Decimal`, `int`, or numeric `str` (e.g. `"19.99"`). `bool` and `float` are rejected. Negative and non-finite (NaN/Infinity) values are rejected.
  - `quantity`: a positive `int`. `bool`, `float`, strings, zero and negatives are rejected.
- Missing fields, wrong types or invalid values raise `ValueError` with a clear message.
- An empty list returns `Decimal("0.00")`.

### Output

- A `decimal.Decimal` quantized to two decimal places (e.g. `Decimal("41.75")`). Rounding (`ROUND_HALF_UP`) is applied once, to the final sum.

### Run the tests

```
python -m unittest -v
```
