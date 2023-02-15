from extractors.wwr import extract_wwr_jobs
from extractors.indeed import Indeed

try:
    keyword = input("What do you want to search for?") or "python"

    wwr = extract_wwr_jobs(keyword)
    indeed = Indeed().extract_indeed_jobs(keyword)

    jobs = wwr + indeed

    for job in jobs:
        print(job)
    input("press enter to exit")
except Exception as error:
    print(error)
