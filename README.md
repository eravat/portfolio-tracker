# Portfolio Tracker

A REST API backend that lets users manage a stock portfolio: register/log in, record buy and sell transactions, view current holdings with their average prices and quantity of shares owned displayed, and calculate profit & loss (P&L) including live unrealized P&L using real-time stock prices.

Built as a personal project to practice backend fundamentals ahead of placement year applications.

## Features

- **Authentication** — user registration and login with hashed passwords (bcrypt) and JWT-based session tokens
- **Portfolios** — users can create and manage one or more portfolios
- **Transactions** — record buy/sell transactions per portfolio, with input validation (positive quantity/price, valid transaction type, no future-dated transactions, no selling more than currently held)
- **Holdings** — current quantity and average cost basis per ticker, derived from transaction history using FIFO (first-in, first-out) matching
- **P&L** — realized P&L (from completed sells) and unrealized P&L (on current holdings, using live market prices)
- **Live prices** — real-time stock price lookup via the Alpha Vantage API, with in-memory caching to avoid hitting API rate limits

## Tech stack

- **Language:** Python
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Migrations:** Alembic
- **Auth:** JWT (python-jose), bcrypt for password hashing
- **Testing:** Pytest
- **External API:** Alpha Vantage (live stock prices)

## Key design decisions

**Holdings are derived, not stored.** There's no `holdings` table. Current quantity and average cost per ticker are calculated on the fly from the full transaction history. This avoids a sync problem where stored holdings could drift out of line with the actual transaction record.

**FIFO for cost basis and realized P&L.** When shares are sold, the specific "lots" they came from are determined using first-in-first-out matching against prior buys. This is what makes it possible to correctly calculate both realized profit on a sale and the remaining average cost basis of what's still held.

**JWT access tokens for auth.** A single access token (not a separate ID token) is used for both authenticating requests and identifying the user, since this project doesn't need federated/third-party identity — it's a self-contained auth system.

**In-memory price caching.** Live prices are cached in memory for a short window to avoid exceeding the external API's rate limit. This is a deliberate simplification: it works well for a single running instance, but wouldn't scale correctly across multiple server instances (a production version would use Redis instead).

**Alembic for schema migrations.** Rather than relying on SQLAlchemy's `create_all()` (which can only create new tables, not modify existing ones), the project uses Alembic to track schema changes incrementally and reversibly.

## Getting started

### Prerequisites

- Python 3.10+
- PostgreSQL running locally (or accessible via a connection string)
- An [Alpha Vantage API key](https://www.alphavantage.co/support/#api-key) (free tier)

### Setup

1. Clone the repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root:
   ```
   DATABASE_URL=postgresql://<user>:<password>@localhost:5432/<dbname>
   SECRET_KEY=<a random secret, e.g. via secrets.token_hex(32)>
   ALGORITHM=HS256
   API_KEY=<your Alpha Vantage API key>
   ```

3. Run migrations to set up the database schema:
   ```bash
   alembic upgrade head
   ```

4. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

5. Open the interactive API docs at `http://127.0.0.1:8000/docs`.

## API overview

Full interactive documentation is available at `/docs` once the server is running. Key endpoints:

| Endpoint | Description |
|---|---|
| `POST /auth/register` | Create a new user account |
| `POST /auth/login` | Log in and receive an access token |
| `GET /auth/info` | View user profile |
| `POST /portfolios` | Create a new portfolio |
| `GET /portfolios` | List the logged-in user's portfolios |
| `POST /portfolios/{portfolio_id}/transactions` | Add a buy/sell transaction to a portfolio |
| `GET /portfolios/{portfolio_id}/transactions` | List a portfolio's transactions |
| `GET /portfolios/{portfolio_id}/holdings` | Get current holdings (quantity, average cost) |
| `GET /portfolios/{portfolio_id}/holdings/pnl` | Get current holdings pnl info (unrealised P&L, realized P&L) |
| `GET /stocks/{ticker}/price` | Get the current price for a ticker |

All routes except registration, login, and price require a valid Bearer token (obtained via `/auth/login`) in the `Authorization` header.

## Testing

Unit tests cover the FIFO holdings/P&L calculation logic — the highest-risk part of the codebase — including single-lot sells, single-lot buys, partial lot consumption, sells spanning multiple lots, and the over-sell error case.

Run tests with:
```bash
pytest
```

## Known limitations / future improvements

- In-memory price cache doesn't survive server restarts and wouldn't be shared across multiple instances — a production version would use Redis
- No tests yet for routes end-to-end (integration tests) or the Pydantic validators
- No support for multiple currencies
- No rate limiting on the API itself (only caching to limit calls to the external price API)
