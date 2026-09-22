"""
OTP generation, storage, verification, and real email/SMS delivery.
Providers: SMTP (email), Fast2SMS / MSG91 / Twilio (SMS).
Falls back to demo mode only when no provider is configured.
"""
import random
import smtplib
import json
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from database import get_db_connection
import config

try:
    import requests
except ImportError:
    requests = None


def _generate_otp(length=6):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


def create_and_send_otp(target, channel, purpose='register'):
    """
    channel: 'email' | 'phone'
    Returns: {success, message, demo_otp?}
    """
    target = (target or '').strip().lower() if channel == 'email' else (target or '').strip()
    if not target:
        return {'success': False, 'message': 'Target email or phone is required.'}

    if channel == 'email' and '@' not in target:
        return {'success': False, 'message': 'Invalid email address.'}
    if channel == 'phone' and (not target.isdigit() or len(target) != 10):
        return {'success': False, 'message': 'Phone must be a 10-digit Indian mobile number.'}

    otp = _generate_otp(6)
    expires = datetime.now() + timedelta(minutes=config.OTP_EXPIRY_MINUTES)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE otp_tokens SET is_verified = 1 WHERE target = ? AND channel = ? AND purpose = ?",
        (target, channel, purpose)
    )
    cursor.execute(
        """INSERT INTO otp_tokens (target, channel, otp_code, purpose, expires_at)
           VALUES (?, ?, ?, ?, ?)""",
        (target, channel, otp, purpose, expires.strftime('%Y-%m-%d %H:%M:%S'))
    )
    conn.commit()
    conn.close()

    sent_via = None
    error_detail = None

    if channel == 'email':
        if config.email_configured():
            try:
                _send_email_otp(target, otp)
                sent_via = 'email'
            except Exception as e:
                error_detail = str(e)
        else:
            error_detail = 'SMTP not configured (set SMTP_USER and SMTP_PASSWORD)'
    elif channel == 'phone':
        if config.sms_configured():
            try:
                _send_sms_otp(target, otp)
                sent_via = 'sms'
            except Exception as e:
                error_detail = str(e)
        else:
            error_detail = 'SMS not configured (set FAST2SMS_API_KEY or MSG91_AUTH_KEY or Twilio keys)'

    # Real delivery succeeded
    if sent_via:
        return {
            'success': True,
            'message': f'OTP sent successfully via {sent_via} to {target}. Valid for {config.OTP_EXPIRY_MINUTES} minutes.',
            'channel': channel,
            'expires_minutes': config.OTP_EXPIRY_MINUTES,
            'demo_otp': None
        }

    # Demo fallback when keys missing OR delivery failed and demo allowed
    if config.OTP_DEMO_MODE:
        return {
            'success': True,
            'message': f'OTP generated (demo mode — configure API keys for real delivery). {error_detail or ""}',
            'demo_otp': otp,
            'channel': channel,
            'expires_minutes': config.OTP_EXPIRY_MINUTES
        }

    return {
        'success': False,
        'message': f'Failed to send OTP via {channel}. {error_detail or "Provider error."}'
    }


def verify_otp(target, channel, otp_code, purpose='register'):
    target = (target or '').strip().lower() if channel == 'email' else (target or '').strip()
    otp_code = (otp_code or '').strip()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT * FROM otp_tokens
           WHERE target = ? AND channel = ? AND purpose = ? AND is_verified = 0
           ORDER BY id DESC LIMIT 1""",
        (target, channel, purpose)
    )
    row = cursor.fetchone()
    if not row:
        conn.close()
        return {'success': False, 'message': 'No active OTP found. Please request a new one.'}

    try:
        expires = datetime.strptime(row['expires_at'], '%Y-%m-%d %H:%M:%S')
        if datetime.now() > expires:
            conn.close()
            return {'success': False, 'message': 'OTP has expired. Please request a new one.'}
    except Exception:
        pass

    if row['attempts'] >= config.OTP_MAX_ATTEMPTS:
        conn.close()
        return {'success': False, 'message': 'Too many failed attempts. Request a new OTP.'}

    if row['otp_code'] != otp_code:
        cursor.execute("UPDATE otp_tokens SET attempts = attempts + 1 WHERE id = ?", (row['id'],))
        conn.commit()
        conn.close()
        return {'success': False, 'message': 'Incorrect OTP. Please try again.'}

    cursor.execute("UPDATE otp_tokens SET is_verified = 1 WHERE id = ?", (row['id'],))
    conn.commit()
    conn.close()
    return {'success': True, 'message': f'{channel.capitalize()} verified successfully.'}


def is_target_verified(target, channel, purpose='register', within_minutes=30):
    target = (target or '').strip().lower() if channel == 'email' else (target or '').strip()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT id FROM otp_tokens
           WHERE target = ? AND channel = ? AND purpose = ? AND is_verified = 1
             AND created_at >= datetime('now', ?)
           ORDER BY id DESC LIMIT 1""",
        (target, channel, purpose, f'-{within_minutes} minutes')
    )
    row = cursor.fetchone()
    conn.close()
    return row is not None


