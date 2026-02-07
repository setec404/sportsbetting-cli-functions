"""Tests for hold calculation functions"""
import pytest
from decimal import Decimal

from sbcli.core.hold import (
    us_to_hold,
    decimal_to_hold,
)


class TestUS2Hold:
    """Tests for US to Hold conversion"""

    def test_two_way_market(self):
        """Test hold calculation for standard two-way market"""
        result = us_to_hold([-110, -110])
        # Each side: 110/(110+100) = 0.523809523809...
        # Total: 1.047619... - 1 = 0.047619... = 4.7619%
        expected = Decimal('0.047619')
        assert abs(result - expected) < Decimal('0.000001')

    def test_asymmetric_market(self):
        """Test hold calculation for asymmetric market"""
        result = us_to_hold([-200, 170])
        # -200: 200/(200+100) = 0.666666...
        # +170: 100/(170+100) = 0.370370...
        # Total: 1.037037... - 1 = 0.037037...
        expected = Decimal('0.037037')
        assert abs(result - expected) < Decimal('0.000001')

    def test_three_way_market(self):
        """Test hold calculation for three-way market"""
        result = us_to_hold([-110, -110, -110])
        # Each: 0.523809523809...
        # Total: 1.571428... - 1 = 0.571428...
        expected = Decimal('0.571428')
        assert abs(result - expected) < Decimal('0.000001')


class TestDec2Hold:
    """Tests for Decimal to Hold conversion"""

    def test_two_way_market(self):
        """Test hold calculation for standard two-way market"""
        result = decimal_to_hold([Decimal('1.909090909'), Decimal('1.909090909')])
        # Each side: 1/1.909090909 = 0.523809523809...
        # Total: 1.047619... - 1 = 0.047619...
        expected = Decimal('0.047619')
        assert abs(result - expected) < Decimal('0.000001')

    def test_even_odds(self):
        """Test hold with no vig (even odds)"""
        result = decimal_to_hold([Decimal('2.0'), Decimal('2.0')])
        # Each side: 1/2.0 = 0.5
        # Total: 1.0 - 1 = 0.0
        expected = Decimal('0.0')
        assert abs(result - expected) < Decimal('0.000001')

    def test_roundtrip(self):
        """Test that US and Decimal produce same hold"""
        from sbcli.core.converters import us_to_decimal

        us_odds = [-110, -110]
        decimal_odds = [us_to_decimal(o) for o in us_odds]

        us_hold = us_to_hold(us_odds)
        dec_hold = decimal_to_hold(decimal_odds)

        assert abs(us_hold - dec_hold) < Decimal('0.000000001')
