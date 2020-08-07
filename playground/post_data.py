import requests
import json
msg = {
            'unique_id':'asdsad',
            'contact_time':'sad',
            'average_range': 'asd'
}

request_body = json.dumps(msg)
req = requests.post(url="http://192.168.0.5:8080/api/v1/6td1h840wsS6YhISq8u2/telemetry", json=msg)
print(req.status_code)