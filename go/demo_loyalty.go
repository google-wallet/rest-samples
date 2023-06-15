/*
 * Copyright 2023 Google Inc.
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
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"github.com/golang-jwt/jwt"
	"github.com/google/uuid"
	"golang.org/x/oauth2"
	"golang.org/x/oauth2/google"
	oauthJwt "golang.org/x/oauth2/jwt"
	"io"
	"net/http"
	"os"
	"strings"
)

// [END imports]

const (
	batchUrl  = "https://walletobjects.googleapis.com/batch"
	classUrl  = "https://walletobjects.googleapis.com/walletobjects/v1/loyaltyClass"
	objectUrl = "https://walletobjects.googleapis.com/walletobjects/v1/loyaltyObject"
)

// [END setup]

type demoLoyalty struct {
	credentials                   *oauthJwt.Config
	httpClient                    *http.Client
	batchUrl, classUrl, objectUrl string
}

// [START auth]
// Create authenticated HTTP client using a service account file.
func (d *demoLoyalty) auth() {
	b, _ := os.ReadFile(os.Getenv("GOOGLE_APPLICATION_CREDENTIALS"))
	credentials, _ := google.JWTConfigFromJSON(b, "https://www.googleapis.com/auth/wallet_object.issuer")
	d.credentials = credentials
	d.httpClient = d.credentials.Client(oauth2.NoContext)
}

// [END auth]

// [START createClass]
// Create a class.
func (d *demoLoyalty) createClass(issuerId, classSuffix string) {
	newClass := fmt.Sprintf(`
	{
		"programName": "Program name",
		"issuerName": "Issuer name",
		"reviewStatus": "UNDER_REVIEW",
		"id": "%s.%s",
		"programLogo": {
			"contentDescription": {
				"defaultValue": {
					"value": "Logo description",
					"language": "en-US"
				}
			},
			"sourceUri": {
				"uri": "http://farm8.staticflickr.com/7340/11177041185_a61a7f2139_o.jpg"
			}
		}
	}
	`, issuerId, classSuffix)

	res, err := d.httpClient.Post(classUrl, "application/json", bytes.NewBuffer([]byte(newClass)))

	if err != nil {
		fmt.Println(err)
	} else {
		b, _ := io.ReadAll(res.Body)
		fmt.Printf("Class insert response:\n%s\n", b)
	}
}

// [END createClass]

// [START createObject]
// Create an object.
func (d *demoLoyalty) createObject(issuerId, classSuffix, objectSuffix string) {
	newObject := fmt.Sprintf(`
	{
		"classId": "%s.%s",
		"heroImage": {
			"contentDescription": {
				"defaultValue": {
					"value": "Hero image description",
					"language": "en-US"
				}
			},
			"sourceUri": {
				"uri": "https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg"
			}
		},
		"barcode": {
			"type": "QR_CODE",
			"value": "QR code"
		},
		"locations": [
			{
				"latitude": 37.424015499999996,
				"longitude": -122.09259560000001
			}
		],
		"accountName": "Account name",
		"state": "ACTIVE",
		"linksModuleData": {
			"uris": [
				{
					"id": "LINK_MODULE_URI_ID",
					"uri": "http://maps.google.com/",
					"description": "Link module URI description"
				},
				{
					"id": "LINK_MODULE_TEL_ID",
					"uri": "tel:6505555555",
					"description": "Link module tel description"
				}
			]
		},
		"imageModulesData": [
			{
				"id": "IMAGE_MODULE_ID",
				"mainImage": {
					"contentDescription": {
						"defaultValue": {
							"value": "Image module description",
							"language": "en-US"
						}
					},
					"sourceUri": {
						"uri": "http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg"
					}
				}
			}
		],
		"textModulesData": [
			{
				"body": "Text module body",
				"header": "Text module header",
				"id": "TEXT_MODULE_ID"
			}
		],
		"id": "%s.%s",
		"loyaltyPoints": {
			"balance": {
				"int": 800
			},
			"label": "Points"
		},
		"accountId": "Account id"
	}
	`, issuerId, classSuffix, issuerId, objectSuffix)

	res, err := d.httpClient.Post(objectUrl, "application/json", bytes.NewBuffer([]byte(newObject)))

	if err != nil {
		fmt.Println(err)
	} else {
		b, _ := io.ReadAll(res.Body)
		fmt.Printf("Object insert response:\n%s\n", b)
	}
}

// [END createObject]

// [START expireObject]
// Expire an object.
//
// Sets the object's state to Expired. If the valid time interval is
// already set, the pass will expire automatically up to 24 hours after.
func (d *demoLoyalty) expireObject(issuerId, objectSuffix string) {
	patchBody := `{"state": "EXPIRED"}`
	url := fmt.Sprintf("%s/%s.%s", objectUrl, issuerId, objectSuffix)
	req, _ := http.NewRequest(http.MethodPatch, url, bytes.NewBuffer([]byte(patchBody)))
	res, err := d.httpClient.Do(req)

	if err != nil {
		fmt.Println(err)
	} else {
		b, _ := io.ReadAll(res.Body)
		fmt.Printf("Object expiration response:\n%s\n", b)
	}
}

// [END expireObject]

// [START jwtNew]
// Generate a signed JWT that creates a new pass class and object.
//
// When the user opens the "Add to Google Wallet" URL and saves the pass to
// their wallet, the pass class and object defined in the JWT are
// created. This allows you to create multiple pass classes and objects in
// one API call when the user saves the pass to their wallet.
func (d *demoLoyalty) createJwtNewObjects(issuerId, classSuffix, objectSuffix string) {
	newClass := fmt.Sprintf(`
	{
		"programName": "Program name",
		"issuerName": "Issuer name",
		"reviewStatus": "UNDER_REVIEW",
		"id": "%s.%s",
		"programLogo": {
			"contentDescription": {
				"defaultValue": {
					"value": "Logo description",
					"language": "en-US"
				}
			},
			"sourceUri": {
				"uri": "http://farm8.staticflickr.com/7340/11177041185_a61a7f2139_o.jpg"
			}
		}
	}
	`, issuerId, classSuffix)

	newObject := fmt.Sprintf(`
	{
		"classId": "%s.%s",
		"heroImage": {
			"contentDescription": {
				"defaultValue": {
					"value": "Hero image description",
					"language": "en-US"
				}
			},
			"sourceUri": {
				"uri": "https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg"
			}
		},
		"barcode": {
			"type": "QR_CODE",
			"value": "QR code"
		},
		"locations": [
			{
				"latitude": 37.424015499999996,
				"longitude": -122.09259560000001
			}
		],
		"accountName": "Account name",
		"state": "ACTIVE",
		"linksModuleData": {
			"uris": [
				{
					"id": "LINK_MODULE_URI_ID",
					"uri": "http://maps.google.com/",
					"description": "Link module URI description"
				},
				{
					"id": "LINK_MODULE_TEL_ID",
					"uri": "tel:6505555555",
					"description": "Link module tel description"
				}
			]
		},
		"imageModulesData": [
			{
				"id": "IMAGE_MODULE_ID",
				"mainImage": {
					"contentDescription": {
						"defaultValue": {
							"value": "Image module description",
							"language": "en-US"
						}
					},
					"sourceUri": {
						"uri": "http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg"
					}
				}
			}
		],
		"textModulesData": [
			{
				"body": "Text module body",
				"header": "Text module header",
				"id": "TEXT_MODULE_ID"
			}
		],
		"id": "%s.%s",
		"loyaltyPoints": {
			"balance": {
				"int": 800
			},
			"label": "Points"
		},
		"accountId": "Account id"
	}
	`, issuerId, classSuffix, issuerId, objectSuffix)

	var payload map[string]interface{}
	json.Unmarshal([]byte(fmt.Sprintf(`
	{
		"genericClasses": [%s],
		"genericObjects": [%s]
	}
	`, newClass, newObject)), &payload)

	claims := jwt.MapClaims{
		"iss":     d.credentials.Email,
		"aud":     "google",
		"origins": []string{"www.example.com"},
		"typ":     "savetowallet",
		"payload": payload,
	}

	// The service account credentials are used to sign the JWT
	key, _ := jwt.ParseRSAPrivateKeyFromPEM(d.credentials.PrivateKey)
	token, _ := jwt.NewWithClaims(jwt.SigningMethodRS256, claims).SignedString(key)

	fmt.Println("Add to Google Wallet link")
	fmt.Println("https://pay.google.com/gp/v/save/" + token)
}

// [END jwtNew]

// [START jwtExisting]
// Generate a signed JWT that references an existing pass object.

// When the user opens the "Add to Google Wallet" URL and saves the pass to
// their wallet, the pass objects defined in the JWT are added to the
// user's Google Wallet app. This allows the user to save multiple pass
// objects in one API call.
func (d *demoLoyalty) createJwtExistingObjects(issuerId string) {
	var payload map[string]interface{}
	json.Unmarshal([]byte(fmt.Sprintf(`
	{
		"eventTicketObjects": [{
			"id": "%s.EVENT_OBJECT_SUFFIX",
			"classId": "%s.EVENT_CLASS_SUFFIX"
		}],

		"flightObjects": [{
			"id": "%s.FLIGHT_OBJECT_SUFFIX",
			"classId": "%s.FLIGHT_CLASS_SUFFIX"
		}],

		"genericObjects": [{
			"id": "%s.GENERIC_OBJECT_SUFFIX",
			"classId": "%s.GENERIC_CLASS_SUFFIX"
		}],

		"giftCardObjects": [{
			"id": "%s.GIFT_CARD_OBJECT_SUFFIX",
			"classId": "%s.GIFT_CARD_CLASS_SUFFIX"
		}],

		"loyaltyObjects": [{
			"id": "%s.LOYALTY_OBJECT_SUFFIX",
			"classId": "%s.LOYALTY_CLASS_SUFFIX"
		}],

		"offerObjects": [{
			"id": "%s.OFFER_OBJECT_SUFFIX",
			"classId": "%s.OFFER_CLASS_SUFFIX"
		}],

		"transitObjects": [{
			"id": "%s.TRANSIT_OBJECT_SUFFIX",
			"classId": "%s.TRANSIT_CLASS_SUFFIX"
		}]
	}
	`, issuerId)), &payload)

	claims := jwt.MapClaims{
		"iss":     d.credentials.Email,
		"aud":     "google",
		"origins": []string{"www.example.com"},
		"typ":     "savetowallet",
		"payload": payload,
	}

	// The service account credentials are used to sign the JWT
	key, _ := jwt.ParseRSAPrivateKeyFromPEM(d.credentials.PrivateKey)
	token, _ := jwt.NewWithClaims(jwt.SigningMethodRS256, claims).SignedString(key)

	fmt.Println("Add to Google Wallet link")
	fmt.Println("https://pay.google.com/gp/v/save/" + token)
}

// [END jwtExisting]

// [START batch]
// Batch create Google Wallet objects from an existing class.
func (d *demoLoyalty) batchCreateObjects(issuerId, classSuffix string) {
	data := ""
	for i := 0; i < 3; i++ {
		objectSuffix := strings.ReplaceAll(uuid.New().String(), "-", "_")

		batchObject := fmt.Sprintf(`
		{
			"classId": "%s.%s",
			"heroImage": {
				"contentDescription": {
					"defaultValue": {
						"value": "Hero image description",
						"language": "en-US"
					}
				},
				"sourceUri": {
					"uri": "https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg"
				}
			},
			"barcode": {
				"type": "QR_CODE",
				"value": "QR code"
			},
			"locations": [
				{
					"latitude": 37.424015499999996,
					"longitude": -122.09259560000001
				}
			],
			"accountName": "Account name",
			"state": "ACTIVE",
			"linksModuleData": {
				"uris": [
					{
						"id": "LINK_MODULE_URI_ID",
						"uri": "http://maps.google.com/",
						"description": "Link module URI description"
					},
					{
						"id": "LINK_MODULE_TEL_ID",
						"uri": "tel:6505555555",
						"description": "Link module tel description"
					}
				]
			},
			"imageModulesData": [
				{
					"id": "IMAGE_MODULE_ID",
					"mainImage": {
						"contentDescription": {
							"defaultValue": {
								"value": "Image module description",
								"language": "en-US"
							}
						},
						"sourceUri": {
							"uri": "http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg"
						}
					}
				}
			],
			"textModulesData": [
				{
					"body": "Text module body",
					"header": "Text module header",
					"id": "TEXT_MODULE_ID"
				}
			],
			"id": "%s.%s",
			"loyaltyPoints": {
				"balance": {
					"int": 800
				},
				"label": "Points"
			},
			"accountId": "Account id"
		}
		`, issuerId, classSuffix, issuerId, objectSuffix)

		data += "--batch_createobjectbatch\n"
		data += "Content-Type: application/json\n\n"
		data += "POST /walletobjects/v1/loyaltyObject\n\n"
		data += batchObject + "\n\n"
	}
	data += "--batch_createobjectbatch--"

	res, err := d.httpClient.Post(batchUrl, "multipart/mixed; boundary=batch_createobjectbatch", bytes.NewBuffer([]byte(data)))

	if err != nil {
		fmt.Println(err)
	} else {
		b, _ := io.ReadAll(res.Body)
		fmt.Printf("Batch insert response:\n%s\n", b)
	}
}

// [END batch]

func main() {
	if len(os.Args) == 0 {
		fmt.Println("Usage: go run demo_loyalty.go <issuer-id>")
		os.Exit(1)
	}

	issuerId := os.Getenv("WALLET_ISSUER_ID")
	classSuffix := strings.ReplaceAll(uuid.New().String(), "-", "_")
	objectSuffix := fmt.Sprintf("%s-%s", strings.ReplaceAll(uuid.New().String(), "-", "_"), classSuffix)

	d := demoLoyalty{}

	d.auth()
	d.createClass(issuerId, classSuffix)
	d.createObject(issuerId, classSuffix, objectSuffix)
	d.expireObject(issuerId, objectSuffix)
	d.createJwtNewObjects(issuerId, classSuffix, objectSuffix)
	d.createJwtExistingObjects(issuerId)
	d.batchCreateObjects(issuerId, classSuffix)
}
