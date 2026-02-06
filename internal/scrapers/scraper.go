package scrapers

import (
	"context"

	"github.com/2spy/vinted-discord-bot/pkg/models"
)

type Scraper interface {
	Search(ctx context.Context, job models.ScrapeJob) ([]models.Item, error)

	Name() string
}
