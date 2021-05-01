
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt

db = SQLAlchemy()

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


    def getArtistShows(query):
        return  [
                    {
                        "artist_id": s.artist.id,
                        "artist_name": s.artist.name,
                        "artist_image_link": s.artist.image_link,
                        "start_time": s.Start_time.strftime('%Y-%m-%d %H:%M:%S')
                    }
                    for s in query
            ]


    @property
    def getAggVenue(self):
        return {
            'city': self.city,
            'state': self.state,
            'venues': [
                        venue.getVenueShowJson for venue in Venue.query.filter(Venue.city == self.city,
                                                                       Venue.state == self.state).all()
                      ]
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

    def getVenueShows(query):
        return  [
                    {
                        "venue_id": s.venue.id,
                        "venue_name": s.venue.name,
                        "venue_image_link": s.venue.image_link,
                        "start_time": s.Start_time.strftime('%Y-%m-%d %H:%M:%S')
                    }
                    for s in query
            ]


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

