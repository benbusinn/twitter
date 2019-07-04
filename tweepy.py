import tweepy
access_token = "1146328410265808896-qjD3HWpxUYjnmgFfd5kwc8mxiILzuD"
access_token_secret = "QKyLnM8AWpxDBjRY6WArvg6K9kUPAQz27KkNeea6ve94s"
consumer_key = "5KJPRiderXjDWSYsnpYVWoKam"
consumer_secret = "YLfxgH8zlQnElmU41uVzjdEYB5wOzdw35NmK3ZYGdVmszqukfX"
import datetime
import pandas as pd
import numpy as np
tweets_count = 0
tweets_list2 = []
bio = []
IST = datetime.timedelta(hours = 5, minutes = 30)
df = pd.DataFrame(columns = ["created_at", "id_str","text"])
class StreamListener(tweepy.StreamListener):
    def on_status(self, status, tweet_mode='extended'):
        global stat
        stat = status
        if (not status.retweeted) and ("RT" not in status.text[:2]):
            text = status.text
            id_str = status.id_str
            created = (status.created_at + IST).strftime("%d-%b-%Y (%H:%M:%S)")
            print(tweets_count)
            try: 
                tweets_list2.append(status.extended_tweet['full_text'])
                df.loc[len(tweets_list2) - 1] = [created, id_str, text]

            except:
                print("not success")
                tweets_list2.append(text)
                df.loc[len(tweets_list2) - 1] = [created, id_str, text]

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False
    
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
keywords = "Budget, survey, india, economy, finance, investment, public, money, infrastructure, education, sports, culture, health, water, sanitation, housing, caste, tribes, labor, security, nutrition, urban, development, village, agriculture, rural, irrigation, flood, expenditure, capital, budgetary, revenue, energy, industry, minerals, transport, communications, science, technology, environment, services, loans, state, government, central, crop, husbandry, soil, conservation, food, storage, warehousing, power, fiscal, interest, debt, police, pension, bank, employment, fisheries, unemployment, forestry, wildlife, plantations, petroleum, ports, houses, road, air, transport, tourism, schemes, grants, plan, dairy, research, institutions, taxes, market, savings, provident, mutual, fund, stock, equity, NSE, BSE, NIFTY, auto, financial, FMCG, IT, media, metal, pharma, private, PSU, realty, smallcap, midcap, largecap, commodities, CPSE, consumption, MNC, PSE, futures, alpha, beta, dividend, opportunities, growth, quality, efficiency, G-Sec, benchmark, bond, banking, T-bills, SBI, LIC, land, labour, famine, disinvestment, remittances, outlay, iron, steel, mining, metallurgical, bridges, NABARD, surplus, deficit, policy, e-commerce, resources, trade, commerce, data, FRBM, GDP, non-development, non-plan, borrowings, non-tax, wages, salaries, B2B, B2C, consumer, business, BE, CSO, discoms, electricity, renewable, GST, tax, MGNREGS, Siksha, IBC, cleanliness, poor, farmer, income, workers, women, youth, MSMEs, traders, defence, digital, entertainment, taxpayers, customs, border, demonetisation, black, subsidies, CGST, IGST, e-way, railways, fertiliser, telecom, tribal, justice, swaraj, gram, rashtriya, cities, schools, colleges, universities, minorities, krishi, yojna, swachh, bharat, fuel, urea, electronics, HIV, foodgrains, kisan, export, import, rehabilitation, migrants, wind, solar, metro, employees, competition, skill, livelihood, highways, innovation, biotechnology, space, cotton, silk, tourist, ganga, rivers"
keywords_list = keywords.split(", ")
stream.filter(track=keywords_list)