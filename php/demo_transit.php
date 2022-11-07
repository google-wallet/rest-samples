<?php
/*
 * Copyright 2022 Google Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the 'License');
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an 'AS IS' BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

require __DIR__ . '/vendor/autoload.php';

// Download the PHP client library from the following URL
// https://developers.google.com/wallet/generic/resources/libraries
require __DIR__ . '/lib/Walletobjects.php';

// [START setup]
// [START imports]
use Firebase\JWT\JWT;
use Google\Auth\Credentials\ServiceAccountCredentials;
use Google\Client as Google_Client;
// [END imports]

/** Demo class for creating and managing Transit passes in Google Wallet. */
class DemoTransit
{
  /**
   * Path to service account key file from Google Cloud Console. Environment
   * variable: GOOGLE_APPLICATION_CREDENTIALS.
   */
  public string $keyFilePath;

  /**
   * Service account credentials for Google Wallet APIs.
   */
  public ServiceAccountCredentials $credentials;

  /**
   * Google Wallet service client.
   */
  public Google_Service_Walletobjects $service;

  public function __construct()
  {
    $this->keyFilePath = getenv('GOOGLE_APPLICATION_CREDENTIALS') ?: '/path/to/key.json';
  }
  // [END setup]

  // [START auth]
  /**
   * Create authenticated HTTP client using a service account file.
   */
  public function auth()
  {
    $scope = 'https://www.googleapis.com/auth/wallet_object.issuer';

    $this->credentials = new ServiceAccountCredentials(
      $scope,
      $this->keyFilePath
    );

    // Initialize Google Wallet API service
    $this->client = new Google_Client();
    $this->client->setApplicationName('APPLICATION_NAME');
    $this->client->setScopes($scope);
    $this->client->setAuthConfig($this->keyFilePath);

    $this->service = new Google_Service_Walletobjects($this->client);
  }
  // [END auth]

  // [START class]
  /**
   * Create a class via the API. This can also be done in the Google Pay and Wallet console.
   *
   * @param string $issuerId The issuer ID being used for this request.
   * @param string $classSuffix Developer-defined unique ID for this pass class.
   *
   * @return string The pass class ID: "{issuerId}.{classSuffix}"
   */
  public function createTransitClass(string $issuerId, string $classSuffix)
  {
    // See link below for more information on required properties
    // https://developers.google.com/wallet/tickets/transit-passes/qr-code/rest/v1/transitclass
    $transitClass = new Google_Service_Walletobjects_TransitClass(['id' => "{$issuerId}.{$classSuffix}",
      'issuerName' => 'Issuer name',
      'reviewStatus' => 'UNDER_REVIEW',
      'logo' => new Google_Service_Walletobjects_Image([
        'sourceUri' => new Google_Service_Walletobjects_ImageUri([
          'uri' => 'https://live.staticflickr.com/65535/48690277162_cd05f03f4d_o.png',
        ]),
        'contentDescription' => new Google_Service_Walletobjects_LocalizedString([
          'defaultValue' => new Google_Service_Walletobjects_TranslatedString([
            'language' => 'en-US',
            'value' => 'Logo description',
          ]),
        ]),
      ]),
      'transitType' => 'BUS',
    ]);

    try {
      $response = $this->service->transitclass->insert($transitClass);

      print "Class insert response\n";
      print_r($response);

      return $response->id;
    } catch (Google\Service\Exception $ex) {
      if ($ex->getCode() == 409) {
        print "Class {$issuerId}.{$classSuffix} already exists";
        return;
      }

      // Something else went wrong
      print $ex->getTraceAsString();
    }
  }
  // [END class]

