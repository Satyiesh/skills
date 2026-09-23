# Option strategies for scheduled events (IV crush and pre-event run-up), with selection rules applied to Indian NSE options

Research notes, compiled 2026-09-23. **Method caveat:** the network proxy blocked direct fetches of orats.com, optionalpha.com, steadyoptions.com, bsic.it, medium.com, ssrn.com and rice.edu. The findings below come from search-engine summaries of those pages, not from reading the full text. Treat the numbers as indicative and check them against the primary PDF or post before using them in a model. Greeks and payoff descriptions that no source here backs are marked as inferences (standard textbook option mechanics, not verified research).

---

## 1. Short-volatility (IV crush) structures: short straddle, strangle, iron condor, iron butterfly, broken-wing butterfly, ratio spread, jade lizard

### Takeaway
All of these sell the event premium and profit when the realized move is smaller than the implied move and IV collapses. The evidence that event premium selling works is mixed, and much of it cannot be replicated independently. The sources warn about fat-tail losses and advise against naked short straddles as a reliable alpha source. For India, the defined-risk forms (iron fly, iron condor, jade lizard with a covered upside) are the practical choice. Hedged positions get large margin offsets. Naked shorts in stock options also carry physical-settlement exposure.

### Cited Findings
- ORATS tested four strategies: buy straddle, sell straddle, buy calendar, sell calendar. Entry was the day before the announcement and exit the day after (a one-day hold). The **long calendar was the best performer**. The long straddle was worst in sample and the short calendar worst out of sample. The search summary did not report the short straddle's result. — [ORATS blog: Earnings Options Strategies Backtest](https://orats.com/blog/earnings-options-strategies-backtest)
- Khan & Khan (SSRN 2024) ran a 17-year backtest of straddles around S&P 500 earnings. They concluded that "short straddles near expiration significantly raised the risk of early assignment, rendering them unviable". They advise against short straddles around earnings as a reliable way to generate alpha. The early-assignment point is a US American-style issue; NSE stock options are European. — [SSRN 4832160](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4832160); [paperswithbacktest summary](https://paperswithbacktest.com/strategies/hamzah-17-year-backtest-of-straddles-around-sp500-earnings-announcements)
- Gao, Xing & Zhang (JFQA 2018) found that ATM straddles bought 3 days before earnings and held to the announcement date earn +3.34% on average (highly significant). They conclude that **investors underestimate event uncertainty**. The implication is that, on average, the short side of the event straddle was *not* compensated in their US sample. — [Cambridge Core JFQA PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/7B34877AD5E06304BA3C55FBA3219FDD/S0022109018000285a.pdf/anticipating-uncertainty-straddles-around-earnings-announcements.pdf); [SSRN 2204549](https://doi.org/10.2139/ssrn.2204549)
- tastylive claims its iron fly backtest from 2006 onward had an 89% success rate when managed at 10% of the credit. tastylive also claims a 70% win rate and $61 average P/L on a $10-wide iron fly taking profit at 10%. An independent replication on another platform got a **55% win rate and −$8 average P/L**, which suggests tastylive's own results may be misleading. — [Option Alpha community thread "0 DTE Backtest Tasty gives completely different results"](https://optionalpha.com/community/posts/0-dte-backtest-tasty-gives-completely--202508077174) (search summary; not specifically an earnings study)
- tastylive's approach puts the probability of success for iron condors at about 67%. It recommends closing at 50% of max profit to raise the win rate. — [HaiKhuu: tastylive Iron Condor](https://haikhuu.com/education/tastytrade-iron-condor)
- Jade lizard win rates of 80–85% are claimed (practitioner source, no methodology given). The structure is a short put plus a short call spread, collected for a total credit larger than the call-spread width, so there is no upside risk. — [Theta Profits: Jade Lizard](https://www.thetaprofits.com/jade-lizard-options-strategy-explained-no-upside-risk/)
- Option Alpha paused its earnings trades after an extensive earnings backtest across tickers and sectors (podcast episode 174, "We Stopped Trading Earnings After We Saw This New Research"). The detailed findings were not available in search snippets. — [Spotify: Option Alpha Podcast #174](https://creators.spotify.com/pod/show/dudunk-alafasi/episodes/174-We-Stopped-Trading-Earnings-After-We-Saw-This-New-Research-epr9l7)
- The tastytrade "expected move" is a 1-SD (68%) range, calculated as 0.6×ATM straddle + 0.3×1st OTM strangle + 0.1×2nd OTM strangle. In practice stocks stay inside it about 70% of the time. — [tastytrade Help Center](https://support.tastytrade.com/support/s/solutions/articles/43000435415); [Volatility Box](https://volatilitybox.com/research/expected-move-options/)
- Defined-risk iron condors are easier to manage around earnings than undefined-risk straddles. They give a lower reward but a known maximum loss. — [Options Samurai: iron condor earnings](https://optionsamurai.com/blog/iron-condor-earnings/)
- Euan Sinclair's illustration: selling a straddle priced at $5 against a normal $2 looks attractive. But if the stock then moves $10, the seller loses badly even though the straddle *was* overpriced. Being right about rich implied vol does not guarantee a profit on a single event. — [Moontower: hard earned trading wisdom (Sinclair)](https://blog.moontower.ai/hard-earned-trading-wisdom/)
- SteadyOptions describes using ratio spreads to trade earnings (details not retrieved). — [SteadyOptions: Trading Earnings With Ratio Spread](https://steadyoptions.com/articles/trading-earnings-with-ratio-spread-r803/)
- **Indian margin rules:**
  - Stock F&O positions still open at expiry settle physically. On expiry day, margin on futures and ITM short options rises to 40% of contract value or SPAN+Exposure, whichever is higher, reaching 100% of delivery margin by expiry. — [Angel One](https://www.angelone.in/knowledge-center/derivatives/settlement-procedure); [Zerodha Varsity: physical settlement](https://zerodha.com/varsity/chapter/quick-note-on-physical-settlement-2/)
  - ITM spread positions in a 1:1 ratio net off for delivery. — [Angel One](https://www.angelone.in/knowledge-center/derivatives/settlement-procedure)
  - SEBI added an extra 2% ELM on short index options on expiry day. — [ICICI Direct](https://www.icicidirect.com/faqs/fno/what-other-changes-has-sebi-introduced-in-the-f-o-segment); [Business Standard](https://www.business-standard.com/amp/markets/news/sebi-announces-six-key-changes-to-curb-speculation-in-derivatives-trading-124100101316_1.html)
- A short strangle with the same short strikes as an iron condor generally earns more, but it has no protection against large moves. — [Wikipedia: Iron condor](https://en.wikipedia.org/wiki/Iron_condor)

### Inferences
- Greeks by structure (textbook mechanics):
  - **Short straddle and short strangle:** short vega, short gamma (most short at ATM), long theta. Max loss is unlimited. This is the highest margin (SPAN+exposure on naked shorts).
  - **Iron fly:** the same shape with max loss = wing width − credit. It has the best credit-to-risk ratio of the defined-risk shapes when the implied move is rich. It is the closest defined-risk proxy for the straddle.
  - **Iron condor:** lower gamma at the spot price and a wider profit zone, but a smaller credit. It suits cases where implied > historical move but the tails are fat.
  - **Broken-wing butterfly and jade lizard:** skewed to remove risk on one side. They suit Indian stocks with a directional bias or a steep put skew.
  - **Ratio spreads (1×2):** leave a naked tail. They are not risk-defined and are margin-heavy in India.
- In India, a defined-risk structure mainly helps **margin efficiency**. NSE SPAN recognises hedges, so an iron fly or condor typically needs a fraction of a naked straddle's margin (the exact ratio was not retrieved and is a gap).
- Event crush on NSE stocks is often harvested in the **current monthly series**. If the result lands near expiry week, physical-settlement margin escalation and the loss of calendar-spread margin benefit on expiry day argue for exiting before expiry-day T-1.
- The US academic evidence (Gao–Xing–Zhang long-straddle premium; Khan & Khan) leans *against* systematic event premium selling. The practitioner support for selling (tastylive) has replication problems. An Indian engine should therefore **filter** events rather than sell every event: sell only when the implied/historical move ratio is high (see section 5).
- Early-assignment risk (Khan & Khan) does not apply to NSE European options. That removes one of their main objections to short straddles, but not the tail-risk objection.

### Gaps
- The full ORATS table was not retrieved: its sell-straddle numbers, and the filters (implied vs historical move, IV ratio) that raised Sharpe.
- No tastylive earnings-specific study (e.g., "strangle vs iron condor through earnings") could be verified.
- No Sensibull, Opstra or Stockmock backtest of short straddles through Indian quarterly results was found.
- No quantified margin comparison for NSE (naked straddle vs iron fly) was found. It is easy to compute with the NSE SPAN file or a broker margin calculator.

---

## 2. Term-structure structures: calendars, double calendars, diagonals across the event

### Takeaway
A long calendar (sell the event-containing expiry, buy the next) isolates the front-month IV crush with much lower net gamma. It was ORATS's best-performing one-day earnings strategy. SteadyOptions reports that calendars opened a week or so ahead also profit from the *pre-event* front-IV rise, and often exits them before the event. In India, stock options are monthly only, so the "back leg" is next month (about 30 days further out). SEBI's removal of the calendar-spread margin benefit on expiry day makes a front leg that expires on or just after the event costly to hold.

### Cited Findings
- ORATS results for the long calendar (one-day hold across earnings, entry the day before, exit the day after):
  - In sample: **+0.90% average return on 205 trades** (3.9% of possible announcements, i.e., heavily filtered). Largest loss −10.3%, largest gain +6.1%.
  - Out of sample: **+0.91% on 54 trades**.
  - The short calendar was the worst performer out of sample. — [ORATS blog](https://orats.com/blog/earnings-options-strategies-backtest)
- ORATS also backtests calendar spreads selected on **IV contango** (term-structure slope). Calendars profit when near-term IV is high relative to longer-term IV. ORATS forecasts the IV with and without earnings, and the earnings move from 12 quarters of history, to judge whether the front premium will collapse. Example given: a 6% priced move against a 4.5% historical forecast argues for selling. — [ORATS: Backtesting Calendar Spreads Based on IV Contango](https://orats.com/blog/backtesting-calendar-spreads-based-on-iv-contango); [ORATS: HV forecasts](https://orats.com/blog/how-to-use-hv-forecasts)
- The ORATS Earnings Move Report gives implied move, historical average move, IV with earnings and with earnings removed ("ex-earnings IV"), and HV with and without earnings days. — [ORATS blog](https://orats.com/blog/earnings-options-strategies-backtest); [ORATS University: volatility around earnings](https://orats.com/university/volatility-around-earnings)
- SteadyOptions uses **pre-earnings calendars**: the short option expires a few days after earnings, and the position is **closed before the announcement**.
  - The front IV rises sharply in the days before earnings, offsetting negative theta and widening the calendar.
  - For some stocks the front IV rise cannot keep up with theta.
  - Targets: 20–30% profit, with a mental stop of 15–20%.
  - The rationale for holding through earnings instead is that the front IV collapses much more than the back. — [SteadyOptions: Why We Sell Our Calendars Before Earnings](https://steadyoptions.com/articles/why-we-sell-our-calendars-before-earnings-r149/); [SteadyOptions: Calendar Spread Guide](https://steadyoptions.com/articles/calendar-spread/)
- Short-dated equity IV curves often become **concave** before earnings. This reflects a bimodal risk-neutral distribution, which matters for choosing calendar and fly strikes. — [Review of Finance: Pricing event risk, concave IV curves](https://academic.oup.com/rof/article/29/4/963/8079062)
- **NSE rules:**
  - SEBI removes the calendar-spread margin benefit on the expiry day of the near leg; both legs are margined independently at full rates. (One broker says the removal starts at 4 PM the day before expiry.) — [ICICI Direct: calendar spreads after SEBI rules](https://www.icicidirect.com/futures-and-options/articles/calendar-spreads-in-f-o-after-sebi-s-new-rules-what-you-need-to-know); [Jainam](https://www.jainam.in/blog/sebi-new-rules-for-fo-trading/)
  - All NSE derivative expiries moved to **Tuesday** from September 2025. — [Angel One / search summary](https://www.angelone.in/knowledge-center/derivatives/settlement-procedure)
  - The weekly-expiry curbs apply only to index F&O. Stock options were never weekly on NSE; they are monthly. — [NiftyDesk](https://niftydesk.app/blog/sebi-new-fno-rules-2026-guide); [Zerodha Z-Connect](https://zerodha.com/z-connect/business-updates/sebis-new-rules-for-index-derivatives-heres-whats-changing)

### Inferences
- **Greeks of a long calendar (same strike):** long vega net, but *short* front-month vega, which is the leg that gets crushed. There is a small short gamma near the strike, and theta is positive. Max loss is roughly the debit, though it can exceed the debit if the back-month IV also collapses or the spot gaps far from the strike. It is capital-light.
- A **double calendar** (put calendar below and call calendar above spot, or at ±implied move) widens the profit zone for events with a bimodal distribution.
- A **diagonal** (buy a further-OTM back month) adds directional tilt.
- **India mapping:** if the result date falls in the current month, sell current-month ATM and buy next-month ATM.
  - The calendar works best when the result is **well before** current expiry, so the short leg still has time value and the expiry-day loss of margin benefit is avoided.
  - If the result falls after current expiry, the "event expiry" is next month. The calendar is then next-month vs far-month. Far-month stock options are often illiquid, so a liquidity filter is essential.
- The ~30-day gap between NSE monthly legs is larger than the US weekly-to-weekly gap. This lowers the vega mismatch efficiency: the back leg also loses IV after the event, because monthly IVs include the event. The US calendar edge may therefore **transfer only partially**.
- **Run-up calendar (SteadyOptions-style)** in India: enter about 5–10 trading days before the result, short current-month and long next-month, and exit the day before the result. It profits from front-IV expansion with low gap risk, and it avoids crush exposure altogether.

### Gaps
- No Indian backtest of stock-option calendars across quarterly results was found.
- ORATS's IV-contango threshold values (e.g., front/back IV ratio > X) were not retrieved.

---

## 3. Run-up (long vol) structures: buy straddles, strangles or calendars 5–20 days before and exit before the announcement

### Takeaway
The evidence is mixed. Gao–Xing–Zhang find short-window pre-announcement straddles (3–5 days) profitable in the US. Khan & Khan find that long straddles opened 30 days before lose value to theta up to T-1. Option Alpha's 20-days-before straddle was profitable only because of about 10 outlier trades out of 1,205. The IV run-up tends to cover theta only over short windows and only for names with a strong historical run-up.

### Cited Findings
- Gao, Xing & Zhang (JFQA 2018):
  - ATM straddles bought **3 days before** earnings and held to the announcement date earned **+3.34%** (highly significant). They also tested entries 5 and 1 trading days before, and exits on the announcement day or the day after.
  - Returns are larger for small firms, high-volatility and high-kurtosis firms, firms with volatile past earnings surprises, and firms with low volume or high transaction costs. That last point means part of the edge may be eaten by spreads. — [ideas.repec JFQA](https://ideas.repec.org/a/cup/jfinqa/v53y2018i06p2587-2617_00.html); [paperswithbacktest](https://paperswithbacktest.com/strategies/anticipating-uncertainty-straddles-around-earnings-announcements)
  - Caveat: "held to the announcement date" may include the announcement reaction, so this is not purely a run-up trade.
- Khan & Khan (17 years, S&P 500):
  - Long ATM straddles opened **30 trading days before** earnings *declined in value* up to one day before the event, because theta outweighed the IV rise.
  - Buying the straddle one day before and selling one day after gave a **108% CAGR, Sharpe 2.2, on 13,120 trades**. However, single-week losses reached **83.8%**, and commissions, slippage and taxes were not modelled. — [paperswithbacktest summary](https://paperswithbacktest.com/strategies/hamzah-17-year-backtest-of-straddles-around-sp500-earnings-announcements); [SSRN 4832160](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4832160)
  - This conflicts with ORATS, where the one-day long straddle across earnings was the *worst* in-sample strategy. The difference probably comes from the universe, period, pricing (mid vs bid/ask) and filters.
- Option Alpha backtest:
  - The best variant was a 50-delta long straddle opened **20 days before** earnings using about 20-DTE options and exited at or just after earnings. It made total profits of $95k, average win $616, average loss $294, and a 41% win rate.
  - **Removing the top 10 of 1,205 trades made it unprofitable.**
  - Win rates showed "no meaningful difference" between exiting before earnings and exiting the day of or after. — [Option Alpha podcast: Long Straddle Earnings Backtest](https://optionalpha.com/podcast/long-straddle-earnings-option-strategy)
- SteadyOptions trades pre-earnings straddles and closes them before the announcement. The logic is that the pre-event IV increase offsets theta, while options tend to overprice the event move and are crushed the day after. — [SteadyOptions: Why We Sell Our Straddles Before Earnings](https://steadyoptions.com/articles/why-we-sell-our-straddles-before-earnings-r148/); [SteadyOptions: Best strategies for trading earnings](https://steadyoptions.com/articles/ep-options-strategies-for-trading-earnings/)
- There is also a published analysis on the edge of pre-earnings vs post-earnings trades (not retrieved). — [Barchart](https://www.barchart.com/story/news/31395102/trading-pre-earnings-vs-post-earnings-when-options-traders-have-an-edge)
- **India:** a common retail mistake is buying calls right before quarterly results, then losing to the IV collapse even when the stock rises. — [Market Insights India](https://www.marketinsightsindia.in/option-analytics-guide-for-indian-derivative-traders/)

### Inferences
- **Run-up straddle Greeks:** long vega (the profit engine), long gamma (a bonus from pre-event drift), short theta (the cost). It is profitable only if Δ(front IV) × vega > cumulative theta + slippage.
- The run-up is steepest in the last 3–7 days. That suggests entries around **T-7 to T-3**, not T-20, and exit at the T-1 close.
- In India, stock options are monthly. If the result is late in the month, the event expiry is also close to expiry, so theta is large and gamma is high: the run-up straddle is expensive. If the result is early in the series (about 20+ DTE), theta is mild, which favours a run-up long straddle or strangle in the current month.
- A **long calendar held to T-1** (short current month, long next month) collects the front IV run-up. It works as a lower-theta way to express the run-up.
- A **reverse calendar** (buy front, sell back) is long front vega and short back vega. It profits if the front IV rises faster than the back. It is rarely liquid enough in Indian stock options.
- Because the edge is concentrated in outliers (Option Alpha), run-up strategies need **many small bets across events**, not concentration.

### Gaps
- No study of the size of the Indian stock-option IV run-up before results (e.g., median front-IV rise from T-10 to T-1) was found. This is a core parameter to estimate from NSE bhavcopy/IV history.
- No Stockmock or Sensibull backtest of the run-up was found.

---

## 4. Directional and skew plays around events

### Takeaway
Use debit spreads or risk reversals only when there is directional conviction. A debit vertical largely neutralizes vega (long one option, short another), so it is less exposed to the crush than a naked long option. Broken-wing flies and jade lizards are ways to express a skewed view while keeping the short-vol carry.

### Cited Findings
- Stocks with a higher put-minus-call IV spread before earnings earn significantly **negative** abnormal returns over the two-day announcement window, and stocks with a lower spread earn positive returns. Skew is therefore a directional signal. — [Journal of Banking & Finance: Volatility spreads and earnings announcement returns](https://www.sciencedirect.com/science/article/abs/pii/S0378426613004081)
- A jade lizard has no upside risk when the credit exceeds the call-spread width. — [Theta Profits](https://www.thetaprofits.com/jade-lizard-options-strategy-explained-no-upside-risk/); [QuantInsti: Jade Lizard in Python](https://blog.quantinsti.com/jade-lizard-options-trading-strategy-python/)
- One example of a contrarian defined-risk trade: a bull put spread opened after an earnings dip to exploit elevated IV. — [TradingView idea (GS)](https://in.tradingview.com/chart/GS/odnOqXU3-Bull-Put-Spread-su-GS)

### Inferences
- **Debit call or put spread:** near-zero net vega, limited gamma, max loss = debit. It is suitable in India because it is hedged and gets a margin offset, although the long leg must be paid in full.
- **Risk reversal** (long OTM call and short OTM put, or the reverse): this monetises steep skew, but the short leg is naked. In India that means high margin and physical-settlement risk on stock options.
- A skew-based directional filter (the put–call IV spread) could decide whether an iron condor is tilted into a broken-wing butterfly or jade lizard.

### Gaps
- No evidence was found that the put–call IV spread predicts announcement returns in India.

---

## 5. Selection rules and risk management

### Takeaway
Practitioners and vendors (ORATS, SteadyOptions, tastylive, Sinclair) screen on a small set of measures:
- **implied vs historical move ratio**
- **ex-earnings IV vs event IV** (the event premium)
- **term-structure slope** (front/back IV)
- IV rank or percentile
- **liquidity**

They then size small per event and spread risk across many events, because the P&L distributions are fat-tailed and outlier-driven.

### Cited Findings
- **Implied vs historical move:** ORATS uses 12 quarters of historical earnings moves. If the implied move (e.g., 6%) is well above the forecast (e.g., 4.5%), sell premium. — [ORATS HV forecasts](https://orats.com/blog/how-to-use-hv-forecasts)
- The implied earnings move comes from the ATM straddle of the first expiry after the event. — [SpotGamma implied earnings moves](https://spotgamma.com/free-tools/implied-earnings-moves/)
- Market Chameleon and Barchart publish implied-vs-historical earnings move comparisons, showing how often a stock's actual move landed inside or outside the priced move. — [Trader Central guide](https://traderc.com/how-to-find-expected-move-before-earnings/); [Market Chameleon Earnings Strategy Screener](https://marketchameleon.com/EarningsReport/EarningsOptionStrategyScreener)
- **Heavy filtering:** ORATS's profitable calendar used only 3.9% of possible announcements (205 trades). — [ORATS](https://orats.com/blog/earnings-options-strategies-backtest)
- **Cross-sectional predictors of long-straddle profitability:** small size, high volatility and kurtosis, volatile past surprises, and illiquidity (Gao–Xing–Zhang). The sell-side mirror: avoid shorting these names. — [ideas.repec](https://ideas.repec.org/a/cup/jfinqa/v53y2018i06p2587-2617_00.html)
- **Position sizing:**
  - Option Alpha's TLT iron condor backtest went from **−67% to +6.86%** return (max drawdown about 45%) only by cutting position size. Over-allocation was the main cause of the loss. — [Option Alpha podcast: Position Sizing Impact](https://optionalpha.com/podcast/iron-condor-backtest)
  - Khan & Khan urge conservative sizing given single-week losses up to 83.8%. — [paperswithbacktest](https://paperswithbacktest.com/strategies/hamzah-17-year-backtest-of-straddles-around-sp500-earnings-announcements)
- **Management rules:** tastylive closes iron condors at 50% of max profit ([HaiKhuu](https://haikhuu.com/education/tastytrade-iron-condor)). SteadyOptions targets 20–30% profit with a 15–20% stop on calendars ([SteadyOptions](https://steadyoptions.com/articles/why-we-sell-our-calendars-before-earnings-r149/)).
- **Indian tools:** Sensibull and Opstra provide IV Rank/IV Percentile, and Opstra adds historical IV and backtesting. — [HDFC Sky / Sensibull summary](https://web.sensibull.com/live-options-charts?tradingsymbol=NIFTY); [Market Insights India](https://www.marketinsightsindia.in/option-analytics-guide-for-indian-derivative-traders/)

### Inferences
Suggested decision rules for the NSE engine. These are a synthesis, not a published rule-set, and every threshold needs calibration on NSE data.
1. Implied move / median historical result-day move (last 8–12 quarters):
   - ratio **> 1.2–1.3**: short-vol candidate (iron fly or iron condor, or a calendar if the term structure is inverted);
   - ratio **< 0.8**: long-vol candidate (run-up straddle, or hold-through long straddle for high-kurtosis names);
   - in between: no trade.
2. **Front/back IV ratio > ~1.1–1.2:** prefer a calendar, which isolates the event premium, over a straddle.
3. **Liquidity gate:** tight ATM bid-ask as a % of the straddle price, and open interest in both months. This is vital because many NSE stock option chains are thin beyond the ATM ±2 strikes and in the next month.
4. **Sizing:** max loss per event ≤ 0.5–2% of capital, using defined-risk structures so max loss is known. Use fractional Kelly (≤ ¼) at most, because edge estimates are noisy and outlier-driven.
5. **Diversification:** spread risk across many results per season, and cap sector concentration, since results cluster by sector.
6. **After the event:** close short-vol trades at the first liquid prices after the crush (the ORATS one-day hold). Do not carry positions into the expiry-day margin escalation or physical settlement. Delta-hedging leftover gamma with futures is optional.

### Gaps
- No published Kelly-fraction guidance specific to event option trades was found.
- tastylive's specific IVR thresholds for earnings trades were not verified.

---

## 6. Macro-event variants for index options (Nifty, BankNifty: RBI MPC, Budget, elections, CPI, FOMC)

### Takeaway
India VIX reliably rises into big scheduled events and collapses after them. It dropped about 30–34% on general-election result days in 2014 and 2019. Practitioners use short straddles or iron condors to capture the crush, long straddles for the highest-uncertainty events, or simply avoid buying options before the event. Since November 2024, only one weekly index expiry per exchange remains (Nifty on NSE), and BankNifty is monthly only. Index contract sizes are now ₹15–20 lakh, and there is a 2% extra ELM on short options on expiry day.

### Cited Findings
- India VIX fell almost **34% (2014)** and **30% (2019)** on general-election result days. In 2024 it rose **191%** from a 52-week low of 8.4 to above 24 during the Lok Sabha polls. — [Business Standard, 2024-05-28](https://www.business-standard.com/amp/markets/news/lok-sabha-elections-2024-why-is-india-vix-up-5-on-tuesday-may-28-124052800677_1.html); [Business Standard: VIX steepest slump](https://www.business-standard.com/amp/markets/news/india-vix-index-sharply-slumps-20-the-biggest-drop-in-five-years-124042301001_1.html)
- India VIX rose 6% to 21.95 the day before the 2022 Union Budget. The Sensex historically swings about 3% on Budget day. — [Business Standard, 2022-01-31](https://www.business-standard.com/amp/article/markets/india-vix-soars-6-to-21-95-a-day-ahead-of-union-budget-122013101779_1.html)
- India VIX hit a 4-year high ahead of the 2019 poll results. — [Business Standard 2019](https://www.business-standard.com/article/markets/markets-live-sensex-nifty-lok-sabha-2019-elections-modi-nda-oil-rupee-119052200132_1.html)
- For index options, RBI policy is "less about direction and more about repricing of volatility". Strategies cited: a long straddle, short straddles or iron condors before the event to capture the crush, and buying options only after IV normalises. — [HDFC Sky: RBI policy day options](https://hdfcsky.com/sky-learn/trading-strategies/how-to-use-options-for-rbi-policy-and-other-event-days)
- One retail-broker claim: before RBI policy, VIX "jumps 5–8 points" and premiums rise 15–30%, then crash after the event. This looks exaggerated or unverified; treat it with caution. — [Sahi blog](https://www.sahi.com/blogs/why-your-option-premium-drops-even)
- **SEBI index rule changes:** one weekly expiry per exchange (NSE: Nifty) from 20 November 2024, index contract value raised to ₹15–20 lakh, 2% ELM on short index options on expiry day, and removal of the expiry-day calendar-spread benefit. — [Business Standard](https://www.business-standard.com/amp/markets/news/sebi-announces-six-key-changes-to-curb-speculation-in-derivatives-trading-124100101316_1.html); [Zerodha Z-Connect](https://zerodha.com/z-connect/business-updates/sebis-new-rules-for-index-derivatives-heres-whats-changing); [ICICI Direct](https://www.icicidirect.com/futures-and-options/articles/calendar-spreads-in-f-o-after-sebi-s-new-rules-what-you-need-to-know)

### Inferences
- **RBI MPC, CPI and US FOMC:** index realized moves are usually small relative to the event premium. The typical trade is a short Nifty weekly iron fly or condor entered the day before or the morning of the event, and exited after the announcement or at the next open.
  - For FOMC, the announcement comes during Indian night hours. The risk is therefore an **overnight gap at the next open**, with no chance to adjust. Defined risk is mandatory.
- **Budget and election results:** these are high-kurtosis events (the 2024 result day saw a very large intraday Nifty fall and VIX spike). The premium can be *under*priced, so avoid naked short vol. Use either:
  - wide iron condors sized small, or
  - calendars (short the event weekly, long the next weekly or monthly), which capture the VIX collapse while limiting gap exposure;
  - or run-up long straddles exited before results.
- BankNifty is now monthly only, so BankNifty event trades use the monthly series. That means higher vega per unit of event and weaker crush capture than the old weeklies.
- The India VIX regime (about 10–14 in calm periods) affects edge: with low baseline IV, the event premium is small in absolute terms, so a vega-light, defined-risk structure is needed to cover costs.

### Gaps
- No systematic Indian study was found of Nifty or BankNifty straddle returns around RBI MPC, CPI or FOMC. The HDFC Sky and Sahi pieces are educational, not backtests.
- No Stockmock, Sensibull or Opstra event backtest was retrievable.
- US evidence is mostly single-stock earnings; transfer to Indian index macro events is unverified.
