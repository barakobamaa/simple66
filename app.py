from flask import Flask

app = Flask(__name__)

@app.route('/')
def Test():
   return "This is working"
if __name__=='__main__':
   app.run()