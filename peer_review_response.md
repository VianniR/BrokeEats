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
