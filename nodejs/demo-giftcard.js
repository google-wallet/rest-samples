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

// [START setup]
// [START imports]
const { GoogleAuth } = require('google-auth-library');
const jwt = require('jsonwebtoken');
const { v4: uuidv4 } = require('uuid');
// [END imports]

/**
 * Demo class for creating and managing Gift cards in Google Wallet.
 */
class DemoGiftCard {
  constructor() {
    /**
     * Path to service account key file from Google Cloud Console. Environment
     * variable: GOOGLE_APPLICATION_CREDENTIALS.
     */
    this.keyFilePath = process.env.GOOGLE_APPLICATION_CREDENTIALS || '/path/to/key.json';

    /**
     * Base URL for Google Wallet API requests.
     */
    this.baseUrl = 'https://walletobjects.googleapis.com/walletobjects/v1'
  }
  // [END setup]

  // [START auth]
  /**
   * Create authenticated HTTP client using a service account file.
   */
  auth() {
    this.credentials = require(this.keyFilePath);

    this.httpClient = new GoogleAuth({
      credentials: this.credentials,
      scopes: 'https://www.googleapis.com/auth/wallet_object.issuer',
    });
  }
  // [END auth]

  // [START class]
  /**
   * Create a class via the API. This can also be done in the Google Pay and
   * Wallet console.
   *
   * @param {string} issuerId The issuer ID being used for this request.
   * @param {string} classSuffix Developer-defined unique ID for this pass class.
   *
   * @returns {string} The pass class ID: `${issuerId}.${classSuffix}`
   */
  async createGiftCardClass(issuerId, classSuffix) {
    const giftCardClassUrl = `${this.baseUrl}/giftCardClass`;

    // See link below for more information on required properties
    // https://developers.google.com/wallet/retail/gift-cards/rest/v1/giftcardclass
    let giftCardClass = {
      'id': `${issuerId}.${classSuffix}`,
      'issuerName': 'Issuer name',
      'reviewStatus': 'UNDER_REVIEW',
    };

    let response = await this.httpClient.request({
      url: giftCardClassUrl,
      method: 'POST',
      data: giftCardClass,
    });

    console.log('Class insert response');
    console.log(response);

    return response.data.id;
  }
  // [END class]

  // [START object]
  /**
   * Create an object via the API.
   *
   * @param {string} issuerId The issuer ID being used for this request.
   * @param {string} classSuffix Developer-defined unique ID for this pass class.
   * @param {string} userId Developer-defined user ID for this object.
   *
   * @returns {string} The pass object ID: `${issuerId}.${userId}`
   */
  async createGiftCardObject(issuerId, classSuffix, userId) {
    const giftCardObjectUrl = `${this.baseUrl}/giftCardObject`;

    // Generate the object ID
    // Should only include alphanumeric characters, '.', '_', or '-'
    let objectId = `${issuerId}.${userId.replace(/[^\w.-]/g, '_')}`;

    // See link below for more information on required properties
    // https://developers.google.com/wallet/retail/gift-cards/rest/v1/giftcardobject
    let giftCardObject = {
      'id': `${objectId}`,
      'classId': `${issuerId}.${classSuffix}`,
      'state': 'ACTIVE',
      'heroImage': {
        'sourceUri': {
          'uri': 'https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg',
        },
        'contentDescription': {
          'defaultValue': {
            'language': 'en-US',
            'value': 'Hero image description',
          },
        },
      },
      'textModulesData': [
        {
          'header': 'Text module header',
          'body': 'Text module body',
          'id': 'TEXT_MODULE_ID',
        },
      ],
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
      'imageModulesData': [
        {
          'mainImage': {
            'sourceUri': {
              'uri': 'http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg',
            },
            'contentDescription': {
              'defaultValue': {
                'language': 'en-US',
                'value': 'Image module description',
              },
            },
          },
          'id': 'IMAGE_MODULE_ID',
        },
      ],
      'barcode': {
        'type': 'QR_CODE',
        'value': 'QR code',
      },
      'locations': [
        {
          'latitude': 37.424015499999996,
          'longitude': -122.09259560000001,
        },
      ],
      'cardNumber': 'Card number',
      'pin': '1234',
      'balance': {
        'micros': 20000000,
        'currencyCode': 'USD',
      },
      'balanceUpdateTime': {
        'date': '2020-04-12T16:20:50.52-04:00',
      },
    };

    let response;
    try {
      response = await this.httpClient.request({
        url: `${giftCardObjectUrl}/${objectId}`,
        method: 'GET',
      });

      console.log('Object get response');
      console.log(response);

      return response.data.id;
    } catch (err) {
      if (err.response && err.response.status === 404) {
        // Object does not yet exist
        // Send POST request to create it
        response = await this.httpClient.request({
          url: giftCardObjectUrl,
          method: 'POST',
          data: giftCardObject,
        });

        console.log('Object insert response');
        console.log(response);

        return response.data.id;
      } else {
        // Something else went wrong
        console.log(err);
      }
    }
  }
  // [END object]

