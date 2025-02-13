📌 Buffet AI – Intelligent Stock Valuation

📖 Overview

Buffet AI is an agentic AI system that retrieves stock data from Yahoo Finance using the yfinance API and evaluates whether a stock is overvalued or undervalued based on Warren Buffett’s principles of:
✔ Enterprise Value (EV)
✔ Owner’s Earnings (OE)
✔ Intrinsic Value Calculation

The system provides insights into True P/E Ratio and Rate of Return to help investors make smarter decisions.

⚙️ Features

✅ Fetch real-time stock data using yfinance
✅ Calculate Enterprise Value & Owner’s Earnings
✅ Compute True P/E Ratio (EV/OE)
✅ Determine Rate of Return (1 / True P/E Ratio)
✅ Analyze stock valuation over 2, 5, and 10 years

📥 Installation

Please get a Google Gemini API Key. Instructions are available here: https://ai.google.dev/gemini-api/docs/api-key

1️⃣ Clone this repository:

git clone https://github.com/shashankkotturi/buffet_ai.git
cd buffet-ai

2️⃣ Install dependencies:

pip install -r requirements.txt

3️⃣ Run the script:

python buffet_ai.py

🛠️ How It Works

1️⃣ Enter a stock ticker (e.g., AAPL, PLTR, TSLA)
2️⃣ Buffet AI fetches financial data via yfinance
3️⃣ Calculates Enterprise Value & Owner’s Earnings
4️⃣ Computes True P/E Ratio & Rate of Return
5️⃣ Evaluates if the stock is overvalued or undervalued

📌 Future Enhancements

🔹 Add historical valuation trends
🔹 Implement machine learning predictions
🔹 Connect with Google Gemini API v2 for deeper insights

📩 Contributing

Feel free to fork, submit PRs, or report issues! 🚀

📂 License: MIT