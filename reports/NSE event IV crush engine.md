# Build the NSE event-volatility engine on point-in-time data

The best way to build this engine is as a point-in-time event-study platform first and a strategy backtester second. Its core job is to measure, for every scheduled NSE event, how much variance the option market priced in and how much the event actually delivered. Only after that should it decide which structure (short iron fly, calendar, run-up straddle, directional spread) monetises the gap after realistic Indian costs, margin and fills. That order matters because the evidence settles the *shape* of event volatility but not the *sign* of the edge. US data going back to 1979 and the one rigorous Indian study (IIM Ahmedabad, 2024) agree that IV rises steadily into an announcement and collapses after it. Whether selling that premium pays has flipped between regimes, though. US long straddles into earnings earned +3.34% in 1996–2013, lost money in 2011–2021, and returned roughly +45% in the late-2025 season. No published study measures NSE event-straddle profitability at all. Indian macro events show the same double edge. India VIX fell on every one of 15 Budget days until Budget 2026, when a surprise STT hike sent it up more than 17%. It fell about 30–34% on the 2014 and 2019 election results days and rose about 23–28% on the 2024 upset. Market structure changed at least eight times between November 2024 and April 2026: weekly expiries cut to Nifty only, a move to Tuesday expiries, new lot sizes, expiry-day margin add-ons and a 50% STT hike on option sales. A backtest that ignores these dates will quietly produce the wrong answer. The report below sets out the evidence, the methodology, the strategy rules and what remains unverified. It ends with a copy-paste Master Prompt for an AI coding agent.

## Crush is certain; whether selling it pays is not

