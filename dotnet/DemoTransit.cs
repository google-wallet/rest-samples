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
using System.IdentityModel.Tokens.Jwt;
using System.Net;
using System.Net.Http.Headers;
using System.Text.RegularExpressions;
using Google.Apis.Auth.OAuth2;
using Microsoft.IdentityModel.Tokens;
using Newtonsoft.Json;
// [END imports]


class DemoTransit
{
  /*
  * keyFilePath - Path to service account key file from Google Cloud Console
  *             - Environment variable: GOOGLE_APPLICATION_CREDENTIALS
  */
  static string keyFilePath = Environment.GetEnvironmentVariable("GOOGLE_APPLICATION_CREDENTIALS") ?? "/path/to/key.json";

  /*
  * issuerId - The issuer ID being used in this request
  *          - Environment variable: WALLET_ISSUER_ID
  */
  static string issuerId = Environment.GetEnvironmentVariable("WALLET_ISSUER_ID") ?? "issuer-id";

  /*
  * classId - Developer-defined ID for the wallet class
  *         - Environment variable: WALLET_CLASS_ID
  */
  static string classId = Environment.GetEnvironmentVariable("WALLET_CLASS_ID") ?? "test-transit-class-id";

  /*
  * userId - Developer-defined ID for the user, such as an email address
  *        - Environment variable: WALLET_USER_ID
  */
  static string userId = Environment.GetEnvironmentVariable("WALLET_USER_ID") ?? "user-id";

  /*
  * objectId - ID for the wallet object
  *          - Format: `issuerId.identifier`
  *          - Should only include alphanumeric characters, '.', '_', or '-'
  *          - `identifier` is developer-defined and unique to the user
  */
  static string objectId = $"{issuerId}.{new Regex(@"[^\w.-]", RegexOptions.Compiled).Replace(userId, "_")}-{classId}";
  // [END setup]

  static ServiceAccountCredential credentials;
  static HttpClient httpClient;

  async static void Auth()
  {
    ///////////////////////////////////////////////////////////////////////////////
    // Create authenticated HTTP client, using service account file.
    ///////////////////////////////////////////////////////////////////////////////

    // [START auth]
    credentials = (ServiceAccountCredential)GoogleCredential.FromFile(keyFilePath)
        .CreateScoped(new[] { "https://www.googleapis.com/auth/wallet_object.issuer" })
        .UnderlyingCredential;

    httpClient = new HttpClient();
    httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue(
        "Bearer",
        await credentials.GetAccessTokenForRequestAsync()
    );
    // [END auth]
  }

  async static void CreateTransitClass()
  {
    ///////////////////////////////////////////////////////////////////////////////
    // Create a class via the API (this can also be done in the business console).
    ///////////////////////////////////////////////////////////////////////////////

    // [START class]
    string classUrl = "https://walletobjects.googleapis.com/walletobjects/v1/transitClass/";
    var classPayload = new
    {
      id = $"{issuerId}.{classId}",
      issuerName = "test issuer name",
      reviewStatus = "underReview",
      transitType = "bus",
      logo = new
      {
        kind = "walletobjects#image",
        sourceUri = new
        {
          kind = "walletobjects#uri",
          uri = "https://live.staticflickr.com/65535/48690277162_cd05f03f4d_o.png",
          description = "Test logo description"
        }
      }
    };

    HttpRequestMessage classRequest = new HttpRequestMessage(HttpMethod.Post, classUrl);
    classRequest.Content = new StringContent(JsonConvert.SerializeObject(classPayload));
    HttpResponseMessage classResponse = httpClient.Send(classRequest);

    string classContent = await classResponse.Content.ReadAsStringAsync();

    Console.WriteLine($"class POST response: {classContent}");
    // [END class]
  }

