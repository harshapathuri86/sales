# Deployment setup

Updated the `settings.py` for deployment.

Use `.secret_key.txt` as key if not generate it.

Static folder is set to `/var/www/sales/static`.

Create required log and run directories and change ownership

Update static files

```
sudo mkdir -pv /var/{log,run}/gunicorn
sudo chown -cR ubuntu:ubuntu /var/{log,run}/gunicorn/
sudo mkdir -pv /var/www/sales/static/
sudo chown -cR ubuntu:ubuntu /var/www/sales/ 
python manager.py collectstatic
```

Use `gunicorn_config.py` as config for gunicorn.

run ` gunicorn backend.wsgi:application -c gunicorn_config.py` to run the program

use the `sales.pathuri.xyz` nginx config to deploy
use the sales.service to autostart the server.

