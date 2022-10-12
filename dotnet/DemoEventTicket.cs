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
using System.Net.Http.Headers;
using System.Text.RegularExpressions;
using Google.Apis.Auth.OAuth2;
using Google.Apis.Services;
using Google.Apis.Walletobjects.v1;
using Google.Apis.Walletobjects.v1.Data;
using Microsoft.IdentityModel.Tokens;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
// [END imports]


/// <summary>
/// Demo class for creating and managing Event tickets in Google Wallet.
/// </summary>
class DemoEventTicket
{
  /// <summary>
  /// Path to service account key file from Google Cloud Console. Environment
  /// variable: GOOGLE_APPLICATION_CREDENTIALS.
  /// </summary>
  public static string keyFilePath;

  /// <summary>
  /// Service account credentials for Google Wallet APIs
  /// </summary>
  public static ServiceAccountCredential credentials;

  /// <summary>
  /// Google Wallet service client
  /// </summary>
  public static WalletobjectsService service;

  public DemoEventTicket()
  {
    keyFilePath = Environment.GetEnvironmentVariable(
        "GOOGLE_APPLICATION_CREDENTIALS") ?? "/path/to/key.json";
  }
  // [END setup]


  // [START auth]
  /// <summary>
  /// Create authenticated service client using a service account file.
  /// </summary>
  public void Auth()
  {
    credentials = (ServiceAccountCredential)GoogleCredential
        .FromFile(keyFilePath)
        .CreateScoped(new[]
        {
          "https://www.googleapis.com/auth/wallet_object.issuer"
        })
        .UnderlyingCredential;

    service = new WalletobjectsService(
        new BaseClientService.Initializer()
        {
          HttpClientInitializer = credentials,
        });
  }
  // [END auth]

  // [START class]
  /// <summary>
  /// Create a pass class via the API. This can also be done in the Google Pay
  /// and Wallet Console
  /// </summary>
  /// <param name="issuerId">The issuer ID being used for this request.</param>
  /// <param name="classSuffix">Developer-defined unique ID for this pass class.</param>
  /// <returns>The pass class ID: "{issuerId}.{classSuffix}"</returns>
  public string CreateEventTicketClass(string issuerId, string classSuffix)
  {
    // See below for more information on required properties
    // https://developers.google.com/wallet/tickets/events/rest/v1/eventticketclass
    EventTicketClass eventTicketClass = new EventTicketClass
    {
      IssuerName = "Issuer name",
      ReviewStatus = "UNDER_REVIEW",
      EventId = $"{issuerId}.{classSuffix}",
      EventName = new LocalizedString
      {
        DefaultValue = new TranslatedString
        {
          Language = "en-US",
          Value = "Event name"
        }
      }
    };

    Stream responseStream = service.Eventticketclass
        .Insert(eventTicketClass)
        .ExecuteAsStream();

    StreamReader responseReader = new StreamReader(responseStream);
    JObject jsonResponse = JObject.Parse(responseReader.ReadToEnd());

    if (jsonResponse.ContainsKey("error"))
    {
      if (jsonResponse["error"].Value<int>("code") == 409)
      {
        Console.WriteLine($"Class {issuerId}.{classSuffix} already exists");

        return $"{issuerId}.{classSuffix}";
      }
      else
      {
        Console.WriteLine("Something else went wrong");
        Console.WriteLine(jsonResponse.ToString());

        return jsonResponse.ToString();
      }
    }
    else
    {
      Console.WriteLine("Class insert response");
      Console.WriteLine(jsonResponse.ToString());

      return jsonResponse.Value<string>("id");
    }
  }
  // [END class]

