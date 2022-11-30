# Google Wallet Java samples

## Overview

The files in this directory each implement a demo class for a specific Google
Wallet pass type. Each class implements methods for performing tasks such as
creating a pass class, updating issuer permissions, and more.

| Pass type                  | File                                                         |
|----------------------------|--------------------------------------------------------------|
| Event tickets              | [DemoEventTicket.java](./src/main/java/DemoEventTicket.java) |
| Flight boarding passes     | [DemoFlight.java](./src/main/java/DemoFlight.java)           |
| Generic passes             | [DemoGeneric.java](./src/main/java/DemoGeneric.java)         |
| Gift cards                 | [DemoGiftCard.java](./src/main/java/DemoGiftCard.java)       |
| Loyalty program membership | [DemoLoyalty.java](./src/main/java/DemoLoyalty.java)         |
| Offers and promotions      | [DemoOffer.java](./src/main/java/DemoOffer.java)             |
| Transit passes             | [DemoTransit.java](./src/main/java/DemoTransit.java)         |

## Prerequisites

*   Java 17+
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
    DemoEventTicket demo = new DemoEventTicket();

    // Create a pass class
    demo.CreateClass("issuer_id", "class_suffix");

    // Update a pass class
    demo.UpdateClass("issuer_id", "class_suffix");

    // Patch a pass class
    demo.PatchClass("issuer_id", "class_suffix");

    // Add a message to a pass class
    demo.AddClassMessage("issuer_id", "class_suffix", "header", "body");

    // Create a pass object
    demo.CreateObject("issuer_id", "class_suffix", "object_suffix");

    // Update a pass object
    demo.UpdateObject("issuer_id", "object_suffix");

    // Patch a pass object
    demo.PatchObject("issuer_id", "object_suffix");

    // Add a message to a pass object
    demo.AddObjectMessage("issuer_id", "object_suffix", "header", "body");

    // Expire a pass object
    demo.ExpireObject("issuer_id", "object_suffix");

    // Generate an Add to Google Wallet link that creates a new pass class and object
    demo.CreateJWTNewObjects("issuer_id", "class_suffix", "object_suffix");

    // Generate an Add to Google Wallet link that references existing pass object(s)
    demo.CreateJWTExistingObjects("issuer_id");

    // Create pass objects in batch
    demo.BatchCreateObjects("issuer_id", "class_suffix");
    ```
