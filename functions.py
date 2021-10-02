# coding=utf8
import requests
import numpy as np
import pandas as pd
import time
from bs4 import BeautifulSoup
import sys
import os
import re
from random import choice

def get_folder():
    return os.path.dirname(os.path.abspath(__file__))



# define function for random header

def randomheader():
    """
    Gibt einen Header mit zufälligem User Agent für eine Request zurück
    """
    desktop_agents = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
                     ]
    return {
        'Host': 'www.amazon.de',
        'User-Agent': choice(desktop_agents), #nimm dir einen Agent aus der Liste
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
        'Accept-Language' : 'en-US,en;q=0.5',
        'Accept-Encoding' : 'gzip', 
        'DNT' : '1', # Do Not Track Request Header 
        'Connection' : 'keep-alive',
        'Upgrade-Insecure-Requests': '1', #http wird zu https
        'DNT' : '1' # Do Not Track Request Header 
        }

#define the function to read the actual website and return the html code
def htmlreader(url,header):
    

    session = requests.session()
    header = header
    session.headers = header
#now begin download the source code


    response = session.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    else:
        return response.status_code
    
# define the function to shorten the search function
def finder(values,otype,definer=None):
    if definer == None:
        if values.find(otype):
            return values.find(otype).get_text().strip()
        else:
            return '-1'
    else:
        if values.find(otype,definer):
            return values.find(otype,definer).get_text().strip()
        else:
            return '-1'

def links_holen(suchstring,anz_seiten=1):
    """
    Funktion um zu einem Suchbegriff (var=suchstring) bei Amazon die zugehörigen Links zu bekommen.
    Es ist auswählbar wie viele Seiten man suchsuchen will.
    
    Ausgabe ist eine liste
    
    """
    links = list()
    suchstring = suchstring.replace(" ","+") #damit man einfach Klartext eingeben kann im Aufruf der Suche
    headers = randomheader() #Zufälligen Header holen

    for item in range(1, anz_seiten+1): #durch eine vorgegebene Anzahl an Seiten suchen nach Artikeln
        r = requests.get(
            f'https://www.amazon.de/s?k={suchstring}&page={item}&ref=sr_pg_{item}', headers=headers) #URL generieren die in Amazon nach dem Suchstring sucht
        soup = BeautifulSoup(r.text, 'html.parser')
        for item in soup.findAll('a', attrs={'class': 'a-link-normal a-text-normal'}): #Artikellistenelemente haben Klasse 'a-link-normal a-text-normal' und die Links liegen unter href
            link = f"https://www.amazon.de{item.get('href')}"
            #print(link)
            links.append(link)
            
            
        sek_pause = [3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5]
        sleeptime = choice(sek_pause) 
        time.sleep(sleeptime) #nach jeder Seite um Bot Detektion zu vermeiden
        
        
    return links


