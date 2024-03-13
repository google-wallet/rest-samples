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
const { google } = require('googleapis');
const jwt = require('jsonwebtoken');
const { v4: uuidv4 } = require('uuid');
// [END imports]

/**
 * Demo class for creating and managing Flights in Google Wallet.
 */
class DemoFlight {
  constructor() {
    /**
     * Path to service account key file from Google Cloud Console. Environment
     * variable: GOOGLE_APPLICATION_CREDENTIALS.
     */
    this.keyFilePath = process.env.GOOGLE_APPLICATION_CREDENTIALS || '/path/to/key.json';
    this.auth();
  }
  // [END setup]

  // [START auth]
  /**
   * Create authenticated HTTP client using a service account file.
   */
  auth() {
    const auth = new google.auth.GoogleAuth({
      keyFile: this.keyFilePath,
      scopes: ['https://www.googleapis.com/auth/wallet_object.issuer'],
    });

    this.credentials = require(this.keyFilePath);

    this.client = google.walletobjects({
      version: 'v1',
      auth: auth,
    });
  }
  // [END auth]

  // [START createClass]
  /**
   * Create a class.
   *
   * @param {string} issuerId The issuer ID being used for this request.
   * @param {string} classSuffix Developer-defined unique ID for this pass class.
   *
   * @returns {string} The pass class ID: `${issuerId}.${classSuffix}`
   */
  async createClass(issuerId, classSuffix) {
    let response;

    // Check if the class exists
    try {
      response = await this.client.flightclass.get({
        resourceId: `${issuerId}.${classSuffix}`
      });

      console.log(`Class ${issuerId}.${classSuffix} already exists!`);

      return `${issuerId}.${classSuffix}`;
    } catch (err) {
      if (err.response && err.response.status !== 404) {
        // Something else went wrong...
        console.log(err);
        return `${issuerId}.${classSuffix}`;
      }
    }

    // See link below for more information on required properties
    // https://developers.google.com/wallet/tickets/boarding-passes/rest/v1/flightclass
    let newClass = {
      'id': `${issuerId}.${classSuffix}`,
      'issuerName': 'Issuer name',
      'reviewStatus': 'UNDER_REVIEW',
      'localScheduledDepartureDateTime': '2023-07-02T15:30:00',
      'flightHeader': {
        'carrier': {
          'carrierIataCode': 'LX'
        },
        'flightNumber': '123'
      },
      'origin': {
        'airportIataCode': 'LAX',
        'terminal': '1',
        'gate': 'A2'
      },
      'destination': {
        'airportIataCode': 'SFO',
        'terminal': '2',
        'gate': 'C3'
      }
    };

    response = await this.client.flightclass.insert({
      requestBody: newClass
    });

    console.log('Class insert response');
    console.log(response);

    return `${issuerId}.${classSuffix}`;
  }
  // [END createClass]

  // [START updateClass]
  /**
   * Update a class.
   *
   * **Warning:** This replaces all existing class attributes!
   *
   * @param {string} issuerId The issuer ID being used for this request.
   * @param {string} classSuffix Developer-defined unique ID for this pass class.
   *
   * @returns {string} The pass class ID: `${issuerId}.${classSuffix}`
   */
  async updateClass(issuerId, classSuffix) {
    let response;

    // Check if the class exists
    try {
      response = await this.client.flightclass.get({
        resourceId: `${issuerId}.${classSuffix}`
      });
    } catch (err) {
      if (err.response && err.response.status === 404) {
        console.log(`Class ${issuerId}.${classSuffix} not found!`);
        return `${issuerId}.${classSuffix}`;
      } else {
        // Something else went wrong...
        console.log(err);
        return `${issuerId}.${classSuffix}`;
      }
    }

    // Class exists
    let updatedClass = response.data;

    // Update the class by adding a homepage
    updatedClass['homepageUri'] = {
      'uri': 'https://developers.google.com/wallet',
      'description': 'Homepage description'
    };

    // Note: reviewStatus must be 'UNDER_REVIEW' or 'DRAFT' for updates
    updatedClass['reviewStatus'] = 'UNDER_REVIEW';

    response = await this.client.flightclass.update({
      resourceId: `${issuerId}.${classSuffix}`,
      requestBody: updatedClass
    });

    console.log('Class update response');
    console.log(response);

    return `${issuerId}.${classSuffix}`;
  }
  // [END updateClass]

