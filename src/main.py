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


    result = client.send_mail(
        sender=os.getenv("SMTP_EMAIL"),
        password=os.getenv("SMTP_PASSWORD"),
        recipients=[
            os.getenv("SMTP_RECEIVER"),
            os.getenv("SMTP_RECEIVER_TEST")
        ],
        message="""Subject: SMTP Client Test

    Hello,
    This email was sent using raw SMTP socket client.
    """
    )
    print(result)


if __name__ == "__main__":
    main()
    