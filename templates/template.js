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
  const classId = process.env.WALLET_CLASS_ID || 'test-$object_type-class-id';

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
  const classUrl = 'https://walletobjects.googleapis.com/walletobjects/v1/$object_typeClass/';
  const classPayload = $class_payload;

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
  const objectUrl = 'https://walletobjects.googleapis.com/walletobjects/v1/$object_typeObject/';
  const objectPayload = $object_payload;

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
      $object_typeObjects: [{id: $object_id}],
    },
  };

  const token = jwt.sign(claims, credentials.private_key, {algorithm: 'RS256'});
  const saveUrl = `https://pay.google.com/gp/v/save/${token}`;
  console.log(saveUrl);
  // [END jwt]

};

main().catch(console.error);