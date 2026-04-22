import time
import logging

logger = logging.getLogger(__name__)


def send_task_created_email(user_email: str, task_title: str):
    # simulate slow work
    time.sleep(2)

    logger.info(
        f"Email sent to {user_email} for task '{task_title}'"
    )