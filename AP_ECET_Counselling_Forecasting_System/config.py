"""
Central configuration for AP ECET Counselling Forecasting System.
OTP: set real API keys below (or via environment variables) for live email/SMS.
"""
import os

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
DB_ENGINE = os.environ.get('DB_ENGINE', 'sqlite').lower()
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'ap_ecet.db')

MYSQL_HOST = os.environ.get('MYSQL_HOST', '127.0.0.1')
MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'ap_ecet')

# ---------------------------------------------------------------------------
# Security
# ---------------------------------------------------------------------------
# Production: always set SECRET_KEY env var (Render generateValue / python -c "import secrets;print(secrets.token_hex(32))")
SECRET_KEY = os.environ.get('SECRET_KEY') or 'apecet_dev_only_change_me_in_production_x7z'
MAX_LOGIN_ATTEMPTS = 5
LOGIN_LOCKOUT_MINUTES = 15
OTP_EXPIRY_MINUTES = 10
OTP_MAX_ATTEMPTS = 5

# ---------------------------------------------------------------------------
# OTP providers — put YOUR real keys here (or export as env vars)
# ---------------------------------------------------------------------------
# Set OTP_DEMO_MODE=0 after configuring at least one email or SMS provider.
OTP_DEMO_MODE = os.environ.get('OTP_DEMO_MODE', '1') == '1'

# --- Email via SMTP (Gmail App Password recommended) ---
# 1. Google Account → Security → 2-Step Verification → App passwords
# 2. Create app password for "Mail"
# 3. Fill values below OR export SMTP_* environment variables
SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_USER = os.environ.get('SMTP_USER', '')          # e.g. yourgmail@gmail.com
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')  # Gmail App Password (16 chars)
SMTP_FROM = os.environ.get('SMTP_FROM', '') or SMTP_USER or 'noreply@apecet.gov.in'
SMTP_USE_TLS = os.environ.get('SMTP_USE_TLS', '1') == '1'

# --- SMS Provider preference: fast2sms | msg91 | twilio ---
SMS_PROVIDER = os.environ.get('SMS_PROVIDER', 'fast2sms').lower()

# Fast2SMS (India) — https://www.fast2sms.com/ → Dev API → Authorization key
# Free trial credits available after signup
FAST2SMS_API_KEY = os.environ.get('FAST2SMS_API_KEY', '')
FAST2SMS_SENDER_ID = os.environ.get('FAST2SMS_SENDER_ID', 'FSTSMS')
FAST2SMS_ROUTE = os.environ.get('FAST2SMS_ROUTE', 'q')  # q = promotional/quick, d = DLT transactional

# MSG91 (India) — https://msg91.com/
MSG91_AUTH_KEY = os.environ.get('MSG91_AUTH_KEY', '')
MSG91_TEMPLATE_ID = os.environ.get('MSG91_TEMPLATE_ID', '')
MSG91_SENDER_ID = os.environ.get('MSG91_SENDER_ID', 'APECET')

# Twilio (international)
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
TWILIO_FROM_NUMBER = os.environ.get('TWILIO_FROM_NUMBER', '')


def email_configured():
    return bool(SMTP_HOST and SMTP_USER and SMTP_PASSWORD)


def sms_configured():
    if SMS_PROVIDER == 'fast2sms':
        return bool(FAST2SMS_API_KEY)
    if SMS_PROVIDER == 'msg91':
        return bool(MSG91_AUTH_KEY)
    if SMS_PROVIDER == 'twilio':
        return bool(TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_FROM_NUMBER)
    return bool(FAST2SMS_API_KEY or MSG91_AUTH_KEY or (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN))
