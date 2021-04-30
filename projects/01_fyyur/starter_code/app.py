#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
from os import abort
import sys
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime as dt
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
migrate=Migrate(app,db)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String))
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    image_link = db.Column(db.String(500))

    @property
    def getJson(self):
      return {'id':self.id,
              'name':self.name,
              'genres':self.genres,
              'address':self.address,
              'city':self.city,
              'state':self.state,
              'phone':self.phone,
              'website':self.website,
              'facebook_link':self.facebook_link,
              'seeking_talent':self.seeking_talent,
              'seeking_description':self.seeking_description,
              'image_link':self.image_link
              }

    @property
    def getVenueShowJson(self):
      return {
        "id": self.id,
        "name": self.name,
        "genres": self.genres,
        "address": self.address,
        "city": self.city,
        "state": self.state,
        "phone": self.phone,
        "website": self.website,
        "facebook_link": self.facebook_link,
        "seeking_talent": self.seeking_talent,
        "seeking_description": self.seeking_description,
        "image_link": self.image_link,
        "past_shows": [show.getJson for show in Show.query.filter(Show.Venue_id == self.id,Show.Start_time<dt.now())],
        "upcoming_shows": [show.getJson for show in Show.query.filter(Show.Venue_id == self.id,Show.Start_time>dt.now())],
        "past_shows_count": len(Show.query.filter(Show.Venue_id == self.id,Show.Start_time<dt.now()).all()),
        "upcoming_shows_count": len(Show.query.filter(Show.Venue_id == self.id,Show.Start_time>=dt.now()).all())
      }



class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_decription = db.Column(db.String(120))
    image_link = db.Column(db.String(500))

    @property
    def getJson(self):
      return {'id': self.id,
              'name': self.name,
              'city': self.city,
              'state': self.state,
              'phone': self.phone,
              'genres': self.genres,
              'image_link': self.image_link,
              'facebook_link': self.facebook_link,
              'seeking_venue': self.seeking_venue
              }

    @property
    def getArtistShowJson(self):
        return {
          'id': self.id,
          'name': self.name,
          'city': self.city,
          'state': self.state,
          'phone': self.phone,
          'genres': self.genres,
          'image_link': self.image_link,
          'facebook_link': self.facebook_link,
          'seeking_venue': self.seeking_venue,
          "past_shows":[show.getJson for show in Show.query\
            .filter(Show.Artist_id == self.id,Show.Start_time < dt.now())],
          'past_shows_count':len(Show.query.filter(Show.Artist_id == self.id,Show.Start_time < dt.now()).all()),
          "upcoming_shows":[show.getJson for show in Show.query \
            .filter(Show.Artist_id == self.id,Show.Start_time >= dt.now())],
          "upcoming_shows_count":len(Show.query.filter(Show.Artist_id == self.id,Show.Start_time >= dt.now()).all())
        }

class Show(db.Model):
  __tablename__ = 'Show'
  id = db.Column(db.Integer, primary_key = True)
  Venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'),nullable=False)
  Artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  Start_time = db.Column(db.DateTime(),nullable=False)
  venue = db.relationship('Venue',backref=db.backref('shows'))
  artist = db.relationship('Artist', backref=db.backref('shows'))

  @property
  def getJson(self):
    return {
            "venue_id": self.Venue_id,
            "venue_name": self.venue.name,
            "artist_id": self.Artist_id,
            "artist_name": self.artist.name,
            "artist_image_link": self.artist.image_link,
            "venue_image_link":self.venue.image_link,
            "start_time": self.Start_time.strftime("%m/%d/%Y, %H:%M:%S")
            }

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=[{
    "city": "San Francisco",
    "state": "CA",
    "venues": [{
    "id": 14,
    "name": "The Musical Hop",
    "num_upcoming_shows": 0,
    }, {
      "id": 15,
      "name": "Park Square Live Music & Coffee",
      "num_upcoming_shows": 1,
    }]
  }, {
    "city": "New York",
    "state": "NY",
    "venues": [{
    "id": 16,
    "name": "The Dueling Pianos Bar",
    "num_upcoming_shows": 0,
    }]
  }]
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search = request.form.get('search_term')
  VenueFilter = Venue.name.ilike(f"%{search}%")
  venues = Venue.query.filter(VenueFilter).all()
  response = {
      "count":len(venues),
      "data":[venue.getJson for venue in venues]
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)
  data = venue.getVenueShowJson
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  venueform = VenueForm(request.form)
  try:
    venue = Venue(name = venueform.name.data,
                  city = venueform.city.data,
                  state = venueform.state.data,
                  address = venueform.address.data,
                  phone = venueform.phone.data,
                  image_link = venueform.image_link.data,
                  facebook_link = venueform.facebook_link.data,
                  genres = venueform.genres.data,
                  seeking_talent = venueform.genres.data,
                  website = venueform.website_link.data
                  )
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')

  except Exception as e:
    db.session.rollback()
    print (e)
    print ("Create record failed, db rolledback.")
    flash('An error occurred. Venue ' + venue.name + ' could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  data = Artist.query.get(artist_id)
  showdata = data.getArtistShowJson
  return render_template('pages/show_artist.html', artist=showdata)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist_update = Artist.query.get(artist_id)
  if artist_update is None:
    abort(404)
  artist=artist_update.getJson
  form = ArtistForm(data=artist)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  form = ArtistForm(request.form)
  try:
    artist = Artist.query.get(artist_id)
    artist.name = form.name.data
    artist.state = form.state.data
    artist.phone = form.phone.data
    artist.genres = form.genres.data
    artist.facebook_link = form.facebook_link.data
    artist.image_link = form.image_link.data
    artist.website = form.website_link.data
    artist.seeking_venue = form.seeking_venue.data
    artist.seeking_decription = form.seeking_description.data
    db.session.commit()
  except:
    db.session.rollback()
    print ("Update failed, db rollbacked.")
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue_update = Venue.query.get(venue_id)
  if not venue_update:
    abort(404)
  venue=venue_update.getJson
  form = VenueForm(data=venue)

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  form = VenueForm(request.form)
  try:
    venue = Venue.query.get(venue_id)
    venue.name = form.name.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.address = form.address.data
    venue.phone = form.phone.data
    venue.genres = form.genres.data
    venue.facebook_link = form.facebook_link.data
    venue.image_link = form.image_link.data
    venue.website = form.website_link.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_description = form.seeking_description.data

    db.session.commit()
  except Exception as e:
    db.session.rollback()
    print ("Update failed, db rollbacked.")
  finally:
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form)
  try:
    artist = Artist(name = form.name.data,
                    city = form.city.data,
                    state = form.state.data,
                    phone = form.phone.data,
                    genres = form.genres.data,
                    image_link = form.image_link.data,
                    facebook_link = form.facebook_link.data,
                    seeking_venue = form.seeking_venue.data,
                    website = form.website_link.data
                    )
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except Exception as e:
    db.session.rollback()
    print (e)
    print ("Db record create failed. Db Rollbacked.")
    flash('An error occurred. Artist ' + artist.name + ' could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  show = Show.query.all()
  data = [s.getJson for s in show]
  #print (data)
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  showForm = ShowForm(request.form)
  try:
    show = Show(Artist_id = showForm.artist_id.data,
                Venue_id = showForm.venue_id.data,
                Start_time = showForm.start_time.data)
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except Exception as e:
    db.session.rollback()
    print (e)
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
