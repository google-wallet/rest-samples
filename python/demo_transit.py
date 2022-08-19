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
# [START imports]
import os
import re

from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account
from google.auth import jwt, crypt
# [END imports]

# KEY_FILE_PATH - Path to service account key file from Google Cloud Console
#               - Environment variable: GOOGLE_APPLICATION_CREDENTIALS
KEY_FILE_PATH = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS",
                               "/path/to/key.json")

# ISSUER_ID - The issuer ID being updated in this request
#           - Environment variable: WALLET_ISSUER_ID
ISSUER_ID = os.environ.get("WALLET_ISSUER_ID", "issuer-id")

# CLASS_ID - Developer-defined ID for the wallet class
#         - Environment variable: WALLET_CLASS_ID
CLASS_ID = os.environ.get("WALLET_CLASS_ID", "test-transit-class-id")

# USER_ID - Developer-defined ID for the user, such as an email address
#        - Environment variable: WALLET_USER_ID
USER_ID = os.environ.get("WALLET_USER_ID", "test@example.com")

# objectId - ID for the wallet object
#          - Format: `issuerId.userId`
#          - Should only include alphanumeric characters, '.', '_', or '-'
OBJECT_ID = "%s.%s-%s" % (ISSUER_ID, re.sub(r"[^\w.-]", "_", USER_ID), CLASS_ID)
# [END setup]

###############################################################################
# Create authenticated HTTP client, using service account file.
###############################################################################

# [START auth]
credentials = service_account.Credentials.from_service_account_file(
  KEY_FILE_PATH,
  scopes=["https://www.googleapis.com/auth/wallet_object.issuer"])

http_client = AuthorizedSession(credentials)
# [END auth]

###############################################################################
# Create a class via the API (this can also be done in the business console).
###############################################################################

# [START class]
CLASS_URL = "https://walletobjects.googleapis.com/walletobjects/v1/transitClass/"
class_payload = {
  "id": f"{ISSUER_ID}.{CLASS_ID}",
  "issuerName": "test issuer name",
  "reviewStatus": "underReview",
  "transitType": "bus",
  "logo": {
    "kind": "walletobjects#image",
    "sourceUri": {
      "kind": "walletobjects#uri",
      "uri": "https://live.staticflickr.com/65535/48690277162_cd05f03f4d_o.png",
      "description": "Test logo description"
    }
  }
}

class_response = http_client.post(
  CLASS_URL,
  json=class_payload
)
print("class POST response: ", class_response.text)
# [END class]

###############################################################################
# Get or create an object via the API.
###############################################################################

# [START object]
OBJECT_URL = "https://walletobjects.googleapis.com/walletobjects/v1/transitObject/"
object_payload = {
  "id": OBJECT_ID,
  "classId": f"{ISSUER_ID}.{CLASS_ID}",
  "heroImage": {
    "sourceUri": {
      "uri": "https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg",
      "description": "Test heroImage description"
    }
  },
  "textModulesData": [
    {
      "header": "Test text module header",
      "body": "Test text module body"
    }
  ],
  "linksModuleData": {
    "uris": [
      {
        "kind": "walletobjects#uri",
        "uri": "http://maps.google.com/",
        "description": "Test link module uri description"
      },
      {
        "kind": "walletobjects#uri",
        "uri": "tel:6505555555",
        "description": "Test link module tel description"
      }
    ]
  },
  "imageModulesData": [
    {
      "mainImage": {
        "kind": "walletobjects#image",
        "sourceUri": {
          "kind": "walletobjects#uri",
          "uri": "http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg",
          "description": "Test image module description"
        }
      }
    }
  ],
  "barcode": {
    "kind": "walletobjects#barcode",
    "type": "qrCode",
    "value": "Test QR Code"
  },
  "passengerType": "singlePassenger",
  "passengerNames": "Test passenger names",
  "ticketLeg": {
    "originStationCode": "LA",
    "originName": {
      "kind": "walletobjects#localizedString",
      "translatedValues": [
        {
          "kind": "walletobjects#translatedString",
          "language": "en-us",
          "value": "Test translated origin name"
        }
      ],
      "defaultValue": {
        "kind": "walletobjects#translatedString",
        "language": "en-us",
        "value": "Test default origin name"
      }
    },
    "destinationStationCode": "SFO",
    "destinationName": {
      "kind": "walletobjects#localizedString",
      "translatedValues": [
        {
          "kind": "walletobjects#translatedString",
          "language": "en-us",
          "value": "Test translated destination name"
        }
      ],
      "defaultValue": {
        "kind": "walletobjects#translatedString",
        "language": "en-us",
        "value": "Test default destination name"
      }
    },
    "departureDateTime": "2020-04-12T16:20:50.52Z",
    "arrivalDateTime": "2020-04-12T20:20:50.52Z",
    "fareName": {
      "kind": "walletobjects#localizedString",
      "translatedValues": [
        {
          "kind": "walletobjects#translatedString",
          "language": "en-us",
          "value": "Test translated fare name"
        }
      ],
      "defaultValue": {
        "kind": "walletobjects#translatedString",
        "language": "en-us",
        "value": "Test default fare name"
      }
    }
  },
  "locations": [
    {
      "kind": "walletobjects#latLongPoint",
      "latitude": 37.424015499999996,
      "longitude": -122.09259560000001
    }
  ]
}

object_response = http_client.get(OBJECT_URL + OBJECT_ID)
if object_response.status_code == 404:
  # Object does not yet exist
  # Send POST request to create it
  object_response = http_client.post(
    OBJECT_URL,
    json=object_payload
  )

print("object GET or POST response:", object_response.text)
# [END object]

###############################################################################
# Create a JWT for the object, and encode it to create a "Save" URL.
###############################################################################

# [START jwt]
claims = {
  "iss": http_client.credentials.service_account_email,
  "aud": "google",
  "origins": ["www.example.com"],
  "typ": "savetowallet",
  "payload": {
    "transitObjects": [
      {
        "id": OBJECT_ID
      }
    ]
  }
}

signer = crypt.RSASigner.from_service_account_file(KEY_FILE_PATH)
token = jwt.encode(signer, claims).decode("utf-8")
save_url = f"https://pay.google.com/gp/v/save/{token}"

print(save_url)
# [END jwt]

###############################################################################
# Create a new Google Wallet issuer account
###############################################################################

# [START createIssuer]
# New issuer name
ISSUER_NAME = "name"

# New issuer email address
ISSUER_EMAIL = "email-address"

# Issuer API endpoint
ISSUER_URL = "https://walletobjects.googleapis.com/walletobjects/v1/issuer"

# New issuer information
issuer_payload = {
  "name": ISSUER_NAME,
  "contactInfo": {
    "email": ISSUER_EMAIL
  }
}

# Make the POST request
issuer_response = http_client.post(
  url=ISSUER_URL,
  json=issuer_payload
)

print("issuer POST response:", issuer_response.text)
# [END createIssuer]

###############################################################################
# Update permissions for an existing Google Wallet issuer account
###############################################################################

# [START updatePermissions]
# Permissions API endpoint
permissions_url = f"https://walletobjects.googleapis.com/walletobjects/v1/permissions/{ISSUER_ID}"

# New issuer permissions information
permissions_payload = {
  "issuerId": ISSUER_ID,
  "permissions": [
    # Copy as needed for each email address that will need access
    {
      "emailAddress": "email-address",
      "role": "READER | WRITER | OWNER"
    },
  ]
}

permissions_response = http_client.put(
  permissions_url,
  json=permissions_payload
)

print("permissions PUT response:", permissions_response.text)
# [END updatePermissions]