  // [START object]
  /**
   * Create an object via the API.
   *
   * @param string $issuerId The issuer ID being used for this request.
   * @param string $classSuffix Developer-defined unique ID for this pass class.
   * @param string $userId Developer-defined user ID for this pass object.
   *
   * @return string The pass object ID: "{issuer_id}.{user_id}"
   */
  public function createTransitObject(string $issuerId, string $classSuffix, string $userId)
  {
    // Generate the object ID
    // Should only include alphanumeric characters, '.', '_', or '-'
    $newUserId = preg_replace('/[^\w.-]/i', '_', $userId);
    $objectId = "{$issuerId}.{$newUserId}";

    // See link below for more information on required properties
    // https://developers.google.com/wallet/tickets/transit-passes/qr-code/rest/v1/transitobject
    $transitObject = new Google_Service_Walletobjects_TransitObject([
      'id' => "{$objectId}",
      'classId' => "{$issuerId}.{$classSuffix}",
      'state' => 'ACTIVE',
      'heroImage' => new Google_Service_Walletobjects_Image([
        'sourceUri' => new Google_Service_Walletobjects_ImageUri([
          'uri' => 'https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg',
        ]),
        'contentDescription' => new Google_Service_Walletobjects_LocalizedString([
          'defaultValue' => new Google_Service_Walletobjects_TranslatedString([
            'language' => 'en-US',
            'value' => 'Hero image description',
          ]),
        ]),
      ]),
      'textModulesData' => [
        new Google_Service_Walletobjects_TextModuleData([
          'header' => 'Text module header',
          'body' => 'Text module body',
          'id' => 'TEXT_MODULE_ID',
        ]),
      ],
      'linksModuleData' => new Google_Service_Walletobjects_LinksModuleData([
        'uris' => [
          new Google_Service_Walletobjects_Uri([
            'uri' => 'http://maps.google.com/',
            'description' => 'Link module URI description',
            'id' => 'LINK_MODULE_URI_ID',
          ]),
          new Google_Service_Walletobjects_Uri([
            'uri' => 'tel:6505555555',
            'description' => 'Link module tel description',
            'id' => 'LINK_MODULE_TEL_ID',
          ]),
        ],
      ]),
      'imageModulesData' => [
        new Google_Service_Walletobjects_ImageModuleData([
          'mainImage' => new Google_Service_Walletobjects_Image([
            'sourceUri' => new Google_Service_Walletobjects_ImageUri([
              'uri' => 'http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg',
            ]),
            'contentDescription' => new Google_Service_Walletobjects_LocalizedString([
              'defaultValue' => new Google_Service_Walletobjects_TranslatedString([
                'language' => 'en-US',
                'value' => 'Image module description',
              ]),
            ]),
          ]),
          'id' => 'IMAGE_MODULE_ID',
        ])
      ],
      'barcode' => new Google_Service_Walletobjects_Barcode([
        'type' => 'QR_CODE',
        'value' => 'QR code value',
      ]),
      'locations' => [
        new Google_Service_Walletobjects_LatLongPoint([
          'latitude' => 37.424015499999996,
          'longitude' =>  -122.09259560000001,
        ]),
      ],
      'passengerType' => 'SINGLE_PASSENGER',
      'passengerNames' => 'Passenger names',
      'tripType' => 'ONE_WAY',
      'ticketLeg' => new Google_Service_Walletobjects_TicketLeg([
        'originStationCode' => 'LA',
        'originName' => new Google_Service_Walletobjects_LocalizedString([
          'defaultValue' => new Google_Service_Walletobjects_TranslatedString([
            'language' => 'en-US',
            'value' => 'Origin name',
          ]),
        ]),
        'destinationStationCode' => 'SFO',
        'destinationName' => new Google_Service_Walletobjects_LocalizedString([
          'defaultValue' => new Google_Service_Walletobjects_TranslatedString([
            'language' => 'en-US',
            'value' => 'Destination name',
          ]),
        ]),
        'departureDateTime' => '2020-04-12T16:20:50.52Z',
        'arrivalDateTime' => '2020-04-12T20:20:50.52Z',
        'fareName' => new Google_Service_Walletobjects_LocalizedString([
          'defaultValue' => new Google_Service_Walletobjects_TranslatedString([
            'language' => 'en-US',
            'value' => 'Fare name',
          ]),
        ]),
      ]),
    ]);

    try {
      $response = $this->service->transitobject->insert($transitObject);

      print "Object insert response\n";
      print_r($response);

      return $response->id;
    } catch (Google\Service\Exception $ex) {
      if ($ex->getCode() == 409) {
        print "Object {$objectId} already exists";
        return;
      }

      // Something else went wrong
      print $ex->getTraceAsString();
    }
  }
  // [END object]