  // [START patchClass]
  /**
   * Patch a class.
   *
   * The PATCH method supports patch semantics.
   *
   * @param {string} issuerId The issuer ID being used for this request.
   * @param {string} classSuffix Developer-defined unique ID for this pass class.
   *
   * @returns {string} The pass class ID: `${issuerId}.${classSuffix}`
   */
  async patchClass(issuerId, classSuffix) {
    let response;

    // Check if the class exists
    try {
      response = await this.client.flightclass.get({
        resourceId: `${issuerId}.${classSuffix}`
      });
    } catch (err) {
      if (err.response && err.response.status === 404) {
        console.log(`Class ${issuerId}.${classSuffix} not found!`);
        return `${issuerId}.${classSuffix}`;
      } else {
        // Something else went wrong...
        console.log(err);
        return `${issuerId}.${classSuffix}`;
      }
    }

    // Patch the class by adding a homepage
    let patchBody = {
      'homepageUri': {
        'uri': 'https://developers.google.com/wallet',
        'description': 'Homepage description'
      },

      // Note: reviewStatus must be 'UNDER_REVIEW' or 'DRAFT' for updates
      'reviewStatus': 'UNDER_REVIEW'
    };

    response = await this.client.flightclass.patch({
      resourceId: `${issuerId}.${classSuffix}`,
      requestBody: patchBody
    });

    console.log('Class patch response');
    console.log(response);

    return `${issuerId}.${classSuffix}`;
  }
  // [END patchClass]

  // [START addMessageClass]
  /**
   * Add a message to a pass class.
   *
   * @param {string} issuerId The issuer ID being used for this request.
   * @param {string} classSuffix Developer-defined unique ID for this pass class.
   * @param {string} header The message header.
   * @param {string} body The message body.
   *
   * @returns {string} The pass class ID: `${issuerId}.${classSuffix}`
   */
  async addClassMessage(issuerId, classSuffix, header, body) {
    let response;

    // Check if the class exists
    try {
      response = await this.client.flightclass.get({
        resourceId: `${issuerId}.${classSuffix}`
      });
    } catch (err) {
      if (err.response && err.response.status === 404) {
        console.log(`Class ${issuerId}.${classSuffix} not found!`);
        return `${issuerId}.${classSuffix}`;
      } else {
        // Something else went wrong...
        console.log(err);
        return `${issuerId}.${classSuffix}`;
      }
    }

    response = await this.client.flightclass.addmessage({
      resourceId: `${issuerId}.${classSuffix}`,
      requestBody: {
        'message': {
          'header': header,
          'body': body
        }
      }
    });

    console.log('Class addMessage response');
    console.log(response);

    return `${issuerId}.${classSuffix}`;
  }
  // [END addMessageClass]

  // [START createObject]
  /**
   * Create an object.
   *
   * @param {string} issuerId The issuer ID being used for this request.
   * @param {string} classSuffix Developer-defined unique ID for the pass class.
   * @param {string} objectSuffix Developer-defined unique ID for the pass object.
   *
   * @returns {string} The pass object ID: `${issuerId}.${objectSuffix}`
   */
  async createObject(issuerId, classSuffix, objectSuffix) {
    let response;

    // Check if the object exists
    try {
      response = await this.client.flightobject.get({
        resourceId: `${issuerId}.${objectSuffix}`
      });

      console.log(`Object ${issuerId}.${objectSuffix} already exists!`);

      return `${issuerId}.${objectSuffix}`;
    } catch (err) {
      if (err.response && err.response.status !== 404) {
        // Something else went wrong...
        console.log(err);
        return `${issuerId}.${objectSuffix}`;
      }
    }

    // See link below for more information on required properties
    // https://developers.google.com/wallet/tickets/boarding-passes/rest/v1/flightobject
    let newObject = {
      'id': `${issuerId}.${objectSuffix}`,
      'classId': `${issuerId}.${classSuffix}`,
      'state': 'ACTIVE',
      'heroImage': {
        'sourceUri': {
          'uri': 'https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg'
        },
        'contentDescription': {
          'defaultValue': {
            'language': 'en-US',
            'value': 'Hero image description'
          }
        }
      },
      'textModulesData': [
        {
          'header': 'Text module header',
          'body': 'Text module body',
          'id': 'TEXT_MODULE_ID'
        }
      ],
      'linksModuleData': {
        'uris': [
          {
            'uri': 'http://maps.google.com/',
            'description': 'Link module URI description',
            'id': 'LINK_MODULE_URI_ID'
          },
          {
            'uri': 'tel:6505555555',
            'description': 'Link module tel description',
            'id': 'LINK_MODULE_TEL_ID'
          }
        ]
      },
      'imageModulesData': [
        {
          'mainImage': {
            'sourceUri': {
              'uri': 'http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg'
            },
            'contentDescription': {
              'defaultValue': {
                'language': 'en-US',
                'value': 'Image module description'
              }
            }
          },
          'id': 'IMAGE_MODULE_ID'
        }
      ],
      'barcode': {
        'type': 'QR_CODE',
        'value': 'QR code'
      },
      'locations': [
        {
          'latitude': 37.424015499999996,
          'longitude': -122.09259560000001
        }
      ],
      'passengerName': 'Passenger name',
      'boardingAndSeatingInfo': {
        'boardingGroup': 'B',
        'seatNumber': '42'
      },
      'reservationInfo': {
        'confirmationCode': 'Confirmation code'
      }
    };

    response = await this.client.flightobject.insert({
      requestBody: newObject
    });

    console.log('Object insert response');
    console.log(response);

    return `${issuerId}.${objectSuffix}`;
  }
  // [END createObject]

