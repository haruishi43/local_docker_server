# Useful Commands and Useful Knowledge:

## How to stop

Running the server locally will use up local resources, so when you're not using the server, you should stop it.

```Bash
$ docker stop $(docker ps -aq)
```

Note that you can restart the server using `./run_all.sh` again.

## How to delete your containers and images

```Bash
$ docker stop $(docker ps -aq)
$ docker rm $(docker ps -aq)  # delete all containers
$ docker rmi $(docker images -q)  # delete all images
```


## Build Command:
```
docker build ./ -t [Image Name]
```

## Stop all containers:
```
docker stop $(docker ps -a -q)
```

## Prune:
```
docker system prune -a -f
```

## Shared Memory:

Sometime, when dataloaders use up a lot of shared memory, you might need to expand `--shm-size`.
You can do this by changing `--shm-size` on the `run.sh` scripts for each server, but if you're already running the container, you can manually change the shared memory size by first checking the maximum shared memory size by running:
```
df -h /dev/shm
```
Then in the container run:
```
sudo mount -o remount,size=<shm-size> /dev/shm
```
where `<shm-size>` should be no larger than the host's `/dev/shm` size.
