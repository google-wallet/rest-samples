# Google Wallet Java samples

## Overview

The files in this directory each implement a demo class for a specific Google
Wallet pass type. Each class implements methods for performing tasks such as
creating a pass class, updating issuer permissions, and more.

| Pass type | File |
|-----------|------|
| Event tickets | [DemoEventTicket.cs](./DemoEventTicket.cs) |
| Flight boarding passes | [DemoFlight.cs](./DemoFlight.cs) |
| Generic passes | [DemoGeneric.cs](./DemoGeneric.cs) |
| Gift cards | [DemoGiftCard.cs](./DemoGiftCard.cs) |
| Loyalty program membership | [DemoLoyalty.cs](./DemoLoyalty.cs) |
| Offers and promotions | [DemoOffer.cs](./DemoOffer.cs) |
| Transit passes | [DemoTransit.cs](./DemoTransit.cs) |

## Prerequisites

* Java 17+
* JDK 11+
* Follow the steps outlined in the [Google Wallet prerequisites](https://developers.google.com/wallet/generic/web/prerequisites) to create the Google Wallet issuer account and Google Cloud service account
* Download the Java
[Google Wallet API Client library](https://developers.google.com/wallet/generic/resources/libraries#java)

## Environment variables

The following environment variables must be set. Alternatively, you can update
the code files to set the values directly. They can be found in the constructor
for each class file.

| Enviroment variable | Description | Example |
|---------------------|-------------|---------|
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to a Google Cloud service account key file | `/path/to/key.json` |

## How to use the code samples

1. Open the [`java`](./java/) project folder in your editor of choice.
2. Copy the path to the Google Wallet API Client library (
`libwalletobjects_public_java_lib_v1.jar` file) you downloaded. If needed,
update the path in [`build.gradle`](./build.gradle) (line 14).

    ```plain
    implementation files('lib/libwalletobjects_public_java_lib_v1.jar')
    ```

3. Build the project to install the dependencies.
4. In your Java code, import a demo class and call its method(s). An example
can be found below

    ```java
    // Create a demo class instance
    DemoEventTicket demo = new DemoEventTicket();

    // Create the authenticated HTTP client
    demo.Auth();

    // Create a pass class
    demo.CreateEventTicketClass("issuer_id", "class_suffix");

    // Create a pass object
    demo.CreateEventTicketObject("issuer_id", "class_suffix", "user_id");

    // Create an Add to Google Wallet link
    demo.CreateJWTSaveURL("issuer_id", "class_suffix", "user_id");

    // Create an issuer account
    demo.CreateIssuerAccount("issuer_name", "issuer_email");

    // Create pass objects in batch
    demo.BatchCreateEventTicketObjects("issuer_id", "class_suffix");
    ```
