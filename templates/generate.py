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

import os
import json

default_class_payload = {
    "id": "$class_id",
    "issuerName": "test issuer name",
}

default_object_payload = {
    "id": "$object_id",
    "classId": "$class_id",
    "heroImage": {
        "sourceUri": {
            "uri":
                "https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg",
            "description":
                "Test heroImage description",
        },
    },
    "textModulesData": [{
        "header": "Test text module header",
        "body": "Test text module body",
    },],
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
    "imageModulesData": [{
        "mainImage": {
            "kind": "walletobjects#image",
            "sourceUri": {
                "kind":
                    "walletobjects#uri",
                "uri":
                    "http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg",
                "description":
                    "Test image module description",
            },
        },
    },],
    "barcode": {
        "kind": "walletobjects#barcode",
        "type": "qrCode",
        "value": "Test QR Code",
    },
}

BASE_URL = "https://developers.google.com/wallet"

url_map = {
    "generic": "/generic/rest/v1/genericobject",
    "offer": "/retail/offers/rest/v1/offerobject",
    "loyalty": "/retail/loyalty-cards/rest/v1/loyaltyobject",
    "giftCard": "/retail/gift-cards/rest/v1/giftcardobject",
    "eventTicket": "/tickets/events/rest/v1/eventticketobject",
    "flight": "/tickets/boarding-passes/rest/v1/flightobject",
    "transit": "/tickets/transit-passes/qr-code/rest/v1/transitobject",
}

payloads = {}

for object_type in [
        "generic",
        "offer",
        "loyalty",
        "giftCard",
        "eventTicket",
        "flight",
        "transit",
]:
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
            "uri":
                "https://storage.googleapis.com/wallet-lab-tools-codelab-artifacts-public/pass_google_logo.jpg"
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
    "reviewStatus": "underReview",
    "title": "test title",
    "redemptionChannel": "online",
})

payloads["offer"]["$object_payload"].update({
    "state":
        "active",
    "barcode": {
        "type": "qrCode",
        "value": "Testing Offers QR Code"
    },
    "validTimeInterval": {
        "kind": "walletobjects#timeInterval",
        "start": {
            "date": "2023-06-12T23:20:50.52Z"
        },
        "end": {
            "date": "2023-12-12T23:20:50.52Z"
        },
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
            "kind":
                "walletobjects#uri",
            "uri":
                "http://farm8.staticflickr.com/7340/11177041185_a61a7f2139_o.jpg",
        },
    },
    "reviewStatus": "underReview",
})

payloads["loyalty"]["$object_payload"].update({
    "state":
        "active",
    "accountId":
        "Test account id",
    "accountName":
        "Test account name",
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
    "cardNumber":
        "Test card number",
    "cardPin":
        "Test card pin",
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
    "state":
        "active",
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
    "ticketHolderName":
        "Test ticket holder name",
    "ticketNumber":
        "Test ticket number",
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
    "localScheduledDepartureDateTime": "2023-07-02T15:30:00",
    "reviewStatus": "underReview",
})

payloads["flight"]["$object_payload"].update({
    "state":
        "active",
    "passengerName":
        "Test passenger name",
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
            "kind":
                "walletobjects#uri",
            "uri":
                "https://live.staticflickr.com/65535/48690277162_cd05f03f4d_o.png",
            "description":
                "Test logo description",
        },
    },
})

