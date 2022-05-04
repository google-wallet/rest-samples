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
  "issuerName": "test issuer name",
}

default_object_payload = {
  "id": "$object_id",
  "classId": "$class_id",
  "heroImage": {
    "sourceUri": {
      "uri": "https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg",
      "description": "Test heroImage description",
    },
  },
  "textModulesData": [
    {
      "header": "Test text module header",
      "body": "Test text module body",
    },
  ],
  "linksModuleData": {
    "uris": [
      {
        "kind": "walletobjects#uri",
        "uri": "http://maps.google.com/",
        "description": "Test link module uri description",
      },
      {
        "kind": "walletobjects#uri",
        "uri": "tel:6505555555",
        "description": "Test link module tel description",
      },
    ],
  },
  "imageModulesData": [
    {
      "mainImage": {
        "kind": "walletobjects#image",
        "sourceUri": {
          "kind": "walletobjects#uri",
          "uri":  "http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg",
          "description": "Test image module description",
        },
      },
    },
  ],
  "barcode": {
    "kind": "walletobjects#barcode",
    "type": "qrCode",
    "value": "Test QR Code"
  },
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
  },
})

#################
# Offer
#################

payloads["offer"]["$class_payload"].update({
  "provider": "test provider",
  "reviewStatus" : "underReview",
  "title": "test title",
  "redemptionChannel" : "online"
})

payloads["offer"]["$object_payload"].update({
  "state" : "active",
  "barcode": {
    "type": "qrCode",
    "value": "Testing Offers QR Code"
  },
  "validTimeInterval": {
    "kind": "walletobjects#timeInterval",
    "start": {"date": "2023-06-12T23:20:50.52Z"},
    "end": {"date": "2023-12-12T23:20:50.52Z"},
  },
  "locations": [{
    "kind": "walletobjects#latLongPoint",
    "latitude": 37.424015499999996,
    "longitude": -122.09259560000001,
  }],
})

#################
# Loyalty
#################

payloads["loyalty"]["$class_payload"].update({
  "programName": "test program name",
  "programLogo": {
    "kind": "walletobjects#image",
    "sourceUri": {
      "kind": "walletobjects#uri",
      "uri": "http://farm8.staticflickr.com/7340/11177041185_a61a7f2139_o.jpg",
    },
  },
  "reviewStatus": "underReview",
})

payloads["loyalty"]["$object_payload"].update({
  "state" : "active",
  "accountId": "Test account id",
  "accountName": "Test account name",
  "loyaltyPoints": {
    "balance": {
      "string": "800"
    },
    "label": "Points",
  },
  "locations": [{
    "kind": "walletobjects#latLongPoint",
    "latitude": 37.424015499999996,
    "longitude": -122.09259560000001,
  }],
})

#################
# GiftCard
#################

payloads["giftCard"]["$class_payload"].update({
  "merchantName": "Test merchant name",
  "allowMultipleUsersPerObject": "true",
  "reviewStatus": "underReview",
})

payloads["giftCard"]["$object_payload"].update({
  "cardNumber": "Test card number",
  "cardPin": "Test card pin",
  "balance": {
    "kind": "walletobjects#money",
    "micros": 20000000,
    "currencyCode": "USD",
  },
  "balanceUpdateTime": {
    "date": "2020-04-12T16:20:50.52Z",
  },
  "locations": [{
    "kind": "walletobjects#latLongPoint",
    "latitude": 37.424015499999996,
    "longitude": -122.09259560000001,
  }],
})

#################
# Eventticket
#################

payloads["eventTicket"]["$class_payload"].update({
  "eventName": {
    "defaultValue": {
      "language": "en-US",
      "value": "Test event name",
    },
  },
  "reviewStatus": "underReview",
})

payloads["eventTicket"]["$object_payload"].update({
  "state" : "active",
  "seatInfo": {
    "kind": "walletobjects#eventSeat",
    "seat": {
      "kind": "walletobjects#localizedString",
      "defaultValue": {
        "kind": "walletobjects#translatedString",
        "language": "en-us",
        "value": "42",
      },
    },
    "row": {
      "kind": "walletobjects#localizedString",
      "defaultValue": {
        "kind": "walletobjects#translatedString",
        "language": "en-us",
        "value": "G3",
      },
    },
    "section": {
      "kind": "walletobjects#localizedString",
      "defaultValue": {
        "kind": "walletobjects#translatedString",
        "language": "en-us",
        "value": "5",
      },
    },
    "gate": {
      "kind": "walletobjects#localizedString",
      "defaultValue": {
        "kind": "walletobjects#translatedString",
        "language": "en-us",
        "value": "A",
      },
    },
  },
  "ticketHolderName": "Test ticket holder name",
  "ticketNumber": "Test ticket number",
  "locations": [{
    "kind": "walletobjects#latLongPoint",
    "latitude": 37.424015499999996,
    "longitude": -122.09259560000001,
  }],
})

