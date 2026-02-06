package vinted

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/url"
	"strconv"

	"github.com/2spy/vinted-discord-bot/pkg/logger"
	"github.com/2spy/vinted-discord-bot/pkg/models"
	"github.com/2spy/vinted-discord-bot/pkg/stealth"
	http "github.com/bogdanfinn/fhttp"
	tls_client "github.com/bogdanfinn/tls-client"
	"go.uber.org/zap"
)

type VintedScraper struct {
	client tls_client.HttpClient
}

func NewVintedScraper() *VintedScraper {
	client, err := stealth.CreateClient()
	if err != nil {
		panic(err)
	}
	return &VintedScraper{
		client: client,
	}
}

func (s *VintedScraper) Search(ctx context.Context, job models.ScrapeJob) ([]models.Item, error) {
	logger.Info("Searching on Vinted", zap.String("query", job.Query))
	encodedJobQuery := url.QueryEscape(job.Query)
	client := s.client
	req_init, err := http.NewRequest("GET", "https://www.vinted.fr/catalog?search_text="+encodedJobQuery, nil)
	if err != nil {
		logger.Error("Error creating request", zap.Error(err))
		return nil, err
	}
	req_init.Header.Set("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0")
	req_init.Header.Set("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
	req_init.Header.Set("Accept-Language", "fr,fr-FR;q=0.9,en-US;q=0.8,en;q=0.7")
	// req.Header.Set("Accept-Encoding", "gzip, deflate, br, zstd")
	req_init.Header.Set("Connection", "keep-alive")
	req_init.Header.Set("Referer", "https://www.vinted.fr/")
	req_init.Header.Set("Upgrade-Insecure-Requests", "1")
	req_init.Header.Set("Sec-Fetch-Dest", "document")
	req_init.Header.Set("Sec-Fetch-Mode", "navigate")
	req_init.Header.Set("Sec-Fetch-Site", "same-origin")
	req_init.Header.Set("Sec-Fetch-User", "?1")
	req_init.Header.Set("Priority", "u=0, i")
	req_init.Header.Set("Pragma", "no-cache")
	req_init.Header.Set("Cache-Control", "no-cache")
	req_init.Header.Set("TE", "trailers")
	resp_init, err := client.Do(req_init)
	if err != nil {
		logger.Error("Error making request", zap.Error(err))
		return nil, err
	}
	defer resp_init.Body.Close()
	_, err = io.ReadAll(resp_init.Body)
	if err != nil {
		logger.Error("Error reading response body", zap.Error(err))
		return nil, err
	}
	req, err := http.NewRequest("GET", fmt.Sprintf("https://www.vinted.fr/api/v2/catalog/items?page=1&per_page=96&global_search_session_id=6a53863d-01f4-4af4-be77-982348a3c80d&search_text=%s&catalog_ids=&order=newest_first&size_ids=&brand_ids=&status_ids=&color_ids=&material_ids=", encodedJobQuery), nil)
	if err != nil {
		logger.Error("Error making request", zap.Error(err))
		return nil, err
	}
	req.Header.Set("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0")
	req.Header.Set("Accept", "application/json")
	req.Header.Set("Accept-Language", "fr,fr-FR;q=0.9,en-US;q=0.8,en;q=0.7")
	// req.Header.Set("Accept-Encoding", "gzip, deflate, br, zstd")
	req.Header.Set("Connection", "keep-alive")
	req.Header.Set("Referer", "https://www.vinted.fr/")
	req.Header.Set("Upgrade-Insecure-Requests", "1")
	req.Header.Set("Sec-Fetch-Dest", "document")
	req.Header.Set("Sec-Fetch-Mode", "navigate")
	req.Header.Set("Sec-Fetch-Site", "same-origin")
	req.Header.Set("Sec-Fetch-User", "?1")
	req.Header.Set("Priority", "u=0, i")
	req.Header.Set("Pragma", "no-cache")
	req.Header.Set("Cache-Control", "no-cache")
	req.Header.Set("TE", "trailers")
	resp, err := client.Do(req)
	if err != nil {
		logger.Error("Error making request", zap.Error(err))
		return nil, err
	}
	defer resp.Body.Close()
	bodyText, err := io.ReadAll(resp.Body)
	if err != nil {
		logger.Error("Error reading response body", zap.Error(err))
		return nil, err
	}
	var response VintedResponse
	err = json.Unmarshal(bodyText, &response)
	if err != nil {
		logger.Error("Error unmarshalling response", zap.Error(err))
		return nil, err
	}
	var items []models.Item
	for _, item := range response.Items {
		price, err := strconv.ParseFloat(item.Price.Amount, 64)
		if err != nil {
			logger.Error("Error parsing price", zap.Error(err))
			continue
		}
		items = append(items, models.Item{
			ID:       strconv.FormatInt(item.ID, 10),
			Title:    item.Title,
			Price:    price,
			Currency: item.Price.CurrencyCode,
			URL:      item.URL,
			ImageURL: item.Photo.URL,
			Platform: "vinted",
		})
	}
	return items, nil
}

func (s *VintedScraper) Name() string {
	return "vinted"
}
