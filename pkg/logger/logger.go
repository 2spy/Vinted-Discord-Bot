package logger

import "go.uber.org/zap"

var Logger *zap.Logger

func Init() {
	Logger, _ = zap.NewProduction()
}

func Info(msg string, fields ...zap.Field) {
	Logger.Info(msg, fields...)
}

func Error(msg string, fields ...zap.Field) {
	Logger.Error(msg, fields...)
}

func Debug(msg string, fields ...zap.Field) {
	Logger.Debug(msg, fields...)
}
