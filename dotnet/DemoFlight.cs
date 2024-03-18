﻿/*
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
/// Demo class for creating and managing Flights in Google Wallet.
/// </summary>
class DemoFlight
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

  public DemoFlight()
  {
    keyFilePath = Environment.GetEnvironmentVariable(
        "GOOGLE_APPLICATION_CREDENTIALS") ?? "/path/to/key.json";

    Auth();
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
        .CreateScoped(new List<string>
        {
          WalletobjectsService.ScopeConstants.WalletObjectIssuer
        })
        .UnderlyingCredential;

    service = new WalletobjectsService(
        new BaseClientService.Initializer()
        {
          HttpClientInitializer = credentials
        });
  }
  // [END auth]

  // [START createClass]
  /// <summary>
  /// Create a class.
  /// </summary>
  /// <param name="issuerId">The issuer ID being used for this request.</param>
  /// <param name="classSuffix">Developer-defined unique ID for this pass class.</param>
  /// <returns>The pass class ID: "{issuerId}.{classSuffix}"</returns>
  public string CreateClass(string issuerId, string classSuffix)
  {
    // Check if the class exists
    Stream responseStream = service.Flightclass
        .Get($"{issuerId}.{classSuffix}")
        .ExecuteAsStream();

    StreamReader responseReader = new StreamReader(responseStream);
    JObject jsonResponse = JObject.Parse(responseReader.ReadToEnd());

    if (!jsonResponse.ContainsKey("error"))
    {
      Console.WriteLine($"Class {issuerId}.{classSuffix} already exists!");
      return $"{issuerId}.{classSuffix}";
    }
    else if (jsonResponse["error"].Value<int>("code") != 404)
    {
      // Something else went wrong...
      Console.WriteLine(jsonResponse.ToString());
      return $"{issuerId}.{classSuffix}";
    }

    // See link below for more information on required properties
    // https://developers.google.com/wallet/tickets/boarding-passes/rest/v1/flightclass
    FlightClass newClass = new FlightClass
    {
      Id = $"{issuerId}.{classSuffix}",
      IssuerName = "Issuer name",
      ReviewStatus = "UNDER_REVIEW",
      LocalScheduledDepartureDateTime = "2023-07-02T15:30:00",
      FlightHeader = new FlightHeader
      {
        Carrier = new FlightCarrier
        {
          CarrierIataCode = "LX"
        },
        FlightNumber = "123"
      },
      Origin = new AirportInfo
      {
        AirportIataCode = "LAX",
        Terminal = "1",
        Gate = "A2"
      },
      Destination = new AirportInfo
      {
        AirportIataCode = "SFO",
        Terminal = "2",
        Gate = "C3"
      }
    };

    responseStream = service.Flightclass
        .Insert(newClass)
        .ExecuteAsStream();

    responseReader = new StreamReader(responseStream);
    jsonResponse = JObject.Parse(responseReader.ReadToEnd());

    Console.WriteLine("Class insert response");
    Console.WriteLine(jsonResponse.ToString());

    return $"{issuerId}.{classSuffix}";
  }
  // [END createClass]

  // [START updateClass]
  /// <summary>
  /// Update a class.
  /// <para />
  /// <strong>Warning:</strong> This replaces all existing class attributes!
  /// </summary>
  /// <param name="issuerId">The issuer ID being used for this request.</param>
  /// <param name="classSuffix">Developer-defined unique ID for this pass class.</param>
  /// <returns>The pass class ID: "{issuerId}.{classSuffix}"</returns>
  public string UpdateClass(string issuerId, string classSuffix)
  {
    // Check if the class exists
    Stream responseStream = service.Flightclass
        .Get($"{issuerId}.{classSuffix}")
        .ExecuteAsStream();

    StreamReader responseReader = new StreamReader(responseStream);
    JObject jsonResponse = JObject.Parse(responseReader.ReadToEnd());

    if (jsonResponse.ContainsKey("error"))
    {
      if (jsonResponse["error"].Value<int>("code") == 404)
      {
        // Class does not exist
        Console.WriteLine($"Class {issuerId}.{classSuffix} not found!");
        return $"{issuerId}.{classSuffix}";
      }
      else
      {
        // Something else went wrong...
        Console.WriteLine(jsonResponse.ToString());
        return $"{issuerId}.{classSuffix}";
      }
    }

    // Class exists
    FlightClass updatedClass = JsonConvert.DeserializeObject<FlightClass>(jsonResponse.ToString());

    // Update the class by adding a homepage
    updatedClass.HomepageUri = new Google.Apis.Walletobjects.v1.Data.Uri
    {
      UriValue = "https://developers.google.com/wallet",
      Description = "Homepage description"
    };

    // Note: reviewStatus must be 'UNDER_REVIEW' or 'DRAFT' for updates
    updatedClass.ReviewStatus = "UNDER_REVIEW";

    responseStream = service.Flightclass
        .Update(updatedClass, $"{issuerId}.{classSuffix}")
        .ExecuteAsStream();

    responseReader = new StreamReader(responseStream);
    jsonResponse = JObject.Parse(responseReader.ReadToEnd());

    Console.WriteLine("Class update response");
    Console.WriteLine(jsonResponse.ToString());

    return $"{issuerId}.{classSuffix}";
  }
  // [END updateClass]

  // [START patchClass]
  /// <summary>
  /// Patch a class.
  /// <para />
  /// The PATCH method supports patch semantics.
  /// </summary>
  /// <param name="issuerId">The issuer ID being used for this request.</param>
  /// <param name="classSuffix">Developer-defined unique ID for this pass class.</param>
  /// <returns>The pass class ID: "{issuerId}.{classSuffix}"</returns>
  public string PatchClass(string issuerId, string classSuffix)
  {
    // Check if the class exists
    Stream responseStream = service.Flightclass
        .Get($"{issuerId}.{classSuffix}")
        .ExecuteAsStream();

    StreamReader responseReader = new StreamReader(responseStream);
    JObject jsonResponse = JObject.Parse(responseReader.ReadToEnd());

    if (jsonResponse.ContainsKey("error"))
    {
      if (jsonResponse["error"].Value<int>("code") == 404)
      {
        // Class does not exist
        Console.WriteLine($"Class {issuerId}.{classSuffix} not found!");
        return $"{issuerId}.{classSuffix}";
      }
      else
      {
        // Something else went wrong...
        Console.WriteLine(jsonResponse.ToString());
        return $"{issuerId}.{classSuffix}";
      }
    }

    // Patch the class by adding a homepage
    FlightClass patchBody = new FlightClass
    {
      HomepageUri = new Google.Apis.Walletobjects.v1.Data.Uri
      {
        UriValue = "https://developers.google.com/wallet",
        Description = "Homepage description"
      },

      // Note: reviewStatus must be 'UNDER_REVIEW' or 'DRAFT' for updates
      ReviewStatus = "UNDER_REVIEW"
    };

    responseStream = service.Flightclass
        .Patch(patchBody, $"{issuerId}.{classSuffix}")
        .ExecuteAsStream();

    responseReader = new StreamReader(responseStream);
    jsonResponse = JObject.Parse(responseReader.ReadToEnd());

    Console.WriteLine("Class patch response");
    Console.WriteLine(jsonResponse.ToString());

    return $"{issuerId}.{classSuffix}";
  }
  // [END patchClass]

  // [START addMessageClass]
  /// <summary>
  /// Add a message to a pass class.
  /// </summary>
  /// <param name="issuerId">The issuer ID being used for this request.</param>
  /// <param name="classSuffix">Developer-defined unique ID for this pass class.</param>
  /// <param name="header">The message header.</param>
  /// <param name="body">The message body.</param>
  /// <returns>The pass class ID: "{issuerId}.{classSuffix}"</returns>
  public string AddClassMessage(string issuerId, string classSuffix, string header, string body)
  {
    // Check if the class exists
    Stream responseStream = service.Flightclass
        .Get($"{issuerId}.{classSuffix}")
        .ExecuteAsStream();

    StreamReader responseReader = new StreamReader(responseStream);
    JObject jsonResponse = JObject.Parse(responseReader.ReadToEnd());

    if (jsonResponse.ContainsKey("error"))
    {
      if (jsonResponse["error"].Value<int>("code") == 404)
      {
        // Class does not exist
        Console.WriteLine($"Class {issuerId}.{classSuffix} not found!");
        return $"{issuerId}.{classSuffix}";
      }
      else
      {
        // Something else went wrong...
        Console.WriteLine(jsonResponse.ToString());
        return $"{issuerId}.{classSuffix}";
      }
    }

    AddMessageRequest message = new AddMessageRequest
    {
      Message = new Message
      {
        Header = header,
        Body = body
      }
    };

    responseStream = service.Flightclass
        .Addmessage(message, $"{issuerId}.{classSuffix}")
        .ExecuteAsStream();

    responseReader = new StreamReader(responseStream);
    jsonResponse = JObject.Parse(responseReader.ReadToEnd());

    Console.WriteLine("Class addMessage response");
    Console.WriteLine(jsonResponse.ToString());

    return $"{issuerId}.{classSuffix}";
  }
  // [END addMessageClass]

  // [START createObject]
  /// <summary>
  /// Create an object.
  /// </summary>
  /// <param name="issuerId">The issuer ID being used for this request.</param>
  /// <param name="classSuffix">Developer-defined unique ID for this pass class.</param>
  /// <param name="objectSuffix">Developer-defined unique ID for this pass object.</param>
  /// <returns>The pass object ID: "{issuerId}.{objectSuffix}"</returns>
  public string CreateObject(string issuerId, string classSuffix, string objectSuffix)
  {
    // Check if the object exists
    Stream responseStream = service.Flightobject
        .Get($"{issuerId}.{objectSuffix}")
        .ExecuteAsStream();

    StreamReader responseReader = new StreamReader(responseStream);
    JObject jsonResponse = JObject.Parse(responseReader.ReadToEnd());

    if (!jsonResponse.ContainsKey("error"))
    {
      Console.WriteLine($"Object {issuerId}.{objectSuffix} already exists!");
      return $"{issuerId}.{objectSuffix}";
    }
    else if (jsonResponse["error"].Value<int>("code") != 404)
    {
      // Something else went wrong...
      Console.WriteLine(jsonResponse.ToString());
      return $"{issuerId}.{objectSuffix}";
    }

    // See link below for more information on required properties
    // https://developers.google.com/wallet/tickets/boarding-passes/rest/v1/flightobject
    FlightObject newObject = new FlightObject
    {
      Id = $"{issuerId}.{objectSuffix}",
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
      PassengerName = "Passenger name",
      BoardingAndSeatingInfo = new BoardingAndSeatingInfo
      {
        BoardingGroup = "B",
        SeatNumber = "42"
      },
      ReservationInfo = new ReservationInfo
      {
        ConfirmationCode = "Confirmation code"
      }
    };

    responseStream = service.Flightobject
        .Insert(newObject)
        .ExecuteAsStream();
    responseReader = new StreamReader(responseStream);
    jsonResponse = JObject.Parse(responseReader.ReadToEnd());

    Console.WriteLine("Object insert response");
    Console.WriteLine(jsonResponse.ToString());

    return $"{issuerId}.{objectSuffix}";
  }
  // [END createObject]

  // [START updateObject]
  /// <summary>
  /// Update an object.
  /// <para />
  /// <strong>Warning:</strong> This replaces all existing class attributes!
  /// </summary>
  /// <param name="issuerId">The issuer ID being used for this request.</param>
  /// <param name="objectSuffix">Developer-defined unique ID for this pass object.</param>
  /// <returns>The pass object ID: "{issuerId}.{objectSuffix}"</returns>
  public string UpdateObject(string issuerId, string objectSuffix)
  {
    // Check if the object exists
    Stream responseStream = service.Flightobject
        .Get($"{issuerId}.{objectSuffix}")
        .ExecuteAsStream();

    StreamReader responseReader = new StreamReader(responseStream);
    JObject jsonResponse = JObject.Parse(responseReader.ReadToEnd());

    if (jsonResponse.ContainsKey("error"))
    {
      if (jsonResponse["error"].Value<int>("code") == 404)
      {
        // Object does not exist
        Console.WriteLine($"Object {issuerId}.{objectSuffix} not found!");
        return $"{issuerId}.{objectSuffix}";
      }
      else
      {
        // Something else went wrong...
        Console.WriteLine(jsonResponse.ToString());
        return $"{issuerId}.{objectSuffix}";
      }
    }

    // Object exists
    FlightObject updatedObject = JsonConvert.DeserializeObject<FlightObject>(jsonResponse.ToString());

    // Update the object by adding a link
    Google.Apis.Walletobjects.v1.Data.Uri newLink = new Google.Apis.Walletobjects.v1.Data.Uri
    {
      UriValue = "https://developers.google.com/wallet",
      Description = "New link description"
    };

    if (updatedObject.LinksModuleData == null)
    {
      // LinksModuleData was not set on the original object
      updatedObject.LinksModuleData = new LinksModuleData
      {
        Uris = new List<Google.Apis.Walletobjects.v1.Data.Uri>()
      };
    }
    updatedObject.LinksModuleData.Uris.Add(newLink);

    responseStream = service.Flightobject
        .Update(updatedObject, $"{issuerId}.{objectSuffix}")
        .ExecuteAsStream();

    responseReader = new StreamReader(responseStream);
    jsonResponse = JObject.Parse(responseReader.ReadToEnd());

    Console.WriteLine("Object update response");
    Console.WriteLine(jsonResponse.ToString());

    return $"{issuerId}.{objectSuffix}";
  }
  // [END updateObject]

  // [START patchObject]
  /// <summary>
  /// Patch an object.
  /// </summary>
  /// <param name="issuerId">The issuer ID being used for this request.</param>
  /// <param name="objectSuffix">Developer-defined unique ID for this pass object.</param>
  /// <returns>The pass object ID: "{issuerId}.{objectSuffix}"</returns>
  public string PatchObject(string issuerId, string objectSuffix)
  {
    // Check if the object exists
    Stream responseStream = service.Flightobject
        .Get($"{issuerId}.{objectSuffix}")
        .ExecuteAsStream();

    StreamReader responseReader = new StreamReader(responseStream);
    JObject jsonResponse = JObject.Parse(responseReader.ReadToEnd());

    if (jsonResponse.ContainsKey("error"))
    {
      if (jsonResponse["error"].Value<int>("code") == 404)
      {
        // Object does not exist
        Console.WriteLine($"Object {issuerId}.{objectSuffix} not found!");
        return $"{issuerId}.{objectSuffix}";
      }
      else
      {
        // Something else went wrong...
        Console.WriteLine(jsonResponse.ToString());
        return $"{issuerId}.{objectSuffix}";
      }
    }

    // Object exists
    FlightObject existingObject = JsonConvert.DeserializeObject<FlightObject>(jsonResponse.ToString());

    // Patch the object by adding a link
    Google.Apis.Walletobjects.v1.Data.Uri newLink = new Google.Apis.Walletobjects.v1.Data.Uri
    {
      UriValue = "https://developers.google.com/wallet",
      Description = "New link description"
    };

    FlightObject patchBody = new FlightObject();

    if (existingObject.LinksModuleData == null)
    {
      // LinksModuleData was not set on the original object
      patchBody.LinksModuleData = new LinksModuleData
      {
        Uris = new List<Google.Apis.Walletobjects.v1.Data.Uri>()
      };
    }
    else
    {
      // LinksModuleData was set on the original object
      patchBody.LinksModuleData = existingObject.LinksModuleData;
    }
    patchBody.LinksModuleData.Uris.Add(newLink);

    responseStream = service.Flightobject
        .Patch(patchBody, $"{issuerId}.{objectSuffix}")
        .ExecuteAsStream();

    responseReader = new StreamReader(responseStream);
    jsonResponse = JObject.Parse(responseReader.ReadToEnd());

    Console.WriteLine("Object patch response");
    Console.WriteLine(jsonResponse.ToString());

    return $"{issuerId}.{objectSuffix}";
  }
  // [END patchObject]

  // [START expireObject]
  /// <summary>
  /// Expire an object.
  /// <para />
  /// Sets the object's state to Expired. If the valid time interval is already
  /// set, the pass will expire automatically up to 24 hours after.
  /// </summary>
  /// <param name="issuerId">The issuer ID being used for this request.</param>
  /// <param name="objectSuffix">Developer-defined unique ID for this pass object.</param>
  /// <returns>The pass object ID: "{issuerId}.{objectSuffix}"</returns>
  public string ExpireObject(string issuerId, string objectSuffix)
  {
    // Check if the object exists
    Stream responseStream = service.Flightobject
        .Get($"{issuerId}.{objectSuffix}")
        .ExecuteAsStream();

    StreamReader responseReader = new StreamReader(responseStream);
    JObject jsonResponse = JObject.Parse(responseReader.ReadToEnd());

    if (jsonResponse.ContainsKey("error"))
    {
      if (jsonResponse["error"].Value<int>("code") == 404)
      {
        // Object does not exist
        Console.WriteLine($"Object {issuerId}.{objectSuffix} not found!");
        return $"{issuerId}.{objectSuffix}";
      }
      else
      {
        // Something else went wrong...
        Console.WriteLine(jsonResponse.ToString());
        return $"{issuerId}.{objectSuffix}";
      }
    }

    // Patch the object, setting the pass as expired
    FlightObject patchBody = new FlightObject
    {
      State = "EXPIRED"
    };

    responseStream = service.Flightobject
        .Patch(patchBody, $"{issuerId}.{objectSuffix}")
        .ExecuteAsStream();

    responseReader = new StreamReader(responseStream);
    jsonResponse = JObject.Parse(responseReader.ReadToEnd());

    Console.WriteLine("Object expiration response");
    Console.WriteLine(jsonResponse.ToString());

    return $"{issuerId}.{objectSuffix}";
  }
  // [END expireObject]

  // [START addMessageObject]
  /// <summary>
  /// Add a message to a pass object.
  /// </summary>
  /// <param name="issuerId">The issuer ID being used for this request.</param>
  /// <param name="objectSuffix">Developer-defined unique ID for this pass object.</param>
  /// <param name="header">The message header.</param>
  /// <param name="body">The message body.</param>
  /// <returns>The pass object ID: "{issuerId}.{classSuffix}"</returns>
  public string AddObjectMessage(string issuerId, string objectSuffix, string header, string body)
  {
    // Check if the object exists
    Stream responseStream = service.Flightobject
        .Get($"{issuerId}.{objectSuffix}")
        .ExecuteAsStream();

    StreamReader responseReader = new StreamReader(responseStream);
    JObject jsonResponse = JObject.Parse(responseReader.ReadToEnd());

    if (jsonResponse.ContainsKey("error"))
    {
      if (jsonResponse["error"].Value<int>("code") == 404)
      {
        // Class does not exist
        Console.WriteLine($"Object {issuerId}.{objectSuffix} not found!");
        return $"{issuerId}.{objectSuffix}";
      }
      else
      {
        // Something else went wrong...
        Console.WriteLine(jsonResponse.ToString());
        return $"{issuerId}.{objectSuffix}";
      }
    }

    AddMessageRequest message = new AddMessageRequest
    {
      Message = new Message
      {
        Header = header,
        Body = body
      }
    };

    responseStream = service.Flightobject
        .Addmessage(message, $"{issuerId}.{objectSuffix}")
        .ExecuteAsStream();

    responseReader = new StreamReader(responseStream);
    jsonResponse = JObject.Parse(responseReader.ReadToEnd());

    Console.WriteLine("Object addMessage response");
    Console.WriteLine(jsonResponse.ToString());

    return $"{issuerId}.{objectSuffix}";
  }
  // [END addMessageObject]

  // [START jwtNew]
  /// <summary>
  /// Generate a signed JWT that creates a new pass class and object.
  /// <para />
  /// When the user opens the "Add to Google Wallet" URL and saves the pass to
  /// their wallet, the pass class and object defined in the JWT are created.
  /// This allows you to create multiple pass classes and objects in one API
  /// call when the user saves the pass to their wallet.
  /// <para />
  /// The Google Wallet C# library uses Newtonsoft.Json.JsonPropertyAttribute
  /// to specify the property names when converting objects to JSON. The
  /// Newtonsoft.Json.JsonConvert.SerializeObject method will automatically
  /// serialize the object with the right property names.
  /// </summary>
  /// <param name="issuerId">The issuer ID being used for this request.</param>
  /// <param name="classSuffix">Developer-defined unique ID for this pass class.</param>
  /// <param name="objectSuffix">Developer-defined unique ID for the pass object.</param>
  /// <returns>An "Add to Google Wallet" link.</returns>
  public string CreateJWTNewObjects(string issuerId, string classSuffix, string objectSuffix)
  {
    // Ignore null values when serializing to/from JSON
    JsonSerializerSettings excludeNulls = new JsonSerializerSettings()
    {
      NullValueHandling = NullValueHandling.Ignore
    };

    // See link below for more information on required properties
    // https://developers.google.com/wallet/tickets/boarding-passes/rest/v1/flightclass
    FlightClass newClass = new FlightClass
    {
      Id = $"{issuerId}.{classSuffix}",
      IssuerName = "Issuer name",
      ReviewStatus = "UNDER_REVIEW",
      LocalScheduledDepartureDateTime = "2023-07-02T15:30:00",
      FlightHeader = new FlightHeader
      {
        Carrier = new FlightCarrier
        {
          CarrierIataCode = "LX"
        },
        FlightNumber = "123"
      },
      Origin = new AirportInfo
      {
        AirportIataCode = "LAX",
        Terminal = "1",
        Gate = "A2"
      },
      Destination = new AirportInfo
      {
        AirportIataCode = "SFO",
        Terminal = "2",
        Gate = "C3"
      }
    };

    // See link below for more information on required properties
    // https://developers.google.com/wallet/tickets/boarding-passes/rest/v1/flightobject
    FlightObject newObject = new FlightObject
    {
      Id = $"{issuerId}.{objectSuffix}",
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
      PassengerName = "Passenger name",
      BoardingAndSeatingInfo = new BoardingAndSeatingInfo
      {
        BoardingGroup = "B",
        SeatNumber = "42"
      },
      ReservationInfo = new ReservationInfo
      {
        ConfirmationCode = "Confirmation code"
      }
    };

    // Create JSON representations of the class and object
    JObject serializedClass = JObject.Parse(
        JsonConvert.SerializeObject(newClass, excludeNulls));
    JObject serializedObject = JObject.Parse(
        JsonConvert.SerializeObject(newObject, excludeNulls));

    // Create the JWT as a JSON object
    JObject jwtPayload = JObject.Parse(JsonConvert.SerializeObject(new
    {
      iss = credentials.Id,
      aud = "google",
      origins = new List<string>
      {
        "www.example.com"
      },
      typ = "savetowallet",
      payload = JObject.Parse(JsonConvert.SerializeObject(new
      {
        // The listed classes and objects will be created
        // when the user saves the pass to their wallet
        flightClasses = new List<JObject>
        {
          serializedClass
        },
        flightObjects = new List<JObject>
        {
          serializedObject
        }
      }))
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
  // [END jwtNew]

  // [START jwtExisting]
  /// <summary>
  /// Generate a signed JWT that references an existing pass object.
  /// <para />
  /// When the user opens the "Add to Google Wallet" URL and saves the pass to
  /// their wallet, the pass objects defined in the JWT are added to the user's
  /// Google Wallet app. This allows the user to save multiple pass objects in
  /// one API call.
  /// <para />
  /// The objects to add must follow the below format:
  /// <para />
  /// { 'id': 'ISSUER_ID.OBJECT_SUFFIX', 'classId': 'ISSUER_ID.CLASS_SUFFIX' }
  /// <para />
  /// The Google Wallet C# library uses Newtonsoft.Json.JsonPropertyAttribute
  /// to specify the property names when converting objects to JSON. The
  /// Newtonsoft.Json.JsonConvert.SerializeObject method will automatically
  /// serialize the object with the right property names.
  /// </summary>
  /// <param name="issuerId">The issuer ID being used for this request.</param>
  /// <returns>An "Add to Google Wallet" link.</returns>
  public string CreateJWTExistingObjects(string issuerId)
  {
    // Ignore null values when serializing to/from JSON
    JsonSerializerSettings excludeNulls = new JsonSerializerSettings()
    {
      NullValueHandling = NullValueHandling.Ignore
    };

    // Multiple pass types can be added at the same time
    // At least one type must be specified in the JWT claims
    // Note: Make sure to replace the placeholder class and object suffixes
    Dictionary<string, Object> objectsToAdd = new Dictionary<string, Object>();

    // Event tickets
    objectsToAdd.Add("eventTicketObjects", new List<EventTicketObject>
    {
      new EventTicketObject
      {
        Id = $"{issuerId}.EVENT_OBJECT_SUFFIX",
        ClassId = $"{issuerId}.EVENT_CLASS_SUFFIX"
      }
    });

    // Boarding passes
    objectsToAdd.Add("flightObjects", new List<FlightObject>
    {
      new FlightObject
      {
        Id = $"{issuerId}.FLIGHT_OBJECT_SUFFIX",
        ClassId = $"{issuerId}.FLIGHT_CLASS_SUFFIX"
      }
    });

    // Generic passes
    objectsToAdd.Add("genericObjects", new List<GenericObject>
    {
      new GenericObject
      {
        Id = $"{issuerId}.GENERIC_OBJECT_SUFFIX",
        ClassId = $"{issuerId}.GENERIC_CLASS_SUFFIX"
      }
    });

    // Gift cards
    objectsToAdd.Add("giftCardObjects", new List<GiftCardObject>
    {
      new GiftCardObject
      {
        Id = $"{issuerId}.GIFT_CARD_OBJECT_SUFFIX",
        ClassId = $"{issuerId}.GIFT_CARD_CLASS_SUFFIX"
      }
    });

    // Loyalty cards
    objectsToAdd.Add("loyaltyObjects", new List<LoyaltyObject>
    {
      new LoyaltyObject
      {
        Id = $"{issuerId}.LOYALTY_OBJECT_SUFFIX",
        ClassId = $"{issuerId}.LOYALTY_CLASS_SUFFIX"
      }
    });

    // Offers
    objectsToAdd.Add("offerObjects", new List<OfferObject>
    {
      new OfferObject
      {
        Id = $"{issuerId}.OFFER_OBJECT_SUFFIX",
        ClassId = $"{issuerId}.OFFER_CLASS_SUFFIX"
      }
    });

    // Transit passes
    objectsToAdd.Add("transitObjects", new List<TransitObject>
    {
      new TransitObject
      {
        Id = $"{issuerId}.TRANSIT_OBJECT_SUFFIX",
        ClassId = $"{issuerId}.TRANSIT_CLASS_SUFFIX"
      }
    });

    // Create a JSON representation of the payload
    JObject serializedPayload = JObject.Parse(
        JsonConvert.SerializeObject(objectsToAdd, excludeNulls));

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
      payload = serializedPayload
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
  // [END jwtExisting]

  // [START batch]
  /// <summary>
  /// Batch create Google Wallet objects from an existing class.
  /// </summary>
  /// <param name="issuerId">The issuer ID being used for this request.</param>
  /// <param name="classSuffix">Developer-defined unique ID for this pass class.</param>
  public async void BatchCreateObjects(string issuerId, string classSuffix)
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
      // Generate a random object suffix
      string objectSuffix = Regex.Replace(Guid.NewGuid().ToString(), "[^\\w.-]", "_");

      // See link below for more information on required properties
      // https://developers.google.com/wallet/tickets/boarding-passes/rest/v1/flightobject
      FlightObject batchObject = new FlightObject
      {
        Id = $"{issuerId}.{objectSuffix}",
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
        PassengerName = "Passenger name",
        BoardingAndSeatingInfo = new BoardingAndSeatingInfo
        {
          BoardingGroup = "B",
          SeatNumber = "42"
        },
        ReservationInfo = new ReservationInfo
        {
          ConfirmationCode = "Confirmation code"
        }
      };

      data += "--batch_createobjectbatch\n";
      data += "Content-Type: application/json\n\n";
      data += "POST /walletobjects/v1/flightObject/\n\n";

      data += JsonConvert.SerializeObject(batchObject) + "\n\n";
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
