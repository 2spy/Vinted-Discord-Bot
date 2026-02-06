package main

import (
	"context"
	"fmt"
	"log"

	"github.com/2spy/vinted-discord-bot/internal/scrapers/vinted"
	"github.com/2spy/vinted-discord-bot/pkg/models"
)

func main() {
	fmt.Println("Starting Vinted Scraper Test...")

	scraper := vinted.NewVintedScraper()

	// Create a dummy job
	job := models.ScrapeJob{
		Query:    "iphone 13",
		MaxPrice: 500,
	}

	fmt.Printf("Searching for: %s\n", job.Query)

	items, err := scraper.Search(context.Background(), job)
	if err != nil {
		log.Fatalf("Error searching: %v", err)
	}

	fmt.Printf("Found items (length: %d, but printing raw HTML likely for now)\n", len(items))
}
