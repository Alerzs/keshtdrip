# Production steps — KeshtDrip

Use this after the app is on a PaaS. Commands assume the process working directory is `keshtdrip/` (the folder that contains `manage.py`).
 The platform should start the site from `Procfile`.

---

## 1. Environment variables

Set these in the PaaS dashboard (or a production `.env` the host injects). Do not commit secrets.

| Variable | Required | Value |
|---|---|---|
| `django_secret_key` | Yes | A long random secret, different from local |
| `DEBUG` | Yes | `False` |
| `CSRF_TRUSTED_ORIGINS` | Yes in production | Exact site origin **with https**, e.g. `https://your-app.liara.run` or `https://keshtdrip.ir`. Comma-separate several: `https://example.com,https://www.example.com` |
| `SITE_URL` | Optional | Same as one trusted origin, e.g. `https://keshtdrip.ir` |
| `ALLOWED_HOSTS` | Recommended | Host only, no scheme: `keshtdrip.ir,www.keshtdrip.ir`. Defaults to `*` if unset. |

Admin login **403 CSRF** on a PaaS is usually missing `CSRF_TRUSTED_ORIGINS` or Django not seeing HTTPS behind the proxy. After setting the variables above, redeploy and try `/admin/` again over **https** (not http).

Do not include a trailing slash. `https://example.com/` is wrong; `https://example.com` is correct.

If the host sets `PORT` and the process fails to bind, change `Procfile` from `--bind 0.0.0.0:8000` to `--bind 0.0.0.0:$PORT`.

---

## 2. Before you push (local)

Rebuild CSS whenever templates or `tailwind/input.css` change. The server does not run Node. Do not put the Tailwind source file under `static/` — `collectstatic` would treat `@import "tailwindcss"` as a missing CSS URL.

```bash
npm run build:css
```

Commit `static/css/output.css`. Then push.

---

## 3. Release commands (every deploy)

Run after the new build is on the server, before or as the `web` process starts. Many platforms have a **Release** / **Build** command field — put this there:

```bash
python manage.py migrate --noinput
python manage.py collectstatic --noinput
```

- `migrate` applies Django schema changes (SQLite file: `db.sqlite3`).
- `collectstatic` copies files from `static/` into `staticfiles/`. WhiteNoise serves that folder when `DEBUG=False`.

---

## 4. One-time setup (first deploy only)

Seed the sample catalog if you want demo products:

```bash
python manage.py seed_shop
```

Create an admin user:

```bash
python manage.py createsuperuser
```

Admin URL: `/admin/`

Skip `seed_shop` if you already have real data.

---

## 5. Web process

The platform should run:

```text
web: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120
```

That loads `config.wsgi:application`.

---

## 6. After deploy — quick checks

- Home page loads and CSS is applied (header green, Vazirmatn).
- `/static/css/output.css` returns 200.
- Uploaded images under `/media/` work only if the host keeps `media/` on disk.
- Login, cart, and checkout still work.

---

## SQLite / media warning

This project uses:

- Database: `db.sqlite3`
- Uploads: `media/`

On most PaaS instances the filesystem is discarded on each deploy unless you attach a **persistent volume**. If you do not, you will lose products, orders, and uploaded images. For real production, use Postgres (or similar) and object storage, or mount a persistent disk for `db.sqlite3` and `media/`.

---

## Useful one-liners

SSH / one-off shell on the host:

```bash
python manage.py migrate --noinput && python manage.py collectstatic --noinput
python manage.py createsuperuser
python manage.py seed_shop
```
