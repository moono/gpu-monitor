# gpu-monitor/rest_api_server

# Dependencies
* Only works with Ubuntu & Nvidia graphic cards
    * It uses `nvidia-smi` command to parse GPU infomation 
    * -> needs nvidia graphic card driver
* Docker, Docker-compose

# Important Note
* Try `nvidia-smi` on terminal and see if it outputs fairly fast enough.
* If not, turn persistance mode on.
```bash
moono@moono-ubuntu:~$ sudo nvidia-smi --persistence-mode=1
```

## This repo will use following commands, use at your own risk!!
* When inside container, it cannot parse processes that are not created inside the same container
    * which leads to use ```docker run --pid=host ... ... ...```
* To run docker commands (```docker inspect```) inside docker container, it needs to install docker.io 
    * which leads to use ```docker run -v /var/run/docker.sock:/var/run/docker.sock ... ... ...```
    * Ref
        * https://stackoverflow.com/questions/20995351/docker-how-to-get-container-information-from-within-the-container
        * https://stackoverflow.com/questions/27879713/is-it-ok-to-run-docker-from-inside-docker
        * https://forums.docker.com/t/how-can-i-run-docker-command-inside-a-docker-container/337
* To get docker ID with ```cat /proc/<pid>/cgroup```, it needs host's /proc mapped into container
    * ```docker run -v /proc:/host_proc ... ... ...```
    
# How to use

```bash
# get the source
moono@moono-ubuntu:~$ git clone https://github.com/moono/gpu-monitor.git
moono@moono-ubuntu:~$ cd gpu-monitor/rest_api_server

# run docker-compose
moono@moono-ubuntu:~/gpu-monitor/rest_api_server$ docker-compose up -d --build
```

# Test
```bash
moono@moono-ubuntu:~$ curl -X GET http://127.0.0.1:3032/gpu_stat
```