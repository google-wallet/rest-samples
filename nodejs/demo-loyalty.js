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
  const { GoogleAuth } = require('google-auth-library');
  const jwt = require('jsonwebtoken');

  // Path to service account key file obtained from Google CLoud Console.
  const serviceAccountFile = process.env.GOOGLE_APPLICATION_CREDENTIALS || '/path/to/key.json';

  // Issuer ID obtained from Google Pay Business Console.
  const issuerId = process.env.WALLET_ISSUER_ID || '<issuer ID>';

  // Developer defined ID for the wallet class.
  const classId = process.env.WALLET_CLASS_ID || 'test-loyalty-class-id';

  // Developer defined ID for the user, eg an email address.
  const userId = process.env.WALLET_USER_ID || 'test@example.com';

  // ID for the wallet object, must be in the form `issuerId.userId` where userId is alphanumeric.
  const objectId = `${issuerId}.${userId.replace(/[^\w.-]/g, '_')}-${classId}`;
  // [END setup]

  ///////////////////////////////////////////////////////////////////////////////
  // Create authenticated HTTP client, using service account file.
  ///////////////////////////////////////////////////////////////////////////////

  // [START auth]
  const credentials = require(serviceAccountFile);
  const httpClient = new GoogleAuth({
    credentials: credentials,
    scopes: 'https://www.googleapis.com/auth/wallet_object.issuer'
  });
  // [END auth]

  ///////////////////////////////////////////////////////////////////////////////
  // Create a class via the API (this can also be done in the business console).
  ///////////////////////////////////////////////////////////////////////////////

  // [START class]
  const classUrl = 'https://walletobjects.googleapis.com/walletobjects/v1/loyaltyClass/';
  const classPayload = {
    "id": `${issuerId}.${classId}`,
    "issuerName": "test issuer name",
    "programName": "test program name",
    "programLogo": {
      "kind": "walletobjects#image",
      "sourceUri": {
        "kind": "walletobjects#uri",
        "uri": "http://farm8.staticflickr.com/7340/11177041185_a61a7f2139_o.jpg"
      }
    },
    "reviewStatus": "underReview"
  };

  let classResponse;
  try {
    classResponse = await httpClient.request({url: classUrl, method: 'POST', data: classPayload});
  } catch (err) {
    classResponse = err;
  }
  console.log('class POST response:', classResponse);
  // [END class]

  ///////////////////////////////////////////////////////////////////////////////
  // Get or create an object via the API.
  ///////////////////////////////////////////////////////////////////////////////

  // [START object]
  const objectUrl = 'https://walletobjects.googleapis.com/walletobjects/v1/loyaltyObject/';
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
    "accountId": "Test account id",
    "accountName": "Test account name",
    "loyaltyPoints": {
      "balance": {
        "string": "800"
      },
      "label": "Points"
    },
    "locations": [
      {
        "kind": "walletobjects#latLongPoint",
        "latitude": 37.424015499999996,
        "longitude": -122.09259560000001
      }
    ]
  };

  // Retrieve the object, or create it if it doesn't exist.
  let objectResponse;
  try {
    objectResponse = await httpClient.request({url: objectUrl + objectId, method: 'GET'});
  } catch (err) {
    if (err.response && err.response.status === 404) {
      objectResponse = await httpClient.request({url: objectUrl, method: 'POST', data: objectPayload});
    } else {
      objectResponse = err;
    }
  }
  console.log('object GET or POST response:', objectResponse);
  // [END object]

  ///////////////////////////////////////////////////////////////////////////////
  // Create a JWT for the object, and encode it to create a "Save" URL.
  ///////////////////////////////////////////////////////////////////////////////

  // [START jwt]
  const claims = {
    iss: credentials.client_email, // `client_email` in service account file.
    aud: 'google',
    origins: ['www.example.com'],
    typ: 'savetowallet',
    payload: {
      loyaltyObjects: [{id: objectId}],
    },
  };

  const token = jwt.sign(claims, credentials.private_key, {algorithm: 'RS256'});
  const saveUrl = `https://pay.google.com/gp/v/save/${token}`;
  console.log(saveUrl);
  // [END jwt]

};

main().catch(console.error);