  // [START object]
  /// <summary>
  /// Create an object via the API.
  /// </summary>
  /// <param name="issuerId">The issuer ID being used for this request.</param>
  /// <param name="classSuffix">Developer-defined unique ID for this pass class.</param>
  /// <param name="userId">Developer-defined user ID for this object.</param>
  /// <returns>The pass object ID: "{issuerId}.{userId}"</returns>
  public string CreateEventTicketObject(string issuerId, string classSuffix, string userId)
  {
    // Generate the object ID
    // Should only include alphanumeric characters, '.', '_', or '-'
    string newUserId = new Regex(@"[^\w.-]", RegexOptions.Compiled)
        .Replace(userId, "_");
    string objectId = $"{issuerId}.{newUserId}";

    // Check if the object exists
    Stream responseStream = service.Eventticketclass
        .Get(objectId)
        .ExecuteAsStream();
    StreamReader responseReader = new StreamReader(responseStream);
    JObject jsonResponse = JObject.Parse(responseReader.ReadToEnd());

    if (jsonResponse.ContainsKey("error"))
    {
      if (jsonResponse["error"].Value<int>("code") == 404)
      {
        // Object does not exist
        // Send insert request to create it
        // See below for more information on required properties
        // https://developers.google.com/wallet/tickets/events/rest/v1/eventticketobject
        EventTicketObject eventTicketObject = new EventTicketObject
        {
          Id = objectId,
          ClassId = $"{issuerId}.{classSuffix}",
          State = "ACTIVE",
          HeroImage = new Image
          {
            SourceUri = new ImageUri
            {
              Uri = "https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg"
            },
            ContentDescription = new LocalizedString
            {
              DefaultValue = new TranslatedString
              {
                Language = "en-US",
                Value = "Hero image description"
              }
            }
          },
          TextModulesData = new List<TextModuleData>
          {
            new TextModuleData
            {
              Header = "Text module header",
              Body = "Text module body",
              Id = "TEXT_MODULE_ID"
            }
          },
          LinksModuleData = new LinksModuleData
          {
            Uris = new List<Google.Apis.Walletobjects.v1.Data.Uri>
            {
              new Google.Apis.Walletobjects.v1.Data.Uri
              {
                UriValue = "http://maps.google.com/",
                Description = "Link module URI description",
                Id = "LINK_MODULE_URI_ID"
              },
              new Google.Apis.Walletobjects.v1.Data.Uri
              {
                UriValue = "tel:6505555555",
                Description = "Link module tel description",
                Id = "LINK_MODULE_TEL_ID"
              }
            }
          },
          ImageModulesData = new List<ImageModuleData>
          {
            new ImageModuleData
            {
              MainImage = new Image
              {
                SourceUri = new ImageUri
                {
                  Uri = "http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg"
                },
                ContentDescription = new LocalizedString
                {
                  DefaultValue = new TranslatedString
                  {
                    Language = "en-US",
                    Value = "Image module description"
                  }
                }
              },
              Id = "IMAGE_MODULE_ID"
            }
          },
          Barcode = new Barcode
          {
            Type = "QR_CODE",
            Value = "QR code"
          },
          Locations = new List<LatLongPoint>
          {
            new LatLongPoint
            {
              Latitude = 37.424015499999996,
              Longitude = -122.09259560000001
            }
          },
          SeatInfo = new EventSeat
          {
            Seat = new LocalizedString
            {
              DefaultValue = new TranslatedString
              {
                Language = "en-US",
                Value = "42"
              }
            },
            Row = new LocalizedString
            {
              DefaultValue = new TranslatedString
              {
                Language = "en-US",
                Value = "G3"
              }
            },
            Section = new LocalizedString
            {
              DefaultValue = new TranslatedString
              {
                Language = "en-US",
                Value = "5"
              }
            },
            Gate = new LocalizedString
            {
              DefaultValue = new TranslatedString
              {
                Language = "en-US",
                Value = "A"
              }
            }
          },
          TicketHolderName = "Ticket holder name",
          TicketNumber = "Ticket number"
        };

        responseStream = service.Eventticketobject
            .Insert(eventTicketObject)
            .ExecuteAsStream();
        responseReader = new StreamReader(responseStream);
        jsonResponse = JObject.Parse(responseReader.ReadToEnd());

        Console.WriteLine("Object insert response");
        Console.WriteLine(jsonResponse.ToString());

        return jsonResponse.Value<string>("id");
      }
      else
      {
        Console.WriteLine("Something else went wrong");
        Console.WriteLine(jsonResponse.ToString());

        return jsonResponse.ToString();
      }
    }
    else
    {
      Console.WriteLine("Object get response");
      Console.WriteLine(jsonResponse.ToString());

      return jsonResponse.Value<string>("id");
    }
  }
  // [END object]