  // [START jwt]
  /**
   * Generate a signed JWT that creates a new pass class and object.
   *
   * When the user opens the "Add to Google Wallet" URL and saves the pass to
   * their wallet, the pass class and object defined in the JWT are
   * created. This allows you to create multiple pass classes and objects in
   * one API call when the user saves the pass to their wallet.
   *
   * @param {string} issuerId The issuer ID being used for this request.
   * @param {string} classSuffix Developer-defined unique ID for this pass class.
   * @param {string} userId Developer-defined user ID for this object.
   *
   * @returns {string} An "Add to Google Wallet" link.
   */
  createJwtSaveUrl(issuerId, classSuffix, userId) {
    // Generate the object ID
    // Should only include alphanumeric characters, '.', '_', or '-'
    let objectId = `${issuerId}.${userId.replace(/[^\w.-]/g, '_')}`;

    // See link below for more information on required properties
    // https://developers.google.com/wallet/retail/gift-cards/rest/v1/giftcardclass
    let giftCardClass = {
      'id': `${issuerId}.${classSuffix}`,
      'issuerName': 'Issuer name',
      'reviewStatus': 'UNDER_REVIEW',
    };

    // See link below for more information on required properties
    // https://developers.google.com/wallet/retail/gift-cards/rest/v1/giftcardobject
    let giftCardObject = {
      'id': `${objectId}`,
      'classId': `${issuerId}.${classSuffix}`,
      'state': 'ACTIVE',
      'heroImage': {
        'sourceUri': {
          'uri': 'https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg',
        },
        'contentDescription': {
          'defaultValue': {
            'language': 'en-US',
            'value': 'Hero image description',
          },
        },
      },
      'textModulesData': [
        {
          'header': 'Text module header',
          'body': 'Text module body',
          'id': 'TEXT_MODULE_ID',
        },
      ],
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
      'imageModulesData': [
        {
          'mainImage': {
            'sourceUri': {
              'uri': 'http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg',
            },
            'contentDescription': {
              'defaultValue': {
                'language': 'en-US',
                'value': 'Image module description',
              },
            },
          },
          'id': 'IMAGE_MODULE_ID',
        },
      ],
      'barcode': {
        'type': 'QR_CODE',
        'value': 'QR code',
      },
      'locations': [
        {
          'latitude': 37.424015499999996,
          'longitude': -122.09259560000001,
        },
      ],
      'cardNumber': 'Card number',
      'pin': '1234',
      'balance': {
        'micros': 20000000,
        'currencyCode': 'USD',
      },
      'balanceUpdateTime': {
        'date': '2020-04-12T16:20:50.52-04:00',
      },
    };

    // Create the JWT claims
    let claims = {
      iss: this.credentials.client_email,
      aud: 'google',
      origins: ['www.example.com'],
      typ: 'savetowallet',
      payload: {
        // The listed classes and objects will be created
        giftCardClasses: [giftCardClass,],
        giftCardObjects: [giftCardObject,],
      },
    };

    // The service account credentials are used to sign the JWT
    let token = jwt.sign(claims, this.credentials.private_key, { algorithm: 'RS256' });

    console.log('Add to Google Wallet link');
    console.log(`https://pay.google.com/gp/v/save/${token}`);

    return `https://pay.google.com/gp/v/save/${token}`;
  }
  // [END jwt]

  // [START createIssuer]
  /**
   * Create a new Google Wallet issuer account.
   *
   * @param {string} issuerName The issuer's name.
   * @param {string} issuerEmail The issuer's email address.
   */
  async createIssuerAccount(issuerName, issuerEmail) {
    // Issuer API endpoint
    const issuerUrl = `${this.baseUrl}/issuer`;

    // New issuer information
    let issuer = {
      name: issuerName,
      contactInfo: {
        email: issuerEmail,
      },
    };

    let response = await this.httpClient.request({
      url: issuerUrl,
      method: 'POST',
      data: issuer
    });

    console.log('Issuer insert response');
    console.log(response);
  }
  // [END createIssuer]

