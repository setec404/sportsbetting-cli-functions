"""Tests for win/loss calculation functions"""
import pytest
from decimal import Decimal

from sbcli.core.winnings import (
    us_to_win,
    decimal_to_win,
    us_to_result,
    decimal_to_result,
)


class TestUS2Win:
    """Tests for US to Win conversion"""

    def test_negative_odds_with_wager(self):
        """Test win calculation with negative odds and wager"""
        result = us_to_win(-120, 120)
        expected = Decimal('100')
        assert abs(result - expected) < Decimal('0.01')

    def test_negative_odds_default_wager(self):
        """Test win calculation with negative odds and default wager"""
        result = us_to_win(-110)
        expected = Decimal('0.909090909')
        assert abs(result - expected) < Decimal('0.000000001')

    def test_positive_odds_with_wager(self):
        """Test win calculation with positive odds and wager"""
        result = us_to_win(150, 100)
        expected = Decimal('150')
        assert abs(result - expected) < Decimal('0.01')

    def test_positive_odds_default_wager(self):
        """Test win calculation with positive odds and default wager"""
        result = us_to_win(150)
        expected = Decimal('1.5')
        assert abs(result - expected) < Decimal('0.01')

    def test_even_odds(self):
        """Test win calculation with even odds"""
        result = us_to_win(100, 100)
        expected = Decimal('100')
        assert abs(result - expected) < Decimal('0.01')


class TestDec2Win:
    """Tests for Decimal to Win conversion"""

    def test_decimal_with_wager(self):
        """Test win calculation with decimal odds and wager"""
        result = decimal_to_win(Decimal('1.909090909'), 110)
        expected = Decimal('100')
        assert abs(result - expected) < Decimal('0.01')

    def test_decimal_default_wager(self):
        """Test win calculation with decimal odds and default wager"""
        result = decimal_to_win(Decimal('2.5'))
        expected = Decimal('1.5')
        assert abs(result - expected) < Decimal('0.01')

    def test_underdog_decimal(self):
        """Test win calculation with underdog decimal odds"""
        result = decimal_to_win(Decimal('2.5'), 100)
        expected = Decimal('150')
        assert abs(result - expected) < Decimal('0.01')


class TestUS2Res:
    """Tests for US to Result conversion"""

    def test_push(self):
        """Test result calculation for push"""
        result = us_to_result(-120, 120, "PUSH")
        expected = Decimal('0')
        assert result == expected

    def test_push_p(self):
        """Test result calculation for push with 'P'"""
        result = us_to_result(-120, 120, "P")
        expected = Decimal('0')
        assert result == expected

    def test_push_zero(self):
        """Test result calculation for push with 0"""
        result = us_to_result(-120, 120, 0)
        expected = Decimal('0')
        assert result == expected

    def test_win(self):
        """Test result calculation for win"""
        result = us_to_result(-110, 200, "Win")
        expected = Decimal('181.818181818')
        assert abs(result - expected) < Decimal('0.01')

    def test_win_w(self):
        """Test result calculation for win with 'W'"""
        result = us_to_result(-110, 200, "W")
        expected = Decimal('181.818181818')
        assert abs(result - expected) < Decimal('0.01')

    def test_win_one(self):
        """Test result calculation for win with 1"""
        result = us_to_result(-110, 200, 1)
        expected = Decimal('181.818181818')
        assert abs(result - expected) < Decimal('0.01')

    def test_loss(self):
        """Test result calculation for loss"""
        result = us_to_result(-110, 100, "LOSS")
        expected = Decimal('-100')
        assert result == expected

    def test_loss_l(self):
        """Test result calculation for loss with 'L'"""
        result = us_to_result(-110, 100, "L")
        expected = Decimal('-100')
        assert result == expected

    def test_loss_negative_one(self):
        """Test result calculation for loss with -1"""
        result = us_to_result(-110, 100, -1)
        expected = Decimal('-100')
        assert result == expected

    def test_positive_odds_win(self):
        """Test result calculation for positive odds win"""
        result = us_to_result(150, 100, "WIN")
        expected = Decimal('150')
        assert abs(result - expected) < Decimal('0.01')


class TestDec2Res:
    """Tests for Decimal to Result conversion"""

    def test_win(self):
        """Test result calculation for win"""
        result = decimal_to_result(Decimal('1.909090909'), 200, "Win")
        expected = Decimal('181.818181818')
        assert abs(result - expected) < Decimal('0.01')

    def test_loss(self):
        """Test result calculation for loss"""
        result = decimal_to_result(Decimal('2.5'), 100, "LOSS")
        expected = Decimal('-100')
        assert result == expected

    def test_push(self):
        """Test result calculation for push"""
        result = decimal_to_result(Decimal('2.0'), 100, "P")
        expected = Decimal('0')
        assert result == expected

    def test_win_default_wager(self):
        """Test result calculation with default wager"""
        result = decimal_to_result(Decimal('2.5'), result="WIN")
        expected = Decimal('1.5')
        assert abs(result - expected) < Decimal('0.01')
