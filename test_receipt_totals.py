"""Unit tests for receipt_totals.calculate_subtotal (stdlib unittest only)."""

import unittest
from decimal import Decimal

from receipt_totals import calculate_subtotal


class CalculateSubtotalTest(unittest.TestCase):
    def test_multiple_valid_items(self):
        items = [
            {"unit_price": Decimal("10.25"), "quantity": 3},
            {"unit_price": 5, "quantity": 2},
            {"unit_price": "0.50", "quantity": 1},
        ]
        result = calculate_subtotal(items)
        self.assertEqual(result, Decimal("41.25"))  # 30.75 + 10 + 0.50
        self.assertIsInstance(result, Decimal)
        self.assertEqual(str(result), "41.25")  # exactly two decimal places

    def test_string_price_and_decimal_price(self):
        items = [
            {"unit_price": "19.99", "quantity": 2},
            {"unit_price": Decimal("0.01"), "quantity": 1},
        ]
        self.assertEqual(calculate_subtotal(items), Decimal("39.99"))

    def test_empty_input_returns_zero(self):
        result = calculate_subtotal([])
        self.assertEqual(result, Decimal("0.00"))
        self.assertIsInstance(result, Decimal)
        self.assertEqual(str(result), "0.00")

    def test_round_half_up(self):
        # 2.675 in binary float would round DOWN to 2.67; Decimal must give 2.68.
        self.assertEqual(
            calculate_subtotal([{"unit_price": Decimal("2.675"), "quantity": 1}]),
            Decimal("2.68"),
        )
        # 0.005 * 3 = 0.015 -> exactly halfway -> rounds UP to 0.02.
        self.assertEqual(
            calculate_subtotal([{"unit_price": "0.005", "quantity": 3}]),
            Decimal("0.02"),
        )
        # 1.005 * 1 -> 1.01 (rounds up at the final quantize step).
        self.assertEqual(
            calculate_subtotal([{"unit_price": Decimal("1.005"), "quantity": 1}]),
            Decimal("1.01"),
        )
        # Rounding is applied to the final sum, not per line: 0.005 + 0.005 = 0.01.
        self.assertEqual(
            calculate_subtotal(
                [
                    {"unit_price": "0.005", "quantity": 1},
                    {"unit_price": "0.005", "quantity": 1},
                ]
            ),
            Decimal("0.01"),
        )

    def test_negative_price_rejected(self):
        for bad in (-1, Decimal("-0.01"), "-5.00"):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    calculate_subtotal([{"unit_price": bad, "quantity": 1}])

    def test_zero_and_negative_quantity_rejected(self):
        for bad_qty in (0, -1, -100):
            with self.subTest(bad_qty=bad_qty):
                with self.assertRaises(ValueError):
                    calculate_subtotal([{"unit_price": Decimal("1.00"), "quantity": bad_qty}])

    def test_non_integer_and_boolean_quantity_rejected(self):
        for bad_qty in (2.0, 1.5, "3", True, False):
            with self.subTest(bad_qty=bad_qty):
                with self.assertRaises(ValueError):
                    calculate_subtotal([{"unit_price": Decimal("1.00"), "quantity": bad_qty}])

    def test_missing_required_field_rejected(self):
        with self.assertRaises(ValueError):
            calculate_subtotal([{"quantity": 1}])  # unit_price missing
        with self.assertRaises(ValueError):
            calculate_subtotal([{"unit_price": Decimal("1.00")}])  # quantity missing

    def test_float_and_boolean_price_rejected(self):
        for bad_price in (9.99, 10.0, True, False):
            with self.subTest(bad_price=bad_price):
                with self.assertRaises(ValueError):
                    calculate_subtotal([{"unit_price": bad_price, "quantity": 1}])

    def test_invalid_input_rejected(self):
        cases = [
            None,                      # items is not a list
            "not a list",              # items is not a list
            42,                        # items is not a list
            ["just a string"],         # item is not a dict
            [{"unit_price": "abc", "quantity": 1}],   # unparseable price string
            [{"unit_price": "", "quantity": 1}],      # empty price string
            [{"unit_price": "NaN", "quantity": 1}],   # non-finite price
            [{"unit_price": Decimal("Infinity"), "quantity": 1}],
            [{"unit_price": Decimal("1.00"), "quantity": None}],  # quantity None
        ]
        for bad_input in cases:
            with self.subTest(bad_input=bad_input):
                with self.assertRaises(ValueError):
                    calculate_subtotal(bad_input)


if __name__ == "__main__":
    unittest.main()