def review_scraper(url):
    """
    Funktion um die Reviews aus den Amazon webseiten zu laden und in Listenform zurück zu geben. Dazu werden die Urls an die funktion übergeben.
    die Erste liste enthält die Produktinformationen und die 2. Liste die Reviewinformationen. Sonderzeichen werden entsprechend umgewandelt.
    Genau so wie Monate.

    """
    list_komp = []
    starturl = url
    values = htmlreader(url,randomheader())
    dir_rating = [{'data-hook':'review-star-rating'},{'data-hook':'review-star-rating'},{'data-hook':'cmps-review-star-rating'}]
    dir_title = ['a','span']
    # create mapping Dictionarys
    chars = {'ö':'oe','ä':'ae','ü':'ue','Ö':'Oe','Ä':'Ae','Ü':'Ue'}
    months = 'januar|februar|märz|april|mai|juni|juli|august|september|oktober|november|dezember'
    monthmap = {'januar':'january','februar':'february','märz':'march'
                ,'april':'april','mai':'may','juni':'june','juli':'july','august':'august','september':'september'
                ,'oktober':'october','november':'november','dezember':'december'}
    # create the header list and dataframe out of it
    title = finder(values,'h1',{'id':'title'})
    our_price = finder(values,'span',{'id':'priceblock_ourprice'})
    price = finder(values,'span',{'id':'priceblock_saleprice'})
    avg_rating = finder(values,'span', {'class':'a-icon-alt'})
    
    found=True
    # get the first link to the review site
    url = values.find('a', {'data-hook':'see-all-reviews-link-foot'})['href']
    
    # run loop and extract the data
    while found == True:
        
        
        sek_pause = [3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5]
        sleeptime = choice(sek_pause) 
        time.sleep(sleeptime) #nach jedem Fragen um Bot Detektion zu vermeiden
        
        for i in range(0,10): #einfach mal ein paar mal versuchen falls es beim ersten Mal nicht klappt
            try:
                if url[0] == '/':
                    url = 'https://www.amazon.de' + url
                rh = randomheader()
                values = htmlreader(url,rh)
                reviews = values.findAll('div', class_='a-section celwidget')
                for review in reviews:
                    rating = '-1'
                    for keyvalue in dir_rating:
                        if rating is None or rating == '-1':
                            rating = finder(review,'i',keyvalue)
                    r_title = '-1'
                    for keyvalue in dir_title:
                        if r_title is None or r_title == '-1':
                            r_title = finder(review,keyvalue,{'data-hook':'review-title'})
                    r_content = finder(review,'span', {'data-hook':'review-body'})
                    verified = finder(review,'span',{'data-hook':'avp-badge'})
                    helpful = re.sub('[^0-9]','',finder(review,'span',{'data-hook':'helpful-vote-statement'}))
                    c_comments = finder(review,'span',{'class':'review-comment-total aok-hidden'})
                    y_published = re.findall('[0-9]{4}$',finder(review,'span',{'data-hook':'review-date'}))[0]
                    month_str = re.search(months,finder(review,'span',{'data-hook':'review-date'}),re.IGNORECASE).group(0)
                    day = re.findall('(?<=vom )[0-9]{2}|[0-9]{1}(?=\.)',finder(review,'span',{'data-hook':'review-date'}))[0]
                    month_en = month_str.lower()
                    for char in monthmap:
                        month_en = month_en.replace(char,monthmap[char])
                    published = str(day) + '. ' + month_en + ' ' + y_published

                    row_komp = [starturl,title,our_price,price,avg_rating,rating,r_title,r_content,
                                verified,helpful,c_comments,y_published,month_str,day,published]

                    for i,s in enumerate(row_komp):
                        if isinstance(row_komp[i],str) == True:
                            for char in chars:
                                row_komp[i] = row_komp[i].replace(char,chars[char])
                        if row_komp[i] == '-1':
                            row_komp[i] = np.nan

                    list_komp.append(row_komp)
                break
            except:
                continue

        
    # Go to next site if its not the last site of reviews. Else end the loop
        check = finder(values,'li',{'class':'a-disabled'})
        #if check == '-1':
         #   found = False
        #else:
        found = True
        try:
            url = values.find('li',class_='a-last').find('a', href=True)['href']
            found = True
        except:
            found = False
    return list_komp
    # create dataframe for the reviews out of the lists
    #r_df = pd.DataFrame(r_list,columns=['rating','r_title','r_content','verified','helpful','c_comments','y_published','month_name','day','Datestring'])
    #r_df['published_date'] = pd.to_datetime(r_df['Datestring'])

    # adding information to the header and save everything as csvs
   # h_df['c_reviews'] = r_df['rating'].count()
    #h_df['first_review_date'] = r_df['published_date'].min()
    #h_df['last_review_date'] = r_df['published_date'].max()
    #print('done1')
    #h_df.to_excel('header_file.xlsx')
    #r_df.to_excel('review_file.xlsx')

    #print('Done')

    
    
def review_liste(suchstring,anzahl_suchseiten):
    """
    Gibt für suchstring und anzahl suchseiten alle Reviews als Dataframe
    
    """
    links = links_holen(suchstring,anzahl_suchseiten) #Liste an Artikellinks generieren 
    cols = ["starturl","title","our_price","price","avg_rating","rating","r_title","r_content","verified","helpful","c_comments","y_published","month_str","day","published"] # Spalten der Rezensionen definieren
    
    #ein DataFrame mit den erfolgreich geholten Reviews und eines mit den übersprungenen Links initiieren
    df_reviews = pd.DataFrame(columns=cols)
    df_skipped = pd.DataFrame(columns=["geskipped"])
    
    anz_skipped = 0
    a = 0 #Zähler für die Links
    
    list_komp = []
    print(f"Anzahl Links: {len(links)}")



    for link in links: #alle Artikellinks durchgehen
        buffer_rez = len(df_reviews)
        a+=1
        try: #versuch dir die Rezensionen zu holen. Sonst schreib in eine Error Tabelle 
            list_komp = review_scraper(link) #Rezensionen in eine Liste schreiben
            
            df_zwischen = pd.DataFrame(list_komp, columns=cols)
            df_zwischen['starturl'] = link
            df_reviews = df_reviews.append(df_zwischen, ignore_index=True) #alle Infos in das DataFrame geben 
            
            #Anzahlen an Rezensionen berechnen
            anzahl_rez = len(df_reviews)
            anzahl_rez_neu = anzahl_rez - buffer_rez
            print(f"Link Nummer {a} - Anzahl Rezensionen: {anzahl_rez} - Anzahl Neu: {anzahl_rez_neu} - Link: {link}")
            
        except:
            df_skipped = df_skipped.append([link], ignore_index=True)
            anz_skipped+=1
            pass

    print(f"{anz_skipped} geskipped")
    
    return df_reviews, df_skipped