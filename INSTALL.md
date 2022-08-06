# Utopia Content Management System Installation

Documentation about installing Utopia's CMS.

## Install requirements

- System packages, names can vary by OS/distribution:

  mariadb mariadb-devel nginx libtiff libtiff-devel giflib giflib-devel python-pillow python-vobject pytz pycrypto python-requests-oauthlib rubygem-sass npm gcc libmaxminddb-devel

- npm (Node.js packages):

  postcss-cli autoprefixer

### Local installation for development in Linux or Mac (Devs / DevOps)

#### Local repository and virtualenv configuration

- Clone the project repository to any local destination directory and init its git submodules (this can take some minutes):

  ```
  user@host:~ $ git clone -b main https://github.com/ladiaria/utopia-cms
  cd utopia-cms && git submodule update --init
  ```

- Clone also another repo with more static files needed:

  `user@host:~/utopia-cms $ git clone -b main https://github.com/ladiaria/lightGallery static/lightGallery`

- Create a virtualenv (venv) for Python3 using system-site-packages (the subdirectory `~/.virtualenvs` is not needed, we use it in this guide because is the default virtualenv directory in the tool [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/), also the virtual environment name can be any other, "utopiacms" is chosen in this guide):

  `user@host:~/utopia-cms $ mkdir -p ~/.virtualenvs && virtualenv --system-site-packages ~/.virtualenvs/utopiacms`

- Activate the new virtual environment and install the required Python modules:

  ```
  user@host:~/utopia-cms $ source ~/.virtualenvs/utopiacms/bin/activate
  (utopiacms) user@host:~/utopia-cms $ pip install --upgrade pip && pip install -r portal/requirements.txt
  ```

#### Database setup

- Create a new database and grant user privileges to a new or existing database user:

```
(utopiacms) user@host:~/utopia-cms $ sudo mysqladmin create utopiacms
(utopiacms) user@host:~/utopia-cms $ sudo mysql
MariaDB [(none)]> CREATE USER 'utopiacms_user'@'localhost' IDENTIFIED BY 'password';
MariaDB [(none)]> GRANT ALL PRIVILEGES ON utopiacms.* TO 'utopiacms_user'@'localhost';
```

- Create a local settings module based on the sample given and edit the file created with your database settings created above and also fill the `SECRET_KEY` variable using any string or a more secure one generated for example with [this web tool](https://djecrety.ir/).

```
(utopiacms) user@host:~/utopia-cms $ cd portal
(utopiacms) user@host:~/utopia-cms/portal $ cp local_settings_sample.py local_settings.py
(utopiacms) user@host:~/utopia-cms/portal $ vim portal/local_settings.py
```

- Create needed tables using Django's `migrate` management command twice, without and with the `--run-syncdb` argument:

```
(utopiacms) user@host:~/utopia-cms/portal $ python -W ignore manage.py migrate
(utopiacms) user@host:~/utopia-cms/portal $ python -W ignore manage.py migrate --run-syncdb
```

#### Development environment setup

- Create a Django superuser and collect static files using this commands:

```
(utopiacms) user@host:~/utopia-cms/portal $ python -W ignore manage.py createsuperuser
(utopiacms) user@host:~/utopia-cms/portal $ python -W ignore manage.py collectstatic --noinput
```

- Configure Nginx for reverse proxying the Django's development server and start it:

```
(utopiacms) user@host:~/utopia-cms/portal $ sudo cp ../docs/nginx_example_conf/utopia-cms-dev.conf /etc/nginx/conf.d
(utopiacms) user@host:~/utopia-cms/portal $ sudo systemctl restart nginx
(utopiacms) user@host:~/utopia-cms/portal $ ./runserver yoogle.com:8000
```

- Login with superuser created before, edit the default site domain and create a publication with the same slug to the one configured in `settings.DEFAULT_PUB`:

NOTE: If you change the default `settings.DEFAULT_PUB` value from `default` to any `otherslug` value in your local settings, then you should update the permission codename used to check when a user is subscribed to this publication, to perform this update, run this SQL sentence below. Ignore this note and the sentence related if the setting was not modified.

`UPDATE auth_permission SET codename='es_suscriptor_otherslug' WHERE codename='es_suscriptor_default';`

Point your preferred web browser to https://yoogle.com/admin/sites/site/1/ and you will be redirected to the Django's admin site login page, after login you will be redirected again to the default site change form, change its domain to `yoogle.com` and optionally also change its display name to any name you want, save the changes and then go to https://yoogle.com/admin/core/publication/add/ fill the form to create the new publication, save it and then you will be able to see the home page working at https://yoogle.com/.