  // [START jwt]
  /// <summary>
  /// Generate a signed JWT that creates a new pass class and object.
  ///
  /// When the user opens the "Add to Google Wallet" URL and saves the pass to
  /// their wallet, the pass class and object defined in the JWT are created.
  /// This allows you to create multiple pass classes and objects in
  /// one API call when the user saves the pass to their wallet.
  ///
  /// The Google Wallet C# library uses Newtonsoft.Json.JsonPropertyAttribute
  /// to specify the property names when converting objects to JSON. The
  /// Newtonsoft.Json.JsonConvert.SerializeObject method will automatically
  /// serialize the object with the right property names.
  ///
  /// </summary>
  /// <param name="issuerId">The issuer ID being used for this request.</param>
  /// <param name="classSuffix">Developer-defined unique ID for this pass class.</param>
  /// <param name="userId">Developer-defined user ID for this object.</param>
  /// <returns>An "Add to Google Wallet" link.</returns>
  public string CreateJWTSaveURL(string issuerId, string classSuffix, string userId)
  {
    // Ignore null values when serializing to/from JSON
    JsonSerializerSettings excludeNulls = new JsonSerializerSettings()
    {
      NullValueHandling = NullValueHandling.Ignore
    };

    // Generate the object ID
    // Should only include alphanumeric characters, '.', '_', or '-'
    string newUserId = new Regex(@"[^\w.-]", RegexOptions.Compiled)
        .Replace(userId, "_");
    string objectId = $"{issuerId}.{newUserId}";

    // See below for more information on required properties
    // https://developers.google.com/wallet/tickets/events/rest/v1/eventticketclass
    EventTicketClass eventTicketClass = new EventTicketClass
    {
      Id = $"{issuerId}.{classSuffix}",
      IssuerName = "Issuer name",
      ReviewStatus = "UNDER_REVIEW",
      EventId = classSuffix,
      EventName = new LocalizedString
      {
        DefaultValue = new TranslatedString
        {
          Language = "en-US",
          Value = "Event name"
        }
      }
    };

    // Create a JSON representation of the class
    JObject serializedClass = JObject.Parse(
        JsonConvert.SerializeObject(eventTicketClass, excludeNulls));

    // See below for more information on required properties
    // https://developers.google.com/wallet/tickets/events/rest/v1/eventticketobject
    EventTicketObject eventTicketObject = new EventTicketObject
    {
      Id = objectId,
      ClassId = $"{issuerId}.{classSuffix}",
      State = "ACTIVE",
      HeroImage = new Image
      {
        SourceUri = new ImageUri
        {
          Uri = "https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg"
        },
        ContentDescription = new LocalizedString
        {
          DefaultValue = new TranslatedString
          {
            Language = "en-US",
            Value = "Hero image description"
          }
        }
      },
      TextModulesData = new List<TextModuleData>
      {
        new TextModuleData
        {
          Header = "Text module header",
          Body = "Text module body",
          Id = "TEXT_MODULE_ID"
        }
      },
      LinksModuleData = new LinksModuleData
      {
        Uris = new List<Google.Apis.Walletobjects.v1.Data.Uri>
        {
          new Google.Apis.Walletobjects.v1.Data.Uri
          {
            UriValue = "http://maps.google.com/",
            Description = "Link module URI description",
            Id = "LINK_MODULE_URI_ID"
          },
          new Google.Apis.Walletobjects.v1.Data.Uri
          {
            UriValue = "tel:6505555555",
            Description = "Link module tel description",
            Id = "LINK_MODULE_TEL_ID"
          }
        }
      },
      ImageModulesData = new List<ImageModuleData>
      {
        new ImageModuleData
        {
          MainImage = new Image
          {
            SourceUri = new ImageUri
            {
              Uri = "http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg"
            },
            ContentDescription = new LocalizedString
            {
              DefaultValue = new TranslatedString
              {
                Language = "en-US",
                Value = "Image module description"
              }
            }
          },
          Id = "IMAGE_MODULE_ID"
        }
      },
      Barcode = new Barcode
      {
        Type = "QR_CODE",
        Value = "QR code"
      },
      Locations = new List<LatLongPoint>
      {
        new LatLongPoint
        {
          Latitude = 37.424015499999996,
          Longitude = -122.09259560000001
        }
      },
      SeatInfo = new EventSeat
      {
        Seat = new LocalizedString
        {
          DefaultValue = new TranslatedString
          {
            Language = "en-US",
            Value = "42"
          }
        },
        Row = new LocalizedString
        {
          DefaultValue = new TranslatedString
          {
            Language = "en-US",
            Value = "G3"
          }
        },
        Section = new LocalizedString
        {
          DefaultValue = new TranslatedString
          {
            Language = "en-US",
            Value = "5"
          }
        },
        Gate = new LocalizedString
        {
          DefaultValue = new TranslatedString
          {
            Language = "en-US",
            Value = "A"
          }
        }
      },
      TicketHolderName = "Ticket holder name",
      TicketNumber = "Ticket number"
    };

    // Create a JSON representation of the pass
    JObject serializedObject = JObject.Parse(
        JsonConvert.SerializeObject(eventTicketObject, excludeNulls));

    // Create the JWT as a JSON object
    JObject jwtPayload = JObject.Parse(JsonConvert.SerializeObject(new
    {
      iss = credentials.Id,
      aud = "google",
      origins = new string[]
      {
        "www.example.com"
      },
      typ = "savetowallet",
      payload = JObject.Parse(JsonConvert.SerializeObject(new
      {
        // The listed classes and objects will be created
        // when the user saves the pass to their wallet
        eventTicketClasses = new JObject[]
        {
          serializedClass
        },
        eventTicketObjects = new JObject[]
        {
          serializedObject
        }
      })),
    }));

    // Deserialize into a JwtPayload
    JwtPayload claims = JwtPayload.Deserialize(jwtPayload.ToString());

    // The service account credentials are used to sign the JWT
    RsaSecurityKey key = new RsaSecurityKey(credentials.Key);
    SigningCredentials signingCredentials = new SigningCredentials(
        key, SecurityAlgorithms.RsaSha256);
    JwtSecurityToken jwt = new JwtSecurityToken(
        new JwtHeader(signingCredentials), claims);
    string token = new JwtSecurityTokenHandler().WriteToken(jwt);

    Console.WriteLine("Add to Google Wallet link");
    Console.WriteLine($"https://pay.google.com/gp/v/save/{token}");

    return $"https://pay.google.com/gp/v/save/{token}";
  }
  // [END jwt]

