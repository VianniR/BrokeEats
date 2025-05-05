Profiles


1.1 GET /profiles/{userId}

 Retrieve a user’s profile.
 
Path parameter:

 • userId (string, required)
 
 Request body (any of):
 
 {
 
 "name": "string"
 
 }
 
 Response 200:
 
 {
 
 "userId": "string",
 
 "name": "string",
 
 "joinedAt": "date"
 
 }


1.2 PATCH /profiles/{userId}

 Update profile settings
 
 Path parameter:
 
 • userId (string, required)
 
 Request body (any of):
 
 {
 
 "name": "string"
 
 }
 
 Response 200:
 
 {
 
 "success": true,
 
 "profile": {
 
 "userId": "string",
 
 "name": "string",
 
 "joinedAt": "date"
 
 }
 
 }
 

===================
===================

Preferences


2.1 GET /profiles/{userId}/preferences

 Get a user’s saved food preferences.
 
 Path parameter:
 
 • userId (string, required)
 
 Response 200:
 
 {
 
 "budgetMax": 15,
 
 "dietary": ["vegan",“gluten free”,“keto”],
 
 "cuisines": ["mexican","thai"]
 
 }
 
2.2 PATCH /profiles/{userId}/preferences

 Update budget, dietary restrictions, or favorite cuisines.
 
 Path parameter:
 
 • userId (string, required)
 
 Request body (any of):
 
 {
 
 "budgetMax": 10,
 
 "dietary": ["vegetarian","nut free"],
 
 "cuisines": ["italian"]
 
 }
 
 Response 200:
 
 {
 
 "success": true,
 
 "preferences": {
 
 "budgetMax": 10,
 
 "dietary": ["vegetarian","nut free"],
 
 "cuisines": ["italian"]
 
 }
 
 }


===================
===================

Restaurants


3.1 GET /restaurants

 List or filter all restaurants.
 
 parameters (all optional):
 
 • budgetMax (integer)
 
 • cuisine (string)
 
 • minRating (number, 1–5)
 
 • page (integer, default 1)
 
 • limit (integer, default 20, max 50)
 
 Response 200:
 
 {
 
 "results": [
 
 {
 
 "restaurantId": "string",
 
 "name": "string",
 
 "cuisine": "string",
 
 "avgPrice": 8,
 
 "avgRating": 4.2,
 
 "tags": ["big portions"]
 
 },
 
{...}

]

3.2 GET /restaurants/{restaurantId}

 Get full details for one restaurant.
 
 Path parameter:
 
 • restaurantId (string, required)
 
 Response 200:
 
 {
 
 "restaurantId": "string",
 
 "name": "string",
 
 "address": "string",
 
 "cuisine": "string",
 
 "avgPrice": 7,
 
 "avgRating": 4.5,
 
 "tags": ["cheap"],
 
 "reviewsCount": 14
 
 }

 
3.3 GET /restaurants/{restaurantId}/reviews

 List all reviews for a restaurant.
 
 Path parameter:
 
 • restaurantId (string, required)
 
 Query parameters:
 
 • page (integer)
 
 • limit (integer)
 
 Response 200:
 
 {
 
 "results": [
 
 {
 
 "reviewId": "string", 
 
 "userId": "string",
 
 "priceRating": 4,
 
 "valueRating": 5,
 
 "comment": "Great deal! Staff was friendly.",
 
 "createdAt": "date"
 
 },
 
 {... }
 
]

===================
===================
Reviews


4.1 POST /reviews

 Submit a new review.
 
 Request body:
 
 {
 
 "restaurantId": "string",
 
 "userId": "string",
 
 "priceRating": 3,
 
 "valueRating": 4,
 
 "comment": "Portions were huge for $8."
 
 }
 
 Response 200:
 
 {
 
 "success": true,
 
 "reviewId": "string"
 
 }
 
4.2 PATCH /reviews/{reviewId}

 Edit an existing review.
 
 Path parameter:
 
 • reviewId (string, required)
 
 Request body (any of):
 
 {
 
 "priceRating": 1,
 
 "valueRating": 5,
 
 "comment": "Food was amazing, but there were a ton of hidden fees!!"
 
 }
 
 Response 200:
 
 {
 
 "success": true,
 
 "review": {
 
 "reviewId": "string",
 
 "userId": "string",
 
 "priceRating": 1,
 
 "valueRating": 5,
 
 "comment":  "Food was amazing, but there were a ton of hidden fees!!",
 
 "createdAt": "date"
 
 }
 
 }
 
4.3 DELETE /reviews/{reviewId}

 Delete a review.
 
 Path parameter:
 
 • reviewId (string, required)
 
 Response 204: No content.
 
===================
===================
Recommendations


5.1 GET /profiles/{userId}/recommendations

 Get restaurant recommendations based on saved preferences and past reviews.
 
 Path parameter:
 
 • userId (string, required)
 
 Response 200:
 
 {
 
 "recommendations": [
 
 {
 
 "restaurantId": "string",
 
 "name": "string",
 
 "matchScore": 0.87
 
 },
 
{...}

 ]
 
 }
 
 
