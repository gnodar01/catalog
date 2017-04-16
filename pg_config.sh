apt-get -qqy update
apt-get -qqy install postgresql
apt-get -qqy install python-pip
pip install --upgrade six
pip install psycopg2
pip install flask
pip install SQLAlchemy
pip install bleach
pip install oauth2client
pip install requests
pip install httplib2
pip install passlib
pip install itsdangerous
pip install flask-httpauth
su postgres -c 'createuser -dRS vagrant'
su vagrant -c 'createdb'

vagrantTip="[35m[1mThe shared directory is located at /vagrant\nTo access your shared files: cd /vagrant(B[m"
echo -e $vagrantTip > /etc/motd