  // [START updateObject]
  /**
   * Update an object.
   *
   * **Warning:** This replaces all existing object attributes!
   *
   * @param {string} issuerId The issuer ID being used for this request.
   * @param {string} objectSuffix Developer-defined unique ID for the pass object.
   *
   * @returns {string} The pass object ID: `${issuerId}.${objectSuffix}`
   */
  async updateObject(issuerId, objectSuffix) {
    let response;

    // Check if the object exists
    try {
      response = await this.client.flightobject.get({
        resourceId: `${issuerId}.${objectSuffix}`
      });
    } catch (err) {
      if (err.response && err.response.status === 404) {
        console.log(`Object ${issuerId}.${objectSuffix} not found!`);
        return `${issuerId}.${objectSuffix}`;
      } else {
        // Something else went wrong...
        console.log(err);
        return `${issuerId}.${objectSuffix}`;
      }
    }

    // Object exists
    let updatedObject = response.data;

    // Update the object by adding a link
    let newLink = {
      'uri': 'https://developers.google.com/wallet',
      'description': 'New link description'
    }
    if (updatedObject['linksModuleData'] === undefined) {
      updatedObject['linksModuleData'] = {
        'uris': [newLink]
      };
    } else {
      updatedObject['linksModuleData']['uris'].push(newLink);
    }

    response = await this.client.flightobject.update({
      resourceId: `${issuerId}.${objectSuffix}`,
      requestBody: updatedObject
    });

    console.log('Object update response');
    console.log(response);

    return `${issuerId}.${objectSuffix}`;
  }
  // [END updateObject]

  // [START patchObject]
  /**
   * Patch an object.
   *
   * @param {string} issuerId The issuer ID being used for this request.
   * @param {string} objectSuffix Developer-defined unique ID for the pass object.
   *
   * @returns {string} The pass object ID: `${issuerId}.${objectSuffix}`
   */
  async patchObject(issuerId, objectSuffix) {
    let response;

    // Check if the object exists
    try {
      response = await this.client.flightobject.get({
        resourceId: `${issuerId}.${objectSuffix}`
      });
    } catch (err) {
      if (err.response && err.response.status === 404) {
        console.log(`Object ${issuerId}.${objectSuffix} not found!`);
        return `${issuerId}.${objectSuffix}`;
      } else {
        // Something else went wrong...
        console.log(err);
        return `${issuerId}.${objectSuffix}`;
      }
    }

    // Object exists
    let existingObject = response.data;

    // Patch the object by adding a link
    let newLink = {
      'uri': 'https://developers.google.com/wallet',
      'description': 'New link description'
    };

    let patchBody = {};
    if (existingObject['linksModuleData'] === undefined) {
      patchBody['linksModuleData'] = {
        'uris': []
      };
    } else {
      patchBody['linksModuleData'] = {
        'uris': existingObject['linksModuleData']['uris']
      };
    }
    patchBody['linksModuleData']['uris'].push(newLink);

    response = await this.client.flightobject.patch({
      resourceId: `${issuerId}.${objectSuffix}`,
      requestBody: patchBody
    });

    console.log('Object patch response');
    console.log(response);

    return `${issuerId}.${objectSuffix}`;
  }
  // [END patchObject]

