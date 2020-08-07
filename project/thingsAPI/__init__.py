from tb_rest_client.rest_client_ce import *
from tb_rest_client.rest import ApiException
import logging
import requests
import json

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class ThingsBoardAPI(object):
    
    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url      = url
        self.RestClient = RestClientCE(self.url)    
            
    def loggedIn(self):
        self.RestClient.login(self.username, self.password)
    
    def loggedOut(self):
        self.RestClient.logout()
    
    def deviceControl(self, deviceId, command):
        control = self.RestClient.handle_two_way_device_rpc_request(deviceId, command)
        
    def createDevice(self, deviceName, deviceType):
        device = Device(name=deviceName, type=deviceType)
        device = self.RestClient.save_device(device)
        return device.id.id
    
    def deleteDevice(self, deviceId):
        return self.RestClient.delete_device(deviceId)
    
    def getDeviceToken(self, id):
        token = self.RestClient.get_device_credentials_by_device_id(id)
        return token.credentials_id
    
    def assignToCustomer(self, customerId, deviceId, dashboardId):
        assignDashboard = self.RestClient.assign_dashboard_to_customer(customerId, dashboardId)
        assign = self.RestClient.assign_device_to_customer(customerId, deviceId)
        
    def createCustomer(self, userEmail, userPassword):
        customer = Customer(title=userEmail)
        customer = self.RestClient.save_customer(customer)
        user = User(
                    authority="CUSTOMER_USER",
                    customer_id=customer.id,
                    email=userEmail)
        user = self.RestClient.save_user(user, send_activation_mail=False)
        self.RestClient.activate_user(user.id, userPassword)
        return customer.id.id, user.id.id
    
    def getAttribute(self, token):
        r = requests.get(f'{self.url}/api/v1/{token}/attributes')
        data = r.json()
        return data
    @staticmethod
    def send_telemetry(request_body):
        req = requests.post(url="http://192.168.0.5:8080/api/v1/6td1h840wsS6YhISq8u2/telemetry", json=request_body)
        return req.status_code