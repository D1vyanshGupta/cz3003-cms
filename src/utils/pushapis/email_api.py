"""
    Email API
"""
from django.core.mail import send_mail
from django.core.mail import EmailMessage


class EmailAPI:
    DEFAULT_EMAIL_SENDER = 'cz3003crisismanagement@gmail.com'

    def push_update(self, to_email, subject, content, attachment=None):
        try:
            email = EmailMessage(
                subject, content, self.DEFAULT_EMAIL_SENDER, [to_email])
            if attachment:
                email.attach_file(attachment)
            email.send()
            return True
        except Exception as e:
            print(e)
            return False
