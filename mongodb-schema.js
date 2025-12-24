// DATABASE: inventory_logs
use("inventory_logs");

// COLLECTION: product_reviews
db.createCollection("product_reviews");

db.product_reviews.insertOne({
  productId: 1,
  rating: 5,
  comment: "Excellent product quality",
  createdAt: new Date()
});


// COLLECTION: user_activity_logs
db.createCollection("user_activity_logs");

db.user_activity_logs.insertOne({
  userId: 1,
  action: "CREATE_ORDER",
  metadata: {
    orderId: 2
  },
  timestamp: new Date()
});

// COLLECTION: system_events
db.createCollection("system_events");

db.system_events.insertOne({
  eventType: "ORDER_RECEIVED",
  referenceId: 2,
  message: "Purchase order received and inventory updated",
  createdAt: new Date()
});
