import sqlite3
from google import genai
from google.genai import types
import time
import re

class NLPStockScreener:
    """
    A simplified ChatGPT-like stock screener that:
    1. Connects to a stock database
    2. Uses Google's Gemini AI to provide conversational responses
    3. Maintains conversation context
    4. Provides stock recommendations based on user queries
    """
    
    def __init__(self, api_key: str, db_path: str):
        """
        Initialize the stock screener
        
        Args:
            api_key: Google Gemini API key
            db_path: Path to SQLite database containing stock data
        """
        # Set up AI client
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.5-flash"
        
        # Database connection
        self.db_path = db_path
        
        # Memory for conversation
        self.conversation_history = []  # Stores previous messages
        self.current_stocks = []       # Currently loaded stock data
        
        # Instructions for the AI on how to behave
        self.system_prompt = """
You are a friendly stock market expert. You help users find good stocks to invest in.

Your database contains Indian stocks with these details:
- symbol, name, sector, industry
- market_cap, pe_ratio, pb_ratio, roe
- debt_to_equity, current_ratio, revenue_growth
- net_profit_margin, dividend_yield, price, volume

Be conversational, friendly, and give specific stock recommendations with reasons.
"""

    def connect_to_database(self):
        """
        Create a connection to the SQLite database
        Returns: sqlite3.Connection object
        """
        return sqlite3.connect(self.db_path)

    def search_stocks(self, user_query: str):
        try:
            # Connect to database
            conn = self.connect_to_database()
            cursor = conn.cursor()
            
            # Decide what SQL query to run based on user's words the create_sql_query will writen the qeury and  than save it to sql_query
            sql_query = self.create_sql_query(user_query)
            
            # Execute the query using cursor.execute 
            cursor.execute(sql_query) 
            
            # Get column names of the companies 0th index one by one save in column as list . # it will return all columns names
            columns = [description[0] for description in cursor.description]
            
            # Convert results to list of dictionaries  , 
            results = []
            for row in cursor.fetchall(): # cursor.fetchall() retrieves all rows from the result set.Each row is a tuple of values (e.g., ("ITC", 195.12)).
                stock_dict = dict(zip(columns, row)) # save one by one with key value and the row value zip(columns, row) pairs each column name with the corresponding value from the row.
                results.append(stock_dict) # append the result vy this dict 
            
            conn.close()
            return results 
            
        except Exception as e:
            print(f"Database error: {e}")
            return []

    def create_sql_query(self, user_query: str) -> str:
        query = user_query.lower() # query the is saved in lower case 
        
        # Look for keywords and return appropriate SQL
        if any(word in query for word in ['value', 'cheap', 'undervalued']):
            # Value stocks: low PE, low PB, good ROE
            return """
            SELECT * FROM stocks 
            WHERE pe_ratio < 15 AND pb_ratio < 2 AND roe > 10 
            ORDER BY pe_ratio ASC 
            LIMIT 15
            """
        
        elif any(word in query for word in ['growth', 'growing', 'high growth']):
            # Growth stocks: high revenue growth, good ROE
            return """
            SELECT * FROM stocks 
            WHERE revenue_growth > 15 AND roe > 20 
            ORDER BY revenue_growth DESC 
            LIMIT 15
            """
        
        elif any(word in query for word in ['dividend', 'income', 'yield']):
            # Dividend stocks: high dividend yield
            return """
            SELECT * FROM stocks 
            WHERE dividend_yield > 2 
            ORDER BY dividend_yield DESC 
            LIMIT 15
            """
        
        elif any(word in query for word in ['safe', 'stable', 'low risk']):
            # Safe stocks: low debt, good liquidity, decent ROE
            return """
            SELECT * FROM stocks 
            WHERE debt_to_equity < 0.5 AND current_ratio > 1.5 AND roe > 10 
            ORDER BY debt_to_equity ASC 
            LIMIT 15
            """
        
        elif any(word in query for word in ['large cap', 'big', 'large']):
            # Large cap stocks: high market cap
            return """
            SELECT * FROM stocks 
            WHERE market_cap > 50000 
            ORDER BY market_cap DESC 
            LIMIT 15
            """
        
        else:
            # Default: good quality stocks
            return """
            SELECT * FROM stocks 
            WHERE roe > 15 AND pe_ratio < 30 AND debt_to_equity < 1 
            ORDER BY roe DESC 
            LIMIT 15
            """

    def create_ai_prompt(self, user_message: str, stock_data: list = None) -> str:
        prompt = f"{self.system_prompt}\n\n" # system prompt saving in prompt 
        
        # Add previous conversation for context 
        if self.conversation_history:
            prompt += "Previous conversation:\n"
            # Only include last 4 messages to keep prompt manageable
            for msg in self.conversation_history[-4:]: # the last -4 in will be saved 
                prompt += f"User: {msg['user']}\n" # adding the user message
                prompt += f"You: {msg['assistant']}\n\n" # assistent message from history 
        
        # Add current stock data if we have it
        if stock_data:
            prompt += "Here are the stocks I found in the database:\n"
            for i, stock in enumerate(stock_data[:8], 1):  # Show max 8 stocks
                prompt += f"{i}. {stock.get('name', 'N/A')} ({stock.get('symbol', 'N/A')})\n"
                prompt += f"   Sector: {stock.get('sector', 'N/A')}\n"
                prompt += f"   PE Ratio: {stock.get('pe_ratio', 'N/A')}\n"
                prompt += f"   ROE: {stock.get('roe', 'N/A')}%\n"
                prompt += f"   Market Cap: ₹{stock.get('market_cap', 'N/A')} crores\n\n"
        
        # Add the current user question 
        prompt += f"User's current question: {user_message}\n\n"
        prompt += "Please respond conversationally and recommend specific stocks with reasons."
        
        return prompt

    def get_ai_response(self, prompt: str) -> str:
       
        try:
            # Call Gemini API with the prompt .
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,  # Controls randomness (0-1)
                    thinking_config=types.ThinkingConfig(thinking_budget=0)
                )
            )
            # it will return text  response
            return response.text
            
        except Exception as e:
            return f"Sorry, I encountered an error: {e}"

    def simulate_typing(self, text: str):


        sentences = re.split(r'(?<=[.!?])\s+', text) 
        
        
        for sentence in sentences:
            words = sentence.split()
            for word in words:
                print(word, end=" ", flush=True)
                time.sleep(0.00)  # Adjust typing speed here




            # Pause at end of sentences
            if sentence.strip().endswith(('.', '!', '?')):
                time.sleep(0.00)
        

        print()  # New line at the end

    def process_user_message(self, user_message: str) -> str:

        # it will check that if user message alerady have this messages if it have than it will save it to needs_stock_data 
        needs_stock_data = any(keyword in user_message.lower() for keyword in [
            'find', 'show', 'recommend', 'suggest', 'good', 'best', 'stocks', 
            'companies', 'investment', 'buy', 'portfolio'
        ])
        
        stock_data = [] # declaring the stock_data as list 
        if needs_stock_data:
            print(" Searching database for stocks...", end="", flush=True) # 
            stock_data = self.search_stocks(user_message) # if needs_stock_data have any of those keyword than it will call the search_stocks with users messages and save the output in stock_data as list 
            print(f" Found {len(stock_data)} stocks") # print that we have found 
            self.current_stocks = stock_data # and save the stock_data in current_stocks 
        
        # Create the prompt for AI
        prompt = self.create_ai_prompt(user_message, stock_data) # create the prompt with the user message and the stock data which we have found 
        
        print("\n AI Assistant: ", end="", flush=True)
        
        # Get AI response
        response = self.get_ai_response(prompt) # cakk the response by calling the get_ai_response
        
        # this is typing response function effect . 
        self.simulate_typing(response) 
        
        # Save conversation to memory saving the conversation for history by calling 
        self.conversation_history.append({
            'user': user_message,
            'assistant': response
        })
        
        return response

    def show_current_stocks(self):
        """Display stocks currently loaded in memory"""
        if not self.current_stocks:
            print("No stocks currently loaded")
            return
        
        print(f"\n📊 Current stocks ({len(self.current_stocks)}):")
        for i, stock in enumerate(self.current_stocks[:10], 1):
            print(f"{i}. {stock.get('name', 'N/A')} ({stock.get('symbol', 'N/A')})")
        
        if len(self.current_stocks) > 10:
            print(f"... and {len(self.current_stocks) - 10} more")

    def clear_conversation(self):
        """Clear conversation history and current stocks"""
        self.conversation_history = []
        self.current_stocks = []
        print("✅ Conversation cleared")


def main():
    """
    Main function to run the stock screener
    """
    # Configuration - Replace with your actual values
    API_KEY = "***************************************"
    DB_PATH = "*******************************"
    
    # Create the screener
    screener = NLPStockScreener(API_KEY, DB_PATH)
    
    # Welcome message
    print("🚀 Simple Stock Screener")
    print("💬 Ask me about Indian stocks! I can help you find good investments.")
    print("📋 Commands: /clear, /stocks, /quit")
    print("-" * 50)
    
    # Main conversation loop
    while True:
        try:
            # Get user input
            user_input = input("\n🔵 You: ").strip()
            
            if not user_input:
                continue
            
            # Handle special commands
            if user_input.lower() in ['/quit', '/exit', 'bye']:
                print("\n👋 Thanks for using the stock screener!")
                break
            
            elif user_input.lower() == '/clear':
                screener.clear_conversation()
                continue
            
            elif user_input.lower() == '/stocks':
                screener.show_current_stocks()
                continue
            
            # Process normal message
            screener.process_user_message(user_input)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
