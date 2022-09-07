/*
 * Copyright 2022 Google Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

async function main() {

  // [START setup]
  // [START imports]
  const { GoogleAuth } = require('google-auth-library');
  const jwt = require('jsonwebtoken');
  const { v4: uuidv4 } = require('uuid');
  // [END imports]

  /*
   * keyFilePath - Path to service account key file from Google Cloud Console
   *             - Environment variable: GOOGLE_APPLICATION_CREDENTIALS
   */
  const keyFilePath = process.env.GOOGLE_APPLICATION_CREDENTIALS || '/path/to/key.json';

  /*
   * issuerId - The issuer ID being updated in this request
   *          - Environment variable: WALLET_ISSUER_ID
   */
  const issuerId = process.env.WALLET_ISSUER_ID || 'issuer-id';

  /*
   * classId - Developer-defined ID for the wallet class
   *         - Environment variable: WALLET_CLASS_ID
   */
  const classId = process.env.WALLET_CLASS_ID || 'test-eventTicket-class-id';

  /*
   * userId - Developer-defined ID for the user, such as an email address
   *        - Environment variable: WALLET_USER_ID
   */
  let userId = process.env.WALLET_USER_ID || 'user-id';

  /*
   * objectId - ID for the wallet object
   *          - Format: `issuerId.identifier`
   *          - Should only include alphanumeric characters, '.', '_', or '-'
   *          - `identifier` is developer-defined and unique to the user
   */
  let objectId = `${issuerId}.${userId.replace(/[^\w.-]/g, '_')}-${classId}`;
  // [END setup]

  ///////////////////////////////////////////////////////////////////////////////
  // Create authenticated HTTP client, using service account file.
  ///////////////////////////////////////////////////////////////////////////////

  // [START auth]
  const credentials = require(keyFilePath);

  const httpClient = new GoogleAuth({
    credentials: credentials,
    scopes: 'https://www.googleapis.com/auth/wallet_object.issuer'
  });
  // [END auth]

  ///////////////////////////////////////////////////////////////////////////////
  // Create a class via the API (this can also be done in the business console).
  ///////////////////////////////////////////////////////////////////////////////

  // [START class]
  const classUrl = 'https://walletobjects.googleapis.com/walletobjects/v1/eventTicketClass/';
  const classPayload = {
    "id": `${issuerId}.${classId}`,
    "issuerName": "test issuer name",
    "eventName": {
      "defaultValue": {
        "language": "en-US",
        "value": "Test event name"
      }
    },
    "reviewStatus": "underReview"
  };

  let classResponse = await httpClient.request({
    url: classUrl,
    method: 'POST',
    data: classPayload
  });

  console.log('class POST response: ', classResponse);
  // [END class]

  ///////////////////////////////////////////////////////////////////////////////
  // Get or create an object via the API.
  ///////////////////////////////////////////////////////////////////////////////

  // [START object]
  const objectUrl = 'https://walletobjects.googleapis.com/walletobjects/v1/eventTicketObject/';
  const objectPayload = {
    "id": objectId,
    "classId": `${issuerId}.${classId}`,
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
    "state": "active",
    "seatInfo": {
      "kind": "walletobjects#eventSeat",
      "seat": {
        "kind": "walletobjects#localizedString",
        "defaultValue": {
          "kind": "walletobjects#translatedString",
          "language": "en-us",
          "value": "42"
        }
      },
      "row": {
        "kind": "walletobjects#localizedString",
        "defaultValue": {
          "kind": "walletobjects#translatedString",
          "language": "en-us",
          "value": "G3"
        }
      },
      "section": {
        "kind": "walletobjects#localizedString",
        "defaultValue": {
          "kind": "walletobjects#translatedString",
          "language": "en-us",
          "value": "5"
        }
      },
      "gate": {
        "kind": "walletobjects#localizedString",
        "defaultValue": {
          "kind": "walletobjects#translatedString",
          "language": "en-us",
          "value": "A"
        }
      }
    },
    "ticketHolderName": "Test ticket holder name",
    "ticketNumber": "Test ticket number",
    "locations": [
      {
        "kind": "walletobjects#latLongPoint",
        "latitude": 37.424015499999996,
        "longitude": -122.09259560000001
      }
    ]
  };
  let objectResponse;

  try {
    objectResponse = await httpClient.request({
      url: objectUrl + objectId,
      method: 'GET'
    });
  } catch (err) {
    if (err.response && err.response.status === 404) {
      // Object does not yet exist
      // Send POST request to create it
      objectResponse = await httpClient.request({
        url: objectUrl,
        method: 'POST',
        data: objectPayload
      });
    } else {
      objectResponse = err;
    }
  }

  console.log('object GET or POST response:', objectResponse);
  // [END object]

  ///////////////////////////////////////////////////////////////////////////////
  // Create a JWT for the object, and encode it to create a 'Save' URL.
  ///////////////////////////////////////////////////////////////////////////////

  // [START jwt]
  const claims = {
    iss: credentials.client_email,
    aud: 'google',
    origins: ['www.example.com'],
    typ: 'savetowallet',
    payload: {
      eventTicketObjects: [{
        id: objectId
      }],
    }
  };

  const token = jwt.sign(claims, credentials.private_key, { algorithm: 'RS256' });
  const saveUrl = `https://pay.google.com/gp/v/save/${token}`;

  console.log(saveUrl);
  // [END jwt]

  ///////////////////////////////////////////////////////////////////////////////
  // Create a new Google Wallet issuer account
  ///////////////////////////////////////////////////////////////////////////////

  // [START createIssuer]
  // New issuer name
  const issuerName = 'name';

  // New issuer email address
  const issuerEmail = 'email-address';

  // Issuer API endpoint
  const issuerUrl = 'https://walletobjects.googleapis.com/walletobjects/v1/issuer';

  // New issuer information
  let issuerPayload = {
    name: issuerName,
    contactInfo: {
      email: issuerEmail
    }
  };

  let issuerResponse = await httpClient.request({
    url: issuerUrl,
    method: 'POST',
    data: issuerPayload
  });

  console.log('issuer POST response:', issuerResponse);
  // [END createIssuer]

  ///////////////////////////////////////////////////////////////////////////////
  // Update permissions for an existing Google Wallet issuer account
  ///////////////////////////////////////////////////////////////////////////////

  // [START updatePermissions]
  // Permissions API endpoint
  permissionsUrl = `https://walletobjects.googleapis.com/walletobjects/v1/permissions/${issuerId}`;

  // New issuer permissions information
  permissionsPayload = {
    issuerId: issuerId,
    permissions: [
      // Copy as needed for each email address that will need access
      {
        emailAddress: 'email-address',
        role: 'READER | WRITER | OWNER'
      }
    ]
  };

  let permissionsResponse = await httpClient.request({
    url: permissionsUrl,
    method: 'PUT',
    data: permissionsPayload
  });

  console.log('permissions PUT response:', permissionsResponse);
  // [END updatePermissions]

  ///////////////////////////////////////////////////////////////////////////////
  // Batch create Google Wallet objects from an existing class
  ///////////////////////////////////////////////////////////////////////////////

  //[START batch]
  // The request body will be a multiline string
  // See below for more information
  // https://cloud.google.com/compute/docs/api/how-tos/batch#example
  let data = '';
  let batchObject;

  // Example: Generate three new pass objects
  for (let i = 0; i < 3; i++) {
    // Generate a random user ID
    userId = uuidv4().replace('[^\\w.-]', '_');

    // Generate an object ID with the user ID
    objectId = `${issuerId}.${userId}-${classId}`;
    batchObject = {
      "id": objectId,
      "classId": `${issuerId}.${classId}`,
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
      "state": "active",
      "seatInfo": {
        "kind": "walletobjects#eventSeat",
        "seat": {
          "kind": "walletobjects#localizedString",
          "defaultValue": {
            "kind": "walletobjects#translatedString",
            "language": "en-us",
            "value": "42"
          }
        },
        "row": {
          "kind": "walletobjects#localizedString",
          "defaultValue": {
            "kind": "walletobjects#translatedString",
            "language": "en-us",
            "value": "G3"
          }
        },
        "section": {
          "kind": "walletobjects#localizedString",
          "defaultValue": {
            "kind": "walletobjects#translatedString",
            "language": "en-us",
            "value": "5"
          }
        },
        "gate": {
          "kind": "walletobjects#localizedString",
          "defaultValue": {
            "kind": "walletobjects#translatedString",
            "language": "en-us",
            "value": "A"
          }
        }
      },
      "ticketHolderName": "Test ticket holder name",
      "ticketNumber": "Test ticket number",
      "locations": [
        {
          "kind": "walletobjects#latLongPoint",
          "latitude": 37.424015499999996,
          "longitude": -122.09259560000001
        }
      ]
    };

    data += '--batch_createobjectbatch\n';
    data += 'Content-Type: application/json\n\n';
    data += 'POST /walletobjects/v1/eventTicketObject/\n\n';

    data += JSON.stringify(batchObject) + '\n\n';
  }
  data += '--batch_createobjectbatch--';

  // Invoke the batch API calls
  let batchResponse = await httpClient.request({
    url: 'https://walletobjects.googleapis.com/batch',
    method: 'POST',
    data: data,
    headers: {
      // `boundary` is the delimiter between API calls in the batch request
      'Content-Type': 'multipart/mixed; boundary=batch_createobjectbatch'
    }
  });

  console.log('batch POST response:', batchResponse);
  // [END batch]
};