  async static void CreateTransitObject()
  {
    ///////////////////////////////////////////////////////////////////////////////
    // Create an object via the API.
    ///////////////////////////////////////////////////////////////////////////////

    // [START object]
    string objectUrl = "https://walletobjects.googleapis.com/walletobjects/v1/transitObject/";
    var objectPayload = new
    {
      id = objectId,
      classId = $"{issuerId}.{classId}",
      heroImage = new
      {
        sourceUri = new
        {
          uri = "https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg",
          description = "Test heroImage description"
        }
      },
      textModulesData = new object[]
      {
        new
        {
          header = "Test text module header",
          body = "Test text module body"
        }
      },
      linksModuleData = new
      {
        uris = new object[]
        {
          new
          {
            kind = "walletobjects#uri",
            uri = "http://maps.google.com/",
            description = "Test link module uri description"
          },
          new
          {
            kind = "walletobjects#uri",
            uri = "tel:6505555555",
            description = "Test link module tel description"
          }
        }
      },
      imageModulesData = new object[]
      {
        new
        {
          mainImage = new
          {
            kind = "walletobjects#image",
            sourceUri = new
            {
              kind = "walletobjects#uri",
              uri = "http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg",
              description = "Test image module description"
            }
          }
        }
      },
      barcode = new
      {
        kind = "walletobjects#barcode",
        type = "qrCode",
        value = "Test QR Code"
      },
      passengerType = "singlePassenger",
      passengerNames = "Test passenger names",
      ticketLeg = new
      {
        originStationCode = "LA",
        originName = new
        {
          kind = "walletobjects#localizedString",
          translatedValues = new object[]
          {
            new
            {
              kind = "walletobjects#translatedString",
              language = "en-us",
              value = "Test translated origin name"
            }
          },
          defaultValue = new
          {
            kind = "walletobjects#translatedString",
            language = "en-us",
            value = "Test default origin name"
          }
        },
        destinationStationCode = "SFO",
        destinationName = new
        {
          kind = "walletobjects#localizedString",
          translatedValues = new object[]
          {
            new
            {
              kind = "walletobjects#translatedString",
              language = "en-us",
              value = "Test translated destination name"
            }
          },
          defaultValue = new
          {
            kind = "walletobjects#translatedString",
            language = "en-us",
            value = "Test default destination name"
          }
        },
        departureDateTime = "2020-04-12T16:20:50.52Z",
        arrivalDateTime = "2020-04-12T20:20:50.52Z",
        fareName = new
        {
          kind = "walletobjects#localizedString",
          translatedValues = new object[]
          {
            new
            {
              kind = "walletobjects#translatedString",
              language = "en-us",
              value = "Test translated fare name"
            }
          },
          defaultValue = new
          {
            kind = "walletobjects#translatedString",
            language = "en-us",
            value = "Test default fare name"
          }
        }
      },
      locations = new object[]
      {
        new
        {
          kind = "walletobjects#latLongPoint",
          latitude = 37.424015499999996,
          longitude = -122.09259560000001
        }
      }
    };

    HttpRequestMessage objectRequest = new HttpRequestMessage(HttpMethod.Get, $"{objectUrl}{objectId}");
    HttpResponseMessage objectResponse = httpClient.Send(objectRequest);
    if (objectResponse.StatusCode == HttpStatusCode.NotFound)
    {
      // Object does not yet exist
      // Send POST request to create it
      objectRequest = new HttpRequestMessage(HttpMethod.Post, objectUrl);
      objectRequest.Content = new StringContent(JsonConvert.SerializeObject(objectPayload));
      objectResponse = httpClient.Send(objectRequest);
    }

    string objectContent = await objectResponse.Content.ReadAsStringAsync();
    Console.WriteLine($"object GET or POST response: {objectContent}");
    // [END object]
  }

