from sqlalchemy import Column, Integer, String, func, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(128), unique=True) 
    password = Column(String(16))
    name = Column(String(512))
    age = Column(Integer)
    email = Column(String(256), unique=True)
    
    measurement_user = relationship("Measurement", back_populates='user_measurement')
    city_user = relationship("City", back_populates='user_city')
    tool_user = relationship("Tool", back_populates='user_tool')

class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    name = Column(String(512))
    country = Column(String(512))
    userid = Column(Integer, ForeignKey('user.id'))
    date = Column(DateTime)

    measurement_city = relationship("Measurement", back_populates='city_measurement')
    google_city = relationship("GoogleWeather", back_populates='city_google')
    tool_city = relationship("Tool", back_populates='city_tool')
    user_city = relationship("User", back_populates='city_user')

class WeatherDescription(Base):
    __tablename__ = 'description'

    id = Column(Integer, primary_key=True)
    skydescription = Column(String(512), unique=True)

    measurement_description = relationship("Measurement", back_populates='description_measurement')
    google_description = relationship("GoogleWeather", back_populates='description_google')

class Measurement(Base):
    __tablename__ = 'measurment'

    id = Column(Integer, primary_key=True)
    userid = Column(Integer, ForeignKey('user.id')) 
    descriptionid = Column(Integer, ForeignKey('description.id'))
    cityid = Column(Integer, ForeignKey('city.id'))
    toolid = Column(Integer, ForeignKey('tool.id'))
    date = Column(DateTime)
    temperature = Column(Integer)
    humidity = Column(Integer)
    windspeed = Column(Integer)

    user_measurement = relationship("User", back_populates='measurement_user')
    city_measurement = relationship("City", back_populates='measurement_city')
    description_measurement = relationship("WeatherDescription", back_populates='measurement_description')
    tool_measurement = relationship("Tool", back_populates='measurement_tool')

class GoogleWeather(Base):
    __tablename__ = 'forecast'

    id = Column(Integer, primary_key=True) 
    descriptionid = Column(Integer, ForeignKey('description.id'))
    cityid = Column(Integer, ForeignKey('city.id'))
    date = Column(DateTime)
    temperature = Column(Integer)
    humidity = Column(Integer)
    wind = Column(Integer)

    city_google = relationship("City", back_populates='google_city')
    description_google = relationship("WeatherDescription", back_populates='google_description')

class Tool(Base):
    __tablename__ = 'tool'

    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    descriprion = Column(String(1024))
    cityid = Column(Integer, ForeignKey('city.id'))
    userid = Column(Integer, ForeignKey('city.id'))

    measurement_tool = relationship("Measurement", back_populates='tool_measurement')
    city_tool = relationship("City", back_populates='tool_city')
    user_tool = relationship("User", back_populates='tool_user')