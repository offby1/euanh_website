import smtplib
from email.message import EmailMessage

from euanh_website.defaults import gmail_password, gmail_username, templates


class EmailService:
    def __init__(self):
        self.gmail_username = gmail_username
        self.gmail_password = gmail_password

    def send_email(
        self,
        subject,
        body,
        to,
        alt="This is a fallback plain text message for email clients that do not support HTML.",
    ):
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            msg = EmailMessage()
            msg.set_content(alt)
            msg.add_alternative(body, subtype="html")
            msg["Subject"] = subject
            msg["From"] = self.gmail_username
            msg["To"] = to
            msg["Reply-To"] = self.gmail_username
            msg["Bcc"] = self.gmail_username

            try:
                smtp.login(self.gmail_username, self.gmail_password)
                smtp.send_message(msg)
            except smtplib.SMTPException as e:
                print(f"Error sending email: {e}")

    def send_template_email(
        self,
        subject,
        template,
        to,
        alt="This is a fallback plain text message for email clients that do not support HTML.",
        **kwargs,
    ):
        body = templates.get_template(template).render(**kwargs)
        self.send_email(subject, body, to, alt=alt)
