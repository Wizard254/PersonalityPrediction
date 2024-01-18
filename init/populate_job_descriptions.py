from resumeuploads.models import JobDescription
import pandas as pd


def load(file, max_rows=-1):
    df = pd.read_csv(file)
    count = 0
    for index, row in df.iterrows():
        job_title = row['job_title']
        category = row['category']
        job_description = row['job_description']

        jd = JobDescription()
        jd.title = job_title
        jd.description = job_description
        jd.category = category
        jd.save()
        if count >= max_rows:
            break
            pass
        count += 1
        pass

    pass


def load0():
    load('init/job_descriptions.csv')
    pass


def load1(max_rows):
    load('init/job_descriptions.csv', max_rows=max_rows)
    pass