  // [START createIssuer]
  /// <summary>
  /// Create a new Google Wallet issuer account.
  /// </summary>
  /// <param name="issuerName">The issuer's name.</param>
  /// <param name="issuerEmail">The issuer's email address.</param>
  public void CreateIssuerAccount(string issuerName, string issuerEmail)
  {
    // New issuer information
    Issuer issuer = new Issuer()
    {
      ContactInfo = new IssuerContactInfo()
      {
        Email = issuerEmail
      },
      Name = issuerName,
    };

    Stream responseStream = service.Issuer
        .Insert(issuer)
        .ExecuteAsStream();
    StreamReader responseReader = new StreamReader(responseStream);
    JObject jsonResponse = JObject.Parse(responseReader.ReadToEnd());

    Console.WriteLine("Issuer insert response");
    Console.WriteLine(jsonResponse.ToString());
  }
  // [END createIssuer]

  // [START updatePermissions]
  /// <summary>
  /// Update permissions for an existing Google Wallet issuer account.
  /// <strong>Warning:</strong> This operation overwrites all existing
  /// permissions!
  ///
  /// <para>Example permissions list argument below. Copy the add entry as needed for each email
  /// address that will need access.Supported values for role are: 'READER', 'WRITER', and 'OWNER'</para>
  ///
  /// <para>List<Permission> permissions = new List<Permission>();
  /// permissions.Add(new Permission { EmailAddress = "emailAddress", Role = "OWNER"});</para>
  /// </summary>
  /// <param name="issuerId">The issuer ID being used for this request.</param>
  /// <param name="permissions">The list of email addresses and roles to assign.</param>
  public void UpdateIssuerAccountPermissions(string issuerId, List<Permission> permissions)
  {
    Stream responseStream = service.Permissions
        .Update(new Permissions
        {
          IssuerId = long.Parse(issuerId),
          PermissionsValue = permissions,
        },
          long.Parse(issuerId))
        .ExecuteAsStream();
    StreamReader responseReader = new StreamReader(responseStream);
    JObject jsonResponse = JObject.Parse(responseReader.ReadToEnd());

    Console.WriteLine("Issuer permissions update response");
    Console.WriteLine(jsonResponse.ToString());
  }
  // [END updatePermissions]