The academic record leaves no doubt that option markets price scheduled announcements as lumps of variance. Patell and Wolfson documented systematic changes in Black-Scholes implied variance around earnings dates in 1979 ([IDEAS/RePEc](https://ideas.repec.org/a/eee/jaecon/v1y1979i2p117-140.html)). Dubinsky and Johannes then showed that adding a deterministic-date jump to option models **drastically reduces pricing errors**, and that anticipated earnings uncertainty is large, time-varying and informative about future realized volatility ([SSRN 600593](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=600593)). The anticipated jump inverts the short end of the term structure before the event. That inversion is what lets an engine back out event variance from two expiries ([Moontower](https://blog.moontower.ai/how-an-option-trader-extracts-earnings-from-a-vol-term-structure/); [CME Event Volatility Calculator](https://www.cmegroup.com/tools-information/quikstrike/event-volatility-calculator.html)).

The India evidence is thinner but consistent. Saurav, Agarwalla and Varma (IIMA, *American Business Review* 2024) used exact broadcast timestamps from NSE corporate announcements and near-month series expiring after the announcement. They found that single-stock **IV and skew rise monotonically before results and fall after**. Option volume relative to spot and futures follows the same pattern, and **pre-announcement skew and put-call volume ratio predict the sign of the surprise one day ahead** ([IIMA](https://www.iima.ac.in/publicationasymmetric-uncertainty-around-earnings-announcements-evidence-options-markets); [ABR](https://digitalcommons.newhaven.edu/americanbusinessreview/vol27/iss2/4/)). At the index level, Nifty options carry a **negative and significant variance risk premium**, and market-neutral Nifty straddles earn significantly negative excess returns ([IREF 2020](https://www.sciencedirect.com/science/article/abs/pii/S1059056020301222)). The premium also differs between overnight and intraday periods ([Papagelis, JFM 2025](https://onlinelibrary.wiley.com/doi/full/10.1002/fut.22589)). That split matters because Indian results often land after the close.

Profitability is where the evidence splits. Gao, Xing and Zhang found **ATM straddles bought three days before US earnings earned +3.34%**, concentrated in small, volatile, high-kurtosis, illiquid names ([SSRN 2204549](https://doi.org/10.2139/ssrn.2204549)). A Bocconi student-fund backtest of 2011–2021 found consistently negative returns for the same idea ([BSIC](https://bsic.it/straddling-outside-and-into-earnings-part-ii-2/)). ORATS reported that straddles averaged about −2% over twelve quarters, then **about +45% in the season to February 2026**, as realized moves exceeded implied ones ([ORATS](https://orats.com/blog/earnings-straddles-strong-season-2026)). Khan and Khan's T−1 to T+1 long straddle showed a Sharpe of 2.2. It also had **single-week losses of up to 83.8%** and excluded costs ([SSRN 4832160](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4832160)). Retail buyers lose **5–9% on average around announcements and 10–14% on high-expected-vol ones**, mostly to market makers ([de Silva, Smith & So](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4050165)). Concave pre-event smiles flag names where straddle and calendar returns are significantly lower, meaning the market already over-prices the event there ([Alexiou et al., RoF 2025](https://academic.oup.com/rof/article/29/4/963/8079062)). The engineering consequence follows directly. The engine must never report one pooled mean. It needs regime-sliced results, a filter that separates rich events from cheap ones, and tail metrics that expose the gap losses behind high win rates.

| Claim | Market | Strength | Source |
|---|---|---|---|
| IV rises into and collapses after earnings | US (1979–) | Peer-reviewed, replicated | Patell–Wolfson; Dubinsky–Johannes |
| Same run-up/crush, plus skew build-up, in NSE stock options | **India** | One peer-reviewed study | Saurav–Agarwalla–Varma 2024 |
| Nifty straddles lose on average (negative VRP) | **India** (index, not event-specific) | Peer-reviewed | IREF 2020 |
| Pre-event straddle +3.34% (1996–2013) | US only | Peer-reviewed | Gao–Xing–Zhang |
| Event straddles negative 2011–2021; ~−2% then +45% | US only | Practitioner | BSIC; ORATS |
| Long calendar best 1-day earnings strategy (+0.90% IS, +0.91% OOS, 3.9% of events) | US only | Vendor blog | ORATS |
| Size of NSE post-results crush, containment rate, straddle P&L | **Missing** | None found | — |

## India's historical event record already shows the regime flips

The request asks for backtested results on historical events. No public, statistically documented NSE event backtest exists yet, so producing that panel is the engine's first deliverable. The public record does, however, give a usable prior for macro events. It already shows where short-vol breaks.

| Event | Pre-event IV behaviour | Event-day outcome | Source |
|---|---|---|---|
| 15 Union Budgets to 2025 | VIX builds into Budget | **VIX fell on every Budget day, >9% on average** | [Arihant Plus](https://www.arihantplus.com/blogs/market-updates/union-budget-day-and-market-behaviour-15-year-trend-analysis) |
| Budget 2022 | VIX +6% to 21.95 on T−1 | VIX −5.11% intraday to 20.83 | [Business Standard](https://www.business-standard.com/amp/article/markets/india-vix-soars-6-to-21-95-a-day-ahead-of-union-budget-122013101779_1.html) |
| Budget 23 Jul 2024 | — | Nifty −0.12% after a 405-pt intraday recovery; **VIX −17.42% to 12.75** | [Business Standard](https://www.business-standard.com/amp/markets/capital-market-news/market-ends-with-tiny-cuts-fmcg-shares-rally-vix-tanks-17-124072300954_1.html) |
| Budget 1 Feb 2026 (Sunday) | VIX +3.66% to 13.86 in run-up | STT hike; **Nifty −1.96%, VIX +17% to 15.66** | [Business Standard live](https://www.business-standard.com/markets/news/stock-market-live-updates-february-1-union-budget-2026-nirmala-sitharaman-speech-sensex-nifty-share-market-today-126020100067_1.html) |
| 2014 exit polls / results | VIX at 5-yr high | Exit-poll day VIX −23.88%; results day ~−34% | [Business Standard](https://www.business-standard.com/article/markets/vix-heads-towards-biggest-slump-in-over-4-1-2-years-114051300385_1.html); [BS](https://www.business-standard.com/amp/article/news-ians/volatility-index-drops-by-another-16-119052400614_1.html) |
| 2019 results | VIX ~30 on T−1 | ~−30% on results day | [Business Standard](https://www.business-standard.com/article/news-ians/sensex-ends-140-pts-higher-vix-at-4-yr-high-119052201155_1.html) |
| 4 Jun 2024 results (upset) | VIX >20 through polling | **Nifty −5.9%; VIX +23–28%** | [BusinessToday](https://www.businesstoday.in/markets/market-commentary/story/election-results-2024-india-vix-jumps-india-alliance-exceeds-expectations-432101-2024-06-04) |
| RBI, 4 May 2022 (unscheduled hike) | None (unscheduled) | Nifty −2.29% | [BusinessToday](https://www.businesstoday.in/markets/stocks/story/sensex-crashes-900-points-nifty-falls-as-rbi-hikes-repo-rate-332270-2022-05-04) |
| RBI, 6 Jun 2025 (50 bp + CRR surprise) | — | BankNifty record, ~+1.5%; VIX −1.47% | [BusinessToday](https://www.businesstoday.in/amp/markets/stocks/story/nifty-bank-hits-record-high-after-rbi-rate-cuts-banking-financial-stocks-rally-479278-2025-06-06) |
| Sun Pharma USFDA warning letter, Dec 2015 | — | Stock −4.5% | [Business Standard](https://www.business-standard.com/article/pti-stories/sun-pharma-shares-dip-4-5-on-warning-letter-from-usfda-115122100694_1.html) |

Read together, the table shows three event classes. **Budget days and "expected" election outcomes behave like classic crush events.** One practitioner backtest of a Nifty monthly short straddle into the Budget reports a **79% win rate and an outlier-adjusted profit factor of 2.06**, but its sample years and entry/exit rules are unknown ([Options IQ](https://optionsiq.substack.com/p/nifty-short-straddle-performance)). **Policy surprises aimed at market participants (Budget 2026's STT hike) and electoral upsets (2024) invert the crush.** The 2024 gap was roughly three to four times the move implied by a mid-20s VIX. **RBI decisions are small-vol events for Nifty**: VIX changes on policy day usually stay within ±5%, and the August 2026 policy left VIX at about 12.0–12.5 ([HDFC Sky](https://hdfcsky.com/news/india-vix-slips-3-12-percent-as-rbi-policy-wait-keeps-volatility-contained-august-5-2026)). The implication is that the "event premium" on RBI day is often too thin to pay Indian costs. Exogenous shocks such as the yen-carry unwind (5 Aug 2024, VIX up nearly 62% intraday) and the April 2025 tariff day (+57% close) are not scheduled events. They are the tail that sizing must survive ([BIS Bulletin 90](https://www.bis.org/publ/bisbull90.pdf); [Business Standard](https://www.business-standard.com/amp/markets/news/india-vix-logs-biggest-single-day-jump-signals-rocky-road-ahead-125040701001_1.html)).

Evidence is missing on India VIX behaviour around US FOMC, US CPI and Indian CPI/GDP. It is also missing on single-stock IV around mergers, splits, index inclusions and USFDA actions, beyond price reactions. MSCI and index rebalances look like closing-auction liquidity events rather than volatility events: the August 2026 MSCI rebalance set a record ₹39,718 crore closing-auction turnover, but that figure came from a snippet with no URL, so treat it as unconfirmed. The engine should therefore build these event classes as **hypothesis tests with no presumed edge**.

## Eight regime breaks since November 2024 rewrite NSE trade design

A 2026 NSE event engine operates in a market that differs materially from the one most Indian retail backtests were built on. Since 20 Nov 2024, NSE lists **weekly options only on Nifty 50**, and BSE only on Sensex. BankNifty, FinNifty and MidcpNifty now have monthly options only; their last weeklies expired 13–19 Nov 2024 ([Motilal Oswal](https://www.motilaloswal.com/learning-centre/2024/10/nse-discontinues-weekly-derivatives-on-bank-nifty-nifty-midcap-select-and-finnifty)). Single-stock options were always monthly ([NiftyDesk](https://niftydesk.app/blog/sebi-new-fno-rules-2026-guide)). Since 1 Sep 2025, **NSE contracts expire on Tuesday** (Nifty weekly each Tuesday, monthlies on the last Tuesday) and BSE contracts on Thursday ([News On AIR](https://www.newsonair.gov.in/nse-bse-swap-derivatives-expiry-days)). From the January 2026 series, index lots are **Nifty 65, BankNifty 30, FinNifty 60, MidcpNifty 120, NiftyNxt50 25** ([NSE circular FAOP70616](https://nsearchives.nseindia.com/content/circulars/FAOP70616.pdf)), and Sensex is 20 ([Sahi](https://www.sahi.com/blogs/nifty-lot-size-2026-bank-nifty-sensex)).

The margin changes land squarely on event trades. Short options carry an **extra 2% ELM on expiry day from 20 Nov 2024** ([Fyers](https://fyers.in/notice-board/sebi-announces-significant-reforms-in-equity-index-derivatives-framework/)). Some sources say this applies to all short options and others to short *index* options only, which is an unresolved conflict. Buyers pay full premium upfront from 1 Feb 2025. **Calendar spreads lose their margin benefit on the near leg's expiry day from 10 Feb 2025**, and one broker says the removal starts at 4 PM the day before ([ICICI Direct](https://www.icicidirect.com/futures-and-options/articles/calendar-spreads-in-f-o-after-sebi-s-new-rules-what-you-need-to-know)). Stock F&O positions open at expiry settle physically. Margin on ITM short options and futures rises toward 40% of contract value or SPAN+exposure, whichever is higher, and reaches full delivery margin by expiry ([Angel One](https://www.angelone.in/knowledge-center/derivatives/settlement-procedure); [Zerodha Varsity](https://zerodha.com/varsity/chapter/quick-note-on-physical-settlement-2/)). Delta-based OI, a new MWPL (lower of 15% of free float or 65× average daily cash volume) and a ₹5,000 crore intraday net FutEq limit came in from 1 Oct 2025 ([Business Today](https://www.businesstoday.in/markets/story/sebi-equity-fo-rules-futeq-method-mwpl-risk-management-478321-2025-05-29); [Business Standard](https://www.business-standard.com/markets/news/sebi-stricter-intraday-position-limits-options-market-regulation-125090200971_1.html)). An F&O pre-open session started in December 2025. A September 2026 SEBI consultation proposes a VWAP-blended derivative settlement price; it is not in force ([Dynamite News](https://www.dynamitenews.com/business/sebis-big-fo-move-new-expiry-rules-could-change-trading-forever), secondary source).

Costs moved against sellers too. From **1 Apr 2026, STT is 0.15% of premium on option sales (up from 0.10%), 0.15% of intrinsic value on exercised options (up from 0.125%) and 0.05% on futures** ([Upstox](https://upstox.com/news/personal-finance/tax/explained-how-the-stt-hike-on-equity-futures-and-options-affects-traders-and-investors/article-189260/); [Motilal Oswal](https://www.motilaloswal.com/learning-centre/2026/2/union-budget-2026-27-stt-update-and-market-impact-analysis)). The NSE option transaction charge is **₹35.03 per lakh of premium (0.03503%)** from 1 Oct 2024, though a later circular (FA73061) may have revised it ([NSE intimation](https://nsearchives.nseindia.com/corporate/BSE_27092024184037_NSEintimation.pdf); [NSE FA73061](https://nsearchives.nseindia.com/content/circulars/FA73061.pdf)). Because STT falls only on the sell leg, **the 2026 hike taxes short-vol crush trades more than long-vol run-up trades**. Exercise STT and close-out STT now carry the same rate, so the old "STT trap" on ITM expiry is gone.

The design consequences are concrete. Stock-results crush trades must use **monthly options that often carry one to four weeks of non-event diffusion**. That dilutes the crush and makes accurate separation of diffusive variance essential. BankNifty, the natural RBI instrument, now has only monthly options. **Nifty weeklies (Tuesday) and Sensex weeklies (Thursday) are the only short-dated macro instruments.** Events that fall in expiry week collide with the expiry-day ELM, the loss of calendar-spread margin benefit and physical-delivery margin, so the default is to **exit stock-option event trades before expiry-day T−1**.

The data layer is workable but uneven. The free NSE F&O bhavcopy moved to the **UDiFF format on 8 Jul 2024**, and a community archive holds validated files from April 2020 to August 2026 ([GitHub NSE-FNO-Data-bank](https://github.com/SantoshSrinivas79/NSE-FNO-Data-bank)). Intraday history for expired options comes from the **Dhan Expired Options Data API** (rolling five years, ATM ±10 strikes, with IV and OI) ([DhanHQ](https://dhanhq.co/docs/v2/expired-options-data/)) and **Upstox's Expired Historical Candle API** (1-minute to daily bars, Plus plan) ([Upstox](https://upstox.com/developer/api-documentation/get-expired-historical-candle-data/)). Kite Connect historically did not serve expired-option candles ([Kite forum](https://kite.trade/forum/discussion/14374/how-to-fetch-candlestick-data-for-expired-options)). **None of these retail sources provides historical bid/ask quotes.** Quote-aware fills therefore need a paid vendor (GDFL, TrueData, TickData), self-recorded snapshots, or a modelled spread that is explicitly labelled. Results dates come from NSE board-meeting and announcement pages, which have no official API ([NseIndiaApi](https://bennythadikaran.github.io/NseIndiaApi/api.html)). The RBI publishes the MPC calendar each year; FY27 runs from 6–8 Apr 2026 to 3–5 Feb 2027 ([Angel One](https://www.angelone.in/news/economy/rbi-releases-mpc-meeting-calendar-for-fy27-what-you-need-to-know)). For the risk-free rate, **India VIX itself uses tenor-matched NSE MIBOR**, which makes MIBOR the exchange-consistent choice ([NSE India VIX methodology](https://nsearchives.nseindia.com/web/sites/default/files/inline-files/India_VIX_comp_meth.pdf)).

## Total-variance arithmetic isolates the event from the diffusion

The pricing core should follow India VIX's own conventions. India VIX uses **the same-expiry Nifty futures price as the forward** and fills bad quotes with a natural cubic spline ([ICICI Direct](https://www.icicidirect.com/faqs/fno/how-is-india-vix-computed)). The engine should therefore price with **Black-76 on the matching futures or a put-call-parity implied forward**, which removes explicit dividend and repo inputs. It should invert prices with **Jäckel's "Let's Be Rational"**, available vectorised in py_vollib_vectorized ([GitHub](https://github.com/marcdemers/py_vollib_vectorized)), with newer GPU libraries such as fast-vollib as an option ([arXiv 2604.27210](https://arxiv.org/html/2604.27210v1)). It should fit **SSVI**, whose Gatheral–Jacquier conditions exclude calendar and butterfly arbitrage across the whole surface ([Gatheral & Jacquier](https://www.imperial.ac.uk/media/imperial-college/research-centres-and-groups/stochastic-analysis-group/preprints-2012/12-11.pdf)). A shared ρ and φ across expiries matters on NSE, where many stock chains have only three to eight liquid strikes. Constant-maturity ATM IV is interpolated in **total variance w = σ²T, linearly in time**. It is never interpolated in σ, and the event-containing expiry is flagged so that the CM series does not jump when the event rolls off.

Event variance then follows from additivity ([FlashAlpha](https://flashalpha.com/articles/volatility-term-structure-contango-backwardation-events)). Take two expiries T1 < T2 that both span the event, with a common diffusive vol σ_d. Then σ_i²T_i = σ_d²T_i + σ_E², which gives **σ_E² = T1·T2·(σ1² − σ2²)/(T2 − T1)** and σ_d² = (σ2²T2 − σ1²T1)/(T2 − T1). If σ1 ≤ σ2 there is no inversion: the estimate is clipped to zero and flagged. For NSE stocks the pair is current-month and next-month, which is **structurally the primary tool** because no weeklies exist. The straddle shortcut gives mean absolute move ≈ straddle/F, with 1σ ≈ 1.2533 × straddle/F, since straddle ≈ √(2/π)·σ·√T·F ([Brilliant](https://brilliant.org/wiki/straddle-approximation-formula/)). The residual diffusive days are stripped out with σ_E² ≈ (1.2533·straddle/F)² − σ_d²·T. Run-up is the front ATM IV change from T−N to the last pre-event snapshot (N = 5, 10, 20). Crush is the change from that snapshot to the first post-event close, measured on both a fixed-strike and an ATM-forward basis, and compared with the model-predicted post-event vol √((σ1²T1 − σ_E²)/T1′). The key outcome is **R = |ln(S_post/S_pre)| ÷ implied move**. IV rank must use ex-event (diffusive) IV, otherwise every pre-results date looks "high rank". These formulas are standard algebra consistent with Dubinsky–Johannes. Their exact day-count conventions were not verified from full text.

Event timing is the single easiest place to corrupt the study. Indian companies release results during market hours or in the evening. Every event therefore needs an announcement timestamp, a pre-market/intraday/post-market flag, and a `first_seen_ts` recording when the date became known. The reaction session is T+1 for post-market releases and T for intraday ones. The IIMA study took exact broadcast times from NSE announcement pages for this reason ([ABR PDF](https://digitalcommons.newhaven.edu/cgi/viewcontent.cgi?article=2897&context=americanbusinessreview)). Corporate actions follow NSE's rules. Strikes and lots are adjusted after close on the last cum-date. Dividends **below 2% of market value are "ordinary" and not adjusted**. Splits and bonuses scale lot up and strike down so that contract value is unchanged ([m.Stock](https://www.mstock.com/articles/corporate-actions-fo-contracts); [NSE](https://www.nseindia.com/static/products-services/equity-derivatives-corporate-actions-adjustments)). The contract master must therefore be versioned by validity date, the raw table kept immutable, and a dated F&O-eligibility table maintained so that stocks later dropped from F&O stay in the history.

## Selection rules turn event richness into a structure choice

The practitioner consensus screens on a small set of inputs: the implied-to-historical move ratio, the event premium over ex-event IV, the front/back term slope, IV rank and liquidity. It then **filters hard**. ORATS's profitable earnings calendar traded only **3.9% of possible announcements** ([ORATS](https://orats.com/blog/earnings-options-strategies-backtest); [ORATS HV forecasts](https://orats.com/blog/how-to-use-hv-forecasts)). The evidence also warns that high win rates hide outliers. Option Alpha's 20-day pre-earnings straddle became **unprofitable once the top 10 of 1,205 trades were removed** ([Option Alpha](https://optionalpha.com/podcast/long-straddle-earnings-option-strategy)). An independent replication of a tastylive iron-fly result produced a 55% win rate and a −$8 average, against the published 70% and +$61 ([Option Alpha community](https://optionalpha.com/community/posts/0-dte-backtest-tasty-gives-completely--202508077174)). Position size alone turned one iron-condor backtest from −67% to +6.86% ([Option Alpha](https://optionalpha.com/podcast/iron-condor-backtest)). The table below is a synthesis to be calibrated on NSE data; none of its thresholds is a published Indian rule.

| Condition (at last pre-event snapshot) | Default structure | Entry / exit | India-specific note |
|---|---|---|---|
| Implied/historical-median move > ~1.2–1.3, liquid ATM, front ≥ ~5 DTE after event | **Short iron fly** (iron condor if fat tails) | Enter T−1 close (or pre-announcement for intraday events); exit first liquid post-event print or T+1 close | Defined risk sharply cuts SPAN; avoid naked straddles on physically settled stocks |
| Rich premium and front/back IV > ~1.1–1.2 | **Long calendar / double calendar** (short event month, long next) | Enter T−1; exit T+1 | Front leg must not expire on/near event (loss of margin benefit on expiry day); next-month liquidity gate |
| Implied/historical < ~0.8, high kurtosis or volatile surprise history | **Long straddle/strangle held through** | Enter T−3 to T−1; exit T+1 | GXZ edge concentrated in illiquid names where spreads may erase it |
| Strong historical run-up, event early in series (~20+ DTE) | **Run-up straddle or run-up calendar** | Enter T−7 to T−3; **exit T−1**, never hold through | Monthly-only stocks carry more theta; the run-up calendar is the lower-theta version |
| Skew/PCR signal plus directional conviction | **Debit vertical, broken-wing fly, jade lizard** | Enter T−1; exit T+1 | Skew predicts surprise sign on NSE (IIMA); naked risk reversals margin-heavy |
| Budget, election results, policy surprise risk | **Wide, small iron condor or calendar**, or run-up only | Exit before results for run-up | Budget 2026 and 2024 results broke the crush |
| RBI, CPI, FOMC on Nifty | **Short Nifty weekly iron fly/condor** only if premium clears costs | T−1 / morning of; exit post-announcement or next open | FOMC lands overnight IST, so gap risk has no adjustment window; defined risk is mandatory |
| Implied/historical 0.8–1.2 or liquidity fails | **No trade** | — | Default outcome for most events |

Risk rules follow from negatively skewed P&L. Cap max loss per event at about 0.5–2% of capital and use fractional Kelly of at most ¼. Cap sector concentration, since Indian results cluster by sector in mid-January, April–May, July–August and October–November. Stress every short position with the stock's own historical maximum gap. Sinclair's warning applies here: a correctly identified overpriced straddle still loses badly on a single large move ([Moontower](https://blog.moontower.ai/hard-earned-trading-wisdom/)).

## Clustered events and serial trials demand stricter statistics

Earnings seasons put dozens of events on the same date, so cross-sectional residuals are correlated. Standard errors must be **clustered by event date (or two-way by firm and date)**, and bootstraps must resample whole event-dates. The engine should apply **Harvey–Liu–Zhu's t > 3.0 hurdle** for any newly "discovered" signal ([RFS 2016](https://academic.oup.com/rfs/article/29/1/5/1843824)). The headline Sharpe should be the **Deflated Sharpe Ratio**, which corrects for the number of trials and for skew and kurtosis ([Bailey & López de Prado](https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf)). Report **PBO** via CSCV ([Bailey et al.](https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf)), and use purged, embargoed and combinatorial CV for any tuned model ([QuantInsti](https://blog.quantinsti.com/cross-validation-embargo-purging-combinatorial/)). This requires a trial registry that logs every configuration ever run. A realistic sample of about 180–200 F&O stocks × 4 results a year × ~10 years is only 7–8k events, so feature counts and hyperparameter searches must stay small.

Fill realism outranks model sophistication. The engine should fill at bid/ask, or at mid ± α·half-spread with α calibrated, and never at LTP or settle on illiquid strikes. Post-event opens should be simulated with widened spreads. Results should be reported separately for sub-periods before and after each regime break. An event-driven portfolio layer (NautilusTrader has first-class options and is actively released ([docs](https://nautilustrader.io/docs/latest/concepts/options/))) should sit on top of a vectorised event-trade ledger built with polars and DuckDB. QuantLib, released quarterly with v1.42 in April 2026, serves as the independent pricing check ([libraries.io](https://libraries.io/pypi/QuantLib)).

## Conclusion

The central insight is that event IV crush on NSE is a *measurement* problem before it is a *trading* problem. The crush itself is near-certain, but the edge depends on whether the implied move exceeded what the event delivered, net of an Indian cost and margin stack that got more expensive for sellers in April 2026. The engine's most valuable output will not be a strategy. It will be the first clean NSE panel of event variance, run-up, crush and realized/implied ratios. That panel is the evidence gap that every Indian practitioner claim currently papers over. Expect it to show thinner edges on RBI and CPI days than retail lore suggests, richer but fat-tailed premia on Budget and election days, and a stock-results edge concentrated in a filtered minority of liquid names.

Two further points follow from the evidence. Structural changes since 2024 (monthly-only BankNifty, Tuesday expiries, expiry-day margin add-ons) have shifted the natural instrument for many events from weekly straddles to defined-risk monthlies and calendars. US calendar evidence will only partly transfer, because NSE's roughly 30-day gap between monthly legs means the back leg also carries the event. And because every regulatory and cost figure here came through secondary coverage or blocked primary pages, verification against NSE and SEBI circulars is a design requirement, not a formality. It belongs in the engine's configuration layer, with effective dates.

## Evidence flags at a glance

| Category | Items |
|---|---|
| **US-only evidence** | Pre-event straddle premium (GXZ); regime flips (BSIC, ORATS); calendar superiority (ORATS); run-up theta dominance (Khan & Khan); retail overpayment (de Silva et al.); concave-smile signal (Alexiou et al.); bellwether premia (Barth & So); 70–75% containment in implied move (practitioner) |
| **Indian evidence missing** | Average NSE post-results crush size; implied-vs-realized containment rates; stock-event straddle/calendar/iron-fly P&L; run-up magnitude T−10→T−1; IV around RBI/CPI/FOMC; IV around USFDA, M&A, splits, index inclusions; stock-option bid/ask spreads; naked vs iron-fly margin ratios; India VIX half-life |
| **Unverified figures** | Stock options European-style (widely stated, not confirmed from a circular); strike-interval scheme; stamp duty 0.003% and SEBI fee ₹10/crore; current NSE transaction charge after FA73061; whether expiry-day +2% ELM applies to all short options or index only; delivery-margin schedule; exposure-margin %; RBI announcement ~10:00 IST; CPI release 12th at 16:00 IST; Budget on 1 Feb by convention; India VIX methodology after the Tuesday/weekly changes; status of the Sept 2026 SEBI VWAP-settlement consultation; Options IQ backtest period and rules; 2024 results-day VIX (+23% vs +27.7%) |

## Master Prompt

Copy everything inside the block below and give it to an AI coding agent.

```text
=====================================================================
MASTER PROMPT — NSE EVENT VOLATILITY RESEARCH & BACKTESTING ENGINE
=====================================================================

ROLE / PERSONA
You are a senior quantitative developer and derivatives researcher with
institutional experience building options research platforms (vol surface
construction, event studies, backtesting infrastructure) for Indian NSE F&O.
You write production-quality, typed, tested Python. You are sceptical of
backtest results, you never fill at prices that could not have been traded,
and you treat every regulatory or cost figure as configuration that must be
verified against a primary NSE/SEBI source with an effective date.

---------------------------------------------------------------------
0. KICKOFF — GRILL ME BEFORE YOU BUILD (MANDATORY)
---------------------------------------------------------------------
Before writing any code, run a grilling session with me:
 - Interview me relentlessly about every aspect of this plan until we
   reach a shared understanding. Walk down each branch of the design
   tree, resolving dependencies between decisions one by one.
 - Ask ONE question at a time and wait for my answer before the next.
   For every question, give your recommended answer and a one-line why.
 - If a FACT can be found by reading this prompt, the repo, docs or a
   primary source, look it up instead of asking me. The DECISIONS are
   mine: put each one to me and wait.
 - Do NOT start M0 until I confirm we have reached a shared understanding.
Branches to cover (in dependency order; add any you find):
  1. Purpose and end user: personal research, a desk tool, or a
     product; is live trading ever in scope?
  2. Capital, max loss per event, max concurrent events, risk appetite
     for undefined-risk structures.
  3. Event priority for the first release (results only? + RBI/Budget/
     elections? which "other" classes, if any).
  4. Universe: which stocks/indices; minimum liquidity; history depth.
  5. Data budget and vendors: EOD bhavcopy only vs Dhan/Upstox intraday
     vs a paid quote vendor (GDFL/TrueData); whether to start recording
     live quote snapshots now.
  6. Announcement-timestamp source and how much manual cleaning I accept.
  7. Default fill tier and spread model when no bid/ask exists.
  8. Margin model: approximate SPAN grid vs NSE SPAN files.
  9. Which strategies ship first; which selection thresholds are fixed
     priors vs calibrated.
 10. Statistical bar: holdout length, t-threshold, DSR/PBO gates for
     calling a result "real".
 11. Tech stack and runtime: local machine vs cloud, storage size,
     Streamlit vs other UI, scheduling.
 12. Verification ownership: who confirms each UNVERIFIED item in
     section 16 and how blocking it is.
Record every answer in docs/DESIGN_DECISIONS.md (question, options,
decision, rationale, date) and treat it as binding config. Where an answer
conflicts with this prompt, the answer wins; note the change. At the start
of each later milestone, run a short grilling round on any new decisions
that milestone raises before coding it.

---------------------------------------------------------------------
1. OBJECTIVES
---------------------------------------------------------------------
Build, end to end, a point-in-time research and backtesting engine that:
 (a) Builds a clean historical panel of scheduled events on NSE F&O
     underlyings (stocks and indices) with exact announcement timestamps.
 (b) For every event measures: implied move, extracted event variance,
     pre-event IV run-up, post-event IV crush, realized move, and the
     realized/implied ratio, plus context (IV rank on ex-event IV, skew,
     term slope, liquidity).
 (c) Backtests a library of option structures around each event with
     realistic fills, full Indian cost stack, SPAN-like margin, liquidity
     gates and India-specific settlement/expiry rules.
 (d) Produces statistically honest results (event-date clustering,
     deflated Sharpe, PBO, walk-forward) sliced by event type, regime,
     sector and liquidity bucket.
 (e) Outputs, for any upcoming event, a ranked recommendation of which
     structure (or NO TRADE) to use, with entry/exit timing, expected P&L
     distribution, tail risk, margin and the historical evidence behind it.
The engine is a research tool first. Live order routing is out of scope
(optionally stub an OpenAlgo/broker adapter for paper snapshots only).

---------------------------------------------------------------------
2. SCOPE
---------------------------------------------------------------------
Markets: NSE equity derivatives (single-stock options and futures; index
options/futures on NIFTY, BANKNIFTY, FINNIFTY, MIDCPNIFTY, NIFTYNXT50).
Optional: BSE SENSEX weeklies (Thursday expiry) as a second macro
instrument. India VIX as a context series.
Event types (each an enum with its own session/timing rules):
  CORPORATE_RESULTS   quarterly/annual results (board meeting outcome)
  RBI_MPC             scheduled policy decisions (+ flag unscheduled actions)
  UNION_BUDGET        incl. interim budgets and weekend special sessions
  ELECTION            sub-events: POLL_PHASE, EXIT_POLL, RESULTS (general
                      and major state elections)
  CPI_INDIA, GDP_INDIA
  US_FOMC, US_CPI     (announce in Indian night hours -> next-open gap)
  INDEX_REBALANCE     Nifty/Sensex/MSCI/FTSE inclusion/exclusion effective
  USFDA_ACTION        warning letters, OAI/EIR, import alerts (pharma)
  CORP_ACTION         split, bonus, special dividend, merger/demerger record
  OTHER_SCHEDULED     AGMs, analyst days, tariff decisions, court rulings
Treat all non-earnings, non-Budget/election classes as HYPOTHESIS TESTS with
no presumed edge: there is no published evidence on NSE single-stock IV
around USFDA/M&A/splits/rebalances, or on India VIX around CPI/FOMC.

---------------------------------------------------------------------
3. DATA LAYER AND SOURCES
---------------------------------------------------------------------
EOD options/futures:
  - NSE F&O bhavcopy. Legacy CSV before 8 Jul 2024; UDiFF "Common
    Bhavcopy" from 8 Jul 2024. URL pattern (verify):
    https://archives.nseindia.com/content/fo/BhavCopy_NSE_FO_0_0_0_YYYYMMDD_F_0000.csv.zip
  - Community archive github.com/SantoshSrinivas79/NSE-FNO-Data-bank
    (Apr 2020 - Aug 2026) for bootstrap; validate against NSE.
  - Libraries: jugaad-data, nselib, nsepython (fragile scrapers; EOD only;
    rate-limit and cache aggressively).
  - Bhavcopy has NO bid/ask. Close is often stale for illiquid strikes;
    prefer settle with volume/OI filters and flag staleness.
Intraday (event windows):
  - Dhan Expired Options Data API (rolling 5 yrs, ATM +/-10 strikes,
    OHLC, IV, OI, spot; 1/5/15/25/60-min).
  - Upstox Expired Instruments + Expired Historical Candle API (1-min to
    daily; Plus plan).
  - Kite Connect does not (historically) serve expired option candles.
Quotes (bid/ask): paid vendor (GDFL, TrueData, TickData) or self-recorded
  live snapshots going forward. If unavailable, use a MODELLED spread
  (function of moneyness, DTE, premium, underlying liquidity) fitted on
  whatever quote snapshots exist, and label every result that uses it.
Spot/index: NSE equity bhavcopy, index history, India VIX history (NSE).
Rates: NSE MIBOR matched to tenor (India VIX convention); 91-day T-bill as
  fallback.
Corporate actions: NSE corporate-action adjustment circulars / NSE Clearing.
Contract master / lot sizes: NSE fo_mktlots archive and circulars
  (e.g. FAOP70616 for Jan 2026 index lots).
F&O universe history: NSE entry/exit circulars; build dated membership.
Event calendars:
  - Results: NSE board-meeting page + corporate announcements (use the
    filing TIMESTAMP of the outcome, not just the meeting date); BSE as
    cross-check. Snapshot scraped calendars daily to capture revisions.
  - RBI MPC annual calendar (RBI press release); FY27: 6-8 Apr 2026 ...
    3-5 Feb 2027 (verify intermediate dates).
  - MOSPI advance release calendar (CPI/GDP); Union Budget dates (MoF);
    ECI schedules; US Fed FOMC calendar; BLS CPI calendar;
    NSE Indices / MSCI / FTSE rebalance notices; USFDA warning-letter
    database and company disclosures.
  - Consensus/surprise labels (optional): Reuters/ET polls for RBI.

---------------------------------------------------------------------
4. POINT-IN-TIME (BITEMPORAL) DATA MODEL
---------------------------------------------------------------------
Storage: Parquet partitioned by trade_date/underlying; query with DuckDB and
polars. Raw tables are IMMUTABLE; adjusted views are derived.
Every row carries valid_from/valid_to (business time) and
recorded_at/first_seen_ts (knowledge time).

contract_master        token, underlying, instrument_type, expiry_date,
                       expiry_rule_id, strike_raw, strike_adj_factor,
                       lot_size, option_type, exercise_style,
                       settlement_type {CASH, PHYSICAL}, tick_size,
                       valid_from, valid_to, source_circular
expiry_calendar        underlying, expiry_date, is_weekly, is_monthly,
                       weekday, holiday_shifted_flag, regime_id
lot_size_history       underlying, lot_size, effective_series, valid_from,
                       valid_to, source_circular
strike_scheme_history  underlying, strike_interval rules by moneyness/
                       tenor, valid_from, valid_to, source
corporate_actions      symbol, ex_date, last_cum_date, type, ratio,
                       dividend_amt, pct_of_mkt_value, nse_adjusted(bool,
                       >=2% dividend rule), strike_factor, lot_factor
fo_universe            symbol, in_fo_from, in_fo_to, exit_reason
option_quotes          ts, token, bid, ask, bid_qty, ask_qty, ltp, open,
                       high, low, close, settle, volume, oi, source_flag
                       {EOD_BHAV, INTRADAY_BAR, QUOTE_SNAPSHOT}, stale_secs
futures_quotes, spot_quotes, india_vix, rates_curve
events                 event_id, symbol_or_index, event_type, sub_type,
                       scheduled_date, announce_ts (IST, to the minute),
                       session_flag {PRE_MARKET, INTRADAY, POST_MARKET,
                       NON_TRADING_DAY, UNKNOWN}, reaction_session_date,
                       fiscal_period, is_scheduled, first_seen_ts,
                       revised_from, source_url, surprise_label(optional)
regime_breaks          regime_id, date, description, source
margin_params          date, underlying, span_file_ref, exposure_pct,
                       elm_expiry_addon, calendar_benefit_rules
cost_params            effective_from, effective_to, component, rate,
                       basis, side, verified(bool), source_url
trial_registry         trial_id, timestamp, config_hash, params, dataset
                       version, metrics  (EVERY backtest run is logged)

Rules:
 - Reaction session: POST_MARKET (>=15:30 IST) -> next trading session;
   PRE_MARKET/INTRADAY -> same session; NON_TRADING_DAY (e.g. Sunday Budget
   1 Feb 2026, Saturday Budgets 2020/2025 were special sessions) -> handle
   explicitly. The pre-event snapshot is the last print BEFORE announce_ts.
 - Never use an event date whose first_seen_ts is after the decision time.
 - Corporate actions: NSE adjusts strike and lot after close on last
   cum-date; dividends <2% of market value are NOT adjusted. Split/bonus
   scale lot up and strike down (contract value unchanged). P&L always on
   the contracts actually traded; adjusted views only for analytics.
 - Survivorship: universe on each date = fo_universe membership on that
   date, including later-delisted names.
 - Known regime breaks to seed (verify each):
     2024-07-08 UDiFF bhavcopy format
     2024-10-01 STT options sell 0.10%, fut 0.02%; NSE txn charge flat
                0.03503% of premium
     2024-11-20 one weekly benchmark per exchange (NSE: NIFTY only);
                +2% ELM on short options on expiry day; min contract
                value ~Rs15 lakh
     2025-02-01 full upfront premium collection
     2025-02-10 no calendar-spread margin benefit on expiry day
     2025-04    intraday position-limit monitoring
     2025-09-01 NSE expiries move to Tuesday (monthly = last Tuesday);
                BSE Thursday
     2025-10-01 delta-based OI; new MWPL (min of 15% free float, 65x ADV);
                Rs5,000 cr intraday net FutEq limit (index)
     2025-12    F&O pre-open session; expiry-day breach penalties
     2026-01    index lots: NIFTY 65, BANKNIFTY 30, FINNIFTY 60,
                MIDCPNIFTY 120, NIFTYNXT50 25 (weeklies from 6 Jan 2026
                expiry, monthlies from 27 Jan 2026 expiry); SENSEX 20
     2026-04-01 STT: options sell 0.15% of premium; exercised 0.15% of
                intrinsic; futures 0.05%
     2026-09    SEBI consultation on VWAP-blended settlement price
                (PROPOSAL; make settlement-price rule pluggable)

---------------------------------------------------------------------
5. IV / PRICING METHODOLOGY
---------------------------------------------------------------------
 - Model: Black-76 on the forward. C = D[F N(d1) - K N(d2)],
   d1 = [ln(F/K) + sigma^2 T/2]/(sigma sqrt T), d2 = d1 - sigma sqrt T,
   D = exp(-rT). Put by parity.
 - Forward: same-expiry futures price (India VIX convention) AND
   put-call-parity implied forward: regress (C - P) on K over near-ATM
   strikes with tight spreads to get D and F. Log the gap
   F_implied - F_futures; large gaps flag stale data or dividend/borrow.
   BSM with discrete dividends only as a fallback.
 - Rate: tenor-matched NSE MIBOR (fallback 91-day T-bill).
 - Time: trading-minute or business-day time using the NSE holiday
   calendar; store both calendar-year and business-day T.
 - Solver: Jaeckel "Let's Be Rational" (py_vollib_vectorized or vendored
   implementation; optional fast-vollib GPU backend). Prices below
   intrinsic or above the forward bound -> NaN (never zero vol).
   Cross-check a random sample against QuantLib.
 - Quote hygiene: OTM only (puts K<F, calls K>F); drop zero bid,
   spread/mid > threshold (30-50%), stale prints, OI/volume below
   threshold, premium < few ticks (tick Rs0.05).
 - Surface: SSVI (Gatheral-Jacquier) across expiries, parameterised by ATM
   total variance theta_t, rho, phi(theta); enforce no calendar/butterfly
   arbitrage. For thin stock chains share rho/phi across expiries or fit in
   delta space; weight by 1/spread or vega. Fall back to per-slice
   quadratic smile with a quality flag.
 - Constant-maturity ATM IV: interpolate TOTAL VARIANCE w = sigma^2 T
   linearly in T at ATM-forward (k = 0). Never interpolate sigma. Tag
   whether the bracketing expiries contain the event; also produce an
   ex-event CM IV using sigma_d.
 - Greeks: Black-76 on the fitted surface; used for attribution.

---------------------------------------------------------------------
6. EVENT METRICS (compute per event, store in event_metrics table)
---------------------------------------------------------------------
Notation: sigma_i ATM IV of expiry i, T_i year fraction, sigma_d
diffusive vol, sigma_E^2 event (one-day jump) variance.
 - Additive model: sigma_i^2 T_i = sigma_d^2 T_i + sigma_E^2
 - Two-expiry extraction (both expiries span the event; for NSE stocks
   = current month vs next month):
     sigma_d^2 = (sigma_2^2 T_2 - sigma_1^2 T_1) / (T_2 - T_1)
     sigma_E^2 = T_1 T_2 (sigma_1^2 - sigma_2^2) / (T_2 - T_1)
   If sigma_1 <= sigma_2: set sigma_E^2 = 0 and flag NO_INVERSION.
 - Straddle-implied move: mean-abs move = (C_atm + P_atm)/F;
   1-sigma move = 1.2533 * straddle/F.
   Event-only: sigma_E^2 ~= (1.2533*straddle/F)^2 - sigma_d^2 * T_front.
   Store raw straddle/F, straddle-based sigma_E, term-structure sigma_E.
 - Time-series (realized crush) estimator:
   sigma_E^2 ~= sigma_pre^2 T_pre - sigma_post^2 T_post (same expiry).
 - Run-up: dIV_runup(N) = IV_front_ATM(pre-event snapshot) -
   IV_front_ATM(T-N), N in {3,5,10,20}; also event-variance share
   sigma_E^2/(sigma_1^2 T_1) and India VIX change for index events.
 - Crush: dIV_crush = IV_front(first post-event close or chosen
   post-event snapshot) - IV_front(pre-event snapshot), on BOTH fixed-strike
   and ATM-forward/fixed-delta bases; relative crush = dIV/IV_pre; compare
   with the model-predicted post-event vol
   sqrt((sigma_1^2 T_1 - sigma_E^2) / T_1').
 - Realized/implied: R = |ln(S_post/S_pre)| / implied_move (define
   S_pre = last pre-announcement price; S_post = first post-event close;
   also compute open-based variant). ln(R) is the main ML target.
 - Context: IV rank = (IV - min_252)/(max_252 - min_252) and IV percentile,
   BOTH computed on ex-event (diffusive) IV; 25-delta risk reversal and
   butterfly; smile concavity; term slope IV_front/IV_next; historical
   median |event move| for the same underlying over last 8-12 events
   (strictly prior events); liquidity metrics (ATM spread % of straddle,
   OI both months).
 - Statistical tests: Wilcoxon signed-rank on dIV_crush and dIV_runup;
   test median ln(R) = 0; all with event-date clustering.

---------------------------------------------------------------------
7. STRATEGY LIBRARY, TIMING AND SELECTION RULES
---------------------------------------------------------------------
Implement each as a parameterised structure (strike by delta, % of
implied move, or fixed width), with entry/exit anchored to announce_ts:
  SHORT: short straddle, short strangle, iron butterfly, iron condor,
         broken-wing butterfly, jade lizard, 1x2 ratio (flag naked tail)
  TERM:  long calendar, double calendar (strikes at +/- implied move),
         diagonal
  LONG:  long straddle/strangle (hold-through), run-up straddle (exit
         pre-event), run-up calendar (exit pre-event)
  DIRECTIONAL: debit vertical, risk reversal (flag naked leg)
Timing grid to test: entry T-20, T-10, T-7, T-5, T-3, T-1 close,
pre-announcement intraday snapshot; exit pre-event snapshot, first
post-event liquid print (+15/30 min), T+1 close, T+2 close.
Default selection rules (thresholds are PRIORS to calibrate via
walk-forward, never hard-coded truths):
  - implied / hist-median move > 1.2-1.3 AND liquidity OK -> short iron
    fly (iron condor if kurtosis high); exit first liquid post-event print
    or T+1 close.
  - rich premium AND IV_front/IV_next > 1.1-1.2 -> long calendar/double
    calendar (short event month, long next).
  - implied / hist-median move < 0.8 (esp. high kurtosis, volatile past
    surprises) -> long straddle/strangle T-3..T-1 to T+1.
  - strong historical run-up AND event early in series (~20+ DTE) ->
    run-up straddle or run-up calendar T-7..T-3 to T-1; never hold through.
  - skew / put-call volume signal + conviction -> debit vertical, BWB or
    jade lizard.
  - BUDGET / ELECTION_RESULTS -> only small wide iron condors, calendars
    or run-up trades (Budget 2026 and 2024 results inverted the crush).
  - RBI / CPI / FOMC on NIFTY -> short NIFTY weekly iron fly/condor only if
    expected credit after costs clears a threshold; FOMC = overnight gap,
    defined risk mandatory.
  - otherwise -> NO TRADE (expected to be the majority outcome).
India-specific constraints (hard rules in the simulator):
  - Single-stock options: MONTHLY only, expire last Tuesday (post
    1 Sep 2025; last Thursday before). Index weeklies: NIFTY only (Tuesday)
    from 20 Nov 2024; BANKNIFTY/FINNIFTY/MIDCPNIFTY monthly only.
  - Stock options are PHYSICALLY settled; index options cash-settled.
    Stock options exercise style: widely stated as European - VERIFY and
    store in contract_master.exercise_style.
  - Force-close stock-option event positions before expiry-day T-1 unless
    a scenario explicitly models delivery margin and delivery.
  - Expiry day: +2% ELM on short options (verify whether index-only);
    calendar-spread margin benefit removed (one broker: from 4 PM T-1).
  - Choose the event expiry: if the event falls in the current series
    with enough DTE use current month (back leg next month); if it falls in
    expiry week, prefer next month and flag reduced crush capture.
  - Enforce lot sizes, strike grid and tick size from the PIT master.

---------------------------------------------------------------------
8. BACKTEST REALISM
---------------------------------------------------------------------
Fills (three tiers, all reported): CONSERVATIVE buy@ask/sell@bid;
REALISTIC mid +/- alpha*half_spread (alpha calibrated, ~0.5-1.0 for stock
options); OPTIMISTIC mid (sensitivity only). Never fill at LTP/settle on
illiquid strikes. Widen spreads at post-event open. Size cap: qty <= x% of
displayed depth or day volume; else partial fill/reject.
Liquidity gates at entry: min OI, min contracts traded, max spread/mid,
premium >= k ticks, strike within +/-N% of F, next-month liquidity for
calendars.
Costs (per fill; load from cost_params with effective dates):
  brokerage (default Rs20/order, configurable)
  STT: options sell 0.15% of premium (from 1 Apr 2026; 0.10% 1 Oct 2024 -
       31 Mar 2026; 0.0625% before); exercised ITM 0.15% of intrinsic
       (0.125% before Apr 2026); futures 0.05% (0.02% before)
  NSE transaction charge 0.03503% of premium each side (from 1 Oct 2024;
       CHECK circular FA73061 for later revision)
  stamp duty on buys (0.003% - UNVERIFIED), SEBI fee (Rs10/crore -
       UNVERIFIED), GST 18% on brokerage + exchange + SEBI fees,
  DP/delivery charges if physically settled.
Margin: SPAN (from NSE Clearing daily SPAN risk-parameter files, or a
16-scenario price/vol grid reimplementation) + exposure margin + expiry-day
+2% ELM + full upfront premium for longs + calendar benefit removal on
expiry day + delivery margin escalation for stock options near expiry
(approx: max(40% of contract value, SPAN+exposure) on expiry day for ITM
shorts/futures - VERIFY). Flag approximated margins. Report return on
margin.
Gaps: simulate post-event open; stress each short with the underlying's
historical max event gap and with 2x/3x implied-move shocks.
Architecture: vectorised event-trade ledger (polars) feeding an event-driven
portfolio simulator (NautilusTrader-style or custom) for capital, margin,
overlapping positions and sector caps.

---------------------------------------------------------------------
9. STATISTICS AND ANTI-OVERFITTING
---------------------------------------------------------------------
 - Unit of observation = event. Standard errors clustered by event date
   (or two-way firm x date); block/stationary bootstrap resampling whole
   event dates for CIs of mean P&L, win rate, CVaR.
 - Harvey-Liu-Zhu: require t > 3.0 for any new signal/filter.
 - Deflated Sharpe Ratio as headline Sharpe:
   PSR(SR*) = Phi[(SR_hat - SR*) sqrt(T-1) /
              sqrt(1 - g3 SR_hat + (g4-1)/4 SR_hat^2)],
   SR* = sqrt(V[SR_n]) [(1-gamma) Phi^-1(1-1/N) + gamma Phi^-1(1-1/(N e))],
   gamma = 0.5772; N and V[SR_n] from trial_registry. Verify symbols
   against Bailey & Lopez de Prado (2014).
 - PBO via CSCV across all logged configurations.
 - Purged + embargoed k-fold and CPCV for any fitted model; groups =
   event dates (never random k-fold across a results date).
 - Anchored walk-forward by earnings season / quarter; a final untouched
   holdout (last 12-18 months) opened once.
 - Report every metric separately per regime_id and pre/post each break.
 - Leakage guards: first_seen_ts; no T-close features for intraday events;
   expanding (not full-sample) normalisation; survivorship-free universe;
   unadjusted-strike fake moves.
 - Optional ML: target ln(R) or sign of short-straddle P&L; features as of
   the pre-event snapshot only (implied move, sigma_E, event-variance share,
   run-up, ex-event IV rank, prior R history, hist |move|, RV 5/20/60 vs IV,
   RR25, BF25, concavity, term slope, sector, size/liquidity, India VIX
   level/change, session flag, DTE, peers reported so far, OI/PCR change).
   Baseline regularised linear/quantile regression, then LightGBM with
   monotonic constraints; evaluate economically (after-cost DSR of a
   trade-on-prediction rule). Expect ~7-8k stock events in 10 years: keep
   features and searches small.

---------------------------------------------------------------------
10. RISK MANAGEMENT AND POSITION SIZING
---------------------------------------------------------------------
 - Prefer defined-risk structures; max loss per event 0.5-2% of capital
   (configurable); fractional Kelly <= 0.25 on shrunk edge estimates.
 - Caps: per-sector and per-date concentration during results season;
   gross vega and gap-stress loss caps for the book.
 - Profit-take / stop rules as testable parameters (e.g. 50% of max profit
   for condors; 20-30% target, 15-20% stop for run-up calendars).
 - Optional delta hedge of residual gamma with futures.
 - Kill-switch: skip short-vol when event is flagged as policy-surprise
   risk (e.g. Budget with market-tax proposals) or when India VIX regime
   filter trips.
 - Respect position limits/MWPL (irrelevant at small size; enforce anyway).

---------------------------------------------------------------------
11. REPORTING / DASHBOARD
---------------------------------------------------------------------
Per event: IV term structure and smile before/after, implied vs realized
move, sigma_E, run-up and crush, R, structure P&L with Greek attribution
dP ~ delta dS + 0.5 gamma dS^2 + vega dSigma + theta dt + residual.
Per strategy: P&L in Rs, % of premium, % of margin; win rate; expectancy;
payoff ratio; median; P5/P1; max loss as multiple of credit; CVaR95/99;
tail ratio; skew/kurtosis; Sharpe/Sortino (annualised by events/yr or a
daily MTM series); DSR; PBO; max drawdown and duration; Calmar; return on
margin.
Heatmaps: sector x ex-event IV-rank decile; implied-move bucket x R;
session flag; front DTE bucket; year/regime.
Event-type scorecards (results, RBI, Budget, election, CPI, FOMC,
rebalance, USFDA, corp action) with sample size and CI.
Upcoming-event screener: for each scheduled event, current implied move,
sigma_E, hist median move, ratio, term slope, liquidity grade, recommended
structure or NO TRADE, expected P&L distribution and margin, plus the
historical analog events.
Every report shows: data sources, fill tier, cost version, margin model
(exact vs approximated), and a banner listing any UNVERIFIED parameters used.
UI: Streamlit (or Dash/Plotly). Also export static HTML/Parquet.

---------------------------------------------------------------------
12. TECH STACK
---------------------------------------------------------------------
Python 3.12+, polars, DuckDB, pyarrow/Parquet, numpy, scipy (SSVI
calibration), numba, py_vollib_vectorized / Let's Be Rational (optional
fast-vollib), QuantLib (validation), statsmodels/linearmodels (clustered
SEs), scikit-learn + LightGBM (optional ML), NautilusTrader or a custom
event-driven simulator, jugaad-data/nselib/nsepython (EOD ingestion),
Dhan/Upstox SDKs (intraday), OpenAlgo (optional broker snapshots),
Streamlit/Plotly, pydantic for configs, pytest + hypothesis, ruff + mypy,
Prefect or plain cron for scheduled ingestion. Pin all versions; verify
library maintenance status on PyPI before adopting.

---------------------------------------------------------------------
13. MODULE / REPO STRUCTURE
---------------------------------------------------------------------
nse_event_vol/
  config/            costs.yaml, margins.yaml, regimes.yaml, expiry_rules.yaml,
                     sources.yaml  (every value has effective dates, source
                     URL, verified flag)
  ingest/            bhavcopy_legacy.py, bhavcopy_udiff.py, dhan_expired.py,
                     upstox_expired.py, vix.py, rates.py, corp_actions.py,
                     lots_strikes.py, fo_universe.py
  events/            results_nse.py, rbi.py, budget.py, elections.py,
                     mospi.py, fomc_uscpi.py, rebalances.py, usfda.py,
                     calendar_snapshotter.py, session_mapper.py
  pit/               contract_master.py, adjustments.py, universe.py,
                     asof.py (as-of joins), regimes.py
  pricing/           black76.py, forward.py, iv_solver.py, ssvi.py,
                     cm_iv.py, greeks.py, quote_filters.py
  metrics/           event_variance.py, implied_move.py, runup_crush.py,
                     realized.py, context.py
  strategies/        base.py, short_vol.py, term.py, long_vol.py,
                     directional.py, selector.py
  sim/               fills.py, costs.py, margin_span.py, settlement.py,
                     ledger.py, portfolio.py, stress.py
  stats/             clustering.py, bootstrap.py, dsr.py, pbo.py, cv.py,
                     walkforward.py, trial_registry.py
  ml/                features.py, models.py, evaluation.py
  reports/           tearsheet.py, heatmaps.py, event_card.py, screener.py
  app/               streamlit_app.py
  tests/             unit/, property/, golden/, integration/
  notebooks/         exploratory only; nothing imported from here
  docs/              DESIGN_DECISIONS.md, METHODOLOGY.md, DATA_SOURCES.md,
                     VERIFICATION_LOG.md

---------------------------------------------------------------------
14. PHASED MILESTONES
---------------------------------------------------------------------
Pre-M0 Grilling session (section 0) completed and DESIGN_DECISIONS.md
   confirmed by me. No code before this.
M0 Verification & config: build VERIFICATION_LOG.md; populate
   config/*.yaml; every UNVERIFIED item below either confirmed from a
   primary NSE/SEBI/RBI/MOSPI source (URL + circular no. + effective date)
   or explicitly marked unverified and surfaced in reports.
M1 Data: EOD bhavcopy ingestion (legacy + UDiFF), spot, futures, VIX,
   rates; PIT contract master, lots, corp actions, F&O universe; data QA.
M2 Events: results calendar with timestamps + session mapping; macro
   calendars (RBI, Budget, elections, CPI, FOMC); snapshotting; first_seen.
M3 Pricing: Black-76, forward, LBR solver, quote filters, SSVI, CM IV,
   Greeks; validation vs QuantLib and vs India VIX (replicate VIX within
   tolerance from Nifty chain as an integration check where quotes exist).
M4 Event metrics panel for all events; descriptive study (run-up, crush,
   R distributions by event type/regime) - this is the first deliverable.
M5 Simulator: fills, costs, margin, settlement, strategies, ledger;
   backtest short straddle / iron fly / calendar / run-up straddle on
   results; then macro events on NIFTY/BANKNIFTY.
M6 Statistics: clustering, bootstrap, DSR, PBO, walk-forward, holdout.
M7 Selector + screener + dashboard; optional ML layer.
M8 Hardening: intraday data (Dhan/Upstox) for event windows, quote-based
   fills if a vendor is added, performance, docs.

---------------------------------------------------------------------
15. ACCEPTANCE TESTS (must pass in CI)
---------------------------------------------------------------------
 - Black-76 price->IV->price round trip < 1e-8 across moneyness/DTE grid;
   LBR matches QuantLib IV within 1e-6 on a random sample.
 - Put-call parity forward within tolerance of same-expiry futures on
   liquid days; NaN (not 0) for sub-intrinsic prices.
 - SSVI fit passes butterfly (g(k) >= 0) and calendar (w non-decreasing in
   T at fixed k) checks on every fitted date.
 - CM IV interpolates in total variance: synthetic test with known
   sigma_d and sigma_E recovers inputs.
 - Event-variance extractor recovers sigma_E from a synthetic surface
   generated with the additive model (error < 1% rel.); flags NO_INVERSION.
 - Session mapper: post-market announcement -> reaction T+1; intraday ->
   T; Sunday Budget handled; pre-event snapshot strictly before announce_ts.
 - As-of joins never return data with recorded_at/first_seen_ts after the
   decision timestamp (property-based test).
 - Corporate actions: a 1:1 bonus doubles lot, halves strike, preserves
   contract value; dividend <2% leaves strike unchanged.
 - Lot size for NIFTY = 75 on Dec 2025 monthly and 65 from the 27 Jan
   2026 monthly (and 6 Jan 2026 weekly); expiry weekday = Thursday before
   1 Sep 2025 and Tuesday after (golden tests from config).
 - Cost engine reproduces a hand-computed ledger for a sample trade under
   pre- and post-1 Apr 2026 STT; exercise STT example: NIFTY 24,800 CE
   settling at 25,000, 65 qty -> 0.15% x 200 x 65 = Rs19.50.
 - Margin engine applies +2% ELM and removes calendar benefit on expiry
   day; defined-risk structure margin < naked equivalent.
 - Fill tiers ordered: conservative P&L <= realistic <= optimistic.
 - Survivorship: universe on a past date includes names later removed.
 - Stats: DSR implementation matches the paper's worked example; clustered
   SEs wider than naive SEs on a synthetic clustered panel; trial_registry
   increments on every run.
 - Reproducibility: same config hash + dataset version -> identical ledger.

---------------------------------------------------------------------
16. VERIFICATION INSTRUCTIONS (MANDATORY BEFORE USE)
---------------------------------------------------------------------
Before any parameter is used in a backtest reported to a human, verify it
against a PRIMARY source (nseindia.com / nsearchives / nseclearing.in
circulars, sebi.gov.in circulars, rbi.org.in, mospi.gov.in, incometax /
Finance Act for STT) and record circular number, URL, effective date in
VERIFICATION_LOG.md and config. Items known to be UNVERIFIED or
secondary-sourced:
  - stock options exercise style (European?) and physical-settlement
    circular text; delivery-margin schedule near expiry
  - strike-interval scheme (stocks and indices) by date
  - current NSE options transaction charge (post circular FA73061) and
    BSE charges
  - stamp duty 0.003% (buy side) and SEBI fee Rs10/crore; IPFT
  - whether +2% expiry-day ELM applies to all short options or only index
  - exposure-margin percentages (index vs stock) in 2026
  - calendar-benefit removal timing (expiry day vs 4 PM on T-1)
  - 2026 stock lot-size revisions (fo_mktlots)
  - RBI announcement time (~10:00 IST), CPI release time (~12th, 16:00
    IST), Budget date convention (1 Feb)
  - FY27 Aug/Oct/Dec MPC dates
  - India VIX methodology after weekly/Tuesday changes
  - status of Sept 2026 SEBI consultation on VWAP settlement / closing
    auction
  - all MOSPI, ECI, MSCI/FTSE/NSE Indices rebalance dates
Never silently default an unverified value: use it only behind a flag
that prints a warning banner on every report.

---------------------------------------------------------------------
17. EVIDENCE FLAGS TO CARRY INTO DOCS AND REPORTS
---------------------------------------------------------------------
 - US-ONLY evidence (do not assume transfer): pre-event straddle premium
   (Gao-Xing-Zhang +3.34%), regime flips (BSIC 2011-21 negative; ORATS
   ~-2% then ~+45% late 2025), long-calendar superiority (ORATS),
   run-up theta dominance (Khan & Khan), retail overpayment (de Silva et
   al.), concave-smile signal (Alexiou et al.), bellwether premia, 70-75%
   implied-move containment.
 - INDIAN evidence that exists: monotonic IV/skew run-up and post-results
   decline, skew/PCR predict surprise sign (IIMA 2024); negative Nifty VRP
   (IREF 2020); VIX fell on 15 Budget days to 2025 but rose >17% on Budget
   2026; election results VIX -34% (2014), -30% (2019), +23-28% (2024).
 - INDIAN evidence MISSING (the engine must produce it): crush size after
   results; implied-vs-realized containment; event straddle/calendar/iron
   fly P&L; run-up size; IV around RBI/CPI/FOMC, USFDA, M&A, splits,
   rebalances; stock-option spreads; margin ratios; VIX half-life.
Report every conclusion with its sample size, regime, fill tier and
confidence interval. If the data says NO TRADE for an event class, say so.

---------------------------------------------------------------------
18. WORKING IN AN AGENTIC IDE (GOOGLE ANTIGRAVITY OR SIMILAR)
---------------------------------------------------------------------
This prompt is model- and tool-agnostic; these rules apply to whichever
agent/model runs it (Antigravity with Gemini, Claude, or another model).
 - Persistent context: keep a repo-root rules file (AGENTS.md, and the
   rules location Antigravity currently documents, if different) that
   summarises this prompt and links docs/DESIGN_DECISIONS.md,
   docs/METHODOLOGY.md and docs/VERIFICATION_LOG.md. Re-read them at the
   start of every task; never rely on chat memory for decisions.
 - One milestone = one task. Before coding, produce a written plan
   (files, tests, risks) and wait for my approval; after coding, produce
   a walkthrough (what changed, tests run with output, open risks).
 - Tests first for every formula and rule in section 15; a task is not
   done until `pytest`, `ruff` and `mypy` pass locally.
 - No invented facts: the agent must not fill regulatory, cost, lot-size,
   calendar or API-behaviour values from model memory. Look them up from a
   primary source or leave them UNVERIFIED per section 16.
 - Secrets: Upstox/Dhan API keys and tokens live only in macOS Keychain or
   an untracked .env; never in code, logs, prompts or commits. Add
   .env and data/ to .gitignore before the first commit.
 - Safety: no order-placement endpoints anywhere in the codebase; the
   browser/terminal agent must not log in to broker accounts or run
   destructive commands (rm -rf, force-push, dropping data/) without my
   explicit approval.
 - Autonomy: agent may run read-only commands and tests freely; any
   command that downloads bulk data, spends money (Dhan subscription,
   cloud VM) or writes outside the repo needs my approval.
 - Reproducibility: pin dependencies (uv or pip-tools lockfile); every
   backtest run logs to trial_registry regardless of which model ran it.
 - Local environment: macOS (Apple Silicon assumed; confirm), Python 3.12
   via uv or pyenv, Homebrew for system packages; recorder deploy target
   is a Linux VM, so keep recorder code OS-independent.

DELIVERABLES: the repository above, passing CI, a DESIGN_DECISIONS.md, a
METHODOLOGY.md, a VERIFICATION_LOG.md, the event-metrics panel (Parquet), backtest ledgers,
tearsheets per event type and strategy, and the Streamlit app with the
upcoming-event screener. Work milestone by milestone; at the end of each,
summarise what was built, what was verified, and open risks.
=====================================================================
```
