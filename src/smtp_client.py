class SMTPError(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")

    @property
    def is_transient(self):
        return 400 <= self.code < 500


class SMTPClient:

    def __init__(
        self,
        host: str,
        port: int,
        timeout: float = 30.0,
        use_ssl: bool = False,
        verbose: bool = False
    ):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.use_ssl = use_ssl
        self.verbose = verbose

        self.socket = None
        self.capabilities = {}

    def connect(self):
        pass

    def ehlo(self, domain="localhost"):
        pass

    def starttls(self):
        pass

    def auth(
        self,
        username,
        password,
        mechanism="LOGIN"
    ):
        pass

    def mail_from(self, address):
        pass

    def rcpt_to(self, address):
        pass

    def data(self, message):
        pass

    def send_mail(
        self,
        sender,
        recipients,
        message
    ):
        pass

    def quit(self):
        pass

    def _send(self, line):
        pass

    def _recv(self):
        pass