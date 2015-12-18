# Triangulate
* By Jason Shin, Franklin Wang, Rong Yu, and Masahero Masuda*

## What's this app?
* Triangulate is an application that will allow you to find the most
  convenient location for you and your friends to meet up, whether
  it be to grab a bite or watch a movie.

## Potential Ideas
* Implementation
  * Use home address if not connected to the app.
  * If connected, our program will use the Geolocation API to take the current
    location of the user and store it in a database so your friends can access it.

* Accounts
  * Records places you've been to.
  * Friend users to meet up with them (Maybe a meet-with-strangers feature?).
  * 
  
* Have a page where you can invite people to your event
  * Chatroom to talk to others going to your event/meetup.
  * Live feed of where you and your friends are on a map (using AJAX calls).

* Filter potential destinations by...
  * Distance or time willing to travel.
  * Type of place you want to meet (Restaurant, Park, etc.).

## Tools We Will Use:
* Google Maps API.
* Mongodb for users who want to track where they have been.
* MTA/Uber API for transportation.
* Geolocation API to track current location.
* JQuery to live track where your friends are (AJAX).

## What We Don't Know How to Do:
* Getting the locations of other people you want to meet up with.

## Team Roles
|Person            |Role           |
|------------------|---------------|
| Franklin Wang    |Leader	   |
| Masahero Masuda  |Frontend       |
| Jason Shin       |Backend        |
| Rong Yu	   |Middleware     |