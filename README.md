# Raw SMTP Client

## Setup

python -m venv my_env

pip install -r requirements.txt


## Environment

Create .env:

SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_RECEIVER=receiver@gmail.com


## Run

python src/main.py


## Supported

- SMTP over STARTTLS (587)
- SMTP over SSL/TLS (465)
- AUTH LOGIN
- Multiple recipients
- SMTP error handling