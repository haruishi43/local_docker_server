# $1: port
# $2: container name
# $3: image

docker run --name ${2} \
    --shm-size 16G \
    -dP --privileged \
    -p 388$1:8888 \
    -p 389$1:8889 \
    -p 300$1:22 \
    $3
