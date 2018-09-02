#!/bin/sh

command=$1
LOG_DIR=/apps/web/logs

if [ "$command" = "restart" ]; then
    echo "restart"
    kill -HUP `cat $LOG_DIR/gunicorn.pid`
    ps -ef | grep python

elif [ "$command" = "stop" ]; then
    echo "stop"
    kill -QUIT `cat $LOG_DIR/gunicorn.pid`

elif [ "$command" = "start" ]; then
    echo "start"
    gunicorn -c /apps/web/blog_python/v3/gunicorn.py index:app -D --capture-output --enable-stdio-inheritance
    ps -ef | grep python

else
    echo "usage: $0 start|stop|restart"
fi