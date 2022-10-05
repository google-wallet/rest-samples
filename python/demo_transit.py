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
import json
import os
import re
from typing import List
import uuid

from google.auth.transport.requests import AuthorizedSession
from google.oauth2.service_account import Credentials
from google.auth import jwt, crypt
# [END imports]


class DemoTransit:
    """Demo class for creating and managing Transit passes in Google Wallet.

    Attributes:
        key_file_path: Path to service account key file from Google Cloud
            Console. Environment variable: GOOGLE_APPLICATION_CREDENTIALS.
        base_url: Base URL for Google Wallet API requests.
    """

    def __init__(self):
        self.key_file_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS',
                                            '/path/to/key.json')
        self.base_url = 'https://walletobjects.googleapis.com/walletobjects/v1'

        # Set up authenticated client
        self.auth()

    # [END setup]

    # [START auth]
    def auth(self):
        """Create authenticated HTTP client using a service account file."""
        self.credentials = Credentials.from_service_account_file(
            self.key_file_path,
            scopes=['https://www.googleapis.com/auth/wallet_object.issuer'])

        self.http_client = AuthorizedSession(self.credentials)

    # [END auth]

    # [START class]
    def create_transit_class(self, issuer_id: str, class_suffix: str) -> str:
        """Create a class via the API.

        This can also be done in the Google Pay and Wallet console.

        Args:
            issuer_id (str): The issuer ID being used for this request.
            class_suffix (str): Developer-defined unique ID for this pass class.

        Returns:
            The pass class ID: f"{issuer_id}.{class_suffix}"
        """
        class_url = f'{self.base_url}/transitClass'

        # See below for more information on required properties
        # https://developers.google.com/wallet/tickets/transit-passes/qr-code/rest/v1/transitclass
        transit_class = {
            'id': f'{issuer_id}.{class_suffix}',
            'issuerName': 'Issuer name',
            'reviewStatus': 'UNDER_REVIEW',
            'logo': {
                'sourceUri': {
                    'uri':
                        'https://live.staticflickr.com/65535/48690277162_cd05f03f4d_o.png',
                },
                'contentDescription': {
                    'defaultValue': {
                        'language': 'en-US',
                        'value': 'Logo description',
                    },
                },
            },
            'transitType': 'BUS',
        }

        response = self.http_client.post(
            url=class_url,
            json=transit_class,
        )

        print('Class insert response')
        print(response.text)

        return response.json().get('id')

    # [END class]

    # [START object]
    def create_transit_object(self, issuer_id: str, class_suffix: str,
                              user_id: str) -> str:
        """Create an object via the API.

        Args:
            issuer_id (str): The issuer ID being used for this request.
            class_suffix (str): Developer-defined unique ID for this pass class.
            user_id (str): Developer-defined user ID for this pass object.

        Returns:
            The pass object ID: f"{issuer_id}.{user_id}"
        """
        object_url = f'{self.base_url}/transitObject'

        # Generate the object ID
        # Should only include alphanumeric characters, '.', '_', or '-'
        new_user_id = re.sub(r'[^\w.-]', '_', user_id)
        object_id = f'{issuer_id}.{new_user_id}'

        # See below for more information on required properties
        # https://developers.google.com/wallet/tickets/transit-passes/qr-code/rest/v1/transitobject
        transit_object = {
            'id': f'{object_id}',
            'classId': f'{issuer_id}.{class_suffix}',
            'state': 'ACTIVE',
            'heroImage': {
                'sourceUri': {
                    'uri':
                        'https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg',
                },
                'contentDescription': {
                    'defaultValue': {
                        'language': 'en-US',
                        'value': 'Hero image description',
                    },
                },
            },
            'textModulesData': [{
                'header': 'Text module header',
                'body': 'Text module body',
                'id': 'TEXT_MODULE_ID',
            },],
            'linksModuleData': {
                'uris': [
                    {
                        'uri': 'http://maps.google.com/',
                        'description': 'Link module URI description',
                        'id': 'LINK_MODULE_URI_ID',
                    },
                    {
                        'uri': 'tel:6505555555',
                        'description': 'Link module tel description',
                        'id': 'LINK_MODULE_TEL_ID',
                    },
                ],
            },
            'imageModulesData': [{
                'mainImage': {
                    'sourceUri': {
                        'uri':
                            'http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg',
                    },
                    'contentDescription': {
                        'defaultValue': {
                            'language': 'en-US',
                            'value': 'Image module description',
                        },
                    },
                },
                'id': 'IMAGE_MODULE_ID',
            },],
            'barcode': {
                'type': 'QR_CODE',
                'value': 'QR code',
            },
            'locations': [{
                'latitude': 37.424015499999996,
                'longitude': -122.09259560000001,
            },],
            'passengerType': 'SINGLE_PASSENGER',
            'passengerNames': 'Passenger names',
            'ticketLeg': {
                'originStationCode': 'LA',
                'originName': {
                    'defaultValue': {
                        'language': 'en-US',
                        'value': 'Origin name',
                    },
                },
                'destinationStationCode': 'SFO',
                'destinationName': {
                    'defaultValue': {
                        'language': 'en-US',
                        'value': 'Destination name',
                    },
                },
                'departureDateTime': '2020-04-12T16:20:50.52Z',
                'arrivalDateTime': '2020-04-12T20:20:50.52Z',
                'fareName': {
                    'defaultValue': {
                        'language': 'en-US',
                        'value': 'Fare name',
                    },
                },
            },
        }

        response = self.http_client.get(f'{object_url}{object_id}')
        if response.status_code == 404:
            # Object does not yet exist
            # Send POST request to create it
            response = self.http_client.post(
                url=object_url,
                json=transit_object,
            )

            print('Object insert response')
            print(response.text)
        else:
            print('Object get response')
            print(response.text)

        return response.json().get('id')

    # [END object]

    # [START jwt]
    def create_jwt_save_url(self, issuer_id: str, class_suffix: str,
                            user_id: str) -> str:
        """Generate a signed JWT that creates a new pass class and object.

        When the user opens the "Add to Google Wallet" URL and saves the pass to
        their wallet, the pass class and object defined in the JWT are
        created. This allows you to create multiple pass classes and objects in
        one API call when the user saves the pass to their wallet.

        Args:
            issuer_id (str): The issuer ID being used for this request.
            class_suffix (str): Developer-defined unique ID for this pass class.
            user_id (str): Developer-defined user ID for this pass object.

        Returns:
            An "Add to Google Wallet" link
        """

        # Generate the object ID
        # Should only include alphanumeric characters, '.', '_', or '-'
        new_user_id = re.sub(r'[^\w.-]', '_', user_id)
        object_id = f'{issuer_id}.{new_user_id}'

        # See below for more information on required properties
        # https://developers.google.com/wallet/tickets/transit-passes/qr-code/rest/v1/transitclass
        transit_class = {
            'id': f'{issuer_id}.{class_suffix}',
            'issuerName': 'Issuer name',
            'reviewStatus': 'UNDER_REVIEW',
            'logo': {
                'sourceUri': {
                    'uri':
                        'https://live.staticflickr.com/65535/48690277162_cd05f03f4d_o.png',
                },
                'contentDescription': {
                    'defaultValue': {
                        'language': 'en-US',
                        'value': 'Logo description',
                    },
                },
            },
            'transitType': 'BUS',
        }

        # See below for more information on required properties
        # https://developers.google.com/wallet/tickets/transit-passes/qr-code/rest/v1/transitobject
        transit_object = {
            'id': f'{object_id}',
            'classId': f'{issuer_id}.{class_suffix}',
            'state': 'ACTIVE',
            'heroImage': {
                'sourceUri': {
                    'uri':
                        'https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg',
                },
                'contentDescription': {
                    'defaultValue': {
                        'language': 'en-US',
                        'value': 'Hero image description',
                    },
                },
            },
            'textModulesData': [{
                'header': 'Text module header',
                'body': 'Text module body',
                'id': 'TEXT_MODULE_ID',
            },],
            'linksModuleData': {
                'uris': [
                    {
                        'uri': 'http://maps.google.com/',
                        'description': 'Link module URI description',
                        'id': 'LINK_MODULE_URI_ID',
                    },
                    {
                        'uri': 'tel:6505555555',
                        'description': 'Link module tel description',
                        'id': 'LINK_MODULE_TEL_ID',
                    },
                ],
            },
            'imageModulesData': [{
                'mainImage': {
                    'sourceUri': {
                        'uri':
                            'http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg',
                    },
                    'contentDescription': {
                        'defaultValue': {
                            'language': 'en-US',
                            'value': 'Image module description',
                        },
                    },
                },
                'id': 'IMAGE_MODULE_ID',
            },],
            'barcode': {
                'type': 'QR_CODE',
                'value': 'QR code',
            },
            'locations': [{
                'latitude': 37.424015499999996,
                'longitude': -122.09259560000001,
            },],
            'passengerType': 'SINGLE_PASSENGER',
            'passengerNames': 'Passenger names',
            'ticketLeg': {
                'originStationCode': 'LA',
                'originName': {
                    'defaultValue': {
                        'language': 'en-US',
                        'value': 'Origin name',
                    },
                },
                'destinationStationCode': 'SFO',
                'destinationName': {
                    'defaultValue': {
                        'language': 'en-US',
                        'value': 'Destination name',
                    },
                },
                'departureDateTime': '2020-04-12T16:20:50.52Z',
                'arrivalDateTime': '2020-04-12T20:20:50.52Z',
                'fareName': {
                    'defaultValue': {
                        'language': 'en-US',
                        'value': 'Fare name',
                    },
                },
            },
        }

        # Create the JWT claims
        claims = {
            'iss': self.credentials.service_account_email,
            'aud': 'google',
            'origins': ['www.example.com'],
            'typ': 'savetowallet',
            'payload': {
                # The listed classes and objects will be created
                'transitClasses': [transit_class,],
                'transitObjects': [transit_object,],
            },
        }

        # The service account credentials are used to sign the JWT
        signer = crypt.RSASigner.from_service_account_file(self.key_file_path)
        token = jwt.encode(signer, claims).decode('utf-8')

        print('Add to Google Wallet link')
        print(f'https://pay.google.com/gp/v/save/{token}')

        return f'https://pay.google.com/gp/v/save/{token}'

    # [END jwt]

    # [START createIssuer]
    def create_issuer_account(self, issuer_name: str, issuer_email: str):
        """Create a new Google Wallet issuer account.

        Args:
            issuer_name (str): The issuer's name.
            issuer_email (str): The issuer's email address.
        """
        # Issuer API endpoint
        issuer_url = f'{self.base_url}/issuer'

        # New issuer information
        issuer = {
            'name': issuer_name,
            'contactInfo': {
                'email': issuer_email,
            },
        }

        # Make the POST request
        response = self.http_client.post(
            url=issuer_url,
            json=issuer,
        )

        print('Issuer insert response')
        print(response.text)

    # [END createIssuer]

    # [START updatePermissions]
    def update_issuer_account_permissions(self, issuer_id: str,
                                          permissions: List):
        """Update permissions for an existing Google Wallet issuer account.

        **Warning:** This operation overwrites all existing
        permissions!

        Example permissions list argument below. Copy the dict entry as
        needed for each email address that will need access. Supported
        values for role are: 'READER', 'WRITER', and 'OWNER'

        permissions = [
            {
                'emailAddress': 'email-address',
                'role': 'OWNER',
            },
        ]

        Args:
            issuer_id (str): The issuer ID being used for this request.
            permissions (List): The list of email addresses and roles to assign.
        """
        # Permissions API endpoint
        permissions_url = f'{self.base_url}/permissions/{issuer_id}'

        response = self.http_client.put(
            url=permissions_url,
            json={
                'issuerId': issuer_id,
                'permissions': permissions,
            },
        )

        print('Permissions update response')
        print(response.text)

    # [END updatePermissions]

    # [START batch]
    def batch_create_transit_objects(self, issuer_id: str, class_suffix: str):
        """Batch create Google Wallet objects from an existing class.

        The request body will be a multiline string. See below for information.

        https://cloud.google.com/compute/docs/api/how-tos/batch#example

        Args:
            issuer_id (str): The issuer ID being used for this request.
            class_suffix (str): Developer-defined unique ID for this pass class.
        """
        data = ''

        # Example: Generate three new pass objects
        for _ in range(3):
            # Generate a random user ID
            user_id = str(uuid.uuid4()).replace('[^\\w.-]', '_')

            # Generate an object ID with the user ID
            # Should only include alphanumeric characters, '.', '_', or '-'
            object_id = f'{issuer_id}.{user_id}'

            # See below for more information on required properties
            # https://developers.google.com/wallet/tickets/transit-passes/qr-code/rest/v1/transitobject
            batch_transit_object = {
                'id': f'{object_id}',
                'classId': f'{issuer_id}.{class_suffix}',
                'state': 'ACTIVE',
                'heroImage': {
                    'sourceUri': {
                        'uri':
                            'https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg',
                    },
                    'contentDescription': {
                        'defaultValue': {
                            'language': 'en-US',
                            'value': 'Hero image description',
                        },
                    },
                },
                'textModulesData': [{
                    'header': 'Text module header',
                    'body': 'Text module body',
                    'id': 'TEXT_MODULE_ID',
                },],
                'linksModuleData': {
                    'uris': [
                        {
                            'uri': 'http://maps.google.com/',
                            'description': 'Link module URI description',
                            'id': 'LINK_MODULE_URI_ID',
                        },
                        {
                            'uri': 'tel:6505555555',
                            'description': 'Link module tel description',
                            'id': 'LINK_MODULE_TEL_ID',
                        },
                    ],
                },
                'imageModulesData': [{
                    'mainImage': {
                        'sourceUri': {
                            'uri':
                                'http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg',
                        },
                        'contentDescription': {
                            'defaultValue': {
                                'language': 'en-US',
                                'value': 'Image module description',
                            },
                        },
                    },
                    'id': 'IMAGE_MODULE_ID',
                },],
                'barcode': {
                    'type': 'QR_CODE',
                    'value': 'QR code',
                },
                'locations': [{
                    'latitude': 37.424015499999996,
                    'longitude': -122.09259560000001,
                },],
                'passengerType': 'SINGLE_PASSENGER',
                'passengerNames': 'Passenger names',
                'ticketLeg': {
                    'originStationCode': 'LA',
                    'originName': {
                        'defaultValue': {
                            'language': 'en-US',
                            'value': 'Origin name',
                        },
                    },
                    'destinationStationCode': 'SFO',
                    'destinationName': {
                        'defaultValue': {
                            'language': 'en-US',
                            'value': 'Destination name',
                        },
                    },
                    'departureDateTime': '2020-04-12T16:20:50.52Z',
                    'arrivalDateTime': '2020-04-12T20:20:50.52Z',
                    'fareName': {
                        'defaultValue': {
                            'language': 'en-US',
                            'value': 'Fare name',
                        },
                    },
                },
            }

            data += '--batch_createobjectbatch\n'
            data += 'Content-Type: application/json\n\n'
            data += 'POST /walletobjects/v1/transitObject/\n\n'

            data += json.dumps(batch_transit_object) + '\n\n'

        data += '--batch_createobjectbatch--'

        # Invoke the batch API calls
        response = self.http_client.post(
            url='https://walletobjects.googleapis.com/batch',
            data=data,
            headers={
                # `boundary` is the delimiter between API calls in the batch request
                'Content-Type':
                    'multipart/mixed; boundary=batch_createobjectbatch'
            })

        print('Batch insert response')
        print(response.content.decode('UTF-8'))

    # [END batch]
