# smunchData OUT OF DATE
This directory contains all work done during the summer of 2017 at Smunch internship

Each directory contains different approaches to predictions and gathering information.
csvPredictions was the initial work when only the master csv file that has been manually 
entered was avaliable for use. It served well in allowing me to generate my alogrith 
and test it on basic data. 
The dbPredictions is the transition from the csv file to the
locally running postgreSQL smunch database. This served to make query's much more efficient 
but also precise. In this directory the same prediction alogirthm is in place as long as a 
more general format for including new paramters such as a time dependence.
The gui_qtApp directory is exactly that. An incomplete framework for a native Desktop app.
I was initially building this because I was unsure if I was going to have time to implement
my predictions on the server before I left. It was also helpful in creating a format for 
displaying and working with the predictions. 