# Google Wallet Go samples

## Overview

The files in this directory each implement a demo type for a specific Google
Wallet pass type. Each demo type has methods implemented for performing tasks such as
creating a pass class, updating issuer permissions, and more.

| Pass type                  | File                                           |
|----------------------------|------------------------------------------------|
| Event tickets              | [`demo_eventticket.go`](./demo_eventticket.go) |
| Flight boarding passes     | [`demo_flight.go`](./demo_flight.go)           |
| Generic passes             | [`demo_generic.go`](./demo_generic.go)         |
| Gift cards                 | [`demo_giftcard.go`](./demo_giftcard.go)       |
| Loyalty program membership | [`demo_loyalty.go`](./demo_loyalty.go)         |
| Offers and promotions      | [`demo_offer.go`](./demo_offer.go)             |
| Transit passes             | [`demo_transit.go`](./demo_transit.go)         |

## Prerequisites

*   Go 1.20.x
*   Follow the steps outlined in the
    [Google Wallet prerequisites](https://developers.google.com/wallet/generic/web/prerequisites)
    to create the Google Wallet issuer account and Google Cloud service account

## Environment variables

The following environment variables must be set. Alternatively, you can update
the code files to set the values directly.

| Enviroment variable              | Description                                     | Example             |
|----------------------------------|-------------------------------------------------|---------------------|
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to a Google Cloud service account key file | `/path/to/key.json` |
| `WALLET_ISSUER_ID`               | Your Google Wallet Issuer ID                    | 1234567890          |

## How to use the code samples

1.  First install the dependencies for the sample you wish to run (this isn't necessary a second time for running subsequent samples)

    ```bash
    go install demo_eventticket.go
    ```

2.  Run the sample

    ```bash
    go run demo_eventticket.go
    ```

3.  Optionally, you can manually copy the demo type in your own project. An example
    can be found below

    ```go
    // Create a demo type instance
    // Creates the authenticated HTTP client
    d := demoEventticket{}
    d.auth()

    // Create a pass class
    d.createClass(issuerId, classSuffix)

    // Create a pass object
    d.createObject(issuerId, classSuffix, objectSuffix)

    // Expire a pass object
    d.expireObject(issuerId, objectSuffix)

    // Create an "Add to Google Wallet" link
    // that generates a new pass class and object
    d.createJwtNewObjects(issuerId, classSuffix, objectSuffix)

    // Create an "Add to Google Wallet" link
    // that references existing pass classes and objects
    d.createJwtExistingObjects(issuerId)

    // Create pass objects in batch
    d.batchCreateObjects(issuerId, classSuffix)
    ```
