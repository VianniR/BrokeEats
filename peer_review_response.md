Schema
* Most problems found were already fixed in later alembic revisions
* Most of the things mentioned are already implemented

Cuisines
* Cuisines wasnt working due to a mistake in import is fixed now
* simplified pathnames of endpoints
* no longer case sensitive
* removed array for parameter binding
* No need to use scalar_one over scalar for try/except blocks
* Will not check if cuisine exists
   * Would rather insert and deal with the error how we already have it set up
* Get cuisine does not have a filter as we believe there are not that many cuisines that it needs to be implemented
* Cuisine length is now checked

Preferences
* Simplified pathnames of endpoints
* no longer case sensitive
* removed array for parameter binding
* Functions now 'pass' instead of x=1 if the insert was already done
* add_restaurant_preference takes in the name of the preference so users can just input a name and not remember a preference id
* NewPreference is used
* At this time there is no plan to add delete preference to users nor restaurants nor just delete a preference itself
* get_pref_rec_id now uses row mapping for better readability
* preference length is now checked

Reviews 
* Added created_at for reviews class. When calling get_reviews, users can now see date
* Added cuisine_id to review class.
* Fields have been added reviews. 0.0 - 5.0 are valid
* Changed name to cuisine_name for filtering. Less ambiguity about what name is being filtered
* Filtering by cuisine_name is no longer case sensitive. 
* In create_review checking for existing review before inserting
* Delete reviews now has scalar_one_or_none to check review exists before deleting
* Error code 409 to 404 because it's not found instead of conflict
* Removed loops from happening inside db call. Using fetchall so I can do the loop outside
* Pathnames were simplified.
* Fixed router.patch to router.delete in delete_review
* Will not return 204 in create_review
  * I believe seeing the created review is better. You can see the response of what was posted. Can immediately update if there's some error. 204 prevents that possibility

Restaurants
* Added GET restaurants endpoint
* Added GET restaurants/id endpoint
* Simplified pathnames of endpoints
* Added additional ResponseModels for creating and updating Restaurants
* last_updated_at is now set when Restaurant is created
* User no longer needs to manually set last_updated_at
* Added data validation to Restaurant models


Users
* Removed f-strings from SQL queries (parameterized them properly).
* Fixed missing / in @router.patch("/profile/{id}").
* Used **row via .mappings() for cleaner recommendation building.
* Eliminated unnecessary [ ] around SQL param dicts.
* Refactored loop over recommendations for compactness.
* Added field validation for name, username, and email.
* Made username lookup in get_profile case-insensitive.
* Added ensure_user_exists helper and integrated it into the patch route.
