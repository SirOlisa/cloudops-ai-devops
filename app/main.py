import os
import time
import logging
from fastapi import FastAPI, Response, status
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# Configure structured logging to stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger("cloudops-bank-api")

app = FastAPI(title="CloudOps Bank - Payment API", version="1.0.0")

# Operational Metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency', ['endpoint'])

FAILURE_MODE = False

@app.get("/health")
def health_check(response: Response):
    """Health check probe for load balancers and orchestrators."""
    if FAILURE_MODE:
        logger.error("Health check failed: Database connection pool exhausted.")
        REQUEST_COUNT.labels(method="GET", endpoint="/health", status="500").inc()
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"status": "unhealthy", "reason": "Database connection pool exhausted"}
    
    REQUEST_COUNT.labels(method="GET", endpoint="/health", status="200").inc()
    logger.info("Health check passed.")
    return {"status": "healthy", "service": "payment-api"}

@app.post("/api/v1/payments")
def process_payment(response: Response):
    """Simulates a core banking transaction endpoint."""
    start_time = time.time()
    
    if FAILURE_MODE:
        logger.error("Payment failure: Connection timeout on DB cluster.")
        REQUEST_COUNT.labels(method="POST", endpoint="/api/v1/payments", status="500").inc()
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        REQUEST_LATENCY.labels(endpoint="/api/v1/payments").observe(time.time() - start_time)
        return {"error": "Internal Server Error", "code": "ERR_DB_TIMEOUT"}
    
    REQUEST_COUNT.labels(method="POST", endpoint="/api/v1/payments", status="200").inc()
    REQUEST_LATENCY.labels(endpoint="/api/v1/payments").observe(time.time() - start_time)
    logger.info("Payment processed successfully.")
    return {"transaction_id": "tx_994821", "amount": 150.00, "status": "completed"}

@app.post("/simulate/fail")
def toggle_failure(enable: bool = True):
    """Chaos engineering endpoint to trigger controlled incidents."""
    global FAILURE_MODE
    FAILURE_MODE = enable
    state = "enabled" if enable else "disabled"
    logger.warning(f"Simulated failure mode has been {state}.")
    return {"failure_mode": state}

@app.get("/metrics")
def metrics():
    """Prometheus metrics scraping endpoint."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)