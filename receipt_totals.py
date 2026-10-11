"""Subtotal calculation for receipts / invoices.

`calculate_subtotal(items)` computes the sum of ``unit_price * quantity``
over all items using exact ``Decimal`` arithmetic (no binary floating
point) and returns the total quantized to two decimal places with
``ROUND_HALF_UP``.
"""

from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

__all__ = ["calculate_subtotal"]

_TWO_PLACES = Decimal("0.01")


def _parse_unit_price(value):
    """Validate and normalize a single ``unit_price`` value to Decimal.

    Accepts ``Decimal``, ``int`` or numeric ``str``. Rejects ``bool``,
    ``float``, non-finite values (NaN / Infinity), negatives and
    unparseable strings. All rejections raise ``ValueError``.
    """
    if isinstance(value, bool):
        raise ValueError(
            "unit_price must be Decimal, int or a numeric string, not bool"
        )
    if isinstance(value, Decimal):
        price = value
    elif isinstance(value, int):
        price = Decimal(value)
    elif isinstance(value, str):
        try:
            price = Decimal(value.strip())
        except InvalidOperation:
            raise ValueError(
                f"unit_price is not a valid numeric string: {value!r}"
            ) from None
    else:
        raise ValueError(
            "unit_price must be Decimal, int or a numeric string, "
            f"got {type(value).__name__}"
        )
    if not price.is_finite():
        raise ValueError("unit_price must be a finite number (no NaN/Infinity)")
    if price < 0:
        raise ValueError(f"unit_price must not be negative, got {price}")
    return price


def _parse_quantity(value):
    """Validate a single ``quantity`` value.

    Must be a positive ``int``. Rejects ``bool`` (a subclass of ``int``),
    floats, strings, zero, negatives. All rejections raise ``ValueError``.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(
            f"quantity must be a positive integer, got {type(value).__name__}"
        )
    if value <= 0:
        raise ValueError(f"quantity must be a positive integer, got {value}")
    return value


def calculate_subtotal(items):
    """Return the receipt subtotal as a ``Decimal`` with exactly 2 decimals.

    Contract:
      * ``items`` must be a ``list`` of ``dict`` objects.
      * Each item requires the fields ``unit_price`` (``Decimal``, ``int``
        or numeric ``str``; not ``bool``/``float``; not negative) and
        ``quantity`` (positive ``int``; ``bool`` and non-integers rejected).
      * Missing fields, wrong types and invalid values raise ``ValueError``.
      * An empty list returns ``Decimal("0.00")``.
      * Arithmetic is exact ``Decimal`` math; rounding to 2 decimal places
        (applied once, to the final sum) uses ``ROUND_HALF_UP``.
    """
    if not isinstance(items, list):
        raise ValueError(
            f"items must be a list of item dictionaries, got {type(items).__name__}"
        )
    total = Decimal(0)
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(
                f"item at index {index} must be a dictionary, "
                f"got {type(item).__name__}"
            )
        for field in ("unit_price", "quantity"):
            if field not in item:
                raise ValueError(
                    f"item at index {index} is missing required field {field!r}"
                )
        price = _parse_unit_price(item["unit_price"])
        quantity = _parse_quantity(item["quantity"])
        total += price * quantity
    return total.quantize(_TWO_PLACES, rounding=ROUND_HALF_UP)
