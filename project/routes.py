from quart import Blueprint, request, abort, jsonify, current_app
from .database.models import Device
import asyncio
from .thingsAPI import ThingsBoardAPI
from .parsing_data import group_by_idx, rssi_to_meter, post_data, seperate_data
import datetime
thingUSER = 'tenant@thingsboard.org'
thingPASS = 'tenant'
thingURL = 'http://192.168.0.2:8080'

thingsAPI = ThingsBoardAPI(thingUSER, thingPASS, thingURL)

main = Blueprint('main', __name__)

data = []

@main.route('/search', methods=['POST'])
async def search_db():
    msg = {
        'this.device':None,
        'this.callnumber':None,
        'contact.with':None
    }
    data = await request.get_json()
    if not data:
        abort(404)
    if 'call_number' in data:
        data = await Device.search_by_call_number(call_number=data['call_number'])
        msg['this.callnumber'] = data['call_number']
        msg['this.device'] = data['unique_id']
        msg['contact.with'] = data['contact_devices']
        return jsonify(msg)
    elif 'unique_id' in data:
        data = await Device.search_by_unique_id(unique_id=data['unique_id'])
        msg['this.callnumber'] = data['call_number']
        msg['this.device'] = data['unique_id']
        msg['contact.with'] = data['contact_devices']
        return jsonify(msg)
    else:
        abort(404)
        
@main.route('/register', methods=['POST'])
async def register_device():
    if not request.json:
        abort(404)
    if 'call_number' not in request.json and 'unique_id' not in request.json:
        abort(404)
    call_number = request.json['call_number']
    unique_id = request.json['unique_id']
    if Device.register(call_number, unique_id):
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error'})

@main.route('/update', methods=['POST'])
async def update_contact():
    if not request.json:
        abort(404)
    if 'contact_devices' not in request.json and 'unique_id' not in request.json:
        abort(404)
    else:
        contact_devices = request.json['contact_devices']
        unique_id = request.json['unique_id']
        Device.update_contact_device(unique_id, contact_devices)
        return jsonify({'Success'})
    
@main.route('/postdevice', methods=['POST'])
async def post_device():
    global data
    json_data = await request.get_json()
    user_agent = await request.headers.get('User-Agent')
    if not json_data:
        abort(404)
    if 'devices' in json_data:
        list_data = await seperate_data(json_data['devices'])
        list_data = await group_by_idx(list_data, 0, False)
        deviceName = json_data['deviceName']
        await post_data(list_data, ThingsBoardAPI, deviceName)
        data = datetime.datetime.now()
    else:
        return jsonify({'ok':"ok"}) 
    return jsonify({'ok':"ok"}) 


@main.route('/getdevice', methods=['GET'])
async def get_device():
    global data
    return jsonify({'last_post': data})
