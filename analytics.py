import csv
import pandas

data_path = "./StatisticData.csv"


# changing format of hours and dates from GA type to comfortable for analytics, i.e '000058' -> '10'
def date_hours_preprocessing(statistics):
    date_counter = 1
    month = 3
    for event in statistics:
        event["Індекс години"] = str(int(event.get("Індекс години")) - 24*(int(event.get("Індекс години"))//24))
        event["Діапазон дат"] = str('{0:02d}'.format(date_counter) + "." + '{0:02d}'.format(month) + ".2019")
        if date_counter == 31 and event["Сегмент"] == 'Трафік мобільних пристроїв':
            date_counter = 0
            month += 1
        if event["Індекс години"] == str(23) and event["Сегмент"] == 'Трафік мобільних пристроїв':
            date_counter += 1


# changing format of average session duration to time in seconds, i.e '00:01:12:' -> '72'
def time_preprocessing(statistics):
    for event in statistics:
        event["Сер. тривалість сеансу"] = int(event.get("Сер. тривалість сеансу").split(':')[0])*3600 + \
                                          int(event.get("Сер. тривалість сеансу").split(':')[1])*60 + \
                                          int(event.get("Сер. тривалість сеансу").split(':')[2])


# parsing data from source *.csv
def parser(path_to_file):
    statistics = list()
    with open(path_to_file, 'r', encoding='utf-8') as csv_f:
        data = csv.DictReader(csv_f, delimiter=',')
        for event in data:
            statistics.append(event)

    date_hours_preprocessing(statistics)
    time_preprocessing(statistics)
    return statistics


# Splitting data on three segments ('New Users', 'Users who use tablets and PC's', 'Users who use mobiles')
def split_data(data):
    new_users = list()
    pc = list()
    mobile = list()
    for event in data:
        if event["Сегмент"] == 'Нові користувачі':
            new_users.append(event)
        elif event["Сегмент"] == 'Трафік із планшетних і настільних ПК':
            pc.append(event)
        else:
            mobile.append(event)
    return new_users, pc, mobile


# Return max value of average session duration for specific segment
def get_max_value(data):
    max_value = int(data[0]["Сер. тривалість сеансу"])
    for event in data[1:]:
        if max_value < int(event.get("Сер. тривалість сеансу")):
            max_value = int(event.get("Сер. тривалість сеансу"))
    return max_value


# Normalizing data in range [0;1]
def normalize(data):
    max_value = get_max_value(data)
    for event in data:
        event["Сер. тривалість сеансу"] = str('{:.3f}'.format(int(event.get("Сер. тривалість сеансу"))/max_value))


# Return list of all average session duration for specific segment
def get_session_duration(segments):
    sd = list()
    for segment in segments:
        for event in segment:
            sd.append(float(event.get("Сер. тривалість сеансу")))
    return sd


# Return outliers that did not pass the confidence interval
def find_outliers(data, sd):
    x = pandas.Series(sd)
    outliers = list()
    for event in data:
        if float(event.get("Сер. тривалість сеансу")) > x.quantile(.98) or \
                float(event.get("Сер. тривалість сеансу")) < x.quantile(.02):
            outliers.append(event)
    return outliers


# Write results with outliers of each segment to *.csv
def csv_writer(name, data):
    with open(name + ".csv", mode='w', encoding='utf-8', newline='') as csv_file:
        fieldnames = ['Індекс години', 'Діапазон дат', 'Сегмент', 'Сер. тривалість сеансу']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for event in data:
            writer.writerow(event)


if __name__ == '__main__':
    new_users, pc, mobile = split_data(parser(data_path))

    # Normalizing data to range [0;1]
    normalize(new_users)
    normalize(pc)
    normalize(mobile)

    # Get outliers from the data
    new_users_outliers = find_outliers(new_users, get_session_duration([pc, mobile]))
    pc_outliers = find_outliers(pc, get_session_duration([new_users, mobile]))
    mobile_outliers = find_outliers(mobile, get_session_duration([new_users, pc]))

    # Write results to *.csv files
    csv_writer('new_users_outliers', new_users_outliers)
    csv_writer('pc_outliers', pc_outliers)
    csv_writer('mobile_outliers', mobile_outliers)
