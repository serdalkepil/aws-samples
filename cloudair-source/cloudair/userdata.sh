#!/bin/bash
systemctl enable amazon-ssm-agent
systemctl start amazon-ssm-agent
#### INITIALIZE VARIABLES ####
JDBC_CONNECTION_STRING="jdbc:mysql://123.123.123.123:3306/devlounge?useSSL=false&autoReconnect=true"
JDBC_UID="root"
DB_NAME="devlounge"
LOGFILE="/home/ec2-user/cloudair.log"
JDBC_PWD="dropbear"
echo "$(date "+%d%m%Y %T") : ---------- Commencing Setup of Prerequisites ----------" >> $LOGFILE 2>&1
#### SETUP PREREQUISITES ####
cd /home/ec2-user
set +e
touch cloudair.log
yum update -y >> $LOGFILE 2>&1
yum install docker -y >> $LOGFILE 2>&1
yum install git -y >> $LOGFILE 2>&1
yum install wget -y >> $LOGFILE 2>&1
wget http://dev.mysql.com/get/mysql57-community-release-el7-8.noarch.rpm >> $LOGFILE 2>&1
yum localinstall -y mysql57-community-release-el7-8.noarch.rpm >> $LOGFILE 2>&1
yum install -y mysql-community-server --nogpgcheck  >> $LOGFILE 2>&1
service docker start >> $LOGFILE 2>&1
#### BIND NEW IP ADDRESS ####
ip addr add 123.123.123.123/24 dev eth0 >> $LOGFILE 2>&1
set -e
#### BUILD CONTAINERS ####
echo "$(date "+%d%m%Y %T") : ---------- Commencing Container Builds ----------" >> $LOGFILE 2>&1
cd /home/ec2-user >> $LOGFILE 2>&1
wget https://cloudair123.s3.eu-west-1.amazonaws.com/cloudair.zip >> $LOGFILE 2>&1
unzip cloudair.zip >> $LOGFILE 2>&1
cd /home/ec2-user/cloudair >> $LOGFILE 2>&1
docker build -t cloudair . >> $LOGFILE 2>&1
docker pull mysql:5.7.22 >> $LOGFILE 2>&1
docker run --name mysql --restart unless-stopped -p 3306:3306 -e MYSQL_ROOT_PASSWORD=${JDBC_PWD} -d mysql:5.7.22 >> $LOGFILE 2>&1
mysqlcontid="$(docker ps -aqf "name=mysql")" >> $LOGFILE 2>&1
echo "$(date "+%d%m%Y %T") : Running container ${mysqlcontid} for MySQL" >> $LOGFILE 2>&1
echo "$(date "+%d%m%Y %T") : ---------- Ending Container Builds ----------" >> $LOGFILE 2>&1
#### CREATE DATABASE AND UPDATE SCHEMA ####
echo "$(date "+%d%m%Y %T") : Creating Database & Schema" >> $LOGFILE 2>&1
sleep 20
mysql -h "localhost" -u $JDBC_UID -p$JDBC_PWD --protocol=tcp --skip-ssl -e "CREATE DATABASE ${DB_NAME};" >> $LOGFILE 2>&1
sleep 25
mysql -h "localhost" -u $JDBC_UID -p$JDBC_PWD --protocol=tcp --skip-ssl -e "GRANT SELECT,INSERT,UPDATE,DELETE ON ${DB_NAME}.* TO '${JDBC_UID}'@'%' IDENTIFIED BY '${JDBC_PWD}';" >> $LOGFILE 2>&1
sleep 5
mysql -h "localhost" -u $JDBC_UID -p$JDBC_PWD --protocol=tcp --skip-ssl -e "FLUSH PRIVILEGES;" >> $LOGFILE 2>&1
sleep 10
mysql -h "localhost" -u $JDBC_UID -p$JDBC_PWD --protocol=tcp --skip-ssl < seed_cloudair_db.sql >> $LOGFILE 2>&1
sleep 5
mysql -h "localhost" -u $JDBC_UID -p$JDBC_PWD --protocol=tcp --skip-ssl -e "SHOW DATABASES;" >> $LOGFILE 2>&1
echo "$(date "+%d%m%Y %T") : ---------- Database & Schema creation completed ----------" >> $LOGFILE 2>&1
#### LAUNCH CLOUDAIR ####
echo "$(date "+%d%m%Y %T") : Launching Cloud Air Container" >> $LOGFILE 2>&1
cd /home/ec2-user/cloudair
docker run --rm --env-file setenv.sh --name cloudair \
    --link mysql:mysql         \
    -e MYSQL_DATABASE=${DB_NAME}  \
    -e MYSQL_USER=${JDBC_UID}    \
    -e MYSQL_PASSWORD=${JDBC_PWD} \
    -d -p 80:8080 cloudair &
sleep 5
docker cp cloudair.war `docker ps -l -q`:/usr/local/tomcat/webapps
echo "$(date "+%d%m%Y %T") : Cloud Air Launched" >> $LOGFILE 2>&1
echo >> $LOGFILE 2>&1
echo >> $LOGFILE 2>&1
ipaddress="$(curl http://169.254.169.254/latest/meta-data/public-ipv4)"
#### LAUNCH COMPLETE ####
echo >> $LOGFILE 2>&1
echo >> $LOGFILE 2>&1
echo "$(date "+%d%m%Y %T") : Launch complete ..." >> $LOGFILE 2>&1
echo "##################################################" >> $LOGFILE 2>&1
echo "$(date "+%d%m%Y %T") : Cloud Air is available via http://$ipaddress/cloudair" >> $LOGFILE 2>&1
echo "##################################################" >> $LOGFILE 2>&1