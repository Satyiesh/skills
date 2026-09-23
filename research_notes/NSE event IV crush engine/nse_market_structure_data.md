# NSE F&O Market Structure, Regulation, Costs & Data Sources for an Event-Driven Options Backtester (state as of Sept 2026)

Research notes compiled 2026-09-23. Several primary sites (zerodha.com, support.zerodha.com, icicidirect.com, upstox.com) were blocked by the research proxy, so many figures come from search-result summaries of those pages rather than full fetches. Treat a figure as confirmed only when a primary source (NSE or SEBI circular) is cited. Items from background knowledge that I could not confirm in this session are labelled **[unverified]** and appear only under Inferences or Gaps.

## 1. Contract specifications (stock and index options, expiries, lot sizes, strikes)

### Takeaway
As of 2026, NSE offers **weekly options only on Nifty 50**, and BSE only on **Sensex**. Every other index (BankNifty, FinNifty, MidcpNifty, NiftyNxt50, Bankex, Sensex50) and all single-stock options expire **monthly**. Since Sept 2025, NSE contracts expire on **Tuesday** (weekly Nifty on Tuesdays; monthly on the last Tuesday) and BSE contracts on **Thursday**. Index lot sizes were cut again from the Jan 2026 series: Nifty 65 and BankNifty 30. These cuts were within SEBI's minimum contract value of about ₹15 lakh.

