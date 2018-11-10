# pipocryte

## Migrating

Turns out migrating in Django 1.3.1 is not that easy. It's _pretty_ easy, but not as easy as it should be. I'm using an add-on called `South`. Basically what I did to get South going is:

1. I did `pip install South`
2. I added `'south'` to my `INSTALLED_APPS` in settings.py
3. I did `./manage.py syncdb` (this puts south's internal migrations wizardry in your database)
4. I did `./manage.py convert_to_south myapp`, which makes a dummy migration so that South can have a 'last migration' to compare changes to your model to.
5. I updated the models with the new `canonical_image` field for articles.
5. I did `/manage.py schemamigration myapp --auto`.

Hopefully this will work as well with Postgres as it did with Sqlite3! 
