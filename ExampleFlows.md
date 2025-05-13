# Flows

Bob is signing up for BrokeEats and wants to set a gluten-free dietary preference

- First, Bob retrieves his profile by calling GET/profiles.  **Output**: JSON with profile data
- Bob then changing his display name using PATCH/profiles.  **Output**: 200 OK with new profile data
- Bob then sets his food preference using PATCH/profiles/preferences and adds “gluten free” to his dietary preferences  **Output**: 200 OK

- First, Bob makes his profile by calling POST/users/profiles
- Then, Bob retrieves his profile by calling GET/profiles. 
- Bob then changes his display name using PATCH/profiles. 
- Bob then adds a food preference using POST/profiles/preferences and adds “gluten free” to his dietary preferences

Carol wants to discover new restaurants in San Luis Obispo.

First, Carol gets the list of restaurants by calling GET/users/reccomendations Output: JSON with filtered data
Carol reads the most recent reviews by calling GET/reviews/{restaurantId} Output: JSON with review objects

Dave is a food critic that wants to post a review, change it after trying a weekday deal, and then remove it when he changes his mind

- Dave starts by submitting a review using POST/reviews  **Output**: 201 Created
- Dave then updates his review after discovering a weekday special. For this, he calls PATCH/reviews/{reviewId}  **Output**: 200 OK
- Finally, Dave deletes his review using DELETE/reviews/{reviewId}  **Output**: 204 No Content
