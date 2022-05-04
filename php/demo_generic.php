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
use Firebase\JWT\JWT;
use Google\Auth\Credentials\ServiceAccountCredentials;
use Google\Auth\Middleware\AuthTokenMiddleware;
use GuzzleHttp\Client;
use GuzzleHttp\HandlerStack;
use GuzzleHttp\Exception\ClientException;

// Path to service account key file obtained from Google CLoud Console.
$serviceAccountFile = getenv('GOOGLE_APPLICATION_CREDENTIALS') ?: '/path/to/key.json';

// Issuer ID obtained from Google Pay Business Console.
$issuerId = getenv('WALLET_ISSUER_ID') ?: '<issuer ID>';

// Developer defined ID for the wallet class.
$classId = getenv('WALLET_CLASS_ID') ?: "test-generic-class-id";

// Developer defined ID for the user, eg an email address.
$userId = getenv('WALLET_USER_ID') ?: 'test@example.com';

// ID for the wallet object, must be in the form `issuer_id.user_id` where user_id is alphanumeric.
$objectId = "{$issuerId}." . preg_replace('/[^\w.-]/i', '_', $userId) . "-{$classId}";
// [END setup]

///////////////////////////////////////////////////////////////////////////////
// Create authenticated HTTP client, using service account file.
///////////////////////////////////////////////////////////////////////////////

// [START auth]
$credentials = new ServiceAccountCredentials('https://www.googleapis.com/auth/wallet_object.issuer', $serviceAccountFile);
$middleware = new AuthTokenMiddleware($credentials); 
$stack = HandlerStack::create();
$stack->push($middleware);
$httpClient = new Client(['handler' => $stack, 'auth' => 'google_auth']);
// [END auth]

///////////////////////////////////////////////////////////////////////////////
// Create a class via the API (this can also be done in the business console).
///////////////////////////////////////////////////////////////////////////////

// [START class]
$classUrl = "https://walletobjects.googleapis.com/walletobjects/v1/genericClass/";
$classPayload = <<<EOD
{
  "id": "{$issuerId}.{$classId}",
  "issuerName": "test issuer name"
}
EOD;

try {
	$classResponse = $httpClient->post($classUrl, ['json' => json_decode($classPayload)]);
} catch (ClientException $e) {
  $classResponse = $e->getResponse();
}
echo "class POST response: " . $classResponse->getBody();
// [END class]

///////////////////////////////////////////////////////////////////////////////
// Get or create an object via the API.
///////////////////////////////////////////////////////////////////////////////

// [START object]
$objectUrl = "https://walletobjects.googleapis.com/walletobjects/v1/genericObject/";
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
  "genericType": "GENERIC_TYPE_UNSPECIFIED",
  "hexBackgroundColor": "#4285f4",
  "logo": {
    "sourceUri": {
      "uri": "https://storage.googleapis.com/wallet-lab-tools-codelab-artifacts-public/pass_google_logo.jpg"
    }
  },
  "cardTitle": {
    "defaultValue": {
      "language": "en-US",
      "value": "Testing Generic Title"
    }
  },
  "header": {
    "defaultValue": {
      "language": "en-US",
      "value": "Testing Generic Header"
    }
  },
  "subheader": {
    "defaultValue": {
      "language": "en",
      "value": "Testing Generic Sub Header"
    }
  }
}
EOD;

// Retrieve the object, or create it if it doesn't exist.
try {
  $objectResponse = $httpClient->get($objectUrl . $objectId);
} catch (ClientException $e) {
  $objectResponse = $e->getResponse();
  if ($objectResponse->getStatusCode() == 404) {
    $objectResponse = $httpClient->post($objectUrl, ['json' => json_decode($objectPayload)]);
  }
}
echo "object GET or POST response: " . $objectResponse->getBody();
// [END object]

///////////////////////////////////////////////////////////////////////////////
// Create a JWT for the object, and encode it to create a "Save" URL.
///////////////////////////////////////////////////////////////////////////////

// [START jwt]
$serviceAccount = json_decode(file_get_contents($serviceAccountFile), true);
$claims = [
  'iss' => $serviceAccount['client_email'],
  'aud' => 'google',
  'origins' => ['www.example.com'],
  'typ' => 'savetowallet',
  'payload' => ['genericObjects' => [['id' => $objectId]]]
];

$token = JWT::encode($claims, $serviceAccount['private_key'], 'RS256');
$saveUrl = "https://pay.google.com/gp/v/save/${token}";
echo $saveUrl;
// [END jwt]