  // [START updatePermissions]
  /**
   * Update permissions for an existing Google Wallet issuer account.
   * **Warning:** This operation overwrites all existing permissions!
   *
   * Example permissions list argument below. Copy the dict entry as
   * needed for each email address that will need access. Supported
   * values for role are: 'READER', 'WRITER', and 'OWNER'
   *
   * let permissions = [
   *  {
   *    'emailAddress': 'email-address',
   *    'role': 'OWNER',
   *  },
   * ];
   *
   * @param {string} issuerId The issuer ID being used for this request.
   * @param {Array} permissions The list of email addresses and roles to assign.
   */
  async updateIssuerPermissions(issuerId, permissions) {
    // Permissions API endpoint
    const permissionsUrl = `${this.baseUrl}/permissions/${issuerId}`;

    let response = await this.httpClient.request({
      url: permissionsUrl,
      method: 'PUT',
      data: {
        issuerId: issuerId,
        permissions: permissions,
      }
    });

    console.log('Permissions update response');
    console.log(response);
  }
  // [END updatePermissions]

  // [START batch]
  /**
   * Batch create Google Wallet objects from an existing class.
   *
   * @param {string} issuerId The issuer ID being used for this request.
   * @param {string} classSuffix Developer-defined unique ID for this pass class.
   */
  async batchCreateGiftCardObjects(issuerId, classSuffix) {
    // See below for more information
    // https://cloud.google.com/compute/docs/api/how-tos/batch#example
    let data = '';
    let giftCardObject;
    let userId;
    let objectId;

    // Example: Generate three new pass objects
    for (let i = 0; i < 3; i++) {
      // Generate a random user ID
      userId = uuidv4().replace('[^\w.-]', '_');

      // Generate an object ID with the user ID
      // Should only include alphanumeric characters, '.', '_', or '-'
      objectId = `${issuerId}.${userId}`;

      // See link below for more information on required properties
      // https://developers.google.com/wallet/retail/gift-cards/rest/v1/giftcardobject
      giftCardObject = {
        'id': `${objectId}`,
        'classId': `${issuerId}.${classSuffix}`,
        'state': 'ACTIVE',
        'heroImage': {
          'sourceUri': {
            'uri': 'https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg',
          },
          'contentDescription': {
            'defaultValue': {
              'language': 'en-US',
              'value': 'Hero image description',
            },
          },
        },
        'textModulesData': [
          {
            'header': 'Text module header',
            'body': 'Text module body',
            'id': 'TEXT_MODULE_ID',
          },
        ],
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
        'imageModulesData': [
          {
            'mainImage': {
              'sourceUri': {
                'uri': 'http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg',
              },
              'contentDescription': {
                'defaultValue': {
                  'language': 'en-US',
                  'value': 'Image module description',
                },
              },
            },
            'id': 'IMAGE_MODULE_ID',
          },
        ],
        'barcode': {
          'type': 'QR_CODE',
          'value': 'QR code',
        },
        'locations': [
          {
            'latitude': 37.424015499999996,
            'longitude': -122.09259560000001,
          },
        ],
        'cardNumber': 'Card number',
        'pin': '1234',
        'balance': {
          'micros': 20000000,
          'currencyCode': 'USD',
        },
        'balanceUpdateTime': {
          'date': '2020-04-12T16:20:50.52-04:00',
        },
      };

      data += '--batch_createobjectbatch\n';
      data += 'Content-Type: application/json\n\n';
      data += 'POST /walletobjects/v1/giftCardObject\n\n';

      data += JSON.stringify(giftCardObject) + '\n\n';
    }
    data += '--batch_createobjectbatch--';

    // Invoke the batch API calls
    let response = await this.httpClient.request({
      url: `${this.baseUrl}/batch`,
      method: 'POST',
      data: data,
      headers: {
        // `boundary` is the delimiter between API calls in the batch request
        'Content-Type': 'multipart/mixed; boundary=batch_createobjectbatch'
      }
    });

    console.log('Batch insert response');
    console.log(response);
  }
  // [END batch]
}

module.exports = { DemoGiftCard };
