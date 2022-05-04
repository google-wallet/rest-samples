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
import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import com.google.api.client.googleapis.auth.oauth2.GoogleCredential;
import okhttp3.*;

import java.io.FileInputStream;
import java.security.interfaces.RSAPrivateKey;
import java.util.*;

public class DemoFlight {
  public static void main(String[] args) throws Exception {

    // Path to service account key file obtained from Google CLoud Console.
    String serviceAccountFile = System.getenv("GOOGLE_APPLICATION_CREDENTIALS");

    // Issuer ID obtained from Google Pay Business Console.
    String issuerId = System.getenv("WALLET_ISSUER_ID");

    // Developer defined ID for the wallet class.
    String classId = System.getenv("WALLET_CLASS_ID");

    // Developer defined ID for the user, eg an email address.
    String userId = System.getenv("WALLET_USER_ID");

    // ID for the wallet object, must be in the form `issuerId.userId` where userId is alphanumeric.
    String objectId = String.format("%s.%s-%s", issuerId, userId.replaceAll("[^\\w.-]", "_"), classId);
    // [END setup]

    ///////////////////////////////////////////////////////////////////////////////
    // Create authenticated HTTP client, using service account file.
    ///////////////////////////////////////////////////////////////////////////////

    // [START auth]
    GoogleCredential credential =
        GoogleCredential.fromStream(new FileInputStream(serviceAccountFile))
            .createScoped(Collections.singleton("https://www.googleapis.com/auth/wallet_object.issuer"));
    credential.refreshToken();
    OkHttpClient httpClient = new OkHttpClient();
    // [END auth]

    ///////////////////////////////////////////////////////////////////////////////
    // Create a class via the API (this can also be done in the business console).
    ///////////////////////////////////////////////////////////////////////////////

    // [START class]
    String classUrl = "https://walletobjects.googleapis.com/walletobjects/v1/flightClass/";
    String classPayload = String.format(
        "{"
      + "  \"id\": \"%s.%s\","
      + "  \"issuerName\": \"test issuer name\","
      + "  \"destination\": {"
      + "    \"airportIataCode\": \"SFO\","
      + "    \"gate\": \"C3\","
      + "    \"terminal\": \"2\""
      + "  },"
      + "  \"flightHeader\": {"
      + "    \"carrier\": {"
      + "      \"carrierIataCode\": \"LX\""
      + "    },"
      + "    \"flightNumber\": \"123\""
      + "  },"
      + "  \"origin\": {"
      + "    \"airportIataCode\": \"LAX\","
      + "    \"gate\": \"A2\","
      + "    \"terminal\": \"1\""
      + "  },"
      + "  \"localScheduledDepartureDateTime\": \"2023-07-02T15:30:00\","
      + "  \"reviewStatus\": \"underReview\""
      + "}", issuerId, classId);

    Request.Builder builder =
        new Request.Builder()
            .url(classUrl)
            .addHeader("Authorization", "Bearer " + credential.getAccessToken());
    builder.method("POST", RequestBody.create(classPayload, MediaType.get("application/json; charset=utf-8")));
    try (Response response = httpClient.newCall(builder.build()).execute()) {
      System.out.println("class POST response:" + Objects.requireNonNull(response.body()).string());
    }
    // [END class]

    ///////////////////////////////////////////////////////////////////////////////
    // Create an object via the API.
    ///////////////////////////////////////////////////////////////////////////////

    // [START object]
    String objectUrl = "https://walletobjects.googleapis.com/walletobjects/v1/flightObject/";
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
      + "  \"state\": \"active\","
      + "  \"passengerName\": \"Test passenger name\","
      + "  \"reservationInfo\": {"
      + "    \"confirmationCode\": \"Test confirmation code\""
      + "  },"
      + "  \"boardingAndSeatingInfo\": {"
      + "    \"seatNumber\": \"42\","
      + "    \"boardingGroup\": \"B\""
      + "  },"
      + "  \"locations\": ["
      + "    {"
      + "      \"kind\": \"walletobjects#latLongPoint\","
      + "      \"latitude\": 37.424015499999996,"
      + "      \"longitude\": -122.09259560000001"
      + "    }"
      + "  ]"
      + "}", objectId, issuerId, classId);
    String output = null;

    builder =
        new Request.Builder()
            .url(objectUrl + objectId)
            .addHeader("Authorization", "Bearer " + credential.getAccessToken())
            .get();
    try (Response response = httpClient.newCall(builder.build()).execute()) {
        if (response.code() != 404) {
            output = Objects.requireNonNull(response.body()).string();
        }
    }
    if (output == null) {
        builder =
            new Request.Builder()
                .url(objectUrl)
                .addHeader("Authorization", "Bearer " + credential.getAccessToken());
        builder.method("POST", RequestBody.create(objectPayload, MediaType.get("application/json; charset=utf-8")));
        try (Response response = httpClient.newCall(builder.build()).execute()) {
          output = Objects.requireNonNull(response.body()).string();
        }
    }
    System.out.println("object GET or POST response: " + output);
    // [END object]

    ///////////////////////////////////////////////////////////////////////////////
    // Create a JWT for the object, and encode it to create a "Save" URL.
    ///////////////////////////////////////////////////////////////////////////////

    // [START jwt]
    Map<String, Object> claims = new HashMap();
    claims.put("iss", credential.getServiceAccountId()); // `client_email` in service account file.
    claims.put("aud", "google");
    claims.put("origins", new ArrayList<>(Arrays.asList("www.example.com")));
    claims.put("typ", "savetowallet");

    Map<String, Object> payload = new HashMap();
    Map<String, String> objectIdMap = new HashMap();
    objectIdMap.put("id", objectId);
    payload.put("flightObjects", new ArrayList<>(Arrays.asList(objectIdMap)));
    claims.put("payload", payload);

    Algorithm algorithm = Algorithm.RSA256(null, (RSAPrivateKey) credential.getServiceAccountPrivateKey());
    String token = JWT.create()
          .withPayload(claims)
          .sign(algorithm);
    String saveUrl = "https://pay.google.com/gp/v/save/" + token;
    System.out.println(saveUrl);
    // [END jwt]

  }
}
