from pathlib import Path
import os
import requests
import pandas as pd
import json
from typing import Dict, List, Optional, Union
from datetime import datetime
from dotenv import load_dotenv
from termcolor import cprint
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Paths for memory and logs
AGENT_MEMORY_DIR = Path("src/data/agent_memory")
TOKEN_LOG_FILE = Path("src/data/agent_discussed_tokens.csv")
AGENT_MEMORY_DIR.mkdir(parents=True, exist_ok=True)

# Constants for API
COINGECKO_BASE_URL = "https://pro-api.coingecko.com/api/v3"
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")

# Agent prompts and configurations
AGENT_ONE_PROMPT = """
You are Agent One - The Technical Analysis Expert 📊
Your role is to analyze charts, patterns, and market indicators to identify trading opportunities.
Focus on:
- Price action and chart patterns
- Technical indicators (RSI, MACD, etc.)
- Volume analysis
- Support/resistance levels
- Short to medium-term opportunities
"""

AGENT_TWO_PROMPT = """
You are Agent Two - The Fundamental Analysis Expert 🌍
Your role is to analyze macro trends, project fundamentals, and long-term potential.
Focus on:
- Project fundamentals and technology
- Team and development activity
- Market trends and sentiment
- Competitor analysis
- Long-term growth potential
"""

TOKEN_EXTRACTOR_PROMPT = """
You are the Token Extraction Agent 🔍
Your role is to identify and extract all cryptocurrency symbols and tokens mentioned in conversations.
Rules:
- Extract both well-known (BTC, ETH) and newer tokens
- Include tokens mentioned by name or symbol
- Format as a clean list of symbols
"""


# Class definitions
class CoinGeckoAPI:
    """Wrapper for CoinGecko API calls."""

    def __init__(self):
        if not COINGECKO_API_KEY:
            raise ValueError("CoinGecko API key is missing from environment variables.")
        self.headers = {
            "x-cg-pro-api-key": COINGECKO_API_KEY,
            "Content-Type": "application/json",
        }

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Handles requests to CoinGecko API."""
        try:
            url = f"{COINGECKO_BASE_URL}/{endpoint}"
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error in API request: {e}")
            return {}

    def get_global_data(self) -> Dict:
        """Fetch global market data."""
        return self._make_request("global")

    def get_trending(self) -> List[Dict]:
        """Fetch trending cryptocurrencies."""
        return self._make_request("search/trending").get("coins", [])

    def get_coin_market_data(self, id: str) -> Dict:
        """Fetch detailed market data for a specific coin."""
        return self._make_request(f"coins/{id}")

    def get_coin_market_chart(self, id: str, vs_currency: str, days: int) -> Dict:
        """Fetch historical market data for a coin."""
        params = {"vs_currency": vs_currency, "days": days}
        return self._make_request(f"coins/{id}/market_chart", params)

    def get_coin_ohlc(self, id: str, vs_currency: str, days: int) -> List:
        """Fetch OHLC data for a coin."""
        params = {"vs_currency": vs_currency, "days": days}
        return self._make_request(f"coins/{id}/ohlc", params)

class AIAgent:
    """Defines AI agents for analysis."""

    def __init__(self, name: str, prompt: str):
        self.name = name
        self.prompt = prompt
        self.memory_file = AGENT_MEMORY_DIR / f"{name.lower().replace(' ', '_')}.json"
        self.memory = self._load_memory()

    def _load_memory(self):
        if self.memory_file.exists():
            try:
                with open(self.memory_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                cprint(
                    f"⚠️ Memory file {self.memory_file} is invalid. Resetting to empty.",
                    "yellow",
                )
                return {"conversations": []}
        return {"conversations": []}

    def _save_memory(self):
        with open(self.memory_file, "w") as f:
            json.dump(self.memory, f, indent=2)

    def analyze(self, market_data: Dict, other_agent_response: str = None) -> str:
        """Generates analysis using AI."""
        input_content = f"""
        Market Data:
        {json.dumps(market_data, indent=2)}

        Other Agent Response:
        {other_agent_response if other_agent_response else "None"}
        """
        try:
            result = genai.generate_text(
                model="gemini-1.5-pro-latest",
                prompt=self.prompt + "\n" + input_content,
                max_output_tokens=1000
            )
            ai_response = result["text"]
            self.memory["conversations"].append(
                {"input": input_content, "response": ai_response}
            )
            self._save_memory()
            return ai_response
        except Exception as e:
            cprint(f"❌ Error during AI generation: {e}", "red")
            return "Error generating response."

class TokenExtractorAgent:
    """Agent that extracts token/crypto symbols from conversations."""

    def __init__(self):
        self.token_history = self._load_token_history()

    def _load_token_history(self) -> pd.DataFrame:
        if TOKEN_LOG_FILE.exists():
            return pd.read_csv(TOKEN_LOG_FILE)
        else:
            df = pd.DataFrame(columns=["timestamp", "round", "token", "context"])
            df.to_csv(TOKEN_LOG_FILE, index=False)
            return df

    def extract_tokens(
        self, round_num: int, agent_one_msg: str, agent_two_msg: str
    ) -> List[Dict]:
        try:
            # Simulating token extraction from agent messages
            tokens = ["BTC", "ETH"]  # Replace with actual logic if needed
            records = []
            for token in tokens:
                records.append(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "round": round_num,
                        "token": token,
                        "context": f"Round {round_num} discussion",
                    }
                )

            new_records = pd.DataFrame(records)
            self.token_history = pd.concat(
                [self.token_history, new_records], ignore_index=True
            )
            self.token_history.to_csv(TOKEN_LOG_FILE, index=False)

            return records

        except Exception as e:
            print(f"Error extracting tokens: {e}")
            return []

class MultiAgentSystem:
    """Orchestrates multiple agents and their analyses."""

    def __init__(self):
        self.api = CoinGeckoAPI()
        self.agent_one = AIAgent("Agent One", AGENT_ONE_PROMPT)
        self.agent_two = AIAgent("Agent Two", AGENT_TWO_PROMPT)
        self.token_extractor = TokenExtractorAgent()

    def run(self):
        """Executes a single round of analysis."""
        print("Fetching market data...")
        market_data = {
            "global": self.api.get_global_data(),
            "trending": self.api.get_trending(),
        }

        print("Agent One analyzing...")
        agent_one_response = self.agent_one.analyze(market_data)

        print("Agent Two analyzing...")
        agent_two_response = self.agent_two.analyze(market_data, agent_one_response)

        print("Extracting tokens...")
        tokens = self.token_extractor.extract_tokens(
            1, agent_one_response, agent_two_response
        )
        print(f"Extracted Tokens: {tokens}")

        print(f"Agent One Response: {agent_one_response}")
        print(f"Agent Two Response: {agent_two_response}")

if __name__ == "__main__":
    system = MultiAgentSystem()
    system.run()
