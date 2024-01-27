# User should not run this script
exit

# Delete all docker images and stopped containers
docker system prune -a

# List all docker volumes
docker volume ls

# delete a given docker volume named, vol1
docker volume rm vol1

# When you run this command, it will start printing the contents of
# the file (logger.txt) to the console. It will continue to monitor the file
# and display any new lines that are written to it in real-time.
tail -f logger.txt

# START Deployment

# Download the latest Dockerfile
curl -O https://raw.githubusercontent.com/Wizard254/PersonalityPrediction/master/Dockerfile

# Build the docker container, tag it as `app2` in this case
docker build -t app2 .

# (Optional) Check the container TAG and version
$ docker images
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
app2         latest    b7bbe8834d49   25 seconds ago   4.09GB
$

# Create the docker volume, named `persist_vol`
docker volume create persist_vol

# Start the `app2` container, mounting the necessary docker volumes, `persist_vol` to `/persist_vol`
## Either run in foreground
docker run -p 80:80 --mount type=volume,src=persist_vol,target=/persist_vol app2

## Or as a daemon (recommended)
docker run -dp 80:80 --mount type=volume,src=persist_vol,target=/persist_vol app2

# Get container id
## Once started, we can get the container id from the command `docker ps`
$ docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS                                       NAMES
edc492093c7c   app2      "./entrypoint.sh"        58 seconds ago   Up 57 seconds   0.0.0.0:80->80/tcp, :::80->80/tcp           fervent_clarke
$

# - As shown above, we note that the started container has the id: `edc492093c7c`

# Using the container id: `edc492093c7c44f`, we can open an interactive bash shell in the container
docker exec -it edc492093c7c44f bash
# The above commands opens a shell as illustrated below:
$ docker exec -it edc492093c7c44f bash
root@edc492093c7c:/app/PersonalityPrediction# ls
Dockerfile             entrypoint.sh   notes.sh                   requirements.txt       streamlit                    tmp.py
PersonalityPrediction  heavyimport.py  old                        resumeuploads          streamlit.zip                unzipall.py
README.md              init            personalityprediction.py   runpredictor.py        streamlitjobcategorypred.py
dumps                  installs.py     personalityprediction.zip  runpredictorclient.py  templates
dumps.zip              manage.py       preprocessing              static                 textpreprocessing.py
root@edc492093c7c:/app/PersonalityPrediction#

## From the shell we must check if we have some migrations to run

## From the shell we may choose to create a superuser


## Or open the Django shell


## Or read the Django server log file
### In this Django project, we have the logfile at `/persist_vol/debug.log`
### We can only read the most recent logs as the log file may be very large

## Or read the Django server log file in realtime

# Run some project specific initializations

## 1. Load the Job Predictions CSV data to the database
$ docker exec -it edc492093c7c44f bash
root@edc492093c7c:/app/PersonalityPrediction# ls
Dockerfile             entrypoint.sh   old                        runpredictor.py              templates
PersonalityPrediction  heavyimport.py  personalityprediction.py   runpredictorclient.py        textpreprocessing.py
README.md              init            personalityprediction.zip  static                       tmp.py
__pycache__            installs.py     preprocessing              streamlit                    unzipall.py
dumps                  manage.py       requirements.txt           streamlit.zip
dumps.zip              notes.sh        resumeuploads              streamlitjobcategorypred.py
root@edc492093c7c:/app/PersonalityPrediction# python manage.py shell
Python 3.11.7 (main, Jan 11 2024, 10:43:21) [GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from init.populate_job_descriptions import load1
>>> load1(1000)
>>> quit()
root@edc492093c7c:/app/PersonalityPrediction#


## 2. Start the `runpredictor.py` background Personality Prediction process to load the prediction models


# END Deployment

# Local deployment with uvicorn
python3 -m uvicorn --host 0.0.0.0 --port 8080 PersonalityPrediction.asgi:application

