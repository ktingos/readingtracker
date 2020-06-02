My project is to be tested with the CS50 IDE. You just need to put all the files, templates, database, etc that I submit into
CS50 IDE and run it with flask by typing "flask run" once you are in my project folder. Within this folder, all the html files
should be inside of a templates folder. Also, the styles.css and the bookspic.jpg should be inside of a static folder. Once this
happens you will be able to go on the website that I created called Reading Tracker.

At this point you will need to hit the register button to create an account (assuming you don't already have one). You must enter a
unique username (you will be told if it not unique) and a password and the confirm the password. Once on the website you will be
able to use the navigation bar at the top to click around and get to various parts of the website.

On the homepage you will see a graph of the pages that you have read the past week and a list of what other people on the website
are reading. Originally the graph will be blank because you have not logged any reading yet.

The first thing you will need to do is add a book by clicking on "Add Book" on the navigation bar. At this point you will have to
fill out various things about the book including the title, author, genre, and the date you started reading the book. You can leave
the date you finished the book blank because it is possible that you started reading the book and are in the process of finishing
it. At this point you can click on "My Books" on the navigation bar to see all of the books that you have entered and the
information for each. When you finish a book that you have already logged but have not entered a finish date, you can do so by going
to "Finish Book." There you will select the unfinished book and select the finish date. This finish date must be on or after the
date you started the book or it will throw an error.

Once you have put down a book, you can log the reading that you have done by going to "Log Reading." At this point you will have to
select the book you read and what day you did the reading, and input the number of pages you read. You must enter a positive integer
number of pages and select a date that is on or after the starting date of your book and before or on the finish date of your book
(if you entered one). At this point you can go to "Reading History" to see all of the readings that you have logged. Originally it
will show a table for the readings with all your books. However, you can select a specific book from the dropdown menu and hit the
button to see your reading history just for that particular book.

A feature of both the "Reading History" and the "My Books" is that the table is interactive. That means you can search for
something in the table to find it. You can also click on the column headers in order to organize the table by that column (and hit
it again if you want to organize it by that column in reverse).

If you have logged your reading then you should see the graph of the number of pages you have read on the homepage if it was
within the last week or so. The final thing is that you can click the "About" section of the navigation bar to learn a little
bit about the origins of the website.

At this point you can log off and then just log in on any subsequent time that you want to access your account.