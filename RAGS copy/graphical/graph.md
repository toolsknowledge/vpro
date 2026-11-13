// 1. Create nodes
MERGE (rahul:Customer {name: "Rahul"})
MERGE (iphone:Product {name: "iPhone 16"})
MERGE (apple:Brand {name: "Apple"})
MERGE (airpods:Accessory {name: "AirPods Pro"})
MERGE (phoneCase:RelatedProduct {name: "Phone Case"})
MERGE (seller:Seller {name: "Seller ABC"})

// 2. Create relationships
MERGE (rahul)-[:PURCHASED]->(iphone)
MERGE (iphone)-[:MADE_BY]->(apple)
MERGE (iphone)-[:COMPATIBLE_WITH]->(airpods)
MERGE (iphone)-[:FREQUENTLY_BOUGHT_WITH]->(phoneCase)
MERGE (phoneCase)-[:SOLD_BY]->(seller)

// 3. Display the complete graph
WITH rahul, iphone, apple, airpods, phoneCase, seller
MATCH (n)-[r]->(m)
WHERE n IN [rahul, iphone, apple, airpods, phoneCase, seller]
  AND m IN [rahul, iphone, apple, airpods, phoneCase, seller]
RETURN n, r, m;