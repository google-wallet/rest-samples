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

/** Demo class for creating and managing Generic passes in Google Wallet. */
public class DemoGeneric {
  /**
   * Path to service account key file from Google Cloud Console. Environment variable:
   * GOOGLE_APPLICATION_CREDENTIALS.
   */
  public static String keyFilePath;

  /** Service account credentials for Google Wallet APIs. */
  public static GoogleCredentials credentials;

  /** Google Wallet service client. */
  public static Walletobjects service;

  public DemoGeneric() throws Exception {
    keyFilePath =
        System.getenv().getOrDefault("GOOGLE_APPLICATION_CREDENTIALS", "/path/to/key.json");

    Auth();
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

    // Initialize Google Wallet API service
    service =
        new Walletobjects.Builder(
                httpTransport,
                GsonFactory.getDefaultInstance(),
                new HttpCredentialsAdapter(credentials))
            .setApplicationName("APPLICATION_NAME")
            .build();
  }
  // [END auth]

  // [START createClass]
  /**
   * Create a class.
   *
   * @param issuerId The issuer ID being used for this request.
   * @param classSuffix Developer-defined unique ID for this pass class.
   * @return The pass class ID: "{issuerId}.{classSuffix}"
   * @throws IOException
   */
  public String CreateClass(String issuerId, String classSuffix) throws IOException {
    // Check if the class exists
    try {
      service.genericclass().get(String.format("%s.%s", issuerId, classSuffix)).execute();

      System.out.println(String.format("Class %s.%s already exists!", issuerId, classSuffix));
      return String.format("%s.%s", issuerId, classSuffix);
    } catch (GoogleJsonResponseException ex) {
      if (ex.getStatusCode() != 404) {
        // Something else went wrong...
        ex.printStackTrace();
        return String.format("%s.%s", issuerId, classSuffix);
      }
    }

    // See link below for more information on required properties
    // https://developers.google.com/wallet/generic/rest/v1/genericclass
    GenericClass newClass = new GenericClass().setId(String.format("%s.%s", issuerId, classSuffix));

    GenericClass response = service.genericclass().insert(newClass).execute();

    System.out.println("Class insert response");
    System.out.println(response.toPrettyString());

    return response.getId();
  }
  // [END createClass]

  // [START updateClass]
  /**
   * Update a class.
   *
   * <p><strong>Warning:</strong> This replaces all existing class attributes!
   *
   * @param issuerId The issuer ID being used for this request.
   * @param classSuffix Developer-defined unique ID for this pass class.
   * @return The pass class ID: "{issuerId}.{classSuffix}"
   * @throws IOException
   */
  public String UpdateClass(String issuerId, String classSuffix) throws IOException {
    GenericClass updatedClass;

    // Check if the class exists
    try {
      updatedClass =
          service.genericclass().get(String.format("%s.%s", issuerId, classSuffix)).execute();
    } catch (GoogleJsonResponseException ex) {
      if (ex.getStatusCode() == 404) {
        // Class does not exist
        System.out.println(String.format("Class %s.%s not found!", issuerId, classSuffix));
        return String.format("%s.%s", issuerId, classSuffix);
      } else {
        // Something else went wrong...
        ex.printStackTrace();
        return String.format("%s.%s", issuerId, classSuffix);
      }
    }

    // Class exists
    // Update the class by adding a link
    Uri newLink =
        new Uri()
            .setUri("https://developers.google.com/wallet")
            .setDescription("New link description");

    if (updatedClass.getLinksModuleData() == null) {
      // LinksModuleData was not set on the original object
      updatedClass.setLinksModuleData(new LinksModuleData().setUris(new ArrayList<Uri>()));
    }
    updatedClass.getLinksModuleData().getUris().add(newLink);

    GenericClass response =
        service
            .genericclass()
            .update(String.format("%s.%s", issuerId, classSuffix), updatedClass)
            .execute();

    System.out.println("Class update response");
    System.out.println(response.toPrettyString());

    return response.getId();
  }
  // [END updateClass]

