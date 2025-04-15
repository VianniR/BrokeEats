# User Stories and Exceptions

## USER STORIES

1. As a college student, I want to be able to submit reviews for restaurants so I can help others find affordable food options.
2. As a money-saving traveler, I want to filter food spots based on things like price or portion size so that I can eat well while sticking to my budget.
3. As a new user, I want to be able to quickly create an account so that I can quickly start rating restaurants and saving my favorites.
4. As a local business owner, I want to get more publicity for the large portion sizes I give at an affordable price.
5. As someone who goes to the gym, I want to be able to find restaurants that will allow me to bulk while not breaking the bank so I can continue affordably.
6. As a food critic, I want to find the best tasting food in the city so I can add them to my blog.
7. As a broke college student, I want to find cheap food that tastes good so I can take my girlfriend out to dinner while not spending a ton of money.
8. As a picky eater, I want to find places that serve the food I am comfortable with.
9. As someone who likes to try new things, I would like to be able to find places that venture out of the norm like a Jamaican-Mexican fusion spot.
10. As an obsessive Korean fried chicken connoisseur, I want to be able to find the best Korean fried chicken that is also affordable.
11. As someone who appreciates great customer service, I would like to find a restaurant that has amazing food and also treats their customers well.
12. As someone in a caloric deficit, I would like to find the best restaurants that have all the calories of their food listed on their menu.

---

## EXCEPTIONS

1. **Exception: User submits a review without being logged in**  
   The system will return an error and prompt the user to log in.

2. **Exception: Restaurant does not exist in the database**  
   The system will suggest creating a new entry.

3. **Exception: User tries to submit an empty review**  
   The API will reject the submission and return an error saying empty fields aren’t allowed.

4. **Exception: User tries to rate a restaurant they’ve already reviewed**  
   The system will prompt the user to edit the review they’ve already submitted.

5. **Exception: User tries to edit restaurant details**  
   The system will deny the user access to editing details but will prompt the user to suggest an edit.

6. **Exception: User puts explicit language in their review**  
   The system will *** out the word and warn them to be more respectful in the future.

7. **Exception: User inputs a suspiciously low price for a high quality meal**  
   System will prompt user to add further details (special promotions, or maybe just a typo).

8. **Exception: User fills out a half complete review**  
   The system will null out any blank non-essential information.

9. **Exception: User attempts to register with an already existing email**  
   The system will return an error and suggest logging in instead.

10. **Exception: User tries to upload a photo but it fails**  
    System will prompt user to try again or to take another photo.

11. **Exception: User’s reviews are only one word or too short**  
    System will prompt user to add more details to the review to make sure other users will believe their ratings.

12. **Exception: User tries to write a review with improper syntax for the price (ex: $12.999, or ‘very cheap’)**  
    System will flag it as an error and prompt the user to input the price again.