apt-get -qqy update
apt-get -qqy install postgresql python-psycopg2
apt-get -qqy install python-flask python-sqlalchemy
apt-get -qqy install python-pip
pip install --upgrade six
pip install bleach
pip install oauth2client
pip install requests
pip install httplib2
pip install passlib
pip install itsdangerous
pip install flask-httpauth
su postgres -c 'createuser -dRS vagrant'
su vagrant -c 'createdb'
sudo -u postgres psql -c "create role admin with createdb createrole password 'strts1';"
sudo -u postgres psql -c "create role catalog login password 'strts1';"
sudo -u postgres psql -c "create database catalogizer;"
sudo -u postgres psql -c "alter database catalogizer owner to catalog;"
service postgresql restart

vagrantTip="[35m[1mThe shared directory is located at /vagrant\nTo access your shared files: cd /vagrant(B[m"
echo -e $vagrantTip > /etc/motd
