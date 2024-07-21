import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import datetime
import pyjokes


recognizer = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
newsapi = "api_key "
weatherapi = "api_key"

def greetMe():
    hour  = int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        speak("Good Morning")
    elif hour >12 and hour<=18:
        speak("Good Afternoon")

    else:
        speak("Good Evening")

    speak("Please tell me, How can I help you ?")


def speak(text):
    engine.say(text)
    engine.runAndWait()    
  

def processCommand(c):
    c = c.lower()
    sites = [["youtube","https://youtube.com" ],["facebook","https://facebook.com" ],["google","https://google.com" ],["linkedin","https://linkedin.com" ]]

    for site in sites:
        if f"Open {site[0]}".lower() in c:
            speak(f"Opening {site[0]}")
            webbrowser.open(site[1])
            print(f"Opening:{site[0]} ")
                   
        
    if c.startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
        print(f"Playing:{song} ")

    elif "news" in c:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}") 
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles',[])
            for article in articles:
                print(article['title'])
                speak(article['title'])
                                   
    elif "temperature in" in c:
        city = c.lower().split("temperature in")[1]
        r = requests.get(f"https://api.weatherapi.com/v1/current.json?key={weatherapi}&q={city}")
        if r.status_code == 200:
            data = r.json()
            temperature = data['current']['temp_c']
            weather_info = f"The current temperature in {city} is {temperature} degrees Celsius."
            print(weather_info)
            speak(weather_info)   

    elif "today's date" in c:
        today = datetime.datetime.now().strftime("%d/%m/%Y")
        print(f"Today's date is {today}") 
        speak(f"Today's date is {today}")

    elif "time" in c:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"Time is {strTime}")      
        speak(f" The time is {strTime}")

    elif "search for" in c:
        query = c.lower().split("search for", 1)[1].strip()
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)
        speak(f"Searching for {query} online.")
        print(f"Searching for: {query}")

    elif "tell me a joke" in c:
        joke = pyjokes.get_joke()
        print(f"Joke: {joke}")  
        speak(joke)
             

    elif "stop" in c:
        speak("Going to sleep")
        exit()    
                     

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    greetMe()
    while True:
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:            
                print("Listening...")
                audio = r.listen(source)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):           
                with sr.Microphone() as source: 
                    speak("Hmmm")           
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processCommand(command)

        except Exception as e:
            print("Error; {0}".format(e))



