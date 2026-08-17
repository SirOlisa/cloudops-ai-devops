import os
import time
import logging
from fastapi import FastAPI, Response, status

# Configure structured logging to stdout for Loki aggregation
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger("cloudops-bank-api")

app = FastAPI(title="CloudOps Bank - Payment API", version="1.0.0")

# Global flag to simulate infrastructure/app degradation in Phase 15
FAILURE_MODE = False

@app.get("/health")
def health_check(response: Response):
    """Health check probe used by AWS Target Groups, ECS, or Kubernetes."""
    if FAILURE_MODE:
        logger.error("Health check failed: Database connection pool exhausted.")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"status": "unhealthy", "reason": "Database connection pool exhausted"}
    
    logger.info("Health check passed.")
    return {"status": "healthy", "service": "payment-api"}

@app.post("/api/v1/payments")
def process_payment(response: Response):
    """Simulates a core banking transaction endpoint."""
    if FAILURE_MODE:
        logger.error("Payment failure: Connection timeout on DB cluster.")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": "Internal Server Error", "code": "ERR_DB_TIMEOUT"}
    
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