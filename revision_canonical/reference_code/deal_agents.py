from typing import Optional, List
from openai import OpenAI
from .deal_models import ScrapedDeal, DealSelection, Deal
import logging

# Setup Logging
logger = logging.getLogger(__name__)

class Agent:
    """
    Abstract Base Agent
    """
    RED = '\033[31m'
    GREEN = '\033[32m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BG_BLACK = '\033[40m'
    RESET = '\033[0m'

    name: str = "Agent"
    color: str = WHITE

    def log(self, message):
        print(f"{self.color}[{self.name}] {message}{self.RESET}")

class ScannerAgent(Agent):
    MODEL = "gpt-4o-mini" # Updated to modern model
    
    SYSTEM_PROMPT = """You identify and summarize the 5 most detailed deals from a list.
    Respond strictly in JSON using the DealSelection schema.
    Most important is that you respond with the 5 deals that have the most detailed product description with price.
    """

    USER_PROMPT_PREFIX = """Respond with the most promising 5 deals from this list.
    Deals:
    """

    name = "Scanner Agent"
    color = Agent.CYAN

    def __init__(self):
        self.log("Initializing")
        self.openai = OpenAI()

    def fetch_deals(self, memory: List[str]) -> List[ScrapedDeal]:
        self.log("Fetching deals from RSS feeds...")
        scraped = ScrapedDeal.fetch(show_progress=True)
        # Filter out duplicates based on URL
        result = [scrape for scrape in scraped if scrape.url not in memory]
        self.log(f"Found {len(result)} new deals.")
        return result

    def scan(self, memory: List[str] = []) -> Optional[DealSelection]:
        scraped = self.fetch_deals(memory)
        if not scraped:
            return None

        # Build prompt
        user_prompt = self.USER_PROMPT_PREFIX + "\n\n".join([s.describe() for s in scraped]) + "\n\nInclude exactly 5 deals."
        
        self.log("Analyzing deals with LLM...")
        try:
             # Use the new parse method for structured outputs
            completion = self.openai.beta.chat.completions.parse(
                model=self.MODEL,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                response_format=DealSelection,
            )
            selection = completion.choices[0].message.parsed
            # Post-process titles if missing
            for i, deal in enumerate(selection.deals):
                if not deal.title and i < len(scraped):
                     deal.title = scraped[i].title
            
            return selection
        except Exception as e:
            self.log(f"Error parsing deals: {e}")
            return None

class PricerAgent(Agent):
    name = "Pricer Agent"
    color = Agent.GREEN
    MODEL = "gpt-4o-mini"

    def __init__(self):
        self.openai = OpenAI()

    def estimate_value(self, deal: Deal) -> float:
        self.log(f"Estimating value for: {deal.product_description[:50]}...")
        
        completion = self.openai.chat.completions.create(
            model=self.MODEL,
            messages=[
                {"role": "system", "content": "You are an expert appraiser. Estimate the fair market value ($) of this product. Return ONLY the number, no text."},
                {"role": "user", "content": deal.product_description}
            ]
        )
        content = completion.choices[0].message.content.strip()
        import re
        match = re.search(r"(\d+(\.\d+)?)", content.replace(",", ""))
        if match:
            val = float(match.group(1))
            self.log(f"Estimated: ${val}")
            return val
        return 0.0
