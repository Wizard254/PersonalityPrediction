from resumeuploads.models import JobDescription
import pandas as pd


def load(file, max_rows=-1):
    df = pd.read_csv(file)
    count = 0

    items: list[JobDescription] = []

    def buffer_insert(insert_all=False):
        def helper(d_max=0):
            if len(items) >= d_max:
                JobDescription.objects.bulk_create(items)
                items.clear()
                pass
            pass

        if insert_all:
            helper()
            pass
        else:
            helper(100)
            pass
        pass

    for index, row in df.iterrows():
        job_title = row['job_title']
        category = row['category']
        job_description = row['job_description']

        jd = JobDescription()
        jd.title = job_title
        jd.description = job_description
        jd.category = category

        # jd.save()
        buffer_insert()

        if count >= max_rows:
            break
            pass
        count += 1
        pass

    # We may have some items in the list
    buffer_insert(insert_all=True)
    pass


def load0():
    load('init/job_descriptions.csv')
    pass


def load1(max_rows):
    load('init/job_descriptions.csv', max_rows=max_rows)
    pass
