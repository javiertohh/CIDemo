import unittest

from duckfine import DuckFine


class TestDuckFine(unittest.TestCase):
    def test_new_duckfine_starts_with_member_id_and_zero_balance(self):
        fine = DuckFine("member-123")

        self.assertEqual(fine.member_id, "member-123")
        self.assertEqual(fine.total_owed, 0.0)

    def test_first_two_late_days_are_free(self):
        fine = DuckFine("member-123")

        fee = fine.charge(2)

        self.assertEqual(fee, 0.0)
        self.assertEqual(fine.total_owed, 0.0)

    def test_standard_charge_is_fifty_cents_per_chargeable_day(self):
        fine = DuckFine("member-123")

        fee = fine.charge(5)

        self.assertEqual(fee, 1.50)

    def test_deluxe_charge_is_double_the_standard_charge(self):
        fine = DuckFine("member-123")

        fee = fine.charge(5, deluxe=True)

        self.assertEqual(fee, 3.00)

    def test_single_charge_cannot_exceed_the_maximum_fee(self):
        fine = DuckFine("member-123")

        fee = fine.charge(20)

        self.assertEqual(fee, 5.00)

    def test_charges_are_added_to_the_total_balance(self):
        fine = DuckFine("member-123")

        fine.charge(4)
        fine.charge(3)

        self.assertEqual(fine.total_owed, 1.50)

    def test_negative_late_days_are_rejected_without_changing_balance(self):
        fine = DuckFine("member-123")

        with self.assertRaisesRegex(ValueError, "days_late must not be negative"):
            fine.charge(-1)

        self.assertEqual(fine.total_owed, 0.0)


if __name__ == "__main__":
    unittest.main()
