"""Tests for probability calculation functions"""
import pytest
from decimal import Decimal

from sbcli.core.probability import (
    us_to_probability,
    decimal_to_probability,
)


class TestUS2Prob:
    """Tests for US to Probability conversion"""

    def test_even_odds(self):
        """Test probability from even odds (+100)"""
        result = us_to_probability(100)
        expected = Decimal('0.5')
        assert abs(result - expected) < Decimal('0.000001')

    def test_negative_odds(self):
        """Test probability from favorite odds"""
        result = us_to_probability(-110)
        # -110 implies: 110 / (110 + 100) = 110/210 = 0.523809523809...
        expected = Decimal('0.523809523809')
        assert abs(result - expected) < Decimal('0.000000001')

    def test_positive_odds(self):
        """Test probability from underdog odds"""
        result = us_to_probability(150)
        # +150 implies: 100 / (150 + 100) = 100/250 = 0.4
        expected = Decimal('0.4')
        assert abs(result - expected) < Decimal('0.000001')

    def test_heavy_favorite(self):
        """Test probability from heavy favorite"""
        result = us_to_probability(-500)
        # -500 implies: 500 / (500 + 100) = 500/600 = 0.833333...
        expected = Decimal('0.833333333')
        assert abs(result - expected) < Decimal('0.000001')

    def test_heavy_underdog(self):
        """Test probability from heavy underdog"""
        result = us_to_probability(500)
        # +500 implies: 100 / (500 + 100) = 100/600 = 0.166666...
        expected = Decimal('0.166666667')
        assert abs(result - expected) < Decimal('0.000001')

    def test_minus_200(self):
        """Test probability from -200"""
        result = us_to_probability(-200)
        # -200 implies: 200 / (200 + 100) = 200/300 = 0.666666...
        expected = Decimal('0.666666667')
        assert abs(result - expected) < Decimal('0.000001')


class TestDec2Prob:
    """Tests for Decimal to Probability conversion"""

    def test_even_odds(self):
        """Test probability from even decimal odds"""
        result = decimal_to_probability(Decimal('2.0'))
        expected = Decimal('0.5')
        assert abs(result - expected) < Decimal('0.000001')

    def test_favorite_odds(self):
        """Test probability from favorite decimal odds"""
        result = decimal_to_probability(Decimal('1.909090909'))
        # 1 / 1.909090909 = 0.523809523809...
        expected = Decimal('0.523809523809')
        assert abs(result - expected) < Decimal('0.000000001')

    def test_underdog_odds(self):
        """Test probability from underdog decimal odds"""
        result = decimal_to_probability(Decimal('2.5'))
        # 1 / 2.5 = 0.4
        expected = Decimal('0.4')
        assert abs(result - expected) < Decimal('0.000001')

    def test_heavy_favorite(self):
        """Test probability from heavy favorite decimal odds"""
        result = decimal_to_probability(Decimal('1.2'))
        # 1 / 1.2 = 0.833333...
        expected = Decimal('0.833333333')
        assert abs(result - expected) < Decimal('0.000001')

    def test_heavy_underdog(self):
        """Test probability from heavy underdog decimal odds"""
        result = decimal_to_probability(Decimal('6.0'))
        # 1 / 6.0 = 0.166666...
        expected = Decimal('0.166666667')
        assert abs(result - expected) < Decimal('0.000001')


class TestRoundtrip:
    """Test roundtrip conversions between US/Decimal and Probability"""

    def test_us_to_decimal_to_prob(self):
        """Test US -> Decimal -> Prob matches US -> Prob"""
        from sbcli.core.converters import us_to_decimal

        us_odds = -110
        prob_direct = us_to_probability(us_odds)
        decimal_odds = us_to_decimal(us_odds)
        prob_via_decimal = decimal_to_probability(decimal_odds)

        assert abs(prob_direct - prob_via_decimal) < Decimal('0.000000001')
