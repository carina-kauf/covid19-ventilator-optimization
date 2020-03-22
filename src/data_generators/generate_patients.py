# Generates a JSON file with @nbr_patients patients where for each of them a request will be filed
import csv
import json
import random

from ..objects.city import City
from ..objects.person import Person
from ..objects.position import Position

nbr_patients = 20
lon_delta = 0.1
lat_delta = 0.1

def parse_cities():
    cities = {}

    with open('data/data_gatherer/full_population_data.csv', newline='') as csvfile:
        city_reader = csv.reader(csvfile)
        for row in city_reader:
            city = City(
                    ident=row[0], 
                    name=row[1], 
                    position=Position(float(row[3]), float(row[4])), 
                    population=int(row[5]), 
                    state=row[6])
            cities[city.ident] = city

    return cities


def sample_patients(cities):
    patient_cities = random.choices(
            population=list(cities.values()),
            weights=[city.population for city in cities.values()],
            k=nbr_patients)

    patients = {}

    for i, patient_city in enumerate(patient_cities):
        patient = Person(
            ident=i,
            position=Position(
                patient_city.position.lat + random.uniform(-lat_delta, lat_delta),
                patient_city.position.lon + random.uniform(-lon_delta, lon_delta)
            ),
            corona_likelihood=random.random(),
            severity=random.random()
        )
        patients[patient.ident] = patient.to_dict()

    return patients


def generate_patients(write=True):
    cities = parse_cities()

    patients = sample_patients(cities)

    if write:
        with open("data/patient_requests/patients.json", "w") as f:
            json.dump(patients, f)

    return patients 
