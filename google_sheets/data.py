#lib import
import os
from datetime import date

#sheets info
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SPREADSHEET_ID = "1uPy0R0AwzQ0m_rarDM_jGUGdulKABDPJXIB8LyfsQKY"

#date reforms

mes = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь",
       "Декабрь"]

def DateToProgramm(inp):
    datee = [2023, 0, 0]
    mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    while inp > 0:
        datee[1] += 1
        if datee[1] == 13:
            datee[1] = 1
            datee[0] += 1
        inp -= mes[datee[1] - 1]

    datee[2] += mes[datee[1] - 1] + inp
    return datee

def DateToData(inp):
    return (
    lambda x: (int(x[0]) - 2023) * 365 + sum([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][0:int(x[1]) - 1]) + int(
        x[2]))(str(inp).split("-"))

def DateToUser(inp):
    return (lambda x: [x[0], mes[x[1] - 1], x[2]])(Date(inp))

#mer classes

mers = []

class Mer:
    def __init__(self, mer_info):
        "ID, name, date, time, info, lesson="", teacher="""
        self.ID = mer_info[0]
        self.name = mer_info[1]
        self.date = mer_info[2]
        self.time = mer_info[3]
        self.info = mer_info[4]
        self.lesson = mer_info[5]
        self.teacher = mer_info[6]

def MerFindIDWithName(name):
    for mer in mers:
        if mer.name == name:
            return mer.ID

def MerFindIDWithDate(date):
    for mer in mers:
        if mer.date == date:
            return mer.ID

def MerInfo(ID):
    return [mers[ID].name, mers[ID].date, mers[ID].time, mers[ID].info, mers[ID].lesson, mers[ID].teacher]

def MerClass(ID):
    return mers[ID]

def MerInfoDate(ID):
    return mers[ID].date

def MerInfoTime(ID):
    return mers[ID].time

def MerInfoInfo(ID):
    return mers[ID].info

def MerInfoLesson(ID):
    return mers[ID].lesson

def MerInfoTeacher(ID):
    return mers[ID].teacher


#data classes

dates = []

class Date:
    def __init__(self, date_info):
        self.ID = int(date_info[0])
        self.date = DateToProgramm(int(date_info[1]))
        self.dn = int(date_info[2])
        self.mer = list(map(int, date_info[3].split("$")))
        self.info = date_info[4]

def DateFindID(date):
    for elem in dates:
        if date == elem.date:
            return elem.ID

def DateInfo(ID):
    return [dates[ID].date, dates[ID].dn, dates[ID].mer, dates[ID].info]

def DateClass(ID):
    return dates[ID]

def DateInfoDate(ID):
    return dates[ID].date

def DateInfoDn(ID):
    return dates[ID].dn

def DateInfoMer(ID):
    return dates[ID].mer

def DateInfoInfo(ID):
    return dates[ID].info

#sheets main
def main():
    credentials = None
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write((credentials.to_json()))

    try:
        service = build("sheets", "v4", credentials=credentials)
        sheets = service.spreadsheets()

        result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range="Sheet1!A1:G4").execute()

        values = result.get("values", [])

        for row in values:
            for date_info in row:
                if date_info != "":
                    dates.append(Date(date_info.split("|")))

        for out in dates:
            print(out.mer)

    except HttpError as error:
        print(error)

if __name__ == "__main__":
    main()