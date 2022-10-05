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
import com.google.api.client.googleapis.batch.BatchRequest;
import com.google.api.client.googleapis.batch.json.JsonBatchCallback;
import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport;
import com.google.api.client.googleapis.json.GoogleJsonError;
import com.google.api.client.googleapis.json.GoogleJsonResponseException;
import com.google.api.client.http.*;
import com.google.api.client.json.gson.GsonFactory;
import com.google.api.services.walletobjects.Walletobjects;
import com.google.api.services.walletobjects.model.*;
import com.google.auth.http.HttpCredentialsAdapter;
import com.google.auth.oauth2.GoogleCredentials;
import com.google.auth.oauth2.ServiceAccountCredentials;
import java.io.*;
import java.security.interfaces.RSAPrivateKey;
import java.util.*;
// [END imports]

/** Demo class for creating and managing Loyalty cards in Google Wallet. */
public class DemoLoyalty {
  /**
   * Path to service account key file from Google Cloud Console. Environment variable:
   * GOOGLE_APPLICATION_CREDENTIALS.
   */
  public static String keyFilePath;

  /** Service account credentials for Google Wallet APIs. */
  public static GoogleCredentials credentials;

  /** Google Wallet service client. */
  public static Walletobjects service;

  public DemoLoyalty() {
    keyFilePath =
        System.getenv().getOrDefault("GOOGLE_APPLICATION_CREDENTIALS", "/path/to/key.json");
  }
  // [END setup]

  // [START auth]
  /**
   * Create authenticated HTTP client using a service account file.
   *
   * @throws Exception
   */
  public void Auth() throws Exception {
    String scope = "https://www.googleapis.com/auth/wallet_object.issuer";

    credentials =
        GoogleCredentials.fromStream(new FileInputStream(keyFilePath))
            .createScoped(Arrays.asList(scope));
    credentials.refresh();

    HttpTransport httpTransport = GoogleNetHttpTransport.newTrustedTransport();

    service =
        new Walletobjects.Builder(
                httpTransport,
                GsonFactory.getDefaultInstance(),
                new HttpCredentialsAdapter(credentials))
            .setApplicationName("APPLICATION_NAME")
            .build();
  }
  // [END auth]

  // [START class]
  /**
   * Create a class via the API. This can also be done in the Google Pay and Wallet console.
   *
   * @param issuerId The issuer ID being used for this request.
   * @param classSuffix Developer-defined unique ID for this pass class.
   * @return The pass class ID: "{issuerId}.{classSuffix}"
   * @throws IOException
   */
  public String CreateLoyaltyClass(String issuerId, String classSuffix) throws IOException {
    // See link below for more information on required properties
    // https://developers.google.com/wallet/retail/loyalty-cards/rest/v1/loyaltyclass
    LoyaltyClass loyaltyClass =
        new LoyaltyClass()
            .setId(String.format("%s.%s", issuerId, classSuffix))
            .setIssuerName("Issuer name")
            .setReviewStatus("UNDER_REVIEW")
            .setProgramName("Program name")
            .setProgramLogo(
                new Image()
                    .setSourceUri(
                        new ImageUri()
                            .setUri(
                                "https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg"))
                    .setContentDescription(
                        new LocalizedString()
                            .setDefaultValue(
                                new TranslatedString()
                                    .setLanguage("en-US")
                                    .setValue("Logo description"))));

    try {
      LoyaltyClass response = service.loyaltyclass().insert(loyaltyClass).execute();

      System.out.println("Class insert response");
      System.out.println(response.toPrettyString());

      return response.getId();
    } catch (GoogleJsonResponseException ex) {
      if (ex.getStatusCode() == 409) {
        System.out.println(String.format("Class %s.%s already exists", issuerId, classSuffix));
        return String.format("%s.%s", issuerId, classSuffix);
      }

      // Something else went wrong
      ex.printStackTrace();
      return ex.getMessage();
    }
  }
  // [END class]

