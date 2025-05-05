## 1. Change Profile

1. **Fetch full profile**  
   ```
   GET /profiles/{userId}
    200 OK
   {
     "userId":"…",
     "name":"…",
     "joinedAt":"…",
     "preferences":{…}     
   }
   ```

2. **Update profile picture**  
   ```
   PATCH /profiles/{userId}
   Request body (any of):
   {
     "name":"string",         
     "avatarUrl":"https://…"
   }
    200 OK
   {
     "success":true,
     "profile":{
       "userId":"…",
       "name":"…",
       "joinedAt":"…"
     }
   }
   ```

---

## 2. Get Recommendations Based on Your Own Preferences

1. **Fetch profile**  
   ```
   GET /profiles/{userId}
   ```
   

2. **Set or update taste & budget**  
   ```
   PATCH /profiles/{userId}/preferences
   Request body:
   {
     "budgetMax":15,
     "dietary":["vegan","gluten free"],
     "cuisines":["mexican","thai"]
   }
    200 OK
   {
     "success":true,
     "preferences":{
       "budgetMax":15,
       "dietary":[…],
       "cuisines":[…]
     }
   }
   ```

3. **Fetch tailored recommendations**  
   ```
   GET /profiles/{userId}/recommendations
    200 OK
   {
     "recommendations":[
       { "restaurantId":"…","name":"…","matchScore":0.87 },
       …
     ]
   }
   ```

---

## 3. Review Lifecycle

1. **Find restaurant**  

     ```
     GET /restaurants?page=1&limit=50
     ```
    

2. **Get full restaurant details**  
   ```
   GET /restaurants/{restaurantId}
   → returns address, avgPrice, tags, etc.
   ```

3. **Submit a new review**  
   ```
   POST /reviews
   {
     "restaurantId":"…",
     "userId":"…",
     "priceRating":3,
     "valueRating":4,
     "comment":"Huge portions for the price."
   }
    200 OK { "success":true, "reviewId":"…" }
   ```

4. **Edit review**  
   ```
   PATCH /reviews/{reviewId}
   Request body (any of):
   {
     "priceRating":2,
     "valueRating":5,
     "comment":"Actually, they upped their prices…"
   }
    200 OK { "success":true, "review":{…updated…} }
   ```

5. **Locate review**  
   ```
   GET /restaurants/{restaurantId}/reviews?page=1&limit=50
 
   ```

6. **Delete review**  
   ```
   DELETE /reviews/{reviewId}
    204 No Content
   ```
