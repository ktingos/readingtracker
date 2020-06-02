I began with CS50 finance as a basis because I wanted to create a website where the user can create an account in order to keep
track of an activity (in this case their reading). This means I am using session cookies in order for the user to login and not
have to keep entering their password while on the website. Another useful aspect of the CS50 finance that I kept was the "apology"
that helped to deal with the errors and communicate to the user what was going on.

In order to save all the necessary information I created a database called readingtracker.db. Within this database there are three
different tables to store the three different types of information that will be saved. One table keeps track of the user information
such as their username, hashed password, and id number. The second table stores all of the various books. Each entry contains
the information about the book (including title, author, etc) but also a unique book id and the id of the user who has logged that
book. This is because it allows you to link the two tables together if you want to find all the books for a given user. The third
table has all the information for the reading logs. The table contains info for each log (like the pages and the date) but also
the title of the book and the id number of the user. This allows you to access all the logs for a particular book for a particular
user.

I have an application.py file that controls much of what is going on. All the different routes are there that perform various
actions and render the proper html templates (or redirect it to another route). The main route goes into the database and gets
the most recent entries from other people besides this user to act as suggestions for this person. Then it renders the hompepage
template. The check route is used when the user is registering and it checks to see that the username is available and then sends
back true or false. The get info route finds the current date and the dates for this past week and then goes into the database
and sums up all the pages that the user read on each specific day. It then returns a list of dictionaries with the date and pages
for each day in the last week so that they can be displayed on the graph on the homepage. The log in, log out, and register routes
were all from finance.

There are many other routes that I added myself as well. The books route gets all the books from the database that the user has
logged and then renders the books template so that those books can be displayed. For the addBook route, when it is POST it will
get all the information that the user inputted about the book and put it in the database. It then redirects to the books route so
that the user can see the table of all of their books. The finishBook route will get the info from the user and add a finishdate
in the database as long as it fits properly (this is when it is POST). For GET it finds all the unfinished books from the user
in the database so that the user can select which one to add a finishdate to. The readinghistory route will get all the logged
readings of this user from the database. If it is a POST method it will do this only for the book that the user selected. The
logReading route takes the info the user inputted about the reading and puts it in the database and then redirects to
readingHistory so they can see all their reading. The last about route just renders the proper html for the about page.

I also have a layout.html file that helps me take out all of the common html that would be on all of the pages. A lot of it is the
navbar because you want the user to be able to navigate the website from any page on the website. All of my html files are in a
templates folder to keep things organized. Furthermore, I have a styles.css file to factor out the css so it is not directly in the
html.

On several of the html files I incorporated javascript at the bottom. This was to ensure that the user did not leave anything blank
that was supposed to be filled out. This makes sure the person can't even submit it without doing the things that I want them to
do. Even if the person disables javascript, there is another check in the python code in the application.py file to make sure that
all the proper fields were filled out or selected.

Another thing that I decided to implement was a google maps API. This allowed me to insert a map of "where this project all
started" on the about page of the website. I did this instead of using a picture of the map so that the user could have an
interactive experience and see the things around the area.

Something else that I implemented was the CanvasJS API. I used this because it made it easy to present the user's reading
information in a graphical manner. This gives them a visual sense of how much they have been reading which is often preferable
to just seeing the information in a table.