  // [START object]
  /**
   * Create an object via the API.
   *
   * @param issuerId The issuer ID being used for this request.
   * @param classSuffix Developer-defined unique ID for this pass class.
   * @param userId Developer-defined user ID for this object.
   * @return The pass object ID: "{issuerId}.{userId}"
   * @throws IOException
   */
  public String CreateLoyaltyObject(String issuerId, String classSuffix, String userId)
      throws IOException {
    // Generate the object ID
    // Should only include alphanumeric characters, '.', '_', or '-'
    String newUserId = userId.replaceAll("[^\\w.-]", "_");
    String objectId = String.format("%s.%s", issuerId, newUserId);

    try {
      // Check if the object exists
      LoyaltyObject response = service.loyaltyobject().get(objectId).execute();

      System.out.println("Object get response");
      System.out.println(response.toPrettyString());

      return response.getId();
    } catch (GoogleJsonResponseException ex) {
      if (ex.getStatusCode() != 404) {
        // Something else went wrong
        ex.printStackTrace();
        return ex.getMessage();
      }
    }

    // Object doesn't exist, create it now
    // See link below for more information on required properties
    // https://developers.google.com/wallet/retail/loyalty-cards/rest/v1/loyaltyobject
    LoyaltyObject loyaltyObject =
        new LoyaltyObject()
            .setId(objectId)
            .setClassId(String.format("%s.%s", issuerId, classSuffix))
            .setState("ACTIVE")
            .setHeroImage(
                new Image()
                    .setSourceUri(
                        new ImageUri()
                            .setUri(
                                "https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg"))
                    .setContentDescription(
                        new LocalizedString()
                            .setDefaultValue(
                                new TranslatedString()
                                    .setLanguage("en-US")
                                    .setValue("Hero image description"))))
            .setTextModulesData(
                Arrays.asList(
                    new TextModuleData()
                        .setHeader("Text module header")
                        .setBody("Text module body")
                        .setId("TEXT_MODULE_ID")))
            .setLinksModuleData(
                new LinksModuleData()
                    .setUris(
                        Arrays.asList(
                            new Uri()
                                .setUri("http://maps.google.com/")
                                .setDescription("Link module URI description")
                                .setId("LINK_MODULE_URI_ID"),
                            new Uri()
                                .setUri("tel:6505555555")
                                .setDescription("Link module tel description")
                                .setId("LINK_MODULE_TEL_ID"))))
            .setImageModulesData(
                Arrays.asList(
                    new ImageModuleData()
                        .setMainImage(
                            new Image()
                                .setSourceUri(
                                    new ImageUri()
                                        .setUri(
                                            "http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg"))
                                .setContentDescription(
                                    new LocalizedString()
                                        .setDefaultValue(
                                            new TranslatedString()
                                                .setLanguage("en-US")
                                                .setValue("Image module description"))))
                        .setId("IMAGE_MODULE_ID")))
            .setBarcode(new Barcode().setType("QR_CODE").setValue("QR code value"))
            .setLocations(
                Arrays.asList(
                    new LatLongPoint()
                        .setLatitude(37.424015499999996)
                        .setLongitude(-122.09259560000001)))
            .setAccountId("Account ID")
            .setAccountName("Account name")
            .setLoyaltyPoints(
                new LoyaltyPoints()
                    .setLabel("Points")
                    .setBalance(new LoyaltyPointsBalance().setInt(800)));

    LoyaltyObject response = service.loyaltyobject().insert(loyaltyObject).execute();

    System.out.println("Object insert response");
    System.out.println(response.toPrettyString());

    return response.getId();
  }
  // [END object]