  // [START jwt]
  /**
   * Generate a signed JWT that creates a new pass class and object.
   *
   * When the user opens the "Add to Google Wallet" URL and saves the pass to
   * their wallet, the pass class and object defined in the JWT are
   * created.This allows you to create multiple pass classes and objects in
   * one API call when the user saves the pass to their wallet.
   *
   * @param string $issuerId The issuer ID being used for this request.
   * @param string $classSuffix Developer-defined unique ID for this pass class.
   * @param string $userId Developer-defined user ID for this object.
   *
   * @return string An "Add to Google Wallet" link.
   */
  public function createJwtSaveUrl(string $issuerId, string $classSuffix, string $userId)
  {
    // Generate the object ID
    // Should only include alphanumeric characters, '.', '_', or '-'
    $newUserId = preg_replace('/[^\w.-]/i', '_', $userId);
    $objectId = "{$issuerId}.{$newUserId}";

    // See link below for more information on required properties
    // https://developers.google.com/wallet/tickets/transit-passes/qr-code/rest/v1/transitclass
    $transitClass = new Google_Service_Walletobjects_TransitClass(['id' => "{$issuerId}.{$classSuffix}",
      'issuerName' => 'Issuer name',
      'reviewStatus' => 'UNDER_REVIEW',
      'logo' => new Google_Service_Walletobjects_Image([
        'sourceUri' => new Google_Service_Walletobjects_ImageUri([
          'uri' => 'https://live.staticflickr.com/65535/48690277162_cd05f03f4d_o.png',
        ]),
        'contentDescription' => new Google_Service_Walletobjects_LocalizedString([
          'defaultValue' => new Google_Service_Walletobjects_TranslatedString([
            'language' => 'en-US',
            'value' => 'Logo description',
          ]),
        ]),
      ]),
      'transitType' => 'BUS',
    ]);

    // See link below for more information on required properties
    // https://developers.google.com/wallet/tickets/transit-passes/qr-code/rest/v1/transitobject
    $transitObject = new Google_Service_Walletobjects_TransitObject([
      'id' => "{$objectId}",
      'classId' => "{$issuerId}.{$classSuffix}",
      'state' => 'ACTIVE',
      'heroImage' => new Google_Service_Walletobjects_Image([
        'sourceUri' => new Google_Service_Walletobjects_ImageUri([
          'uri' => 'https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg',
        ]),
        'contentDescription' => new Google_Service_Walletobjects_LocalizedString([
          'defaultValue' => new Google_Service_Walletobjects_TranslatedString([
            'language' => 'en-US',
            'value' => 'Hero image description',
          ]),
        ]),
      ]),
      'textModulesData' => [
        new Google_Service_Walletobjects_TextModuleData([
          'header' => 'Text module header',
          'body' => 'Text module body',
          'id' => 'TEXT_MODULE_ID',
        ]),
      ],
      'linksModuleData' => new Google_Service_Walletobjects_LinksModuleData([
        'uris' => [
          new Google_Service_Walletobjects_Uri([
            'uri' => 'http://maps.google.com/',
            'description' => 'Link module URI description',
            'id' => 'LINK_MODULE_URI_ID',
          ]),
          new Google_Service_Walletobjects_Uri([
            'uri' => 'tel:6505555555',
            'description' => 'Link module tel description',
            'id' => 'LINK_MODULE_TEL_ID',
          ]),
        ],
      ]),
      'imageModulesData' => [
        new Google_Service_Walletobjects_ImageModuleData([
          'mainImage' => new Google_Service_Walletobjects_Image([
            'sourceUri' => new Google_Service_Walletobjects_ImageUri([
              'uri' => 'http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg',
            ]),
            'contentDescription' => new Google_Service_Walletobjects_LocalizedString([
              'defaultValue' => new Google_Service_Walletobjects_TranslatedString([
                'language' => 'en-US',
                'value' => 'Image module description',
              ]),
            ]),
          ]),
          'id' => 'IMAGE_MODULE_ID',
        ])
      ],
      'barcode' => new Google_Service_Walletobjects_Barcode([
        'type' => 'QR_CODE',
        'value' => 'QR code value',
      ]),
      'locations' => [
        new Google_Service_Walletobjects_LatLongPoint([
          'latitude' => 37.424015499999996,
          'longitude' =>  -122.09259560000001,
        ]),
      ],
      'passengerType' => 'SINGLE_PASSENGER',
      'passengerNames' => 'Passenger names',
      'tripType' => 'ONE_WAY',
      'ticketLeg' => new Google_Service_Walletobjects_TicketLeg([
        'originStationCode' => 'LA',
        'originName' => new Google_Service_Walletobjects_LocalizedString([
          'defaultValue' => new Google_Service_Walletobjects_TranslatedString([
            'language' => 'en-US',
            'value' => 'Origin name',
          ]),
        ]),
        'destinationStationCode' => 'SFO',
        'destinationName' => new Google_Service_Walletobjects_LocalizedString([
          'defaultValue' => new Google_Service_Walletobjects_TranslatedString([
            'language' => 'en-US',
            'value' => 'Destination name',
          ]),
        ]),
        'departureDateTime' => '2020-04-12T16:20:50.52Z',
        'arrivalDateTime' => '2020-04-12T20:20:50.52Z',
        'fareName' => new Google_Service_Walletobjects_LocalizedString([
          'defaultValue' => new Google_Service_Walletobjects_TranslatedString([
            'language' => 'en-US',
            'value' => 'Fare name',
          ]),
        ]),
      ]),
    ]);

    // Create the JWT as an array of key/value pairs
    $serviceAccount = json_decode(file_get_contents($this->keyFilePath), true);
    $claims = [
      'iss' => $serviceAccount['client_email'],
      'aud' => 'google',
      'origins' => ['www.example.com'],
      'typ' => 'savetowallet',
      'payload' => [
        'transitClasses' => [
          $transitClass,
        ],
        'transitObjects' => [
          $transitObject,
        ],
      ],
    ];

    // The service account credentials are used to sign the JWT
    $token = JWT::encode(
      $claims,
      $serviceAccount['private_key'],
      'RS256'
    );

    print "Add to Google Wallet link\n";
    print "https://pay.google.com/gp/v/save/{$token}";

    return "https://pay.google.com/gp/v/save/{$token}";
  }
  // [END jwt]

