FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Clone the Personality Prediction repository
RUN git clone https://github.com/Wizard254/PersonalityPrediction.git

# Change current working directory
WORKDIR /app/PersonalityPrediction

# Download pre-built models
RUN curl "https://dl.dropboxusercontent.com/scl/fi/jbpkf7pblntgy2d35b4m1/dumps.zip?rlkey=t8j0gp41fu6k4zl4b6noorsz2&dl=0" -o dumps.zip -s
RUN curl "https://dl.dropboxusercontent.com/scl/fi/erhlj8kmh28bqi3k3utr8/personalityprediction.zip?rlkey=rkncynnc55bpaf976q98wt7r2&dl=0" -o personalityprediction.zip -s
RUN curl "https://dl.dropboxusercontent.com/scl/fi/7u8eyj7olhniqjgyfdzw3/streamlit.zip?rlkey=siwxbp7dxnrsjp38hpvhbdr3y&dl=0" -o streamlit.zip -s
RUN curl "https://dl.dropboxusercontent.com/scl/fi/mdvwmbc8pp0905ha6ueb5/job_descriptions.csv?rlkey=r37kelksrxkoq98m8uruf0kb6&dl=0" -o job_descriptions.csv -s

# Ensure the job descriptions is in the init directory
RUN mkdir -p init
RUN mv job_descriptions.csv init/

# Extract all models to their directories
RUN python3 unzipall.py

RUN pip install --upgrade pip

RUN pip3 install -r requirements.txt
RUN pip3 install scikit-learn scipy PyMuPDF

# Download nltk data
RUN python3 installs.py

# Set environment variables for Django
ENV DJ_LOCAL=False
ENV DJ_DEBUG=True

EXPOSE 443

#HEALTHCHECK CMD curl --fail http://localhost:8000/_stcore/health
#ENTRYPOINT ["streamlit", "run", "personalityprediction.py", "--server.port=8501", "--server.address=0.0.0.0"]

#ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8080"]
#ENTRYPOINT ["python",  "-m", "uvicorn", "--host", "0.0.0.0", "--port", "80", "PersonalityPrediction.asgi:application"]

# Give executable permissions to the entrypoint file
RUN chmod a+x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
