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
	"context"
	"encoding/json"
	"fmt"
	"github.com/golang-jwt/jwt"
	"github.com/google/uuid"
	"golang.org/x/oauth2"
	"golang.org/x/oauth2/google"
	oauthJwt "golang.org/x/oauth2/jwt"
	"google.golang.org/api/option"
	"google.golang.org/api/walletobjects/v1"
	"io"
	"log"
	"os"
	"strings"
)

// [END imports]
// [END setup]

type demoFlight struct {
	credentials *oauthJwt.Config
	service     *walletobjects.Service
}

// [START auth]
// Create authenticated HTTP client using a service account file.
func (d *demoFlight) auth() {
	credentialsFile := os.Getenv("GOOGLE_APPLICATION_CREDENTIALS")
	b, _ := os.ReadFile(credentialsFile)
	credentials, err := google.JWTConfigFromJSON(b, walletobjects.WalletObjectIssuerScope)
	if err != nil {
		fmt.Println(err)
		log.Fatalf("Unable to load credentials: %v", err)
	}
	d.credentials = credentials
	d.service, _ = walletobjects.NewService(context.Background(), option.WithCredentialsFile(credentialsFile))
}

// [END auth]

// [START createClass]
// Create a class.
func (d *demoFlight) createClass(issuerId, classSuffix string) {
	flightClass := new(walletobjects.FlightClass)
	flightClass.Id = fmt.Sprintf("%s.%s", issuerId, classSuffix)
	flightClass.ReviewStatus = "UNDER_REVIEW"
	flightClass.IssuerName = "Issuer name"
	flightClass.Origin = &walletobjects.AirportInfo{
		Terminal:        "1",
		Gate:            "A2",
		AirportIataCode: "LAX",
	}
	flightClass.Destination = &walletobjects.AirportInfo{
		Terminal:        "2",
		Gate:            "C3",
		AirportIataCode: "SFO",
	}
	flightClass.FlightHeader = &walletobjects.FlightHeader{
		Carrier: &walletobjects.FlightCarrier{
			CarrierIataCode: "LX",
		},
		FlightNumber: "123",
	}
	flightClass.LocalScheduledDepartureDateTime = "2023-06-12T23:20:50"

	res, err := d.service.Flightclass.Insert(flightClass).Do()
	if err != nil {
		log.Fatalf("Unable to insert class: %v", err)
	} else {
		fmt.Printf("Class insert id:\n%v\n", res.Id)
	}
}

// [END createClass]

// [START createObject]
// Create an object.
func (d *demoFlight) createObject(issuerId, classSuffix, objectSuffix string) {
	flightObject := new(walletobjects.FlightObject)
	flightObject.Id = fmt.Sprintf("%s.%s", issuerId, objectSuffix)
	flightObject.ClassId = fmt.Sprintf("%s.%s", issuerId, classSuffix)
	flightObject.State = "ACTIVE"
	flightObject.PassengerName = "Passenger name"
	flightObject.ReservationInfo = &walletobjects.ReservationInfo{
		ConfirmationCode: "Confirmation code",
	}
	flightObject.BoardingAndSeatingInfo = &walletobjects.BoardingAndSeatingInfo{
		BoardingGroup: "B",
		SeatNumber:    "42",
	}
	flightObject.HeroImage = &walletobjects.Image{
		SourceUri: &walletobjects.ImageUri{
			Uri: "https://farm4.staticflickr.com/3723/11177041115_6e6a3b6f49_o.jpg",
		},
	}
	flightObject.Barcode = &walletobjects.Barcode{
		Type:  "QR_CODE",
		Value: "QR code",
	}
	flightObject.Locations = []*walletobjects.LatLongPoint{
		&walletobjects.LatLongPoint{
			Latitude:  37.424015499999996,
			Longitude: -122.09259560000001,
		},
	}
	flightObject.LinksModuleData = &walletobjects.LinksModuleData{
		Uris: []*walletobjects.Uri{
			&walletobjects.Uri{
				Id:          "LINK_MODULE_URI_ID",
				Uri:         "http://maps.google.com/",
				Description: "Link module URI description",
			},
			&walletobjects.Uri{
				Id:          "LINK_MODULE_TEL_ID",
				Uri:         "tel:6505555555",
				Description: "Link module tel description",
			},
		},
	}
	flightObject.ImageModulesData = []*walletobjects.ImageModuleData{
		&walletobjects.ImageModuleData{
			Id: "IMAGE_MODULE_ID",
			MainImage: &walletobjects.Image{
				SourceUri: &walletobjects.ImageUri{
					Uri: "http://farm4.staticflickr.com/3738/12440799783_3dc3c20606_b.jpg",
				},
			},
		},
	}
	flightObject.TextModulesData = []*walletobjects.TextModuleData{
		&walletobjects.TextModuleData{
			Body:   "Text module body",
			Header: "Text module header",
			Id:     "TEXT_MODULE_ID",
		},
	}

	res, err := d.service.Flightobject.Insert(flightObject).Do()
	if err != nil {
		log.Fatalf("Unable to insert object: %v", err)
	} else {
		fmt.Printf("Object insert id:\n%s\n", res.Id)
	}
}