  // [START createIssuer]
  /**
   * Create a new Google Wallet issuer account.
   *
   * @param string $issuerName The issuer's name.
   * @param string $issuerEmail The issuer's email address.
   */
  public function createIssuerAccount(string $issuerName, string $issuerEmail)
  {
    // New issuer information
    $issuer = new Google_Service_Walletobjects_Issuer([
      'name' => $issuerName,
      'contactInfo' => new Google_Service_Walletobjects_IssuerContactInfo([
        'email' => $issuerEmail,
      ]),
    ]);

    $response = $this->service->issuer->insert($issuer);

    print "Issuer insert response\n";
    print_r($response);
  }
  // [END createIssuer]

  // [START updatePermissions]
  /**
   * Update permissions for an existing Google Wallet issuer account.
   * **Warning:** This operation overwrites all existing permissions!
   *
   * Example permissions list argument below. Copy the entry as
   * needed for each email address that will need access. Supported
   * values for role are: 'READER', 'WRITER', and 'OWNER'
   *
   * $permissions = array(
   *  new Google_Service_Walletobjects_Permission([
   *    'emailAddress' => 'email-address',
   *    'role' => 'OWNER',
   *  ]),
   * );
   *
   * @param string $issuerId The issuer ID being used for this request.
   * @param array $permissions The list of email addresses and roles to assign.
   */
  public function updateIssuerAccountPermissions(string $issuerId, array $permissions)
  {
    // Make the PUT request
    $response = $this->service->permissions->update(
      $issuerId,
      new Google_Service_Walletobjects_Permissions([
        'issuerId' => $issuerId,
        'permissions' => $permissions,
      ])
    );

    print "Permissions update response\n";
    print_r($response);
  }
  // [END updatePermissions]

