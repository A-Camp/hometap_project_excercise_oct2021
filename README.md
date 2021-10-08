# hometap_project_excercise_oct2021
Takehome project excercise for Hometap. Concerns primarily API design and considerations. 

### How To Run
Steps:
1. Fork or clone the git repo to your local computer
2. Cd into the directory and start your python shell
3. Create and run the migrations
4. Start the server from the python shell 
5. You now have two options. Both should work nicely - pick the one that sparks joy ✨ 
    - Go to [the server](http://localhost:8000/homes/) in your browser. You should be able to see a Browsable API provided by Django React Framework (DRF). This browsable framework should let you log-in and interact with the API.
    - Interact with the API via the command line. I like sending requests via httpie. Here are some examples:
        - Run `pip install httpie`
        - You can see a users existing homes via `http -a superuser:password http://127.0.0.1:8000/homes/`
        - You can create a home via `http -a superuser:password http://127.0.0.1:8000/homes.json address="ADDRESS HERE" zipcode="ZIPCODE HERE" city="CITY HERE" state="TWO LETTER STATE ABBR HERE"` Required fields are address and zipcode. The return home should have a `has_septic` field.
        - You can view your created home via `http -a superuser:password http://127.0.0.1:8000/homes/{HOME ID}/`
    - Please note the superuser and password fields from from using `python manage.py createsuperuser` on the command line and utilizing the username and password you give there. That user can also be used to log into the Browsable API. I just had an existing super user/admin in the project with a username of `superuser` and a password of `password`. This isn't how you'd normally do user log in but it allows this API to get up and running quickly. You can add and manipulate more users via the django admin field at `localhost:8000/admin/`

### Thought Process/Assumptions
Based on the assumption that we want to save home-owner answers about potential septic tanks. I have decided that 
I want to do an API that interacts with an existing home model. A home should belong to a user who will provide information about it. A user might initially provide the home address but later provide more information (like answering questions about their septic tank). For security reasons only admin/superuser level accounts and users who own a home should be able to access or change information about a home. 

Due to this I am using a RESTful url pattern based on models. In order to stay minimalist I will only be implenting a POST endpoint at `/home/` and GET and PATCH endpoints at `/home/id`. This should allow a user to give us an address so we can check septic tank status. It should allow the front-end to determine when it wants to know about that septic tank status, and it should allow a user to then answer some questions about their septic tank (if it exists). 

### Shout-Outs

If I had more time this project, or was doing it in a live-database then I would write some sort of migration/script/job/pick-your-favorite to handle back-filling septic tank data for any existing homes in the database. 
