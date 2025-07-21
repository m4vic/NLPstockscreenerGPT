# 🧠 Natural Language StockFinder (Mini Project)

This is a simple prototype project where you can ask questions about stocks using natural language (like chatting), and the AI (Gemini API) will try to answer based on saved stock data.

It’s just a basic test — not a real-time screener or trading app. It's built with Python, and uses Gemini API + yFinance to show how AI can help in stock analysis.

---

## 🧩 What’s Inside

- `StockScrapper.py` – collects stock data from yFinance and saves it
- `StockFinder-GPT.py` – chatbot that lets you ask about stocks using Gemini AI

---

## 📦 What You Need

- Python 3.8 or higher
- Gemini API key (very important) Its FREE
- Some basic Python knowledge (or just follow the steps below)

pip install pandas yfinance beautifulsoup4 requests google-generativeai regex

## 🔧 How to Use (Step by Step)
## Step 1: Copy the Files
Make sure you have these two scripts:

StockScrapper.py

StockFinder-GPT.py

You can put them in the same folder for simplicity.

## Step 2: Add Your Gemini API Key
To use the chatbot, you must add your Gemini API key. You can set it like this:

On Mac/Linux:

bash
Copy
Edit
export GEMINI_API_KEY=your_api_key_here
On Windows (CMD):

cmd
Copy
Edit
set API_KEY=your_api_key_here
Or if you're editing the Python file directly, find the section in StockFinder-GPT.py that loads the API key and paste your key there like this:

python StockScrapper.py
## Step 3: Set the DB Path in Finder Script
Now go to StockFinder-GPT.py and look for where the database path is written.

DB_PATH = "stocks.db"
Make sure the file name/path matches the .db file created by the scrapper. If you moved the file, update the path accordingly.

## Step 4: Run the Chatbot!
Now just run:

bash
Copy
Edit
python3 StockFinder-GPT.py
Start asking:

“Which stock is good for long term?”

“Compare Infosys and TCS”

“Find low PE stocks from banking sector”

The AI will use the saved data and give you answers.

💡 Things to Remember
🔒 Gemini API key is required (it powers the AI responses)

📁 Database path (stocks.db) must match in both scripts

🕐 This is not live data — it’s static, only from the day you scraped it

💬 You can ask follow-up questions too — it keeps the context

🧪 Why I Made This
I wanted to test how LLMs (like Gemini) can work with stock data, and how we can build simple tools using just Python and logic. I’m learning deep learning, LangChain, and more — this is one step in my learning path.

🛑 Disclaimer
This is not for real-time trading or financial advice. Just a test / prototype project for learning purposes.

✅ Done!
You're ready to go. Scrape, chat, explore.
If you get stuck, check your API key or database path — they are the most common issues.



