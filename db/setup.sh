VOL_NAME=augur_vol
CONTAINER_NAME=augur
PASSWORD=changeme
USER=root
docker volume create $VOL_NAME
docker run --name $CONTAINER_NAME -e MYSQL_ROOT_PASSWORD=$PASSWORD -d  \
        -v $VOL_NAME:/var/lib/mysql -p 3306:3306 mysql

docker cp init.sql ${CONTAINER_NAME}:/tmp/init.sql
# # wait for container up and mysql process up
# ret=$( docker exec ${CONTAINER_NAME} bash -c "pgrep mysql")
# while [[ -z $ret ]]; do
#     ret=$( docker exec ${CONTAINER_NAME} bash -c "pgrep mysql")
#     sleep 1
# done
sleep 10
docker exec $CONTAINER_NAME sh -c "mysql -u ${USER} -p${PASSWORD} < /tmp/init.sql"