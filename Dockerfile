# Build Stage
FROM golang:1.22-alpine AS builder

WORKDIR /app

COPY go.mod ./
# COPY go.sum ./
# RUN go mod download

COPY . .

# Build the worker binary
# CGO_ENABLED=0 for static binary (no libc dependency issues)
RUN CGO_ENABLED=0 GOOS=linux go build -o /app/worker ./cmd/worker/main.go

# Final Stage
FROM alpine:latest

WORKDIR /app

# Install CA certificates for HTTPS
RUN apk --no-cache add ca-certificates tzdata

COPY --from=builder /app/worker .
COPY .env .

CMD ["./worker"]
