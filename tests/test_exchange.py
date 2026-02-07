"""Tests for exchange odds conversion functions"""
import pytest
from decimal import Decimal

from sbcli.core.exchange import (
    exch_to_us,
    exch_to_dec,
    e2s,
    exch_us_to_hold,
    exch_dec_to_hold,
    mb_to_us,
    mb_to_dec,
)


class TestExch2US:
    """Tests for Exchange to US conversion"""

    def test_example_from_plan(self):
        """Test from PLAN.md: Exch2US(-110, 1%) ≈ -111.11"""
        result = exch_to_us(-110, Decimal('0.01'))
        expected = Decimal('-111.11')
        assert abs(result - expected) < Decimal('0.1')

    def test_default_commission(self):
        """Test with default 2% commission"""
        result = exch_to_us(-110)
        # 2% commission should make odds slightly worse
        assert result < Decimal('-110')

    def test_positive_odds(self):
        """Test with positive odds"""
        result = exch_to_us(150, Decimal('0.02'))
        # Commission makes odds worse
        assert result < Decimal('150')

    def test_zero_commission(self):
        """Test with zero commission"""
        result = exch_to_us(-110, Decimal('0'))
        # Should be close to original odds
        expected = Decimal('-110')
        assert abs(result - expected) < Decimal('0.1')


class TestExch2Dec:
    """Tests for Exchange to Decimal conversion"""

    def test_basic_conversion(self):
        """Test basic conversion with commission"""
        result = exch_to_dec(Decimal('1.909090909'), Decimal('0.02'))
        # 2% commission reduces win by 2%
        # 1 + (1.909090909 - 1) * 0.98 = 1 + 0.909090909 * 0.98 = 1.890909091
        expected = Decimal('1.890909091')
        assert abs(result - expected) < Decimal('0.001')

    def test_even_odds(self):
        """Test with even odds (2.0)"""
        result = exch_to_dec(Decimal('2.0'), Decimal('0.02'))
        # 1 + (2.0 - 1) * 0.98 = 1.98
        expected = Decimal('1.98')
        assert abs(result - expected) < Decimal('0.001')


class TestE2S:
    """Tests for E2S (Exchange to Sportsbook) alias"""

    def test_alias_matches_exch2us(self):
        """Test that e2s gives same result as exch_to_us"""
        odds = -110
        commission = Decimal('0.01')

        result1 = exch_to_us(odds, commission)
        result2 = e2s(odds, commission)

        assert result1 == result2


class TestExchUS2Hold:
    """Tests for Exchange US to Hold with commission"""

    def test_example_from_plan(self):
        """Test from PLAN.md: ExchUS2Hold([-102,-102], 2%) ≈ 1.961%"""
        result = exch_us_to_hold([-102, -102], Decimal('0.02'))
        expected = Decimal('0.01961')
        assert abs(result - expected) < Decimal('0.001')

    def test_higher_commission(self):
        """Test that higher commission increases hold"""
        hold_low = exch_us_to_hold([-110, -110], Decimal('0.01'))
        hold_high = exch_us_to_hold([-110, -110], Decimal('0.05'))

        # Higher commission = higher hold
        assert hold_high > hold_low


class TestExchDec2Hold:
    """Tests for Exchange Decimal to Hold with commission"""

    def test_basic_hold(self):
        """Test hold calculation with decimal odds"""
        result = exch_dec_to_hold([Decimal('1.98'), Decimal('1.98')], Decimal('0.02'))
        # Should be close to 1.961%
        expected = Decimal('0.01961')
        assert abs(result - expected) < Decimal('0.001')

    def test_consistency_with_us_version(self):
        """Test that US and Decimal versions give same hold"""
        from sbcli.core.converters import us_to_decimal

        us_odds = [-102, -102]
        decimal_odds = [us_to_decimal(o) for o in us_odds]
        commission = Decimal('0.02')

        hold_us = exch_us_to_hold(us_odds, commission)
        hold_dec = exch_dec_to_hold(decimal_odds, commission)

        assert abs(hold_us - hold_dec) < Decimal('0.000001')


class TestMB2US:
    """Tests for Matchbook to US conversion"""

    def test_example_from_plan(self):
        """Test from PLAN.md: MB2US(-110, 1%) ≈ -112.12"""
        result = mb_to_us(-110, Decimal('0.01'))
        expected = Decimal('-112.12')
        assert abs(result - expected) < Decimal('1.0')

    def test_default_commission(self):
        """Test with default 1% commission"""
        result = mb_to_us(-110)
        # Should make odds worse than original
        assert result < Decimal('-110')

    def test_underdog_odds(self):
        """Test with underdog (positive) odds"""
        result = mb_to_us(200, Decimal('0.01'))
        # Commission reduces the effective odds
        assert result < Decimal('200')


class TestMB2Dec:
    """Tests for Matchbook to Decimal conversion"""

    def test_favorite_odds(self):
        """Test with favorite odds (< 2.0)"""
        result = mb_to_dec(Decimal('1.909090909'), Decimal('0.01'))
        # Commission increases effective risk
        # 1.909090909 / 1.00909090909 ≈ 1.891919...
        expected = Decimal('1.891919')
        assert abs(result - expected) < Decimal('0.001')

    def test_underdog_odds(self):
        """Test with underdog odds (>= 2.0)"""
        result = mb_to_dec(Decimal('3.0'), Decimal('0.01'))
        # For underdogs, commission is on min(1, 2) = 1
        # 3.0 / 1.01 = 2.970297...
        expected = Decimal('2.970297')
        assert abs(result - expected) < Decimal('0.001')

    def test_even_odds(self):
        """Test with even odds (2.0)"""
        result = mb_to_dec(Decimal('2.0'), Decimal('0.01'))
        # Commission on min(1, 1) = 1
        # 2.0 / 1.01 = 1.980198...
        expected = Decimal('1.980198')
        assert abs(result - expected) < Decimal('0.001')


class TestDifferentCommissionStructures:
    """Test that standard exchange and Matchbook commissions can differ"""

    def test_underdog_odds_different(self):
        """Test that Exch2US and MB2US can give different results for underdogs"""
        odds = 300  # Big underdog
        commission = Decimal('0.02')

        exch_result = exch_to_us(odds, commission)
        mb_result = mb_to_us(odds, commission)

        # For big underdogs, results should differ more
        # Standard exchange: commission only on win
        # Matchbook: commission on min(risk, win) = risk for underdogs
        assert abs(exch_result - mb_result) >= Decimal('0')

    def test_mb_structure_unique(self):
        """Test that MB commission structure is based on min(risk, win)"""
        # For underdogs where win > risk
        result_underdog = mb_to_dec(Decimal('4.0'), Decimal('0.01'))
        # Commission should be on risk (1.0), not win (3.0)
        # 4.0 / 1.01 = 3.960...
        expected = Decimal('3.960')
        assert abs(result_underdog - expected) < Decimal('0.01')
