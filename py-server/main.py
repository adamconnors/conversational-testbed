import flask
from flask_cors import CORS
from vertexai.language_models import ChatModel, InputOutputTextPair


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = flask.Flask(__name__)
chat_model = ChatModel.from_pretrained("chat-bison@002")
chat = chat_model.start_chat()
cors_headers = {'Access-Control-Allow-Origin': '*'}

@app.route('/api', methods = ['POST', 'GET'])
def api():
    q = flask.request.args.get('q') or flask.request.form.get('q')
    print("Got query: ", q)
    if q is None:
        return "No request sent, use ?q=", 200, cors_headers
    
    # Make request to the server
    resp = chat.send_message(q)

    # Response
    rtn = resp.candidates[0].text, 200, cors_headers
    return rtn

if __name__ == "__main__":
    # Used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host="localhost", port=8080, debug=True)