  // [START expireObject]
  /**
   * Expire an object.
   *
   * Sets the object's state to Expired. If the valid time interval is
   * already set, the pass will expire automatically up to 24 hours after.
   *
   * @param {string} issuerId The issuer ID being used for this request.
   * @param {string} objectSuffix Developer-defined unique ID for the pass object.
   *
   * @returns {string} The pass object ID: `${issuerId}.${objectSuffix}`
   */
  async expireObject(issuerId, objectSuffix) {
    let response;

    // Check if the object exists
    try {
      response = await this.client.flightobject.get({
        resourceId: `${issuerId}.${objectSuffix}`
      });
    } catch (err) {
      if (err.response && err.response.status === 404) {
        console.log(`Object ${issuerId}.${objectSuffix} not found!`);
        return `${issuerId}.${objectSuffix}`;
      } else {
        // Something else went wrong...
        console.log(err);
        return `${issuerId}.${objectSuffix}`;
      }
    }

    // Patch the object, setting the pass as expired
    let patchBody = {
      'state': 'EXPIRED'
    };

    response = await this.client.flightobject.patch({
      resourceId: `${issuerId}.${objectSuffix}`,
      requestBody: patchBody
    });

    console.log('Object expiration response');
    console.log(response);

    return `${issuerId}.${objectSuffix}`;
  }
  // [END expireObject]

  // [START addMessageObject]
  /**
   * Add a message to a pass object.
   *
   * @param {string} issuerId The issuer ID being used for this request.
   * @param {string} objectSuffix Developer-defined unique ID for this pass object.
   * @param {string} header The message header.
   * @param {string} body The message body.
   *
   * @returns {string} The pass class ID: `${issuerId}.${classSuffix}`
   */
  async addObjectMessage(issuerId, objectSuffix, header, body) {
    let response;

    // Check if the object exists
    try {
      response = await this.client.flightobject.get({
        resourceId: `${issuerId}.${objectSuffix}`
      });
    } catch (err) {
      if (err.response && err.response.status === 404) {
        console.log(`Object ${issuerId}.${objectSuffix} not found!`);
        return `${issuerId}.${objectSuffix}`;
      } else {
        // Something else went wrong...
        console.log(err);
        return `${issuerId}.${objectSuffix}`;
      }
    }

    response = await this.client.flightobject.addmessage({
      resourceId: `${issuerId}.${classSuffix}`,
      requestBody: {
        'message': {
          'header': header,
          'body': body
        }
      }
    });

    console.log('Object addMessage response');
    console.log(response);

    return `${issuerId}.${objectSuffix}`;
  }
  // [END addMessageObject]

