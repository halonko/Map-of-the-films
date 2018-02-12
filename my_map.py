import folium
import file_read
from geopy.geocoders import ArcGIS


def find_location(place):
    '''
    :param place: a place where film was made/produced
    :return: latitude and longitude
    '''
    geolocator = ArcGIS(timeout=10)
    location = geolocator.geocode(place)
    lat = location.latitude
    long = location.longitude
    return lat, long


def map_creation(lat, long, name, fgroup, maps):
    '''

    :param lat: a latitude of some place
    :param long: a longitude of some place
    :param name: the name of the film
    :param fgroup: a group of markers, where a poins is added
    :param maps: a needed map, where this markers are shown
    :return: None
    '''
    fgroup.add_child(folium.Marker(location=[lat, long],
                                   popup=str(name).replace("'", "`"),
                                   icon=folium.Icon()))
    maps.add_child(fgroup)
    maps.save(' Map.html ')


def create_layer_population(path, maps):
    '''

    :param path: a way to a file you want to use
    :param maps: a map where population will be seen
    :return: None
    '''
    fg_pp = folium.FeatureGroup(name="Population")
    fg_pp.add_child(folium.GeoJson(data=open(path, 'r',
                                   encoding='utf-8-sig').read(),
                                   style_function=lambda x: {
                                   'fillColor': 'blue'
                                   if x['properties']['POP2005'] < 10000000
                                   else 'green' if 10000000 <=
                                   x['properties']['POP2005'] < 100000000
                                   else 'red'}))
    maps.add_child(fg_pp)
    maps.save(' Map.html ')


def create_layer_area(path, maps):
    '''

    :param path: A way to a needed file
    :param maps: A map where countries area`s will be seen
    :return: None
    '''
    fg_xp = folium.FeatureGroup(name="Area")
    fg_xp.add_child(folium.GeoJson(data=open(path, 'r',
                                   encoding='utf-8-sig').read(),
                                   style_function=lambda x: {
                                   'fillColor': 'yellow'
                                   if x['properties']['AREA'] < 1000
                                   else 'green' if 1000 <=
                                   x['properties']['AREA'] < 10000
                                   else 'blue' if 10000 <=
                                   x['properties']['AREA'] < 100000
                                   else 'red'}))
    maps.add_child(fg_xp)
    maps.save(' Map.html ')


def main():
    # Creating a map and two layers - areas and populations
    print('Creating a map whith two layers - areas of the countries and '
          'populations')
    mapa = folium.Map()
    fg = folium.FeatureGroup(name="Films map")
    create_layer_population('world.json', mapa)
    create_layer_area('world.json', mapa)
    # Working with the file
    print('Working with the file...')
    list_loc = file_read.read_file('loc.txt')
    tuples_set = file_read.create_set(list_loc)
    # Inputing a year of the films
    year = int(input("What year you want? "))
    assert year >= 1883, 'The films hadn`t produced yet'

    print("Finding coordinates of where these films were produced...")
    main_dict = file_read.map_dict(tuples_set, year)
    for i, j in main_dict.items():
        try:
            lat, long = find_location(i)
        except AttributeError:
            continue
        map_creation(lat, long, j, fg, mapa)
    mapa.add_child(folium.LayerControl())
    mapa.save(' Map.html ')


main()
