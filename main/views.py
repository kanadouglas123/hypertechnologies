from django.shortcuts import render, get_object_or_404,redirect
from .models import BlogPost
from django.core.mail import send_mail
from django.contrib import messages
from .models import Project
import os
import base64
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from django.conf import settings
from django.shortcuts import render, redirect
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests

CLIENT_SECRET_FILE = os.path.join(settings.BASE_DIR, 'google_credentials', 'credentials.json')
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def projects(request):
    projects = Project.objects.prefetch_related("features", "sample_images").all()
    return render(request, "projects.html", {"projects": projects})

def blog(request):
    blogs = BlogPost.objects.all().order_by('-published_date')
    return render(request, 'blog.html', {'blogs': blogs})


# Helper function to get Google credentials
def get_google_credentials(request):
    creds = None
    if 'credentials' in request.session:
        creds = Credentials.from_authorized_user_info(request.session['credentials'], SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Store credentials in session
        request.session['credentials'] = creds.to_json()

    return creds

# Helper function to get Google credentials
def get_google_credentials(request):
    creds = None
    if 'credentials' in request.session:
        creds = Credentials.from_authorized_user_info(request.session['credentials'], SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Store credentials in session
        request.session['credentials'] = creds.to_json()

    return creds

def contact(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name", "")
        mobile = request.POST.get("mobile")
        email = request.POST.get("email")
        message = request.POST.get("message")
        captcha_response = request.POST.get("g-recaptcha-response")

        # Skip reCAPTCHA in local environment
        if os.environ.get("DJANGO_ENV") == "development":
            captcha_response = "valid"  # Simulate a valid captcha response

        # Validate inputs
        if not first_name or not mobile or not email or not message:
            messages.error(request, "Please fill in all required fields.")
            return redirect("contact")

        # reCAPTCHA validation (this part can be skipped in development)
        if captcha_response != "valid":
            secret_key = "your-secret-key"
            recaptcha_url = "https://www.google.com/recaptcha/api/siteverify"
            recaptcha_data = {
                'secret': secret_key,
                'response': captcha_response
            }
            recaptcha_response = requests.post(recaptcha_url, data=recaptcha_data)
            recaptcha_result = recaptcha_response.json()

            if not recaptcha_result.get("success"):
                messages.error(request, "Captcha validation failed. Please try again.")
                return redirect("contact")

        # Construct the email message
        subject = f"New Contact Message from {first_name} {last_name}"
        full_message = f"""
        Name: {first_name} {last_name}
        Mobile: {mobile}
        Email: {email}
        
        Message:
        {message}
        """

        try:
            # Get user credentials
            creds = get_google_credentials(request)
            service = build('gmail', 'v1', credentials=creds)

            message = create_message(email, "fluttermonster5@gmail.com", subject, full_message)
            send_message(service, "me", message)

            messages.success(request, "Your message has been sent successfully!")
        except Exception as e:
            messages.error(request, f"Failed to send message. Error: {str(e)}")

        return redirect("contact")  # Redirect after submission

    return render(request, "contact.html")


# Create message
def create_message(sender, to, subject, body):
    message = MIMEMultipart()
    message['to'] = to
    message['subject'] = subject
    msg = MIMEText(body)
    message.attach(msg)

    # Encode the message as base64
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    return {'raw': raw_message}

# Send message
def send_message(service, sender, message):
    try:
        # Use Gmail API to send the email
        send_message = service.users().messages().send(userId=sender, body=message).execute()
        return send_message
    except Exception as error:
        print(f"An error occurred: {error}")
        raise Exception("Unable to send email.")


def blog_detail(request, blog_id):
    blog = get_object_or_404(blog_post, id=blog_id)
    return render(request, 'blog_details.html', {'blog': blog})