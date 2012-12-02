# RSVP - répondez s'il vous plaît

## Quick and dirty RSVP web app.

RSVP (*répondez s'il vous plaît* in French), is a mechanism for an inviter to know how many of the invitees plan to arrive to the invitation. 

As far as I could tell, there is no web app that offers this kind of service as a simple, no registration, no hussle, web app.

I wanted to get an RSVP from students for a recitation I'm giving, so I built this project from scratch, copying code from a previous project, and doing it all quick and dirty (and in Hebrew! but the Hebrew stuff is only at the HTML level).

The idea is for a person to fill in his/her name and click `OK`, and then he will see a `thank you` message. The number of invitees who already responded will be shown, but not their names. 

The inviter, upon entering a password at the name prompt, will see a list of invitees who already responded positively.

## How to use

 *  Install *Python* 2.7.x
 *  Install [Flask](http://flask.pocoo.org/), usually by calling `pip install Flask`
 *  Clone this repository
 *  Run the server: `python server.py`
 
All the back end is included in `server.py`, all the front end is in `templates/index.html` and `static/style.css`.

## License 

The project is currently licensed under [CC BY-NC-SA 3.0](http://creativecommons.org/licenses/by-nc-sa/3.0/).