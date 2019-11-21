#!/bin/sh
sed -e "s/{{PORT}}/$PORT/g" /etc/nginx/nginx.tpl > /etc/nginx/nginx.conf
sed -i -e "s^{{WEB_SERVER}}^$WEB_SERVER^g" /etc/nginx/nginx.conf
sed -i -e "s^{{APP_SERVER}}^$APP_SERVER^g" /etc/nginx/nginx.conf
nginx -g "daemon off;"