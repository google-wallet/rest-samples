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

class DemoMiguelClass
{
  public static string keyFilePath;
  public static ServiceAccountCredential credentials;
  public static WalletobjectsService service;

  public static string issuerId = "123456";
  public static string className = "MiguelClass";
  public static string objectName = "MiguelObject";

  public DemoMiguelClass()
  {
    keyFilePath = Environment.GetEnvironmentVariable(
        "GOOGLE_APPLICATION_CREDENTIALS") ?? "/Users/ncalteen/Downloads/wallet-samples/wallet-samples-391719-0c83624c91d4.json";

    Auth();
  }
  
  public void Auth()
  {
    credentials = (ServiceAccountCredential)GoogleCredential
        .FromFile(keyFilePath)
        .CreateScoped(new List<string>
        {
          "https://www.googleapis.com/auth/wallet_object.issuer"
        })
        .UnderlyingCredential;

    service = new WalletobjectsService(
        new BaseClientService.Initializer()
        {
          HttpClientInitializer = credentials
        });
  }

  public string CreateClass()
  {
    GenericClass newClass = new GenericClass
    {
      Id = $"{issuerId}.{className}",
      ClassTemplateInfo = new ClassTemplateInfo
      {
        CardTemplateOverride = new CardTemplateOverride
        {
          CardRowTemplateInfos = new List<CardRowTemplateInfo>
          {
            new CardRowTemplateInfo
            {
              ThreeItems = new CardRowThreeItems
              {
                StartItem = new TemplateItem
                {
                  FirstValue = new FieldSelector
                  {
                    Fields = new List<FieldReference>
                    {
                      new FieldReference
                      {
                        FieldPath = "object.textModulesData['bancada']"
                      }
                    }
                  }
                },
                MiddleItem = new TemplateItem
                {
                  FirstValue = new FieldSelector
                  {
                    Fields = new List<FieldReference>
                    {
                      new FieldReference
                      {
                        FieldPath = "object.textModulesData['porta']"
                      }
                    }
                  }
                },
                EndItem = new TemplateItem
                {
                  FirstValue = new FieldSelector
                  {
                    Fields = new List<FieldReference>
                    {
                      new FieldReference
                      {
                        FieldPath = "object.textModulesData['sector']"
                      }
                    }
                  }
                }
              }
            },
            new CardRowTemplateInfo
            {
              ThreeItems = new CardRowThreeItems
              {
                StartItem = new TemplateItem
                {
                  FirstValue = new FieldSelector
                  {
                    Fields = new List<FieldReference>
                    {
                      new FieldReference
                      {
                        FieldPath = "object.textModulesData['piso']"
                      }
                    }
                  }
                },
                MiddleItem = new TemplateItem
                {
                  FirstValue = new FieldSelector
                  {
                    Fields = new List<FieldReference>
                    {
                      new FieldReference
                      {
                        FieldPath = "object.textModulesData['fila']"
                      }
                    }
                  }
                },
                EndItem = new TemplateItem
                {
                  FirstValue = new FieldSelector
                  {
                    Fields = new List<FieldReference>
                    {
                      new FieldReference
                      {
                        FieldPath = "object.textModulesData['lugar']"
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    };
    
    responseStream = service.Genericclass
        .Insert(newClass)
        .ExecuteAsStream();

    responseReader = new StreamReader(responseStream);
    jsonResponse = JObject.Parse(responseReader.ReadToEnd());

    Console.WriteLine("Class insert response");
    Console.WriteLine(jsonResponse.ToString());

    return $"{issuerId}.{className}";
  }

  public string CreateObject()
  {
    GenericObject newObject = new GenericObject
    {
      Id = $"{issuerId}.{objectName}",
      ClassId = $"{issuerId}.{className}",
      State = "ACTIVE",
      CardTitle = new LocalizedString
      {
        DefaultValue = new TranslatedString
        {
          Language = "en-US",
          Value = "My Generic Pass Title"
        }
      },
      Header = new LocalizedString
      {
        DefaultValue = new TranslatedString
        {
          Language = "en-US",
          Value = "My Generic Pass Header"
        }
      },
      Subheader = new LocalizedString
      {
        DefaultValue = new TranslatedString
        {
          Language = "en-US",
          Value = "My Generic Pass Subheader"
        }
      },
      Barcode = new Barcode
      {
        Type = "QR_CODE",
        Value = "QR code"
      },
      HexBackgroundColor = "#4285f4",
      Logo = new Image
      {
        SourceUri = new ImageUri
        {
          Uri = "https://storage.googleapis.com/wallet-lab-tools-codelab-artifacts-public/pass_google_logo.jpg"
        },
        ContentDescription = new LocalizedString
        {
          DefaultValue = new TranslatedString
          {
            Language = "en-US",
            Value = "Generic card logo"
          }
        },
      },
      TextModulesData = new List<TextModuleData>
      {
        new TextModuleData
        {
          Header = "Bancada",
          Body = "A",
          Id = "bancada"
        },
        new TextModuleData
        {
          Header = "Porta",
          Body = "O1",
          Id = "porta"
        },
        new TextModuleData
        {
          Header = "Sector",
          Body = "B2",
          Id = "sector"
        },
        new TextModuleData
        {
          Header = "Piso",
          Body = "T",
          Id = "piso"
        },
        new TextModuleData
        {
          Header = "Fila",
          Body = "P",
          Id = "fila"
        },
        new TextModuleData
        {
          Header = "Lugar",
          Body = "21",
          Id = "lugar"
        }
      }
    };

    responseStream = service.Genericobject
        .Insert(newObject)
        .ExecuteAsStream();
    responseReader = new StreamReader(responseStream);
    jsonResponse = JObject.Parse(responseReader.ReadToEnd());

    Console.WriteLine("Object insert response");
    Console.WriteLine(jsonResponse.ToString());

    return $"{issuerId}.{objectName}";
  }
  
  public string CreateJWTExistingObjects()
  {
    JsonSerializerSettings excludeNulls = new JsonSerializerSettings()
    {
      NullValueHandling = NullValueHandling.Ignore
    };

    Dictionary<string, Object> objectsToAdd = new Dictionary<string, Object>();

    objectsToAdd.Add("genericObjects", new List<GenericObject>
    {
      new GenericObject
      {
        Id = $"{issuerId}.{objectName}",
        ClassId = $"{issuerId}.{className}"
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
}
