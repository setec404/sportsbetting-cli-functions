If you're like me, you frequently reuse many of the same excel sports betting formulas. I've compiled a few related to odds manipulation into this Excel template file as VBA functions. Eventually, I plan to greatly expand on these.

Here are the included functions:
SBRVer(): Displays current template version number.
US2Dec(USOdds) (usage 1): Converts US-style to decimal. Example: US2Dec(-110) ≈ 1.909090909
US2Dec(range of USOdds) (usage 2): Converts an array or Excel range of US-style odds to decimal parlay odds. Example: US2Dec(-110,-110) ≈ 3.644628099
US2Par(range of USOdds): Converts an array or Excel range of US-style odds to US-style true parlay odds. Example: US2Par(-110,-110,-110) ≈ +595.7926.
Dec2US(DecimalOdds): Converts decimal odds to US. Example: US2Dec(1.909090909) = -110.
US2Win(USOdds, WagerQuantity {{default = 1}) or Dec2Win(DecOdds, WagerQuantity {{default = 1}): Converts US or Decimal odds and wager size to potential win quantity. Note that by using the default value of 1 for wager size, these two functions effectively convert from US/decimal odds to fractional odds. Example, US2Win(-120,120) = 100, or US2Win(-110) ≈ 0.90909.
US2Res(USOdds, WagerQuantity {{default = 1}, Result) or Dec2Win(DecOdds, WagerQuantity {{default = 1}, Result): Converts US or Decimal odds, wager size, and result (where "WIN", "W", or "1", corresponds to a win; "LOSS", "L", or -1 corresponds to a loss; and "PUSH", "P", or 0 corresponds to a push). Example, US2Res(-120,120,"P") = 0, or =US2Res(-110, 200,"Win") ≈ 181.82.
US2Prob(USOdds) or Dec2Prob(DecimalOdds): Converts from US or decimal odds to probability. Example: US2Prob(+100) = Dec2Prob(2.0000) = 50%.
US2Hold(range of US Odds) or Dec2Hold(range of Decimal Odds): Calculates theoretical hold based on an Excel range of US or decimal odds. Example: if cells A1 and A2 are both -110, US2Hold(A1:A2) = 4.54545%.
{US2Real(range of US Odds)} or {Dec2Real(range of Decimal Odds)}: (array function) Returns an array of zero-vig probabilities based on an Excel range of US or decimal odds. Example: if cells A1 and A2 are both -110, if B1, B2, and B3 were set to the array formula {=US2Real(A1:A2)}, B1 and B2 would both have the value of 50%, and B3 would have the value of the theoretical hold (4.54545%).
{US2Fair(range of US Odds)} or {Dec2Fair(range of Decimal Odds)}: (array function) Returns an array of fair value zero-vig odds based on an Excel range of US or decimal odds. Example: if cells A1 and A2 are -200 and +176, respectively, and if B1 and B2 were set to the array formula {=US2Fair(A1:A2)}, B1 and B2 would display the values of -184 and +184, respectively.
ProbUS2Edge(Probability, USOdds) or ProbDec2Edge(Probability, DecimalOdds): Calculates edge based on win probability and US or decimal odds. Example: ProbUS2Edge(55%,-110) = 5%
EdgeUS2Prob(Edge, USOdds) or EdgeDec2Prob(Edge, DecimalOdds): Calculates win probability based on edge and US or decimal odds. Example: ProbUS2Edge(5%,-110) = 55%.
ProbEdge2US(Probability, Edge) or ProbEdge2Dec(Probability, Edge): Calculates US or decimal odds based on probability and edge. Example: ProbEdge2US(55%,5%) = -110.
USRisk2Win(USOdds, RiskQuantity {default=1}) or DecRisk2Win(DecimalOdds, RiskQuantity {default=1}): Calculates resultant win quantities given US/Decimal odds and risk quantity. (These functions are also aliased as USR2W(·) and DecR2W(·), respectively). Example: USRisk2Win(-110,22) = USR2W(-110,22) = $20.
USWin2Risk(USOdds, WinQuantity{default=1}) or DecWin2Risk(DecimalOdds, WinQuantity {default=1}): Calculates required risk given US/Decimal odds and desired risk amount. (These functions are also aliased as USW2R(·) and DecW2R(·), respectively). Example: USWin2Risk(-110,20) = USW2R(-110,20) = $22.
Exch2US(US Exchange Odds, Commission {default = 2%}) or Exch2Dec(Decimal Exchange Odds, Commission {default = 2%}): Calculate sportsbook equivalent US or decimal odds given US or decimal exchange odds and commission. Example: Exch2US(-110, 1%) would refer to the sportsbook equivalent odds of betting at -110 given 1% sportsbook commission (~-111.11).
E2S(US exchange odds, exchange commission {default = 2%}): Shortcut to Exch2US(US Exchange Odds, Commission).
ExchUS2Hold(range of US Odds, Commission) or ExchDec2Hold(range of Decimal Odds, Commission): Calculates theoretical hold including sports betting exchange commissions based on an Excel range of US or decimal odds. Example: if the values of cells A1 and A2 both equal -102 ExchUS2Holds(A1:A2,2%) would equal the theoretical hold theoretical on the -102/-012 market inclusive of 2% exchange commission (a value of 1.961%).
KUtil(bankroll, Kelly multiplier {default = 1}): Calculates Kelly criterion utility for a given bankroll (expressed in percent terms) and Kelly multiplier. Example: KUtil(1.05, 0.5) would yield half-Kelly utility for a bankroll of 105% of initial.
InvKUtil(utilily, Kelly multiplier {default = 1}): The inverse Kelly Utility function. Calculates the bankroll (expressed in percent terms) implied by a given Kelly criterion utility and Kelly multiplier. Example: InvKutil(KUtil(X, KellyMult),KellyMult) would just equal X (provided X > 0).
SBKelly(Probability, Odds, Kelly Multiplier {default = 1}, Decimal Odds Flag {default = FALSE}): Calculates single bet Kelly stake given an expected win probability, paypout odds, and optional Kelly Multiplier. If the "Decimal Odds Flag" isn't set or is set to FALSE, then the function will use a "best guess" as to whether the odds specified are US or decimal-style (if absolute value < 100, it will assume decimal). Setting the flag to TRUE will cause the function to always assume decimal-style odds (this could be helpful when using decimal-style odds at very high payout levels).
{P2L(range of win probabilities)}: (array function) Returns an array of likelihoods such that the ith element of the output array (i ∈ [0, 1, 2, ..., n], where n = the number of probabilities in the input range) corresponds to to the likelihood of exactly n-i wins and i losses given the n event win probabilities in the input range. Example: if cells (A1, A2, A3) = (75%, 70%, 65%), and cells B1, B2, B3, and B4 were set to the array formula {=P2L(A1:A3)}, cell B1 would correspond to the probability of 3 wins and 0 losses (~ 34.13%), cell B the probability of 2 wins and 1 loss (~44.38%), B3 the probability of 1 win and 2 losses (~18.88%), and B4 the probability of 0 wins and 3 losses (2.63%). Note that this function may be rather slow to calculate for large input sets.
{EnumCombin(range of items, size)}: (array function) Returns a 2-D array of every possible combination of of the specified size of the input range. Example: if cells (A1, A2, A3, A4, A5) = ("A", "B", "C", "D", "E"), then {=ENUMCOMBIN(A1:A5, 2)} would return the 6-row, 2-column array of {("A","B"),("A","C"),("A","D"),("B","C") ,("B","D"),("C","D")}. Note that this function may be rather slow to calculate for large input sets. EnumComin is short for "Enumerate Combinations".
lg(p): Calculates the logit function of probability p, where lg(p) is defined as ln(p) - ln(1-p) ∀ 0 < p < 1.
invlg(x): Calculates the inverse logit function of x where invlg(x) is defined as invlg(x) = Exp(x) / (1 + Exp(x)).
MB2US(US Matchbook Exchange Odds, Commission {default=1%}) or MB2DEC(Decimal Matchbook Exchange Odds, Commission {default=1%}): Calculate sportsbook equivalent US or Decimal odds given US or Decimal Matckbook exchange odds and commission. This references a commission structure where the player pays a set percentage of the lesser of risk or win irrespective of bet outcome. Example: MB2US(-110, 1%) would refer to the sportsbook equivalent odds of betting at -110 given 1% Matchbook commission (~-112.12).
{Bets2Stats(range of Odds, range of Wager Quantities {default=1}, range of Outcomes, range of Edges {default=0%), Decimal Odds Flag = {default = FALSE})}: Array function. Takes a range of betting odds (US odds are the default, but will take decimal odds if the Decimal Odds Flag argument) is set to TRUE, an optional range of wager quantities (if not provided then 1 unit per wager is assumed), a range of outcomes (1 or a string starting with 'W' for a win, -1 or a string starting with 'L' for a loss, anything else for a push/no action), and a range of expected edges (defaults to 0). Returns an array with the following values:
Number of Non-Pushed Bets
Number of Wins
Win %
Unit Return
% Return
Unit Standard Deviation
% Standard Deviation
Standard Score
p-value (from t-distribution)




