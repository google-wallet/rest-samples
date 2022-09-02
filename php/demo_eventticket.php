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

// [START setup]
// [START imports]
use Firebase\JWT\JWT;
use Google\Auth\Credentials\ServiceAccountCredentials;
use Google\Auth\Middleware\AuthTokenMiddleware;
use Google\Client as Google_Client;
use GuzzleHttp\Client;
use GuzzleHttp\HandlerStack;
use GuzzleHttp\Exception\ClientException;
// [END imports]


/*
 * keyFilePath - Path to service account key file from Google Cloud Console
 *             - Environment variable: GOOGLE_APPLICATION_CREDENTIALS
 */
$keyFilePath = getenv('GOOGLE_APPLICATION_CREDENTIALS') ?: '/path/to/key.json';

/*
 * issuerId - The issuer ID being updated in this request
 *          - Environment variable: WALLET_ISSUER_ID
 */
$issuerId = getenv('WALLET_ISSUER_ID') ?: 'issuer-id';

/*
 * classId - Developer-defined ID for the wallet class
 *         - Environment variable: WALLET_CLASS_ID
 */
$classId = getenv('WALLET_CLASS_ID') ?: 'test-eventTicket-class-id';

/*
 * userId - Developer-defined ID for the user, such as an email address
 *        - Environment variable: WALLET_USER_ID
 */
$userId = getenv('WALLET_USER_ID') ?: 'user-id';

/*
 * objectId - ID for the wallet object
 *          - Format: `issuerId.identifier`
 *          - Should only include alphanumeric characters, '.', '_', or '-'
 *          - `identifier` is developer-defined and unique to the user
 */
$objectId = "{$issuerId}." . preg_replace('/[^\w.-]/i', '_', $userId) . "-{$classId}";
// [END setup]

///////////////////////////////////////////////////////////////////////////////
// Create authenticated HTTP client, using service account file.
///////////////////////////////////////////////////////////////////////////////

// [START auth]
$credentials = new ServiceAccountCredentials(
  'https://www.googleapis.com/auth/wallet_object.issuer',
  $keyFilePath
);

$middleware = new AuthTokenMiddleware($credentials);
$stack = HandlerStack::create();
$stack->push($middleware);
$httpClient = new Client([
  'handler' => $stack,
  'auth' => 'google_auth'
]);
// [END auth]

///////////////////////////////////////////////////////////////////////////////
// Create a class via the API (this can also be done in the business console).
///////////////////////////////////////////////////////////////////////////////

// [START class]
$classUrl = "https://walletobjects.googleapis.com/walletobjects/v1/eventTicketClass/";
$classPayload = <<<EOD
{
  "id": "{$issuerId}.{$classId}",
  "issuerName": "test issuer name",
  "eventName": {
    "defaultValue": {
      "language": "en-US",
      "value": "Test event name"
    }
  },
  "reviewStatus": "underReview"
}
EOD;

$classResponse = $httpClient->post(
  $classUrl,
  ['json' => json_decode($classPayload)]
);

echo 'class POST response: ' . $classResponse->getBody();
// [END class]

///////////////////////////////////////////////////////////////////////////////
// Get or create an object via the API.
///////////////////////////////////////////////////////////////////////////////

// [START object]
$objectUrl = "https://walletobjects.googleapis.com/walletobjects/v1/eventTicketObject/";
$objectPayload = <<<EOD
{
  "id": "{$objectId}",
  "classId": "{$issuerId}.{$classId}",
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
}
EOD;

try {
  $objectResponse = $httpClient->get($objectUrl . $objectId);
} catch (ClientException $err) {
  if ($err->getResponse()->getStatusCode() == 404) {
    // Object does not yet exist
    // Send POST request to create it
    $objectResponse = $httpClient->post(
      $objectUrl,
      ['json' => json_decode($objectPayload)]
    );
  }
}

echo 'object GET or POST response: ' . $objectResponse->getBody();
// [END object]

