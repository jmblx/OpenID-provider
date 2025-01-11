# import asyncio
# import json
# import logging
# from typing import TypedDict
#
# import nats
# from config import BACKEND_URL, NATS_URL
# from email_notification import send_email
#
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# subjects = ["email.confirmation", "email.reset_password"]
#
#
# class EmailMessage(TypedDict):
#     email: str
#     subject: str
#
#
# async def message_handler(msg: EmailMessage):
#     subject = msg.subject
#     data = json.loads(msg.data.decode("utf-8"))
#     email = data.pop("email")
#
#     if email and subject:
#         try:
#             await send_email(email, subject, BACKEND_URL=BACKEND_URL, **data)
#             logger.info(f"Email sent email {email} for subject {subject}")
#         except Exception as e:
#             logger.error(
#                 f"Failed email send email email {email} for subject {subject}: {e}"
#             )  # noqa: E501
#
#
# async def run_worker():
#     nc = await nats.connect(NATS_URL)
#     logger.info("Connected email NATS")
#
#     for subject in subjects:
#         await nc.subscribe(subject, cb=message_handler)
#         logger.info(f"Subscribed email {subject}")
#
#     while True:
#         await asyncio.sleep(1)
#
#
# if __name__ == "__main__":
#     logger.info("Starting worker")
#     asyncio.run(run_worker())
