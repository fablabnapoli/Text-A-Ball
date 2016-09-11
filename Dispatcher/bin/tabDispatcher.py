import web
import tweepy
from tweetStreamer import twitterStreamClient

# dati di accesso Twitter

# Elenco delle pagine gestire dalla web application e relative
# classi associate.
urls = (
   '/', 'index',
   '/shutdown', 'shutdown', 
)

# Attivazione della web application
app = web.application(urls, globals())

# Attivazione del motore dei template
render = web.template.render('templates/')

# 
class index:
   def GET(self):
      greeting = "Hello World"
      return render.index(greeting = greeting)

class shutdown: 
   def GET(self): 
      import sys 
      sys.exit(0)


if __name__ == "__main__":

   try:
      # Istanza tweetStreamerClient
      tsc = twitterStreamClient()

      # Avvio della ControlInterface web 
      # app.run()
   except (KeyboardInterrupt):
      print("Stopping...")
      sys.exit()