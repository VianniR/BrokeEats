Workflow:

Bob is signing up for BrokeEats and wants dinner ideas under $12 that fit his gluten-free preference.

- First, Bob makes his profile by calling POST/users/profiles
- Then, Bob retrieves his profile by calling GET/profiles.
- Bob then changes his display name using PATCH/profiles.
- Bob then adds a food preference using POST/profiles/preferences and adds “gluten free” to his dietary preferences
---------------------------------------------------------------------------------------------------------------------
curl -X 'POST' \
  'https://brokeeats.onrender.com/users/profile' \
  -H 'accept: application/json' \
  -H 'access_token: brat' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Bob",
  "username": "BobSponge",
  "email": "bob12@calpoly.edu"
}'

Response: {
  "id": 1,
  "name": "Bob",
  "username": "BobSponge",
  "email": "bob12@calpoly.edu",
  "permissions": 1
}
---------------------------------------------------------------------------------------------------------------------
curl -X 'GET' \
  'https://brokeeats.onrender.com/users/profile/{id}?user_id=1' \
  -H 'accept: application/json' \
  -H 'access_token: brat'

Response:{
  "id": 1,
  "name": "Bob",
  "username": "BobSponge",
  "email": "bob12@calpoly.edu",
  "permissions": 1
}
---------------------------------------------------------------------------------------------------------------------
curl -X 'PATCH' \
  'https://brokeeats.onrender.com/usersprofile/{id}?user_id=1' \
  -H 'accept: application/json' \
  -H 'access_token: brat' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Bob",
  "username": "SpongeBob2Loco",
  "email": "bob12@calpoly.edu"
}'

Response:{
  "id": 1,
  "name": "Bob",
  "username": "SpongeBob2Loco",
  "email": "bob12@calpoly.edu",
  "permissions": 1
}

---------------------------------------------------------------------------------------------------------------------

curl -X 'POST' \
  'https://brokeeats.onrender.com/preferences/preferences' \
  -H 'accept: application/json' \
  -H 'access_token: brat' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "gluten free"
}'

Response:{
  "id": 1,
  "name": "gluten free"
}


