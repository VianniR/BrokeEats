1. Change profile

GET profile 
* profile attributes, preferences listed

PATCH profile
* change profile picture

 


2. Get reccomndations based on own preferences (user did not add preferences on making of account)

GET profile

PATCH preferences 
* edit preferences for what types of food you like, dietary restrictions, and/or budget

GET recommendations
* search for restaurants that fit profile preferences

 

3. Create review for a restaurant, edit it and delete it

GET restaurant
* search for restaturant by name

POST review
* submit a review for a restaurant!

PATCH review - edit review
* Forgot an optional attribute, add to review

GET restaurant/review -search for the review
* search for review based on restaurant and review ID

DELETE review - delete the review
* delete own review
