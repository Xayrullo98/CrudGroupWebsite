"""
[Unit]
Description= This is a Gunicorn instance from PieceX tutorial for our hello world application
After=network.target
[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/xayrullo/crud-api
Environment="PATH=/home/xayrullo/crud-api"
ExecStart=/home/xayrullo/crud-api/bin/gunicorn -workers 3 - bind unix:crud-api.sock -m 007 wsgi:app
[Install]
WantedBy=multi-user.target
/home/xayrullo/crud-api

sudo ln -s /etc/nginx//home/xayrullo/crud-api /etc/nginx/sites-enabled
home/xayrullo/crud-api/bin/gunicorn --workers 3 --bind unix:crud-api.sock -m 007 wsgi:app
/home/xayrullo/crud-api/venv/bin/gunicorn --workers 3 --bind unix:crud-api.sock -m 007 wsgi:app
"""