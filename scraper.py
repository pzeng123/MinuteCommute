from craigslist import CraigslistHousing
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.orm import sessionmaker
from dateutil.parser import parse
import time
import settings

engine = create_engine('sqlite:///listings.db', echo=False)

Base = declarative_base()

class Listing(Base):
    """
    A table to store data on craigslist listings.
    """

    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True)
    link = Column(String, unique=True)
    created = Column(DateTime)
    geotag = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    name = Column(String)
    price = Column(Float)
    location = Column(String)
    cl_id = Column(Integer, unique=True)
    area = Column(String)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def scrape_area(area):
    """
    Scrapes craigslist for a certain geographic area, and finds the latest listings.
    :param area:
    :return: A list of results.
    """
    cl_h = CraigslistHousing(site=settings.CRAIGSLIST_SITE, area=area, category=settings.CRAIGSLIST_HOUSING_SECTION,
                             filters={'max_price': settings.MAX_PRICE, "min_price": settings.MIN_PRICE})

    results = []
    gen = cl_h.get_results(sort_by='newest', geotagged=True, limit=2)
    while True:
        try:
            result = next(gen)
        except StopIteration:
            break
        except Exception:
            continue
        listing = session.query(Listing).filter_by(cl_id=result["id"]).first()

        # Don't store the listing if it already exists.
        if listing is None:
            

            lat = 0
            lon = 0
            if result["geotag"] is None:
                continue
                
            # Assign the coordinates.
            lat = result["geotag"][0]
            lon = result["geotag"][1]

            # Try parsing the price.
            price = 0
            try:
                price = float(result["price"].replace("$", ""))
            except Exception:
                pass

            # Create the listing object.
            listing = Listing(
                link=result["url"],
                created=parse(result["datetime"]),
                lat=lat,
                lon=lon,
                name=result["name"],
                price=price,
                location=result["where"],
                cl_id=result["id"],
                area=result["area"],
            )

            # Save the listing so we don't grab it again.
            session.add(listing)
            session.commit()

            # Return the result 
            results.append(result)
            with open('position.txt', 'a') as f:
                f.write(str(lat) + ',' + str(lon) + '\n')

    return results

def do_scrape():
    """
    Runs the craigslist scraper, and save data to file.
    """

    # Get all the results from craigslist.
    all_results = []
    for area in settings.AREAS:
        results = scrape_area(area)

        all_results += results

    print("{}: Got {} results".format(time.ctime(), len(all_results)))

    # Post each result to file.




do_scrape()