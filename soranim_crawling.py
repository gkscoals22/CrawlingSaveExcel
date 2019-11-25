from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from datetime import date
import pandas as pd
import csv
import time

# 경로 설정입니다. 본인 pc에 맞게 설정해주시면 됩니다.
# path = "D:/CrawlingSaveExcel/chromedriver"
path = "E:/CrawlingSaveExcel/chromedriver"
chrome_options = webdriver.ChromeOptions()

# 드라이버 설정
driver = webdriver.Chrome(path, chrome_options=chrome_options)

current_time = date.today()
save_time = current_time.strftime("%y/%m/%d")

#데이터들 리스트화시키기위한 변수
info = []

A_GRADE = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgdmlld0JveD0iMCAwIDIwIDIwIj4KICAgIDxnIGZpbGw9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCI+CiAgICAgICAgPHJlY3Qgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBmaWxsPSIjMjk4MEU0IiByeD0iMyIvPgogICAgICAgIDxwYXRoIGZpbGw9IiNGRkYiIGQ9Ik0xMi4wMzcgMTIuNjY1SDguNDkzTDcuNzIzIDE1SDZMOS40ODkgNWgxLjU4N2wzLjQ0NyAxMEgxMi44bC0uNzYyLTIuMzM1ek04Ljk1MyAxMS4yN2gyLjYzTDEwLjMgNy4zMjhoLS4wNGwtMS4zMDYgMy45NDN6Ii8+CiAgICA8L2c+Cjwvc3ZnPgo="
A_MINUS_GRADE = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgdmlld0JveD0iMCAwIDIwIDIwIj4KICAgIDxnIGZpbGw9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCI+CiAgICAgICAgPHJlY3Qgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBmaWxsPSIjMjk4MEU0IiByeD0iMyIvPgogICAgICAgIDxwYXRoIGZpbGw9IiNGRkYiIGQ9Ik05LjAzNyAxMi42NjVINS40OTNMNC43MjMgMTVIM0w2LjQ4OSA1aDEuNTg3bDMuNDQ3IDEwSDkuOGwtLjc2Mi0yLjMzNXpNNS45NTMgMTEuMjdoMi42M0w3LjMgNy4zMjhoLS4wNGwtMS4zMDYgMy45NDN6bTEwLjEyNi4xNWgtNC4wNTJ2LTEuMzQ1aDQuMDUydjEuMzQ2eiIvPgogICAgPC9nPgo8L3N2Zz4K"
B_PLUS_GRADE = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgdmlld0JveD0iMCAwIDIwIDIwIj4KICAgIDxnIGZpbGw9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCI+CiAgICAgICAgPHJlY3Qgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBmaWxsPSIjNjFDMDNFIiByeD0iMyIvPgogICAgICAgIDxwYXRoIGZpbGw9IiNGRkYiIGQ9Ik0zIDE1VjVoMy4yNzZjMS4xMDQgMCAxLjk2Ny4yMjggMi41OS42ODMuNjIyLjQ1Ni45MzMgMS4xMzcuOTMzIDIuMDQ0IDAgLjQ0LS4xMjQuODM1LS4zNzQgMS4xODgtLjI1LjM1Mi0uNTk2LjYyLTEuMDQuODAzLjY0LjEwNiAxLjEzNC4zODMgMS40OC44MzEuMzQ1LjQ1LjUxOC45NzYuNTE4IDEuNTggMCAuOTM5LS4zMDcgMS42NTItLjkyIDIuMTQtLjYxNC40ODctMS40Ni43MzEtMi41NDEuNzMxSDN6bTEuNjY5LTQuNTQ3djMuMjE1aDIuMjUzYy41NzcgMCAxLjAyLS4xMzIgMS4zMzItLjM5NS4zMTEtLjI2NC40NjctLjY0NS40NjctMS4xNDQgMC0uNTA0LS4xNTMtLjkwNC0uNDYtMS4yMDItLjMwNy0uMjk3LS43MzctLjQ1NS0xLjI5MS0uNDc0SDQuNjY5em0wLTEuMjQzaDEuNzg2Yy41MTcgMCAuOTI2LS4xMjIgMS4yMjYtLjM2Ny4zLS4yNDUuNDUtLjU5Mi40NS0xLjA0IDAtLjQ5NS0uMTU4LS44NjMtLjQ3NC0xLjEwMy0uMzE2LS4yNC0uNzc3LS4zNi0xLjM4LS4zNkg0LjY2OHYyLjg3em0xMC45NDguMjg5aDIuNjF2MS41MjRoLTIuNjF2Mi45NzRoLTEuNjIxdi0yLjk3NGgtMi42MjRWOS41aDIuNjI0VjYuNzE3aDEuNjJ2Mi43ODJ6Ii8+CiAgICA8L2c+Cjwvc3ZnPgo="
B_GRADE = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgdmlld0JveD0iMCAwIDIwIDIwIj4KICAgIDxnIGZpbGw9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCI+CiAgICAgICAgPHJlY3Qgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBmaWxsPSIjNjFDMDNFIiByeD0iMyIvPgogICAgICAgIDxwYXRoIGZpbGw9IiNGRkYiIGQ9Ik03IDE1VjVoMy4yNzZjMS4xMDQgMCAxLjk2Ny4yMjggMi41OS42ODMuNjIyLjQ1Ni45MzMgMS4xMzcuOTMzIDIuMDQ0IDAgLjQ0LS4xMjQuODM1LS4zNzQgMS4xODgtLjI1LjM1Mi0uNTk2LjYyLTEuMDQuODAzLjY0LjEwNiAxLjEzNC4zODMgMS40OC44MzEuMzQ1LjQ1LjUxOC45NzYuNTE4IDEuNTggMCAuOTM5LS4zMDcgMS42NTItLjkyIDIuMTQtLjYxNC40ODctMS40Ni43MzEtMi41NDEuNzMxSDd6bTEuNjY5LTQuNTQ3djMuMjE1aDIuMjUzYy41NzcgMCAxLjAyLS4xMzIgMS4zMzItLjM5NS4zMTEtLjI2NC40NjctLjY0NS40NjctMS4xNDQgMC0uNTA0LS4xNTMtLjkwNC0uNDYtMS4yMDItLjMwNy0uMjk3LS43MzctLjQ1NS0xLjI5MS0uNDc0SDguNjY5em0wLTEuMjQzaDEuNzg2Yy41MTcgMCAuOTI2LS4xMjIgMS4yMjYtLjM2Ny4zLS4yNDUuNDUtLjU5Mi40NS0xLjA0IDAtLjQ5NS0uMTU4LS44NjMtLjQ3NC0xLjEwMy0uMzE2LS4yNC0uNzc3LS4zNi0xLjM4LS4zNkg4LjY2OHYyLjg3eiIvPgogICAgPC9nPgo8L3N2Zz4K"
B_MINUS_GRADE = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgdmlld0JveD0iMCAwIDIwIDIwIj4KICAgIDxnIGZpbGw9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCI+CiAgICAgICAgPHJlY3Qgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBmaWxsPSIjNjFDMDNFIiByeD0iMyIvPgogICAgICAgIDxwYXRoIGZpbGw9IiNGRkYiIGQ9Ik00IDE1VjVoMy4yNzZjMS4xMDQgMCAxLjk2Ny4yMjggMi41OS42ODMuNjIyLjQ1Ni45MzMgMS4xMzcuOTMzIDIuMDQ0IDAgLjQ0LS4xMjQuODM1LS4zNzQgMS4xODgtLjI1LjM1Mi0uNTk2LjYyLTEuMDQuODAzLjY0LjEwNiAxLjEzNC4zODMgMS40OC44MzEuMzQ1LjQ1LjUxOC45NzYuNTE4IDEuNTggMCAuOTM5LS4zMDcgMS42NTItLjkyIDIuMTQtLjYxNC40ODctMS40Ni43MzEtMi41NDEuNzMxSDR6bTEuNjY5LTQuNTQ3djMuMjE1aDIuMjUzYy41NzcgMCAxLjAyLS4xMzIgMS4zMzItLjM5NS4zMTEtLjI2NC40NjctLjY0NS40NjctMS4xNDQgMC0uNTA0LS4xNTMtLjkwNC0uNDYtMS4yMDItLjMwNy0uMjk3LS43MzctLjQ1NS0xLjI5MS0uNDc0SDUuNjY5em0wLTEuMjQzaDEuNzg2Yy41MTcgMCAuOTI2LS4xMjIgMS4yMjYtLjM2Ny4zLS4yNDUuNDUtLjU5Mi40NS0xLjA0IDAtLjQ5NS0uMTU4LS44NjMtLjQ3NC0xLjEwMy0uMzE2LS4yNC0uNzc3LS4zNi0xLjM4LS4zNkg1LjY2OHYyLjg3em0xMS4zNzQgMi4yMTJIMTIuOTl2LTEuMzQ2aDQuMDUzdjEuMzQ2eiIvPgogICAgPC9nPgo8L3N2Zz4K"
C_PLUS_GRADE = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgdmlld0JveD0iMCAwIDIwIDIwIj4KICAgIDxnIGZpbGw9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCI+CiAgICAgICAgPHJlY3Qgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBmaWxsPSIjRUVDMzA3IiByeD0iMyIvPgogICAgICAgIDxwYXRoIGZpbGw9IiNGRkYiIGQ9Ik0xMC4zOTcgMTEuNjgybC4wMTMuMDRjLjAxOC45OC0uMyAxLjc3LS45NTUgMi4zNzMtLjY1NC42MDMtMS41MzcuOTA1LTIuNjUuOTA1LTEuMTMgMC0yLjA0Ny0uMzgyLTIuNzUtMS4xNDVDMy4zNTIgMTMuMDkyIDMgMTIuMTE2IDMgMTAuOTI4di0xLjg1YzAtMS4xODMuMzQ3LTIuMTU5IDEuMDQxLTIuOTI2QzQuNzM2IDUuMzg0IDUuNjQxIDUgNi43NTggNWMxLjE0NCAwIDIuMDQ0LjI5MSAyLjcuODc0LjY1Ny41ODQuOTc2IDEuMzgyLjk1OSAyLjM5N2wtLjAxNC4wNEg4LjgzNGMwLS42NS0uMTc1LTEuMTQ3LS41MjctMS40OTItLjM1Mi0uMzQ1LS44NjgtLjUxNy0xLjU0OS0uNTE3LS42NTggMC0xLjE4LjI2MS0xLjU2NS43ODRzLS41NzggMS4xODMtLjU3OCAxLjk4djEuODYyYzAgLjgwNS4xOTYgMS40Ny41ODggMS45OTMuMzkyLjUyMi45MjYuNzg0IDEuNjAyLjc4NC42NjMgMCAxLjE2Ny0uMTc0IDEuNTEyLS41Mi4zNDUtLjM0OC41MTctLjg0OS41MTctMS41MDNoMS41NjN6bTQuMzg3LTIuMTdoMi41Mzd2MS40ODNoLTIuNTM3djIuODlIMTMuMjF2LTIuODloLTIuNTVWOS41MTNoMi41NVY2LjgwOWgxLjU3NXYyLjcwNHoiLz4KICAgIDwvZz4KPC9zdmc+Cg=="
C_GRADE = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgdmlld0JveD0iMCAwIDIwIDIwIj4KICAgIDxnIGZpbGw9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCI+CiAgICAgICAgPHJlY3Qgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBmaWxsPSIjRUVDMzA3IiByeD0iMyIvPgogICAgICAgIDxwYXRoIGZpbGw9IiNGRkYiIGQ9Ik0xMy4zOTcgMTEuNjgybC4wMTMuMDRjLjAxOC45OC0uMyAxLjc3LS45NTUgMi4zNzMtLjY1NC42MDMtMS41MzcuOTA1LTIuNjUuOTA1LTEuMTMgMC0yLjA0Ny0uMzgyLTIuNzUtMS4xNDVDNi4zNTIgMTMuMDkyIDYgMTIuMTE2IDYgMTAuOTI4di0xLjg1YzAtMS4xODMuMzQ3LTIuMTU5IDEuMDQxLTIuOTI2QzcuNzM2IDUuMzg0IDguNjQxIDUgOS43NTggNWMxLjE0NCAwIDIuMDQ0LjI5MSAyLjcuODc0LjY1Ny41ODQuOTc2IDEuMzgyLjk1OSAyLjM5N2wtLjAxNC4wNGgtMS41NjljMC0uNjUtLjE3NS0xLjE0Ny0uNTI3LTEuNDkyLS4zNTItLjM0NS0uODY4LS41MTctMS41NDktLjUxNy0uNjU4IDAtMS4xOC4yNjEtMS41NjUuNzg0cy0uNTc4IDEuMTgzLS41NzggMS45OHYxLjg2MmMwIC44MDUuMTk2IDEuNDcuNTg4IDEuOTkzLjM5Mi41MjIuOTI2Ljc4NCAxLjYwMi43ODQuNjYzIDAgMS4xNjctLjE3NCAxLjUxMi0uNTIuMzQ1LS4zNDguNTE3LS44NDkuNTE3LTEuNTAzaDEuNTYzeiIvPgogICAgPC9nPgo8L3N2Zz4K"
C_MINUS_GRADE = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgdmlld0JveD0iMCAwIDIwIDIwIj4KICAgIDxnIGZpbGw9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCI+CiAgICAgICAgPHJlY3Qgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBmaWxsPSIjRUVDMzA3IiByeD0iMyIvPgogICAgICAgIDxwYXRoIGZpbGw9IiNGRkYiIGQ9Ik0xMS4zOTcgMTEuNjgybC4wMTMuMDRjLjAxOC45OC0uMyAxLjc3LS45NTUgMi4zNzMtLjY1NC42MDMtMS41MzcuOTA1LTIuNjUuOTA1LTEuMTMgMC0yLjA0Ny0uMzgyLTIuNzUtMS4xNDVDNC4zNTIgMTMuMDkyIDQgMTIuMTE2IDQgMTAuOTI4di0xLjg1YzAtMS4xODMuMzQ3LTIuMTU5IDEuMDQxLTIuOTI2QzUuNzM2IDUuMzg0IDYuNjQxIDUgNy43NTggNWMxLjE0NCAwIDIuMDQ0LjI5MSAyLjcuODc0LjY1Ny41ODQuOTc2IDEuMzgyLjk1OSAyLjM5N2wtLjAxNC4wNEg5LjgzNGMwLS42NS0uMTc1LTEuMTQ3LS41MjctMS40OTItLjM1Mi0uMzQ1LS44NjgtLjUxNy0xLjU0OS0uNTE3LS42NTggMC0xLjE4LjI2MS0xLjU2NS43ODRzLS41NzggMS4xODMtLjU3OCAxLjk4djEuODYyYzAgLjgwNS4xOTYgMS40Ny41ODggMS45OTMuMzkyLjUyMi45MjYuNzg0IDEuNjAyLjc4NC42NjMgMCAxLjE2Ny0uMTc0IDEuNTEyLS41Mi4zNDUtLjM0OC41MTctLjg0OS41MTctMS41MDNoMS41NjN6bTQuODAxLS4zSDEyLjI2di0xLjMwOWgzLjkzOHYxLjMwOXoiLz4KICAgIDwvZz4KPC9zdmc+Cg=="
D_PLUS_GRADE = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgdmlld0JveD0iMCAwIDIwIDIwIj4KICAgIDxnIGZpbGw9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCI+CiAgICAgICAgPHJlY3Qgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBmaWxsPSIjREQ4NjRFIiByeD0iMyIvPgogICAgICAgIDxwYXRoIGZpbGw9IiNGRkYiIGQ9Ik0zIDE1VjVoMy4zMDRjMS4yNjggMCAyLjMuMzk2IDMuMDk0IDEuMTg4Ljc5NC43OTIgMS4xOTEgMS44MTEgMS4xOTEgMy4wNTd2MS41MTdjMCAxLjI1LS4zOTcgMi4yNy0xLjE5MSAzLjA1N0M4LjYwMyAxNC42MDYgNy41NzIgMTUgNi4zMDQgMTVIM3ptMS42NjktOC42NnY3LjMyOGgxLjYzNWMuOCAwIDEuNDM3LS4yNzIgMS45MDktLjgxNC40NzItLjU0My43MDctMS4yNC43MDctMi4wOTJWOS4yMzFjMC0uODQzLS4yMzUtMS41MzUtLjcwNy0yLjA3OC0uNDcyLS41NDItMS4xMDgtLjgxNC0xLjkxLS44MTRINC42N3ptMTAuNjQ4IDMuMTU5aDIuNjF2MS41MjRoLTIuNjF2Mi45NzRoLTEuNjIxdi0yLjk3NGgtMi42MjRWOS41aDIuNjI0VjYuNzE3aDEuNjJ2Mi43ODJ6Ii8+CiAgICA8L2c+Cjwvc3ZnPgo="
D_GRADE = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgdmlld0JveD0iMCAwIDIwIDIwIj4KICAgIDxnIGZpbGw9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCI+CiAgICAgICAgPHJlY3Qgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBmaWxsPSIjREQ4NjRFIiByeD0iMyIvPgogICAgICAgIDxwYXRoIGZpbGw9IiNGRkYiIGQ9Ik02IDE1VjVoMy4zMDRjMS4yNjggMCAyLjMuMzk2IDMuMDk0IDEuMTg4Ljc5NC43OTIgMS4xOTEgMS44MTEgMS4xOTEgMy4wNTd2MS41MTdjMCAxLjI1LS4zOTcgMi4yNy0xLjE5MSAzLjA1Ny0uNzk1Ljc4Ny0xLjgyNiAxLjE4MS0zLjA5NCAxLjE4MUg2em0xLjY2OS04LjY2djcuMzI4aDEuNjM1Yy44IDAgMS40MzctLjI3MiAxLjkwOS0uODE0LjQ3Mi0uNTQzLjcwNy0xLjI0LjcwNy0yLjA5MlY5LjIzMWMwLS44NDMtLjIzNS0xLjUzNS0uNzA3LTIuMDc4LS40NzItLjU0Mi0xLjEwOC0uODE0LTEuOTEtLjgxNEg3LjY3eiIvPgogICAgPC9nPgo8L3N2Zz4K"