  static void CreateJWTSaveURL()
  {
    ///////////////////////////////////////////////////////////////////////////////
    // Create a JWT for the object, and encode it to create a "Save" URL.
    ///////////////////////////////////////////////////////////////////////////////

    // [START jwt]
    JwtPayload claims = new JwtPayload();
    claims.Add("iss", credentials.Id);
    claims.Add("aud", "google");
    claims.Add("origins", new string[] { "www.example.com" });
    claims.Add("typ", "savetowallet");
    claims.Add("payload", new
    {
      transitObjects = new object[]
      {
        new
        {
          id = objectId
        }
      }
    });

    RsaSecurityKey key = new RsaSecurityKey(credentials.Key);
    SigningCredentials signingCredentials = new SigningCredentials(key, SecurityAlgorithms.RsaSha256);
    JwtSecurityToken jwt = new JwtSecurityToken(new JwtHeader(signingCredentials), claims);
    string token = new JwtSecurityTokenHandler().WriteToken(jwt);
    string saveUrl = $"https://pay.google.com/gp/v/save/{token}";

    Console.WriteLine(saveUrl);
    // [END jwt]
  }

  async static void CreateIssuerAccount()
  {
    ///////////////////////////////////////////////////////////////////////////////
    // Create a new Google Wallet issuer account
    ///////////////////////////////////////////////////////////////////////////////

    // [START createIssuer]
    // New issuer name
    string issuerName = "name";

    // New issuer email address
    string issuerEmail = "email-address";

    // Issuer API endpoint
    string issuerUrl = "https://walletobjects.googleapis.com/walletobjects/v1/issuer";

    // New issuer information
    var issuerPayload = new
    {
      name = issuerName,
      contactInfo = new
      {
        email = issuerEmail
      }
    };

    HttpRequestMessage issuerRequest = new HttpRequestMessage(HttpMethod.Post, issuerUrl);
    issuerRequest.Content = new StringContent(JsonConvert.SerializeObject(issuerPayload));
    HttpResponseMessage issuerResponse = httpClient.Send(issuerRequest);

    Console.WriteLine($"issuer POST response: {await issuerResponse.Content.ReadAsStringAsync()}");
    // [END createIssuer]
  }

  async static void UpdateIssuerAccountPermissions()
  {
    ///////////////////////////////////////////////////////////////////////////////
    // Update permissions for an existing Google Wallet issuer account
    ///////////////////////////////////////////////////////////////////////////////

    // [START updatePermissions]
    // Permissions API endpoint
    string permissionsUrl = $"https://walletobjects.googleapis.com/walletobjects/v1/permissions/{issuerId}";

    // New issuer permissions information
    var permissionsPayload = new
    {
      issuerId = issuerId,
      permissions = new object[]
      {
      // Copy as needed for each email address that will need access
      new
      {
        emailAddress = "email-address",
        role = "READER | WRITER | OWNER"
      }
      }
    };

    HttpRequestMessage permissionsRequest = new HttpRequestMessage(HttpMethod.Put, permissionsUrl);
    permissionsRequest.Content = new StringContent(JsonConvert.SerializeObject(permissionsPayload));
    HttpResponseMessage permissionsResponse = httpClient.Send(permissionsRequest);

    Console.WriteLine($"permissions PUT response: {await permissionsResponse.Content.ReadAsStringAsync()}");
    // [END updatePermissions]
  }

