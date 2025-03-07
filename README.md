# FastAPI Investment & Crypto Query Handler

## Setup and Installation

To set up and run this FastAPI application, follow these steps:

1. **Create a virtual environment:**
   ```sh
   python -m venv venv
   ```
2. **Activate the virtual environment:**
   - On Windows:
     ```sh
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```sh
     source venv/bin/activate
     ```
3. **Install the required dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Run the FastAPI server using Uvicorn:**
   ```sh
   uvicorn app:app --reload --port 8000 --host 0.0.0.0
   ```
   *(You can change the host and port as needed.)*

---

## API Endpoints

### **1. Chat Endpoint**
**Endpoint:** `/chat`

**Method:** `POST`

**Description:** This endpoint processes user queries related to cryptocurrency investment, deposits/withdrawals, and web scraping for token conversions.

**Request Format:**
```json
{
    "query": "<user_query>"
}
```

**Response Format 1:**
```json
{
    "category": "investment",
    "amount": <amount>,
    "profit": <profit>,
    "loss": <loss>,
    "profit_margins": "<% | USD | NIL>",
    "loss_margins": "<% | USD | NIL>"
}
```

**Meanings:**
- **"investment"** - Indicates an investment-related query, returning amount, profit, loss, and margin types:
  - `profit_margins`:
    - `%` - Profit margin is percentage-based.
    - `USD` - Profit is in absolute USD value.
    - `NIL` - Profit margin not specified.
  - `loss_margins`:
    - `%` - Loss margin is percentage-based.
    - `USD` - Loss is in absolute USD value.
    - `NIL` - No loss specified.
  - `profit/loss`:
    - `Non-negative number` - indicating a margin (in USD or %)
    - `-1` - indicating no bounds, infinite allowable profit or loss
    - `NIL` - not specified

**Response Format 2:**
```json
{
    "category": "send_cryptos"
}
```

**Meanings:**
- **"send_cryptos"** - Indicates a transfer of tokens or NFTs into wallets.

**Response Format 3:**
```json
{
    "category": "web_scrape",
    "bot_answer": "<answer_to_query>"
}
```

**Meanings:**
- **"web_scrape"** - Indicates a request for cryptocurrency prices, trends, conversions, or market data.
- **"bot_answer"** - Response generated to user's query/queries.

---

### **2. WebSocket Investment Endpoint**
**Endpoint:** `/inv`

**Method:** `WebSocket`

**Description:** Establishes a WebSocket connection between the user and server to invest USD into Electronic Gold (EGLD/USDT). Returns High-Frequency Trading (HFT)/Scalping-based responses every 2 seconds.

**How It Works:**
1. The client sends initial investment details in JSON format:
   ```json
   {
       "amount": <investment_amount>,
       "profit": <profit_target>,
       "loss": <loss_limit>
   }
   ```
2. The WebSocket continuously returns trading updates every 2 seconds.
3. The client can send a `"stop"` message to liquidate assets and end the session.

**Example Communication Flow:**
- **Client sends:**
  ```json
  {"amount": 1000, "profit": 5, "loss": 2}
  ```
- **Server responds every 2 seconds:**
  ```
  "EGLD/USDT trade update: Current ROI +2.3%"
  "EGLD/USDT trade update: Current ROI +4.1%"
  ```
- **Client sends:**
  ```
  "stop"
  ```
- **Server responds:**
  ```
  "Stopping Token Investment. Liquidating Assets."
  ```

---

## Notes
- The chat endpoint is designed to automatically classify and extract structured information from user queries.
- The WebSocket endpoint runs real-time trading logic and provides market updates every 2 seconds.
- CORS is enabled to allow cross-origin requests.

This project is built using FastAPI and leverages AI-driven categorization for investment queries, crypto transactions, and market data retrieval.

