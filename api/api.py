from flask import Flask
from flask.helpers import make_response
from flask.templating import render_template
from flask_restful import Api, Resource, reqparse
import pandas as pd
from werkzeug.wrappers import response
import sqlConnector
import json
import paho.mqtt.client as mqtt

app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)


class ESP(Resource):
    def get(self):
        data = sqlConnector.getTodayData()
        data = pd.DataFrame(data, columns=["ID", "Date", "Temp"])
        data["Date"] = data["Date"].dt.strftime("%Y-%m-%d %H:%M:%S")
        data = data.to_dict('records')
        return {'data': data}, 200

    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('temperature', type=float,
                            required=True, location='args')
        args = parser.parse_args()
        new_data = pd.DataFrame({
            'temperature': [args['temperature']],
        })
        sqlConnector.postData(float(args['temperature']))
        return {'data': new_data.to_dict('records')}, 201


# Add URL endpoints
api.add_resource(ESP, '/esp')

#Connection success callback
def on_connect(client, userdata, flags, rc):
    print('Connected with result code '+str(rc))
    client.subscribe('esp32/testTemp')

# Message receiving callback
def on_message(client, userdata, msg):
    sqlConnector.postData(float(msg.payload))

@app.route('/')
def home():
    data = sqlConnector.getTodayData()
    data = pd.DataFrame(data, columns=["ID","Date","Temp"])
    data["Date"] = data["Date"].dt.strftime("%Y-%m-%d %H:%M:%S")
    labels = [row for row in data['Date']][::-1]
    values = [row for row in data['Temp']][::-1]
    return render_template("charts.html", labels=labels, values=values)

@app.route("/chartData")
def data():
    data = sqlConnector.getLastData()
    data = pd.DataFrame(data, columns=["ID","Date","Temp"])
    data["Date"] = data["Date"].dt.strftime("%Y-%m-%d %H:%M:%S")
    data = [data["Date"][0], data["Temp"][0]]
    print(data)
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect('broker.emqx.io', 1883, 60)
    client.loop_start()
    app.run(host="0.0.0.0")