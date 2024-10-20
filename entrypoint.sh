#!/bin/sh

until nc -z -w30 $DB_HOST $DB_PORT ; do
    echo "Waiting for database connection, try after 1 second..."
    sleep 1
done

python manage.py migrate
cat <<EOF | python manage.py shell
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.filter(username='$DJANGO_ADMIN_USER').exists() or User.objects.create_superuser('$DJANGO_ADMIN_USER', '$DJANGO_ADMIN_PASS')
from apps.whitelist.models import Whitelist
Whitelist.objects.update_or_create(id=1, ip="127.0.0.1")
EOF
gunicorn lockey.wsgi:application --bind 0.0.0.0:8000
