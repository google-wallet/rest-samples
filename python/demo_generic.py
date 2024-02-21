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
import uuid

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials
from google.auth import jwt, crypt
# [END imports]


class DemoGeneric:
    """Demo class for creating and managing Generic passes in Google Wallet.

    Attributes:
        key_file_path: Path to service account key file from Google Cloud
            Console. Environment variable: GOOGLE_APPLICATION_CREDENTIALS.
        base_url: Base URL for Google Wallet API requests.
    """

    def __init__(self):
        self.key_file_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS',
                                            '/path/to/key.json')
        # Set up authenticated client
        self.auth()

    # [END setup]

    # [START auth]
    def auth(self):
        """Create authenticated HTTP client using a service account file."""
        self.credentials = Credentials.from_service_account_file(
            self.key_file_path,
            scopes=['https://www.googleapis.com/auth/wallet_object.issuer'])

        self.client = build('walletobjects', 'v1', credentials=self.credentials)

    # [END auth]

    # [START createClass]
    def create_class(self, issuer_id: str, class_suffix: str) -> str:
        """Create a class.

        Args:
            issuer_id (str): The issuer ID being used for this request.
            class_suffix (str): Developer-defined unique ID for this pass class.

        Returns:
            The pass class ID: f"{issuer_id}.{class_suffix}"
        """

        # Check if the class exists
        try:
            self.client.genericclass().get(resourceId=f'{issuer_id}.{class_suffix}').execute()
        except HttpError as e:
            if e.status_code != 404:
                # Something else went wrong...
                print(e.error_details)
                return f'{issuer_id}.{class_suffix}'
        else:
            print(f'Class {issuer_id}.{class_suffix} already exists!')
            return f'{issuer_id}.{class_suffix}'

        # See link below for more information on required properties
        # https://developers.google.com/wallet/generic/rest/v1/genericclass
        new_class = {'id': f'{issuer_id}.{class_suffix}'}

        response = self.client.genericclass().insert(body=new_class).execute()

        print('Class insert response')
        print(response)

        return f'{issuer_id}.{class_suffix}'

    # [END createClass]

    # [START updateClass]
    def update_class(self, issuer_id: str, class_suffix: str) -> str:
        """Update a class.

        **Warning:** This replaces all existing class attributes!

        Args:
            issuer_id (str): The issuer ID being used for this request.
            class_suffix (str): Developer-defined unique ID for this pass class.

        Returns:
            The pass class ID: f"{issuer_id}.{class_suffix}"
        """

        # Check if the class exists
        try:
            response = self.client.genericclass().get(resourceId=f'{issuer_id}.{class_suffix}').execute()
        except HttpError as e:
            if e.status_code == 404:
                print(f'Class {issuer_id}.{class_suffix} not found!')
                return f'{issuer_id}.{class_suffix}'
            else:
                # Something else went wrong...
                print(e.error_details)
                return f'{issuer_id}.{class_suffix}'

        # Class exists
        updated_class = response

        # Update the class by adding a link
        new_link = {
            'uri': 'https://developers.google.com/wallet',
            'description': 'Homepage description'
        }
        if not updated_class.get('linksModuleData'):
            updated_class['linksModuleData'] = {'uris': []}
        updated_class['linksModuleData']['uris'].append(new_link)

        # Note: reviewStatus must be 'UNDER_REVIEW' or 'DRAFT' for updates
        updated_class['reviewStatus'] = 'UNDER_REVIEW'

        response = self.client.genericclass().update(
            resourceId=f'{issuer_id}.{class_suffix}',
            body=updated_class).execute()

        print('Class update response')
        print(response)

        return f'{issuer_id}.{class_suffix}'

    # [END updateClass]

    # [START patchClass]
    def patch_class(self, issuer_id: str, class_suffix: str) -> str:
        """Patch a class.

        The PATCH method supports patch semantics.

        Args:
            issuer_id (str): The issuer ID being used for this request.
            class_suffix (str): Developer-defined unique ID for this pass class.

        Returns:
            The pass class ID: f"{issuer_id}.{class_suffix}"
        """

        # Check if the class exists
        try:
            response = self.client.genericclass().get(resourceId=f'{issuer_id}.{class_suffix}').execute()
        except HttpError as e:
            if e.status_code == 404:
                print(f'Class {issuer_id}.{class_suffix} not found!')
                return f'{issuer_id}.{class_suffix}'
            else:
                # Something else went wrong...
                print(e.error_details)
                return f'{issuer_id}.{class_suffix}'

        # Class exists
        existing_class = response

        # Patch the class by adding a link
        patch_body = {}
        new_link = {
            'uri': 'https://developers.google.com/wallet',
            'description': 'Homepage description'
        }

        if existing_class.get('linksModuleData'):
            patch_body['linksModuleData'] = existing_class.get(
                'linksModuleData')
        else:
            patch_body['linksModuleData'] = {'uris': []}
        patch_body['linksModuleData']['uris'].append(new_link)

        # Note: reviewStatus must be 'UNDER_REVIEW' or 'DRAFT' for patches
        patch_body['reviewStatus'] = 'UNDER_REVIEW'

        response = self.client.genericclass().patch(
            resourceId=f'{issuer_id}.{class_suffix}',
            body=patch_body).execute()

        print('Class patch response')
        print(response)

        return f'{issuer_id}.{class_suffix}'

    # [END patchClass]

    # [START createObject]
    def create_object(self, issuer_id: str, class_suffix: str,
                      object_suffix: str) -> str:
        """Create an object.

        Args:
            issuer_id (str): The issuer ID being used for this request.
            class_suffix (str): Developer-defined unique ID for the pass class.
            object_suffix (str): Developer-defined unique ID for the pass object.

        Returns:
            The pass object ID: f"{issuer_id}.{object_suffix}"
        """

        # Check if the object exists
        try:
            self.client.genericobject().get(resourceId=f'{issuer_id}.{object_suffix}').execute()
        except HttpError as e:
            if e.status_code != 404:
                # Something else went wrong...
                print(e.error_details)
                return f'{issuer_id}.{object_suffix}'
        else:
            print(f'Object {issuer_id}.{object_suffix} already exists!')
            return f'{issuer_id}.{object_suffix}'

        # See link below for more information on required properties
        # https://developers.google.com/wallet/generic/rest/v1/genericobject
        new_object = {
            'id': f'{issuer_id}.{object_suffix}',
            'classId': f'{issuer_id}.{class_suffix}',
            'state': 'ACTIVE',
            'heroImage': {
                'sourceUri': {
                    'uri':
                        'https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg'
                },
                'contentDescription': {
                    'defaultValue': {
                        'language': 'en-US',
                        'value': 'Hero image description'
                    }
                }
            },
            'textModulesData': [{
                'header': 'Text module header',
                'body': 'Text module body',
                'id': 'TEXT_MODULE_ID'
            }],
            'linksModuleData': {
                'uris': [{
                    'uri': 'http://maps.google.com/',
                    'description': 'Link module URI description',
                    'id': 'LINK_MODULE_URI_ID'
                }, {
                    'uri': 'tel:6505555555',
                    'description': 'Link module tel description',
                    'id': 'LINK_MODULE_TEL_ID'
                }]
            },
            'imageModulesData': [{
                'mainImage': {
                    'sourceUri': {
                        'uri':
                            'http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg'
                    },
                    'contentDescription': {
                        'defaultValue': {
                            'language': 'en-US',
                            'value': 'Image module description'
                        }
                    }
                },
                'id': 'IMAGE_MODULE_ID'
            }],
            'barcode': {
                'type': 'QR_CODE',
                'value': 'QR code'
            },
            'cardTitle': {
                'defaultValue': {
                    'language': 'en-US',
                    'value': 'Generic card title'
                }
            },
            'header': {
                'defaultValue': {
                    'language': 'en-US',
                    'value': 'Generic header'
                }
            },
            'hexBackgroundColor': '#4285f4',
            'logo': {
                'sourceUri': {
                    'uri':
                        'https://storage.googleapis.com/wallet-lab-tools-codelab-artifacts-public/pass_google_logo.jpg'
                },
                'contentDescription': {
                    'defaultValue': {
                        'language': 'en-US',
                        'value': 'Generic card logo'
                    }
                }
            }
        }

        # Create the object
        response = self.client.genericobject().insert(body=new_object).execute()

        print('Object insert response')
        print(response)

        return f'{issuer_id}.{object_suffix}'

    # [END createObject]

    # [START updateObject]
    def update_object(self, issuer_id: str, object_suffix: str) -> str:
        """Update an object.

        **Warning:** This replaces all existing object attributes!

        Args:
            issuer_id (str): The issuer ID being used for this request.
            object_suffix (str): Developer-defined unique ID for the pass object.

        Returns:
            The pass object ID: f"{issuer_id}.{object_suffix}"
        """

        # Check if the object exists
        try:
            response = self.client.genericobject().get(resourceId=f'{issuer_id}.{object_suffix}').execute()
        except HttpError as e:
            if e.status_code == 404:
                print(f'Object {issuer_id}.{object_suffix} not found!')
                return f'{issuer_id}.{object_suffix}'
            else:
                # Something else went wrong...
                print(e.error_details)
                return f'{issuer_id}.{object_suffix}'

        # Object exists
        updated_object = response

        # Update the object by adding a link
        new_link = {
            'uri': 'https://developers.google.com/wallet',
            'description': 'New link description'
        }
        if not updated_object.get('linksModuleData'):
            updated_object['linksModuleData'] = {'uris': []}
        updated_object['linksModuleData']['uris'].append(new_link)

        response = self.client.genericobject().update(
            resourceId=f'{issuer_id}.{object_suffix}',
            body=updated_object).execute()

        print('Object update response')
        print(response)

        return f'{issuer_id}.{object_suffix}'

    # [END updateObject]

    # [START patchObject]
    def patch_object(self, issuer_id: str, object_suffix: str) -> str:
        """Patch an object.

        Args:
            issuer_id (str): The issuer ID being used for this request.
            object_suffix (str): Developer-defined unique ID for the pass object.

        Returns:
            The pass object ID: f"{issuer_id}.{object_suffix}"
        """

        # Check if the object exists
        try:
            response = self.client.genericobject().get(resourceId=f'{issuer_id}.{object_suffix}').execute()
        except HttpError as e:
            if e.status_code == 404:
                print(f'Object {issuer_id}.{object_suffix} not found!')
                return f'{issuer_id}.{object_suffix}'
            else:
                # Something else went wrong...
                print(e.error_details)
                return f'{issuer_id}.{object_suffix}'

        # Object exists
        existing_object = response

        # Patch the object by adding a link
        patch_body = {}
        new_link = {
            'uri': 'https://developers.google.com/wallet',
            'description': 'New link description'
        }

        if existing_object.get('linksModuleData'):
            patch_body['linksModuleData'] = existing_object['linksModuleData']
        else:
            patch_body['linksModuleData'] = {'uris': []}
        patch_body['linksModuleData']['uris'].append(new_link)

        response = self.client.genericobject().patch(
            resourceId=f'{issuer_id}.{object_suffix}',
            body=patch_body).execute()

        print('Object patch response')
        print(response)

        return f'{issuer_id}.{object_suffix}'

    # [END patchObject]

    # [START expireObject]
    def expire_object(self, issuer_id: str, object_suffix: str) -> str:
        """Expire an object.

        Sets the object's state to Expired. If the valid time interval is
        already set, the pass will expire automatically up to 24 hours after.

        Args:
            issuer_id (str): The issuer ID being used for this request.
            object_suffix (str): Developer-defined unique ID for the pass object.

        Returns:
            The pass object ID: f"{issuer_id}.{object_suffix}"
        """

        # Check if the object exists
        try:
            response = self.client.genericobject().get(resourceId=f'{issuer_id}.{object_suffix}').execute()
        except HttpError as e:
            if e.status_code == 404:
                print(f'Object {issuer_id}.{object_suffix} not found!')
                return f'{issuer_id}.{object_suffix}'
            else:
                # Something else went wrong...
                print(e.error_details)
                return f'{issuer_id}.{object_suffix}'

        # Patch the object, setting the pass as expired
        patch_body = {'state': 'EXPIRED'}

        response = self.client.genericobject().patch(
            resourceId=f'{issuer_id}.{object_suffix}',
            body=patch_body).execute()

        print('Object expiration response')
        print(response)

        return f'{issuer_id}.{object_suffix}'

    # [END expireObject]

    # [START jwtNew]
    def create_jwt_new_objects(self, issuer_id: str, class_suffix: str,
                               object_suffix: str) -> str:
        """Generate a signed JWT that creates a new pass class and object.

        When the user opens the "Add to Google Wallet" URL and saves the pass to
        their wallet, the pass class and object defined in the JWT are
        created. This allows you to create multiple pass classes and objects in
        one API call when the user saves the pass to their wallet.

        Args:
            issuer_id (str): The issuer ID being used for this request.
            class_suffix (str): Developer-defined unique ID for the pass class.
            object_suffix (str): Developer-defined unique ID for the pass object.

        Returns:
            An "Add to Google Wallet" link.
        """

        # See link below for more information on required properties
        # https://developers.google.com/wallet/generic/rest/v1/genericclass
        new_class = {'id': f'{issuer_id}.{class_suffix}'}

        # See link below for more information on required properties
        # https://developers.google.com/wallet/generic/rest/v1/genericobject
        new_object = {
            'id': f'{issuer_id}.{object_suffix}',
            'classId': f'{issuer_id}.{class_suffix}',
            'state': 'ACTIVE',
            'heroImage': {
                'sourceUri': {
                    'uri':
                        'https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg'
                },
                'contentDescription': {
                    'defaultValue': {
                        'language': 'en-US',
                        'value': 'Hero image description'
                    }
                }
            },
            'textModulesData': [{
                'header': 'Text module header',
                'body': 'Text module body',
                'id': 'TEXT_MODULE_ID'
            }],
            'linksModuleData': {
                'uris': [{
                    'uri': 'http://maps.google.com/',
                    'description': 'Link module URI description',
                    'id': 'LINK_MODULE_URI_ID'
                }, {
                    'uri': 'tel:6505555555',
                    'description': 'Link module tel description',
                    'id': 'LINK_MODULE_TEL_ID'
                }]
            },
            'imageModulesData': [{
                'mainImage': {
                    'sourceUri': {
                        'uri':
                            'http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg'
                    },
                    'contentDescription': {
                        'defaultValue': {
                            'language': 'en-US',
                            'value': 'Image module description'
                        }
                    }
                },
                'id': 'IMAGE_MODULE_ID'
            }],
            'barcode': {
                'type': 'QR_CODE',
                'value': 'QR code'
            },
            'cardTitle': {
                'defaultValue': {
                    'language': 'en-US',
                    'value': 'Generic card title'
                }
            },
            'header': {
                'defaultValue': {
                    'language': 'en-US',
                    'value': 'Generic header'
                }
            },
            'hexBackgroundColor': '#4285f4',
            'logo': {
                'sourceUri': {
                    'uri':
                        'https://storage.googleapis.com/wallet-lab-tools-codelab-artifacts-public/pass_google_logo.jpg'
                },
                'contentDescription': {
                    'defaultValue': {
                        'language': 'en-US',
                        'value': 'Generic card logo'
                    }
                }
            }
        }

        # Create the JWT claims
        claims = {
            'iss': self.credentials.service_account_email,
            'aud': 'google',
            'origins': ['www.example.com'],
            'typ': 'savetowallet',
            'payload': {
                # The listed classes and objects will be created
                'genericClasses': [new_class],
                'genericObjects': [new_object]
            }
        }

        # The service account credentials are used to sign the JWT
        signer = crypt.RSASigner.from_service_account_file(self.key_file_path)
        token = jwt.encode(signer, claims).decode('utf-8')

        print('Add to Google Wallet link')
        print(f'https://pay.google.com/gp/v/save/{token}')

        return f'https://pay.google.com/gp/v/save/{token}'

    # [END jwtNew]

    # [START jwtExisting]
    def create_jwt_existing_objects(self, issuer_id: str) -> str:
        """Generate a signed JWT that references an existing pass object.

        When the user opens the "Add to Google Wallet" URL and saves the pass to
        their wallet, the pass objects defined in the JWT are added to the
        user's Google Wallet app. This allows the user to save multiple pass
        objects in one API call.

        The objects to add must follow the below format:

        {
            'id': 'ISSUER_ID.OBJECT_SUFFIX',
            'classId': 'ISSUER_ID.CLASS_SUFFIX'
        }

        Args:
            issuer_id (str): The issuer ID being used for this request.

        Returns:
            An "Add to Google Wallet" link
        """

        # Multiple pass types can be added at the same time
        # At least one type must be specified in the JWT claims
        # Note: Make sure to replace the placeholder class and object suffixes
        objects_to_add = {
            # Event tickets
            'eventTicketObjects': [{
                'id': f'{issuer_id}.EVENT_OBJECT_SUFFIX',
                'classId': f'{issuer_id}.EVENT_CLASS_SUFFIX'
            }],

            # Boarding passes
            'flightObjects': [{
                'id': f'{issuer_id}.FLIGHT_OBJECT_SUFFIX',
                'classId': f'{issuer_id}.FLIGHT_CLASS_SUFFIX'
            }],

            # Generic passes
            'genericObjects': [{
                'id': f'{issuer_id}.GENERIC_OBJECT_SUFFIX',
                'classId': f'{issuer_id}.GENERIC_CLASS_SUFFIX'
            }],

            # Gift cards
            'giftCardObjects': [{
                'id': f'{issuer_id}.GIFT_CARD_OBJECT_SUFFIX',
                'classId': f'{issuer_id}.GIFT_CARD_CLASS_SUFFIX'
            }],

            # Loyalty cards
            'loyaltyObjects': [{
                'id': f'{issuer_id}.LOYALTY_OBJECT_SUFFIX',
                'classId': f'{issuer_id}.LOYALTY_CLASS_SUFFIX'
            }],

            # Offers
            'offerObjects': [{
                'id': f'{issuer_id}.OFFER_OBJECT_SUFFIX',
                'classId': f'{issuer_id}.OFFER_CLASS_SUFFIX'
            }],

            # Transit passes
            'transitObjects': [{
                'id': f'{issuer_id}.TRANSIT_OBJECT_SUFFIX',
                'classId': f'{issuer_id}.TRANSIT_CLASS_SUFFIX'
            }]
        }

        # Create the JWT claims
        claims = {
            'iss': self.credentials.service_account_email,
            'aud': 'google',
            'origins': ['www.example.com'],
            'typ': 'savetowallet',
            'payload': objects_to_add
        }

        # The service account credentials are used to sign the JWT
        signer = crypt.RSASigner.from_service_account_file(self.key_file_path)
        token = jwt.encode(signer, claims).decode('utf-8')

        print('Add to Google Wallet link')
        print(f'https://pay.google.com/gp/v/save/{token}')

        return f'https://pay.google.com/gp/v/save/{token}'

    # [END jwtExisting]

    # [START batch]
    def batch_create_objects(self, issuer_id: str, class_suffix: str):
        """Batch create Google Wallet objects from an existing class.

        The request body will be a multiline string. See below for information.

        https://cloud.google.com/compute/docs/api/how-tos/batch#example

        Args:
            issuer_id (str): The issuer ID being used for this request.
            class_suffix (str): Developer-defined unique ID for this pass class.
        """
        batch = self.client.new_batch_http_request()

        # Example: Generate three new pass objects
        for _ in range(3):
            # Generate a random object suffix
            object_suffix = str(uuid.uuid4()).replace('[^\\w.-]', '_')

            # See link below for more information on required properties
            # https://developers.google.com/wallet/generic/rest/v1/genericobject
            batch_object = {
                'id': f'{issuer_id}.{object_suffix}',
                'classId': f'{issuer_id}.{class_suffix}',
                'state': 'ACTIVE',
                'heroImage': {
                    'sourceUri': {
                        'uri':
                            'https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg'
                    },
                    'contentDescription': {
                        'defaultValue': {
                            'language': 'en-US',
                            'value': 'Hero image description'
                        }
                    }
                },
                'textModulesData': [{
                    'header': 'Text module header',
                    'body': 'Text module body',
                    'id': 'TEXT_MODULE_ID'
                }],
                'linksModuleData': {
                    'uris': [{
                        'uri': 'http://maps.google.com/',
                        'description': 'Link module URI description',
                        'id': 'LINK_MODULE_URI_ID'
                    }, {
                        'uri': 'tel:6505555555',
                        'description': 'Link module tel description',
                        'id': 'LINK_MODULE_TEL_ID'
                    }]
                },
                'imageModulesData': [{
                    'mainImage': {
                        'sourceUri': {
                            'uri':
                                'http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg'
                        },
                        'contentDescription': {
                            'defaultValue': {
                                'language': 'en-US',
                                'value': 'Image module description'
                            }
                        }
                    },
                    'id': 'IMAGE_MODULE_ID'
                }],
                'barcode': {
                    'type': 'QR_CODE',
                    'value': 'QR code'
                },
                'cardTitle': {
                    'defaultValue': {
                        'language': 'en-US',
                        'value': 'Generic card title'
                    }
                },
                'header': {
                    'defaultValue': {
                        'language': 'en-US',
                        'value': 'Generic header'
                    }
                },
                'hexBackgroundColor': '#4285f4',
                'logo': {
                    'sourceUri': {
                        'uri':
                            'https://storage.googleapis.com/wallet-lab-tools-codelab-artifacts-public/pass_google_logo.jpg'
                    },
                    'contentDescription': {
                        'defaultValue': {
                            'language': 'en-US',
                            'value': 'Generic card logo'
                        }
                    }
                }
            }

            batch.add(self.client.genericobject().insert(body=batch_object))

        # Invoke the batch API calls
        response = batch.execute()

        print('Batch complete')

    # [END batch]
