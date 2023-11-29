from flask import Flask, jsonify
import webcrawler as web
import schedule
import time
import threading

app = Flask(__name__)
news_data = []

def update_news_data():
    global news_data
    temp = web.GetAllData()
    if(temp == None):
        print("debug : News data updating is failed")
    else: 
        print("debug : News data updated")
        news_data = temp

    #db upload 하는 거

#appnews 제공하는 api
@app.route('/api/news',methods = ['GET'])
def getNews():
    res = {}
    
    if(news_data == None):
        res = {
            "message" : "Failed to retrieve news data",
            "data" :[]
        }
    else: res = {
        "message" :"success",
        "data" : news_data
    }
    
    return res

schedule.every(6).hours.do(update_news_data)

def runSchedule():
    while True:
        schedule.run_pending()
        time.sleep(1)
        
if __name__ == '__main__':
    update_news_data()
    
    schedule_thread = threading.Thread(target=runSchedule)
    schedule_thread.start()
    
    app.run()
    #비동기 처리하는 거 while 돌아야 한다.
