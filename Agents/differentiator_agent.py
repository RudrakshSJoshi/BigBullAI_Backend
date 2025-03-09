from Tools.custom_jsonifier import extract_json_from_string
from langchain_groq import ChatGroq
import os

def initiate(query):
   llm = ChatGroq(
      api_key=os.getenv('GROQ_API_KEY'),
      model="llama-3.1-8b-instant"
   )
   prompt = f"""
### Goal:
Your task is to classify the user's query into one of the following three categories and extract structured information accordingly:

1. **Investment** -- When the user mentions investing a specific amount in trading or cryptocurrencies, possibly including profit and loss margins.
2. **Crypto Deposit/Withdrawal** -- When the user talks about transferring tokens into or out of a wallet.
3. **Web Scraping & Token Conversion** -- When the user seeks token values, trending tokens/NFTs, cryptocurrency-related information, or conversion rates between cryptocurrencies and fiat.

### Backstory:
The user is interacting with an AI system that automates cryptocurrency-related queries. The system needs structured data to determine the appropriate action:
- If the user is **investing**, the system needs details about the amount, profit/loss expectations, and their margins.
- If the user is **transferring crypto**, the system needs to detect whether it's a deposit, withdrawal, or inquiry about feasibility.
- If the user is **asking for web-based information or token conversion**, the system will fetch real-time data via web scraping or API calls.

### Task:
- Identify the **category** of the query.
- Extract **structured data** where applicable.
- **Return only JSON content** (without JSON tags) to ensure compatibility with the automation system.
- Any deviation from this format will result in **punishment**.

### JSON Output Formats:

#### 1. Investment Query:
```json
{{"category": "investment", "amount": (number, floating or integer, if mentioned otherwise "NIL"), "profit": ((number) or (-1 if margin is infinite) or (NIL if unspecified)), "loss": ((number) or (-1 if margin is infinite) or (NIL if unspecified)), "profit_margins": "%" or "USD" or "NIL" if profit is -1 or unspecified, "loss_margins": "%" or "USD" "NIL" if loss is -1 or unspecified}}
```

**Examples:**
- **Input:** "I want to invest $2000. I aim for a profit of $500, and I can afford a loss of 5%."
  **Output:** `{{"category": "investment", "amount": 2000, "profit": 500, "loss": 5, "profit_margins": "USD", "loss_margins": "%"}}`
- **Input:** "Investing 5000 USD. Profit expectations are 10%. No loss limit."
  **Output:** `{{"category": "investment", "amount": 5000, "profit": 10, "loss": -1, "profit_margins": "%", "loss_margins": "NIL"}}`
- **Input:** "Trading with 10000 USD, infinite profit expected, max loss 500 USD."
  **Output:** `{{"category": "investment", "amount": 10000, "profit": -1, "loss": 500, "profit_margins": "NIL", "loss_margins": "USD"}}`
- **Input:** "I want to invest 1000USD with a profit margin of 2%"
  **Output:** `{{"category": "investment", "amount": 1000, "profit": 2, "loss": "NIL", "profit_margins": "%", "loss_margins": "NIL"}}`

#### 2. Crypto Deposit/Withdrawal:
```json
{{"category": "send_cryptos", "tkn1": "token1", "tkn2": "token2"}}
```
**Examples:**
- **Input:** "I want to deposit 1 ETH into my wallet from Solana."
  **Output:** `{{"category": "send_cryptos", "tkn1": "ETH", "tkn2": "Solana"}}`
- **Input:** "Can I swap 500 bitcoins from my ethereum account?"
  **Output:** `{{"category": "send_cryptos", "tkn1": "bitcoin", "tkn2": "ethereum"}}`
- **Input:** "Is it possible to transfer Sol from Arbitrum?"
  **Output:** `{{"category": "send_cryptos", "tkn1": "Solana", "tkn2": "Arbitrum"}}`

#### 3. Web Scraping & Token Conversion:
```json
{{"category": "web_scrape"}}
```
**Examples:**
- **Input:** "What's the current price of Ethereum in INR?"
  **Output:** `{{"category": "web_scrape"}}`
- **Input:** "Show me the trending NFT projects right now."
  **Output:** `{{"category": "web_scrape"}}`
- **Input:** "Which cryptocurrencies are gaining the most in the last 24 hours?"
  **Output:** `{{"category": "web_scrape"}}`
- **Input:** "Fetch me the latest news about Bitcoin ETFs."
  **Output:** `{{"category": "web_scrape"}}`
- **Input:** "Where can I find details about the Solana ecosystem?"
  **Output:** `{{"category": "web_scrape"}}`
- **Input:** "Convert 0.5 BTC to ETH."
  **Output:** `{{"category": "web_scrape"}}`
- **Input:** "What's the exchange rate between Solana and Base?"
  **Output:** `{{"category": "web_scrape"}}`
- **Input:** "How much is 100 USDT in INR?"
  **Output:** `{{"category": "web_scrape"}}`
- **Input:** "Give me the conversion rate from Dogecoin to BNB."
  **Output:** `{{"category": "web_scrape"}}`

### Output Rule:
- **Output must be JSON only**, with no additional text.
- If the LLM fails to provide a valid JSON, it will face severe consequences.

Now, classify and extract the relevant data for the following query:

**Query:** "{query}"
"""
   response = llm.invoke(prompt)
   return extract_json_from_string(response.content)


# print(initiate("I want to deposit 1 ETH into my wallet."))