### Cited Findings
- **Expiry weekday (effective Sept 1, 2025):** NSE monthly contracts on NIFTY, BANKNIFTY, FINNIFTY, MIDCPNIFTY, NIFTYNXT50 and **single stocks** expire on the **last Tuesday** of the month. BSE monthly contracts (Sensex, Sensex 50, Bankex) expire on the **last Thursday**. — [ICICI Direct](https://www.icicidirect.com/futures-and-options/articles/revised-expiry-days-for-nse-futures-and-options); [Kotak Neo](https://www.kotakneo.com/news/market-news/sebi-to-end-thursday-expiry/); [News On AIR, Sept 1 2025](https://www.newsonair.gov.in/nse-bse-swap-derivatives-expiry-days)
  - SUPERSEDED: Thursday was the traditional NSE expiry day before Sept 2025 — [Ventura](https://www.venturasecurities.com/blog/changes-in-expiry-nse-and-bse/)
- **One weekly benchmark per exchange (SEBI circular of Oct 1, 2024, effective Nov 20, 2024):** — [Business Standard](https://www.business-standard.com/amp/markets/news/sebi-announces-six-key-changes-to-curb-speculation-in-derivatives-trading-124100101316_1.html); [SEBI circular SEBI/HO/MRD/TPD-1/P/CIR/2024/132 (copy)](https://www.cse-india.com/upload/upload/Oct_011024.pdf)
  - NSE kept **Nifty 50** weeklies. Last weekly expiries: BankNifty Nov 13, 2024; MidcpNifty Nov 18, 2024; FinNifty Nov 19, 2024. Only monthlies remain for these indices. — [Motilal Oswal](https://www.motilaloswal.com/learning-centre/2024/10/nse-discontinues-weekly-derivatives-on-bank-nifty-nifty-midcap-select-and-finnifty); [NSE circular FAOP64506](https://nsearchives.nseindia.com/content/circulars/FAOP64506.pdf)
  - BSE kept only **Sensex** weeklies. Bankex and Sensex 50 weeklies ended; the last Bankex weekly was Nov 18, 2024. — [Motilal Oswal](https://www.motilaloswal.com/learning-centre/2024/10/nse-discontinues-weekly-derivatives-on-bank-nifty-nifty-midcap-select-and-finnifty)
- **Minimum contract value:** SEBI raised the minimum notional of index derivatives to about **₹15 lakh**, up from ₹5–7 lakh (effective Nov 2024). — [Sahi](https://www.sahi.com/blogs/nifty-lot-size-2026-bank-nifty-sensex); [Business Standard](https://www.business-standard.com/amp/markets/news/sebi-announces-six-key-changes-to-curb-speculation-in-derivatives-trading-124100101316_1.html)
- **Index lot sizes from the Jan 2026 series** (NSE circular FAOP70616):
  - Nifty 75 → **65**
  - BankNifty 35 → **30**
  - FinNifty 65 → **60**
  - MidcpNifty 140 → **120**
  - NiftyNxt50 unchanged at **25**
  - Timing: weeklies switched from the Jan 6, 2026 expiry and monthlies from the Jan 27, 2026 expiry. The Dec 2025 contracts kept the old sizes. — [NSE circular FAOP70616](https://nsearchives.nseindia.com/content/circulars/FAOP70616.pdf); [HDFC Sky](https://hdfcsky.com/news/nse-revises-market-lot-sizes-for-major-index-derivatives-effective-january-2026); [Ventura](https://www.venturasecurities.com/blog/nifty-bank-nifty-lot-size-changes-january-2026-know-how-it-impacts-traders/)
  - Sensex lot size in 2026: **20** — [Sahi](https://www.sahi.com/blogs/nifty-lot-size-2026-bank-nifty-sensex)
  - Earlier revision (SUPERSEDED): NSE also changed BankNifty and MidcpNifty lots in a March 2025 circular — [Business Standard, Mar 31 2025](https://www.business-standard.com/amp/markets/capital-market-news/nse-revises-market-lot-sizes-for-nifty-bank-nifty-mid-select-f-o-contracts-125033100440_1.html)
- **Stock F&O eligibility and limits** (SEBI, May 29, 2025 circular):
  - Market-wide position limit (MWPL) = the lower of **15% of free float** or **65× average daily cash volume** across exchanges. Effective **Oct 1, 2025**. — [Business Today](https://www.businesstoday.in/markets/story/sebi-equity-fo-rules-futeq-method-mwpl-risk-management-478321-2025-05-29)
  - NSE publishes the current selection criteria. — [NSE selection criteria page](https://www.nseindia.com/static/products-services/equity-derivatives-selection-criteria)
- **Non-benchmark index eligibility** (effective Nov 3, 2025): at least 14 constituents, no single stock above 20% weight, top three stocks at most 45% combined. — [Business Today](https://www.businesstoday.in/markets/story/sebi-equity-fo-rules-futeq-method-mwpl-risk-management-478321-2025-05-29)

### Inferences
- A backtester needs a **date-versioned contract master** keyed on (underlying, trade date) that holds lot size, expiry weekday rule and weekly/monthly availability. The known regime breaks are Nov 20, 2024 (weeklies cut), Sept 1, 2025 (Tuesday expiry) and the Jan 2026 series (new lots). Lot sizes are revised periodically, usually each half-year.
- For **IV crush on stock earnings**, only monthly stock options exist. The front-month option can therefore have many days to expiry at the event, which dilutes the crush in vega/theta terms. Once the event falls inside the last few days of the series, the next-month contract is the main alternative.
- For **macro events** (RBI MPC, CPI, Budget), Nifty weeklies (Tuesday) and Sensex weeklies (Thursday) are the only short-dated instruments. BankNifty, the natural RBI-sensitive underlying, now has only monthly options.
- [unverified] Stock options are **European-style** and **physically settled** at expiry. This has been NSE practice since the 2018–2019 phased move to physical settlement. Index options are cash-settled. ITM stock options held into expiry therefore become delivery obligations.
- [unverified] Strike intervals are set per underlying by NSE and published in the contract master and circulars. Nifty uses 50-point strikes, with 100-point strikes on far strikes/tenors. I did not fetch the current strike-scheme circular.

### Gaps
- I did not obtain the current NSE strike-interval scheme for stocks or indices in 2026.
- I could not confirm the current stock-option physical-settlement circular text, or the 2026 stock lot-size revision list. NSE publishes the latter as the "fo_mktlots.csv" archive. [unverified]
- I found no source on whether BSE changed the Sensex weekly day after Sept 2025 beyond "Thursday".

## 2. SEBI F&O regulatory changes 2024–2026 and implications for event strategies

### Takeaway
The Oct 2024 package brought in a series of measures between Nov 2024 and Apr 2025:
- upfront premium collection
- +2% extreme loss margin (ELM) on short options on expiry day
- no calendar-spread margin benefit on expiry day
- intraday position-limit monitoring
- the larger contract sizes and single weekly benchmark covered in Section 1

A 2025 package followed:
- delta/futures-equivalent open interest (OI)
- new MWPL
- intraday position limits of ₹5,000 cr net FutEq per entity in index options (from Oct 1, 2025)
- pre-open session for F&O (from Dec 2025)

Budget 2026 raised STT, effective Apr 1, 2026. In Sept 2026 SEBI was consulting on VWAP-based settlement and closing-auction changes.

### Cited Findings
- **Upfront premium:** the full option premium must be collected from buyers upfront, from Feb 1, 2025. — [Fyers notice](https://fyers.in/notice-board/sebi-announces-significant-reforms-in-equity-index-derivatives-framework/); [Marketfeed](https://www.marketfeed.com/read/en/understanding-sebis-new-rules-and-their-impact-on-indian-options-trading)
- **Expiry-day ELM:** an extra **2% ELM on short options** on expiry day, from **Nov 20, 2024**. — [Fyers](https://fyers.in/notice-board/sebi-announces-significant-reforms-in-equity-index-derivatives-framework/)
- **Calendar spread:** no margin benefit for calendar spreads on expiry day, from **Feb 10, 2025**. — [ICICI Direct](https://www.icicidirect.com/futures-and-options/articles/calendar-spreads-in-f-o-after-sebi-s-new-rules-what-you-need-to-know)
- **Intraday position-limit monitoring** was part of the Oct 2024 package (effective Apr 2025). — [Business Standard](https://www.business-standard.com/amp/markets/news/sebi-announces-six-key-changes-to-curb-speculation-in-derivatives-trading-124100101316_1.html)
- **Delta-based (FutEq) OI** replaced notional OI (SEBI circular of May 2025). — [Bajaj Broking](https://www.bajajbroking.in/blog/sebi-notifies-new-f-and-o-rules-with-higher-index-limits-and-risk-measures); [Kotak Neo](https://www.kotakneo.com/bulletins/sebi-new-f-o-rules-explained-delta-based-oi-new-mwpl-what-it-means-for-your-trading/)
  - Index options end-of-day limits: net FutEq **₹1,500 cr**, gross long and short **₹10,000 cr** each. — [Bajaj Broking](https://www.bajajbroking.in/blog/sebi-notifies-new-f-and-o-rules-with-higher-index-limits-and-risk-measures)
- **Intraday position limit** (SEBI circular of Sept 1, 2025): net intraday FutEq position capped at **₹5,000 cr per entity** in index derivatives, effective **Oct 1, 2025**. — [Business Standard](https://www.business-standard.com/markets/news/sebi-stricter-intraday-position-limits-options-market-regulation-125090200971_1.html); [Outlook Money](https://www.outlookmoney.com/invest/equity/sebi-outlines-new-framework-for-monitoring-of-intraday-position-limits-for-index-derivatives)
- **Expiry-day breach penalties** apply from Dec 6, 2025. — [Business Standard summary via search](https://www.business-standard.com/markets/capital-market-news/sebi-overhauls-f-o-regulations-to-boost-risk-monitoring-and-market-alignment-125053000758_1.html)
- **Single-stock position limits and MWPL monitoring:**
  - Individuals are capped at 10% of MWPL, proprietary traders at 20%, FPIs and brokers at 30%. — [Business Today](https://www.businesstoday.in/markets/story/sebi-equity-fo-rules-futeq-method-mwpl-risk-management-478321-2025-05-29)
  - Intraday MWPL checks happen at least four random times a day, from Nov 3, 2025. — [same](https://www.businesstoday.in/markets/story/sebi-equity-fo-rules-futeq-method-mwpl-risk-management-478321-2025-05-29)
- **Pre-open session in F&O:** applies to current-month futures from Dec 6, 2025, and to next-month contracts in the 5 days before expiry. — [Business Today](https://www.businesstoday.in/markets/story/sebi-equity-fo-rules-futeq-method-mwpl-risk-management-478321-2025-05-29)
- **Sept 2026 consultation (proposal only, not in force):**
  - SEBI paper of Sept 12, 2026 on the closing auction session, derivative settlement price (a blended VWAP) and market timings. Comments are due Oct 3, 2026. — [Dynamite News](https://www.dynamitenews.com/business/sebis-big-fo-move-new-expiry-rules-could-change-trading-forever) (secondary, low-tier source; confirm on sebi.gov.in)
  - In Sept 2025 there was talk that SEBI was weighing an end to weekly contracts. BSE shares fell on it, but no such rule has been confirmed. — [Business Standard](https://www.business-standard.com/markets/capital-market-news/bse-tumbles-on-buzz-sebi-weighs-end-of-weekly-f-o-contracts-125091100596_1.html)
- **Motivation:** 9.25 million individuals lost ₹51,689 cr in NSE index derivatives in FY24. — [Business Standard](https://www.business-standard.com/amp/markets/news/sebi-announces-six-key-changes-to-curb-speculation-in-derivatives-trading-124100101316_1.html)

### Inferences
- **Short-vol event trades** (selling a straddle or strangle into results or RBI policy) that are held to expiry day face +2% ELM. Calendar trades (short front, long next) also lose their spread benefit on expiry day. The margin model should switch regimes on expiry day.
- **The pre-open session** in derivatives from Dec 2025 changes the price at which a post-event open can be modelled. Pre- and post-Dec-2025 opening fills should not be treated the same way.
- **Proposed VWAP-based settlement** would change how the final expiry-day payoff is computed if adopted. The engine should keep the settlement-price rule pluggable.
- **Position limits** (₹5,000 cr intraday FutEq) are irrelevant to retail and small-fund sizes, but matter for delta-hedged book simulation at scale.

### Gaps
- I did not fetch primary SEBI circular PDFs for the May 2025 or Sept 2025 circulars. Dates come from secondary coverage.
- I did not confirm whether the Sept 2026 consultation has been finalised.

## 3. Transaction costs

### Takeaway
From **Apr 1, 2026**, STT on options is:
- **0.15% of premium on the sell side** (was 0.10%)
- **0.15% of intrinsic value on exercised options** (was 0.125%)

STT on futures rose from 0.02% to 0.05% of turnover. Other charges on each order:
- **NSE exchange transaction charge on options:** 0.03503% of premium (since Oct 1, 2024)
- **Discount-broker brokerage:** about ₹20 per order
- plus stamp duty, GST and SEBI fees

Bid-ask spreads for stock options, which usually dominate costs, were not quantified in any source I found.

### Cited Findings
- **Budget 2026 STT (effective Apr 1, 2026):**
  - Options sell side: **0.10% → 0.15% of premium**
  - Futures: **0.02% → 0.05%**
  - Exercised options: **0.125% → 0.15% of intrinsic value**
  - Sources: [Upstox explainer](https://upstox.com/news/personal-finance/tax/explained-how-the-stt-hike-on-equity-futures-and-options-affects-traders-and-investors/article-189260/); [Finnovate](https://www.finnovate.in/learn/blog/budget-2026-stt-hike-fno-trades-explained); [ClearTax](https://cleartax.in/s/securities-transaction-tax-stt); [Motilal Oswal](https://www.motilaloswal.com/learning-centre/2026/2/union-budget-2026-27-stt-update-and-market-impact-analysis)
  - Worked example of exercise STT on intrinsic value: Nifty 24,800 CE settling at 25,000 gives ₹200 intrinsic per unit, so 0.15% × 200 × 65 = ₹19.50 per lot. — [Finnovate](https://www.finnovate.in/learn/blog/budget-2026-stt-hike-fno-trades-explained)
  - STT collections rose 53% to ₹40,214 cr in FY27 to date after the hike. — [Business Standard, Sept 2026](https://www.business-standard.com/amp/markets/news/stt-collections-surge-53-to-40-214-crore-in-fy27-after-rate-hike-126091801033_1.html)
- **SUPERSEDED rates:**
  - Oct 1, 2024 – Mar 31, 2026: options sell 0.10% of premium; futures 0.02%; exercised options 0.125% of intrinsic value. — [Zerodha Z-Connect](https://zerodha.com/z-connect/business-updates/revision-in-exchange-transaction-charges-and-securities-transaction-tax-from-october-1-2024); [Accelpix/Zerodha calculator summary](https://accelpix.com/brokerage-calculator/brokers/zerodha.html)
  - Before Oct 2024: options sell 0.0625% and futures 0.0125%. The rise was announced in Budget July 2024. — [Business Standard](https://www.business-standard.com/amp/markets/news/budget-2024-hikes-ltcg-tax-rate-to-12-5-stcg-to-20-stt-on-f-o-also-up-124072300553_1.html)
- **NSE exchange transaction charge:** **₹35.03 per lakh of premium (0.03503%)** on each side for equity options, flat under SEBI's "true-to-label" circular of Jul 1, 2024. Effective Oct 1, 2024; this replaced the earlier volume-slab rebates. — [NSE intimation](https://nsearchives.nseindia.com/corporate/BSE_27092024184037_NSEintimation.pdf); [TeamLease RegTech](https://www.teamleaseregtech.com/updates/article/35552/nse-issued-the-revised-in-transaction-charges/); [Pinnacle charges sheet](https://www.pinnacletrades.com/pdf/Charges01-10-2024.pdf)
  - NSE has issued later transaction-charge circulars (e.g., FA73061). The current rate may differ; verify. — [NSE circular FA73061](https://nsearchives.nseindia.com/content/circulars/FA73061.pdf)
- **Brokerage:** Zerodha charges a flat ₹20 per executed options order. — [Chittorgarh Zerodha review 2026](https://www.chittorgarh.com/stockbroker/zerodha/18/); [Zerodha charges page (listed)](https://zerodha.com/charges/)

### Inferences
- **Cost model per fill:**
  - brokerage ₹20
  - exchange transaction charge 0.03503% × premium turnover (NSE)
  - STT 0.15% × premium on sells only (post Apr 1, 2026)
  - stamp duty on buys
  - SEBI fee
  - GST at 18% on (brokerage + exchange transaction charge + SEBI fee)
  - at expiry: exercise STT 0.15% × intrinsic × quantity on ITM long options
- [unverified, from background knowledge] Stamp duty is 0.003% on the options buy side and SEBI turnover fee is ₹10 per crore.
- **Exercise STT versus closing out:** exercise STT is charged on intrinsic value, while a close-out sale is charged on premium at the same 0.15%. Since Apr 2026 both rates are equal, so the old "STT trap" is gone. Near-expiry, closing is roughly equal-cost or cheaper once exchange charges are included. Stock options also carry physical delivery, so closing before expiry dominates.
- **Short-premium event trades pay STT on the sell leg.** The 50% STT hike raises the cost of short-vol IV-crush trades more than long-vol run-up trades.

### Gaps
- Could not fetch the Zerodha charges page (proxy block) to confirm the current stamp duty, SEBI fee and IPFT rates, the BSE options transaction charge, or any 2025–26 revision of the NSE charge.
- **No quantitative source found** for bid-ask spreads in stock options versus index options. This must be measured from tick/quote data or broker L1 snapshots. Nifty weekly ATM spreads are typically a few paise to ₹0.5; many single-stock options have wide spreads and thin far strikes [unverified].

## 4. Margin (SPAN + exposure; straddles vs spreads)

### Takeaway
Upfront margin for a short option is NSE Clearing's **SPAN** requirement plus **exposure margin**, plus **+2% ELM on expiry day** since Nov 2024. SPAN is the worst loss across a 16-scenario price/volatility grid run on the whole portfolio. Hedged spreads on the same underlying get large reductions because their worst-case loss is capped. Naked straddles and strangles carry full SPAN plus exposure on both legs, less some offset between the legs.

### Cited Findings
- SPAN, run by NSE Clearing, charges the worst loss across **16 price/volatility scenarios** for the portfolio. — [OneTradeJournal](https://onetradejournal.com/glossary/span-margin)
- Total margin = SPAN + exposure. Exposure is roughly 1.5–5% of contract value. — [CapMint](https://www.capmint.com/learn/glossary/option-margin); [Sahi](https://www.sahi.com/blogs/9-margins-and-capital-requirements)
- Hedges reduce margin only within the same underlying. Hedged spreads get large benefits because their loss is capped. — [5paisa](https://www.5paisa.com/blog/margin-benefits-hedged-option-positions)
- Expiry-day +2% ELM on short options and the loss of the calendar-spread benefit are described in Section 2. — [Fyers](https://fyers.in/notice-board/sebi-announces-significant-reforms-in-equity-index-derivatives-framework/); [ICICI Direct](https://www.icicidirect.com/futures-and-options/articles/calendar-spreads-in-f-o-after-sebi-s-new-rules-what-you-need-to-know)
- NSE publishes daily SPAN risk-parameter files. Open-source tools such as "Marginism" can compute SPAN in Python from them. — [Marketcalls](https://www.marketcalls.in/python/python-tutorial-on-span-margin-calculator-using-marginism.html)

### Inferences
- For backtests, the most practical route is to **approximate margin**: SPAN from the NSE daily span files, or a scenario-grid re-implementation, plus exposure at an index or stock percentage. On expiry days, add the 2% ELM on short-option notional. Defined-risk structures (iron fly/condor) as event-short trades need roughly 3–5× less capital than naked straddles [directional claim from the hedging-benefit sources; ratio unverified].
- [unverified] Peak-margin rules (four intraday snapshots, in force since 2021) mean intraday-opened positions must be fully margined too. The "intraday leverage" assumption is not valid.
- For stock options, physical settlement brings **delivery margins** that rise in the final days before expiry [unverified]. This is another reason to exit stock-option event positions before expiry week.

### Gaps
- I found no source giving current exposure-margin percentages for 2026 (index vs stock), or the delivery-margin schedule for stock F&O near expiry.
- I found no worked 2026 rupee example of straddle vs iron-fly margin from a primary source.

## 5. Historical and real-time data sources

### Takeaway
- **EOD:** the NSE F&O bhavcopy is free. It moved to the **UDiFF common bhavcopy format on Jul 8, 2024**, and community archives cover 2020 onward.
- **Intraday history of expired options** (needed for IV crush backtests) is scarce. The most accessible retail sources in 2026:
  - **Upstox Expired Instruments API** (1-min to daily OHLC on expired option contracts; Upstox Plus plan)
  - **Dhan Expired Options Data API** (5 rolling years, ATM ±10 strikes, including IV and OI)
- Paid vendors (TrueData, GDFL, TickData) sell deeper tick or minute history, sometimes only under institutional licensing.

### Cited Findings
- **NSE UDiFF bhavcopy:** the "F&O-UDiFF Common Bhavcopy Final" replaced the legacy CSV from **Jul 8, 2024** (NSE circular 62424 of Jun 12, 2024).
  - URL pattern: `https://archives.nseindia.com/content/fo/BhavCopy_NSE_FO_0_0_0_YYYYMMDD_F_0000.csv.zip`
  - A community data bank holds validated archives from Apr 13, 2020 to Aug 31, 2026 (about 1.2 GB).
  - Sources: [GitHub NSE-FNO-Data-bank](https://github.com/SantoshSrinivas79/NSE-FNO-Data-bank); [NSE all reports – derivatives](https://www.nseindia.com/all-reports-derivatives)
- **Libraries:** `jugaad-data` (Python, `bhavcopy_fo_save`) and the R package `nser` (F&O bhavcopy from Jan 1, 2020). — [jugaad-data](https://github.com/jugaad-py/jugaad-data); [nser](https://cran.r-project.org/web/packages/nser/nser.pdf)
- **Upstox:**
  - The Expired Historical Candle Data API returns OHLC for expired contracts at 1, 3, 5, 15 and 30 minute and daily intervals. Expired instrument keys come from the Get Expired Option Contracts API. — [Upstox docs](https://upstox.com/developer/api-documentation/get-expired-historical-candle-data/); [Expired Instruments](https://upstox.com/developer/api-documentation/expired-instruments/)
  - These APIs sit within the **Upstox Plus** plan. — [Upstox announcement](https://upstox.com/developer/api-documentation/announcements/expired-instruments-api/)
- **Dhan:**
  - The Expired Options Data API gives the **last 5 years** on a rolling basis, **ATM and up to 10 strikes above and below**, with OHLC, **IV**, volume, OI and spot. — [DhanHQ v2 docs](https://dhanhq.co/docs/v2/expired-options-data/)
  - Intraday candles come at 1, 5, 15, 25 and 60 minutes; daily history goes back to instrument inception. — [DhanHQ historical data](https://dhanhq.co/docs/v2/historical-data/); [Dhan support](https://dhan.co/support/platforms/dhanhq-api/what-timeframe-data-is-available-through-dhan-s-historical-data-apis/)
- **Kite Connect (Zerodha):** candle data for **expired options** has historically not been available through the historical API. The developer forum thread discusses workarounds. — [Kite forum](https://kite.trade/forum/discussion/14374/how-to-fetch-candlestick-data-for-expired-options)
- **GDFL (Global Datafeeds):** an authorised distributor with APIs for real-time, historical, snapshot and option chain/Greeks data. — [GDFL docs](https://globaldatafeeds.in/global-datafeeds-apis/global-datafeeds-apis/introduction/type-of-data-available/)
  - The NimbleData product offers about 2 months of 1-min intraday history, 2 days of ticks and EOD since 2010. — [TradersGurukul listing](https://tradersgurukul.com/product/56717/gdfl-nimbledata-proplus-cash-or-f-o-)
- **TrueData:** an authorised NSE/BSE/MCX vendor with WebSocket and REST APIs and an option chain with Greeks. — [TrueData](https://www.truedata.in/); [TrueData APIs](https://www.truedata.in/market-data-apis)
  - A user report says TrueData will not sell options history to individuals (anecdotal). — [TradingQnA thread](https://tradingqna.com/t/which-is-the-best-source-for-options-historical-data/176182)
- **Institutional tick data:** TickData offers NSE data. — [TickData NSE](https://www.tickdata.com/equity-data/national-stock-exchange-of-india)
- **Kaggle:** community NSE F&O 1-minute datasets exist (quality and licensing unverified). — [Kaggle](https://www.kaggle.com/general/545727)

### Inferences
- **Recommended stack:**
  1. The NSE UDiFF bhavcopy, plus pre-2024 legacy bhavcopies, for EOD settle/close, OI and the full strike universe. This supports daily-granularity IV-crush studies across all stocks.
  2. Dhan expired-options data (which includes IV) or Upstox expired candles for intraday event windows over the last ~5 years.
  3. A paid vendor (GDFL/TrueData/TickData) if bid-ask quotes are needed. None of the retail APIs above provide historical **quotes**; they provide trade OHLC. Bid-ask modelling therefore needs a paid source or self-recorded live snapshots.
- EOD bhavcopy "close" for illiquid stock options is often stale (last trade). Use "settle price" with caution and filter on contracts traded and OI.
- **India VIX history** is downloadable from NSE's historical index data pages [unverified; not fetched].

### Gaps
- Current 2026 pricing for TrueData, GDFL, Accelpix, ICharts, Fyers, Breeze (ICICI) historical options data was not retrieved. The ICICI, Upstox and Zerodha sites were blocked.
- Fyers, Breeze and Accelpix expired-contract coverage is unverified.
- I did not verify the exact NSE URL for the India VIX historical CSV.

## 6. Event calendar sources (results, RBI, CPI, Budget, elections)

### Takeaway
- **Corporate results dates:** NSE's board-meetings page and corporate-announcement feeds. There is no official public API; people use scraping libraries (e.g., the `nse` Python package) or paid scrapers/vendors (Anakin, Apify, TrueData announcements).
- **RBI:** publishes the MPC calendar annually; FY27 meetings start Apr 6–8, 2026 and end Feb 3–5, 2027.

### Cited Findings
- **NSE board meetings:** the page lists board-meeting notices, including results dates. — [NSE Board Meetings](https://www.nseindia.com/static/investor-relations/board-meetings)
- **Python `nse` package:** has methods for board meetings over a date range and for financial results (quarterly, annual, half-yearly). — [NseIndiaApi docs](https://bennythadikaran.github.io/NseIndiaApi/api.html)
- **Paid/managed options:** Anakin.io endpoints for upcoming board meetings and earnings dates; the Apify NSE/BSE announcements scraper; TrueData's categorised announcements feed. No official financial-info API exists. — [Anakin](https://anakin.io/catalog/nse_india); [Apify](https://apify.com/nexgendata/nse-bse-announcements/api/python); [TrueData](https://www.truedata.in/products/marketdataapi)
- **RBI MPC FY2026-27:** six meetings, announced Mar 23, 2026. The first is Apr 6–8, 2026, the second Jun 3–5, then August, October, December, and the last Feb 3–5, 2027. — [Angel One](https://www.angelone.in/news/economy/rbi-releases-mpc-meeting-calendar-for-fy27-what-you-need-to-know); [5paisa](https://www.5paisa.com/blog/rbi-mpc-meeting-schedule); [News On AIR, Apr 8 2026](https://www.newsonair.gov.in/rbi-to-announce-its-first-bi-monthly-monetary-policy-statement-for-financial-year-2026-27-today)
  - Previous year: the FY26 first decision was Apr 9, 2025. — [Business Standard](https://www.business-standard.com/amp/economy/news/rbi-announces-mpc-schedule-for-fy26-first-rates-decision-on-april-9-125032600957_1.html)
  - A Feb 4, 2026 MPC meeting took place. — [News On AIR](https://www.newsonair.gov.in/rbi-to-hold-monetary-policy-committee-meeting-today/)

### Inferences
- **Results dates:** the event timestamp matters. Indian companies often announce results after market hours, or during market hours on the board-meeting day. The engine should record the actual filing time from NSE/BSE announcement timestamps, not just the board-meeting date. Scraped historical board-meeting data should be snapshotted, because companies revise dates.
- **Macro events:** RBI announcements fall on the last day of the MPC window at about 10:00 IST [unverified]. This is intraday, so IV crush is realised within the session.

### Gaps
- Exact FY27 August, October and December MPC dates were not retrieved; the Upstox page was blocked.
- Not researched in this session:
  - the MOSPI CPI release calendar (typically the 12th of each month at 16:00 IST [unverified]) and the MOSPI advance release calendar URL
  - Union Budget dates (by convention Feb 1 [unverified])
  - ECI election schedules
- I found no source on the BSE announcements API.

## 7. Risk-free rate, dividends, India VIX methodology

### Takeaway
NSE's India VIX uses a CBOE-style variance-swap method on near and next-month Nifty OTM option bid/ask quotes. It uses the **NSE MIBOR of the relevant tenor (30-day or 90-day)** as the risk-free rate, measures time to expiry in minutes, and interpolates to a 30-day constant maturity. MIBOR is therefore a defensible, exchange-consistent choice for r in BSM/Black-76 pricing.

### Cited Findings
- India VIX follows CBOE methodology adapted to the Nifty order book:
  - Rate: the relevant-tenor NSE MIBOR (30 or 90 days) for each expiry.
  - Inputs: best bid/ask of OTM near and next-month Nifty options.
  - Time: to expiry in minutes.
  - Output: variances interpolated to 30 days, then √ × 100.
  - Sources: [NSE India VIX computation methodology](https://nsearchives.nseindia.com/web/sites/default/files/inline-files/India_VIX_comp_meth.pdf); [NSE white paper](https://nsearchives.nseindia.com/web/sites/default/files/inline-files/white_paper_IndiaVIX.pdf)

### Inferences
- **Recommended convention:** use the Black-76 model on the synthetic forward implied by put-call parity at each expiry, or on the matching futures price. This removes the need for explicit dividend and repo inputs, which matters for single stocks where ex-dividend dates can fall inside the option's life. BSM with explicit discrete dividends is the fallback when futures or parity data are missing.
- **Rate choice:** MIBOR (overnight or term) or the 91-day T-bill yield. The choice changes IV only marginally at the short tenors involved in event trades.
- **Post-2025 VIX weeklies:** NSE Nifty weeklies expire on Tuesday. Whether the VIX "near/next" still means weekly contracts should be checked against the current methodology PDF [unverified].

### Gaps
- I did not verify whether NSE updated the VIX methodology after the weekly/Tuesday changes.
- I found no source on current MIBOR or T-bill levels in 2026, or on NSE's treatment of dividends in any published IV.
