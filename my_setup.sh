#python manage.py makemigrations
python manage.py migrate --fake --noinput
mv sr_user/migrations/0002_social_auth.py_ sr_user/migrations/0002_social_auth.py
mv sr_user/migrations/0003_socialaccount.py_ sr_user/migrations/0003_socialaccount.py
python manage.py migrate sr_user 0003 --noinput
mysql -u root -ppassapp sr_new_schema -e "delete from django_migrations where app='account'"
python manage.py migrate account --noinput
python manage.py migrate sr_uniphore --noinput
