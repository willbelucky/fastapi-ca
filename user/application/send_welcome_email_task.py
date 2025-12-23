import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery import Task

from config import get_settings

settings = get_settings()

logger = logging.getLogger(__name__)


class SendWelcomeEmailTask(Task):
    name = "send_welcome_email_task"

    def run(self, receiver_email: str):
        sender_email = "rlakim5521@gmail.com"
        password = settings.email_password

        try:
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = "회원 가입을 환영합니다."

            body = "TIL 서비스를 이용해주셔서 감사합니다."
            message.attach(MIMEText(body, "plain"))

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, password)
                server.send_message(message)

            logger.info(f"이메일 전송 성공: {receiver_email}")
            print(f"[SUCCESS] 이메일 전송 성공: {receiver_email}")
        except Exception as e:
            logger.error(f"이메일 전송 실패: {receiver_email}, 오류: {str(e)}")
            print(f"[ERROR] 이메일 전송 실패: {receiver_email}, 오류: {str(e)}")
            raise
