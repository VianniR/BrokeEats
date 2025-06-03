We distributed the 1 million rows  of data the following way 
* 300k users
* 700k reviews
* 1k restaurants
* 50 preferences
* 30 cuisines

  We decided on 700k reviews because with this number, the average user will have between 1-2 reviews. There will always be more reviews than users, so about a 2:1 ratio seemed reasoable. Since it's a db that focuses on reviewing restaurants, we wanted most of our data to be for reviews. Reviews should be the focus of our data. 
  
  The 300k users seemed like a moderately popular app. Using 3/10 of our alloted million rows on users seems reasonable. Getting 3/10 students to sign up for a restaurant review db seems doable. It also has a good ratio with the number of our reviews.
  
  1k restarants seemed like a good number. There's roughly 7 restaurants per 1000 people, which would be about 2100 restaurants.However, since our target demographic includes students who often live in dorms or shared apartments, we expect fewer total restaurant options in college towns. There's also a limited number of restaurant space in college cities.

  50 preferences seemed like a good number. Obviously many people have many prefences, but we just selected some of the most popular. With 50, users have an ample selection while also not feeling overwhelmed by the number of choices.

  There are countless cuisines worldwide, but realistically, only a subset is commonly offered in most restaurant scenes—especially in smaller college cities. Like preferences, we focused on the most popular or commonly found cuisines. Limiting this to 30 options keeps the data relevant, normalized, and efficient for filtering and recommendation systems  



