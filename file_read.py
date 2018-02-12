def read_file(new_file):
    '''
    file -> list
    :param new_file: A file you want to read
    :return: list of the lines of the file
    '''
    with open(new_file, 'r', encoding='utf-8', errors='ignore') as \
            txt_locations:
        txt_locations = txt_locations.readlines()
    return txt_locations


def create_set(lst):
    '''
    Writes all needed infomation into tuples (Ex.->(year, place, name)),
    then coverts it to a set
    :param lst: list of the lines, made of read_file function
    :return: A set of tuples
    '''
    new_set = set()
    for loc in lst:
        loc = loc.strip('\n')
        location = loc.split('\t')
        need_tuple = find_year(location[0])
        if len(location) >= 2:
            i = 1
            while location[i] == '':
                location.remove(location[i])
            result_tuple = (need_tuple[0], location[1], need_tuple[1])
            new_set.add(result_tuple)
        else:
            continue
    return new_set


def find_year(line):
    '''
    An additional function to the create_set
    Finds a year from the unformed string
    :param line: a string of a list of the function read_file
    :return: year, film: returns a tuple with a year and a film
    '''
    for i in range(len(line)):
        if line[i] == '(':
            try:
                year = int(line[i+1: i+5])
            except ValueError:
                year = line[i+1: i+5]
            film = line[0: i-1]
            return year, film


def map_dict(sett, year):
    '''
    Makes a dictionary from a tuple that
    is an element of the set
    (Ex. ((needed year, place, name)->{location: name)
    :param sett:
    :param year:
    :return: dictionary of the location as key and name of the film as value
    '''
    dictionary = {}
    for i in sett:
        if i[0] == year:
            dictionary.update({i[1]: i[2]})
        else:
            continue
    return dictionary