  // [START patchClass]
  /**
   * Patch a class.
   *
   * <p>The PATCH method supports patch semantics.
   *
   * @param issuerId The issuer ID being used for this request.
   * @param classSuffix Developer-defined unique ID for this pass class.
   * @return The pass class ID: "{issuerId}.{classSuffix}"
   * @throws IOException
   */
  public String PatchClass(String issuerId, String classSuffix) throws IOException {
    GenericClass existingClass;

    // Check if the class exists
    try {
      existingClass =
          service.genericclass().get(String.format("%s.%s", issuerId, classSuffix)).execute();
    } catch (GoogleJsonResponseException ex) {
      if (ex.getStatusCode() == 404) {
        // Class does not exist
        System.out.println(String.format("Class %s.%s not found!", issuerId, classSuffix));
        return String.format("%s.%s", issuerId, classSuffix);
      } else {
        // Something else went wrong...
        ex.printStackTrace();
        return String.format("%s.%s", issuerId, classSuffix);
      }
    }

    // Class exists
    // Patch the class by adding a homepage
    GenericClass patchBody = new GenericClass();

    // Class exists
    // Update the class by adding a link
    Uri newLink =
        new Uri()
            .setUri("https://developers.google.com/wallet")
            .setDescription("New link description");

    if (existingClass.getLinksModuleData() == null) {
      // LinksModuleData was not set on the original object
      patchBody.setLinksModuleData(new LinksModuleData().setUris(new ArrayList<Uri>()));
    } else {
      patchBody.setLinksModuleData(existingClass.getLinksModuleData());
    }
    patchBody.getLinksModuleData().getUris().add(newLink);

    GenericClass response =
        service
            .genericclass()
            .patch(String.format("%s.%s", issuerId, classSuffix), patchBody)
            .execute();

    System.out.println("Class patch response");
    System.out.println(response.toPrettyString());

    return response.getId();
  }
  // [END patchClass]

  // [START createObject]
  /**
   * Create an object.
   *
   * @param issuerId The issuer ID being used for this request.
   * @param classSuffix Developer-defined unique ID for this pass class.
   * @param objectSuffix Developer-defined unique ID for this pass object.
   * @return The pass object ID: "{issuerId}.{objectSuffix}"
   * @throws IOException
   */
  public String CreateObject(String issuerId, String classSuffix, String objectSuffix)
      throws IOException {
    // Check if the object exists
    try {
      service.genericobject().get(String.format("%s.%s", issuerId, objectSuffix)).execute();

      System.out.println(String.format("Object %s.%s already exists!", issuerId, objectSuffix));
      return String.format("%s.%s", issuerId, objectSuffix);
    } catch (GoogleJsonResponseException ex) {
      if (ex.getStatusCode() != 404) {
        // Something else went wrong...
        ex.printStackTrace();
        return String.format("%s.%s", issuerId, objectSuffix);
      }
    }

    // See link below for more information on required properties
    // https://developers.google.com/wallet/generic/rest/v1/genericobject
    GenericObject newObject =
        new GenericObject()
            .setId(String.format("%s.%s", issuerId, objectSuffix))
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
            .setCardTitle(
                new LocalizedString()
                    .setDefaultValue(
                        new TranslatedString().setLanguage("en-US").setValue("Generic card title")))
            .setHeader(
                new LocalizedString()
                    .setDefaultValue(
                        new TranslatedString().setLanguage("en-US").setValue("Generic header")))
            .setHexBackgroundColor("#4285f4")
            .setLogo(
                new Image()
                    .setSourceUri(
                        new ImageUri()
                            .setUri(
                                "https://storage.googleapis.com/wallet-lab-tools-codelab-artifacts-public/pass_google_logo.jpg"))
                    .setContentDescription(
                        new LocalizedString()
                            .setDefaultValue(
                                new TranslatedString()
                                    .setLanguage("en-US")
                                    .setValue("Generic card logo"))));

    GenericObject response = service.genericobject().insert(newObject).execute();

    System.out.println("Object insert response");
    System.out.println(response.toPrettyString());

    return response.getId();
  }
  // [END createObject]

