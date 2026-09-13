# SMTP Client

## Features
- Raw socket SMTP client
- EHLO
- STARTTLS
- AUTH LOGIN
- MAIL FROM
- RCPT TO
- DATA
- QUIT

## Setup

Create .env:

SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_RECEIVER=receiver@gmail.com


## Run

python src/main.py


## Example output

{
 'receiver@gmail.com': True,
 'invalid@gmail.com': False
}