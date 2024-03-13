const { DemoEventTicket } = require('./demo-eventticket.js');
const { DemoFlight } = require('./demo-flight.js');
const { DemoGeneric } = require('./demo-generic.js');
const { DemoGiftCard } = require('./demo-giftcard.js');
const { DemoLoyalty } = require('./demo-loyalty.js');
const { DemoOffer } = require('./demo-offer.js');
const { DemoTransit } = require('./demo-transit.js');

async function main() {

  // Create a demo class instance
  // Creates the authenticated HTTP client
  let demo = new DemoEventTicket(); // change to demo a different pass type

  const issuer_id = process.env.WALLET_ISSUER_ID || 'your-issuer-id';
  const class_suffix = (process.env.WALLET_CLASS_SUFFIX || 'your-class-suffix') + demo.constructor.name;
  const object_suffix = (process.env.WALLET_OBJECT_SUFFIX || 'your-object-suffix') + demo.constructor.name;

  // Create a pass class
  demo.createClass(issuer_id, class_suffix);

  // Update a pass class
  demo.updateClass(issuer_id, class_suffix);

  // Patch a pass class
  demo.patchClass(issuer_id, class_suffix);

  // // Create a pass object
  demo.createObject(issuer_id, class_suffix, object_suffix);

  // Update a pass object
  demo.updateObject(issuer_id, object_suffix);

  // Patch a pass object
  demo.patchObject(issuer_id, object_suffix);

  // Expire a pass object
  demo.expireObject(issuer_id, object_suffix);

  // Generate an Add to Google Wallet link that creates a new pass class and object
  demo.createJwtNewObjects(issuer_id, class_suffix, object_suffix);

  // Generate an Add to Google Wallet link that references existing pass object(s)
  demo.createJwtExistingObjects(issuer_id);

  // // Create pass objects in batch
  demo.batchCreateObjects(issuer_id, class_suffix);

}

main().catch(console.error);