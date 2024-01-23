## Database

### Populate the Job Descriptions database

In the Django management shell (`python manage.py shell`), execute:

```python
from init.populate_job_descriptions import load0
load0()
```

# Deployment


# Feature roadmap
1. [x] User login
2. [x] Upload and Save their resume 
3. [x] Show jobs recommendation
4. [ ] Fuzzy search to search for jobs on their own 
5. [ ] Show related jobs if applied to a job
6. [x] Add/update  jobs as admin login


