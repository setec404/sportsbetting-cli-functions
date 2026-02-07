"""Tests for edge calculation functions"""
import pytest
from decimal import Decimal

from sbcli.core.edge import (
    prob_us_to_edge,
    prob_dec_to_edge,
    edge_us_to_prob,
    edge_dec_to_prob,
    prob_edge_to_us,
    prob_edge_to_dec,
)


class TestProbUS2Edge:
    """Tests for Probability and US Odds to Edge"""

    def test_basic_edge(self):
        """Test edge calculation from PLAN.md example"""
        result = prob_us_to_edge(Decimal('0.55'), -110)
        # 55% win prob at -110 = 5% edge
        expected = Decimal('0.05')
        assert abs(result - expected) < Decimal('0.001')

    def test_zero_edge(self):
        """Test zero edge (fair odds)"""
        # -110 implies 52.38% probability, so that should give 0 edge
        result = prob_us_to_edge(Decimal('0.523809524'), -110)
        expected = Decimal('0.0')
        assert abs(result - expected) < Decimal('0.001')

    def test_negative_edge(self):
        """Test negative edge (bad bet)"""
        result = prob_us_to_edge(Decimal('0.50'), -110)
        # 50% win prob at -110 (which implies 52.38%) should be negative edge
        assert result < Decimal('0')

    def test_positive_odds(self):
        """Test edge with positive odds"""
        result = prob_us_to_edge(Decimal('0.45'), 150)
        # +150 implies 40% probability
        # 45% at those odds should give positive edge
        assert result > Decimal('0')


class TestProbDec2Edge:
    """Tests for Probability and Decimal Odds to Edge"""

    def test_basic_edge(self):
        """Test edge calculation"""
        result = prob_dec_to_edge(Decimal('0.55'), Decimal('1.909090909'))
        # 55% * 1.909090909 - 1 = 1.05 - 1 = 0.05
        expected = Decimal('0.05')
        assert abs(result - expected) < Decimal('0.001')

    def test_zero_edge(self):
        """Test zero edge"""
        # 1/1.909090909 = 0.523809524
        result = prob_dec_to_edge(Decimal('0.523809524'), Decimal('1.909090909'))
        expected = Decimal('0.0')
        assert abs(result - expected) < Decimal('0.001')

    def test_even_odds(self):
        """Test with even odds"""
        result = prob_dec_to_edge(Decimal('0.55'), Decimal('2.0'))
        # 0.55 * 2.0 - 1 = 0.1
        expected = Decimal('0.1')
        assert abs(result - expected) < Decimal('0.001')


class TestEdgeUS2Prob:
    """Tests for Edge and US Odds to Probability"""

    def test_basic_prob(self):
        """Test probability calculation from PLAN.md example"""
        result = edge_us_to_prob(Decimal('0.05'), -110)
        # 5% edge at -110 = 55% probability
        expected = Decimal('0.55')
        assert abs(result - expected) < Decimal('0.001')

    def test_zero_edge(self):
        """Test with zero edge"""
        result = edge_us_to_prob(Decimal('0.0'), -110)
        # 0% edge means implied probability = true probability
        # -110 implies 52.38%
        expected = Decimal('0.523809524')
        assert abs(result - expected) < Decimal('0.001')

    def test_roundtrip(self):
        """Test roundtrip: prob -> edge -> prob"""
        original_prob = Decimal('0.55')
        edge = prob_us_to_edge(original_prob, -110)
        recovered_prob = edge_us_to_prob(edge, -110)
        assert abs(original_prob - recovered_prob) < Decimal('0.000001')


class TestEdgeDec2Prob:
    """Tests for Edge and Decimal Odds to Probability"""

    def test_basic_prob(self):
        """Test probability calculation"""
        result = edge_dec_to_prob(Decimal('0.05'), Decimal('1.909090909'))
        # (0.05 + 1) / 1.909090909 = 0.55
        expected = Decimal('0.55')
        assert abs(result - expected) < Decimal('0.001')

    def test_roundtrip(self):
        """Test roundtrip: prob -> edge -> prob"""
        original_prob = Decimal('0.55')
        decimal_odds = Decimal('1.909090909')
        edge = prob_dec_to_edge(original_prob, decimal_odds)
        recovered_prob = edge_dec_to_prob(edge, decimal_odds)
        assert abs(original_prob - recovered_prob) < Decimal('0.000001')


class TestProbEdge2US:
    """Tests for Probability and Edge to US Odds"""

    def test_basic_odds(self):
        """Test odds calculation from PLAN.md example"""
        result = prob_edge_to_us(Decimal('0.55'), Decimal('0.05'))
        # 55% probability with 5% edge = -110 odds
        expected = Decimal('-110')
        assert abs(result - expected) < Decimal('1')

    def test_underdog_odds(self):
        """Test with underdog odds"""
        result = prob_edge_to_us(Decimal('0.40'), Decimal('0.05'))
        # Should give positive odds
        assert result > Decimal('0')

    def test_roundtrip(self):
        """Test roundtrip: odds -> prob/edge -> odds"""
        original_odds = -110
        prob = edge_us_to_prob(Decimal('0.05'), original_odds)
        recovered_odds = prob_edge_to_us(prob, Decimal('0.05'))
        assert abs(recovered_odds - Decimal(str(original_odds))) < Decimal('1')


class TestProbEdge2Dec:
    """Tests for Probability and Edge to Decimal Odds"""

    def test_basic_odds(self):
        """Test odds calculation"""
        result = prob_edge_to_dec(Decimal('0.55'), Decimal('0.05'))
        # (0.05 + 1) / 0.55 = 1.909090909
        expected = Decimal('1.909090909')
        assert abs(result - expected) < Decimal('0.001')

    def test_even_odds(self):
        """Test with 50% probability"""
        result = prob_edge_to_dec(Decimal('0.50'), Decimal('0.0'))
        # (0 + 1) / 0.50 = 2.0
        expected = Decimal('2.0')
        assert abs(result - expected) < Decimal('0.001')

    def test_roundtrip(self):
        """Test roundtrip: odds -> prob/edge -> odds"""
        original_odds = Decimal('1.909090909')
        prob = edge_dec_to_prob(Decimal('0.05'), original_odds)
        recovered_odds = prob_edge_to_dec(prob, Decimal('0.05'))
        assert abs(recovered_odds - original_odds) < Decimal('0.000001')


class TestConsistency:
    """Test consistency between US and Decimal versions"""

    def test_edge_calculation_consistency(self):
        """Test that US and Dec versions give same edge"""
        from sbcli.core.converters import us_to_decimal

        us_odds = -110
        decimal_odds = us_to_decimal(us_odds)
        prob = Decimal('0.55')

        edge_us = prob_us_to_edge(prob, us_odds)
        edge_dec = prob_dec_to_edge(prob, decimal_odds)

        assert abs(edge_us - edge_dec) < Decimal('0.000001')

    def test_prob_calculation_consistency(self):
        """Test that US and Dec versions give same probability"""
        from sbcli.core.converters import us_to_decimal

        us_odds = -110
        decimal_odds = us_to_decimal(us_odds)
        edge = Decimal('0.05')

        prob_us = edge_us_to_prob(edge, us_odds)
        prob_dec = edge_dec_to_prob(edge, decimal_odds)

        assert abs(prob_us - prob_dec) < Decimal('0.000001')
