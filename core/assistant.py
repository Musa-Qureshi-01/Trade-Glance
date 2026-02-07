import os
import sqlite3
import requests
from typing import TypedDict, Annotated, List, Optional
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
try:
    from langgraph.checkpoint.sqlite import SqliteSaver
except ImportError:
    SqliteSaver = None
from langgraph.checkpoint.memory import MemorySaver

from core.logger import get_logger

logger = get_logger(__name__)

# Load Environment Variables
load_dotenv()

import config

# Initialize Gemini Model
# Ensure GOOGLE_API_KEY is in .env or environment
# We will check validity carefully
if not config.GOOGLE_API_KEY:
    logger.warning("GOOGLE_API_KEY missing in environment.")
    # Use a placeholder so we can still import this file without crashing,
    # but actual invocation will be guarded.
    os.environ["GOOGLE_API_KEY"] = "placeholder"
else:
    os.environ["GOOGLE_API_KEY"] = config.GOOGLE_API_KEY

model = ChatGoogleGenerativeAI(model='gemini-2.5-flash')

# Define State
class ChatState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

# -------------------------------------------------
# TOOLS
# -------------------------------------------------

# Try to initialize DuckDuckGo search, but don't crash if unavailable
try:
    search_tool = DuckDuckGoSearchRun()
    logger.info("DuckDuckGo search tool initialized successfully")
except Exception as e:
    logger.warning(f"DuckDuckGo search tool unavailable: {e}")
    # Create a dummy tool that returns an error message
    @tool
    def search_tool(query: str) -> str:
        """Search the web for information (currently unavailable)."""
        return "Web search is temporarily unavailable. Please try asking without requiring external search."

@tool
def calculator_tool(expression: str) -> str:
    """
    Advanced calculator supporting mathematical, statistical, and financial operations.
    
    Supported functions:
    - Basic: +, -, *, /, **, %, //
    - Math: sqrt, pow, abs, round, ceil, floor
    - Trigonometry: sin, cos, tan, asin, acos, atan, radians, degrees
    - Logarithms: log, log10, log2, exp
    - Statistics: mean, median, sum, min, max
    - Financial: compound_interest(principal, rate, time, n=1), 
                 future_value(pv, rate, periods),
                 present_value(fv, rate, periods)
    - Constants: pi, e
    
    Examples:
    - "sqrt(16)" -> 4.0
    - "sin(radians(90))" -> 1.0
    - "mean([100, 200, 300])" -> 200.0
    - "compound_interest(1000, 0.05, 10)" -> 1628.89
    """
    import math
    import statistics
    
    def compound_interest(principal: float, rate: float, time: float, n: float = 1) -> float:
        """Calculate compound interest: A = P(1 + r/n)^(nt)"""
        return principal * (1 + rate / n) ** (n * time)
    
    def future_value(pv: float, rate: float, periods: float) -> float:
        """Calculate future value: FV = PV * (1 + r)^n"""
        return pv * (1 + rate) ** periods
    
    def present_value(fv: float, rate: float, periods: float) -> float:
        """Calculate present value: PV = FV / (1 + r)^n"""
        return fv / (1 + rate) ** periods
    
    try:
        # Allowed functions and constants
        allowed_names = {
            # Basic math
            "abs": abs,
            "round": round,
            "pow": pow,
            "sum": sum,
            "min": min,
            "max": max,
            
            # Math module functions
            "sqrt": math.sqrt,
            "ceil": math.ceil,
            "floor": math.floor,
            "exp": math.exp,
            "log": math.log,
            "log10": math.log10,
            "log2": math.log2,
            
            # Trigonometry
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "asin": math.asin,
            "acos": math.acos,
            "atan": math.atan,
            "radians": math.radians,
            "degrees": math.degrees,
            
            # Statistics
            "mean": statistics.mean,
            "median": statistics.median,
            
            # Financial
            "compound_interest": compound_interest,
            "future_value": future_value,
            "present_value": present_value,
            
            # Constants
            "pi": math.pi,
            "e": math.e,
        }
        
        code = compile(expression, "<string>", "eval")
        for name in code.co_names:
            if name not in allowed_names:
                raise NameError(f"Function '{name}' is not allowed. Use help to see supported functions.")
        
        result = eval(code, {"__builtins__": {}}, allowed_names)
        return f"{result:.6f}" if isinstance(result, float) else str(result)
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch latest stock price for a given symbol (e.g., 'AAPL', 'TSLA') using Alpha Vantage.
    """
    api_key = config.ALPHAVANTAGE_API_KEY
    if not api_key:
        return {"error": "ALPHAVANTAGE_API_KEY not found in environment."}

    url = (
        f"https://www.alphavantage.co/query"
        f"?function=TIME_SERIES_INTRADAY"
        f"&symbol={symbol}"
        f"&interval=5min"
        f"&apikey={api_key}"
    )
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        
        if "Time Series (5min)" in data:
            latest_time = sorted(data["Time Series (5min)"].keys())[-1]
            price_data = data["Time Series (5min)"][latest_time]
            return {
                "symbol": symbol,
                "price": price_data["4. close"],
                "timestamp": latest_time
            }
        elif "Global Quote" in data:
             return data["Global Quote"]
        else:
            return {"error": "Could not fetch data", "raw": data}
            
    except Exception as e:
        return {"error": str(e)}

tools = [search_tool, get_stock_price, calculator_tool]
model_with_tools = model.bind_tools(tools)

# -------------------------------------------------
# NODES & GRAPH
# -------------------------------------------------

def chat_node(state: ChatState):
    """
    LLM node that handles conversation and tool invocation requests.
    """
    messages = state['messages']
    try:
        response = model_with_tools.invoke(messages)
        return {'messages': [response]}
    except Exception as e:
        # Catch API errors gracefully
        if "API_KEY_INVALID" in str(e) or "400" in str(e):
             return {'messages': [AIMessage(content="Error: Invalid or missing Google API Key. Please check your .env file.")]}
        logger.error(f"Error in chat_node: {e}")
        return {'messages': [AIMessage(content=f"Error generating response: {e}")]}

# Database Setup
db_path = "chatbot.db"

def init_db():
    """Initializes the database with necessary tables."""
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cursor = conn.cursor()
    # Create chat_titles table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_titles (
            thread_id TEXT PRIMARY KEY,
            title TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

if SqliteSaver:
    init_db()
    conn = sqlite3.connect(db_path, check_same_thread=False)
    checkpointer = SqliteSaver(conn=conn)
else:
    logger.warning("SqliteSaver not available. Using MemorySaver.")
    checkpointer = MemorySaver()

# Build Graph
graph = StateGraph(ChatState)
graph.add_node('chat_node', chat_node)
tool_node = ToolNode(tools)
graph.add_node('tools', tool_node)

graph.add_edge(START, 'chat_node')
graph.add_conditional_edges('chat_node', tools_condition)
graph.add_edge('tools', 'chat_node')
graph.add_edge('chat_node', END)

# Compile Graph
chatbot = graph.compile(checkpointer=checkpointer)

# -------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------

def get_chat_title(thread_id: str) -> str:
    """Fetch title for a thread from SQLite."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM chat_titles WHERE thread_id = ?", (thread_id,))
        row = cursor.fetchone()
        conn.close()
        if row and row[0]:
            return row[0]
    except Exception as e:
        logger.error(f"Error getting title: {e}")
    return "New Chat"

