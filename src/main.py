from dotenv import load_dotenv
import os

load_dotenv()
from smtp_client import SMTPClient
def main():

    client = SMTPClient(
        host="smtp.gmail.com",
        port=587,
        use_ssl=False,
        verbose=True
    )


    client.send_mail(
        sender=os.getenv("SMTP_EMAIL"),
        password=os.getenv("SMTP_PASSWORD"),
        recipients=[
            os.getenv("SMTP_RECEIVER")
        ],
        message="""Subject: SMTP Client Test

    Hello,
    This email was sent using raw SMTP socket client.
    """
    )



if __name__ == "__main__":
    main()
    