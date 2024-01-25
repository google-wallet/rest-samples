# Google Wallet Java samples

## Overview

The files in this directory each implement a demo class for a specific Google
Wallet pass type. Each class implements methods for performing tasks such as
creating a pass class, updating issuer permissions, and more.

| Pass type                  | File                                                         |
|----------------------------|--------------------------------------------------------------|
| Event tickets              | [com.google.developers.wallet.rest.DemoEventTicket.java](./src/main/java/com.google.developers.wallet.rest.DemoEventTicket.java) |
| Flight boarding passes     | [com.google.developers.wallet.rest.DemoFlight.java](./src/main/java/com.google.developers.wallet.rest.DemoFlight.java)           |
| Generic passes             | [com.google.developers.wallet.rest.DemoGeneric.java](./src/main/java/com.google.developers.wallet.rest.DemoGeneric.java)         |
| Gift cards                 | [com.google.developers.wallet.rest.DemoGiftCard.java](./src/main/java/com.google.developers.wallet.rest.DemoGiftCard.java)       |
| Loyalty program membership | [com.google.developers.wallet.rest.DemoLoyalty.java](./src/main/java/com.google.developers.wallet.rest.DemoLoyalty.java)         |
| Offers and promotions      | [com.google.developers.wallet.rest.DemoOffer.java](./src/main/java/com.google.developers.wallet.rest.DemoOffer.java)             |
| Transit passes             | [com.google.developers.wallet.rest.DemoTransit.java](./src/main/java/com.google.developers.wallet.rest.DemoTransit.java)         |

## Prerequisites

*   Java 11+
*   JDK 11+
*   Follow the steps outlined in the
    [Google Wallet prerequisites](https://developers.google.com/wallet/generic/web/prerequisites)
    to create the Google Wallet issuer account and Google Cloud service account
*   Download the Java
    [Google Wallet API Client library](https://developers.google.com/wallet/generic/resources/libraries#java)

## Environment variables

The following environment variables must be set. Alternatively, you can update
the code files to set the values directly. They can be found in the constructor
for each class file.

| Enviroment variable              | Description                                     | Example             |
|----------------------------------|-------------------------------------------------|---------------------|
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to a Google Cloud service account key file | `/path/to/key.json` |

## How to use the code samples

1.  Open the [`java`](./java/) project folder in your editor of choice.
2.  Copy the path to the Google Wallet API Client library (
    `libwalletobjects_public_java_lib_v1.jar` file) you downloaded. If needed,
    update the path in [`build.gradle`](./build.gradle) (line 14).

    ```plain
    implementation files('lib/libwalletobjects_public_java_lib_v1.jar')
    ```

3.  Build the project to install the dependencies.
4.  In your Java code, import a demo class and call its method(s). An example
    can be found below

    ```java
    // Create a demo class instance
    // Creates the authenticated HTTP client
    com.google.developers.wallet.rest.DemoEventTicket demo = new com.google.developers.wallet.rest.DemoEventTicket();

    // Create a pass class
    demo.createClass("issuer_id", "class_suffix");

    // Update a pass class
    demo.updateClass("issuer_id", "class_suffix");

    // Patch a pass class
    demo.patchClass("issuer_id", "class_suffix");

    // Add a message to a pass class
    demo.addClassMessage("issuer_id", "class_suffix", "header", "body");

    // Create a pass object
    demo.createObject("issuer_id", "class_suffix", "object_suffix");

    // Update a pass object
    demo.updateObject("issuer_id", "object_suffix");

    // Patch a pass object
    demo.patchObject("issuer_id", "object_suffix");

    // Add a message to a pass object
    demo.addObjectMessage("issuer_id", "object_suffix", "header", "body");

    // Expire a pass object
    demo.expireObject("issuer_id", "object_suffix");

    // Generate an Add to Google Wallet link that creates a new pass class and object
    demo.createJWTNewObjects("issuer_id", "class_suffix", "object_suffix");

    // Generate an Add to Google Wallet link that references existing pass object(s)
    demo.createJWTExistingObjects("issuer_id");

    // Create pass objects in batch
    demo.batchCreateObjects("issuer_id", "class_suffix");
    ```
