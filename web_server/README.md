# gpu-monitor/web_server

# What is it?
* Simple web server that visualizes multiple GPU server's GPU information

# Dependencies
* gpu-monitor/rest_api_server
* Flask
* Docker, Docker-compose

# How to use
1. install & run ```gpu-monitor/rest_api_server``` on each GPU server that want to monitor
2. modify ```config.json``` file to match each ipaddr / port from step 1 with distinguisable name
3. modify ```user_names.json``` file if you want to filter user name on right pie chart legend
4. run web server
```bash
:~/gpu-monitor/web_server$ docker-compose up -d
```