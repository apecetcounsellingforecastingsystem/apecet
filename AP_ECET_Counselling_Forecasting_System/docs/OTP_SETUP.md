# Real OTP Setup Guide (Email + Mobile)

The registration form requires **email OTP** and **mobile OTP** before creating an account.

## Demo mode (default)

If API keys are **not** configured, the system still generates a real OTP, stores it in the database, and **shows the code on the registration page** so you can complete verification offline (viva / local demo).

Set `OTP_DEMO_MODE=0` only after you configure at least one real provider.

---

## 1. Email OTP (Gmail SMTP) — recommended

1. Open [Google Account → Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification**
3. Create an **App password** (Mail)
4. Set environment variables:

```bash
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER=yourgmail@gmail.com
export SMTP_PASSWORD="your 16-char app password"
export SMTP_FROM=yourgmail@gmail.com
export OTP_DEMO_MODE=0
```

Or edit `config.py` and put the same values in the SMTP_* fields.

---

## 2. Mobile OTP (India) — Fast2SMS

1. Sign up at https://www.fast2sms.com
2. Go to **Dev API** → copy **Authorization** key
3. Free trial wallet credits are usually enough for testing

```bash
export SMS_PROVIDER=fast2sms
export FAST2SMS_API_KEY="your_authorization_key"
export FAST2SMS_ROUTE=q
export OTP_DEMO_MODE=0
```

> For production DLT-compliant SMS in India, use `FAST2SMS_ROUTE=d` with an approved template and sender ID.

---

## 3. Mobile OTP — MSG91

```bash
export SMS_PROVIDER=msg91
export MSG91_AUTH_KEY="your_authkey"
export MSG91_TEMPLATE_ID="your_template_id"   # optional but preferred
export MSG91_SENDER_ID=APECET
export OTP_DEMO_MODE=0
```

---

## 4. Mobile OTP — Twilio

```bash
pip install twilio
export SMS_PROVIDER=twilio
export TWILIO_ACCOUNT_SID=ACxxxxxxxx
export TWILIO_AUTH_TOKEN=xxxxxxxx
export TWILIO_FROM_NUMBER=+1xxxxxxxx
export OTP_DEMO_MODE=0
```

---

## Quick test

```bash
python -c "
from otp_service import create_and_send_otp, verify_otp
r = create_and_send_otp('your@email.com', 'email')
print(r)
# if demo_otp present, use it; if real email, check inbox
"
```

## Security notes

- Never commit real API keys to GitHub.
- Use environment variables or a local `.env` file (see `.env.example`).
- OTP expires in 10 minutes; max 5 wrong attempts per code.
