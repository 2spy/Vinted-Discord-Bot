package models

type Item struct {
	ID       string  `json:"id"`
	Title    string  `json:"title"`
	Price    float64 `json:"price"`
	Currency string  `json:"currency"`
	URL      string  `json:"url"`
	ImageURL string  `json:"image_url"`
	Platform string  `json:"platform"`
}
