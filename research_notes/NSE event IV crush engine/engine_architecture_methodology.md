# Options Event-Study & Backtesting Engine: Methodology and Architecture (NSE F&O focus)

Research notes as of 2026-09-23. Research method note: the egress proxy blocked several primary sources (nseindia.com, nsearchives.nseindia.com, arxiv.org, business.columbia.edu, stern.nyu.edu, orats.com). Where a primary PDF could not be read, findings rely on search-result abstracts and secondary pages, and this is flagged. Standard textbook derivations (Black-76, forward variance, straddle approximation) are placed under **Inferences**, labelled as standard derivations, because no source could be fetched to cite them directly.

---

## 1. Data model: point-in-time chains, corporate actions, event calendar, survivorship

### Takeaway
The core data model is a point-in-time (PIT), bitemporal store: option quotes/bhavcopy keyed by (trade_date, snapshot_ts, symbol, expiry, strike, option_type), plus a contract-master table with lot size and strike as they were on that date. Add a corporate-action adjustment ledger that follows NSE's own rules (strike and lot adjusted on the last cum-date, and only for dividends at or above 2% of market value), an event calendar with announcement timestamps, and a dated F&O-eligibility universe table so that survivorship bias is avoided.

### Cited Findings
- NSE F&O corporate-action rules: dividends **below 2% of the underlying's market value are "ordinary"** and do not adjust the strike. Extraordinary dividends (≥2%) adjust the strike price. — [m.Stock summary of NSE rules](https://www.mstock.com/articles/corporate-actions-fo-contracts); canonical pages: [NSE Adjustments in case of Corporate Actions](https://www.nseindia.com/static/products-services/equity-derivatives-corporate-actions-adjustments), [NSE Clearing Corporate Actions Adjustment](https://www.nseclearing.in/clearing-settlement/equity-derivatives/corporate-actions-adjustment) (not fetchable here, so this detail is secondary).
- Bonus/split: the lot size rises in proportion and the strike falls in proportion, so contract value is unchanged. For example, a 1:1 bonus doubles the lot and halves the strike. — [m.Stock](https://www.mstock.com/articles/corporate-actions-fo-contracts); [Zerodha support](https://support.zerodha.com/category/trading-and-markets/trading-faqs/f-otrading/articles/adjustment-f-o-contracts)
- NSE fraction-rounding procedure: (1) value the position before adjustment, (2) value it with the exact adjustment factor, (3) round the strike and market lot, (4) revalue. The exchange handles any residual so that no forced closure is needed. — [NSE (www1) corporate adjustment page via search snippet](https://www1.nseindia.com/products/content/derivatives/equities/corporate_adjustment.htm)
- Timing: adjustments are made **on the last day the security trades cum-basis, after close**. — same NSE page (search snippet)
- The NSE F&O stock list changes over time (entry and exit under SEBI eligibility criteria). SEBI's late-2024 F&O measures also changed contract sizes to Rs 15–20 lakh for index derivatives, which changed lot sizes across history. — [ICICI Direct FAQ](https://www.icicidirect.com/faqs/fno/what-other-changes-has-sebi-introduced-in-the-f-o-segment); [Zerodha Z-Connect](https://zerodha.com/z-connect/business-updates/sebis-new-rules-for-index-derivatives-heres-whats-changing)
- Expiry-day schedule changes: from 1 Sep 2025 (per ICICI, "effective from 29th August 2025"), the Nifty weekly expiry moved to **Tuesday**. From 20 Nov 2024, each exchange may offer weekly expiries on only one benchmark index. — [Jainam](https://www.jainam.in/blog/sebi-new-rules-for-fo-trading/); [ICICI revised expiry FAQ](https://www.icicidirect.com/faqs/fno/what-is-revised-expiry-schedule-for-nse-contracts)

### Inferences
- **Schema sketch (Parquet/Arrow, partitioned by trade_date/underlying):**
  - `contract_master(pit)`: token, underlying, expiry, strike_raw, strike_adj_factor, lot_size, option_type, valid_from, valid_to. Strikes and lots must be versioned, because the same contract changes strike and lot after a bonus or split.
  - `option_quotes`: ts, token, bid, ask, bid_qty, ask_qty, ltp, volume, OI, and a source flag (EOD bhavcopy vs intraday snapshot). EOD bhavcopy has only OHLC, settle, OI and volume, with **no bid/ask**, so spread-based fill models need intraday or order-book snapshots, or a modelled spread.
  - `underlying_spot`, `futures` (same-expiry futures price, needed for Black-76), `rates` (MIBOR/T-bill curve).
  - `corporate_actions`: ex_date, type, ratio, dividend amount, adjustment factor, and whether NSE adjusted it (≥2% rule).
  - `events`: symbol, event_type (results, AGM, policy, budget), announce_ts, session_flag {pre-market, intraday, post-market, unknown}, fiscal_period, source, first_seen_ts (the time the calendar entry became known, which blocks look-ahead on unscheduled or rescheduled dates).
  - `fo_universe`: symbol, in_fo_from, in_fo_to, plus the reason for exit.
- **Event day-0 mapping rule:** if an announcement is after-market (≥15:30 IST), the first reaction session is T+1. If it is pre-market or intraday, the reaction session is T. Indian companies often release results during market hours or late evening, so a timestamp-level field is required, not just a date. Using the wrong session misaligns the "T-1 close" pre-event snapshot and contaminates IV-crush statistics.
- Back-adjust history with the NSE factor on a **separate adjusted view**. Keep the raw table immutable so that P&L is computed on the contracts actually traded.

### Gaps
- Could not fetch NSE's primary corporate-action page or the SEBI F&O eligibility circular text. Exact current stock-entry and exit criteria (for example, the MWPL/ADTV thresholds revised in 2024–25) are unverified here.
- No verified free source was found for timestamped Indian earnings-announcement calendars. NSE corporate-announcement filings carry timestamps (general knowledge, not verified here).

---

## 2. IV computation and surface construction

### Takeaway
For NSE single-stock and index options (European, cash-settled index, physically settled stocks), price with **Black-76 on the same-expiry futures**, or on a put-call-parity implied forward. This avoids estimating dividends and repo. Invert with Jäckel's "Let's Be Rational" (vectorized via py_vollib_vectorized). Fit per-expiry SVI, or SSVI across expiries, to get an arbitrage-free surface. Interpolate ATM total variance in time to constant maturities. This mirrors India VIX, which uses the futures price as the forward and cubic splines to fill bad quotes.

### Cited Findings
- India VIX uses best bid/ask of **near- and next-month NIFTY options**, following CBOE methodology "with suitable amendments... using cubic splines". It measures expected volatility over the next 30 calendar days. — [ICICI Direct FAQ](https://www.icicidirect.com/faqs/fno/how-is-india-vix-computed); [NSE India VIX page](https://www.nseindia.com/static/products-services/indices-indiavix-index); [NSE white paper (not fetchable)](https://nsearchives.nseindia.com/web/sites/default/files/inline-files/white_paper_IndiaVIX.pdf)
- India VIX takes **the latest traded price of the NIFTY futures of the respective expiry as the forward**. The ATM strike K0 is the strike just below the forward. Missing or inappropriate quotes are interpolated with a **natural cubic spline** on the mid quotes of other strikes. — [search summary of NSE/ICICI/Bajaj sources](https://www.icicidirect.com/faqs/fno/how-is-india-vix-computed)
- py_vollib_vectorized implements a vectorized version of **Jäckel (2015) "Let's Be Rational"** for Black, Black-Scholes and Black-Scholes-Merton. It supports numpy and pandas and depends on numba and py_lets_be_rational. — [py_vollib_vectorized GitHub](https://github.com/marcdemers/py_vollib_vectorized); [docs](https://py-vollib-vectorized.readthedocs.io/en/latest/pkg_ref/iv.html)
- A 2026 arXiv paper, "Fast-Vollib", presents a newer IV library with PyTorch, JAX and CUDA fused-kernel backends. This suggests the older vollib stack is being superseded for GPU and large-batch work (abstract only, not fetched). — [ResearchGate](https://www.researchgate.net/publication/404333035_Fast-Vollib_A_Fast_Implied_Volatility_Library_for_Pythonwith_PyTorch_JAX_and_CUDA_Fused-Kernel_Backends); [arXiv 2604.27210](https://arxiv.org/html/2604.27210v1)
- SSVI (Gatheral & Jacquier, *Quantitative Finance* 14(1), 2014, 59–71) gives an explicit whole-surface parameterization with conditions that exclude calendar and butterfly arbitrage. It is parameterized by the ATM total variance curve θ_t, a constant correlation ρ and a curvature function φ(θ). Raw SVI slices by themselves have no known general no-arbitrage conditions. — [Gatheral & Jacquier preprint (Imperial)](https://www.imperial.ac.uk/media/imperial-college/research-centres-and-groups/stochastic-analysis-group/preprints-2012/12-11.pdf); [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2033323); [Baruch slides](https://mfe.baruch.cuny.edu/wp-content/uploads/2013/01/OsakaSVI2012.pdf)
- Reference code: Jacquier's SSVI repo (SSVI plus the corresponding local vol) — [GitHub JackJacquier/SSVI](https://github.com/JackJacquier/SSVI). Robust SSVI slice calibration and arbitrage-free interpolation: [Hendriks & Martini / arXiv 1804.04924](https://arxiv.org/pdf/1804.04924). Generalised SSVI: [arXiv 1210.7111](https://arxiv.org/pdf/1210.7111)
- Tighter uniform bounds for Black-Scholes IV can improve root-finder initial guesses. — [arXiv 2302.08758](https://arxiv.org/pdf/2302.08758)
- QuantConnect LEAN offers both a daily precomputed Greeks/IV dataset (as of the prior close) and on-the-fly indicator-based IV/Greeks. It computes them only on request, for cost reasons. — [QuantConnect docs](https://www.quantconnect.com/docs/v2/writing-algorithms/securities/asset-classes/equity-options/greeks-and-implied-volatility/key-concepts)

### Inferences (standard derivations, not fetched from a source)
- **Black-76:** C = D·[F·N(d1) − K·N(d2)], with d1 = [ln(F/K) + σ²T/2]/(σ√T) and D = e^{−rT}. Using F = same-expiry futures removes the need for dividend and repo inputs. For stock options, the futures and options on NSE share expiry dates (monthly), so this is natural.
- **Implied forward from parity:** C − P = D·(F − K). Regress (C−P) on K across near-ATM strikes, using mids with a tight-spread filter, to get D and F jointly. Alternatively, use the r curve and solve for F at the strike that minimises |C−P|, as CBOE/VIX do. Compare F_implied with F_futures: the gap flags stale quotes, or an implied dividend or borrow component.
- **Solver:** Let's Be Rational reaches machine precision in about 2 iterations and is robust deep OTM. Newton-Raphson on vega fails near zero vega, and Brent is a slower fallback. Treat prices below intrinsic, or above the forward bound, as NaN and not as zero vol.
- **Quote hygiene before fitting:** drop quotes with zero bid, spread/mid above a threshold (for example 30–50%), stale LTP (time since last trade), and OI/volume below a threshold. Use OTM options only (puts for K<F, calls for K>F). Weight the fit by 1/spread or by vega.
- **Constant-maturity ATM IV:** interpolate **total variance w = σ²T linearly in T**, not σ, between the bracketing expiries at the ATM-forward strike (log-moneyness 0). For event studies, **exclude or adjust the event-containing expiry** (see §3), otherwise CM-IV jumps mechanically when the event rolls out of the window. Consider business-day or trading-minute time (India VIX uses a CBOE-style minute count, per the CBOE lineage) and holiday calendars from NSE.
- **Illiquid single-stock chains:** many NSE stock options have only 3–8 liquid strikes near the money. SSVI with a shared ρ and φ, or a quadratic/SVI-JW fit in delta space, is more stable than a per-slice 5-parameter raw SVI.

### Gaps
- Could not read the India VIX white paper directly, so exact details (rate used, minute-count convention, strike cutoff rule) are unverified.
- The current maintenance status of py_vollib, py_lets_be_rational and py_vollib_vectorized (last release dates) was not verified. The fast-vollib abstract implies these older libraries are dated. Treat them as "stable, low activity" and verify on PyPI.

---

## 3. Event-volatility metrics

### Takeaway
Measure the event with: (a) the straddle-implied move, (b) the Dubinsky-Johannes term-structure decomposition of total variance into diffusive plus event-jump variance, (c) run-up = CM or ex-event IV change from T−N to T−1, (d) crush = the change in the front expiry's ATM IV from T−1 close to the first post-event close, (e) realized/implied ratio = |post-event return| ÷ implied move, and (f) contextual ranks (IV rank or percentile, skew, and term slope).

### Cited Findings
- Dubinsky & Johannes developed no-arbitrage option pricing with scheduled earnings jumps, plus estimators of "earnings jump volatility". They find that earnings uncertainty is central to option prices, and they document IV **rising into announcements and dropping sharply afterward**. — [Dubinsky & Johannes, SSRN](https://papers.ssrn.com/sol3/Delivery.cfm/SSRN_ID760564_code248412.pdf?abstractid=600593&mirid=1&type=2); [Columbia PDF (blocked)](https://business.columbia.edu/sites/default/files-efs/pubfiles/6051/DJ_2006.pdf); [VU "Option Pricing of Earnings Announcement Risks"](https://research.vu.nl/ws/portalfiles/portal/108247883/Option_Pricing_of_Earnings_Announcement_Risks.pdf)
- An anticipated jump produces a large increase in short-dated ATM IV and a **downward-sloping (inverted) term structure** before the announcement. IV immediately before a scheduled event consists of two components, diffusive and event. — search summaries of the same sources, plus [ORATS University](https://orats.com/university/volatility-around-earnings) (blocked)
- Related literature: concave IV smiles as a signature of event (bimodal) risk. — [Alexiou-Goyal-Kostakis-Rompolis, "Pricing Event Risk: Evidence from Concave Implied Volatility Curves"](https://fmai.memberclicks.net/assets/docs/Derivatives2022/Concave_AGKR.pdf). Non-spanning identification of scheduled event risk (2026). — [arXiv 2606.12872](https://arxiv.org/pdf/2606.12872). Option-implied event-study settings are also used for elections, macro announcements and M&A. — [search summary](https://tippie.uiowa.edu/sites/tippie.uiowa.edu/files/2023-05/Do%20Shareholder%20Meetings%20Matter_2023%20holland-2.pdf)

### Inferences (standard formulas, to be verified against the DJ paper during the spec)
- **Term-structure event variance (DJ style):** assume constant diffusive vol σ_d across the two expiries T1 < T2, both after the event. Then σ_i²·T_i = σ_d²·T_i + σ_J², which gives
  **σ_J² = T1·T2·(σ1² − σ2²)/(T2 − T1)** (checked algebraically: subtract the two equations to get σ_d², then substitute back) (the T's are year fractions and σ_J is the one-day event move stdev). Implied event move ≈ σ_J (as a %). Ex-event diffusive vol: σ_d² = (σ2²T2 − σ1²T1)/(T2 − T1). If σ1 < σ2 (no inversion), clip σ_J² at 0 and flag the observation.
- **Straddle implied move:** E|ΔS|/S ≈ Straddle_ATM / F (a raw, "market-maker" convention). Under normality E|X| = σ√(2/π), so Straddle ≈ 0.8·σ·√T·F. Report both the raw straddle/F and the variance-based σ_J. Strip non-event time value: implied event move ≈ (straddle − diffusive straddle)/F, using σ_d from the next expiry.
- **Run-up:** ΔIV_runup = IV_front,ATM(T−1 close) − IV_front,ATM(T−N), with N ∈ {5, 10, 20} trading days. Also track the pure event-variance share σ_J²/(σ1²T1).
- **Crush:** ΔIV_crush = IV_front(T+1 close, or first post-event session) − IV_front(T−1 close). Compute it on a **fixed-strike and a fixed-delta/ATM-forward basis**, because the ATM strike moves after the jump. Normalise it as crush/(pre-event IV) and compare it with the model-predicted crush of √(σ1² − σ_J²/T1).
- **Realized/implied ratio:** R = |ln(S_post/S_pre)| ÷ implied move, where S_pre is the T−1 close (or the last pre-announcement price for intraday events) and S_post is the first post-event close. Choose between open and close consistently. R < 1 means the event premium was overpriced. This is the main ML target (§8).
- **Context metrics:** IV rank = (IV − min_252)/(max_252 − min_252); IV percentile = % of days in 252 with IV below today. Use **ex-event (diffusive) IV** for rank, otherwise every pre-earnings date looks "high rank". Skew: 25Δ risk reversal and 25Δ butterfly, or SVI ρ and curvature. Term slope: IV_front/IV_next or σ_J share.

### Gaps
- The Dubinsky-Johannes PDFs (Columbia, NYU Stern) were blocked, so the exact estimator forms and reported magnitudes are unverified. The formula above is the standard derivation under their constant-diffusive-vol assumption.
- No Indian-market-specific empirical study of IV crush on NSE stock options was found in this pass.

---

## 4. Event-study statistics

### Takeaway
Use a classic event-study frame (MacKinlay-style windows, with abnormal return = return minus model-expected return, and abnormal vol/IV = change minus a matched control), aggregated cross-sectionally. Standard errors should be robust to event clustering (the same date across many stocks during earnings season), for example two-way clustered by firm and date, or with block/cluster bootstrap. Apply a strict multiple-testing penalty (HLZ t > 3.0, the deflated Sharpe ratio, PBO) and purged/embargoed CV or walk-forward for any parameter tuning.

### Cited Findings
- Harvey, Liu & Zhu (RFS 29(1), 2016, pp. 5–68): given extensive data mining, a newly discovered factor should clear **t > 3.0** rather than 2.0. Their framework allows for correlated tests and publication bias. — [Oxford Academic](https://academic.oup.com/rfs/article/29/1/5/1843824); [NBER w20592](https://www.nber.org/papers/w20592); [Duke PDF](https://people.duke.edu/~charvey/Research/Published_Papers/P118_and_the_cross.PDF)
- A counterpoint: "Most claimed statistical findings in cross-sectional return predictability are likely true". — [arXiv 2206.15365](https://arxiv.org/pdf/2206.15365) (title only, not read). This conflicts in emphasis with HLZ.
- Deflated Sharpe Ratio (Bailey & López de Prado, JPM 2014): corrects for **selection bias under multiple testing and non-normal returns (skew, kurtosis)**. The maximum SR over many noise trials is inflated. — [SSRN 2460551](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551); [PDF](https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf)
- Probability of Backtest Overfitting (Bailey, Borwein, López de Prado, Zhu) is a CV-based (CSCV) estimate of how often the in-sample-best configuration underperforms the median out of sample. PBO grows quickly with the number of trials. — [PDF](https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf); [Statistical Overfitting and Backtest Performance](https://sdm.lbl.gov/oapapers/ssrn-id2507040-bailey.pdf)
- Purged k-fold CV (López de Prado, 2017/AFML): **purging** removes training observations whose label-formation window overlaps the test set. An **embargo** (for example 5% of observations) is removed after each test fold. Combinatorial purged CV (CPCV) produces many backtest paths. — [Wikipedia: Purged cross-validation](https://en.wikipedia.org/wiki/Purged_cross-validation); [QuantInsti blog](https://blog.quantinsti.com/cross-validation-embargo-purging-combinatorial/)

### Inferences
- **DSR formula (from the paper, as commonly stated):** PSR(SR*) = Φ[(SR̂ − SR*)·√(T−1) / √(1 − γ3·SR̂ + (γ4−1)/4·SR̂²)], with SR* = √V[SR_n]·[(1−γ)·Φ⁻¹(1−1/N) + γ·Φ⁻¹(1−1/(N·e))], where γ ≈ 0.5772 (Euler-Mascheroni) and N = number of independent trials. The engine must **log every configuration tried** (the trial registry) to compute N and V[SR]. Verify these symbols against the PDF.
- Clustering: earnings seasons in India (mid-Jan, Apr–May, Jul–Aug, Oct–Nov) concentrate events on the same dates, so cross-sectional residuals correlate. Use date-clustered or two-way-clustered standard errors (for example `linearmodels` or `statsmodels`), or calendar-time portfolios, or a bootstrap that resamples whole event-dates.
- Bootstrap: use a stationary/block bootstrap over event-dates for the confidence intervals of mean P&L, win rate and CVaR. Report the bootstrap distribution of Sharpe alongside DSR.
- Holdout design: fix a final untouched OOS period (for example the last 12–18 months), and run anchored walk-forward (expanding train, rolling test by quarter/earnings season) for hyperparameters. The regime breaks from SEBI rule changes (Nov 2024 and Feb 2025 measures, lot-size changes) argue for reporting pre/post sub-periods separately.
- Tests for IV-crush significance: a paired test on ΔIV per event (Wilcoxon signed-rank as a robust alternative). For realized/implied, test the median of ln(R) = 0, since R is right-skewed.

### Gaps
- No India-specific event-study statistical standards were found. The methods above are general.

---

## 5. Backtest realism

### Takeaway
Options backtests fail mostly on fills and liquidity, so the design must be quote-aware. Fill at bid/ask, or mid ± k·half-spread with k calibrated, never at LTP/settle for illiquid strikes. Add liquidity filters, a full Indian cost stack, SPAN plus exposure margin simulation (including the post-2025 SEBI rules: upfront premium, no calendar-spread benefit on expiry day, 2% extra ELM on short index options on expiry day), and physical-settlement handling for stock options. An event-driven core with vectorized pre-computation is the standard hybrid design.

### Cited Findings
- SEBI measures in effect: calendar-spread margin benefit **removed on expiry day** of the near contract (from 10 Feb 2025). An **additional 2% ELM on short index options on expiry day**. **Option premium collected upfront** (Feb 2025). **Intraday position-limit monitoring with 4 snapshots/day** (Apr 2025). Index contract size raised to Rs 15–20 lakh. — [Jainam](https://www.jainam.in/blog/sebi-new-rules-for-fo-trading/); [ICICI calendar-spread article](https://www.icicidirect.com/futures-and-options/articles/calendar-spreads-in-f-o-after-sebi-s-new-rules-what-you-need-to-know); [Zerodha Z-Connect](https://zerodha.com/z-connect/business-updates/sebis-new-rules-for-index-derivatives-heres-whats-changing)
- LEAN uses QuoteBar (bid/ask) data so that simulated option fills include the spread cost. — [QuantConnect docs](https://www.quantconnect.com/docs/v2/writing-algorithms/securities/asset-classes/index-options/handling-data)
- An example of an event-driven engine with first-class options: NautilusTrader has option instrument types, option-chain aggregation, venue Greeks streaming and a local Black-Scholes Greeks calculator. It is actively developed, with v1.225/1.226 and OKX option Greeks added in April 2026. — [NautilusTrader Options docs](https://nautilustrader.io/docs/latest/concepts/options/); [RELEASES.md](https://github.com/nautechsystems/nautilus_trader/blob/develop/RELEASES.md)
- "Implementation risk" in backtesting is a separately quantifiable error source (2026 paper, title only). — [arXiv 2603.20319](https://arxiv.org/pdf/2603.20319)

### Inferences
- **Fill model tiers:** (1) conservative: buy at ask, sell at bid; (2) realistic: mid ± α·(spread/2), with α ≈ 0.5–1.0 for stock options; (3) optimistic: mid, for sensitivity analysis only. Size cap: order qty ≤ x% of displayed depth or of the day's volume, otherwise partial fill or rejection. Where only EOD bhavcopy exists, model spread as a function of moneyness, DTE, underlying liquidity and premium (fitted from any intraday snapshots), and state this assumption in the report.
- **Liquidity filters at entry:** min OI, min contracts traded, max spread/mid, premium ≥ tick-size multiple (NSE tick is Rs 0.05, which is significant for cheap OTM options), strike within ±N% of the forward.
- **Indian cost stack (verify the current rates before the spec; not fetched here):** brokerage, STT on options (sell side on premium; on exercise, on intrinsic value), exchange transaction charges, SEBI turnover fee, stamp duty (buy side), 18% GST on brokerage and exchange fees, plus DP charges on physical delivery. STT rates were raised in the Union Budget 2024 (Oct 2024). Exact current rates are a gap.
- **Margin simulation:** margin = SPAN (scenario-based, 16 scenarios, from the NSE Clearing risk-parameter files) + exposure/ELM + the expiry-day extra ELM + premium for longs. Reproducing SPAN requires the daily NSCCL SPAN parameter file. A simpler approximation (a % of notional by underlying volatility) is acceptable for research but should be flagged. Margin drives capital usage and so return on margin, a key metric for short-vol event trades.
- **Settlement:** NSE stock options are **physically settled** (since 2018–19), with ITM long and short positions going to delivery. Index options are cash-settled. European exercise means no early-assignment modelling. The engine must either force-close before expiry-week delivery margins rise, or simulate delivery obligation and cost. Event trades usually exit at T+1, but events near expiry hit this.
- **Gap risk:** events produce overnight gaps. For short straddles, simulate at the post-event open with a wide spread (spreads widen at the open), and stress with historical max gaps per stock.
- **Architecture:** vectorized (polars/numpy over an event×contract matrix) suits the event study and parameter sweeps, because each event is an independent short-horizon trade. Use an event-driven engine (NautilusTrader-style) for portfolio-level constraints: margin, overlapping positions, capital limits, hedging. A common design is a vectorized "event trade ledger" generator feeding an event-driven portfolio simulator.

### Gaps
- Could not fetch the NSE Clearing SPAN methodology or the current NSE/SEBI fee schedule. Exact STT and exchange-charge rates as of 2026 are not verified.
- No public empirical calibration of NSE stock-option effective spreads was found.

---

## 6. Metrics and reporting

### Takeaway
Report per-event P&L distributions (normalised per unit premium and per unit margin), and not just aggregate Sharpe. Short-vol event strategies have negatively skewed P&L, so tail metrics (CVaR, max loss, tail ratio) and Greek attribution are essential, alongside hit rate and expectancy. Slice by sector, IV rank, implied-move bucket and event session.

### Cited Findings
- The DSR adjusts Sharpe for skew and kurtosis and for the number of trials. It is therefore the appropriate headline Sharpe for a negatively skewed options strategy. — [Bailey & López de Prado](https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf)
- Optopsy-style reporting includes chronological trade simulation with capital tracking, position limits, equity curves and multi-strategy portfolio simulation. — [goldspanlabs/optopsy](https://github.com/goldspanlabs/optopsy)

### Inferences
- **Per-event:** P&L (Rs, % of premium, % of margin), win rate, expectancy = p·avg_win − (1−p)·avg_loss, payoff ratio, median, 5th/1st percentile, and max loss as a multiple of the premium collected.
- **Portfolio:** CAGR on margin, Sharpe and Sortino (annualised by events/year, not √252, when trades are sparse; or build a daily MTM series), max drawdown and duration, CVaR/ES 95/99 (the average of the worst 5%/1%), tail ratio = |P95|/|P5|, Calmar, skew and kurtosis.
- **Greek attribution (daily or per-leg):** ΔP ≈ δ·ΔS + ½Γ·ΔS² + ν·Δσ + θ·Δt + residual. Use Black-76 Greeks on the fitted surface at t−1 to separate "vega P&L from crush" from "gamma P&L from the move". This is the key diagnostic for an IV-crush strategy (crush profit vs gap loss). Track the residual (a large residual means the surface or smile moved non-parallel).
- **Heatmaps:** P&L or R by sector × IV-rank decile, implied-move bucket × realized/implied, event session (pre/intra/post), DTE of the front expiry, and year (regime). Plotly/Dash or Streamlit.

### Gaps
- No authoritative industry standard for options-backtest report templates was found. The metrics above are common practice.

---

## 7. Open-source tooling (status as of 2026)

### Takeaway
A pragmatic 2026 stack: **polars + DuckDB over Parquet/Arrow** for storage and research; **py_vollib_vectorized / Let's Be Rational** (or newer GPU libraries such as fast-vollib) for IV; **QuantLib (actively released, 1.43)** for validation and curves; custom SVI/SSVI fitting on scipy; **NautilusTrader** (active) as the event-driven engine where needed; Optopsy (active forks) as a reference for strategy definition; India data via **jugaad-data / nselib / nsepython** (scrapers, fragile) and **OpenAlgo** for broker connectivity; Streamlit or Dash for dashboards.

### Cited Findings
- **QuantLib (Python):** 1.40 (14 Oct 2025), 1.41 (13 Jan 2026), 1.42 (14 Apr 2026), 1.42.1 (17 Apr 2026). Libraries.io lists 1.43. It follows a quarterly cadence and is actively maintained. There is also a new "PyQuantLib" modern-bindings project. — [libraries.io QuantLib](https://libraries.io/pypi/QuantLib); [QuantLib-Python docs](https://quantlib-python-docs.readthedocs.io/en/latest/); [PyQuantLib](https://libraries.io/pypi/pyquantlib)
- **py_vollib_vectorized:** vectorized Let's Be Rational with Black, BS and BSM, IV and Greeks. It depends on py_vollib ≥1.0.1, numba and py_lets_be_rational. — [GitHub](https://github.com/marcdemers/py_vollib_vectorized); [py_vollib docs 1.0.3](https://vollib.org/documentation/1.0.3/autoapi/py_vollib/black_scholes/implied_volatility/index.html)
- **fast-vollib (2026):** PyTorch/JAX/CUDA IV library. — [ResearchGate](https://www.researchgate.net/publication/404333035_Fast-Vollib_A_Fast_Implied_Volatility_Library_for_Pythonwith_PyTorch_JAX_and_CUDA_Fused-Kernel_Backends)
- **Optopsy:** the original is apryor6. The actively maintained fork is **goldspanlabs/optopsy** (formerly michaelchu/optopsy), with 38 built-in strategies (spreads, condors, calendars, diagonals), per-leg delta targeting, a trade simulator with capital tracking and portfolio simulation. An "optopsy-mcp" Rust rewrite exists for LLM/MCP use. — [goldspanlabs/optopsy](https://github.com/goldspanlabs/optopsy); [apryor6/optopsy](https://github.com/apryor6/optopsy); [PyPI](https://pypi.org/project/optopsy/1.0.1/)
- **NautilusTrader:** Rust core with Python API, option instruments, chains, Greeks calculator. Active: 2026 releases v1.225 and v1.226. — [Options docs](https://nautilustrader.io/docs/latest/concepts/options/); [release v1.226.0](https://newreleases.io/project/github/nautechsystems/nautilus_trader/release/v1.226.0)
- **QuantConnect LEAN:** option universes, option-chain filtering, IV/Greeks indicators, multiple option price models, QuoteBar-based spread-aware fills. There is no native NSE options data in the docs found. — [QuantConnect equity options](https://www.quantconnect.com/docs/v2/writing-algorithms/universes/equity-options); [pricing models](https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/options-models/pricing)
- **SSVI reference implementation:** [JackJacquier/SSVI](https://github.com/JackJacquier/SSVI); a MATLAB SVI implementation also exists: [MathWorks File Exchange 49962](https://ch.mathworks.com/matlabcentral/fileexchange/49962-gatherals-and-jacquier-s-arbitrage-free-svi-volatility-surfaces)
- **India data:**
  - **jugaad-data** downloads historical and live NSE stocks, F&O, index and index F&O data plus RBI rates. It has a CLI and caching and targets the new NSE site (v0.31.1 on libraries.io). — [GitHub](https://github.com/jugaad-py/jugaad-data); [libraries.io](https://libraries.io/pypi/jugaad-data)
  - **nselib** fetches equity and derivatives bhavcopies, F&O price-volume data and live option chains (Python ≥3.8). — [PyPI](https://pypi.org/project/nselib/)
  - **nsepython** runs in server environments and absorbed the unmaintained NSEpy/NSETools functions. — [PyPI](https://pypi.org/project/nsepython/)
  - **nser** is an R package for F&O bhavcopies. — [nser](https://nandp1.github.io/nser/)
- **OpenAlgo:** self-hosted Flask + React 19 platform with about 36 broker plugins (35 Indian securities brokers plus Delta Exchange) and TradingView/Amibroker/Python integrations. It is a FOSS Hack 2026 partner project and actively developed. The canonical repo is marketcalls/openalgo. — [docs.openalgo.in](https://docs.openalgo.in/); [GitHub marketcalls/openalgo](https://github.com/marketcalls/openalgo); [FOSS United](https://fossunited.org/fosshack/2026/partner-projects/openalgo)

### Inferences
- **Storage:** Parquet partitioned by date/underlying, queried with DuckDB (SQL, zero-ops) and polars (lazy dataframes). This is enough for an NSE universe of about 200 F&O stocks × ~15 years of EOD. Move to ClickHouse or TimescaleDB only for tick or minute option snapshots at scale (billions of rows) or multi-user serving.
- **NSE scrapers:** NSE blocks aggressive scraping and changes endpoints. Use scrapers for EOD bhavcopy archives only. For intraday option-chain history, you need paid vendor data (for example, TrueData or Global Datafeeds, not researched here) or self-collected broker API snapshots via OpenAlgo or a broker SDK.
- py_vollib and py_lets_be_rational are mature but low-activity (not verified). Pin versions, or vendor the Jäckel algorithm via QuantLib or fast-vollib.
- vectorbt and backtrader: not researched in this pass. backtrader is widely considered unmaintained (unverified). vectorbt has no native options Greeks/chain model (unverified).

### Gaps
- Maintenance status of vollib, py_vollib_vectorized, OptionLab, optlib, backtrader and vectorbt (open vs PRO) was not verified in this pass.
- Release dates of the latest versions of nselib and nsepython were not captured.

---

## 8. ML/stat models for predicting realized/implied ratio

### Takeaway
Treat each event as one sample, with target = ln(realized move ÷ implied move) (or the sign of the short-straddle P&L). Features must be computed strictly from data up to the T−1 snapshot. Use gradient boosting (LightGBM/XGBoost) with purged, embargoed, time-ordered CV grouped by event-date, and evaluate with economic metrics (the P&L of trading on the prediction) plus DSR/PBO across all tried configurations.

### Cited Findings
- Purging and embargo prevent leakage from overlapping label windows, and CPCV gives multiple OOS paths. — [Wikipedia](https://en.wikipedia.org/wiki/Purged_cross-validation); [QuantInsti](https://blog.quantinsti.com/cross-validation-embargo-purging-combinatorial/)
- PBO estimates the chance that the in-sample-best model underperforms OOS. — [Bailey et al.](https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf)
- Concave smiles signal bimodal event risk, and are a candidate feature. — [AGKR](https://fmai.memberclicks.net/assets/docs/Derivatives2022/Concave_AGKR.pdf)

### Inferences
- **Features (all as of T−1 close or the pre-announcement snapshot):** implied move and σ_J; event-variance share; run-up magnitude; ex-event IV rank; historical realized/implied for the same stock (the last 4–8 events, an expanding mean, **excluding the current event**); historical average absolute event move; realized vol (5/20/60d) vs IV; skew (25Δ RR), butterfly, smile concavity; term slope; sector; market-cap/liquidity; India VIX level and change; announcement session; days to front expiry; the number of peers already reported this season, and their surprise dispersion (only if reported before T); pre-event drift and momentum; OI/PCR changes.
- **Leakage traps:** (1) using the announcement date from a calendar that was revised after the fact (use first_seen_ts); (2) intraday announcements where the "T−1 close" is fine but features using T's close leak; (3) cross-sectional normalisation using the full-sample mean or std (use expanding statistics); (4) survivorship, by training only on currently F&O-listed stocks; (5) corporate-action-unadjusted strikes creating fake moves; (6) random k-fold across the same earnings date, since peers' outcomes are correlated, so group by date.
- **Model:** start with a regularised linear or quantile regression baseline, then LightGBM with monotonic constraints where theory suggests them (for example, a higher historical R gives a higher predicted R). Calibrate with isotonic or quantile outputs. Use SHAP for attribution. Choose the evaluation metric on a decision basis: the Sharpe/DSR of a rule that trades (sells the straddle) only when predicted R < threshold, after costs.
- Sample size: about 180–200 NSE F&O stocks × 4 results/year × ~10 years gives roughly 7–8k events. That is modest for GBMs, so keep feature counts small and hyperparameter searches narrow (every trial counts toward the DSR's N).

### Gaps
- No published study applying ML to NSE event implied/realized ratios was found in this pass.
- Exact NSE F&O stock count per year (for the survivorship table sizing) is not verified.
