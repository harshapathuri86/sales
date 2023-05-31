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

using [sqlite backup](https://github.com/efrecon/sqlite-backup) to backup sqlite db for last 30 backups
```
backup.sh -k 30 -d /home/ubuntu/sales/dumps/ -s 10 /home/ubuntu/sales/backend/db.sqlite3
```

need to run this periodically as cron to do regular backups