def _send_email_otp(to_email, otp):
    body = (
        f"Your AP ECET verification code is: {otp}\n\n"
        f"This code expires in {config.OTP_EXPIRY_MINUTES} minutes.\n"
        f"Do not share this code with anyone.\n\n"
        f"— AP ECET Counselling Forecasting System"
    )
    msg = MIMEText(body)
    msg['Subject'] = f'AP ECET OTP: {otp}'
    msg['From'] = config.SMTP_FROM
    msg['To'] = to_email

    with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT, timeout=20) as server:
        if config.SMTP_USE_TLS:
            server.starttls()
        server.login(config.SMTP_USER, config.SMTP_PASSWORD)
        server.send_message(msg)


def _send_sms_otp(phone, otp):
    provider = (config.SMS_PROVIDER or 'fast2sms').lower()
    message = f'AP ECET OTP is {otp}. Valid for {config.OTP_EXPIRY_MINUTES} min. Do not share.'

    if provider == 'fast2sms':
        _send_fast2sms(phone, otp, message)
    elif provider == 'msg91':
        _send_msg91(phone, otp, message)
    elif provider == 'twilio':
        _send_twilio(phone, message)
    else:
        # Try Fast2SMS first, then MSG91
        if config.FAST2SMS_API_KEY:
            _send_fast2sms(phone, otp, message)
        elif config.MSG91_AUTH_KEY:
            _send_msg91(phone, otp, message)
        elif config.TWILIO_ACCOUNT_SID:
            _send_twilio(phone, message)
        else:
            raise RuntimeError('No SMS provider API key configured')


def _send_fast2sms(phone, otp, message):
    """https://docs.fast2sms.com/#quick-sms"""
    if not requests:
        raise RuntimeError('requests package required for Fast2SMS')
    if not config.FAST2SMS_API_KEY:
        raise RuntimeError('FAST2SMS_API_KEY not set')

    url = 'https://www.fast2sms.com/dev/bulkV2'
    headers = {
        'authorization': config.FAST2SMS_API_KEY,
        'Content-Type': 'application/json'
    }
    # Quick SMS route (works without DLT for trial); use route=d + template for production DLT
    payload = {
        'route': config.FAST2SMS_ROUTE or 'q',
        'message': message,
        'language': 'english',
        'flash': 0,
        'numbers': phone
    }
    if config.FAST2SMS_ROUTE == 'd' and config.FAST2SMS_SENDER_ID:
        payload['sender_id'] = config.FAST2SMS_SENDER_ID
        payload['variables_values'] = otp

    resp = requests.post(url, json=payload, headers=headers, timeout=20)
    data = resp.json() if resp.content else {}
    if resp.status_code != 200 or not data.get('return', False):
        raise RuntimeError(f'Fast2SMS error: {data.get("message") or resp.text or resp.status_code}')


def _send_msg91(phone, otp, message):
    """https://docs.msg91.com/reference/send-sms"""
    if not requests:
        raise RuntimeError('requests package required for MSG91')
    if not config.MSG91_AUTH_KEY:
        raise RuntimeError('MSG91_AUTH_KEY not set')

    # Flow API (template) preferred when TEMPLATE_ID set
    if config.MSG91_TEMPLATE_ID:
        url = 'https://control.msg91.com/api/v5/flow/'
        headers = {
            'authkey': config.MSG91_AUTH_KEY,
            'content-type': 'application/json'
        }
        payload = {
            'template_id': config.MSG91_TEMPLATE_ID,
            'short_url': '0',
            'recipients': [{'mobiles': f'91{phone}', 'OTP': otp, 'var': otp}]
        }
        resp = requests.post(url, json=payload, headers=headers, timeout=20)
    else:
        url = 'https://control.msg91.com/api/v5/flow/'
        # Simple send SMS endpoint
        url = 'https://api.msg91.com/api/sendhttp.php'
        params = {
            'authkey': config.MSG91_AUTH_KEY,
            'mobiles': f'91{phone}',
            'message': message,
            'sender': config.MSG91_SENDER_ID or 'APECET',
            'route': '4',
            'country': '91'
        }
        resp = requests.get(url, params=params, timeout=20)

    if resp.status_code not in (200, 201):
        raise RuntimeError(f'MSG91 error: {resp.text[:200]}')


def _send_twilio(phone, message):
    try:
        from twilio.rest import Client
    except ImportError:
        raise RuntimeError('Install twilio: pip install twilio')
    client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=config.TWILIO_FROM_NUMBER,
        to=f'+91{phone}'
    )
