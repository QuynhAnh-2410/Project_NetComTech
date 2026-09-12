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
        import socket

        try:
            self.socket = socket.create_connection(
                (self.host, self.port),
                timeout=self.timeout
                )

            code, message = self._recv()

            if code != 220:
                raise SMTPError(code, message)

            return code, message

        except socket.error as e:
            raise SMTPError(
                -1,
                f"Connection failed: {e}"
                )

    def ehlo(self, domain="localhost"):

        self._send(
            f"EHLO {domain}"
        )

        code, message = self._recv()

        if code != 250:
            raise SMTPError(code, message)

        self.capabilities = {}

        for line in message.splitlines():

            parts = line.split()

            if len(parts) == 0:
                continue

            key = parts[0].upper()

            values = parts[1:]

            if values:
                self.capabilities[key] = values
            else:
                self.capabilities[key] = True

        return self.capabilities

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

        if self.verbose:
            print("->", line)

        self.socket.sendall(
            (line + "\r\n").encode("utf-8")
        )

    def _recv(self):

        data = self.socket.recv(4096)

        response = data.decode(
            "utf-8",
            errors="replace"
        )

        if self.verbose:
            print("<-", response)

        lines = response.splitlines()

        first_line = lines[0]

        code = int(first_line[:3])

        message = "\n".join(
            line[4:]
            for line in lines
        )

        return code, message