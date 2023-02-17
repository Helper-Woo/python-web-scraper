from extractors.wwr import extract_wwr_jobs
from extractors.indeed import Indeed

try:
    keyword = input("What do you want to search for?") or "python"

    wwr = extract_wwr_jobs(keyword)
    indeed = Indeed().extract_indeed_jobs(keyword)
    jobs = wwr + indeed

    file = open(f"{keyword}.csv", "w")
    file.write("Position,Company,Location,URL\n")
    for job in jobs:
        file.write(f"{job['position'],job['company'],job['location'],job['link']}\n")
    file.close()
except Exception as error:
    print(error)
finally:
    input("press enter to exit")
