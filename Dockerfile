FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*


RUN curl "https://dl.dropboxusercontent.com/scl/fi/jbpkf7pblntgy2d35b4m1/dumps.zip?rlkey=t8j0gp41fu6k4zl4b6noorsz2&dl=0" -o dumps.zip -s
RUN curl "https://dl.dropboxusercontent.com/scl/fi/erhlj8kmh28bqi3k3utr8/personalityprediction.zip?rlkey=rkncynnc55bpaf976q98wt7r2&dl=0" -o personalityprediction.zip -s
RUN curl "https://dl.dropboxusercontent.com/scl/fi/7u8eyj7olhniqjgyfdzw3/streamlit.zip?rlkey=siwxbp7dxnrsjp38hpvhbdr3y&dl=0" -o streamlit.zip -s
RUN #curl "https://dl.dropboxusercontent.com/scl/fi/w32039hfw1nx0pgy6frjw/installs.py?rlkey=1ob6e3f9tpgk525a4mukwaoc6&dl=0" -o installs.py -s
RUN #curl "https://dl.dropboxusercontent.com/scl/fi/avs25ye5a6f5j3934ka6n/requirements.txt?rlkey=3tlj2fjynqtquxe6k16x0rxnl&dl=0" -o requirements.txt -s
RUN #curl "https://dl.dropboxusercontent.com/scl/fi/3g05vn6yydpmhx96wbn7d/unzipall.py?rlkey=v9bl9dlj797tsdvzxzhkb5tr4&dl=0" -o unzipall.py -s
RUN curl "https://dl.dropboxusercontent.com/scl/fi/mdvwmbc8pp0905ha6ueb5/job_descriptions.csv?rlkey=r37kelksrxkoq98m8uruf0kb6&dl=0" -o job_descriptions.csv -s

# Clone the Personality Prediction repository
RUN git clone https://github.com/Wizard254/PersonalityPrediction.git
RUN #mkdir -p init/
RUN mv job_descriptions.csv init/

RUN python3 unzipall.py

RUN pip install --upgrade pip

RUN pip3 install -r requirements.txt
RUN pip3 install scikit-learn scipy PyMuPDF

RUN python3 installs.py

# Set environment variables for Django
ENV DJ_LOCAL=False
ENV DJ_DEBUG=True

RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
# RUN python3 tmp.py

EXPOSE 8080
#EXPOSE 80

#HEALTHCHECK CMD curl --fail http://localhost:8000/_stcore/health
#ENTRYPOINT ["streamlit", "run", "personalityprediction.py", "--server.port=8501", "--server.address=0.0.0.0"]

#ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8080"]
ENTRYPOINT ["python",  "-m", "uvicorn", "--port", "8080", "PersonalityPrediction.asgi:application"]