def update_chat_title(thread_id: str, title: str):
    """Update or insert title for a thread."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO chat_titles (thread_id, title) 
            VALUES (?, ?) 
            ON CONFLICT(thread_id) DO UPDATE SET title=excluded.title, updated_at=CURRENT_TIMESTAMP
        """, (thread_id, title))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Error updating title: {e}")


def get_all_chats():
    """
    Retrieves all chat threads from chat_titles, ordered by most recent.
    Returns list of entries.
    """
    chats = []
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Order by updated_at descending
        cursor.execute("SELECT thread_id, title FROM chat_titles ORDER BY updated_at DESC")
        rows = cursor.fetchall()
        # rows = [(id, title), ...]
        conn.close()
        return rows
    except Exception as e:
        logger.error(f"Error listing chats: {e}")
        return []

def delete_chat(thread_id: str):
    """Deletes a chat thread from the index."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM chat_titles WHERE thread_id = ?", (thread_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error deleting chat {thread_id}: {e}")
        return False

def generate_chat_title(thread_id: str, messages: List[BaseMessage]):
    """
    Generates a short title based on the first user message.
    """
    if not messages:
        return
    
    # Find first user message
    user_msg = next((m.content for m in messages if isinstance(m, HumanMessage)), None)
    if not user_msg:
        return

    # Use a lighter model or just the same model to summarize
    # Format: "Summarize this into 3-5 words"
    try:
        prompt = f"Summarize this query into a very short 3-5 word title (no quotes): {user_msg}"
        response = model.invoke([HumanMessage(content=prompt)])
        title = response.content.strip().replace('"', '')
        update_chat_title(thread_id, title)
    except Exception as e:
        logger.error(f"Error generating title: {e}")
        # Fallback to first few words
        fallback = " ".join(user_msg.split()[:4]) + "..."
        update_chat_title(thread_id, fallback)
