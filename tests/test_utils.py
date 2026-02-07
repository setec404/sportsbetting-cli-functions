"""Tests for utility functions"""
import pytest
from decimal import Decimal
import math

from sbcli.core.utils import invlg


class TestInvLg:
    """Tests for inverse logit function"""

    def test_zero(self):
        """Test invlg(0) = 0.5"""
        result = invlg(0)
        expected = Decimal('0.5')
        assert abs(result - expected) < Decimal('0.000001')

    def test_positive_value(self):
        """Test invlg with positive value"""
        result = invlg(1)
        # exp(1) / (1 + exp(1)) = 2.718... / 3.718... ≈ 0.731
        expected = Decimal('0.731058579')
        assert abs(result - expected) < Decimal('0.000001')

    def test_negative_value(self):
        """Test invlg with negative value"""
        result = invlg(-1)
        # exp(-1) / (1 + exp(-1)) = 0.368... / 1.368... ≈ 0.269
        expected = Decimal('0.268941421')
        assert abs(result - expected) < Decimal('0.000001')

    def test_large_positive(self):
        """Test invlg with large positive value"""
        result = invlg(10)
        # Should approach 1
        assert result > Decimal('0.99')
        assert result < Decimal('1.0')

    def test_large_negative(self):
        """Test invlg with large negative value"""
        result = invlg(-10)
        # Should approach 0
        assert result > Decimal('0.0')
        assert result < Decimal('0.01')

    def test_symmetry(self):
        """Test that invlg(-x) = 1 - invlg(x)"""
        x = Decimal('2')
        result_pos = invlg(x)
        result_neg = invlg(-x)

        # invlg(-x) should equal 1 - invlg(x)
        assert abs(result_neg - (Decimal('1') - result_pos)) < Decimal('0.000001')

    def test_bounds(self):
        """Test that invlg always returns value between 0 and 1"""
        test_values = [-100, -10, -1, 0, 1, 10, 100]

        for x in test_values:
            result = invlg(x)
            assert result >= Decimal('0')
            assert result <= Decimal('1')

    def test_decimal_input(self):
        """Test with Decimal input"""
        result = invlg(Decimal('0.5'))
        # exp(0.5) / (1 + exp(0.5)) ≈ 0.622
        expected = Decimal('0.622459331')
        assert abs(result - expected) < Decimal('0.000001')

    def test_relationship_to_probability(self):
        """Test invlg relationship to log odds"""
        # If p = invlg(x), then x = log(p / (1-p))
        # So invlg(log(p / (1-p))) = p

        p = Decimal('0.7')
        # log_odds = ln(0.7 / 0.3) = ln(2.333...) ≈ 0.847
        log_odds = math.log(float(p) / (1 - float(p)))

        result = invlg(log_odds)
        assert abs(result - p) < Decimal('0.000001')
