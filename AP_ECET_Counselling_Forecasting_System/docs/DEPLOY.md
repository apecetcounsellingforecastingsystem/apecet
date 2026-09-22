# Deploy AP ECET Counselling Forecasting System Online

## Local development
```bash
pip install -r requirements.txt
python reset_passwords.py
python app.py
# → http://127.0.0.1:5000
```

## Production (Gunicorn)
```bash
pip install -r requirements.txt
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
export FLASK_DEBUG=0
export SESSION_COOKIE_SECURE=1   # only behind HTTPS
gunicorn -w 2 -b 0.0.0.0:8000 wsgi:app --timeout 120
```

## Render.com (free URL)
1. Push this folder to GitHub (exclude secrets).
2. Render → New → Web Service → connect repo.
3. Build: `pip install -r requirements.txt`
4. Start: `gunicorn -w 2 -b 0.0.0.0:$PORT wsgi:app --timeout 120`
5. Or use included `render.yaml` (Blueprint).
6. Set env: SECRET_KEY, optional SMTP / FAST2SMS keys.
7. URL example: `https://ap-ecet-xxxx.onrender.com`

**Note:** Free Render disk is ephemeral — SQLite may reset on redeploy.
For persistence use a paid disk or managed Postgres/MySQL.

## PythonAnywhere
1. Upload project / git clone.
2. `pip install --user -r requirements.txt`
3. Web → Manual config → WSGI file:
```python
import sys
path = '/home/YOURUSER/AP ECET COUNSELLING FORECASTING SYSTEM'
if path not in sys.path:
    sys.path.append(path)
from wsgi import app as application
```
4. Reload → `https://YOURUSER.pythonanywhere.com`

## Real OTP on deployed site
```bash
export SMTP_HOST=smtp.gmail.com
export SMTP_USER=you@gmail.com
export SMTP_PASSWORD=app-password
export SMS_PROVIDER=fast2sms
export FAST2SMS_API_KEY=your_key
export OTP_DEMO_MODE=0
```
See OTP_SETUP.md for details.

## MySQL instead of SQLite
```bash
export DB_ENGINE=mysql
export MYSQL_HOST=...
export MYSQL_USER=...
export MYSQL_PASSWORD=...
export MYSQL_DATABASE=ap_ecet
# Then run init_db / etl as needed
```

## Default logins (after reset_passwords.py)
- Student: student@apecet.gov.in / Student@12345
- Admin: admin@apecet.gov.in / Admin@12345
