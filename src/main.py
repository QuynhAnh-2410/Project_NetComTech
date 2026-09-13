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
        sender="lequynhanh24vt@gmail.com",
        password="wpzaceutqmdnwzdf",
        recipients=[
            "leanvy2410@gmail.com"
        ],
        message="""Subject: SMTP Client Test

    Hello,
    This email was sent using raw SMTP socket client.
    """
    )



if __name__ == "__main__":
    main()
    