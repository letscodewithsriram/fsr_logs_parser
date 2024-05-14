import datetime
import shutil
import tarfile
import pandas as pd
import numpy as np

print ("Hello World!")

CUSTOMER="lab"
TIMEZONE_DELTA="+07:00"
ISSUE_TIME_ON_TZ="2024-05-14T07:30:07"

LOGSPATH="C:\\Users\\sramanujam\\OneDrive - Fortinet\\FORTISOAR TAC\\AUTOMATION & ANALYTICS\\LOG ANALYZER\\" + CUSTOMER + "\\"
print(LOGSPATH)
ELOGSPATH = LOGSPATH + "\\fortisoar-logs\\var\\log\\cyops\\"

# Prod Log Analyzer.
# /var/log/cyops/cyops-api/prod.log

def prod_logs_parser(_ELPATH, _UISTIMESTAMP):
    _file = _ELPATH + "cyops-api\\prod.log"
    print(_file)

    proddf = pd.DataFrame(columns=["datetime", "log"], index=range(45))
    idxctr = 0
    with open(_file, "r") as pfile:
        for logline in pfile.readlines():
            logline = logline.strip()
            # print (logline)
            ## [2024-05-14T07:30:07.456299+00:00] app.ERROR: label: This value should not be blank. [] []
            lldate = list(map(int, logline.strip().split("[")[1].split("T")[0].strip().split('-')))
            lltime = list(map(int, logline.strip().split('[')[1].split('T')[1].split('.')[0].strip().split(':')))
            dt = logline.strip().split(']')[0].split("[")[1].split(".")[0].replace("T", " ", 1)
            ll = logline.strip().split('00] ')[1]
            # print(dt)
            proddf.loc[idxctr].datetime = pd.to_datetime(dt)
            proddf.loc[idxctr].log = ll
            # print(datetime.datetime(lldate[0], lldate[1], lldate[2], lltime[0], lltime[1], lltime[2]))
            # print(proddf)
            idxctr = idxctr + 1
    # df['date'] > '2000-6-1') & (df['date'] <= '2000-6-10')
    print(proddf.loc[proddf['datetime'] < pd.Timestamp("2024-05-14 15:30:24")])
    exit()

def get_updated_issue_time(_TZDELTA, _ITIME):
    tzsign = _TZDELTA[0]
    tztime = list(map(int, _TZDELTA[1:].strip().split(':')))

    isdate = list(map(int, _ITIME.strip().split('T')[0].strip().split('-')))
    istime = list(map(int, _ITIME.strip().split('T')[1].strip().split(':')))
    print(isdate, istime)

    uistime = datetime.datetime(isdate[0], isdate[1], isdate[2], istime[0], istime[1], istime[2]) - datetime.timedelta(
        0, 0, 0, 0, tztime[1], tztime[0], 0)

    return uistime

def extract_logs(LOGSPATH):
    _file = tarfile.open(LOGSPATH + "fortisoar-logs.tar.gz")
    print(_file.getnames())
    _file.extractall(".")
    _file.close()

def clear_logs(LOGSPATH):
    shutil.rmtree(LOGSPATH + "fortisoar-logs")

# extract_logs(LOGSPATH)
# clear_logs(LOGSPATH)
UPDATED_ISSUE_TIMESTAMP = get_updated_issue_time(TIMEZONE_DELTA, ISSUE_TIME_ON_TZ)
prod_logs_parser(ELOGSPATH, UPDATED_ISSUE_TIMESTAMP)
