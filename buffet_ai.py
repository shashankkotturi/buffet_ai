import google.generativeai as genai
import yfinance as yf
import json

# Set up Google Gemini API
GEMINI_API_KEY = "GEMINI API KEY"
genai.configure(api_key=GEMINI_API_KEY)

def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info

    financials = stock.quarterly_financials
    # print(financials)

    operating_income = financials.loc['Operating Income'].iloc[:4].sum() if 'Operating Income' in financials.index else financials.loc['Net Income'].iloc[:4].sum()

    
    # Writing to a file
    filename = ticker + ".json"
    with open(filename, "w") as file:
        json.dump(info, file, indent=4)

    return {
        # Basic Company Info
        "ticker": ticker,
        "name": info.get("longName", "N/A"),
        "industry": info.get("industry", "N/A"),
        "sector": info.get("sector", "N/A"),
        "country": info.get("country", "N/A"),
        "employees": info.get("fullTimeEmployees", "N/A"),
        "website": info.get("website", "N/A"),
        "description": info.get("longBusinessSummary", "N/A"),

        # Stock Performance
        "current_price": info.get("currentPrice", 0),
        "previous_close": info.get("previousClose", 0),
        "52_week_high": info.get("fiftyTwoWeekHigh", 0),
        "52_week_low": info.get("fiftyTwoWeekLow", 0),
        "50_day_avg": info.get("fiftyDayAverage", 0),
        "200_day_avg": info.get("twoHundredDayAverage", 0),
        "market_cap": info.get("marketCap", 0),
        "beta": info.get("beta", 0),
        "trailing_PE": info.get("trailingPE", 0),
        "forward_PE": info.get("forwardPE", 0),

        # Financials
        "total_revenue": info.get("totalRevenue", 0),
        "net_income": info.get("netIncomeToCommon", 0),
        "free_cashflow": info.get("freeCashflow", 0),
        "operating_cashflow": info.get("operatingCashflow", 0),
        "total_debt": info.get("totalDebt", 0),
        "total_cash": info.get("totalCash", 0),
        "debt_to_equity": info.get("debtToEquity", 0),
        "operating_income": operating_income,

        # Owner's Earnings Calculation
        "depreciation": info.get("depreciation", 0),
        "capex": info.get("capitalExpenditures", 0),
        "owners_earnings": (operating_income + info.get("depreciation", 0) - info.get("capitalExpenditures", 0)),

        # Enterprise Value Calculation
        "enterprise_value": info.get("enterpriseValue", 0),

        # Share Details
        "shares_outstanding": info.get("sharesOutstanding", 0),
        "float_shares": info.get("floatShares", 0),
        "held_by_insiders": info.get("heldPercentInsiders", 0),
        "held_by_institutions": info.get("heldPercentInstitutions", 0),

        # Analyst Ratings
        "analyst_mean_target": info.get("targetMeanPrice", 0),
        "analyst_high_target": info.get("targetHighPrice", 0),
        "analyst_low_target": info.get("targetLowPrice", 0),
        "recommendation": info.get("recommendationKey", "N/A"),
    }

def calculate_intrinsic_value(financials, growth_rate):
    """Calculates the intrinsic value of the stock using Buffett’s principles."""
    ev = financials["enterprise_value"]
    oe = financials["owners_earnings"]
    # print(oe)
    shares = financials["shares_outstanding"]

    if shares == 0:
        return 0  # Avoid division by zero

    # Buffett-style intrinsic value calculation
    intrinsic_value = ((oe * growth_rate) + ev) / shares
    return intrinsic_value

def analyze_stock(financials):
    """Determines if the stock is undervalued or overvalued based on different timeframes."""
    current_price = financials["current_price"]

    # Growth factors (rough estimations based on historical trends)
    growth_rates = {
        "2_years": 1.10,   # 10% assumed growth
        "5_years": 1.30,   # 30% assumed growth
        "10_years": 1.70,  # 70% assumed growth
    }

    intrinsic_values = {
        timeframe: calculate_intrinsic_value(financials, rate)
        for timeframe, rate in growth_rates.items()
    }

    valuation = {
        timeframe: "Undervalued" if intrinsic_values[timeframe] > current_price else "Overvalued"
        for timeframe in intrinsic_values
    }

    return intrinsic_values, valuation

def summarize_financials(data, intrinsic_values, valuation):

    # Prevent division by zero
    if data['owners_earnings'] == 0:
        true_pe_ratio = None
        rate_of_return = None
    else:
        true_pe_ratio = data['enterprise_value'] / data['owners_earnings']
        rate_of_return = 1 / true_pe_ratio

    """Use Gemini AI to summarize the financials in Buffett-style language"""
    prompt = f"""
    Based on Warren Buffett’s investment principles, analyze {data['ticker']}:

    - Current Price: ${data['current_price']:,}
    - Enterprise Value (EV): ${data['enterprise_value']:,}
    - Owner’s Earnings (OE): ${data['owners_earnings']:,}

    Intrinsic Value Estimates:
    - 2-Year: ${intrinsic_values['2_years']:.2f} ({valuation['2_years']})
    - 5-Year: ${intrinsic_values['5_years']:.2f} ({valuation['5_years']})
    - 10-Year: ${intrinsic_values['10_years']:.2f} ({valuation['10_years']})

    True P/E Ratio and Rate of Return:
    - True P/E Ratio: ${true_pe_ratio}
    - Annual Rate of Return: ${rate_of_return}

    Explain in simple terms whether this stock is a good value investment. Please compare the annual rate of return against the S&P 500 annual rate of return.
    """

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    
    return response.text

def chatbot():
    print("Welcome to the Buffett-Style AI Stock Analyzer!")
    while True:
        ticker = input("\nEnter a stock ticker (or 'exit' to quit): ").strip().upper()
        if ticker == "EXIT":
            print("Goodbye!")
            break
        
        try:
            financials = get_stock_data(ticker)
            intrinsic_values, valuation = analyze_stock(financials)
            summary = summarize_financials(financials, intrinsic_values, valuation)

            print("\n===== Financial Analysis =====")
            print(f"Current Price: ${financials['current_price']:,}")
            print(f"Enterprise Value (EV): ${financials['enterprise_value']:,}")
            print(f"Owner’s Earnings (OE): ${financials['owners_earnings']:,}")

            print("\n===== Intrinsic Value Analysis =====")
            for period in ["2_years", "5_years", "10_years"]:
                print(f"{period.replace('_', ' ').title()}: ${intrinsic_values[period]:.2f} ({valuation[period]})")

            print("\n===== Buffett-Style Summary =====")
            print(summary)
        except Exception as e:
            print("Error fetching data. Please try again.", str(e))

if __name__ == "__main__":
    chatbot()