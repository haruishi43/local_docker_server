# $1: port
# $2: container name
# $3: image

docker run --name ${2} \
    --shm-size 16G \
    -dP --privileged \
    -p 488$1:8888 \
    -p 489$1:8889 \
    -p 400$1:22 \
    $3
