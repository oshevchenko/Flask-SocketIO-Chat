Flask-SocketIO-Chat
===================

A simple chat application that demonstrates how to structure a Flask-SocketIO application.

To run this application using **Gunicorn** + **Nginx** do the following:
1. Install **Python3.8**, setup virtual environment and install packages from `requiremets.txt`
2. Configure **Nginx**. Add this to `/usr/local/nginx/conf/nginx.conf`

```text 
       
       ...    
       location / {
            proxy_pass http://127.0.0.1:7777;
            include proxy_params;
       }

        location /socket.io {
            include proxy_params;
            proxy_http_version 1.1;
            proxy_buffering off;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "Upgrade";
            proxy_pass http://127.0.0.1:7777/socket.io;
        }
        ...
```
3. Configure **Nginx**. Add this to /usr/local/nginx/conf/proxy_params
```
# Put it to /usr/local/nginx/conf/proxy_params
proxy_set_header Host $http_host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;

```
4. Configure **Nginx**. Create  `/lib/systemd/system/nginx.service`
```buildoutcfg
# Copy to /lib/systemd/system/nginx.service 
[Unit]
Description=The NGINX HTTP and reverse proxy server
After=syslog.target network-online.target remote-fs.target nss-lookup.target
Wants=network-online.target

[Service]
Type=forking
PIDFile=/usr/local/nginx/logs/nginx.pid
ExecStartPre=/usr/local/nginx/sbin/nginx -t
ExecStart=/usr/local/nginx/sbin/nginx
ExecReload=/usr/local/nginx/sbin/nginx -s reload
ExecStop=/bin/kill -s QUIT $MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```
5. Run **Nginx** service.
```commandline
$ sudo systemctl start nginx
$ sudo systemctl enable nginx
```
6. Create `/etc/systemd/system/flask_chat.service` 
```buildoutcfg
# Copy to  /etc/systemd/system/flask_chat.service
[Unit]
Description=Gunicorn instance to serve Flask-SocketIO-Chat project.
After=network.target

[Service]
User=oshevchenko
Group=www-data

WorkingDirectory=/home/oshevchenko/workspace/flask_venv/Flask-SocketIO-Chat
Environment="PATH=/home/oshevchenko/workspace/flask_venv_3.8/bin"
ExecStart=/home/oshevchenko/workspace/flask_venv_3.8/bin/gunicorn --bind 127.0.0.1:7777 --worker-class eventlet -w 1 chat:app

[Install]
WantedBy=multi-user.target

```
7. Run `flask_chat.service`
```commandline
$ sudo systemctl start flask_chat
$ sudo systemctl enable flask_chat
```