  // [START updateObject]
  /**
   * Update an object.
   *
   * <p><strong>Warning:</strong> This replaces all existing object attributes!
   *
   * @param issuerId The issuer ID being used for this request.
   * @param objectSuffix Developer-defined unique ID for this pass object.
   * @return The pass object ID: "{issuerId}.{objectSuffix}"
   * @throws IOException
   */
  public String UpdateObject(String issuerId, String objectSuffix) throws IOException {
    GenericObject updatedObject;

    // Check if the object exists
    try {
      updatedObject =
          service.genericobject().get(String.format("%s.%s", issuerId, objectSuffix)).execute();
    } catch (GoogleJsonResponseException ex) {
      if (ex.getStatusCode() == 404) {
        // Object does not exist
        System.out.println(String.format("Object %s.%s not found!", issuerId, objectSuffix));
        return String.format("%s.%s", issuerId, objectSuffix);
      } else {
        // Something else went wrong...
        ex.printStackTrace();
        return String.format("%s.%s", issuerId, objectSuffix);
      }
    }

    // Object exists
    // Update the object by adding a link
    Uri newLink =
        new Uri()
            .setUri("https://developers.google.com/wallet")
            .setDescription("New link description");

    if (updatedObject.getLinksModuleData() == null) {
      // LinksModuleData was not set on the original object
      updatedObject.setLinksModuleData(new LinksModuleData().setUris(Arrays.asList(newLink)));
    } else {
      updatedObject.getLinksModuleData().getUris().add(newLink);
    }

    GenericObject response =
        service
            .genericobject()
            .update(String.format("%s.%s", issuerId, objectSuffix), updatedObject)
            .execute();

    System.out.println("Object update response");
    System.out.println(response.toPrettyString());

    return response.getId();
  }
  // [END updateObject]

  // [START patchObject]
  /**
   * Patch an object.
   *
   * @param issuerId The issuer ID being used for this request.
   * @param objectSuffix Developer-defined unique ID for this pass object.
   * @return The pass object ID: "{issuerId}.{objectSuffix}"
   * @throws IOException
   */
  public String PatchObject(String issuerId, String objectSuffix) throws IOException {
    GenericObject existingObject;

    // Check if the object exists
    try {
      existingObject =
          service.genericobject().get(String.format("%s.%s", issuerId, objectSuffix)).execute();
    } catch (GoogleJsonResponseException ex) {
      if (ex.getStatusCode() == 404) {
        // Object does not exist
        System.out.println(String.format("Object %s.%s not found!", issuerId, objectSuffix));
        return String.format("%s.%s", issuerId, objectSuffix);
      } else {
        // Something else went wrong...
        ex.printStackTrace();
        return String.format("%s.%s", issuerId, objectSuffix);
      }
    }

    // Object exists
    // Patch the object by adding a link
    Uri newLink =
        new Uri()
            .setUri("https://developers.google.com/wallet")
            .setDescription("New link description");

    GenericObject patchBody = new GenericObject();

    if (existingObject.getLinksModuleData() == null) {
      // LinksModuleData was not set on the original object
      patchBody.setLinksModuleData(new LinksModuleData().setUris(new ArrayList<Uri>()));
    } else {
      patchBody.setLinksModuleData(existingObject.getLinksModuleData());
    }
    patchBody.getLinksModuleData().getUris().add(newLink);

    GenericObject response =
        service
            .genericobject()
            .patch(String.format("%s.%s", issuerId, objectSuffix), patchBody)
            .execute();

    System.out.println("Object patch response");
    System.out.println(response.toPrettyString());

    return response.getId();
  }
  // [END patchObject]

  // [START expireObject]
  /**
   * Expire an object.
   *
   * <p>Sets the object's state to Expired. If the valid time interval is already set, the pass will
   * expire automatically up to 24 hours after.
   *
   * @param issuerId The issuer ID being used for this request.
   * @param objectSuffix Developer-defined unique ID for this pass object.
   * @return The pass object ID: "{issuerId}.{objectSuffix}"
   * @throws IOException
   */
  public String ExpireObject(String issuerId, String objectSuffix) throws IOException {
    // Check if the object exists
    try {
      service.genericobject().get(String.format("%s.%s", issuerId, objectSuffix)).execute();
    } catch (GoogleJsonResponseException ex) {
      if (ex.getStatusCode() == 404) {
        // Object does not exist
        System.out.println(String.format("Object %s.%s not found!", issuerId, objectSuffix));
        return String.format("%s.%s", issuerId, objectSuffix);
      } else {
        // Something else went wrong...
        ex.printStackTrace();
        return String.format("%s.%s", issuerId, objectSuffix);
      }
    }

    // Patch the object, setting the pass as expired
    GenericObject patchBody = new GenericObject().setState("EXPIRED");

    GenericObject response =
        service
            .genericobject()
            .patch(String.format("%s.%s", issuerId, objectSuffix), patchBody)
            .execute();

    System.out.println("Object expiration response");
    System.out.println(response.toPrettyString());

    return response.getId();
  }
  // [END expireObject]