  // [START jwt]
  /**
   * Generate a signed JWT that creates a new pass class and object.
   *
   * <p>When the user opens the "Add to Google Wallet" URL and saves the pass to their wallet, the
   * pass class and object defined in the JWT are created. This allows you to create multiple pass
   * classes and objects in one API call when the user saves the pass to their wallet.
   *
   * @param issuerId The issuer ID being used for this request.
   * @param classSuffix Developer-defined unique ID for this pass class.
   * @param userId Developer-defined user ID for this object.
   * @return An "Add to Google Wallet" link.
   */
  public String CreateJWTSaveURL(String issuerId, String classSuffix, String userId) {
    // Generate the object ID
    // Should only include alphanumeric characters, '.', '_', or '-'
    String newUserId = userId.replaceAll("[^\\w.-]", "_");
    String objectId = String.format("%s.%s", issuerId, newUserId);

    // See link below for more information on required properties
    // https://developers.google.com/wallet/retail/loyalty-cards/rest/v1/loyaltyclass
    LoyaltyClass loyaltyClass =
        new LoyaltyClass()
            .setId(String.format("%s.%s", issuerId, classSuffix))
            .setIssuerName("Issuer name")
            .setReviewStatus("UNDER_REVIEW")
            .setProgramName("Program name")
            .setProgramLogo(
                new Image()
                    .setSourceUri(
                        new ImageUri()
                            .setUri(
                                "https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg"))
                    .setContentDescription(
                        new LocalizedString()
                            .setDefaultValue(
                                new TranslatedString()
                                    .setLanguage("en-US")
                                    .setValue("Logo description"))));

    // See link below for more information on required properties
    // https://developers.google.com/wallet/retail/loyalty-cards/rest/v1/loyaltyobject
    LoyaltyObject loyaltyObject =
        new LoyaltyObject()
            .setId(objectId)
            .setClassId(String.format("%s.%s", issuerId, classSuffix))
            .setState("ACTIVE")
            .setHeroImage(
                new Image()
                    .setSourceUri(
                        new ImageUri()
                            .setUri(
                                "https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg"))
                    .setContentDescription(
                        new LocalizedString()
                            .setDefaultValue(
                                new TranslatedString()
                                    .setLanguage("en-US")
                                    .setValue("Hero image description"))))
            .setTextModulesData(
                Arrays.asList(
                    new TextModuleData()
                        .setHeader("Text module header")
                        .setBody("Text module body")
                        .setId("TEXT_MODULE_ID")))
            .setLinksModuleData(
                new LinksModuleData()
                    .setUris(
                        Arrays.asList(
                            new Uri()
                                .setUri("http://maps.google.com/")
                                .setDescription("Link module URI description")
                                .setId("LINK_MODULE_URI_ID"),
                            new Uri()
                                .setUri("tel:6505555555")
                                .setDescription("Link module tel description")
                                .setId("LINK_MODULE_TEL_ID"))))
            .setImageModulesData(
                Arrays.asList(
                    new ImageModuleData()
                        .setMainImage(
                            new Image()
                                .setSourceUri(
                                    new ImageUri()
                                        .setUri(
                                            "http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg"))
                                .setContentDescription(
                                    new LocalizedString()
                                        .setDefaultValue(
                                            new TranslatedString()
                                                .setLanguage("en-US")
                                                .setValue("Image module description"))))
                        .setId("IMAGE_MODULE_ID")))
            .setBarcode(new Barcode().setType("QR_CODE").setValue("QR code value"))
            .setLocations(
                Arrays.asList(
                    new LatLongPoint()
                        .setLatitude(37.424015499999996)
                        .setLongitude(-122.09259560000001)))
            .setAccountId("Account ID")
            .setAccountName("Account name")
            .setLoyaltyPoints(
                new LoyaltyPoints()
                    .setLabel("Points")
                    .setBalance(new LoyaltyPointsBalance().setInt(800)));

    // Create the JWT as a HashMap object
    HashMap<String, Object> claims = new HashMap<String, Object>();
    claims.put("iss", ((ServiceAccountCredentials) credentials).getClientEmail());
    claims.put("aud", "google");
    claims.put("origins", Arrays.asList("www.example.com"));
    claims.put("typ", "savetowallet");

    // Create the Google Wallet payload and add to the JWT
    HashMap<String, Object> payload = new HashMap<String, Object>();
    payload.put("loyaltyClasses", Arrays.asList(loyaltyClass));
    payload.put("loyaltyObjects", Arrays.asList(loyaltyObject));
    claims.put("payload", payload);

    // The service account credentials are used to sign the JWT
    Algorithm algorithm =
        Algorithm.RSA256(
            null, (RSAPrivateKey) ((ServiceAccountCredentials) credentials).getPrivateKey());
    String token = JWT.create().withPayload(claims).sign(algorithm);

    System.out.println("Add to Google Wallet link");
    System.out.println(String.format("https://pay.google.com/gp/v/save/%s", token));

    return String.format("https://pay.google.com/gp/v/save/%s", token);
  }
  // [END jwt]

  // [START createIssuer]
  /**
   * Create a new Google Wallet issuer account.
   *
   * @param issuerName The issuer's name.
   * @param issuerEmail The issuer's email address.
   * @throws IOException
   */
  public void CreateIssuerAccount(String issuerName, String issuerEmail) throws IOException {
    // New issuer information
    Issuer issuer =
        new Issuer()
            .setName(issuerName)
            .setContactInfo(new IssuerContactInfo().setEmail(issuerEmail));

    Issuer response = service.issuer().insert(issuer).execute();

    System.out.println("Issuer insert response");
    System.out.println(response.toPrettyString());
  }
  // [END createIssuer]

