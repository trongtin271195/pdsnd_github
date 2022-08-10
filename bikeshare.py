import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
MONTH_DATA = ['all', 'january', 'february', 'march', 'april', 'may', 'june',
              'july', 'august', 'september', 'october', 'november', 'december']
DOW_DATA = ['monday', 'tuesday', 'wednesday', 'thursday',
            'friday', 'saturday', 'sunday', 'all']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Please enter city name: ").lower()

        if city in CITY_DATA.keys():
            break

        print(f"'{city}' has not supported yet.\n")
        print(
            f"Please try with following cities: {[x for x in CITY_DATA.keys()]}")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input(
            "Please input filtering month (all, january, february, ... , june): ").lower()

        if month in MONTH_DATA or month in [x[:3] for x in MONTH_DATA]:
            if month == 'all':
                months = [i+1 for i, _ in enumerate(MONTH_DATA[1:])]
            elif len(month) == 3:
                months = [i for i, x in enumerate(
                    MONTH_DATA) if x[:3] == month]
            else:
                months = [i for i, x in enumerate(MONTH_DATA) if x == month]
            break

        print(f"'{month}' is invalid.\n")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        dow = input(
            "Please input filtering day of week (all, monday, tuesday, ... sunday):").lower()

        if dow in DOW_DATA or dow in [x[:3] for x in DOW_DATA]:
            if dow == 'all':
                dows = [i for i, _ in enumerate(DOW_DATA[:7])]
            elif len(dow) == 3:
                dows = [i for i, x in enumerate(DOW_DATA) if x[:3] == dow]
            else:
                dows = [i for i, x in enumerate(DOW_DATA) if x == dow]
            break
        
        print(f"'{dow}' is invalid.\n")

    print(f"'{city}' will be filterd with months ({months}) and day of week ({dows})")
    print('-'*40)
    return city, months, dows


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Read csv file and remove NaN records
    df = pd.read_csv(CITY_DATA[city])
    df.dropna()

    # Convert string into datetime value
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Filter record in filtering month
    df['Month'] = df['Start Time'].dt.month
    df = df.loc[df['Month'].isin(month)]

    # Filter record in filtering day of week
    df['DoW'] = df['Start Time'].dt.dayofweek
    df = df.loc[df['DoW'].isin(day)]

    return df


def display_raw_data(df):
    """Displays raw data for user."""

    i = 0
    raw = input(
        "\nWould you like to view first 5 rows? Enter yes (y) or no (n).\n").lower()
    pd.set_option('display.max_columns', 200)

    while True:
        if raw == 'no' or raw == 'n':
            break
        elif raw == 'yes' or raw == 'y':
            print(df.iloc[i:i+5, :])
            raw = input(
                "\nWould you like to view next 5 rows? Enter yes (y) or no (n).\n").lower()
            i += 5
        else:
            raw = input(
                "\nYour input is invalid. Please enter only 'yes'/'y' or 'no'/'n'\n").lower()


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month = df['Month'].value_counts(sort=True).index[0]
    print(f"The most common month is '{MONTH_DATA[month]}'")

    # display the most common day of week
    dow = df['DoW'].value_counts(sort=True).index[0]
    print(f"The most common day of week is '{DOW_DATA[dow]}'")

    # display the most common start hour
    hour = df['Start Time'].dt.hour.value_counts(sort=True).index[0]
    print(f"The most common start hour is '{hour}'")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].value_counts(sort=True).index[0]
    print(f"The most commonly used start station is '{start_station}'")

    # display most commonly used end station
    end_station = df['End Station'].value_counts(sort=True).index[0]
    print(f"The most commonly used end station is '{end_station}'")

    # display most frequent combination of start station and end station trip
    trip = (df['Start Station'] + ' - ' + df['End Station']
            ).value_counts(sort=True).index[0]
    print(
        f"The most frequent combination of start station and end station trip is '{trip}'")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total = (df['End Time'] - df['Start Time']).sum().total_seconds()
    print(f"The total travel time is '{total}' seconds")

    # display mean travel time
    avg = total / len(df)
    print(f"The total travel time is '{avg}' seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    types = df['User Type'].value_counts()
    print("The counts of user types:")
    print(types)

    # Display counts of gender
    if 'Gender' in df.columns:
        genders = df['Gender'].value_counts()
        print("/nThe counts of gender:")
        print(genders)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        year = df['Birth Year'].value_counts(sort=True).index.tolist()
        common = year[0]
        year.sort()
        earliest = year[0]
        recent = year[-1]
        print(f"The earliest year of birth: {earliest}")
        print(f"The most recent year of birth: {recent}")
        print(f"/nThe most common year of birth: {common}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, months, dows = get_filters()
        df = load_data(city, months, dows)

        if len(df) == 0:
            print("\nThere is no available data to analyze. Please try again.\n")
            continue

        display_raw_data(df)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        while True:
            if restart == 'no' or restart == 'n':
                exit()
            elif restart == 'yes' or restart == 'y':
                break
            else:
                restart = input(
                    "\nYour input is invalid. Please enter only 'yes'/'y' or 'no'/'n'\n").lower()


if __name__ == "__main__":
    main()
