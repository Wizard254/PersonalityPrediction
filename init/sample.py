from init.preload_job_descriptions import load_some, load_all

if __name__ == '__main__':
    # Load the first 500 job descriptions
    load_some(500)
    # Load all job descriptions available
    load_all()
    pass
