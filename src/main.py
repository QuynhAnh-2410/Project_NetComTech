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


    client.connect()


    client.ehlo(
        "localhost"
    )


    client.starttls()


    client.auth(
        os.getenv("SMTP_EMAIL"),
        os.getenv("SMTP_PASSWORD")
    )


    client.mail_from(
        os.getenv("SMTP_EMAIL")
    )

    client.rcpt_to(
        os.getenv("SMTP_RECEIVER")
    )


    message = """\
Subject: SMTP Client Test

Hello,
This email was sent using raw SMTP socket client.
"""


    client.data(message)


    client.quit()



if __name__ == "__main__":
    main()
    