import socket
import ssl
import base64
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
        self._buffer = b""

    def connect(self):

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

        self._send("STARTTLS")

        code, message = self._recv()

        if code != 220:
            raise SMTPError(code, message)

        context = ssl.create_default_context()

        self.socket = context.wrap_socket(
            self.socket,
            server_hostname=self.host
        )

        self.ehlo()

    def auth(
        self,
        username,
        password,
        mechanism="LOGIN"
    ):

        if mechanism.upper() != "LOGIN":
            raise SMTPError(
                -1,
                "Only AUTH LOGIN is supported"
            )

        self._send("AUTH LOGIN")

        code, message = self._recv()

        if code != 334:
            raise SMTPError(code, message)


        username_encoded = base64.b64encode(
            username.encode("utf-8")
        ).decode("utf-8")

        self._send(username_encoded)

        code, message = self._recv()

        if code != 334:
            raise SMTPError(code, message)


        password_encoded = base64.b64encode(
            password.encode("utf-8")
        ).decode("utf-8")

        self._send(password_encoded)

        code, message = self._recv()

        if code != 235:
            raise SMTPError(code, message)

        return True

    def mail_from(self, sender):

        self._send(
            f"MAIL FROM:<{sender}>"
        )

        code, message = self._recv()

        if code != 250:
            raise SMTPError(code, message)

        return True

    def rcpt_to(self, recipient):

        self._send(
            f"RCPT TO:<{recipient}>"
        )

        code, message = self._recv()

        return code == 250

    def data(self, message):

        self._send("DATA")

        code, response = self._recv()

        if code != 354:
            raise SMTPError(code, response)


        self._send(message)

        self._send(".")


        code, response = self._recv()

        if code != 250:
            raise SMTPError(code, response)

        return True

    def send_mail(
        self,
        sender,
        password,
        recipients,
        message
    ):
        if not sender:
            raise ValueError("Missing SMTP email")

        if not password:
            raise ValueError("Missing SMTP password")
        result = {}

        try:
            self.connect()

            self.ehlo()

            if not self.use_ssl:
                self.starttls()
                self.ehlo()

            self.auth(
                sender,
                password
            )

            self.mail_from(sender)

            for recipient in recipients:
                result[recipient] = self.rcpt_to(recipient)

            accepted = [
                recipient
                for recipient, ok in result.items()
                if ok
            ]

            if accepted:
                self.data(message)

        finally:
            if self.socket:
                self.quit()

        return result

    def quit(self):

        self._send("QUIT")

        code, message = self._recv()

        if code != 221:
            raise SMTPError(code, message)

        self.socket.close()

        return True

    def _send(self, line):

        if self.verbose:
            print("->", line)

        self.socket.sendall(
            (line + "\r\n").encode("utf-8")
        )

    def _recv(self):

        while b"\r\n" not in self._buffer:
            data = self.socket.recv(4096)

            if data == b"":
                raise SMTPError(
                    -1,
                    "Connection closed by server"
                )

            self._buffer += data


        lines = []

        while True:

            line, _, remaining = self._buffer.partition(b"\r\n")

            if not _:
                break

            self._buffer = remaining

            line = line.decode(
                "utf-8",
                errors="replace"
            )

            lines.append(line)

            # đủ một SMTP reply
            if len(line) >= 4 and line[3] == " ":
                break


        first_line = lines[0]

        code = int(first_line[:3])

        message = "\n".join(
            line[4:]
            for line in lines
        )


        if self.verbose:
            print("<-", "\n".join(lines))


        return code, message