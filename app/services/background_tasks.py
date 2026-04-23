import logging
import time

logger = logging.getLogger(__name__)


def send_task_modified_notification(user_email: str, task_title: str):
    logger.info("Preparing modification notification...")

    time.sleep(2)  # simulate external API/email service

    logger.info(f"EMAIL SENT → {user_email} | Task: {task_title}")

def send_task_fetched_notification(user_email: str):
    logger.info("Preparing notification...")

    time.sleep(2)

    logger.info(f"EMAIL SENT → {user_email}")

def send_task_deleted_notification(user_email: str, task_title: str):
    logger.info("Preparing deletion notification...")

    time.sleep(2)

    logger.info(f"EMAIL SENT → {user_email} | Task: {task_title}")