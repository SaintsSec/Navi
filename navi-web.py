from flask import Flask, render_template, request, jsonify, json
import requests

app = Flask(__name__, static_folder="static", template_folder="templates")


@app.route('/')
def home():
    model_name = get_current_model()
    return render_template('index.html', model_name=model_name)


@app.route('/parse', methods=['POST', 'GET'])
def extract():
    text = str(request.form.get('value1'))
    payload = json.dumps({"sender": "Rasa", "message": text})
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.request(
        "POST", url="http://127.0.0.1:5005/webhooks/rest/webhook", headers=headers, data=payload)
    response = response.json()

    resp = [msg['text'] for msg in response if 'text' in msg]

    return jsonify({"result": resp, "text": text})


def get_current_model():
    try:
        response = requests.get("http://127.0.0.1:5005/model")
        if response.status_code == 200:
            return response.json().get("model_file", "Unknown Model").split("/")[-1]
    except Exception as e:
        return "Unknown Model"
    return "Unknown Model"


if __name__ == "__main__":
    app.run(debug=False, host='127.0.0.1', port=5000)
