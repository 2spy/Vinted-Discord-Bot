package models

type ScrapeJob struct {
	ID          string `json:"id"`
	Query       string `json:"query"`
	Domain      string `json:"domain"`
	MaxPrice    int    `json:"max_price"`
	RateLimitMs int    `json:"rate_limit_ms"`
}