// [END createObject]

// [START expireObject]
// Expire an object.
//
// Sets the object's state to Expired. If the valid time interval is
// already set, the pass will expire automatically up to 24 hours after.
func (d *demoFlight) expireObject(issuerId, objectSuffix string) {
	flightObject := &walletobjects.FlightObject{
		State: "EXPIRED",
	}
	res, err := d.service.Flightobject.Patch(fmt.Sprintf("%s.%s", issuerId, objectSuffix), flightObject).Do()
	if err != nil {
		log.Fatalf("Unable to patch object: %v", err)
	} else {
		fmt.Printf("Object expiration id:\n%s\n", res.Id)
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
func (d *demoFlight) createJwtNewObjects(issuerId, classSuffix, objectSuffix string) {
	flightObject := new(walletobjects.FlightObject)
	flightObject.Id = fmt.Sprintf("%s.%s", issuerId, objectSuffix)
	flightObject.ClassId = fmt.Sprintf("%s.%s", issuerId, classSuffix)
	flightObject.State = "ACTIVE"
	flightObject.PassengerName = "Passenger name"
	flightObject.ReservationInfo = &walletobjects.ReservationInfo{
		ConfirmationCode: "Confirmation code",
	}

	flightJson, _ := json.Marshal(flightObject)
	var payload map[string]any
	json.Unmarshal([]byte(fmt.Sprintf(`
	{
		"flightObjects": [%s]
	}
	`, flightJson)), &payload)
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
func (d *demoFlight) createJwtExistingObjects(issuerId string, classSuffix string, objectSuffix string) {
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

		"flightObjects": [{
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
func (d *demoFlight) batchCreateObjects(issuerId, classSuffix string) {
	data := ""
	for i := 0; i < 3; i++ {
		objectSuffix := strings.ReplaceAll(uuid.New().String(), "-", "_")

		flightObject := new(walletobjects.FlightObject)
		flightObject.Id = fmt.Sprintf("%s.%s", issuerId, objectSuffix)
		flightObject.ClassId = fmt.Sprintf("%s.%s", issuerId, classSuffix)
		flightObject.State = "ACTIVE"
		flightObject.PassengerName = "Passenger name"
		flightObject.ReservationInfo = &walletobjects.ReservationInfo{
			ConfirmationCode: "Confirmation code",
		}

		flightJson, _ := json.Marshal(flightObject)
		batchObject := fmt.Sprintf("%s", flightJson)

		data += "--batch_createobjectbatch\n"
		data += "Content-Type: application/json\n\n"
		data += "POST /walletobjects/v1/flightObject\n\n"
		data += batchObject + "\n\n"
	}
	data += "--batch_createobjectbatch--"

	res, err := d.credentials.Client(oauth2.NoContext).Post("https://walletobjects.googleapis.com/batch", "multipart/mixed; boundary=batch_createobjectbatch", bytes.NewBuffer([]byte(data)))

	if err != nil {
		fmt.Println(err)
	} else {
		b, _ := io.ReadAll(res.Body)
		fmt.Printf("Batch insert response:\n%s\n", b)
	}
}

// [END batch]

func main() {
	issuerId := os.Getenv("WALLET_ISSUER_ID")
	classSuffix := strings.ReplaceAll(uuid.New().String(), "-", "_")
	objectSuffix := fmt.Sprintf("%s-%s", strings.ReplaceAll(uuid.New().String(), "-", "_"), classSuffix)

	d := demoFlight{}

	d.auth()
	d.createClass(issuerId, classSuffix)
	d.createObject(issuerId, classSuffix, objectSuffix)
	d.expireObject(issuerId, objectSuffix)
	d.createJwtNewObjects(issuerId, classSuffix, objectSuffix)
	d.createJwtExistingObjects(issuerId, classSuffix, objectSuffix)
	d.batchCreateObjects(issuerId, classSuffix)
}