  async static void BatchCreateTransitObjects()
  {
    ///////////////////////////////////////////////////////////////////////////////
    // Batch create Google Wallet objects from an existing class
    ///////////////////////////////////////////////////////////////////////////////

    // [START batch]
    // The request body will be a multiline string
    // See below for more information
    // https://cloud.google.com/compute/docs/api/how-tos/batch//example
    string data = "";

    // Example: Generate three new pass objects
    for (int i = 0; i < 3; i++)
    {
      // Generate a random user ID
      userId = Regex.Replace(Guid.NewGuid().ToString(), "[^\\w.-]", "_");

      // Generate an object ID with the user ID
      objectId = $"{issuerId}.{new Regex(@"[^\w.-]", RegexOptions.Compiled).Replace(userId, "_")}-{classId}";
      var batchObject = new
      {
        id = objectId,
        classId = $"{issuerId}.{classId}",
        heroImage = new
        {
          sourceUri = new
          {
            uri = "https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg",
            description = "Test heroImage description"
          }
        },
        textModulesData = new object[]
        {
          new
          {
            header = "Test text module header",
            body = "Test text module body"
          }
        },
        linksModuleData = new
        {
          uris = new object[]
          {
            new
            {
              kind = "walletobjects#uri",
              uri = "http://maps.google.com/",
              description = "Test link module uri description"
            },
            new
            {
              kind = "walletobjects#uri",
              uri = "tel:6505555555",
              description = "Test link module tel description"
            }
          }
        },
        imageModulesData = new object[]
        {
          new
          {
            mainImage = new
            {
              kind = "walletobjects#image",
              sourceUri = new
              {
                kind = "walletobjects#uri",
                uri = "http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg",
                description = "Test image module description"
              }
            }
          }
        },
        barcode = new
        {
          kind = "walletobjects#barcode",
          type = "qrCode",
          value = "Test QR Code"
        },
        passengerType = "singlePassenger",
        passengerNames = "Test passenger names",
        ticketLeg = new
        {
          originStationCode = "LA",
          originName = new
          {
            kind = "walletobjects#localizedString",
            translatedValues = new object[]
            {
              new
              {
                kind = "walletobjects#translatedString",
                language = "en-us",
                value = "Test translated origin name"
              }
            },
            defaultValue = new
            {
              kind = "walletobjects#translatedString",
              language = "en-us",
              value = "Test default origin name"
            }
          },
          destinationStationCode = "SFO",
          destinationName = new
          {
            kind = "walletobjects#localizedString",
            translatedValues = new object[]
            {
              new
              {
                kind = "walletobjects#translatedString",
                language = "en-us",
                value = "Test translated destination name"
              }
            },
            defaultValue = new
            {
              kind = "walletobjects#translatedString",
              language = "en-us",
              value = "Test default destination name"
            }
          },
          departureDateTime = "2020-04-12T16:20:50.52Z",
          arrivalDateTime = "2020-04-12T20:20:50.52Z",
          fareName = new
          {
            kind = "walletobjects#localizedString",
            translatedValues = new object[]
            {
              new
              {
                kind = "walletobjects#translatedString",
                language = "en-us",
                value = "Test translated fare name"
              }
            },
            defaultValue = new
            {
              kind = "walletobjects#translatedString",
              language = "en-us",
              value = "Test default fare name"
            }
          }
        },
        locations = new object[]
        {
          new
          {
            kind = "walletobjects#latLongPoint",
            latitude = 37.424015499999996,
            longitude = -122.09259560000001
          }
        }
      };

      data += "--batch_createobjectbatch\n";
      data += "Content-Type: application/json\n\n";
      data += "POST /walletobjects/v1/transitObject/\n\n";

      data += JsonConvert.SerializeObject(batchObject) + "\n\n";
    }
    data += "--batch_createobjectbatch--";

    // Invoke the batch API calls
    HttpRequestMessage batchObjectRequest = new HttpRequestMessage(
        HttpMethod.Post,
        "https://walletobjects.googleapis.com/batch");

    batchObjectRequest.Content = new StringContent(data);
    batchObjectRequest.Content.Headers.ContentType = new MediaTypeHeaderValue("multipart/mixed");
    batchObjectRequest.Content.Headers.ContentType.Parameters.Add(
        // `boundary` is the delimiter between API calls in the batch request
        new NameValueHeaderValue("boundary", "batch_createobjectbatch"));

    HttpResponseMessage batchObjectResponse = httpClient.Send(batchObjectRequest);

    string batchObjectContent = await batchObjectResponse.Content.ReadAsStringAsync();

    Console.WriteLine($"batch POST response: {batchObjectContent}");
    // [END batch]
  }
}
