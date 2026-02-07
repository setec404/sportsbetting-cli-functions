"""Tests for odds conversion functions"""
import pytest
from decimal import Decimal

from sbcli.core.converters import (
    us_to_decimal,
    us_to_decimal_parlay,
    decimal_to_us,
    us_to_parlay,
)


class TestUS2Dec:
    """Tests for US to Decimal conversion"""

    def test_negative_odds(self):
        """Test conversion of negative US odds"""
        result = us_to_decimal(-110)
        expected = Decimal('1.909090909')
        assert abs(result - expected) < Decimal('0.000000001')

    def test_positive_odds(self):
        """Test conversion of positive US odds"""
        result = us_to_decimal(150)
        expected = Decimal('2.5')
        assert abs(result - expected) < Decimal('0.000000001')

    def test_even_odds(self):
        """Test conversion of even US odds (+100)"""
        result = us_to_decimal(100)
        expected = Decimal('2.0')
        assert abs(result - expected) < Decimal('0.000000001')

    def test_heavy_favorite(self):
        """Test conversion of heavy favorite odds"""
        result = us_to_decimal(-500)
        expected = Decimal('1.2')
        assert abs(result - expected) < Decimal('0.000000001')

    def test_heavy_underdog(self):
        """Test conversion of heavy underdog odds"""
        result = us_to_decimal(500)
        expected = Decimal('6.0')
        assert abs(result - expected) < Decimal('0.000000001')


class TestUS2DecParlay:
    """Tests for US to Decimal Parlay conversion"""

    def test_three_leg_parlay(self):
        """Test 3-leg parlay conversion"""
        result = us_to_decimal_parlay([-110, -110, -110])
        # 1.909090909^3 = 6.957926371...
        expected = Decimal('6.957926371')
        assert abs(result - expected) < Decimal('0.000001')

    def test_two_leg_parlay(self):
        """Test 2-leg parlay conversion"""
        result = us_to_decimal_parlay([-110, 150])
        # -110 = 1.909090909, 150 = 2.5
        # Parlay = 1.909090909 * 2.5 = 4.772727273
        expected = Decimal('4.772727273')
        assert abs(result - expected) < Decimal('0.000000001')

    def test_single_leg(self):
        """Test single leg (should match us_to_decimal)"""
        result = us_to_decimal_parlay([-110])
        expected = us_to_decimal(-110)
        assert abs(result - expected) < Decimal('0.000000001')


class TestDec2US:
    """Tests for Decimal to US conversion"""

    def test_favorite_odds(self):
        """Test conversion of favorite decimal odds"""
        result = decimal_to_us(Decimal('1.909090909'))
        expected = Decimal('-110')
        assert abs(result - expected) < Decimal('0.01')

    def test_underdog_odds(self):
        """Test conversion of underdog decimal odds"""
        result = decimal_to_us(Decimal('2.5'))
        expected = Decimal('150')
        assert abs(result - expected) < Decimal('0.01')

    def test_even_odds(self):
        """Test conversion of even decimal odds"""
        result = decimal_to_us(Decimal('2.0'))
        expected = Decimal('100')
        assert abs(result - expected) < Decimal('0.01')

    def test_roundtrip_negative(self):
        """Test roundtrip conversion (US -> Decimal -> US) for negative odds"""
        original = -110
        decimal = us_to_decimal(original)
        result = decimal_to_us(decimal)
        assert abs(result - Decimal(str(original))) < Decimal('0.01')

    def test_roundtrip_positive(self):
        """Test roundtrip conversion (US -> Decimal -> US) for positive odds"""
        original = 150
        decimal = us_to_decimal(original)
        result = decimal_to_us(decimal)
        assert abs(result - Decimal(str(original))) < Decimal('0.01')


class TestUS2Par:
    """Tests for US to Parlay US conversion"""

    def test_three_leg_parlay_us(self):
        """Test 3-leg parlay to US odds"""
        result = us_to_parlay([-110, -110, -110])
        # Parlay decimal = 6.957926371
        # US odds = (6.957926371 - 1) * 100 = 595.7926371
        expected = Decimal('595.7926')
        assert abs(result - expected) < Decimal('0.1')

    def test_mixed_odds_parlay(self):
        """Test parlay with mixed positive/negative odds"""
        result = us_to_parlay([-110, 150])
        # Parlay decimal = 4.772727273
        # US odds = (4.772727273 - 1) * 100 = 377.2727273
        expected = Decimal('377.2727273')
        assert abs(result - expected) < Decimal('0.1')