payloads["transit"]["$object_payload"].update({
    "passengerType":
        "singlePassenger",
    "passengerNames":
        "Test passenger names",
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


def indent(text, spaces):
    """Enforce spacing/indentation on each new line"""
    return text.replace("\n", "\n" + (" " * spaces))


def format_filename_dotnet(object_type_name):
    """Format .cs filename for .NET"""
    return f"Demo{object_type_name[0].upper()}{object_type_name[1:]}.cs"


def format_payload_dotnet(unformatted_payload):
    """Format JSON payloads for .NET syntax"""
    formatted_output = []

    unformatted_payload = unformatted_payload.replace('  "', "  ")
    unformatted_payload = unformatted_payload.replace('": ', " = ")
    unformatted_payload = unformatted_payload.replace(" string = ",
                                                      " @string = ")
    unformatted_payload = unformatted_payload.replace("]", "}")

    for line in unformatted_payload.split("\n"):
        _indent = len(line) - len(line.lstrip(" "))
        if line.endswith("{"):
            line = line[:-1] + f"new\n{' ' * _indent}{{"
        if line.endswith("["):
            line = line[:-1] + f"new object[]\n{' ' * _indent}{{"

        formatted_output.append(line)
    return "\n".join(formatted_output)


def format_payload_java(unformatted_payload):
    """Format JSON payloads for Java syntax"""
    formatted_payload = unformatted_payload.replace('"', '\\"')
    formatted_payload = formatted_payload.replace("\n", '"\n      + "')

    formatted_payload = '\n        "' + formatted_payload + '"'

    return formatted_payload


def format_with_offset(unformatted_payload, offset):
    """Format request payloads with additional indentation offset."""
    formatted_payload = [unformatted_payload.split("\n")[0]]
    formatted_payload += [
        (" " * offset) + x for x in unformatted_payload.split("\n")[1:]
    ]
    return "\n".join(formatted_payload)


lang_config = {
    "java": {
        "ext": "java",
        "class_id": "%s.%s",
        "object_id": "%s",
        "formatter": format_payload_java,
        "filename": lambda s: f"src/main/java/Demo{s[0].upper()}{s[1:]}.java",
        "indent": 2,
        "continuation_indent": 4,
        "object_indent_offset": 0,
        "class_indent_offset": 0,
        "batch_indent_offset": 0,
        "batch_set_statements": {
            "generic": [
                ".setId(objectId)",
                "            .setClassId(classId)",
                "            .setCardTitle(new LocalizedString().setDefaultValue(new TranslatedString().setLanguage(\"en-US\").setValue(\"TITLE\")))",
                "            .setHeader(new LocalizedString().setDefaultValue(new TranslatedString().setLanguage(\"en-US\").setValue(\"HEADER\")));",
            ],
            "offer": [
                ".setId(objectId)",
                "            .setClassId(classId)",
                "            .setState(\"ACTIVE\");",
            ],
            "loyalty": [
                ".setId(objectId)",
                "            .setClassId(classId)",
                "            .setState(\"ACTIVE\");",
            ],
            "giftCard": [
                ".setId(objectId)",
                "            .setClassId(classId)",
                "            .setState(\"ACTIVE\")",
                "            .setCardNumber(\"CARD_NUMBER\");",
            ],
            "eventTicket": [
                ".setId(objectId)",
                "            .setClassId(classId)",
                "            .setState(\"ACTIVE\");",
            ],
            "flight": [
                ".setId(objectId)",
                "            .setClassId(classId)",
                "            .setState(\"ACTIVE\")",
                "            .setPassengerName(\"NAME\")",
                "            .setReservationInfo(new ReservationInfo());",
            ],
            "transit": [
                ".setId(objectId)",
                "            .setClassId(classId)",
                "            .setState(\"ACTIVE\")",
                "            .setTripType(\"ONE_WAY\");",
            ]
        },
    },
    "python": {
        "ext": "py",
        "class_id": 'f"{ISSUER_ID}.{CLASS_ID}"',
        "object_id": "OBJECT_ID",
        "indent": 4,
        "continuation_indent": 4,
        "object_indent_offset": 0,
        "class_indent_offset": 0,
        "batch_indent_offset": 4,
        "filename": lambda s: f"demo_{s.lower()}.py",
        "batch_set_statements": {
            "generic": [],
            "offer": [],
            "loyalty": [],
            "giftCard": [],
            "eventTicket": [],
            "flight": [],
            "transit": [],
        },
    },
    "nodejs": {
        "ext": "js",
        "class_id": "`${issuerId}.${classId}`",
        "object_id": "objectId",
        "indent": 2,
        "continuation_indent": 4,
        "object_indent_offset": 2,
        "class_indent_offset": 2,
        "batch_indent_offset": 4,
        "filename": lambda s: f"demo-{s.lower()}.js",
        "batch_set_statements": {
            "generic": [],
            "offer": [],
            "loyalty": [],
            "giftCard": [],
            "eventTicket": [],
            "flight": [],
            "transit": [],
        },
    },
    "php": {
        "ext": "php",
        "class_id": '"{$issuerId}.{$classId}"',
        "object_id": '"{$objectId}"',
        "indent": 2,
        "continuation_indent": 4,
        "object_indent_offset": 0,
        "class_indent_offset": 0,
        "batch_indent_offset": 0,
        "filename": lambda s: f"demo_{s.lower()}.php",
        "batch_set_statements": {
            "generic": [
                "$$object_typeObject->setId($objectId);",
                "  $$object_typeObject->setClassId(\"$issuerId.$classId\");",
                "  $$object_typeObject->setCardTitle(new LocalizedString().setDefaultValue(new TranslatedString().setLanguage(\"en-US\").setValue(\"TITLE\")));",
                "  $$object_typeObject->setHeader(new LocalizedString().setDefaultValue(new TranslatedString().setLanguage(\"en-US\").setValue(\"HEADER\")));",
            ],
            "offer": [
                "$$object_typeObject->setId($objectId);",
                "  $$object_typeObject->setClassId(\"$issuerId.$classId\");",
                "  $$object_typeObject->setState(\"ACTIVE\");",
            ],
            "loyalty": [
                "$$object_typeObject->setId($objectId);",
                "  $$object_typeObject->setClassId(\"$issuerId.$classId\");",
                "  $$object_typeObject->setState(\"ACTIVE\");",
            ],
            "giftCard": [
                "$$object_typeObject->setId($objectId);",
                "  $$object_typeObject->setClassId(\"$issuerId.$classId\");",
                "  $$object_typeObject->setState(\"ACTIVE\");",
                "  $$object_typeObject->setCardNumber(\"CARD_NUMBER\");",
            ],
            "eventTicket": [
                "$$object_typeObject->setId($objectId);",
                "  $$object_typeObject->setClassId(\"$issuerId.$classId\");",
                "  $$object_typeObject->setState(\"ACTIVE\");",
            ],
            "flight": [
                "$$object_typeObject->setId($objectId);",
                "  $$object_typeObject->setClassId(\"$issuerId.$classId\");",
                "  $$object_typeObject->setState(\"ACTIVE\");",
                "  $$object_typeObject->setPassengerName(\"NAME\");",
                "  $$object_typeObject->setReservationInfo(new Google_Service_Walletobjects_ReservationInfo());",
            ],
            "transit": [
                "$$object_typeObject->setId($objectId);",
                "  $$object_typeObject->setClassId(\"$issuerId.$classId\");",
                "  $$object_typeObject->setState(\"ACTIVE\");",
                "  $$object_typeObject->setTripType(\"ONE_WAY\");",
            ]
        },
    },
    "dotnet": {
        "ext": "cs",
        "class_id": '$"{issuerId}.{classId}"',
        "object_id": "objectId",
        "formatter": format_payload_dotnet,
        "filename": format_filename_dotnet,
        "indent": 2,
        "continuation_indent": 4,
        "object_indent_offset": 4,
        "class_indent_offset": 4,
        "batch_indent_offset": 6,
        "batch_set_statements": {
            "generic": [],
            "offer": [],
            "loyalty": [],
            "giftCard": [],
            "eventTicket": [],
            "flight": [],
            "transit": [],
        },
    },
    "http": {
        "ext": "http",
        "class_id": "\"issuer-id.class-id\"",
        "object_id": "\"issuer-id.user-id\"",
        "filename": lambda s: f"demo_{s.lower()}.http",
        "indent": 2,
        "continuation_indent": 2,
        "object_indent_offset": 0,
        "class_indent_offset": 0,
        "batch_indent_offset": 0,
        "batch_set_statements": {
            "generic": [],
            "offer": [],
            "loyalty": [],
            "giftCard": [],
            "eventTicket": [],
            "flight": [],
            "transit": [],
        },
    },
}

path = lambda *s: os.path.join(os.path.dirname(os.path.abspath(__file__)), *s)

for lang, config in lang_config.items():
    # Get the language specific template file
    with open(path(f"template.{config['ext']}"), "r", encoding="utf-8") as f:
        template = f.read()

    for object_type, content in payloads.items():
        output = template

        # JSON payloads
        for name, value in content.items():
            if name == "$object_payload":
                payload_offset = config.get("object_indent_offset", 0)
            else:
                payload_offset = config.get("class_indent_offset", 0)
            batch_offset = config.get("batch_indent_offset", 0)

            payload = json.dumps(value, indent=config.get("indent", 2))
            if "formatter" in config:
                payload = config["formatter"](payload)

            if batch_offset > 0:
                batch_payload = format_with_offset(payload, batch_offset)
            else:
                batch_payload = payload
            if payload_offset > 0:
                payload = format_with_offset(payload, payload_offset)

            output = output.replace(f"{name}_batch", batch_payload)
            output = output.replace(name, payload)

        # code placeholders
        config["object_type"] = object_type
        config[
            "object_type_title"] = f"{object_type[0].upper()}{object_type[1:]}"
        config["object_type_lower"] = object_type.lower()
        config[
            "api_url"] = f"{BASE_URL}{url_map.get(object_type, '/generic/rest/v1/genericobject')}"
        config["batch_statement"] = "\n".join(
            config["batch_set_statements"][object_type]).replace(
                "$object_type", object_type)

        for name in ("object_type_title", "object_type_lower", "object_type",
                     "class_id", "object_id", "api_url", "batch_statement"):
            output = output.replace(f'"${name}"', config[name])
            output = output.replace(f"${name}", config[name])

        with open(path("..", lang, config["filename"](object_type)),
                  "w",
                  encoding="utf-8") as f:
            f.write(output)
