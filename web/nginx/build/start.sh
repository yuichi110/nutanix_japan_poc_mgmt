#!/bin/sh
sed -e "s/{{PORT}}/$PORT/g" /etc/nginx/nginx.tpl > /etc/nginx/nginx.conf
sed -i -e "s/{{API_AUTH_HOST}}/$API_AUTH_HOST/g" /etc/nginx/nginx.conf
sed -i -e "s/{{API_AUTH_PORT}}/$API_AUTH_PORT/g" /etc/nginx/nginx.conf
sed -i -e "s/{{API_CLUSTER_HOST}}/$API_CLUSTER_HOST/g" /etc/nginx/nginx.conf
sed -i -e "s/{{API_CLUSTER_PORT}}/$API_CLUSTER_PORT/g" /etc/nginx/nginx.conf
sed -i -e "s/{{API_TASK_HOST}}/$API_TASK_HOST/g" /etc/nginx/nginx.conf
sed -i -e "s/{{API_TASK_PORT}}/$API_TASK_PORT/g" /etc/nginx/nginx.conf
nginx -g "daemon off;"