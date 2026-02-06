# Vinted Bot V2 - Implementation Plan

## Goal
Build a high-performance, scalable Vinted monitoring bot using **Go**, **Redis**, and **Docker**. The goal is 10x performance, properly structured code, and easy deployment to reach 2k+ stars on GitHub.

## Architecture Overview
The system is split into two main components to ensure scalability and separation of concerns:

1.  **The Worker (`cmd/worker`)**:
    -   Responsible for interacting with Vinted's API.
    -   Handles authentication (cookies, TLS fingerprinting management).
    -   Scrapes items based on search criteria.
    -   Uses **Redis** to store seen item IDs (deduplication) to prevent duplicate alerts.
    -   Sends notifications to Discord via Webhooks.
    -   Designed to run multiple instances if needed (sharded by search query).

2.  **The API (`cmd/api`)** (Day 2):
    -   RESTful API to manage the bot's configuration dynamically.
    -   Endpoints to Add/Remove/List watched searches.
    -   Updates the configuration in Redis/Database which the Worker reads.

3.  **Data Store (Redis)**:
    -   **Cache**: Stores `item_id`s with a TTL (e.g., 7 days) to track what has been seen.
    -   **Queue/State**: Can store the list of active search queries (optional for V1, but good for V2).

## Tech Stack
-   **Language**: Go (Golang) 1.22+
-   **Database**: Redis (Alpine Docker image)
-   **Containerization**: Docker & Docker Compose
-   **Notification**: Discord Webhooks (Embeds)
-   **Config**: Environment variables (.env)

## Component Design

### 1. Project Structure
```text
vinted-bot-v2/
├── cmd/
│   ├── worker/          # Main entry point for the scraper
│   └── api/             # Main entry point for the REST API
├── internal/
│   ├── model/           # Data structs (Item, SearchParams, Alert)
│   ├── vinted/          # Vinted API client (Cookie jar, Headers, TLS)
│   ├── notify/          # Discord notification logic
│   └── store/           # Redis interaction layer
├── pkg/
│   └── logger/          # Structured logging setup
├── docker-compose.yml   # Orchestration
├── Dockerfile           # Multi-stage build
└── README.md            # Documentation
```

### 2. Core Modules

#### `internal/vinted`
-   **`NewClient()`**: Initializes a generic HTTP client with specific TLS signatures (JA3) to mimic a real browser and avoid 403s.
-   **`Client.UpdateCookie()`**: Fetches `_vinted_fr_session` cookies.
-   **`Client.Search(query string, filters ProcessParams) ([]Item, error)`**: Calls Vinted API endpoint (reverse-engineered).
-   **`Item` Struct**: Maps important JSON fields: `id`, `title`, `price.amount`, `photo.url`, `brand_title`, `url`.

#### `internal/store` (Redis)
-   **`IsNew(itemID string) bool`**:
    -   Checks if `itemID` exists in Redis `SET` or via simple key existence.
    -   If not exists: Returns `true` and sets key with TTL.
    -   If exists: Returns `false`.
-   **`SaveParams(params SearchParams)`**: Persist what we are monitoring.

#### `internal/notify`
-   **`SendEmbed(webhookURL string, item Item)`**: Formats a beautiful Discord Embed with:
    -   Title (linked to item).
    -   Price (Green if cheap, Red if expensive - logic can be added).
    -   Image thumbnail.
    -   Footer: "Found by Vinted Bot V2".

### 3. Workflow (Worker Loop)
1.  **Init**: Load Config, Connect to Redis.
2.  **Loop**:
    -   Unpack Search Params (e.g., "iPhone 13", MaxPrice: 500).
    -   **Sleep** (Randomized jitter: `Config.Rate` ± 20% to avoid patterns).
    -   **Fetch**: `vintedClient.Search()`.
    -   **Process**:
        -   For each item in response:
        -   if `store.IsNew(item.id)`:
            -   `store.MarkAsSeen(item.id)`
            -   `notify.SendEmbed(item)`
            -   Log: "Found new item: [Name] - [Price] €"

## Implementation Steps (7-Day Plan Alignment)

### Day 1: Foundation (Today)
-   Set up `go.mod` and project structure.
-   Implement `internal/vinted` (Auth & Search).
-   Implement `internal/notify` (Discord).
-   Implement `internal/store` (Redis Stub or Real).
-   Create `Dockerfile` & `docker-compose.yml`.

### Day 2: Dynamic API
-   Add Gin or Echo web framework.
-   Create endpoints to modify search parameters on the fly without restarting the container.

### Day 3-7: Polish & Launch
-   Refine User-Agent rotation.
-   Add Proxy support.
-   Write Marketing/Setup guide.

## Verification Plan

### Manual Verification
1.  **Build**: Run `docker-compose up --build`.
2.  **Redis Connection**: Check logs to confirm Redis connection is successful.
3.  **Search Test**:
    -   Configure `SEARCH_QUERY="sneakers"` in `.env`.
    -   Watch logs for "Fetching items...".
    -   Wait for "Found new item..." log.
4.  **Discord Test**:
    -   Check the provided Webhook channel.
    -   Verify the Embed appears with correct Image, Price, and Link.

### Automated Tests (Future)
-   `go test ./...` for unit tests on parsing logic.
-   Mock Vinted API for offline testing.