  // [START batch]
  /// <summary>
  /// Batch create Google Wallet objects from an existing class.
  /// </summary>
  /// <param name="issuerId">The issuer ID being used for this request.</param>
  /// <param name="classSuffix">Developer-defined unique ID for this pass class.</param>
  public async void BatchCreateEventTicketObjects(string issuerId, string classSuffix)
  {
    // The request body will be a multiline string
    // See below for more information
    // https://cloud.google.com/compute/docs/api/how-tos/batch//example
    string data = "";

    HttpClient httpClient = new HttpClient();
    httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue(
      "Bearer",
      credentials.GetAccessTokenForRequestAsync().Result
    );

    // Example: Generate three new pass objects
    for (int i = 0; i < 3; i++)
    {
      // Generate an object ID with a random user ID
      // Should only include alphanumeric characters, '.', '_', or '-'
      string userId = Regex.Replace(Guid.NewGuid().ToString(), "[^\\w.-]", "_");
      string objectId = $"{issuerId}.{userId}";

      // See below for more information on required properties
      // https://developers.google.com/wallet/tickets/events/rest/v1/eventticketobject
      EventTicketObject batchEventTicketObject = new EventTicketObject
      {
        Id = objectId,
        ClassId = $"{issuerId}.{classSuffix}",
        State = "ACTIVE",
        HeroImage = new Image
        {
          SourceUri = new ImageUri
          {
            Uri = "https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg"
          },
          ContentDescription = new LocalizedString
          {
            DefaultValue = new TranslatedString
            {
              Language = "en-US",
              Value = "Hero image description"
            }
          }
        },
        TextModulesData = new List<TextModuleData>
        {
          new TextModuleData
          {
            Header = "Text module header",
            Body = "Text module body",
            Id = "TEXT_MODULE_ID"
          }
        },
        LinksModuleData = new LinksModuleData
        {
          Uris = new List<Google.Apis.Walletobjects.v1.Data.Uri>
          {
            new Google.Apis.Walletobjects.v1.Data.Uri
            {
              UriValue = "http://maps.google.com/",
              Description = "Link module URI description",
              Id = "LINK_MODULE_URI_ID"
            },
            new Google.Apis.Walletobjects.v1.Data.Uri
            {
              UriValue = "tel:6505555555",
              Description = "Link module tel description",
              Id = "LINK_MODULE_TEL_ID"
            }
          }
        },
        ImageModulesData = new List<ImageModuleData>
        {
          new ImageModuleData
          {
            MainImage = new Image
            {
              SourceUri = new ImageUri
              {
                Uri = "http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg"
              },
              ContentDescription = new LocalizedString
              {
                DefaultValue = new TranslatedString
                {
                  Language = "en-US",
                  Value = "Image module description"
                }
              }
            },
            Id = "IMAGE_MODULE_ID"
          }
        },
        Barcode = new Barcode
        {
          Type = "QR_CODE",
          Value = "QR code"
        },
        Locations = new List<LatLongPoint>
        {
          new LatLongPoint
          {
            Latitude = 37.424015499999996,
            Longitude = -122.09259560000001
          }
        },
        SeatInfo = new EventSeat
        {
          Seat = new LocalizedString
          {
            DefaultValue = new TranslatedString
            {
              Language = "en-US",
              Value = "42"
            }
          },
          Row = new LocalizedString
          {
            DefaultValue = new TranslatedString
            {
              Language = "en-US",
              Value = "G3"
            }
          },
          Section = new LocalizedString
          {
            DefaultValue = new TranslatedString
            {
              Language = "en-US",
              Value = "5"
            }
          },
          Gate = new LocalizedString
          {
            DefaultValue = new TranslatedString
            {
              Language = "en-US",
              Value = "A"
            }
          }
        },
        TicketHolderName = "Ticket holder name",
        TicketNumber = "Ticket number"
      };

      data += "--batch_createobjectbatch\n";
      data += "Content-Type: application/json\n\n";
      data += "POST /walletobjects/v1/eventTicketObject/\n\n";

      data += JsonConvert.SerializeObject(batchEventTicketObject) + "\n\n";
    }
    data += "--batch_createobjectbatch--";

    // Invoke the batch API calls
    HttpRequestMessage batchObjectRequest = new HttpRequestMessage(
        HttpMethod.Post,
        "https://walletobjects.googleapis.com/batch");

    batchObjectRequest.Content = new StringContent(data);
    batchObjectRequest.Content.Headers.ContentType = new MediaTypeHeaderValue(
        "multipart/mixed");
    // `boundary` is the delimiter between API calls in the batch request
    batchObjectRequest.Content.Headers.ContentType.Parameters.Add(
        new NameValueHeaderValue("boundary", "batch_createobjectbatch"));

    HttpResponseMessage batchObjectResponse = httpClient.Send(
        batchObjectRequest);

    string batchObjectContent = await batchObjectResponse
        .Content
        .ReadAsStringAsync();

    Console.WriteLine("Batch insert response");
    Console.WriteLine(batchObjectContent);
  }
  // [END batch]
}
