import datetime
import shutil
import tarfile
import logging
import pandas as pd
import numpy as np

CUSTOMER="lab"
TIMEZONE_DELTA="+07:00"
ISSUE_TIME_ON_TZ="2024-05-14T17:30:07"
DELTA_FOR_RANGE = 60

logging.basicConfig(level=logging.DEBUG)
# logging.debug('This will get logged')
# logging.debug('This is a debug message')
# logging.info('This is an info message')
# logging.warning('This is a warning message')
# logging.error('This is an error message')
# logging.critical('This is a critical message')

# Ref: https://realpython.com/python-logging/

LOGSPATH="C:\\Users\\sramanujam\\OneDrive - Fortinet\\FORTISOAR TAC\\AUTOMATION & ANALYTICS\\LOG ANALYZER\\" + CUSTOMER + "\\"
logging.info("Default Log Path: %s" %(LOGSPATH))

ELOGSPATH = LOGSPATH + "\\fortisoar-logs\\var\\log\\cyops\\"
logging.info("Extracted Log Path: %s" %(ELOGSPATH))

def conn_logs_parser(_ELPATH, _UISTIMESTAMP):
    _file = _ELPATH + "cyops-integrations\\connector.log"
    logging.info("Referring File Name: %s" % (_file))

    proddf = pd.DataFrame(columns=["datetime", "log"], index=range(45))
    idxctr = 0
    with open(_file, "r") as pfile:
        for logline in pfile.readlines():
            logline = logline.strip()

            lldate = list(map(int, logline.strip().split("[")[1].split("T")[0].strip().split('-')))
            lltime = list(map(int, logline.strip().split('[')[1].split('T')[1].split('.')[0].strip().split(':')))

            dt = logline.strip().split(']')[0].split("[")[1].split(".")[0].replace("T", " ", 1)
            ll = logline.strip().split('00] ')[1]

            proddf.loc[idxctr].datetime = pd.to_datetime(dt)
            proddf.loc[idxctr].log = ll

            idxctr = idxctr + 1

    fdf = proddf.loc[(proddf['datetime'] >= pd.Timestamp(_UISTIMESTAMP[0])) & (proddf['datetime'] <= pd.Timestamp(_UISTIMESTAMP[1]))]
    print(fdf.to_string())
    exit()

# Prod Log Analyzer.
# /var/log/cyops/cyops-api/prod.log

def prod_logs_parser(_ELPATH, _UISTIMESTAMP):
    _file = _ELPATH + "cyops-api\\prod.log"
    logging.info("Referring File Name: %s" % (_file))

    proddf = pd.DataFrame(columns=["datetime", "log"], index=range(45))
    idxctr = 0
    with open(_file, "r") as pfile:
        for logline in pfile.readlines():
            logline = logline.strip()

            lldate = list(map(int, logline.strip().split("[")[1].split("T")[0].strip().split('-')))
            lltime = list(map(int, logline.strip().split('[')[1].split('T')[1].split('.')[0].strip().split(':')))

            dt = logline.strip().split(']')[0].split("[")[1].split(".")[0].replace("T", " ", 1)
            ll = logline.strip().split('00] ')[1]

            proddf.loc[idxctr].datetime = pd.to_datetime(dt)
            proddf.loc[idxctr].log = ll

            idxctr = idxctr + 1

    fdf = proddf.loc[(proddf['datetime'] >= pd.Timestamp(_UISTIMESTAMP[0])) & (proddf['datetime'] <= pd.Timestamp(_UISTIMESTAMP[1]))]
    print(fdf.to_string())
    exit()

def get_updated_issue_time(_TZDELTA, _ITIME, _DRANGE):
    logging.info("Issue Time (local TZ): %s " % str(_ITIME))
    tzsign = _TZDELTA[0]
    tztime = list(map(int, _TZDELTA[1:].strip().split(':')))

    isdate = list(map(int, _ITIME.strip().split('T')[0].strip().split('-')))
    istime = list(map(int, _ITIME.strip().split('T')[1].strip().split(':')))

    uistime = datetime.datetime(isdate[0], isdate[1], isdate[2], istime[0], istime[1], istime[2]) - datetime.timedelta(
        0, 0, 0, 0, tztime[1], tztime[0], 0)
    logging.info("Issue Time (At UTC): %s " %  str(uistime))

    suistime = uistime - datetime.timedelta(minutes=_DRANGE)
    logging.info("Adding %s Minute Upper Limit: %s" % (str(_DRANGE), str(suistime)))

    euistime = uistime + datetime.timedelta(minutes=_DRANGE)
    logging.info("Subtracting %s Minute Upper Limit: %s" % (str(_DRANGE), str(euistime)))

    return [suistime, euistime ,uistime]

def extract_logs(LOGSPATH):
    _file = tarfile.open(LOGSPATH + "fortisoar-logs.tar.gz")
    print(_file.getnames())
    _file.extractall(".")
    _file.close()

def clear_logs(LOGSPATH):
    shutil.rmtree(LOGSPATH + "fortisoar-logs")

# extract_logs(LOGSPATH)
# clear_logs(LOGSPATH)
UPDATED_ISSUE_TIMESTAMP = get_updated_issue_time(TIMEZONE_DELTA, ISSUE_TIME_ON_TZ, DELTA_FOR_RANGE)
prod_logs_parser(ELOGSPATH, UPDATED_ISSUE_TIMESTAMP)
