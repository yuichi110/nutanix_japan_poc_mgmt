#!/bin/sh
sed -e "s/{{WEB_PORT}}/$WEB_PORT/g" /etc/nginx/nginx.tpl > /etc/nginx/nginx.conf
sed -i -e "s/{{NODE_HOST}}/$NODE_HOST/g" /etc/nginx/nginx.conf
sed -i -e "s/{{NODE_PORT}}/$NODE_PORT/g" /etc/nginx/nginx.conf
sed -i -e "s/{{API_AUTH_HOST}}/$API_AUTH_HOST/g" /etc/nginx/nginx.conf
sed -i -e "s/{{API_AUTH_PORT}}/$API_AUTH_PORT/g" /etc/nginx/nginx.conf
sed -i -e "s/{{API_CLUSTER_HOST}}/$API_CLUSTER_HOST/g" /etc/nginx/nginx.conf
sed -i -e "s/{{API_CLUSTER_PORT}}/$API_CLUSTER_PORT/g" /etc/nginx/nginx.conf
sed -i -e "s/{{API_TASK_HOST}}/$API_TASK_HOST/g" /etc/nginx/nginx.conf
sed -i -e "s/{{API_TASK_PORT}}/$API_TASK_PORT/g" /etc/nginx/nginx.conf
sed -i -e "s/{{API_FOUNDATION_HOST}}/$API_FOUNDATION_HOST/g" /etc/nginx/nginx.conf
sed -i -e "s/{{API_FOUNDATION_PORT}}/$API_FOUNDATION_PORT/g" /etc/nginx/nginx.conf
sed -i -e "s/{{API_EULA_HOST}}/$API_EULA_HOST/g" /etc/nginx/nginx.conf
sed -i -e "s/{{API_EULA_PORT}}/$API_EULA_PORT/g" /etc/nginx/nginx.conf
sed -i -e "s/{{API_SETUP_HOST}}/$API_SETUP_HOST/g" /etc/nginx/nginx.conf
sed -i -e "s/{{API_SETUP_PORT}}/$API_SETUP_PORT/g" /etc/nginx/nginx.conf
nginx -g "daemon off;"