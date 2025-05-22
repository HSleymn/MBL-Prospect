from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.utils import timezone
from datetime import timedelta
from django.core.mail import EmailMessage
import base64
import mimetypes
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from allauth.socialaccount.models import SocialToken
from django.conf import settings
from utilisateurs.models import MailSent
from django.urls import reverse

def fetch_contacts(contacts,quantity, domain, ):
    today = timezone.now()
    seven_days_ago = today - timedelta(days=7)
    n=0
    contactslist = []
    for contact in contacts:
    # On verifie que :
    #     - le contact n'a jamais reçu de mail ou bien que la derniere fois qu'il a reçu remonte a plus d'une semaine
    #     - le domaine du contact est bien le domaine choisi par l'utilisateur
    #     - le contact possède un champ email
        if contact.lastsend:
            contact_available =  contact.lastsend <= seven_days_ago and (contact.domain == domain) and contact.email
        else:
            contact_available =  (contact.domain.domain_name == domain) and contact.email


        if contact_available:
            contactslist.append(contact)
            n+=1
            print(n)
            print(quantity)
            if(n == quantity):

                return contactslist, n
    for contacta in contactslist:
        print(contacta.email + " numero 1 2 3")
    return contactslist , n

def send_mail_to_contacts(user, subject, body, contactslist, attachment=None):


    try:
        token_obj = SocialToken.objects.get(account__user=user, account__provider='google')
    except SocialToken.DoesNotExist:
        raise Exception("Token Google introuvable. L'utilisateur est-il bien connecté via Google ?")

    credentials = Credentials(
        token=token_obj.token,
        refresh_token=token_obj.token_secret,
        token_uri="https://oauth2.googleapis.com/token",
        client_id="TON_CLIENT_ID.apps.googleusercontent.com",
        client_secret="TON_CLIENT_SECRET",
        scopes=['https://www.googleapis.com/auth/gmail.send'],
    )

    # Création du message MIME
    for c in contactslist:
        mail_record = MailSent.objects.create(
            user=user,
            contact_email=c.email,
            subject=subject,
        )

        message = MIMEMultipart('alternative')

        message['To'] = ', '.join(c.email)
        message['From'] = user.email
        message['Subject'] = subject
        #on cree une url qui va faire fonctionner la view tracking_pixel avec l'id du mail
        tracking_url = settings.SITE_URL + reverse('tracking_pixel', args=[mail_record.id])
        tracking_pixel = f'<img src="{tracking_url}" width="1" height="1" alt="." />'
        html_body = f"""
                <html>
                    <body>
                        <p>{body}</p>
                        {tracking_pixel}
                    </body>
                </html>
                """
        message.attach(MIMEText(body, 'plain')) #au cas ou l utilisateur affiche ses mails en texte brut
        message.attach(MIMEText(html_body, 'html'))
        if attachment:
            file_name = attachment.name
            content_type, _ = mimetypes.guess_type(file_name)
            maintype, subtype = content_type.split('/', 1)
            message.add_attachment(attachment.read(),
                                   maintype=maintype,
                                   subtype=subtype,
                                   filename=file_name)
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        try:
            service = build('gmail', 'v1', credentials=credentials)
            send_result = service.users().messages().send(
                userId="me",
                body={'raw': encoded_message}
            ).execute()




            return send_result
        except Exception as e:
            print("Erreur d'envoi via Gmail API :", e)
            return None


