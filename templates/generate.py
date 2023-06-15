#
# Copyright 2022 Google Inc. All rights reserved.
#
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#

import os, json

default_class_payload = {
  "id": "$class_id",
}

default_object_payload = {
  "id": "$object_id",
  "classId": "$class_id",
  "state": "ACTIVE",
  "heroImage": {
    "sourceUri": {
      "uri": "https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg"
    },
    "contentDescription": {
      "defaultValue": {
        "language": "en-US",
        "value": "Hero image description"
      }
    }
  },
  "textModulesData": [
    {
      "header": "Text module header",
      "body": "Text module body",
      "id": "TEXT_MODULE_ID"
    }
  ],
  "linksModuleData": {
    "uris": [
      {
        "uri": "http://maps.google.com/",
        "description": "Link module URI description",
        "id": "LINK_MODULE_URI_ID"
      },
      {
        "uri": "tel:6505555555",
        "description": "Link module tel description",
        "id": "LINK_MODULE_TEL_ID"
      }
    ]
  },
  "imageModulesData": [
    {
      "mainImage": {
        "sourceUri": {
          "uri": "http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg"
        },
        "contentDescription": {
          "defaultValue": {
            "language": "en-US",
            "value": "Image module description"
          }
        }
      },
      "id": "IMAGE_MODULE_ID"
    }
  ],
  "barcode": {
    "type": "QR_CODE",
    "value": "QR code"
  }
}

payloads = {}

for object_type in ["generic", "offer", "loyalty", "giftCard", "eventTicket", "flight", "transit"]:
  payloads[object_type] = {
    "$class_payload": dict(default_class_payload),
    "$object_payload": dict(default_object_payload),
  }

#################
# Generic
#################

payloads["generic"]["$object_payload"].update({
  "cardTitle": {
    "defaultValue": {
      "language": "en-US",
      "value": "Generic card title"
    }
  },
  "header": {
    "defaultValue": {
      "language": "en-US",
      "value": "Generic header"
    }
  },
  "hexBackgroundColor": "#4285f4",
  "logo": {
    "sourceUri": {
      "uri": "https://storage.googleapis.com/wallet-lab-tools-codelab-artifacts-public/pass_google_logo.jpg"
    },
    "contentDescription": {
      "defaultValue": {
        "language": "en-US",
        "value": "Generic card logo"
      }
    }
  }
})

#################
# Offer
#################

payloads["offer"]["$class_payload"].update({
  "issuerName": "Issuer name",
  "reviewStatus": "UNDER_REVIEW",
  "provider": "Provider name",
  "title": "Offer title",
  "redemptionChannel": "ONLINE"
})

payloads["offer"]["$object_payload"].update({
  "locations": [
    {
      "latitude": 37.424015499999996,
      "longitude": -122.09259560000001
    }
  ],
  "validTimeInterval": {
    "start": {
      "date": "2023-06-12T23:20:50.52Z"
    },
    "end": {
      "date": "2023-12-12T23:20:50.52Z"
    }
  }
})

#################
# Loyalty
#################

payloads["loyalty"]["$class_payload"].update({
  "issuerName": "Issuer name",
  "reviewStatus": "UNDER_REVIEW",
  "programName": "Program name",
  "programLogo": {
    "sourceUri": {
      "uri": "http://farm8.staticflickr.com/7340/11177041185_a61a7f2139_o.jpg"
    },
    "contentDescription": {
      "defaultValue": {
        "language": "en-US",
        "value": "Logo description"
      }
    }
  }
})

payloads["loyalty"]["$object_payload"].update({
  "locations": [
    {
      "latitude": 37.424015499999996,
      "longitude": -122.09259560000001
    }
  ],
  "accountId": "Account id",
  "accountName": "Account name",
  "loyaltyPoints": {
    "label": "Points",
    "balance": {
      "int": 800
    }
  }
})

#################
# GiftCard
#################

payloads["giftCard"]["$class_payload"].update({
  "issuerName": "Issuer name",
  "reviewStatus": "UNDER_REVIEW",
})

payloads["giftCard"]["$object_payload"].update({
  "locations": [
    {
      "latitude": 37.424015499999996,
      "longitude": -122.09259560000001
    }
  ],
  "cardNumber": "Card number",
  "pin": "1234",
  "balance": {
    "micros": 20000000,
    "currencyCode": "USD"
  },
  "balanceUpdateTime": {
    "date": "2020-04-12T16:20:50.52-04:00"
  }
})

#################
# Eventticket
#################

payloads["eventTicket"]["$class_payload"].update({
  "eventId": "EVENT_ID",
  "eventName": {
    "defaultValue": {
      "language": "en-US",
      "value": "Event name"
    }
  },
  "issuerName": "Issuer name",
  "reviewStatus": "UNDER_REVIEW"
})

payloads["eventTicket"]["$object_payload"].update({
  "locations": [
    {
      "latitude": 37.424015499999996,
      "longitude": -122.09259560000001
    }
  ],
  "seatInfo": {
    "seat": {
      "defaultValue": {
        "language": "en-US",
        "value": "42"
      }
    },
    "row": {
      "defaultValue": {
        "language": "en-US",
        "value": "G3"
      }
    },
    "section": {
      "defaultValue": {
        "language": "en-US",
        "value": "5"
      }
    },
    "gate": {
      "defaultValue": {
        "language": "en-US",
        "value": "A"
      }
    }
  },
  "ticketHolderName": "Ticket holder name",
  "ticketNumber": "Ticket number"
})

#################
# Flight
#################

