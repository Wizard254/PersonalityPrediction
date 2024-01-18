C:\Windows\System32\cmd.exe "/K" C:\Users\Anyona\anaconda31\Scripts\activate.bat C:\Users\Anyona\anaconda31

docker build -t app4 .
docker run -dp 127.0.0.1:8000:8000 app4

docker ps


docker exec -it e9e9c5ccf89a  bash

echo "ALLOWED_HOSTS = ['*']" >> settings.py

echo "LOGIN_REDIRECT_URL = '/' " >> settings.py

echo "LOGIN_REDIRECT_URL = '/resume-home/'" >> settings.py




docker run -dp 127.0.0.1:8501:8501 streamlit

docker stop 5debc9783e9b



echo '
# Setup logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "debug.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}' >> settings.py


