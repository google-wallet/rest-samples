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
import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport;
import com.google.api.client.http.*;
import com.google.api.client.http.json.JsonHttpContent;
import com.google.api.client.json.GenericJson;
import com.google.api.client.json.JsonParser;
import com.google.api.client.json.gson.GsonFactory;
import com.google.auth.http.HttpCredentialsAdapter;
import com.google.auth.oauth2.GoogleCredentials;
import com.google.auth.oauth2.ServiceAccountCredentials;
import com.google.common.collect.Lists;

import java.io.*;
import java.security.interfaces.RSAPrivateKey;
import java.util.*;
// [END imports]

public class DemoTransit {
  public static void main(String[] args) throws Exception {
    /*
     * keyFilePath - Path to service account key file from Google Cloud Console
     * - Environment variable: GOOGLE_APPLICATION_CREDENTIALS
     */
    final String keyFilePath = System.getenv().getOrDefault(
        "GOOGLE_APPLICATION_CREDENTIALS",
        "/path/to/key.json");

    /*
     * issuerId - The issuer ID being updated in this request
     * - Environment variable: WALLET_ISSUER_ID
     */
    String issuerId = System.getenv().getOrDefault(
        "WALLET_ISSUER_ID",
        "issuer-id");

    /*
     * classId - Developer-defined ID for the wallet class
     * - Environment variable: WALLET_CLASS_ID
     */
    String classId = System.getenv().getOrDefault(
        "WALLET_CLASS_ID",
        "test-transit-class-id");

    /*
     * userId - Developer-defined ID for the user, such as an email address
     * - Environment variable: WALLET_USER_ID
     */
    String userId = System.getenv().getOrDefault(
        "WALLET_USER_ID",
        "user-id");

    /*
     * objectId - ID for the wallet object
     * - Format: `issuerId.userId`
     * - Should only include alphanumeric characters, '.', '_', or '-'
     */
    String objectId = String.format("%s.%s-%s", issuerId, userId.replaceAll("[^\\w.-]", "_"), classId);
    // [END setup]

    ///////////////////////////////////////////////////////////////////////////////
    // Create authenticated HTTP client, using service account file.
    ///////////////////////////////////////////////////////////////////////////////

    // [START auth]
    GoogleCredentials credentials = GoogleCredentials.fromStream(new FileInputStream(keyFilePath))
        .createScoped(Lists.newArrayList("https://www.googleapis.com/auth/wallet_object.issuer"));
    credentials.refresh();

    HttpTransport httpTransport = GoogleNetHttpTransport.newTrustedTransport();
    HttpRequestFactory httpRequestFactory = httpTransport.createRequestFactory(new HttpCredentialsAdapter(credentials));
    // [END auth]

    ///////////////////////////////////////////////////////////////////////////////
    // Create a class via the API (this can also be done in the business console).
    ///////////////////////////////////////////////////////////////////////////////

    // [START class]
    GenericUrl classUrl = new GenericUrl("https://walletobjects.googleapis.com/walletobjects/v1/transitClass/");
    String classPayload = String.format(
        "{"
      + "  \"id\": \"%s.%s\","
      + "  \"issuerName\": \"test issuer name\","
      + "  \"reviewStatus\": \"underReview\","
      + "  \"transitType\": \"bus\","
      + "  \"logo\": {"
      + "    \"kind\": \"walletobjects#image\","
      + "    \"sourceUri\": {"
      + "      \"kind\": \"walletobjects#uri\","
      + "      \"uri\": \"https://live.staticflickr.com/65535/48690277162_cd05f03f4d_o.png\","
      + "      \"description\": \"Test logo description\""
      + "    }"
      + "  }"
      + "}", issuerId, classId);

    // Convert body to JSON
    JsonParser classParser = GsonFactory.getDefaultInstance().createJsonParser(classPayload);
    GenericJson classJson = classParser.parseAndClose(GenericJson.class);
    HttpContent classBody = new JsonHttpContent(GsonFactory.getDefaultInstance(), classJson);

    // Create and send the request
    HttpRequest classRequest = httpRequestFactory.buildPostRequest(classUrl, classBody);
    HttpResponse classResponse = classRequest.execute();

    System.out.println("class POST response:" + classResponse.parseAsString());
    // [END class]

    ///////////////////////////////////////////////////////////////////////////////
    // Create an object via the API.
    ///////////////////////////////////////////////////////////////////////////////

    // [START object]
    GenericUrl objectUrl = new GenericUrl(
        "https://walletobjects.googleapis.com/walletobjects/v1/transitObject/" + objectId);
    String objectPayload = String.format(
        "{"
      + "  \"id\": \"%s\","
      + "  \"classId\": \"%s.%s\","
      + "  \"heroImage\": {"
      + "    \"sourceUri\": {"
      + "      \"uri\": \"https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg\","
      + "      \"description\": \"Test heroImage description\""
      + "    }"
      + "  },"
      + "  \"textModulesData\": ["
      + "    {"
      + "      \"header\": \"Test text module header\","
      + "      \"body\": \"Test text module body\""
      + "    }"
      + "  ],"
      + "  \"linksModuleData\": {"
      + "    \"uris\": ["
      + "      {"
      + "        \"kind\": \"walletobjects#uri\","
      + "        \"uri\": \"http://maps.google.com/\","
      + "        \"description\": \"Test link module uri description\""
      + "      },"
      + "      {"
      + "        \"kind\": \"walletobjects#uri\","
      + "        \"uri\": \"tel:6505555555\","
      + "        \"description\": \"Test link module tel description\""
      + "      }"
      + "    ]"
      + "  },"
      + "  \"imageModulesData\": ["
      + "    {"
      + "      \"mainImage\": {"
      + "        \"kind\": \"walletobjects#image\","
      + "        \"sourceUri\": {"
      + "          \"kind\": \"walletobjects#uri\","
      + "          \"uri\": \"http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg\","
      + "          \"description\": \"Test image module description\""
      + "        }"
      + "      }"
      + "    }"
      + "  ],"
      + "  \"barcode\": {"
      + "    \"kind\": \"walletobjects#barcode\","
      + "    \"type\": \"qrCode\","
      + "    \"value\": \"Test QR Code\""
      + "  },"
      + "  \"passengerType\": \"singlePassenger\","
      + "  \"passengerNames\": \"Test passenger names\","
      + "  \"ticketLeg\": {"
      + "    \"originStationCode\": \"LA\","
      + "    \"originName\": {"
      + "      \"kind\": \"walletobjects#localizedString\","
      + "      \"translatedValues\": ["
      + "        {"
      + "          \"kind\": \"walletobjects#translatedString\","
      + "          \"language\": \"en-us\","
      + "          \"value\": \"Test translated origin name\""
      + "        }"
      + "      ],"
      + "      \"defaultValue\": {"
      + "        \"kind\": \"walletobjects#translatedString\","
      + "        \"language\": \"en-us\","
      + "        \"value\": \"Test default origin name\""
      + "      }"
      + "    },"
      + "    \"destinationStationCode\": \"SFO\","
      + "    \"destinationName\": {"
      + "      \"kind\": \"walletobjects#localizedString\","
      + "      \"translatedValues\": ["
      + "        {"
      + "          \"kind\": \"walletobjects#translatedString\","
      + "          \"language\": \"en-us\","
      + "          \"value\": \"Test translated destination name\""
      + "        }"
      + "      ],"
      + "      \"defaultValue\": {"
      + "        \"kind\": \"walletobjects#translatedString\","
      + "        \"language\": \"en-us\","
      + "        \"value\": \"Test default destination name\""
      + "      }"
      + "    },"
      + "    \"departureDateTime\": \"2020-04-12T16:20:50.52Z\","
      + "    \"arrivalDateTime\": \"2020-04-12T20:20:50.52Z\","
      + "    \"fareName\": {"
      + "      \"kind\": \"walletobjects#localizedString\","
      + "      \"translatedValues\": ["
      + "        {"
      + "          \"kind\": \"walletobjects#translatedString\","
      + "          \"language\": \"en-us\","
      + "          \"value\": \"Test translated fare name\""
      + "        }"
      + "      ],"
      + "      \"defaultValue\": {"
      + "        \"kind\": \"walletobjects#translatedString\","
      + "        \"language\": \"en-us\","
      + "        \"value\": \"Test default fare name\""
      + "      }"
      + "    }"
      + "  },"
      + "  \"locations\": ["
      + "    {"
      + "      \"kind\": \"walletobjects#latLongPoint\","
      + "      \"latitude\": 37.424015499999996,"
      + "      \"longitude\": -122.09259560000001"
      + "    }"
      + "  ]"
      + "}", objectId, issuerId, classId);

    // Create and send the request
    HttpRequest objectRequest = httpRequestFactory.buildGetRequest(objectUrl);
    HttpResponse objectResponse = objectRequest.execute();

    if (objectResponse.getStatusCode() == 404) {
      // Object does not yet exist
      // Send POST request to create it
      // Convert body to JSON
      JsonParser objectParser = GsonFactory.getDefaultInstance().createJsonParser(objectPayload);
      GenericJson objectJson = objectParser.parseAndClose(GenericJson.class);
      HttpContent objectBody = new JsonHttpContent(GsonFactory.getDefaultInstance(), objectJson);

      // Create and send the request
      objectRequest = httpRequestFactory.buildPostRequest(objectUrl, objectBody);
      objectResponse = objectRequest.execute();
    }

    System.out.println("object GET or POST response: " + objectResponse.parseAsString());
    // [END object]

    ///////////////////////////////////////////////////////////////////////////////
    // Create a JWT for the object, and encode it to create a "Save" URL.
    ///////////////////////////////////////////////////////////////////////////////

    // [START jwt]
    HashMap<String, String> objectIdMap = new HashMap<String, String>();
    objectIdMap.put("id", objectId);

    HashMap<String, Object> payload = new HashMap<String, Object>();
    payload.put("transitObjects", new ArrayList<>(Arrays.asList(objectIdMap)));

    HashMap<String, Object> claims = new HashMap<String, Object>();
    claims.put("iss", ((ServiceAccountCredentials) credentials).getClientEmail());
    claims.put("aud", "google");
    claims.put("origins", new ArrayList<>(Arrays.asList("www.example.com")));
    claims.put("typ", "savetowallet");
    claims.put("payload", payload);

    Algorithm algorithm = Algorithm.RSA256(
        null,
        (RSAPrivateKey) ((ServiceAccountCredentials) credentials).getPrivateKey());
    String token = JWT.create()
        .withPayload(claims)
        .sign(algorithm);
    String saveUrl = "https://pay.google.com/gp/v/save/" + token;

    System.out.println(saveUrl);
    // [END jwt]

    ///////////////////////////////////////////////////////////////////////////////
    // Create a new Google Wallet issuer account
    ///////////////////////////////////////////////////////////////////////////////

    // [START createIssuer]
    // New issuer name
    final String issuerName = "name";

    // New issuer email address
    final String issuerEmail = "email-address";

    // Issuer API endpoint
    GenericUrl issuerUrl = new GenericUrl("https://walletobjects.googleapis.com/walletobjects/v1/issuer");

    // New issuer information
    HashMap<String, Object> issuerPayload = new HashMap<String, Object>() {
      {
        put("name", issuerName);
        put("contactInfo", new HashMap<String, String>() {
          {
            put("email", issuerEmail);
          }
        });
      }
    };

    HttpRequest issuerRequest = httpRequestFactory.buildPostRequest(
        issuerUrl,
        new JsonHttpContent(GsonFactory.getDefaultInstance(), issuerPayload));
    HttpResponse issuerResponse = issuerRequest.execute();

    System.out.println("issuer POST response: " + issuerResponse.parseAsString());
    // [END createIssuer]

    ///////////////////////////////////////////////////////////////////////////////
    // Update permissions for an existing Google Wallet issuer account
    ///////////////////////////////////////////////////////////////////////////////

    // [START updatePermissions]
    // Permissions API endpoint
    GenericUrl permissionsUrl = new GenericUrl(
        "https://walletobjects.googleapis.com/walletobjects/v1/permissions/" + issuerId);

    ArrayList<HashMap<String, String>> permissions = new ArrayList<>();

    // Copy as needed for each email address that will need access
    permissions.add(new HashMap<String, String>() {
      {
        put("emailAddress", "email-address");
        put("role", "READER | WRITER | OWNER");
      }
    });

    // New issuer permissions information
    HashMap<String, Object> permissionsPayload = new HashMap<String, Object>() {
      {
        put("issuerId", issuerId);
        put("permissions", permissions);
      }
    };

    HttpRequest permissionsRequest = httpRequestFactory.buildPutRequest(
        permissionsUrl,
        new JsonHttpContent(new GsonFactory(), permissionsPayload));
    HttpResponse permissionsResponse = permissionsRequest.execute();

    System.out.println("permissions PUT response: " + permissionsResponse.parseAsString());
    // [END updatePermissions]
  }
}
