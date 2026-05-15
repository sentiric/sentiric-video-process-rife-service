import os

class Settings:
    APP_NAME = "Sentiric RIFE Video Processor"
    APP_VERSION = "1.0.0"
    ENV = os.getenv("ENV", "production")
    DEVICE = "cuda"
    
    HTTP_PORT = int(os.getenv("RIFE_SERVICE_HTTP_PORT", "16150"))
    GRPC_PORT = int(os.getenv("RIFE_SERVICE_GRPC_PORT", "16151"))
    METRICS_PORT = int(os.getenv("RIFE_SERVICE_METRICS_PORT", "16152"))

    # mTLS
    GRPC_TLS_CA_PATH = os.getenv("GRPC_TLS_CA_PATH", "/sentiric-certificates/certs/ca.crt")
    CERT_PATH = "/sentiric-certificates/certs/video-process-rife-service-chain.crt"
    KEY_PATH = "/sentiric-certificates/certs/video-process-rife-service.key"

    # Storage & MQ
    S3_ENDPOINT = os.getenv("BUCKET_ENDPOINT_URL", "http://minio:9000")
    S3_ACCESS_KEY = os.getenv("BUCKET_ACCESS_KEY_ID", "sentiric")
    S3_SECRET_KEY = os.getenv("BUCKET_SECRET_ACCESS_KEY", "sentiric-secret-key")
    S3_BUCKET = os.getenv("BUCKET_NAME", "sentiric")
    RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://sentiric:sentiric_pass@rabbitmq:5672/%2f")

settings = Settings()