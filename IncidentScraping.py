from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import pandas as pd

def IncidentScraper(region,day,file,headerCol):
    AllIncidents=[]
    url = 'https://fireandemergency.nz/incidents-and-news/incident-reports/incidents?region='+region+'&day='+day 
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    Incidents = soup.find_all("div", class_="report__table__body")
    for incident in Incidents:
        data = incident.find_all("div",class_="report__table__cell report__table__cell--value")
        singleIncident = []
        for record in data:  # loop will run 6 times 
            singleIncident.append(record.find("p").text)
        
        AllIncidents.append(singleIncident)
    
    # Populate data to csv file
    data_frame = pd.DataFrame(AllIncidents, columns=['Incident number', 'Date and time', 'Location', 'Duration','Attending Stations/Brigades','Result'])
    #data_frame["Region"] = region  As we have separate file for regions now
    data_frame["Day"] = day
    if (headerCol):
        data_frame.to_csv(file,mode='a+', index=True, encoding='utf-8')
    else:
        data_frame.to_csv(file,mode='a+', index=True, header=False, encoding='utf-8')

# Generating list of last 7 days in reverse order
current_date = datetime.now()
week_days = []
for _ in range(7):
    week_days.append(current_date.strftime('%A'))
    current_date -= timedelta(days=1)

# Calling our scraper function, running time approx 6 minutes
    
Regions = ['North','Central','South']
for i in range (3):
    header = True
    for j in range (7):
        if j > 0:
            header = False
        IncidentScraper(str(i+1),week_days[j],'incident_'+Regions[i]+'.csv', header)