#################
# Flight
#################

payloads["flight"]["$class_payload"].update({
  "destination": {
    "airportIataCode": "SFO",
    "gate": "C3",
    "terminal": "2",
  },
  "flightHeader": {
    "carrier": {
      "carrierIataCode": "LX",
    },
    "flightNumber": "123",
  },
  "origin": {
    "airportIataCode": "LAX",
    "gate": "A2",
    "terminal": "1",
  },
  "localScheduledDepartureDateTime" : "2023-07-02T15:30:00",
  "reviewStatus": "underReview",
})

payloads["flight"]["$object_payload"].update({
  "state": "active",
  "passengerName": "Test passenger name",
  "reservationInfo": {
    "confirmationCode": "Test confirmation code",
  },
  "boardingAndSeatingInfo": {
    "seatNumber": "42",
    "boardingGroup": "B",
  },
  "locations": [{
    "kind": "walletobjects#latLongPoint",
    "latitude": 37.424015499999996,
    "longitude": -122.09259560000001,
  }],
})

#################
# Transit
#################

payloads["transit"]["$class_payload"].update({
  "reviewStatus": "underReview",
  "transitType": "bus",
  "logo": {
    "kind": "walletobjects#image",
    "sourceUri": {
      "kind": "walletobjects#uri",
      "uri": "https://live.staticflickr.com/65535/48690277162_cd05f03f4d_o.png",
      "description": "Test logo description",
    },
  },
})

payloads["transit"]["$object_payload"].update({
  "passengerType": "singlePassenger",
  "passengerNames": "Test passenger names",
  "ticketLeg": {
    "originStationCode": "LA",
    "originName": {
      "kind": "walletobjects#localizedString",
      "translatedValues": [{
        "kind": "walletobjects#translatedString",
        "language": "en-us",
        "value": "Test translated origin name",
      }],
      "defaultValue": {
        "kind": "walletobjects#translatedString",
        "language": "en-us",
        "value": "Test default origin name",
      },
    },
    "destinationStationCode": "SFO",
    "destinationName": {
      "kind": "walletobjects#localizedString",
      "translatedValues": [{
        "kind": "walletobjects#translatedString",
        "language": "en-us",
        "value": "Test translated destination name",
      }],
      "defaultValue": {
        "kind": "walletobjects#translatedString",
        "language": "en-us",
        "value": "Test default destination name",
      },
    },
    "departureDateTime": "2020-04-12T16:20:50.52Z",
    "arrivalDateTime": "2020-04-12T20:20:50.52Z",
    "fareName": {
      "kind": "walletobjects#localizedString",
      "translatedValues": [{
        "kind": "walletobjects#translatedString",
        "language": "en-us",
        "value": "Test translated fare name",
      }],
      "defaultValue": {
        "kind": "walletobjects#translatedString",
        "language": "en-us",
        "value": "Test default fare name",
      },
    },
  },
  "locations": [{
    "kind": "walletobjects#latLongPoint",
    "latitude": 37.424015499999996,
    "longitude": -122.09259560000001,
  }],
})

def indent(s, spaces):
  return s.replace("\n", "\n" + (" " * spaces))

def format_payload_dotnet(payload):
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

lang_config = {
  "java": {
    "ext": "java",
    "class_id": "%s.%s",
    "object_id": "%s",
    "formatter": lambda s: '\n        "' + s.replace('"', '\\"').replace("\n", '"\n      + "') + '"',
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
    "formatter": lambda s: indent(s, 2),
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
  with open(path("template.%s" % config["ext"]), "r") as f:
    template = f.read()
  for object_type, content in payloads.items():
    output = template

    # JSON payloads
    for name, value in content.items():
      payload = json.dumps(value, indent=config.get("indent", 2))
      if "formatter" in config:
        payload = config["formatter"](payload)
      output = output.replace(name, payload)

    # code placeholders
    config["object_type"] = object_type
    config["object_type_titlecase"] = object_type.title()
    for name in ("object_type_titlecase", "object_type", "class_id", "object_id"):
      output = output.replace('"$%s"' % name, config[name])
      output = output.replace('$%s' % name, config[name])

    with open(path("..", lang, config["filename"](object_type)), "w") as f:
      f.write(output)
