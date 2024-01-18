## Database

### Populate the Job Descriptions database

In the Django management shell (`python manage.py shell`), execute:

```python
from init.populate_job_descriptions import load0
load0()
```

# Deployment


```shell
C:\Windows\System32\cmd.exe "/K" C:\Users\Anyona\anaconda31\Scripts\activate.bat C:\Users\Anyona\anaconda31

docker build -t app4 .
docker run -dp 127.0.0.1:8000:8000 app4

docker ps


```

```shell
docker run -p 8501:8501 streamlit
docker run -p 8000:8000 app4

docker run -dp 8000:8000 app4



```


```shell
docker build -t app4 .
docker run -dp 80:80 app4
```

```shell
docker build -t personalityprediction2024_01_07 .
docker run -p 8080:8080 personalityprediction2024_01_07
docker run -dp 8080:8080 personalityprediction2024_01_07

docker exec -it 082152f243e2 bash


```




