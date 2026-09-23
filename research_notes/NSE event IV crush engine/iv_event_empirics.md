# Empirics of Implied Volatility Around Scheduled Events: Pre-Event Run-Up, Post-Event Crush, Implied vs Realized Moves (US foundations, Indian NSE stock options focus)

> Research-process note: in this session nearly all full-text fetches (Columbia, Rice, Cambridge, SSRN mirrors, Stern, Moontower, IBKR, Quantpedia, newhaven.edu) were blocked by the network egress proxy. Findings below are drawn from search-result abstracts/snippets of the cited primary pages. Where a paper's detailed tables (e.g., exact jump-vol magnitudes) could not be read, this is flagged in Gaps rather than filled from memory. Market labels: **[US]**, **[India/NSE]**, **[General/method]**.

## Q1. What does the academic literature show about IV run-up before earnings and IV crush after? Magnitudes, holding periods, straddle returns

### Takeaway
Across 45+ years of US evidence, IV rises monotonically into scheduled earnings and collapses immediately after (Patell & Wolfson 1979; Dubinsky & Johannes). Whether the *pre-event premium* is fair is regime-dependent: Gao/Xing/Zhang find ATM straddles bought 3 days before and held into the announcement earned +3.34% (investors *under*-estimate event uncertainty, 1996–2013 era), while later evidence (BSIC 2011–2021, de Silva/Smith/So, ORATS 2023–2025 average) shows event options have more often been *overpriced*, with a sharp reversal in the Q4-2025 season (ORATS: ~+45% avg straddle return). The only India-specific peer-reviewed study found (Saurav, Agarwalla & Varma, IIMA) confirms the same monotonic run-up and post-EA decline for NSE single-stock options, and additionally for skew and option volume.

