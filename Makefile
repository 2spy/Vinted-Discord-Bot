.PHONY: build run test clean docker-build

APP_NAME := vinted-bot

build:
	go build -o bin/worker ./cmd/worker/main.go
	go build -o bin/api ./cmd/api/main.go

run-worker:
	go run ./cmd/worker/main.go

run-api:
	go run ./cmd/api/main.go

test:
	go test ./...

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

clean:
	rm -rf bin/