  // [START jwtNew]
  /**
   * Generate a signed JWT that creates a new pass class and object.
   *
   * When the user opens the "Add to Google Wallet" URL and saves the pass to
   * their wallet, the pass class and object defined in the JWT are
   * created. This allows you to create multiple pass classes and objects in
   * one API call when the user saves the pass to their wallet.
   *
   * @param {string} issuerId The issuer ID being used for this request.
   * @param {string} classSuffix Developer-defined unique ID for the pass class.
   * @param {string} objectSuffix Developer-defined unique ID for the pass object.
   *
   * @returns {string} An "Add to Google Wallet" link.
   */
  createJwtNewObjects(issuerId, classSuffix, objectSuffix) {
    // See link below for more information on required properties
    // https://developers.google.com/wallet/tickets/boarding-passes/rest/v1/flightclass
    let newClass = {
      'id': `${issuerId}.${classSuffix}`,
      'issuerName': 'Issuer name',
      'reviewStatus': 'UNDER_REVIEW',
      'localScheduledDepartureDateTime': '2023-07-02T15:30:00',
      'flightHeader': {
        'carrier': {
          'carrierIataCode': 'LX'
        },
        'flightNumber': '123'
      },
      'origin': {
        'airportIataCode': 'LAX',
        'terminal': '1',
        'gate': 'A2'
      },
      'destination': {
        'airportIataCode': 'SFO',
        'terminal': '2',
        'gate': 'C3'
      }
    };

    // See link below for more information on required properties
    // https://developers.google.com/wallet/tickets/boarding-passes/rest/v1/flightobject
    let newObject = {
      'id': `${issuerId}.${objectSuffix}`,
      'classId': `${issuerId}.${classSuffix}`,
      'state': 'ACTIVE',
      'heroImage': {
        'sourceUri': {
          'uri': 'https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg'
        },
        'contentDescription': {
          'defaultValue': {
            'language': 'en-US',
            'value': 'Hero image description'
          }
        }
      },
      'textModulesData': [
        {
          'header': 'Text module header',
          'body': 'Text module body',
          'id': 'TEXT_MODULE_ID'
        }
      ],
      'linksModuleData': {
        'uris': [
          {
            'uri': 'http://maps.google.com/',
            'description': 'Link module URI description',
            'id': 'LINK_MODULE_URI_ID'
          },
          {
            'uri': 'tel:6505555555',
            'description': 'Link module tel description',
            'id': 'LINK_MODULE_TEL_ID'
          }
        ]
      },
      'imageModulesData': [
        {
          'mainImage': {
            'sourceUri': {
              'uri': 'http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg'
            },
            'contentDescription': {
              'defaultValue': {
                'language': 'en-US',
                'value': 'Image module description'
              }
            }
          },
          'id': 'IMAGE_MODULE_ID'
        }
      ],
      'barcode': {
        'type': 'QR_CODE',
        'value': 'QR code'
      },
      'locations': [
        {
          'latitude': 37.424015499999996,
          'longitude': -122.09259560000001
        }
      ],
      'passengerName': 'Passenger name',
      'boardingAndSeatingInfo': {
        'boardingGroup': 'B',
        'seatNumber': '42'
      },
      'reservationInfo': {
        'confirmationCode': 'Confirmation code'
      }
    };

    // Create the JWT claims
    let claims = {
      iss: this.credentials.client_email,
      aud: 'google',
      origins: ['www.example.com'],
      typ: 'savetowallet',
      payload: {
        // The listed classes and objects will be created
        flightClasses: [newClass],
        flightObjects: [newObject]
      }
    };

    // The service account credentials are used to sign the JWT
    let token = jwt.sign(claims, this.credentials.private_key, { algorithm: 'RS256' });

    console.log('Add to Google Wallet link');
    console.log(`https://pay.google.com/gp/v/save/${token}`);

    return `https://pay.google.com/gp/v/save/${token}`;
  }
  // [END jwtNew]

  // [START jwtExisting]
  /**
   * Generate a signed JWT that references an existing pass object.
   *
   * When the user opens the "Add to Google Wallet" URL and saves the pass to
   * their wallet, the pass objects defined in the JWT are added to the
   * user's Google Wallet app. This allows the user to save multiple pass
   * objects in one API call.
   *
   * The objects to add must follow the below format:
   *
   *  {
   *    'id': 'ISSUER_ID.OBJECT_SUFFIX',
   *    'classId': 'ISSUER_ID.CLASS_SUFFIX'
   *  }
   *
   * @param {string} issuerId The issuer ID being used for this request.
   *
   * @returns {string} An "Add to Google Wallet" link.
   */
  createJwtExistingObjects(issuerId) {
    // Multiple pass types can be added at the same time
    // At least one type must be specified in the JWT claims
    // Note: Make sure to replace the placeholder class and object suffixes
    let objectsToAdd = {
      // Event tickets
      'eventTicketObjects': [{
        'id': `${issuerId}.EVENT_OBJECT_SUFFIX`,
        'classId': `${issuerId}.EVENT_CLASS_SUFFIX`
      }],

      // Boarding passes
      'flightObjects': [{
        'id': `${issuerId}.FLIGHT_OBJECT_SUFFIX`,
        'classId': `${issuerId}.FLIGHT_CLASS_SUFFIX`
      }],

      // Generic passes
      'genericObjects': [{
        'id': `${issuerId}.GENERIC_OBJECT_SUFFIX`,
        'classId': `${issuerId}.GENERIC_CLASS_SUFFIX`
      }],

      // Gift cards
      'giftCardObjects': [{
        'id': `${issuerId}.GIFT_CARD_OBJECT_SUFFIX`,
        'classId': `${issuerId}.GIFT_CARD_CLASS_SUFFIX`
      }],

      // Loyalty cards
      'loyaltyObjects': [{
        'id': `${issuerId}.LOYALTY_OBJECT_SUFFIX`,
        'classId': `${issuerId}.LOYALTY_CLASS_SUFFIX`
      }],

      // Offers
      'offerObjects': [{
        'id': `${issuerId}.OFFER_OBJECT_SUFFIX`,
        'classId': `${issuerId}.OFFER_CLASS_SUFFIX`
      }],

      // Transit passes
      'transitObjects': [{
        'id': `${issuerId}.TRANSIT_OBJECT_SUFFIX`,
        'classId': `${issuerId}.TRANSIT_CLASS_SUFFIX`
      }]
    }

    // Create the JWT claims
    let claims = {
      iss: this.credentials.client_email,
      aud: 'google',
      origins: ['www.example.com'],
      typ: 'savetowallet',
      payload: objectsToAdd
    };

    // The service account credentials are used to sign the JWT
    let token = jwt.sign(claims, this.credentials.private_key, { algorithm: 'RS256' });

    console.log('Add to Google Wallet link');
    console.log(`https://pay.google.com/gp/v/save/${token}`);

    return `https://pay.google.com/gp/v/save/${token}`;
  }
  // [END jwtExisting]