///////////////////////////////////////////////////////////////////////////////
// Create a JWT for the object, and encode it to create a "Save" URL.
///////////////////////////////////////////////////////////////////////////////

// [START jwt]
$serviceAccount = json_decode(file_get_contents($keyFilePath), true);
$claims = [
  'iss' => $serviceAccount['client_email'],
  'aud' => 'google',
  'origins' => ['www.example.com'],
  'typ' => 'savetowallet',
  'payload' => [
    'eventTicketObjects' => [
      ['id' => $objectId]
    ]
  ]
];

$token = JWT::encode($claims, $serviceAccount['private_key'], 'RS256');
$saveUrl = "https://pay.google.com/gp/v/save/${token}";

echo $saveUrl;
// [END jwt]

///////////////////////////////////////////////////////////////////////////////
// Create a new Google Wallet issuer account
///////////////////////////////////////////////////////////////////////////////

// [START createIssuer]
// New issuer name
$issuerName = 'name';

// New issuer email address
$issuerEmail = 'email-address';

// Issuer API endpoint
$issuerUrl = 'https://walletobjects.googleapis.com/walletobjects/v1/issuer';

// New issuer information
$issuerPayload = <<<EOD
{
  "name": $issuerName,
  "contactInfo": {
    "email": $issuerEmail
  }
}
EOD;

$issuerResponse = $httpClient->post(
  $issuerUrl,
  ['json' => json_decode($issuerPayload)]
);

echo 'issuer POST response: ' .  $issuerResponse->getBody();
// [END createIssuer]

///////////////////////////////////////////////////////////////////////////////
// Update permissions for an existing Google Wallet issuer account
///////////////////////////////////////////////////////////////////////////////

// [START updatePermissions]
// Permissions API endpoint
$permissionsUrl = "https://walletobjects.googleapis.com/walletobjects/v1/permissions/{$issuerId}";

// New issuer permissions information
// Copy objects in permissions as needed for each email that will need access
$permissionsPayload = <<<EOD
{
  "issuerId": $issuerId,
  "permissions": [
    {
      "emailAddress": "email-address",
      "role": "READER | WRITER | OWNER"
    },
  ]
}
EOD;

# Make the PUT request
$permissionsResponse = $httpClient->put(
  $permissionsUrl,
  ['json' => json_decode($permissionsPayload)]
);

echo 'permissions PUT response: ' .  $permissionsResponse->getBody();
// [END updatePermissions]

///////////////////////////////////////////////////////////////////////////////
// Batch create Google Wallet objects from an existing class
///////////////////////////////////////////////////////////////////////////////

//[START batch]
// Download the PHP client library from the following URL
// https://developers.google.com/wallet/generic/resources/libraries
require __DIR__ . '/lib/Walletobjects.php';

// The request body will be a multiline string
// See below for more information
// https://cloud.google.com/compute/docs/api/how-tos/batch#example
$client = new Google_Client();
$client->setApplicationName("APPLICATION_NAME");
$client->setScopes("https://www.googleapis.com/auth/wallet_object.issuer");
$client->setAuthConfig($keyFilePath);
$client->setUseBatch(true);

$service = new Google_Service_Walletobjects($client);

$batch = $service->createBatch();

// Example: Generate three new pass objects
for ($i = 0; $i < 3; $i++) {
  // Generate a random user ID
  $userId = str_replace("[^\\w.-]", "_", uniqid());

  // Generate a random object ID with the user ID
  $objectId = "$issuerId.$userId-$classId";

  $eventTicketObject = new Google_Service_Walletobjects_EventTicketObject();
  // See link below for more information on required properties
  // https://developers.google.com/wallet/tickets/events/rest/v1/eventticketobject
  $eventTicketObject->setId($objectId);
  $eventTicketObject->setClassId("$issuerId.$classId");
  $eventTicketObject->setState("ACTIVE");

  $batch->add($service->eventticketobject->insert($eventTicketObject));
}
$results = $batch->execute();

print_r($results);
// [END batch]
