#      Copyright 2020. ThingsBoard
#  #
#      Licensed under the Apache License, Version 2.0 (the "License");
#      you may not use this file except in compliance with the License.
#      You may obtain a copy of the License at
#  #
#          http://www.apache.org/licenses/LICENSE-2.0
#  #
#      Unless required by applicable law or agreed to in writing, software
#      distributed under the License is distributed on an "AS IS" BASIS,
#      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#      See the License for the specific language governing permissions and
#      limitations under the License.
#

import logging
# Importing models and REST client class from Community Edition version
from random import randint
from tb_rest_client.rest_client_ce import *
from tb_rest_client.rest import ApiException


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# ThingsBoard REST API URL
url = "http://localhost:8080"

# Default Tenant Administrator credentials
username = "tenant@thingsboard.org"
password = "tenant"

if __name__ == '__main__':

    # Creating the REST client object with context manager to get auto token refresh
    with RestClientCE(base_url=url) as rest_client:
        # Auth with credentials
        rest_client.login(username=username, password=password)

        # Creating an Asset
        asset = Asset(name="Building %i" % randint(0, 10000000), type="building")
        asset = rest_client.save_asset(asset)

        logging.info("Asset was created:\n%r\n", asset)

        # creating a Device
        # device = Device(name="Thermometer %i" % randint(0, 10000000), type="thermometer")
        # device = rest_client.save_device(device)

        logging.info(" Device was created:\n%r\n", device)

        x = EntityId("DEVICE", "77296d00-d341-11ea-8297-fbb449044c6d")

        attr = rest_client.get_attributes_by_scope(x, "SHARED_SCOPE")

        logging.info(attr)

        # Creating relations from device to asset
        # relation = EntityRelation(_from=asset.id, to=device.id, type="Contains")
        # relation = rest_client.save_relation(relation)
        #
        # logging.info(" Relation was created:\n%r\n", relation)