def getExcelDataline():
    try:
        file = open("Crawling_result.csv", 'r')
        lines = csv.reader(file)
        return lines
    except:
        return 0

def getGrade(_grade):
    if _grade == A_GRADE:
        return 1
    elif _grade == A_MINUS_GRADE:
        return 1
    elif _grade == B_PLUS_GRADE:
        return 2
    elif _grade == B_GRADE:
        return 2
    elif _grade == B_MINUS_GRADE:
        return 2
    elif _grade == C_PLUS_GRADE:
        return 3
    elif _grade == C_GRADE:
        return 3
    elif _grade ==C_MINUS_GRADE:
        return 3
    elif _grade == D_PLUS_GRADE:
        return 4
    elif _grade == D_GRADE:
        return 4
    else:
        return 1
'''
#사이트 최초 접속
driver.get("https://8percent.kr/loan/index/personal/")
driver.implicitly_wait(3)

#투자하기
driver.find_element_by_xpath("//*[@id='gnb-invest-button']").click()
driver.implicitly_wait(3)

#투자 상품 보기
driver.find_element_by_xpath("//*[@id='gnb-invest-deal-list-button']").click()
driver.implicitly_wait(3)

#개인 신용
driver.find_element_by_xpath("//*[@id='app']/div[2]/nav/p/a[3]").click()
driver.implicitly_wait(3)
'''

