"""Tests for fair value calculation functions"""
import pytest
from decimal import Decimal

from sbcli.core.fair_value import (
    us_to_real,
    decimal_to_real,
    us_to_fair,
    decimal_to_fair,
)


class TestUS2Real:
    """Tests for US to Real Probabilities conversion"""

    def test_symmetric_market(self):
        """Test real probabilities for symmetric market"""
        result = us_to_real([-110, -110])
        probs = result['probabilities']
        hold = result['hold']

        # Each implied prob: 0.523809523809...
        # Real prob: 0.523809... / 1.047619... = 0.5
        assert len(probs) == 2
        assert abs(probs[0] - Decimal('0.5')) < Decimal('0.000001')
        assert abs(probs[1] - Decimal('0.5')) < Decimal('0.000001')
        assert abs(hold - Decimal('0.047619')) < Decimal('0.000001')

    def test_probabilities_sum_to_one(self):
        """Test that real probabilities sum to 1"""
        result = us_to_real([-200, 170])
        probs = result['probabilities']

        total = sum(probs)
        assert abs(total - Decimal('1')) < Decimal('0.000001')

    def test_asymmetric_market(self):
        """Test real probabilities for asymmetric market"""
        result = us_to_real([-200, 170])
        probs = result['probabilities']

        # -200 implied: 0.666666...
        # +170 implied: 0.370370...
        # Total: 1.037037...
        # Real probs: 0.666666.../1.037037... ≈ 0.643, 0.370370.../1.037037... ≈ 0.357
        assert abs(probs[0] - Decimal('0.643')) < Decimal('0.001')
        assert abs(probs[1] - Decimal('0.357')) < Decimal('0.001')


class TestDec2Real:
    """Tests for Decimal to Real Probabilities conversion"""

    def test_symmetric_market(self):
        """Test real probabilities for symmetric market"""
        result = decimal_to_real([Decimal('1.909090909'), Decimal('1.909090909')])
        probs = result['probabilities']

        assert len(probs) == 2
        assert abs(probs[0] - Decimal('0.5')) < Decimal('0.000001')
        assert abs(probs[1] - Decimal('0.5')) < Decimal('0.000001')

    def test_no_vig_market(self):
        """Test market with no vig"""
        result = decimal_to_real([Decimal('2.0'), Decimal('2.0')])
        probs = result['probabilities']
        hold = result['hold']

        # No vig means real probs = implied probs
        assert abs(probs[0] - Decimal('0.5')) < Decimal('0.000001')
        assert abs(probs[1] - Decimal('0.5')) < Decimal('0.000001')
        assert abs(hold) < Decimal('0.000001')


class TestUS2Fair:
    """Tests for US to Fair Odds conversion"""

    def test_symmetric_market(self):
        """Test fair odds for symmetric market"""
        result = us_to_fair([-110, -110])
        fair_odds = result['fair_odds']

        # Real prob = 0.5, so fair odds = +100/-100
        assert len(fair_odds) == 2
        assert abs(fair_odds[0] - Decimal('100')) < Decimal('1')
        assert abs(fair_odds[1] - Decimal('100')) < Decimal('1')

    def test_asymmetric_market(self):
        """Test fair odds for asymmetric market"""
        result = us_to_fair([-200, 176])
        fair_odds = result['fair_odds']

        # From PLAN.md example: should be around -184, +184
        assert len(fair_odds) == 2
        assert abs(fair_odds[0] - Decimal('-184')) < Decimal('2')
        assert abs(fair_odds[1] - Decimal('184')) < Decimal('2')

    def test_fair_odds_symmetric(self):
        """Test that fair odds from symmetric implied probs are symmetric"""
        result = us_to_fair([-110, -110])
        fair_odds = result['fair_odds']

        # Should be close to each other (both around +100)
        assert abs(fair_odds[0] - fair_odds[1]) < Decimal('1')


class TestDec2Fair:
    """Tests for Decimal to Fair Odds conversion"""

    def test_symmetric_market(self):
        """Test fair odds for symmetric market"""
        result = decimal_to_fair([Decimal('1.909090909'), Decimal('1.909090909')])
        fair_odds = result['fair_odds']

        # Real prob = 0.5, so fair odds = 2.0
        assert len(fair_odds) == 2
        assert abs(fair_odds[0] - Decimal('2.0')) < Decimal('0.001')
        assert abs(fair_odds[1] - Decimal('2.0')) < Decimal('0.001')

    def test_no_vig_market(self):
        """Test market with no vig"""
        result = decimal_to_fair([Decimal('2.0'), Decimal('2.0')])
        fair_odds = result['fair_odds']

        # No vig means fair odds = original odds
        assert abs(fair_odds[0] - Decimal('2.0')) < Decimal('0.001')
        assert abs(fair_odds[1] - Decimal('2.0')) < Decimal('0.001')


class TestRoundtrip:
    """Test roundtrip conversions"""

    def test_us_to_decimal_fair(self):
        """Test that US and Decimal fair calculations match"""
        from sbcli.core.converters import us_to_decimal, decimal_to_us

        us_odds = [-110, -110]
        decimal_odds = [us_to_decimal(o) for o in us_odds]

        us_result = us_to_fair(us_odds)
        dec_result = decimal_to_fair(decimal_odds)

        # Convert decimal fair odds to US for comparison
        dec_fair_as_us = [decimal_to_us(o) for o in dec_result['fair_odds']]

        assert abs(us_result['fair_odds'][0] - dec_fair_as_us[0]) < Decimal('0.1')
        assert abs(us_result['fair_odds'][1] - dec_fair_as_us[1]) < Decimal('0.1')
