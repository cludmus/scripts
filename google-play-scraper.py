from fileinput import filename
import json
from platform import release
from turtle import title
from google_play_scraper import search, app
from datetime import datetime, date
import statistics
import xlwt
from xlwt import Workbook
import win32com.client as win32
import os


excel_filename = "google-play-scrap-results.xls"
excel_sheet_name = "Sheet 1"
number_of_results = 30 # google play maximum is 30
search_terms = []
titles_have_to_contain = []
#search_terms = ["weather app"] 
#titles_have_to_contain = [["weather", "app"]] # have to be same length as search_terms
keyword_file = open("wallpaper-ideas.txt", "r")
file_lines = keyword_file.readlines()
for line in file_lines:
    line = line.rstrip()
    if line != "" and line[0] != "#":
        search_terms.append(line)
        line_words = line.split()
        titles_have_to_contain.append(line_words)
        print(line)
        print(line_words)
        print("")



def excel_autofit():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = excel.Workbooks.Open(dir_path + "\\" +excel_filename)
    ws = wb.Worksheets(excel_sheet_name)
    ws.Columns.AutoFit()
    wb.Save()
    excel.Application.Quit()

class App:
    def __init__(self, title, score, installs, days_since_release):
        self.title = title
        self.score = score
        self.installs = installs
        self.days_since_release = days_since_release


# Workbook is created
workbook = Workbook()
  
# add_sheet is used to create sheet.
sheet = workbook.add_sheet(excel_sheet_name)
  
sheet.write(0, 0, "keyword")
sheet.write(0, 1, "number_of_apps")
sheet.write(0, 2, "number_of_new_apps")
sheet.write(0, 3, "new_apps_yearly_median_downloads")
sheet.write(0, 4, "new_apps_yearly_average_downloads")
sheet.write(0, 5, "new_app_highest_yearly_download")
sheet.write(0, 6, "all_downloads")
sheet.write(0, 7, "yearly_downloads")
sheet.write(0, 8, "median_rating")

for i in range(number_of_results):
    sheet.write(0, 9+i, str(i+1)+".")

workbook.save(excel_filename)  
excel_autofit()

current_row = 1


for index in range(len(search_terms)):
    result = search(search_terms[index],
                    lang="en",  # defaults to 'en'
                    country="us",  # defaults to 'us'
                    n_hits=number_of_results  # defaults to 30 (= Google's maximum)
    )

    apps_list = []

    for i in range(len(result)):
        title = result[i].get("title")
        title = title.encode('ascii', 'ignore').decode('ascii')
        boolreq = True
        for item in titles_have_to_contain[index]:
            if not item in title.lower():
                boolreq = False
                break
        if not boolreq:
            print("skipping due to title: " + title + "\n")
            continue
        app_id = result[i].get("appId")
        app_result = app(
            app_id,
            lang='en', # defaults to 'en'
            country='us' # defaults to 'us'
        )
        
        release_date = app_result.get("released")
        if release_date == None:
            print("skipping due to no release date: " + title + "\n")
            continue

        
        installs = app_result.get("realInstalls")
        release_date = datetime.strptime(release_date, '%b %d, %Y').date()
        number_of_days = (date.today()-release_date).days
        score = result[i].get("score")

        apps_list.append(App(title,score,installs,number_of_days))


        print(title)
        print(str(installs) + " installs")
        print(str(number_of_days) + " days ago")
        print(str(score) + " score")
        print("")

    ##############################################################

    

    ## result fields
    keyword = search_terms[index]
    number_of_apps = len(apps_list)
    number_of_new_apps = 0
    new_apps_yearly_median_downloads = 0
    new_apps_yearly_average_downloads = 0
    new_app_highest_yearly_download = 0
    all_downloads = 0
    yearly_downloads = 0
    median_rating = 0
    downloads_list = []
    days_since_release_list = []



    ## step fields
    new_apps_downloads_list = []
    rating_list = []
    sorted_apps = sorted(apps_list, key=lambda x: x.installs, reverse=True)

    for current_app in apps_list:
        if current_app.days_since_release < 365:
            new_apps_downloads_list.append(current_app.installs)
        all_downloads += current_app.installs
        yearly_downloads += current_app.installs * 365 / current_app.days_since_release
        rating_list.append(current_app.score)
        
    for current_app in sorted_apps:
        downloads_list.append(f"{current_app.installs:,}")
        days_since_release_list.append(f"{current_app.days_since_release:,}")

    number_of_new_apps = len(new_apps_downloads_list)
    new_apps_yearly_median_downloads =  statistics.median(new_apps_downloads_list) if len(new_apps_downloads_list) != 0 else 0
    new_apps_yearly_average_downloads = round(statistics.mean(new_apps_downloads_list)) if len(new_apps_downloads_list) != 0 else 0 
    new_app_highest_yearly_download = max(new_apps_downloads_list) if len(new_apps_downloads_list) != 0 else 0
    median_rating = round(statistics.median(rating_list), 3) if len(rating_list) != 0 else 0
    yearly_downloads = round(yearly_downloads)



    #####################################################

    print("keyword: " + str(keyword))
    print("number_of_apps: " + str(number_of_apps))
    print("number_of_new_apps: " + str(number_of_new_apps))
    print("new_apps_yearly_median_downloads: " + str(new_apps_yearly_median_downloads))
    print("new_apps_yearly_average_downloads: " + str(new_apps_yearly_average_downloads))
    print("new_app_highest_yearly_download: " + str(new_app_highest_yearly_download))
    print("all_downloads: " + str(all_downloads))
    print("yearly_downloads: " + str(yearly_downloads))
    print("median_rating: " + str(median_rating))
    print("downloads_list: " + str(downloads_list))
    print("days_since_release_list: " + str(days_since_release_list))



    sheet.write(current_row, 0, str(keyword))
    sheet.write(current_row, 1, str(number_of_apps))
    sheet.write(current_row, 2, str(number_of_new_apps))
    sheet.write(current_row, 3, f"{new_apps_yearly_median_downloads:,}")
    sheet.write(current_row, 4, f"{new_apps_yearly_average_downloads:,}")
    sheet.write(current_row, 5, f"{new_app_highest_yearly_download:,}")
    sheet.write(current_row, 6, f"{all_downloads:,}")
    sheet.write(current_row, 7, f"{yearly_downloads:,}")
    sheet.write(current_row, 8, str(median_rating))

    for i in range(len(downloads_list)):
        sheet.write(current_row, 9+i, downloads_list[i])
        sheet.write(current_row+1, 9+i, days_since_release_list[i])

    workbook.save(excel_filename)
    excel_autofit()
    current_row+=2