  // [START batch]
  /**
   * Batch create Google Wallet objects from an existing class.
   *
   * @param string $issuerId The issuer ID being used for this request.
   * @param string $classSuffix Developer-defined unique ID for this pass class.
   */
  public function batchCreateTransitObjects(string $issuerId, string $classSuffix)
  {
    // Update the client to enable batch requests
    $this->client->setUseBatch(true);
    $batch = $this->service->createBatch();

    // Example: Generate three new pass objects
    for ($i = 0; $i < 3; $i++) {
      // Generate a random user ID
      $userId = preg_replace('/[^\w.-]/i', '_', uniqid());

      // Generate a random object ID with the user ID
      // Should only include alphanumeric characters, '.', '_', or '-'
      $objectId = "{$issuerId}.{$userId}";

      // See link below for more information on required properties
      // https://developers.google.com/wallet/tickets/transit-passes/qr-code/rest/v1/transitobject
      $transitObject = new Google_Service_Walletobjects_TransitObject([
        'id' => "{$objectId}",
        'classId' => "{$issuerId}.{$classSuffix}",
        'state' => 'ACTIVE',
        'heroImage' => new Google_Service_Walletobjects_Image([
          'sourceUri' => new Google_Service_Walletobjects_ImageUri([
            'uri' => 'https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg',
          ]),
          'contentDescription' => new Google_Service_Walletobjects_LocalizedString([
            'defaultValue' => new Google_Service_Walletobjects_TranslatedString([
              'language' => 'en-US',
              'value' => 'Hero image description',
            ]),
          ]),
        ]),
        'textModulesData' => [
          new Google_Service_Walletobjects_TextModuleData([
            'header' => 'Text module header',
            'body' => 'Text module body',
            'id' => 'TEXT_MODULE_ID',
          ]),
        ],
        'linksModuleData' => new Google_Service_Walletobjects_LinksModuleData([
          'uris' => [
            new Google_Service_Walletobjects_Uri([
              'uri' => 'http://maps.google.com/',
              'description' => 'Link module URI description',
              'id' => 'LINK_MODULE_URI_ID',
            ]),
            new Google_Service_Walletobjects_Uri([
              'uri' => 'tel:6505555555',
              'description' => 'Link module tel description',
              'id' => 'LINK_MODULE_TEL_ID',
            ]),
          ],
        ]),
        'imageModulesData' => [
          new Google_Service_Walletobjects_ImageModuleData([
            'mainImage' => new Google_Service_Walletobjects_Image([
              'sourceUri' => new Google_Service_Walletobjects_ImageUri([
                'uri' => 'http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg',
              ]),
              'contentDescription' => new Google_Service_Walletobjects_LocalizedString([
                  'defaultValue' => new Google_Service_Walletobjects_TranslatedString([
                    'language' => 'en-US',
                    'value' => 'Image module description',
                  ]),
                ]),
            ]),
            'id' => 'IMAGE_MODULE_ID',
          ])
        ],
        'barcode' => new Google_Service_Walletobjects_Barcode([
          'type' => 'QR_CODE',
          'value' => 'QR code value',
        ]),
        'locations' => [
          new Google_Service_Walletobjects_LatLongPoint([
            'latitude' => 37.424015499999996,
            'longitude' =>  -122.09259560000001,
          ]),
        ],
        'passengerType' => 'SINGLE_PASSENGER',
        'passengerNames' => 'Passenger names',
        'tripType' => 'ONE_WAY',
        'ticketLeg' => new Google_Service_Walletobjects_TicketLeg([
          'originStationCode' => 'LA',
          'originName' => new Google_Service_Walletobjects_LocalizedString([
            'defaultValue' => new Google_Service_Walletobjects_TranslatedString([
              'language' => 'en-US',
              'value' => 'Origin name',
            ]),
          ]),
          'destinationStationCode' => 'SFO',
          'destinationName' => new Google_Service_Walletobjects_LocalizedString([
            'defaultValue' => new Google_Service_Walletobjects_TranslatedString([
              'language' => 'en-US',
              'value' => 'Destination name',
            ]),
          ]),
          'departureDateTime' => '2020-04-12T16:20:50.52Z',
          'arrivalDateTime' => '2020-04-12T20:20:50.52Z',
          'fareName' => new Google_Service_Walletobjects_LocalizedString([
            'defaultValue' => new Google_Service_Walletobjects_TranslatedString([
              'language' => 'en-US',
              'value' => 'Fare name',
            ]),
          ]),
        ]),
      ]);

      $batch->add($this->service->transitobject->insert($transitObject));
    }

    // Make the batch request
    $batchResponse = $batch->execute();

    print "Batch insert response\n";
    foreach ($batchResponse as $key => $value) {
      if ($value instanceof Google_Service_Exception) {
        print_r($value->getErrors());
        continue;
      }
      print "{$value->getId()}\n";
    }
  }
  // [END batch]
}
