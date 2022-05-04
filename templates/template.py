#
# Copyright 2022 Google Inc. All rights reserved.
#
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#

# [START setup]
import os, re, datetime

from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account
from google.auth import jwt, crypt

# Path to service account key file obtained from Google CLoud Console.
service_account_file = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "/path/to/key.json")

# Issuer ID obtained from Google Pay Business Console.
issuer_id = os.environ.get("WALLET_ISSUER_ID", "<issuer ID>")

# Developer defined ID for the wallet class.
class_id = os.environ.get("WALLET_CLASS_ID", "test-$object_type-class-id")

# Developer defined ID for the user, eg an email address.
user_id = os.environ.get("WALLET_USER_ID", "test@example.com")

# ID for the wallet object, must be in the form `issuer_id.user_id` where user_id is alphanumeric.
object_id = "%s.%s-%s" % (issuer_id, re.sub(r"[^\w.-]", "_", user_id), class_id)
# [END setup]

###############################################################################
# Create authenticated HTTP client, using service account file.
###############################################################################

# [START auth]
credentials = service_account.Credentials.from_service_account_file(service_account_file, 
  scopes=["https://www.googleapis.com/auth/wallet_object.issuer"])
http_client = AuthorizedSession(credentials)
# [END auth]

###############################################################################
# Create a class via the API (this can also be done in the business console).
###############################################################################

# [START class]
class_url = "https://walletobjects.googleapis.com/walletobjects/v1/$object_typeClass/"
class_payload = $class_payload

class_response = http_client.post(class_url, json=class_payload)
print("class POST response:", class_response.text)
# [END class]

###############################################################################
# Get or create an object via the API.
###############################################################################

# [START object]
object_url = "https://walletobjects.googleapis.com/walletobjects/v1/$object_typeObject/"
object_payload = $object_payload

# Retrieve the object, or create it if it doesn't exist.
object_response = http_client.get(object_url + object_id)
if object_response.status_code == 404:
  object_response = http_client.post(object_url, json=object_payload)
print("object GET or POST response:", object_response.text)
# [END object]

###############################################################################
# Create a JWT for the object, and encode it to create a "Save" URL.
###############################################################################

# [START jwt]
claims = {
  "iss": http_client.credentials.service_account_email, # `client_email` in service account file.
  "aud": "google",
  "origins": ["www.example.com"],
  "typ": "savetowallet",
  "payload": {
    "$object_typeObjects": [{"id": object_id}]
  }
}

signer = crypt.RSASigner.from_service_account_file(service_account_file)
token = jwt.encode(signer, claims).decode("utf-8")
save_url = "https://pay.google.com/gp/v/save/%s" % token
print(save_url)
# [END jwt]
