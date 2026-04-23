import logging
import time

logger = logging.getLogger(__name__)


def send_task_created_notification(user_email: str, task_title: str):
    logger.info("Preparing notification...")

    time.sleep(2)  # simulate external API/email service

    logger.info(f"EMAIL SENT → {user_email} | Task: {task_title}")