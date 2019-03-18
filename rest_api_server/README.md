# gpu-monitor/rest_api_server

# What is it?
* Every 1-seconds it try to parse each gpu's ...
    * memory consumtion
    * utilization
    * gpu related process's name and it's memory usage
        * if the gpu process is held in docker container, it parses that docker container's name
* Broadcasts via simple REST api server
    * GET http://<ip-address>:3032/gpu_stat
    
# Dependencies
* Flask
* Only works with Ubuntu with Nvidia graphic cards
    * It uses ```nvidia-smi``` command to parse GPU infomation
* Docker, Docker-compose, dind(Docker in Docker)
* Using python's subprocess to call below commands
    * ```nvidia-smi```
    * ```docker-inspect```

# Important Note
* Try `nvidia-smi` on terminal and see if it outputs fairly fast enough.
* If not, turn persistance mode on.
```bash
$ sudo nvidia-smi --persistence-mode=1
```

## This repo will use following commands, use at your own risk!!
* When inside container, it cannot parse processes that are not created inside the same container
    * which leads to use 
    * ```docker run --pid=host ... ... ...```
* To run docker commands (```docker inspect```) inside docker container, it needs to install docker.io 
    * which leads to use 
    * ```docker run -v /var/run/docker.sock:/var/run/docker.sock ... ... ...```
    * Ref
        * https://stackoverflow.com/questions/20995351/docker-how-to-get-container-information-from-within-the-container
        * https://stackoverflow.com/questions/27879713/is-it-ok-to-run-docker-from-inside-docker
        * https://forums.docker.com/t/how-can-i-run-docker-command-inside-a-docker-container/337
* To get docker ID with process id (PID)
    * it needs host's ```/proc``` mapped into container and parse it with,
    * ```cat /proc/<pid>/cgroup```
    * which leads to use
    * ```docker run -v /proc:/host_proc ... ... ...```
    
# How to use

```bash
# get the source
:~$ git clone https://github.com/moono/gpu-monitor.git
:~$ cd gpu-monitor/rest_api_server

# run docker-compose
:~/gpu-monitor/rest_api_server$ docker-compose up -d
```

# Test
```bash
:~$ curl -X GET http://127.0.0.1:3032/gpu_stat
```