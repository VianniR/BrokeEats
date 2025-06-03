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

Three slowest endpoints
1. filter reviews
2. Get preff reccomendations
3. Get reviews

Endpoint times
* Get restaurant
  * Planning = .164 ms
  * Execution = .069 ms

* Create restaurant
  * Planning = .040 ms
  * Execution = 1.537 ms

* Update restaurant
  * Planning = 0.403ms
  * Execution = 0.629 ms

* Delete restaurant
  * Planning = 0.534 ms
  * Execution = 2.505 ms

* Filter restaurant
  * Plan = .966 ms
  * Exe = .402 ms

* Create user
  * Planning = 0.116 ms
  * Exe = 2.434 ms

* Get user
  * Plan = .173 ms
  * Exe = .143 ms

* Update user
  * Plan = .219 ms
  * Exe = .815 ms

* Get prefer recc
  * Plan = 5.445 ms
  * Execution time: 10.088 ms

* Create cuisine 
  * Plan = .080 ms
  * Exe = .5 ms

* Get cuisines
  * Plan = .243
  * Exe = .063

* Create preference
  * Plan = .048 ms
  * Exe = .144 ms

* Get preferences
  * Plan = .216 ms
  * Exe = .172 ms

* Add user preference
  * Plan =  .123ms
  * Exe = .379 ms

* Get user preferences
  * Plan = .924ms
  * Exe = .393 ms

* Add restaurant preferences
  * Plan = .377 ms
  * Exe = 1.828 ms

* Get restaurant poreferences
  * Plan = .344 ms
  * Exe = .140 ms

* Create review
  * Plan .073 ms
  * Exe = 2.088 ms

* Get reviews
  * Plan = .0.191 ms
  * Exe = 13.127 ms

* Delete review
  * Plan = .189 ms
  * Exe = .351 ms

* Update review
  * Plan = .365 ms
  * Exe = .358 ms

* Filter reviews
  * Plan = 1.27 ms
  * Exe = 77.575 ms

Query explain for filter reviews
Limit  (cost=2883.14..2883.14 rows=1 width=167) (actual time=15.702..15.703 rows=0 loops=1)
  ->  Sort  (cost=2883.14..2883.14 rows=1 width=167) (actual time=15.701..15.702 rows=0 loops=1)
        Sort Key: reviews.overall_rating DESC, reviews.price_rating DESC, reviews.food_rating DESC
        Sort Method: quicksort  Memory: 25kB
        ->  Nested Loop  (cost=0.85..2883.13 rows=1 width=167) (actual time=15.696..15.697 rows=0 loops=1)
              ->  Nested Loop  (cost=0.42..2878.69 rows=1 width=167) (actual time=15.696..15.696 rows=0 loops=1)
                    ->  Nested Loop  (cost=0.00..40.88 rows=33 width=12) (actual time=0.024..0.173 rows=29 loops=1)
                          Join Filter: (cuisines.id = restaurants.cuisine_id)
                          Rows Removed by Join Filter: 971
                          ->  Seq Scan on cuisines  (cost=0.00..1.38 rows=1 width=12) (actual time=0.013..0.015 rows=1 loops=1)
"                                Filter: ((name)::text = 'Indian'::text)"
                                Rows Removed by Filter: 29
                          ->  Seq Scan on restaurants  (cost=0.00..27.00 rows=1000 width=8) (actual time=0.005..0.087 rows=1000 loops=1)
                    ->  Index Scan using reviews_restaurant_id_user_id_key on reviews  (cost=0.42..85.98 rows=1 width=159) (actual time=0.535..0.535 rows=0 loops=29)
                          Index Cond: (restaurant_id = restaurants.id)
"                          Filter: ((overall_rating >= '5'::double precision) AND (price_rating >= '4'::double precision) AND (cleanliness_rating >= '3'::double precision) AND (service_rating >= '1'::double precision) AND (food_rating >= '5'::double precision))"
                          Rows Removed by Filter: 690
              ->  Index Only Scan using users_pkey on users  (cost=0.42..4.44 rows=1 width=4) (never executed)
                    Index Cond: (id = reviews.user_id)
                    Heap Fetches: 0
Planning Time: 0.655 ms
Execution Time: 15.735 ms


* Explination
  * Filtering through all restaurants ratings should have an index for a restaurant id and ratings

* solution
CREATE INDEX idx_reviews_filter_sort
ON reviews (
  overall_rating desc,
  price_rating,
  food_rating,
  cleanliness_rating,
  service_rating,
  restaurant_id
  )

  * new explain
  Limit  (cost=201.55..400.94 rows=2 width=167) (actual time=2.394..2.397 rows=0 loops=1)
  ->  Incremental Sort  (cost=201.55..400.94 rows=2 width=167) (actual time=2.392..2.395 rows=0 loops=1)
        Sort Key: reviews.overall_rating DESC, reviews.price_rating DESC, reviews.food_rating DESC
        Presorted Key: reviews.overall_rating
        Full-sort Groups: 1  Sort Method: quicksort  Average Memory: 25kB  Peak Memory: 25kB
        ->  Nested Loop  (cost=2.23..400.85 rows=1 width=167) (actual time=2.383..2.386 rows=0 loops=1)
              ->  Nested Loop  (cost=1.81..396.41 rows=1 width=167) (actual time=2.382..2.384 rows=0 loops=1)
                    Join Filter: (reviews.restaurant_id = restaurants.id)
                    Rows Removed by Join Filter: 232
                    ->  Index Scan using idx_reviews_filter_sort on reviews  (cost=0.42..362.47 rows=5 width=159) (actual time=1.694..1.925 rows=8 loops=1)
"                          Index Cond: ((overall_rating >= '5'::double precision) AND (price_rating >= '4'::double precision) AND (food_rating >= '5'::double precision) AND (cleanliness_rating >= '3'::double precision) AND (service_rating >= '1'::double precision))"
                    ->  Materialize  (cost=1.39..31.54 rows=33 width=12) (actual time=0.014..0.052 rows=29 loops=8)
                          ->  Hash Join  (cost=1.39..31.38 rows=33 width=12) (actual time=0.103..0.390 rows=29 loops=1)
                                Hash Cond: (restaurants.cuisine_id = cuisines.id)
                                ->  Seq Scan on restaurants  (cost=0.00..27.00 rows=1000 width=8) (actual time=0.014..0.161 rows=1000 loops=1)
                                ->  Hash  (cost=1.38..1.38 rows=1 width=12) (actual time=0.025..0.026 rows=1 loops=1)
                                      Buckets: 1024  Batches: 1  Memory Usage: 9kB
                                      ->  Seq Scan on cuisines  (cost=0.00..1.38 rows=1 width=12) (actual time=0.014..0.020 rows=1 loops=1)
"                                            Filter: ((name)::text = 'Indian'::text)"
                                            Rows Removed by Filter: 29
              ->  Index Only Scan using users_pkey on users  (cost=0.42..4.44 rows=1 width=4) (never executed)
                    Index Cond: (id = reviews.user_id)
                    Heap Fetches: 0
Planning Time: 0.930 ms
Execution Time: 2.464 ms


* Outcome
  * This did have the performance improvement I was expecting as it shortened the query execution drastically although we imagine takes up a good amount of memory 




