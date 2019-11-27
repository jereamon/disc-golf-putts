I got totally hooked on disc golf a couple years ago. This is a simple Flask application to track my backyard putting averages. 

Putting sessions are written to the database to keep track of the time of the session and the number of putters I was using.  
Individual "putts" are written to the database with a foreign key corresponding to the active putting session.  
Each "putt" is actually the number of puttsmade from a given distance. Not each individual putt thrown.

When creating a putting session the user can select the option to input distances manually, auto increase distance from 18 feet to 33 feet,
or be given random distances between 15 and 33 feet.

I used ajax to query the database and save each putt so that the page can be updated dynamically without having to be refreshed.

<p align="center">
  <img src="https://github.com/jereamon/disc-golf-putts/blob/master/dg-putts-individual-session.png" width="75%">
</p>
<p align="center">
  <img stv="https://github.com/jereamon/disc-golf-putts/blob/master/dg-putts-save-putt.png" width="75%">
</p>
