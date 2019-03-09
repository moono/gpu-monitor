# gpu-monitor

## rest_api_server
* Parses GPU's memory & utilzation information and broad casts via simple flask server.
* Parses each gpu related processes.
    * If the process is held inside docker container, it will try to obtain container name rather than process name.
    
## web_server
* Collects GPU information from listed servers and try to visualize on web page.