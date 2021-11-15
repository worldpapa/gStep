import csv
import datetime

# --------------------------------MAGIC----------------------

def get_csv(weekday, year, month, amount_of_lines, show_headers=False):
    for p in [weekday, year, month, amount_of_lines]:
        if not type(p) is int:
            raise ValueError("Invalid parameter type '%s'.  This parameter should be an integer" % str(p))
    if year < 2012 or year > 2014:
        raise ValueError("Please enter a year between 2012 and 2014")
    if weekday < 1 or weekday > 7:
        raise ValueError("Please enter a group number between 1 and 7")
    if month < 1 or month > 12:
        raise ValueError("Please enter a month number between 1 and 12")
    month = prettify_month(month)
    return_string = ''
    with open('/srv/jupyterhub/data/group%d/%s-%s.csv' % (weekday, year, month)) as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            if row[1].strip() == 'Date' and not show_headers:
                continue
            if i > amount_of_lines:
                break
            i += 1
            
            return_string += '%s\n' % str(row)
        return return_string


    
    
def prettify_month(month):
    month = str(month)
    if len(month) == 1:
        month = '0%s' % month
    return month
    
def get_data(weekday, year, month, time='07:00', hard=False):
    """
    :param weekday: The day of the week as an integer
    :param year: the year for the data.  Values between 2011 and 2013
    :param month: the month for the data.  1 is January, 12 is December
    :param time: Default 07:00.  The time of interest.  This should be a string in padded 24 hour format,
    e.g. 07:00, 14:00
    :param hard: Default False.  Specifies whether this function is being used for the standard or "hard" version
    of the question.
    :return: A dictionary of the data for the whole route at the time of interest for every day found.
    If hard is True, then it will return as {time: {junction: segment_time}}
    """
    data_dict = {}
    year = str(year)
    month = prettify_month(month)

    with open('/srv/jupyterhub/data/group%d/%s-%s.csv' % (weekday, year, month)) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1].strip() == 'Date':
                continue
            junction = int(row[0])
            segment_time = row[2]
            journey_time = float(row[3].strip())
            day = int(row[1].split('-')[2])

            if not hard and not segment_time.strip() == time:
                continue
            if day not in data_dict:
                data_dict[day] = {}
            if not hard:
                data_dict[day][junction] = float(journey_time)
            else:
                if segment_time not in data_dict[day]:
                    data_dict[day][segment_time] = {}
                data_dict[day][segment_time][junction] = float(journey_time)

        return_list = []
        for d in sorted(data_dict.keys()):
            return_list.append(data_dict[d])
        return return_list


def get_arrival_time(leaving_time, total_seconds):
    """
    :param leaving_time: The leaving time.  Must be in the format HH:MM (24 hour)
    :param total_seconds: The amount of time the journey takes in seconds
    :return: a datetime object of the arrival time
    """
    leaving = datetime.datetime.strptime(leaving_time, "%H:%M")
    arrival = leaving + datetime.timedelta(seconds=total_seconds)

    return datetime.datetime.strftime(arrival, "%H:%M:%S")


def get_next_time(time):
    current_time = datetime.datetime.strptime(time, "%H:%M")
    return datetime.datetime.strftime(current_time + datetime.timedelta(minutes=15), "%H:%M")


# ----------------------------END MAGIC----------------------


def get_time_in_seconds(str_time):
    """
    Returns the amount of seconds since midnight for the given time string
    :str_time is a time string in the format 'HH:MM:SS' or 'HH:MM' (24 hours)
    """    
    if len(str_time.split(':')) == 2:
           str_time += ':00'    
    time_object = datetime.datetime.strptime(str_time, '%H:%M:%S')
    return (time_object - datetime.datetime.strptime('00:00', '%H:%M')).seconds


def get_time_in_str(seconds):
    """
    Returns a string of the time as 'HH:MM'
    :seconds is the amount of seconds since midnight
    """
    a = datetime.datetime(1900,1,1,0,0,0)
    b = a + datetime.timedelta(seconds=seconds)
    return datetime.datetime.strftime(b, '%H:%M')





