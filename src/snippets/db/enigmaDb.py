import datetime

from typing import List
from sqlalchemy import create_engine
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import MetaData
from sqlalchemy import String, Integer, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import csv

Base = declarative_base()


class DRotor(Base):
    __tablename__ = "DRotor"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    wiring = Column(String)
    isReflector = Column(Boolean, default=False)
    notches = Column(String)
    dateIntroduced = Column(String)

    def __repr__(self):
        return f"<DRotor>name={self.name},wiring={self.wiring}"


def createRotorsInDb(rotorInfo):
    session = Session()

    newRotorNames = [x["name"] for x in rotorInfo]
    currentRotors = session.query(DRotor).all()
    rotors2Delete = [x for x in currentRotors if x._name in newRotorNames]
    for x in rotors2Delete:
        session.delete(x)

    session.commit()
    rotors = []

    for info in rotorInfo:
        rotors.append(DRotor(**info))
    session.add_all(rotors)
    session.commit()
    session.close()


def readRotorCsv():
    rotors = []
    infos = []
    with open(r'../../../data/rotorDetails.csv', 'r') as csvfile:
        csv2dbMapping = {"Rotor #": "name",
                         "wiring": "wiring",
                         "Date Introduced": "dateIntroduced"}
        data = csv.DictReader(csvfile, delimiter=';')
        for row in data:
            infos.append({k.rstrip(): v.rstrip() for k, v in row.items()})

    for row in infos:
        rotors.append({csv2dbMapping[k]: v for k, v in row.items() if k in csv2dbMapping})

    return rotors


if __name__ == "__main__":
    engine = create_engine(r"sqlite:///enigma.db", echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    # createRotorsInDb(readRotorCsv())
    print("ende")
