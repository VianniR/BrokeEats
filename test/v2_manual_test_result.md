Carol wants to discover new restaurants in San Luis Obispo.

First, Carol gets the list of restaurants by calling GET/users/reccomendations Output: JSON with filtered data
After seeing the restaurants, she decides she wants to eat Mexican food. She filters by calling restaurant/filter 
Carol reads the most recent reviews by calling GET/reviews/{restaurantId} Output: JSON with review objects

curl -X 'GET' \
  'https://brokeeats.onrender.com/users/users/recommendations?user_id=1&limit=2' \
  -H 'accept: application/json' \
  -H 'access_token: brat'

Response:

[
  {
    "id": 1,
    "name": "El Guero",
    "cuisine": "mexican",
    "address": "1122 Chorro St",
    "city": "San Luis Obispo",
    "state": "CA",
    "zipcode": "93401",
    "phone": "805-540-4637",
    "overall_score": 4.5,
    "food_rating": 5,
    "service_rating": 3,
    "price_rating": 5,
    "cleanliness_rating": 5
  },
  {
    "id": 2,
    "name": "Panda Express",
    "cuisine": "chinese",
    "address": "789 Foothill Blvd",
    "city": "San Luis Obispo",
    "state": "CA",
    "zipcode": "93405",
    "phone": "805-784-0355",
    "overall_score": 3,
    "food_rating": 4,
    "service_rating": 5,
    "price_rating": 2,
    "cleanliness_rating": 1
  }
]

curl -X 'POST' \
  'https://brokeeats.onrender.com/restaurants/filter?limit=2' \
  -H 'accept: application/json' \
  -H 'access_token: brat' \
  -H 'Content-Type: application/json' \
  -d '{
  "city": "San Luis Obispo",
  "state": "CA",
  "overall_rating": 3,
  "food_rating": 3,
  "service_rating": 3,
  "price_rating": 3,
  "cleanliness_rating": 3,
  "cuisine_name": "mexican"
}'

Response:
[
  {
    "id": 1,
    "name": "El Guero",
    "cuisine": "mexican",
    "address": "1122 Chorro St",
    "city": "San Luis Obispo",
    "state": "CA",
    "zipcode": "93401",
    "phone": "805-540-4637",
    "overall_score": 4.5,
    "food_rating": 5,
    "service_rating": 3,
    "price_rating": 5,
    "cleanliness_rating": 5
  }
]

curl -X 'GET' \
  'https://brokeeats.onrender.com/reviews/reviews/1' \
  -H 'accept: application/json' \
  -H 'access_token: brat'

Response:
[
  {
    "user_id": 1,
    "restaurant_id": 1,
    "overall": 4.5,
    "food": 5,
    "service": 3,
    "price": 5,
    "cleanliness": 5,
    "note": "Nice"
  }
]


----------------------------------------------------------------------------------
Dave is a food critic that wants to post a review, change it after trying a weekday deal, and then remove it when he changes his mind

Dave starts by submitting a review using POST/reviews Output: 201 Created
Dave then updates his review after discovering a weekday special. For this, he calls PATCH/reviews/{restaurantId}/{user_id} Output: 200 OK
Finally, Dave deletes his review using DELETE/reviews/delete/{restaurant_id}/ {user_id} Output: 204 No Content

curl -X 'POST' \
  'https://brokeeats.onrender.com/reviews/reviews' \
  -H 'accept: application/json' \
  -H 'access_token: brat' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": 2,
  "restaurant_id": 1,
  "overall": 1,
  "food": 1,
  "service": 1,
  "price": 1,
  "cleanliness": 1,
  "note": "Never going back!"
}'
Response: 
{
  "user_id": 2,
  "restaurant_id": 1,
  "overall": 1,
  "food": 1,
  "service": 1,
  "price": 1,
  "cleanliness": 1,
  "note": "Never going back!"
}

curl -X 'PATCH' \
  'https://brokeeats.onrender.com/reviews/1/2' \
  -H 'accept: application/json' \
  -H 'access_token: brat' \
  -H 'Content-Type: application/json' \
  -d '{
  "overall": 5,
  "food": 5,
  "service": 5,
  "price": 5,
  "cleanliness": 5,
  "note": "I was wrong. Place is gas"
}'
Response: {
  "user_id": 2,
  "restaurant_id": 1,
  "overall": 5,
  "food": 5,
  "service": 5,
  "price": 5,
  "cleanliness": 5,
  "note": "I was wrong. Place is gas"
}

curl -X 'PATCH' \
  'https://brokeeats.onrender.com/reviews/reviews/delete/1/2' \
  -H 'accept: */*' \
  -H 'access_token: brat'

Response:
 alt-svc: h3=":443"; ma=86400 
 cf-cache-status: DYNAMIC 
 cf-ray: 93f021187e1eceed-SJC 
 content-encoding: br 
 content-type: application/json 
 date: Tue,13 May 2025 06:34:18 GMT 
 rndr-id: 892f14fb-e465-415d 
 server: cloudflare 
 vary: Accept-Encoding 
 x-render-origin-server: uvicorn 