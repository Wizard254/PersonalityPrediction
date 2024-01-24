import pandas

from init.batch_apply import BatchApply
from resumeuploads.models import JobDescription


def load(file, max_rows=-1):
    df = pandas.read_csv(file)
    count = 0

    items: list[JobDescription] = []

    ba = BatchApply(JobDescription.objects.bulk_create, items)

    for index, row in df.iterrows():
        job_title = row['job_title']
        category = row['category']
        job_description = row['job_description']

        jd = JobDescription()
        jd.title = job_title
        jd.description = job_description
        jd.category = category

        items.append(jd)
        ba.check_buffer()

        if 0 < max_rows <= count:
            break
            pass
        count += 1
        pass
    ba.check_buffer(True)
    pass


def load_all():
    load('init/job_descriptions.csv')
    pass


def load_some(max_rows):
    load('init/job_descriptions.csv', max_rows=max_rows)
    pass
