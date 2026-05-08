import time
import logging
from fastapi import Request

logger = logging.getLogger(__name__)


async def log_requests(request: Request, call_next):
    start_time = time.time()

    method = request.method
    path = request.url.path

    try:
        response = await call_next(request)
        status_code = response.status_code

    except Exception as e:
        logger.error(f"[REQUEST_ERROR] {method} {path} → {str(e)}")
        raise

    duration = (time.time() - start_time) * 1000

    logger.info(
        f"[REQUEST] {method} {path} → {status_code} ({duration:.2f}ms)"
    )

    return response