  // [START updatePermissions]
  /**
   * Update permissions for an existing Google Wallet issuer account. <strong>Warning:</strong> This
   * operation overwrites all existing permissions!
   *
   * <p>Example permissions list argument below. Copy the add entry as needed for each email address
   * that will need access. Supported values for role are: 'READER', 'WRITER', and 'OWNER'
   *
   * <pre><code>
   * ArrayList<Permission> permissions = new ArrayList<Permission>();
   * permissions.add(new Permission().setEmailAddress("emailAddress").setRole("OWNER"));
   * </code></pre>
   *
   * @param issuerId The issuer ID being used for this request.
   * @param permissions The list of email addresses and roles to assign.
   * @throws IOException
   */
  public void UpdateIssuerAccountPermissions(String issuerId, ArrayList<Permission> permissions)
      throws IOException {

    Permissions response =
        service
            .permissions()
            .update(
                Long.parseLong(issuerId),
                new Permissions().setIssuerId(Long.parseLong(issuerId)).setPermissions(permissions))
            .execute();

    System.out.println("Issuer permissions update response");
    System.out.println(response.toPrettyString());
  }
  // [END updatePermissions]

  // [START batch]
  /**
   * Batch create Google Wallet objects from an existing class.
   *
   * @param issuerId The issuer ID being used for this request.
   * @param classSuffix Developer-defined unique ID for this pass class.
   * @throws IOException
   */
  public void BatchCreateLoyaltyObjects(String issuerId, String classSuffix) throws IOException {
    // Create the batch request client
    BatchRequest batch = service.batch(new HttpCredentialsAdapter(credentials));

    // The callback will be invoked for each request in the batch
    JsonBatchCallback<LoyaltyObject> callback =
        new JsonBatchCallback<LoyaltyObject>() {
          // Invoked if the request was successful
          public void onSuccess(LoyaltyObject response, HttpHeaders responseHeaders) {
            System.out.println(response.toString());
          }

          // Invoked if the request failed
          public void onFailure(GoogleJsonError e, HttpHeaders responseHeaders) {
            System.out.println("Error Message: " + e.getMessage());
          }
        };

    // Example: Generate three new pass objects
    for (int i = 0; i < 3; i++) {
      // Generate a random user ID
      String userId = UUID.randomUUID().toString().replaceAll("[^\\w.-]", "_");

      // Generate a random object ID with the user ID
      // Should only include alphanumeric characters, '.', '_', or '-'
      String objectId = String.format("%s.%s", issuerId, userId);

      // See link below for more information on required properties
      // https://developers.google.com/wallet/retail/loyalty-cards/rest/v1/loyaltyobject
      LoyaltyObject loyaltyObject =
          new LoyaltyObject()
              .setId(objectId)
              .setClassId(String.format("%s.%s", issuerId, classSuffix))
              .setState("ACTIVE")
              .setHeroImage(
                  new Image()
                      .setSourceUri(
                          new ImageUri()
                              .setUri(
                                  "https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg"))
                      .setContentDescription(
                          new LocalizedString()
                              .setDefaultValue(
                                  new TranslatedString()
                                      .setLanguage("en-US")
                                      .setValue("Hero image description"))))
              .setTextModulesData(
                  Arrays.asList(
                      new TextModuleData()
                          .setHeader("Text module header")
                          .setBody("Text module body")
                          .setId("TEXT_MODULE_ID")))
              .setLinksModuleData(
                  new LinksModuleData()
                      .setUris(
                          Arrays.asList(
                              new Uri()
                                  .setUri("http://maps.google.com/")
                                  .setDescription("Link module URI description")
                                  .setId("LINK_MODULE_URI_ID"),
                              new Uri()
                                  .setUri("tel:6505555555")
                                  .setDescription("Link module tel description")
                                  .setId("LINK_MODULE_TEL_ID"))))
              .setImageModulesData(
                  Arrays.asList(
                      new ImageModuleData()
                          .setMainImage(
                              new Image()
                                  .setSourceUri(
                                      new ImageUri()
                                          .setUri(
                                              "http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg"))
                                  .setContentDescription(
                                      new LocalizedString()
                                          .setDefaultValue(
                                              new TranslatedString()
                                                  .setLanguage("en-US")
                                                  .setValue("Image module description"))))
                          .setId("IMAGE_MODULE_ID")))
              .setBarcode(new Barcode().setType("QR_CODE").setValue("QR code value"))
              .setLocations(
                  Arrays.asList(
                      new LatLongPoint()
                          .setLatitude(37.424015499999996)
                          .setLongitude(-122.09259560000001)))
              .setAccountId("Account ID")
              .setAccountName("Account name")
              .setLoyaltyPoints(
                  new LoyaltyPoints()
                      .setLabel("Points")
                      .setBalance(new LoyaltyPointsBalance().setInt(800)));

      service.loyaltyobject().insert(loyaltyObject).queue(batch, callback);
    }

    // Invoke the batch API calls
    batch.execute();
  }
  // [END batch]
}