  // [START batch]
  /**
   * Batch create Google Wallet objects from an existing class.
   *
   * @param {string} issuerId The issuer ID being used for this request.
   * @param {string} classSuffix Developer-defined unique ID for this pass class.
   */
  async batchCreateObjects(issuerId, classSuffix) {
    // See below for more information
    // https://cloud.google.com/compute/docs/api/how-tos/batch#example
    let data = '';
    let batchObject;
    let objectSuffix;

    // Example: Generate three new pass objects
    for (let i = 0; i < 3; i++) {
      // Generate a random object suffix
      objectSuffix = uuidv4().replace('[^\w.-]', '_');

      // See link below for more information on required properties
      // https://developers.google.com/wallet/tickets/boarding-passes/rest/v1/flightobject
      batchObject = {
        'id': `${issuerId}.${objectSuffix}`,
        'classId': `${issuerId}.${classSuffix}`,
        'state': 'ACTIVE',
        'heroImage': {
          'sourceUri': {
            'uri': 'https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg'
          },
          'contentDescription': {
            'defaultValue': {
              'language': 'en-US',
              'value': 'Hero image description'
            }
          }
        },
        'textModulesData': [
          {
            'header': 'Text module header',
            'body': 'Text module body',
            'id': 'TEXT_MODULE_ID'
          }
        ],
        'linksModuleData': {
          'uris': [
            {
              'uri': 'http://maps.google.com/',
              'description': 'Link module URI description',
              'id': 'LINK_MODULE_URI_ID'
            },
            {
              'uri': 'tel:6505555555',
              'description': 'Link module tel description',
              'id': 'LINK_MODULE_TEL_ID'
            }
          ]
        },
        'imageModulesData': [
          {
            'mainImage': {
              'sourceUri': {
                'uri': 'http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg'
              },
              'contentDescription': {
                'defaultValue': {
                  'language': 'en-US',
                  'value': 'Image module description'
                }
              }
            },
            'id': 'IMAGE_MODULE_ID'
          }
        ],
        'barcode': {
          'type': 'QR_CODE',
          'value': 'QR code'
        },
        'locations': [
          {
            'latitude': 37.424015499999996,
            'longitude': -122.09259560000001
          }
        ],
        'passengerName': 'Passenger name',
        'boardingAndSeatingInfo': {
          'boardingGroup': 'B',
          'seatNumber': '42'
        },
        'reservationInfo': {
          'confirmationCode': 'Confirmation code'
        }
      };

      data += '--batch_createobjectbatch\n';
      data += 'Content-Type: application/json\n\n';
      data += 'POST /walletobjects/v1/flightObject\n\n';

      data += JSON.stringify(batchObject) + '\n\n';
    }
    data += '--batch_createobjectbatch--';

    // Invoke the batch API calls
    let response = await this.client.context._options.auth.request({
      url: 'https://walletobjects.googleapis.com/batch',
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

module.exports = { DemoFlight };
