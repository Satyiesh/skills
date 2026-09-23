# India VIX and Nifty/BankNifty Implied Volatility Around Macro and Non-Earnings Events

Research note: every article fetch (BusinessToday, AngelOne, Arihant, Substack) was blocked by the network egress proxy. Every finding below comes from search-result snippets of the cited pages, not full-text reads. Treat the exact decimals as "as reported by the source". Before relying on any number in a backtest, check it against NSE's own India VIX historical data file.

## 1. Union Budget days: India VIX before and after, and the Nifty move on the day

### Takeaway
Up to 2025 the pattern was reliable: India VIX rises into the Budget and falls on Budget day. Arihant's 15-budget study reports a VIX decline on every Budget day, averaging more than 9%. Budget 2026 (1 Feb 2026) broke that pattern. A surprise STT hike on derivatives drove Nifty down about 2% and India VIX up more than 17%. An IV-crush engine therefore needs a "policy surprise" override: on Budget day, the crush is the base case but not a certainty.

### Cited Findings
- **Budget-day VIX pattern:** across 15 observed Budgets (including interim ones), India VIX fell on Budget day every time, by more than 9% on average. The source's reading is that nervousness peaks before the Budget and the announcement removes uncertainty. — [Arihant Plus, 15-year Budget analysis](https://www.arihantplus.com/blogs/market-updates/union-budget-day-and-market-behaviour-15-year-trend-analysis) (as summarised in search results; that summary also cites [BusinessToday, 30 Jan 2026](https://www.businesstoday.in/union-budget/story/sensex-nifty-dip-india-vix-surges-ahead-of-budget-2026-what-historical-data-says-513628-2026-01-30))
- **Direction of the Budget-day move:** since 2014, Sensex and Nifty closed positive on 9 of 15 Budget days, interim Budgets included. — [BusinessToday, 30 Jan 2026](https://www.businesstoday.in/union-budget/story/sensex-nifty-dip-india-vix-surges-ahead-of-budget-2026-what-historical-data-says-513628-2026-01-30) / [Arihant Plus](https://www.arihantplus.com/blogs/market-updates/union-budget-day-and-market-behaviour-15-year-trend-analysis)
- **Largest Budget-day moves:**
  - Biggest gain: 1 Feb 2021, Nifty +4.7% (+646 pts).
  - Biggest fall: 1 Feb 2020, Nifty −2.5% (about −300 pts).
  - Source for both: [Arihant Plus](https://www.arihantplus.com/blogs/market-updates/union-budget-day-and-market-behaviour-15-year-trend-analysis)
- **Pre-Budget run-up examples:**
  - Budget 2026: India VIX rose 3.66% to 13.86 in the run-up (BusinessToday, 30 Jan 2026) — [BusinessToday](https://www.businesstoday.in/union-budget/story/sensex-nifty-dip-india-vix-surges-ahead-of-budget-2026-what-historical-data-says-513628-2026-01-30)
  - Budget 2022: India VIX rose 6% to 21.95 on 31 Jan 2022, the day before the Budget — [Business Standard](https://www.business-standard.com/amp/article/markets/india-vix-soars-6-to-21-95-a-day-ahead-of-union-budget-122013101779_1.html)
  - Budget 2022, Budget day (1 Feb 2022): intraday India VIX was down 5.11% at 20.83 — [Business Standard](https://www.business-standard.com/article/news-cm/nifty-hovers-below-17-550-india-vix-falls-5-11-to-20-83-122020100765_1.html)
- **Pre-Budget drawdowns:** when Nifty or Sensex fell more than 3% in the month before the Budget, a strong rebound followed over the next 1 week, 1 month and 3 months. — [Arihant Plus / BusinessToday summary](https://www.arihantplus.com/blogs/market-updates/union-budget-day-and-market-behaviour-15-year-trend-analysis)
- **Budget 2024-25 (23 Jul 2024), an example of intraday vol followed by a crush:**
  - LTCG tax rose to 12.5% from 10% and STCG to 20% from 15%. STT on F&O also rose.
  - Nifty hit an intraday low of 24,074, then recovered 405 pts to close −0.12% at 24,479. Sensex fell 1,278 pts intraday and closed −0.09%.
  - India VIX fell 17.42% to 12.75.
  - Sources: [Upstox](https://upstox.com/news/market-news/trading/nifty-50-sensex-close-flat-after-volatile-trading-session-led-by-tweaks-in-capital-gains-tax-in-budget/article-104166/); [Business Standard, "VIX tanks 17%"](https://www.business-standard.com/amp/markets/capital-market-news/market-ends-with-tiny-cuts-fmcg-shares-rally-vix-tanks-17-124072300954_1.html); [Business Standard on the tax changes](https://www.business-standard.com/markets/news/budget-2024-hikes-ltcg-tax-rate-to-12-5-stcg-to-20-stt-on-f-o-also-up-124072300553_1.html)
- **Budget 2026 (Sunday 1 Feb 2026), the exception:**
  - STT on futures rose to 0.05% from 0.02%, and STT on options premium to 0.15% from 0.1%.
  - Nifty closed at 24,825, down 495 pts (−1.96%). Sensex fell 1,547 pts to 80,723.
  - India VIX jumped more than 17% to 15.66.
  - Nifty PSU Bank fell more than 4%, and BSE market cap dropped ₹9.72 lakh crore.
  - Sources: [Business Standard live blog](https://www.business-standard.com/markets/news/stock-market-live-updates-february-1-union-budget-2026-nirmala-sitharaman-speech-sensex-nifty-share-market-today-126020100067_1.html); [Upstox](https://upstox.com/news/market-news/trading/stock-market-nifty-50-sensex-live-updates-on-sunday-february-1-union-budget-2026/liveblog-188661/); [Outlook Business](https://www.outlookbusiness.com/budget/budget-2026-how-a-surprise-stt-hike-triggered-a-market-rout-eroding-972-lakh-crore-investors-wealth)
- **Budget-day straddle backtest (Options IQ):**
  - Strategy: a Nifty monthly short straddle entered before the Budget.
  - Results: 79% win rate, average profit 16 pts, median profit 32 pts, outlier-adjusted profit factor 2.06.
  - The author concludes that long straddles and strangles "fall short of expectations on budget days" and that sellers win.
  - The article could not be opened to get the years covered or the entry and exit timing.
  - Sources: [Options IQ Substack](https://optionsiq.substack.com/p/nifty-short-straddle-performance); a related practitioner piece is [Pushkar Raj Thakur, budget-day straddle/strangle backtest](https://pushkarrajthakur.com/budget-day-strategy-straddle-strangle-backtesting-on-buying-ce-pe-best-option-trading/)

### Inferences
- Budget-day IV crush is the base case, with a long track record, but tax and STT changes for market participants are the recognised tail risk. Budget 2026 was the first case in this sample where VIX rose on Budget day.
- Weekend Budgets complicate backtests: 1 Feb 2020 was a Saturday, 1 Feb 2025 a Saturday, and 1 Feb 2026 a Sunday. These were special trading sessions, so the engine needs special handling for DTE, theta, and the following Monday's gap.
- Given a realised move of about −2.5% to +4.7% and a typical India VIX of 13–22 before the Budget, the implied 1-day move (VIX/√252) is roughly 0.8–1.4%. Several Budgets (2020, 2021, 2026) moved more than 1.5× the implied move. This figure is inferred from VIX levels, not computed from straddle prices.

### Gaps
- There is no sourced year-by-year table of pre-Budget VIX, Budget-day VIX change, and the ATM straddle-implied move versus the realised move for 2015–2026, because the Arihant and Cleartax tables could not be fetched.
- The Budget 2025 (1 Feb 2025) VIX change and Nifty move were not found in the searched sources.
- The Options IQ backtest period and entry/exit rules are unknown.

## 2. General elections (2014, 2019, 2024) and state elections

### Takeaway
India VIX rises sharply into general-election results. It drops roughly 30–34% on results day when the outcome matches expectations (2014, 2019), and it rises when the outcome is a surprise (2024: +23% to +28%, with Nifty −5.9%). Exit-poll days are a separate crush event that comes before results day.

### Cited Findings
- **2014:**
  - Ahead of the exit polls, India VIX reached its highest level since 11 Mar 2009, with four straight sessions of gains — [Business Standard, 12 May 2014](https://www.business-standard.com/amp/article/markets/vix-at-five-year-high-ahead-of-exit-polls-114051200340_1.html)
  - On exit-poll day (13 May 2014), VIX fell as much as 23.88%, its biggest one-day fall since 26 Aug 2009. Nifty hit a record 7,116.20 (+1.45%) — [Business Standard, 13 May 2014](https://www.business-standard.com/article/markets/vix-heads-towards-biggest-slump-in-over-4-1-2-years-114051300385_1.html)
- **2014 and 2019 results days:** India VIX fell about 34% (2014) and about 30% (2019) on results day — [Business Standard / BusinessToday summary](https://www.business-standard.com/amp/article/news-ians/volatility-index-drops-by-another-16-119052400614_1.html)
- **2019 run-up:**
  - VIX touched record levels during the run-up and dropped sharply after the exit polls (Monday 20 May 2019).
  - It then rose again to about 30, its highest since 2014, on 22 May, the day before counting (23 May) — [Business Standard, 22 May 2019](https://www.business-standard.com/article/news-ians/sensex-ends-140-pts-higher-vix-at-4-yr-high-119052201155_1.html)
  - It fell a further 16% on 24 May 2019 — [Business Standard](https://www.business-standard.com/amp/article/news-ians/volatility-index-drops-by-another-16-119052400614_1.html)
- **2024 run-up:**
  - On 23 Apr 2024, India VIX recorded its steepest slump in nearly 5 years, about −20% — [Business Standard](https://www.business-standard.com/amp/markets/news/india-vix-index-sharply-slumps-20-the-biggest-drop-in-five-years-124042301001_1.html)
  - On 13 May 2024, VIX crossed 20 during the polling phases — [Business Standard](https://www.business-standard.com/amp/markets/capital-market-news/benchmarks-stage-comeback-after-initial-slump-vix-crosses-20-mark-124051301063_1.html)
- **2024 exit-poll day (3 Jun 2024):** Sensex crossed 76,700 and Nifty went above 23,300, both record highs, up more than 3% on exit polls projecting a large NDA win — [HDFC Sky](https://hdfcsky.com/sky-learn/market-wtf-by-sky/2024-election-day-stock-market-crash-and-two-day-recovery); [BusinessToday](https://www.businesstoday.in/markets/market-commentary/story/election-results-2024-india-vix-jumps-india-alliance-exceeds-expectations-432101-2024-06-04)
- **2024 results day (4 Jun 2024):**
  - Market move: Nifty fell more than 1,379 pts (−5.9%), below 22,000. Sensex fell about 4,390 pts (−5.7%), the worst day in more than 4 years — [Business Standard live blog](https://www.business-standard.com/markets/news/stock-market-live-updates-june-4-sensex-nifty-lok-sabha-election-results-2024-psu-stocks-nse-124060400081_1.html); [Bajaj Broking](https://www.bajajbroking.in/blog/stock-market-crash-and-election-results-2024-updates)
  - India VIX: reported as up 27.70% to 26.74 by [BusinessToday](https://www.businesstoday.in/markets/market-commentary/story/election-results-2024-india-vix-jumps-india-alliance-exceeds-expectations-432101-2024-06-04), and as "over 23%" by [Bajaj Broking](https://www.bajajbroking.in/blog/stock-market-crash-and-election-results-2024-updates). The gap is probably intraday versus close; this is unverified.
- **Recovery after 4 Jun 2024:**
  - HDFC Sky describes a "two-day recovery", driven by clarity on government formation and DII buying, with the RBI policy on 7 Jun 2024 as the next event — [HDFC Sky](https://hdfcsky.com/sky-learn/market-wtf-by-sky/2024-election-day-stock-market-crash-and-two-day-recovery)
  - A later snapshot: the April 2025 tariff spike was reported as the "highest since June 4, 2024", which implies VIX then stayed below its 4 Jun level for about 10 months — [Business Standard, 7 Apr 2025](https://www.business-standard.com/amp/markets/news/india-s-stock-market-volatility-spikes-as-trade-war-fears-rattle-traders-125040700297_1.html)

### Inferences
- The election sequence has three distinct events: (a) the run-up across polling phases (VIX builds over weeks), (b) exit-poll day (a first crush, or a gap), and (c) results day (a crush if expectations are met, an explosion if not). A 2024-style upset gap of 5.9% was about 3–4× the move implied by VIX in the mid-20s (about 1.6%/day).
- Short-vol positions held through results day are exposed to a regime split. In 2014 and 2019, sellers captured a crush of about 30%. In 2024, sellers faced a 6% gap.

### Gaps
- Exact India VIX levels on each results day and exact 2024 recovery figures (Nifty % on 5 Jun and 7 Jun 2024) were not confirmed from fetchable sources.
- No sourced data was found on India VIX reaction to state-election results (for example, the Dec 2023 state results, and the Haryana and Maharashtra results in Oct and Nov 2024).

## 3. RBI MPC policy decisions

### Takeaway
Scheduled RBI decisions are usually low-impact for index vol. VIX changes on policy day are small, typically within ±5%. Surprises are the exception: the unscheduled 40 bp hike on 4 May 2022 (Nifty −2.29%) and the larger-than-expected 50 bp cut plus 100 bp CRR cut on 6 Jun 2025 (Bank Nifty record high, about +1.5%). Pre-policy short-tenor hedging lifts IV into the event.

### Cited Findings
- **4 May 2022, unscheduled 40 bp hike to 4.40% (the first hike since 2018):**
  - Nifty fell 2.29% to 16,677, Sensex fell more than 1,300 pts, and Bank Nifty fell 467 pts to 35,696.
  - Rate-sensitive sectors fell by up to 4%.
  - Sources: [BusinessToday](https://www.businesstoday.in/markets/stocks/story/sensex-crashes-900-points-nifty-falls-as-rbi-hikes-repo-rate-332270-2022-05-04); [Business Standard](https://www.business-standard.com/amp/article/markets/rate-hike-impact-rate-sensitive-shares-tumble-as-rbi-s-ups-rate-by-40bps-122050400582_1.html); [Forbes India](https://www.forbes.com/advisor/in/personal-finance/2022/05/04/indias-rbi-hikes-repo-rate-by-0-4-amid-inflation-woes-first-since-2018/)
- **9 Apr 2025, 25 bp cut to 6%:** Nifty settled near 22,400 and VIX rose 4.83%. This came during the tariff shock. — [Business Standard](https://www.business-standard.com/amp/markets/capital-market-news/nifty-settles-near-22-400-rbi-cuts-repo-rate-by-25-bps-to-6-vix-rallies-4-83-125040900822_1.html)
- **6 Jun 2025, 50 bp cut to 5.50% and 100 bp CRR cut (double the expected size):**
  - Nifty Bank hit a record 56,624.40, up about 1.5%.
  - India VIX fell 1.47% to 14.86.
  - Sources: [BusinessToday](https://www.businesstoday.in/amp/markets/stocks/story/nifty-bank-hits-record-high-after-rbi-rate-cuts-banking-financial-stocks-rally-479278-2025-06-06); [Outlook Business](https://www.outlookbusiness.com/markets/nifty-bank-soars-to-record-high-after-rbis-steeper-than-expected-rate-cut-hdfc-bank-axis-bank-idfc-first-bank-top-gainers); [Business Standard](https://www.business-standard.com/amp/markets/capital-market-news/rbi-cuts-repo-rate-by-50bps-to-5-50-crr-by-100-bps-125060600238_1.html)
- **5 Aug 2022, 50 bp hike to 5.4% (expected):** rate-sensitive shares traded firm — [Business Standard](https://www.business-standard.com/amp/article/markets/rate-sensitive-shares-trade-firm-as-rbi-hikes-repo-rate-by-50-bps-to-5-4-122080500344_1.html)
- **2026 policy weeks:**
  - June 2026 policy week: India VIX swung intraday from 13.46 to 16.37 and closed near 15.78 on 5 Jun 2026 — [HDFC Sky](https://hdfcsky.com/news/india-vix-closes-near-15-78-after-intraday-swing-ahead-of-rbi-policy-as-volatility-eases-from-day-high-on-june-5-2026)
  - August 2026 policy: VIX stayed around 12.0–12.5, with a close of 12.01 on 5 Aug 2026 (−3%) and 12.15 on 7 Aug 2026 — [HDFC Sky 5 Aug 2026](https://hdfcsky.com/news/india-vix-slips-3-12-percent-as-rbi-policy-wait-keeps-volatility-contained-august-5-2026); [HDFC Sky 7 Aug 2026](https://hdfcsky.com/news/india-vix-closes-at-12-15-as-rbi-policy-crude-oil-and-earnings-keep-volatility-in-check-august-7-2026)
- **Practitioner framing:**
  - The pre-policy session usually carries elevated IV, with hedging concentrated in short-tenor index options.
  - The edge is "the gap between implied move and realized move".
  - Source: [HDFC Sky, RBI policy day options](https://hdfcsky.com/sky-learn/trading-strategies/how-to-use-options-for-rbi-policy-and-other-event-days)
- **Historical example:** in May 2013, a VIX surge kept traders wary ahead of the RBI policy — [Business Standard/Reuters](https://www.business-standard.com/amp/article/reuters/india-vix-surge-keeps-many-wary-ahead-of-rbi-policy-113050200446_1.html)

### Inferences
- In event-weighting terms, RBI days are small events for Nifty and moderate ones for BankNifty. The engine should treat BankNifty weekly or near-expiry IV (where listed) as the main instrument, and label surprises by comparing the decision against the consensus from a Reuters or ET poll.
- Unscheduled actions (May 2022) cannot be anticipated by an IV run-up model. They are pure gap risk for short-vol positions.

### Gaps
- No systematic dataset of BankNifty ATM IV change on RBI days was found.
- No published backtest of straddles on RBI days with statistics was found. Note also that NSE reduced weekly index expiries in Nov 2024, so BankNifty weekly options no longer exist; this is from the researcher's background knowledge and was not verified in this session.

## 4. Global and macro shocks (FOMC, US CPI, India CPI/GDP, COVID, Russia-Ukraine, yen carry, tariffs, 2025–2026)

### Takeaway
India VIX spikes of 50–60% in a single day happened on 5 Aug 2024 (yen carry unwind) and 7 Apr 2025 (tariffs). Both mean-reverted within weeks, and Nifty was positive four weeks later in about 75% of cases after a spike of more than 60% (ROC). COVID 2020 is the outlier: VIX hit an all-time closing high of 83.6, and Nifty fell 23% in the four weeks after the spike. In 2026 there was a US-Iran-driven spike to 27.17 (March) and a +26% day (8 Jul 2026).

### Cited Findings
- **COVID:**
  - India VIX closed at an all-time high of 83.61 on 24 Mar 2020 (about 87 intraday) — [CEIC](https://www.ceicdata.com/en/india/national-stock-exchange-of-india-limited/national-stock-exchange-of-india-limited-index-india-vix-index); [TickJournal](https://tickjournal.com/indices/india-vix/historical-data/)
  - On 12 Mar 2020, VIX was at its highest since the 2008 crisis — [Business Standard](https://www.business-standard.com/article/markets/india-vix-rises-to-highest-level-since-2008-crisis-as-fear-grips-markets-120031201406_1.html)
- **2008 GFC:** the intraday peak was about 92.5 (November 2008). VIX has crossed 60 only in 2008 and in 2020. — [Finnovate](https://www.finnovate.in/learn/blog/india-vix-2026-what-fear-index-tells-investors); [CEIC](https://www.ceicdata.com/en/india/national-stock-exchange-of-india-limited/national-stock-exchange-of-india-limited-index-india-vix-index)
- **Russia-Ukraine:**
  - On 15 Feb 2022, indices fell 3% on Ukraine fears and India VIX jumped 23% — [Business Standard](https://www.business-standard.com/amp/article/markets/indices-slump-3-as-fears-on-ukraine-grow-india-vix-index-jumps-23-122021500051_1.html)
  - Sensex and Nifty fell for a seventh straight day on 24 Feb 2022 (invasion day) — [Business Standard](https://www.business-standard.com/article/news-cm/sensex-nifty-decline-for-seventh-day-amid-russia-ukraine-war-122022400980_1.html)
  - The exact VIX close on 24 Feb 2022 was not retrieved.
- **Yen carry unwind, 5 Aug 2024:**
  - India VIX rose more than 60% intraday (nearly 62%), its sharpest surge in 9 years.
  - Triggers: the BoJ hike to 0.25% on 31 Jul 2024, weak US jobs and ISM data, and Israel-Iran tension.
  - Sources: [HDFC Sky](https://hdfcsky.com/blogs/market-wtf-by-sky/the-vix-spike-nobody-saw-coming); [BIS Bulletin 90](https://www.bis.org/publ/bisbull90.pdf)
- **US tariff shock, April 2025:**
  - 1 Apr 2025: VIX rose 10% on tariff fears — [Business Standard](https://www.business-standard.com/amp/markets/news/india-vix-jumps-10-on-tariff-fears-no-need-to-panic-says-devan-choksey-125040100579_1.html)
  - 7 Apr 2025: VIX rose as much as 59.4% intraday to 21.9, the biggest intraday jump since 4 Jun 2024. The close was more than +57%. India faced a 26% reciprocal tariff. — [Business Standard](https://www.business-standard.com/amp/markets/news/india-s-stock-market-volatility-spikes-as-trade-war-fears-rattle-traders-125040700297_1.html); [Business Standard, "biggest single-day jump"](https://www.business-standard.com/amp/markets/news/india-vix-logs-biggest-single-day-jump-signals-rocky-road-ahead-125040701001_1.html)
  - BusinessToday reported "up to 53%" — [BusinessToday](https://www.businesstoday.in/markets/stocks/story/stock-market-crash-fear-index-india-vix-shoots-up-to-53-on-heightened-uncertainty-470927-2025-04-07)
  - Samco describes it as a 9-year high in percentage-jump terms — [Samco](https://www.samco.in/knowledge-center/articles/india-vix-volatility-index-surges-to-9-year-high-amid-global-trade-fears/)
  - Nifty then gained about 12.5% over the next 4 weeks — [Samco spike study](https://www.samco.in/knowledge-center/articles/nifty-rebounds-in-75-of-cases-after-extreme-india-vix-spikes-what-history-reveals/)
- **Operation Sindoor (7 May 2025, after the Pahalgam attack on 22 Apr 2025):** India VIX rose only 3.58% to 19 on 7 May 2025, and markets ended higher — [TheHawk](https://www.thehawk.in/news/economy-and-business/sensex-nifty-end-higher-post-operation-sindoor); [PIB](https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/may/doc2025514554901.pdf)
- **2026 events:**
  - March 2026 (US-Iran conflict): India VIX rose from 13.70 to 27.17 in under a month. The intraday high of 27.17 on 23 Mar 2026 was the highest since June 2024. — [Finnovate](https://www.finnovate.in/learn/blog/india-vix-2026-what-fear-index-tells-investors)
  - 8 Jul 2026 (geopolitical tension and crude oil): VIX rose 26.01% to 14.68 — [HDFC Sky](https://hdfcsky.com/news/india-vix-surges-26percent-to-14-68-as-geopolitical-tensions-and-market-sell-off-lift-volatility-july-8-2026)
  - By 10 Aug 2026, VIX was back around 12.69 — [HDFC Sky](https://hdfcsky.com/news/india-vix-rises-4-36percent-as-volatility-rebounds-after-julys-sharp-spikeaugust-10-2026)
  - A Bullsmart blog reports VIX at 23.36 after a 65% surge in 2026 (date unclear, low-quality source) — [Bullsmart](https://blog.bullsmart.in/india-vix-at-23-with-65-surge-stocks-crash/)
- **Mean reversion after spikes:**
  - Samco studied 15 years of India VIX spikes above 60% on ROC. In week 4 afterwards, Nifty's average gain was about 1.3%, with a 75% probability of a positive return.
  - Outlier: February 2020 (COVID), with −23.2% over 4 weeks.
  - Source: [Samco](https://www.samco.in/knowledge-center/articles/nifty-rebounds-in-75-of-cases-after-extreme-india-vix-spikes-what-history-reveals/)

### Inferences
- The mean-reversion evidence shows up in the dates:
  - After the June 2024 and August 2024 spikes, VIX was back to about 12–13 by July 2024 (Budget day close of 12.75) and later in 2024.
  - The July 2026 spike to 14.68 was back to about 12 within a month.
  - A working heuristic for the engine: exogenous spikes that are not systemic retrace most of the jump within 2–4 weeks. Systemic crises (2008, 2020) take months.
- Geopolitical events involving India directly (Operation Sindoor) produced small VIX moves compared with global risk-off shocks.

### Gaps
- No sourced data was found on India VIX or Nifty IV behaviour around US FOMC, US CPI, Indian CPI or GDP releases specifically. These appear to be low-impact, but no quantitative source was retrieved.
- Exact VIX closes on 5 Aug 2024 and 24 Feb 2022 were not retrieved.

## 5. Corporate and other non-earnings events (single-stock IV)

### Takeaway
Very little public quantitative evidence exists on how single-stock IV behaves around non-earnings events on NSE. The retrieved evidence is limited to price reactions: Sun Pharma −4.5% on a USFDA warning letter (Dec 2015), and a record ₹39,718 crore closing-auction turnover at the Aug 2026 MSCI rebalance. IV studies would need to be built from NSE bhavcopy option data.

### Cited Findings
- **Sun Pharma, USFDA warning letter:** the stock fell 4.5% (about ₹8,655 crore of market value) on the warning letter for its Halol, Gujarat facility, in December 2015 — [Business Standard](https://www.business-standard.com/article/pti-stories/sun-pharma-shares-dip-4-5-on-warning-letter-from-usfda-115122100694_1.html)
- **MSCI rebalance:** NSE's Closing Auction Session processed a record ₹39,718 crore of turnover on 31 Aug 2026 as the MSCI India rebalance took effect, with "sharp and sometimes counterintuitive stock moves" (search-result snippet; source page not identified by URL in results).
- **General practitioner framing:** mergers, acquisitions and regulatory rulings raise IV before the announcement — [m.Stock](https://www.mstock.com/articles/implied-volatility-in-options-trading)
- **Tools:** Sensibull publishes IV charts for NSE stocks, a possible data source — [Sensibull IV chart](https://web.sensibull.com/implied-volatility-chart)

### Inferences
- For binary regulatory outcomes such as USFDA inspections, one-day moves of about 4–10% are plausible for large pharma companies. Rebalances are liquidity events concentrated at the close rather than volatility events, so an IV run-up is unlikely. This is inferred, not tested.

### Gaps
- No sourced IV data was found for:
  - the HDFC–HDFC Bank merger (announced 4 Apr 2022, effective 1 Jul 2023)
  - telecom tariff hikes (for example, July 2024)
  - stock splits or bonuses
  - block deals
  - Nifty or MSCI inclusions
- No academic event studies on NSE single-stock IV around non-earnings events were found in this session.

## 6. India VIX statistics and the Indian volatility risk premium

### Takeaway
India VIX has a long-run central tendency of roughly 15–20. It ranged from an all-time low of 9.15 (26 Dec 2025) to 83.6 at close (Mar 2020) and 92.5 intraday (Nov 2008). Academic work confirms a negative and significant variance risk premium in Nifty options: implied volatility exceeds realised, and straddle returns are negative. Practitioner sources say IV exceeds RV in about 4 of 5 sessions.

### Cited Findings
- **Range:**
  - All-time closing low: 9.15 on 26 Dec 2025 — [CEIC](https://www.ceicdata.com/en/india/national-stock-exchange-of-india-limited/national-stock-exchange-of-india-limited-index-india-vix-index)
  - Highs: 92.5 intraday (Nov 2008) and 83.61 at close (24 Mar 2020) — [CEIC](https://www.ceicdata.com/en/india/national-stock-exchange-of-india-limited/national-stock-exchange-of-india-limited-index-india-vix-index)
  - The long-term mean is often cited as about 18–20. Most of 2009–2019 fell in a 15–22 band — [LiveWorldMarket](https://liveworldmarket.com/symbol/india-vix-live) (low-authority aggregator)
  - CEIC's "median 25.485 (Jan 2012–Sep 2026)" looks inconsistent with these ranges and may reflect a different aggregation. Treat it as suspect.
- **Mean reversion:** extreme India VIX readings "typically revert toward the long-term mean within 1–3 months" — [LiveWorldMarket](https://liveworldmarket.com/symbol/india-vix-live) (practitioner claim, not a formal estimate)
- **NSE research:** NSE Working Paper WP/9/2013, "India Volatility Index (India VIX) and Risk Management in the Indian Stock Market", is the primary NSE study — [NSE](https://nsearchives.nseindia.com/research/content/res_WorkingPaper9.pdf)
- **Recent academic work:** a 2015–2025 study covers the informational content of India VIX for monthly Nifty volatility, using volatility envelopes, causality and conditional volatility — [IJISEM](https://ijisem.com/journal/index.php/ijisem/article/view/478)
- **Academic VRP evidence, "Dynamics of variance risk premium: Evidence from India" (International Review of Economics & Finance, 2020):**
  - Realised variance (intraday) minus model-free implied variance is negative and significant.
  - Market-neutral Nifty straddles earn negative, statistically significant excess returns.
  - Past continuous variance predicts short-term synthetic variance-swap returns; jumps do not.
  - Source: [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1059056020301222)
- **Trading vs non-trading periods:** Nifty options show negative overnight and positive intraday returns, implying the VRP differs across trading and non-trading periods — [Papagelis, Journal of Futures Markets 2025](https://onlinelibrary.wiley.com/doi/full/10.1002/fut.22589) (as summarised in search results)
- **Practitioner claim:** IV exceeds RV in "roughly four sessions in five" — search-result summary; origin unclear, low confidence.
- **India vs US:** India VIX runs structurally higher than US VIX because of higher realised volatility and a political-event risk premium — [LiveWorldMarket](https://liveworldmarket.com/symbol/india-vix-live)

### Inferences
- A structurally negative VRP supports short-vol event-crush strategies on average. The fat left tail (2020, June 2024, Budget 2026) is where the P&L risk sits, so position sizing matters more than signal.

### Gaps
- No formal half-life estimate (for example from an AR(1) or OU fit on daily India VIX) was found in the retrieved sources. It needs to be computed in-house from NSE VIX history. Mean-reversion speed is documented only anecdotally.
- No precise long-run mean or median from NSE itself was retrieved.

## 7. Published backtests (Sensibull, Stockmock, Opstra, Quantsapp, blogs, academic)

### Takeaway
The only quantified public backtest found is Options IQ's Nifty monthly short straddle around the Budget: 79% win rate, profit factor 2.06, median +32 pts. Academic evidence shows Nifty straddles lose money on average (a negative VRP). No quantified public backtests were found for election or RBI days.

### Cited Findings
- **Options IQ Budget short straddle:** 79% win rate, OAPF 2.06, average +16 pts, median +32 pts. Long straddles and strangles underperform on Budget days. — [Options IQ](https://optionsiq.substack.com/p/nifty-short-straddle-performance)
- **Pushkar Raj Thakur:** a practitioner backtest of buying a CE+PE straddle or strangle on Budget day — [pushkarrajthakur.com](https://pushkarrajthakur.com/budget-day-strategy-straddle-strangle-backtesting-on-buying-ce-pe-best-option-trading/)
- **Generic Nifty short-straddle backtest statistics:** [TradingTick](https://tradingtick.in/nifty/option-backtesting/nifty-short-straddle-strategy-backtest-results.php); [NiftyTrader backtester](https://www.niftytrader.in/options-trading-backtesting/nifty/nifty)
- **Rolling straddle charts:** StockMojo notes that on the rolling straddle chart, IV crush typically appears within 15–30 minutes of the event — [StockMojo](https://stockmojo.in/straddle-chart)
- **Academic:** negative, significant excess returns on market-neutral Nifty straddles — [IREF 2020](https://www.sciencedirect.com/science/article/abs/pii/S1059056020301222)

### Inferences
- The public evidence is thin and not peer-reviewed at the event level. The engine should produce its own event-conditional backtests from NSE option bhavcopy and intraday data.

### Gaps
- No Sensibull, Stockmock, Opstra or Quantsapp published event backtests (with statistics) were found.
- No backtests for election or RBI-day straddles were found.