  // [START jwtNew]
  /**
   * Generate a signed JWT that creates a new pass class and object.
   *
   * <p>When the user opens the "Add to Google Wallet" URL and saves the pass to their wallet, the
   * pass class and object defined in the JWT are created. This allows you to create multiple pass
   * classes and objects in one API call when the user saves the pass to their wallet.
   *
   * @param issuerId The issuer ID being used for this request.
   * @param classSuffix Developer-defined unique ID for this pass class.
   * @param objectSuffix Developer-defined unique ID for the pass object.
   * @return An "Add to Google Wallet" link.
   */
  public String CreateJWTNewObjects(String issuerId, String classSuffix, String objectSuffix) {
    // See link below for more information on required properties
    // https://developers.google.com/wallet/generic/rest/v1/genericclass
    GenericClass newClass = new GenericClass().setId(String.format("%s.%s", issuerId, classSuffix));

    // See link below for more information on required properties
    // https://developers.google.com/wallet/generic/rest/v1/genericobject
    GenericObject newObject =
        new GenericObject()
            .setId(String.format("%s.%s", issuerId, objectSuffix))
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
            .setCardTitle(
                new LocalizedString()
                    .setDefaultValue(
                        new TranslatedString().setLanguage("en-US").setValue("Generic card title")))
            .setHeader(
                new LocalizedString()
                    .setDefaultValue(
                        new TranslatedString().setLanguage("en-US").setValue("Generic header")))
            .setHexBackgroundColor("#4285f4")
            .setLogo(
                new Image()
                    .setSourceUri(
                        new ImageUri()
                            .setUri(
                                "https://storage.googleapis.com/wallet-lab-tools-codelab-artifacts-public/pass_google_logo.jpg"))
                    .setContentDescription(
                        new LocalizedString()
                            .setDefaultValue(
                                new TranslatedString()
                                    .setLanguage("en-US")
                                    .setValue("Generic card logo"))));

    // Create the JWT as a HashMap object
    HashMap<String, Object> claims = new HashMap<String, Object>();
    claims.put("iss", ((ServiceAccountCredentials) credentials).getClientEmail());
    claims.put("aud", "google");
    claims.put("origins", Arrays.asList("www.example.com"));
    claims.put("typ", "savetowallet");

    // Create the Google Wallet payload and add to the JWT
    HashMap<String, Object> payload = new HashMap<String, Object>();
    payload.put("genericClasses", Arrays.asList(newClass));
    payload.put("genericObjects", Arrays.asList(newObject));
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
  // [END jwtNew]

  // [START jwtExisting]
  /**
   * Generate a signed JWT that references an existing pass object.
   *
   * <p>When the user opens the "Add to Google Wallet" URL and saves the pass to their wallet, the
   * pass objects defined in the JWT are added to the user's Google Wallet app. This allows the user
   * to save multiple pass objects in one API call.
   *
   * <p>The objects to add must follow the below format:
   *
   * <p>{ 'id': 'ISSUER_ID.OBJECT_SUFFIX', 'classId': 'ISSUER_ID.CLASS_SUFFIX' }
   *
   * @param issuerId The issuer ID being used for this request.
   * @return An "Add to Google Wallet" link.
   */
  public String CreateJWTExistingObjects(String issuerId) {
    // Multiple pass types can be added at the same time
    // At least one type must be specified in the JWT claims
    // Note: Make sure to replace the placeholder class and object suffixes
    HashMap<String, Object> objectsToAdd = new HashMap<String, Object>();

    // Event tickets
    objectsToAdd.put(
        "eventTicketObjects",
        Arrays.asList(
            new EventTicketObject()
                .setId(String.format("%s.%s", issuerId, "EVENT_OBJECT_SUFFIX"));

    // Boarding passes
    objectsToAdd.put(
        "flightObjects",
        Arrays.asList(
            new FlightObject()
                .setId(String.format("%s.%s", issuerId, "FLIGHT_OBJECT_SUFFIX"));

    // Generic passes
    objectsToAdd.put(
        "genericObjects",
        Arrays.asList(
            new GenericObject()
                .setId(String.format("%s.%s", issuerId, "GENERIC_OBJECT_SUFFIX"));

    // Gift cards
    objectsToAdd.put(
        "giftCardObjects",
        Arrays.asList(
            new GiftCardObject()
                .setId(String.format("%s.%s", issuerId, "GIFT_CARD_OBJECT_SUFFIX"));

    // Loyalty cards
    objectsToAdd.put(
        "loyaltyObjects",
        Arrays.asList(
            new LoyaltyObject()
                .setId(String.format("%s.%s", issuerId, "LOYALTY_OBJECT_SUFFIX"));

    // Offers
    objectsToAdd.put(
        "offerObjects",
        Arrays.asList(
            new OfferObject()
                .setId(String.format("%s.%s", issuerId, "OFFER_OBJECT_SUFFIX"));

    // Transit passes
    objectsToAdd.put(
        "transitObjects",
        Arrays.asList(
            new TransitObject()
                .setId(String.format("%s.%s", issuerId, "TRANSIT_OBJECT_SUFFIX"));

    // Create the JWT as a HashMap object
    HashMap<String, Object> claims = new HashMap<String, Object>();
    claims.put("iss", ((ServiceAccountCredentials) credentials).getClientEmail());
    claims.put("aud", "google");
    claims.put("origins", Arrays.asList("www.example.com"));
    claims.put("typ", "savetowallet");
    claims.put("payload", objectsToAdd);

    // The service account credentials are used to sign the JWT
    Algorithm algorithm =
        Algorithm.RSA256(
            null, (RSAPrivateKey) ((ServiceAccountCredentials) credentials).getPrivateKey());
    String token = JWT.create().withPayload(claims).sign(algorithm);

    System.out.println("Add to Google Wallet link");
    System.out.println(String.format("https://pay.google.com/gp/v/save/%s", token));

    return String.format("https://pay.google.com/gp/v/save/%s", token);
  }
  // [END jwtExisting]

  // [START batch]
  /**
   * Batch create Google Wallet objects from an existing class.
   *
   * @param issuerId The issuer ID being used for this request.
   * @param classSuffix Developer-defined unique ID for this pass class.
   * @throws IOException
   */
  public void BatchCreateObjects(String issuerId, String classSuffix) throws IOException {
    // Create the batch request client
    BatchRequest batch = service.batch(new HttpCredentialsAdapter(credentials));

    // The callback will be invoked for each request in the batch
    JsonBatchCallback<GenericObject> callback =
        new JsonBatchCallback<GenericObject>() {
          // Invoked if the request was successful
          public void onSuccess(GenericObject response, HttpHeaders responseHeaders) {
            System.out.println("Batch insert response");
            System.out.println(response.toString());
          }

          // Invoked if the request failed
          public void onFailure(GoogleJsonError e, HttpHeaders responseHeaders) {
            System.out.println("Error Message: " + e.getMessage());
          }
        };

    // Example: Generate three new pass objects
    for (int i = 0; i < 3; i++) {
      // Generate a random object suffix
      String objectSuffix = UUID.randomUUID().toString().replaceAll("[^\\w.-]", "_");

      // See link below for more information on required properties
      // https://developers.google.com/wallet/generic/rest/v1/genericobject
      GenericObject batchObject =
          new GenericObject()
              .setId(String.format("%s.%s", issuerId, objectSuffix))
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
              .setCardTitle(
                  new LocalizedString()
                      .setDefaultValue(
                          new TranslatedString()
                              .setLanguage("en-US")
                              .setValue("Generic card title")))
              .setHeader(
                  new LocalizedString()
                      .setDefaultValue(
                          new TranslatedString().setLanguage("en-US").setValue("Generic header")))
              .setHexBackgroundColor("#4285f4")
              .setLogo(
                  new Image()
                      .setSourceUri(
                          new ImageUri()
                              .setUri(
                                  "https://storage.googleapis.com/wallet-lab-tools-codelab-artifacts-public/pass_google_logo.jpg"))
                      .setContentDescription(
                          new LocalizedString()
                              .setDefaultValue(
                                  new TranslatedString()
                                      .setLanguage("en-US")
                                      .setValue("Generic card logo"))));

      service.genericobject().insert(batchObject).queue(batch, callback);
    }

    // Invoke the batch API calls
    batch.execute();
  }
  // [END batch]
}
