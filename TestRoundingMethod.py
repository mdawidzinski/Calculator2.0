from unittest import TestCase

from RoundingMethod import RoundingMethod


class TestRoundingMethod(TestCase):
    def test_round_away_from_zero_with_zero(self):
        # Given
        val_tested_object = 0
        expected_result = 0.0

        # When
        result = RoundingMethod.round_away_from_zero(val_tested_object, 13)

        # Then
        self.assertEqual(expected_result, result)