#저장할 temp변수들 설정
count = 0

#개인 신용
driver.get("https://8percent.kr/deals/individual")
driver.implicitly_wait(3)

#투자 상품 갯수
count = driver.find_element_by_xpath("//*[@id='app']/div[2]/div/div[2]/div[1]/h1/span").text
count = int(count)

for i in range(2, count+2) :
    try :
        # temp변수들 설정
        save_time = current_time.strftime("%y/%m/%d")
        number = ""
        name = ""
        grade = 0
        profit_percent = 0
        return_time = 0
        now_state = 0
        return_way = 0
        age = 0
        gender = 0
        income_form = 0
        income = 0
        work_size = 0
        in_work_time = 0
        cosume_money = 0
        total_loan = 0

        #개인 신용
        if(driver.current_url != "https://8percent.kr/deals/individual"):
            driver.get("https://8percent.kr/deals/individual")
            driver.implicitly_wait(3)

        #선택
        driver.find_element_by_xpath("//*[@id='app']/div[2]/div/div[2]/div[2]/div[" + str(i) + "]/a").click()
        driver.implicitly_wait(3)

        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
        req = requests.get(driver.current_url, headers=header)
        html = req.text
        parse = BeautifulSoup(html, 'html.parser')

        time.sleep(1)
        #번호 추출
        number = driver.find_element_by_xpath("/html/body/main/header/div[1]/div[1]").text
        driver.implicitly_wait(3)
        number = number[:-1]

        #대출 이름
        name = driver.find_element_by_xpath("/html/body/main/header/div[1]/h1").text
        driver.implicitly_wait(3)

        #나이
        text_age = driver.find_element_by_xpath("/html/body/main/div[2]/section/div[1]/div[2]/p").text
        driver.implicitly_wait(3)
        age = text_age[7:9]
        gender = text_age[11:13]

        #등급
        temp_grade = driver.find_element_by_xpath("/html/body/main/header/div[1]/div[2]/div[1]/p[2]/img")
        driver.implicitly_wait(3)
        temp_grade = temp_grade.get_attribute('src')
        grade = getGrade(temp_grade)

        #예상 수익률
        profit_percent = driver.find_element_by_xpath("/html/body/main/header/div[1]/div[2]/div[3]/p[2]").text
        driver.implicitly_wait(3)
        profit_percent = profit_percent[:-1]

        #모집 현황
        now_state = driver.find_element_by_xpath("/html/body/main/header/div[1]/div[2]/div[9]/p[2]").text
        driver.implicitly_wait(3)
        now_state = now_state.split(" ")[2]
        # print(now_state)

        #상환 방식
        return_way = driver.find_element_by_xpath("/html/body/main/header/div[1]/div[2]/div[7]/p[2]").text
        driver.implicitly_wait(3)

        #상환기간
        return_time = driver.find_element_by_xpath("/html/body/main/header/div[1]/div[2]/div[5]/p[2]").text
        driver.implicitly_wait(3)

        #소득 형태
        income_form = driver.find_element_by_xpath("/html/body/main/div[2]/section/div[1]/div[3]/article/div[2]/table/tr[1]/td").text
        driver.implicitly_wait(3)
        # print(income_form)

        #직장 규모
        work_size = driver.find_element_by_xpath("/html/body/main/div[2]/section/div[1]/div[3]/article/div[2]/table/tr[2]/td").text
        driver.implicitly_wait(3)

        #재직 기간
        in_work_time = driver.find_element_by_xpath("/html/body/main/div[2]/section/div[1]/div[3]/article/div[2]/table/tr[3]/td").text
        driver.implicitly_wait(3)
        in_work_time = in_work_time[:-1]

        #월 평균 소득
        income = driver.find_element_by_xpath("/html/body/main/div[2]/section/div[1]/div[3]/article/div[2]/summary/span[2]").text
        driver.implicitly_wait(3)
        income = income[:-2]

        #월 평균 사용 금액
        cosume_money = driver.find_element_by_xpath("/html/body/main/div[2]/section/div[1]/div[3]/article/div[3]/summary/span[2]").text
        driver.implicitly_wait(3)
        cosume_money = cosume_money[:-2]

        #총 대출 잔액
        total_loan = driver.find_element_by_xpath("/html/body/main/div[2]/section/div[1]/div[3]/article/div[4]/summary/div[2]/span[2]").text
        driver.implicitly_wait(3)

        if total_loan[-2] + total_loan[-1] == "억원":
            total_loan = total_loan[:-2]
            total_loan += "0000"

        else:
            total_loan = total_loan[:-2]
            total_loan = list(total_loan)
            if ' ' in total_loan:
                total_loan.remove(' ')
            if ',' in total_loan:
                total_loan.remove(',')

            temp_loan = total_loan
            total_loan = ""
            for i in temp_loan:
                total_loan += i
            # print(total_loan)
            if total_loan[1] == '억':
                total_loan = list(total_loan)
                if '억' in total_loan:
                    total_loan.remove('억')
                    while (True):
                        if len(total_loan) < 5:
                            total_loan.insert(1, '0')
                        if len(total_loan) == 5:
                            temp_loan = total_loan
                            total_loan = ""
                            for i in temp_loan:
                                total_loan += i
                            break
            elif total_loan[2] == '억':
                total_loan = list(total_loan)
                if '억' in total_loan:
                    total_loan.remove('억')
                    while (True):
                        if len(total_loan) < 6:
                            total_loan.insert(2, '0')
                        if len(total_loan) == 6:
                            temp_loan = total_loan
                            total_loan = ""
                            for i in temp_loan:
                                total_loan += i
                            break
            elif len(total_loan) > 3 and total_loan[3] == '억':
                total_loan = list(total_loan)
                if '억' in total_loan:
                    total_loan.remove('억')
                    while (True):
                        if len(total_loan) < 7:
                            total_loan.insert(3, '0')
                        if len(total_loan) == 7:
                            temp_loan = total_loan
                            total_loan = ""
                            for i in temp_loan:
                                total_loan += i
                            break

        #info 리스트에 데이터 추가
        temp_info = []
        temp_info.append(save_time)
        temp_info.append(number)
        temp_info.append(name)
        temp_info.append(grade)
        temp_info.append(profit_percent)
        temp_info.append(return_time)
        temp_info.append(return_way)
        temp_info.append(now_state)
        temp_info.append(age)
        temp_info.append(gender)
        temp_info.append(income_form)
        temp_info.append(work_size)
        temp_info.append(in_work_time)
        temp_info.append(income)
        temp_info.append(cosume_money)
        temp_info.append(total_loan)

        info.append(temp_info)

        print(number + "호 데이터 저장 완료")
    except:
        print("error발생")


# print(info)

#저장.
if not getExcelDataline() :
    header = ['투자일','번호', '목적', '등급', '예상수익률', '상환기간', '상환방식' , '모집현황', '나이',
              '성별', '소득 형태', '직장 규모','재직 기간' ,'월 평균 소득' ,'월 평균 사용 금액' ,'부채 정보']
    info.insert(0,header)
    data = pd.DataFrame(info)
    data.to_csv('Crawling_result.csv',header=False, index=False, encoding='cp949', mode='w')
else :
    data = pd.DataFrame(info)
    data.to_csv('Crawling_result.csv', header=False, index=False, encoding='cp949', mode='a')