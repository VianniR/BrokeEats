
Workflow:

Bob is signing up for BrokeEats and wants to set a gluten-free dietary preference

First, Bob retrieves his profile by calling GET/profiles. Output: JSON with profile data
Bob then sets his display name using PATCH/profiles. Output: 200 OK
Bob then sets his food preference using PATCH/profiles/preferences and adds “gluten free” to his dietary preferences Output: 200 OK
---------------------------------------------------------
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
-------------------------------------------------
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
------------------------------------------------------
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

-----------------------------------------------------------

curl -X 'POST' \
  'https://brokeeats.onrender.com/preferences/profiles/get_preferences/1?preference_name=gluten%20free' \
  -H 'accept: */*' \
  -H 'access_token: brat' \
  -d ''

----------------------------------------------------------------
curl -X 'GET' \
  'https://brokeeats.onrender.com/preferences/profiles/1' \
  -H 'accept: application/json' \
  -H 'access_token: brat'

  Response:[
  {
    "id": 1,
    "name": "gluten free"
  }
