from flask import Flask
application = Flask(__name__)

@application.route("/")
def hello():
    return """<h1 style='color:blue'>Hello there, Zac! The setup script seems to have run successfully for you! Yay!</h1>
				<br>
				<p>You have a flask webserver running on your EC2 instance. This is where you're going to develop the APIs for your chatbot and do some other fun stuff.</p>
				<a href="https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-16-04">Here's the link to the instructions if you'd like to do yourself in the future.</a>"""

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=41953)
