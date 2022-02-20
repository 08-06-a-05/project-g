web: gunicorn Moneysite.wsgi:application --chdir Moneysite
python Moneysite/manage.py collectstatic --noinput
Moneysite/manage.py migrate