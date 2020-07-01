#!/usr/bin/env bash
createdb uniq;
psql -c "create user uniq with password 'uniq'";
psql -c 'grant all privileges on database uniq to uniq';
sudo rabbitmqctl add_user uniq uniq
sudo rabbitmqctl add_vhost uniq
sudo rabbitmqctl set_user_tags uniq uniq_tag
sudo rabbitmqctl set_permissions -p uniq uniq ".*" ".*" ".*"
mkdir logs;