### Cited Findings
**Foundational [US]**
- Patell & Wolfson (1979, J. Accounting & Economics 1(2):117–140) examined call prices on dates leading up to and through the annual earnings announcement; they confirmed that investors anticipate the release, with *systematic changes in Black-Scholes implied variance rates* around the disclosure date — [IDEAS/RePEc](https://ideas.repec.org/a/eee/jaecon/v1y1979i2p117-140.html); [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/016541017990003X)
- Subsequent literature (JFQA "Creation and Resolution of Market Uncertainty: The Impact of Information Releases on Implied Volatility") confirms IVs increase prior to earnings and drop sharply immediately after — [Cambridge Core JFQA](https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/abs/creation-and-resolution-of-market-uncertainty-the-impact-of-information-releases-on-implied-volatility/7D6E476DAEBC8D2EEBF6EC0E6320F5C8)
- Dubinsky & Johannes ("Earnings Announcements and Equity Options"): build no-arbitrage option models with a jump on the announcement date and estimators of "earnings jump volatility"; find (i) IV increases before announcements, (ii) adding announcement-date jumps *drastically reduces pricing errors*, (iii) anticipated uncertainty is *quantitatively large, time-varying and informative about future realized volatility*, (iv) earnings-uncertainty estimates rise in market stress (2000–2001) — [Columbia Business School](https://business.columbia.edu/faculty/research/earnings-announcements-and-equity-options); [SSRN 600593](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=600593)
- Extended version: Dubinsky, Johannes, Kaeck & Seeger, "Option Pricing of Earnings Announcement Risks" (Review of Financial Studies 2019) — [Tinbergen](https://tinbergen.nl/publication/160062/option-pricing-of-earnings-announcement-risks); [VU Research Portal PDF](https://research.vu.nl/ws/portalfiles/portal/108247883/Option_Pricing_of_Earnings_Announcement_Risks.pdf)

**Straddle returns [US]**
- Gao, Xing & Zhang, "Anticipating Uncertainty: Straddles around Earnings Announcements" (JFQA 2018, 53(6):2587–2617): ATM straddles from **3 days before the EA to the EA date earn a highly significant +3.34%** average return, whereas individual-stock straddles *in general* earn significantly negative returns; interpreted as investors under-estimating EA uncertainty — [SSRN 2204549](https://doi.org/10.2139/ssrn.2204549); [IDEAS](https://ideas.repec.org/a/cup/jfinqa/v53y2018i06p2587-2617_00.html)
- GXZ cross-section: positive EA straddle returns are larger for **smaller firms, higher-volatility firms, higher-kurtosis firms, firms with more volatile past earnings surprises, and lower-volume/higher-transaction-cost stocks** — [SSRN 2204549](https://doi.org/10.2139/ssrn.2204549)
- BSIC (Bocconi) backtest of "straddling into earnings" on S&P 500, 2011–2021: **consistently negative returns**, contrasting with earlier literature that found profitability 1996–2013 — [BSIC Part II](https://bsic.it/straddling-outside-and-into-earnings-part-ii-2/); [BSIC Part I](https://bsic.it/straddling-outside-and-into-earnings/)
- Khan & Khan, "17-Year Backtest of Straddles around SP500 Earnings Announcements" (SSRN 4832160): buy ATM straddle 1 day before, sell 1 day after → reported **108% CAGR, Sharpe 2.2 over 13,120 trades**, but **single-week losses up to 83.8%** and excludes commissions/slippage/taxes; long straddles opened 30 trading days before lose value into T-1 (theta > IV rise); short straddles near expiry judged unviable (early-assignment risk on American options) — [SSRN 4832160](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4832160); [PapersWithBacktest summary](https://paperswithbacktest.com/strategies/hamzah-17-year-backtest-of-straddles-around-sp500-earnings-announcements)
- ORATS (Feb 12, 2026): over the prior four weeks, straddles on US reporters returned **~+45% average vs ~−2% average over the previous twelve quarters**; actual moves consistently exceeded implied moves; attributed to dispersion, guidance sensitivity, macro uncertainty — [ORATS blog](https://orats.com/blog/earnings-straddles-strong-season-2026)

**Risk premium interpretations [US]**
- Barth & So, "Non-Diversifiable Volatility Risk and Risk Premiums at Earnings Announcements" (The Accounting Review 2014, 89(5):1579–1607): investors pay a premium to hedge EAs expected to raise *market* volatility; option-embedded VRP proxy significantly positively related to announcement-specific non-diversifiable vol risk; **premiums concentrated in bellwether firms** and produce *predictable variation in straddle returns around EAs* — [SSRN 1635584](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1635584); [MIT Open Access](https://dspace.mit.edu/bitstream/handle/1721.1/111118/non-diversifiable-volatility-Eric-So.pdf?sequence=1&isAllowed=y)
- de Silva, Smith & So, "Losing is Optional: Retail Option Trading and Expected Announcement Volatility" (Review of Finance 2026, 30(2)): retail buys options concentrated before EAs with high expected abnormal volatility; they **overpay relative to realized volatility, pay large bid-ask spreads, and are slow to respond to predictable post-EA vol declines**; retail losses **5–9% on average around EAs, 10–14% for high-expected-vol EAs**; market makers are the main beneficiaries, especially post-COVID — [SSRN 4050165](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4050165); [Review of Finance](https://academic.oup.com/rof/article-abstract/30/2/489/8301159); [MIT Sloan summary](https://mitsloan.mit.edu/ideas-made-to-matter/retail-investors-lose-big-options-markets-research-shows)

**Practitioner descriptions of the crush [US]**
- IV typically peaks the day before earnings and falls on the first post-release session, "sometimes losing 30%, 40% or more" of IV — (practitioner, non-peer-reviewed) summarised via [IBKR Quant Blog](https://www.interactivebrokers.com/campus/ibkr-quant-news/the-unique-behavior-of-pre-earnings-announcement-implied-volatility/) and [MenthorQ](https://menthorq.com/guide/iv-crush-understanding-the-earnings-driven-volatility-spike-and-how-to-capitalize-on-it/)
- Pre-EA IV build-up and IV spread relate to announcement returns, consistent with informed trading in options (J. Banking & Finance, "Volatility spread and stock market response to earnings announcements") — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0378426617300791)

**India/NSE**
- Saurav, Agarwalla & Varma (IIM Ahmedabad), "Asymmetric Uncertainty Around Earnings Announcements: Evidence from Options Markets" (American Business Review, Nov 2024, 27(2)): using Indian single-stock options, **IV (uncertainty) and options skew (asymmetric uncertainty) increase monotonically before the EA day and decrease after**; option volume relative to spot and futures behaves similarly (informed traders prefer options); **skew and put-call volume ratio predict the sign of the EA surprise one day ahead** — [IIMA](https://www.iima.ac.in/publicationasymmetric-uncertainty-around-earnings-announcements-evidence-options-markets); [ABR record](https://digitalcommons.newhaven.edu/americanbusinessreview/vol27/iss2/4/)
- Same study's methodology (from snippet): exact EA broadcast times taken from NSE corporate-announcement pages; only **near-month option series expiring after the EA** used because they are most liquid — [ABR PDF](https://digitalcommons.newhaven.edu/cgi/viewcontent.cgi?article=2897&context=americanbusinessreview)

### Inferences
- The *sign* of the event premium is not stable: 1996–2013 US favoured long straddles into EAs (GXZ), 2011–2021 and ~2023–2025 favoured sellers (BSIC, ORATS "−2% over 12 quarters"), and Q4-2025/early-2026 flipped strongly to buyers (ORATS +45%). An engine must evaluate strategies by regime/sub-period, not report a single pooled mean.
- Khan & Khan's T-1→T+1 result (Sharpe 2.2) conflicts with BSIC's negative 2011–2021 finding on a near-identical window; differences likely stem from pricing (mid vs bid/ask), strike selection, and cost treatment — reproduce both with explicit fill assumptions before trusting either.
- The Indian evidence establishes the *shape* (run-up, crush, skew build) but not the *profitability* of event straddles on NSE — the latter is the key open gap the engine must fill empirically.

### Gaps
- Exact magnitudes of Dubinsky–Johannes earnings jump vol (typical % move per announcement, pre/post IV level changes) and GXZ window-by-window tables (e.g., returns for holding from −10 days, post-EA returns, Sharpe) could not be read (full text blocked).
- Barth & So numeric premium estimates not retrieved.
- No quantitative magnitude (average IV points or % drop) of NSE post-results crush found in any peer-reviewed or reputable source; Saurav et al.'s numeric tables not accessible.

## Q2. How is event-implied move / event volatility extracted from the term structure? Formulas

### Takeaway
Standard approach (Dubinsky–Johannes; practitioner "total variance" method): variance is additive in time, so total implied variance of an expiry spanning the event = diffusive (ex-event) variance × time + event jump variance. Using two expiries (one or both spanning the event) or a pre-event/post-event time-series comparison isolates the event variance; the implied event move ≈ √(event variance), and the straddle-based shortcut is implied 1σ move ≈ straddle / S × 1.25 (straddle ≈ 0.8·σ√T·S).

### Cited Findings
- Dubinsky & Johannes develop estimators of the anticipated earnings jump volatility from option prices within no-arbitrage models that add a deterministic-date jump — [SSRN 600593](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=600593); [Columbia](https://business.columbia.edu/faculty/research/earnings-announcements-and-equity-options)
- Total variance method: total variance per expiry = IV² × T; variance is additive but vol is not; comparing total variance across expirations straddling the event isolates the event's contribution — [FlashAlpha](https://flashalpha.com/articles/volatility-term-structure-contango-backwardation-events); [DEV Community mirror](https://dev.to/tomasz_dobrowolski_35d32c/how-to-read-volatility-term-structure-contango-backwardation-event-pricing-33g8)
- Event variance is embedded in every expiry on/after the event, with its IV impact attenuated as DTE grows ("in inverse proportion to DTE") — [Moontower](https://blog.moontower.ai/how-an-option-trader-extracts-earnings-from-a-vol-term-structure/); [Moontower term structure part 2](https://blog.moontower.ai/volatility-term-structure-from-multiple-angles-part-2/)
- CME publishes an Event Volatility Calculator (QuikStrike) implementing this decomposition for futures options — [CME Group](https://www.cmegroup.com/tools-information/quikstrike/event-volatility-calculator.html)
- Straddle approximation: ATM straddle ≈ √(2/π)·σ·S·√T ≈ 0.7979·σ·S·√T; hence 1σ expected move ≈ straddle × 1.2533 — [Brilliant wiki](https://brilliant.org/wiki/straddle-approximation-formula/); [MenthorQ](https://menthorq.com/guide/from-straddle-price-to-expected-move/)
- Concave IV smiles (bimodal risk-neutral density) before EAs are an ex-ante option signal of event risk; most visible in short-expiry options — Alexiou, Goyal, Kostakis & Rompolis (Review of Finance 2025, 29(4)) — [SSRN 3840081](https://ssrn.com/abstract=3840081); [OUP](https://academic.oup.com/rof/article/29/4/963/8079062)

### Formulas [General/method — standard algebra consistent with the sources above; derivation mine]
Notation: σ_i = ATM IV of expiry i, T_i = years (or trading days/252) to expiry, σ_d = diffusive (non-event) vol, σ_E² = event jump variance (one-day "event variance", in return² units).

1. **Additive decomposition** (expiry spanning one event):
   σ_i² · T_i = σ_d² · T_i + σ_E²   (event adds a lump of variance, not a rate; DJ-style formulation often writes T_i − 1/252 for the diffusive part to exclude the event day)
2. **Two-expiry (term-structure) estimator**, both expiries spanning the event, same σ_d assumed:
   σ_d² = (σ_2² T_2 − σ_1² T_1) / (T_2 − T_1)
   σ_E² = σ_1² T_1 − σ_d² T_1 = (σ_1² − σ_2²)·T_1·T_2 / (T_2 − T_1)
   (valid only when σ_1 > σ_2, i.e., event-induced inverted front term structure; negative estimates = data/noise issue)
3. **Time-series (pre/post) estimator**: σ_E² ≈ σ_pre² T_pre − σ_post² T_post (same expiry, IV immediately before vs after the event, adjusting for the elapsed day) — a realized "crush"-based estimate.
4. **Forward event vol / expected move**: implied event move (1σ, as % of S) = σ_E; expected absolute move = √(2/π)·σ_E ≈ 0.8·σ_E (under normal jump). Annualised "event-day vol" = σ_E·√252.
5. **Straddle shortcut**: implied move ≈ (Call_ATM + Put_ATM)/S (this is the *mean absolute* move under normality); 1σ move ≈ 1.25 × straddle/S. For a front expiry with residual diffusive days, subtract ex-event variance: σ_E² ≈ (1.2533·Straddle/S)² − σ_d²·T.
6. **Calendar for India**: NSE single-stock options have monthly expiries only (no weeklies on stocks), so the event-spanning front expiry often has many diffusive days left; the two-expiry estimator (current month vs next month) is structurally the primary tool.

### Inferences
- Because NSE stock options lack weeklies, the event variance is diluted in a ~1–4 week front expiry; accurate σ_d estimation (e.g., from next-month IV, post-event IV history, or realized vol ex-event days) matters more than in US names with weekly expiries.
- Concavity of the smile (Alexiou et al.) is a second, strike-space extractor of event risk that complements term-structure extraction.

### Gaps
- Exact DJ time-series and term-structure estimator equations (their specific day-count conventions) not verified from full text.
- The claim that NSE single-stock options have only monthly expiries is from background knowledge, not verified in this session.

## Q3. How often does the implied move overstate vs understate the realized move? What predicts profitable event-vol selling?

### Takeaway
US practitioner data: stocks stay inside the implied move roughly 70–75% of the time (vs 68% theoretical for 1σ), i.e., implied tends to modestly overstate; but tails and regime shifts are material (e.g., late-2025 season realized > implied). Predictors of *richer* event pricing (better for sellers): high expected volatility/retail attention, concave pre-EA smiles (lower straddle returns), bellwether firms (non-diversifiable premium). Predictors of *cheaper* event pricing (better for buyers, per GXZ): small size, high vol/kurtosis, volatile past surprises, low volume. No Indian hit-rate statistics were found.

### Cited Findings
- [US, practitioner] Stocks have historically stayed inside the options implied move roughly **70–75% of the time** vs 68% theoretical 1σ containment; average IV − RV difference cited ~3.25 (vol points) — [Maverick Trading](https://www.mavericktrading.com/free-trading-videos/articles/implied-vs-actual-earnings-moves-is-the-market-overpricing-volatility) (practitioner; methodology not disclosed)
- [US] ORATS: "in recent years" implied earnings moves often overstated realized; last-12-quarter average straddle return ~−2%; then season to Feb-2026 averaged ~+45% as realized exceeded implied — [ORATS](https://orats.com/blog/earnings-straddles-strong-season-2026)
- [US] ORATS research on predictors of earnings moves (historical earnings moves, IV ratio to SPY, etc.) — [ORATS Medium](https://medium.com/option-research-technology-services/the-best-predictors-of-earnings-moves-b7c0e83fba7f); [ORATS IV-ratio spotlight](https://orats.com/blog/options-indicator-spotlight-implied-volatility-ratio-to-spy-0)
- [US] Concave IV curves: delta-neutral straddles, strangles and delta-vega-neutral calendar straddles have **significantly lower (negative) returns** when the pre-EA smile is concave, even though these firms do realize larger EA absolute returns — i.e., the premium more than compensates — [Review of Finance](https://academic.oup.com/rof/article/29/4/963/8079062); [SSRN 3840081](https://ssrn.com/abstract=3840081)
- [US] Firm characteristics (GXZ): long EA straddles better for small, high-vol, high-kurtosis, volatile-surprise, illiquid names — [SSRN 2204549](https://doi.org/10.2139/ssrn.2204549)
- [US] Bellwether firms carry non-diversifiable EA vol premia (sell-side edge concentrated there) — [SSRN 1635584](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1635584)
- [US] High expected announcement volatility attracts retail buyers who overpay; losses rise to 10–14% for high-expected-vol EAs — [SSRN 4050165](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4050165)
- [India] Pre-EA skew and put-call volume ratio predict EA surprise sign (directional info, not magnitude) — [IIMA](https://www.iima.ac.in/publicationasymmetric-uncertainty-around-earnings-announcements-evidence-options-markets)
- [India, practitioner] Zerodha Varsity suggests cross-referencing IV Percentile (IVP) with the earnings calendar; a stock at ~90th IVP with results next week is priced near the top of its range, likely due to the event — [Zerodha Varsity on X](https://x.com/ZerodhaVarsity/status/2075162853032771873)

### Inferences
- Candidate feature set for a sell/buy-vol classifier: implied/historical event-move ratio (current implied move ÷ trailing mean absolute EA move), IV rank/percentile, smile concavity, front/back term-structure slope, size/liquidity, past surprise volatility, bellwether status, retail-flow proxies (on NSE: option-to-futures volume ratio, OI build-up).
- GXZ and Alexiou et al. can be reconciled: GXZ find average under-pricing concentrated in small/illiquid names (where bid-ask costs likely erase it), while concavity identifies names where the market already over-prices the event.

### Gaps
- No systematic Indian (NSE) statistics on implied-move containment rates, average IV-crush size, or straddle P&L around results were found from any credible source; Sensibull/Opstra/Quantsapp publish tools (IV charts, IVP) but I found no published aggregate studies.
- India VIX/earnings linkages: an NSE working paper on India VIX and risk management exists (WP/9/2013) but was not read and appears to concern index vol, not results — [NSE WP 9/2013](https://nsearchives.nseindia.com/research/content/res_WorkingPaper9.pdf).

## Q4. India-specific evidence (NSE stock options, India VIX, IIM/NSE papers, practitioner studies)

### Takeaway
Only one rigorous India-specific event study was located (Saurav–Agarwalla–Varma, IIMA, 2024), confirming the IV run-up/crush, skew build-up and informed-options-trading patterns on NSE single-stock options. Practitioner material (Zerodha Varsity, Sensibull, trade press) describes IV crush qualitatively, with anecdotal numbers only.

### Cited Findings
- India has one of the world's largest single-stock options markets and uniquely liquid single-stock futures *and* options, making it a good laboratory for EA studies — [IIMA](https://www.iima.ac.in/publicationasymmetric-uncertainty-around-earnings-announcements-evidence-options-markets)
- IV and skew rise monotonically into the EA and fall after; options volume (relative to spot and futures) follows the same pattern — [ABR / Saurav, Agarwalla, Varma 2024](https://digitalcommons.newhaven.edu/americanbusinessreview/vol27/iss2/4/)
- Indian Nifty index options exhibit a classic U-shaped smile and term-structure patterns (index, not EA-specific) — Shaikh & Padhi, J. Indian Business Research — [Emerald](https://www.emerald.com/insight/content/doi/10.1108/jibr-12-2013-0103/full/pdf)
- Zerodha Varsity: TCS, Infosys, Tata Steel "tend to make strong moves" after results, framed as long-straddle candidates; TCS reports after market hours (timing matters) — [Zerodha Varsity: Long Straddle](https://zerodha.com/varsity/chapter/the-long-straddle/)
- Trade press on Indian IT results: IV rises in the weeks before IT earnings season, peaks just before announcement, then crashes; buyers often lose even when direction is right; IT stocks react to constant-currency revenue growth, operating margin, TCV/order book and especially guidance — [FirstIndia press release](https://firstindia.co.in/news/press-releases/what-earnings-week-really-does-to-it-stock-options-1787138226) (press release; low evidentiary weight)
- Anecdote: Reliance result where ATM IV reportedly fell from ~35% to ~18% overnight — reported by a Sensibull review site, not a primary Sensibull study — [PaperTradingApp Sensibull review](https://papertradingapp.com/sensibull/) (unverified; treat as illustrative only)
- Tools: Sensibull provides IV charts, IV rank/percentile and skew for NSE stocks — [Sensibull IV chart](https://web.sensibull.com/implied-volatility-chart); [Sensibull IVP option chain](https://besensibull.medium.com/option-chain-with-iv-percentile-d0f296d42445)
- Recent SSRN work testing IV-capture strategies over earnings seasons (30-stock sample, Q1-2020–Q4-2025; market not confirmed as India) — [SSRN 6710818, Minda Lu](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6710818)

### Inferences
- The absence of published NSE event-straddle P&L studies is itself an opportunity/necessity: the engine must build its own panel (NSE bhavcopy F&O EOD data + NSE corporate-announcement timestamps, as Saurav et al. did).
- NSE-specific structural features to model (background knowledge, not verified here): monthly-only stock expiries, physical settlement of stock derivatives at expiry, large lot sizes, STT on exercised options — all affect whether results falling close to expiry are tradable.
- Results announced after market hours or during trading (common in India, board meeting outcomes can come mid-session) make "event day" definition non-trivial; exact timestamps are essential.

### Gaps
- No Indian quantitative measure of average IV-crush size (IV points or %) after results; no hit-rate of implied vs realized moves on NSE; no Opstra/Quantsapp/NSE working paper study located.
- No study located linking India VIX dynamics to aggregate results seasons.

## Q5. Risks/tails of short event vol and evidence on "buy the run-up" (long options 1–3 weeks before, exit pre-event)

### Takeaway
Short event vol wins most of the time but carries fat, gap-driven tails (e.g., single-week losses up to 83.8% for straddle strategies in Khan & Khan; regime flips like ORATS' +45% straddle season). Evidence for "buy the run-up" is weak: long straddles opened ~30 days out lose value into T-1 because theta outweighs the IV rise; practitioner claims of profitable 1–2 week pre-earnings straddles are anecdotal/backtest-dependent.

### Cited Findings
- [US] Long ATM straddles opened 30 trading days before EAs **decline in value up to T-1** — theta decay outweighs the IV rise — [SSRN 4832160](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4832160)
- [US] Same study: T-1→T+1 long straddles had weekly drawdowns up to 83.8%; short straddles near expiry flagged for early-assignment risk (American options) — [PapersWithBacktest](https://paperswithbacktest.com/strategies/hamzah-17-year-backtest-of-straddles-around-sp500-earnings-announcements)
- [US, practitioner] Some traders buy straddles a few days before earnings to capture the IV increase and always exit before the event to avoid the crush — [BSIC](https://bsic.it/straddling-outside-and-into-earnings/); an independent analytical backtest of pre-earnings straddles exists — [jakehanson GitHub](https://github.com/jakehanson/Pre-earnings-Straddle) (results not read)
- [US] Short event-vol regime risk: realized moves exceeded implied through the Q4-2025 season (straddles +45% avg vs −2% prior 12 quarters) — [ORATS](https://orats.com/blog/earnings-straddles-strong-season-2026)
- [US] Investors pay a substantial premium for event gamma risk when smiles are concave, but these names do realize larger EA moves and higher post-EA realized vol — tails are real — [Review of Finance](https://academic.oup.com/rof/article/29/4/963/8079062)
- [India, practitioner] Option sellers harvest the crush but carry gap risk; guidance-driven gaps in IT names can move stocks against headline beats — [FirstIndia](https://firstindia.co.in/news/press-releases/what-earnings-week-really-does-to-it-stock-options-1787138226)

### Inferences
- The distribution of short event-straddle P&L is negatively skewed; the engine should report tail metrics (CVaR, max single-event loss as multiple of premium, clustering of losses within a season) and season-level regime diagnostics rather than mean/Sharpe alone.
- "Buy the run-up" is most plausible only when the IV rise per day exceeds theta per day, i.e., close to the event with a short-dated expiry; on NSE (monthly stock expiries) the front option carries more diffusive theta, making it less favourable — an empirical question for the engine.
- Hedging variants (calendars: short front/long next-month; delta-hedged straddles; defined-risk iron flies) are natural ways to cap gap tails; Alexiou et al. already test delta-vega-neutral calendars.

### Gaps
- No quantitative study of "buy the run-up" returns on NSE stocks found.
- No published analysis of NSE event gaps (e.g., frequency of >2× implied moves) found.
- Full-text numbers for pre-event (e.g., −10 to −1 day) straddle returns from GXZ and BSIC not retrieved.
