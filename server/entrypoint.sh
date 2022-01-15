if [ "$POSTGRES_DB" = "speedcraft" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST 5432; do
      sleep 1
    done
    sleep 5
    echo "PostgreSQL started"
fi

psql $DATABASE_URL -f /var/webserver/initdb.sql
rm /var/webserver/initdb.sql

cd /var/webserver && python3 webserver.py &

# cd /var/mc_server && java -Xmx1024M -Xms1024M -jar server.jar nogui
cd /var/mc_server && python3 ../webserver/toMinecraft.py | java -Xmx1024M -Xms1024M -jar server.jar nogui


exec "$@"