payloads["flight"]["$class_payload"].update({
  "issuerName": "Issuer name",
  "reviewStatus": "UNDER_REVIEW",
  "localScheduledDepartureDateTime": "2023-07-02T15:30:00",
  "flightHeader": {
    "carrier": {
      "carrierIataCode": "LX"
    },
    "flightNumber": "123"
  },
  "origin": {
    "airportIataCode": "LAX",
    "terminal": "1",
    "gate": "A2"
  },
  "destination": {
    "airportIataCode": "SFO",
    "terminal": "2",
    "gate": "C3"
  }
})

payloads["flight"]["$object_payload"].update({
  "locations": [
    {
      "latitude": 37.424015499999996,
      "longitude": -122.09259560000001
    }
  ],
  "passengerName": "Passenger name",
  "boardingAndSeatingInfo": {
    "boardingGroup": "B",
    "seatNumber": "42"
  },
  "reservationInfo": {
    "confirmationCode": "Confirmation code"
  }
})

#################
# Transit
#################

payloads["transit"]["$class_payload"].update({
  "issuerName": "Issuer name",
  "reviewStatus": "UNDER_REVIEW",
  "logo": {
    "sourceUri": {
      "uri": "https://live.staticflickr.com/65535/48690277162_cd05f03f4d_o.png"
    },
    "contentDescription": {
      "defaultValue": {
        "language": "en-US",
        "value": "Logo description"
      }
    }
  },
  "transitType": "BUS"
})

payloads["transit"]["$object_payload"].update({
  "locations": [
    {
      "latitude": 37.424015499999996,
      "longitude": -122.09259560000001
    }
  ],
  "passengerType": "SINGLE_PASSENGER",
  "passengerNames": "Passenger names",
  "tripType": "ONE_WAY",
  "ticketLeg": {
    "originStationCode": "LA",
    "originName": {
      "defaultValue": {
        "language": "en-US",
        "value": "Origin name"
      }
    },
    "destinationStationCode": "SFO",
    "destinationName": {
      "defaultValue": {
        "language": "en-US",
        "value": "Destination name"
      }
    },
    "departureDateTime": "2020-04-12T16:20:50.52Z",
    "arrivalDateTime": "2020-04-12T20:20:50.52Z",
    "fareName": {
      "defaultValue": {
        "language": "en-US",
        "value": "Fare name"
      }
    }
  }
})

def indent(s, spaces):
  return s.replace("\n", "\n" + (" " * spaces))

def format_payload_dotnet(payload, _):
  output = []
  payload = (payload
    .replace('  "', "  ")
    .replace('": ', " = ")
    .replace(" string = ", ' @string = ')
    .replace("]", "}"))
  for line in payload.split("\n"):
    _indent = len(line) - len(line.lstrip(" "))
    if line.endswith("{"):
      line = line[:-1] + "new\n%s{" % (" " * _indent)
    if line.endswith("["):
      line = line[:-1] + "new object[]\n%s{" % (" " * _indent)
    output.append(line)
  return "\n".join(output)

def format_payload_go(payload, name):
  payload = ("\n" + payload.replace("  ", "\t") + "\n").replace("\n", "\n\t").replace(", \n", ",\n")
  if name == "$batch_object_payload":
    payload = payload.replace("\n", "\n\t")
  return payload

lang_config = {
  "go": {
    "ext": "go",
    "class_id": '"%s.%s"',
    "object_id": '"%s.%s"',
    "filename": lambda s: "demo_%s.go" % s.lower(),
    "formatter": format_payload_go,
  },
  "java": {
    "ext": "java",
    "class_id": "%s.%s",
    "object_id": "%s",
    "formatter": lambda s, _: '\n        "' + s.replace('"', '\\"').replace("\n", '"\n      + "') + '"',
    "filename": lambda s: "src/main/java/Demo%s.java" % s.title(),
  },
  "python": {
    "ext": "py",
    "class_id": '"%s.%s" % (issuer_id, class_id)',
    "object_id": "object_id",
    "filename": lambda s: "demo_%s.py" % s.lower(),
  },
  "nodejs": {
    "ext": "js",
    "class_id": "`${issuerId}.${classId}`",
    "object_id": "objectId",
    "formatter": lambda s, _: indent(s, 2),
    "filename": lambda s: "demo-%s.js" % s.lower(),
  },
  "php": {
    "ext": "php",
    "class_id": '"{$issuerId}.{$classId}"',
    "object_id": '"{$objectId}"',
    "filename": lambda s: "demo_%s.php" % s.lower(),
  },
  "dotnet": {
    "ext": "cs",
    "class_id": '$"{issuerId}.{classId}"',
    "object_id": "objectId",
    "formatter": format_payload_dotnet,
    "filename": lambda s: "Demo%s.cs.example" % s.title(),
    "indent": 4,
  },
}

path = lambda *s: os.path.join(os.path.dirname(os.path.abspath(__file__)), *s)

for lang, config in lang_config.items():
  try:
    with open(path("template.%s" % config["ext"]), "r") as f:
      template = f.read()
  except IOError:
    continue
  for object_type, content in payloads.items():
    output = template

    # JSON payloads
    if "$batch_object_payload" not in content:
      content["$batch_object_payload"] = content["$object_payload"]
    for name, value in content.items():
      payload = json.dumps(value, indent=config.get("indent", 2))
      if "formatter" in config:
        payload = config["formatter"](payload, name)
      output = output.replace(name, payload)

    # code placeholders
    config["object_type"] = object_type
    config["object_type_lowercase"] = object_type.lower()
    config["object_type_titlecase"] = object_type.title()
    for name in ("object_type_titlecase", "object_type_lowercase", "object_type", "class_id", "object_id"):
      output = output.replace('"$%s"' % name, config[name])
      output = output.replace('$%s' % name, config[name])

    with open(path("..", lang, config["filename"](object_type)), "w") as f:
      f.write(output)