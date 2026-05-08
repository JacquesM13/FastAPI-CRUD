import logging
import time

logger = logging.getLogger(__name__)


def send_task_modified_notification(user: str, task_title: str):
    logger.info(f"[TASK_CREATE] user: {user} task: '{task_title}'")

def send_task_fetched_notification(user: str):
    logger.info(f"[TASK_FETCH] user: {user}")

def send_task_deleted_notification(user: str, task_title: str):
    logger.info(f"[TASK_DELETE] user: {user} task: {task_title}")