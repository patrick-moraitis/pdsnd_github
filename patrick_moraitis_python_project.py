#python project submission by Patrick Moraitis October 17, 2019

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'data/chicago.csv',
              'new york city': 'data/new_york_city.csv',
              'washington': 'data/washington.csv' }

# making this array global so I can use it in various scopes
months = ['january', 'february', 'march', 'april', 'may', 'june']

#days of week array to validate filter input
days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or 'all' to apply no month filter
        (str) day - name of the day of week to filter by, or 'all' to apply no day filter
    """
    print('HOWDY! Let\'s explore some US bikeshare data!')

    """get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs"""

    # declare empty variable to ensure first iteration of while loop runs
    city = None

    # run this while loop until user enters valid option
    while city not in CITY_DATA:
        city = input('Enter a city (Chicago, New York City, Washington): ').lower()
        
        #check if input is a invalid option, if so alert the user to try again
        if city not in CITY_DATA:
            print('Not a valid response, please try again')


    """get user input for month (all, january, february, ... , june)"""
    
    # declare empty variable to ensure first iteration of while loop runs
    month = None

    # run this while loop until user enters valid option
    while month not in months and month != 'all':
        month = input('Enter a month filter (January to June) or ALL for no filter: ').lower()

        #check if input is a invalid option, if so alert the user to try again
        if month not in months and month != 'all':
            print('Not a valid response, please try again')

    """get user input for day of week (all, monday, tuesday, ... sunday)"""
    
    # declare empty variable to ensure first iteration of while loop runs
    day = None

    # run this while loop until user enters valid option
    while day not in days_of_week and day != 'all':
        day = input('Enter a day filter (Monday to Sunday( or ALL for no filter: ').lower()

        #check if input is a invalid option, if so alert the user to try again
        if day not in days_of_week and day != 'all':
            print('Not a valid response, please try again')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or 'all' to apply no month filter
        (str) day - name of the day of week to filter by, or 'all' to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # load the correct csv file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, & hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # create a new column to show to and from stations
    df['to_and_from_station'] = df['Start Station'] + ' -to-> ' + df['End Station']


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    #print(df)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = months[df['month'].mode()[0]-1].title()
    print('The most common month is: {}'.format(most_common_month))

    # display the most common day of week
    most_common_dow = df['day_of_week'].mode()[0]
    print('The most common day of week is: {}'.format(most_common_dow))

    # display the most common start hour
    most_common_start_hour = df['hour'].mode()[0]

    #convert start hours into more readable formats
    most_common_start_hour_24 = str(most_common_start_hour) + ':00'

    if most_common_start_hour > 12:
        most_common_start_hour_12 = str(most_common_start_hour - 12) + ':00 PM'
    else:
        most_common_start_hour_12 = str(most_common_start_hour) + ':00 AM'

    print('The most common start hour is: {} which is {}'.format(most_common_start_hour_24, most_common_start_hour_12))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most common start station is: {}'.format(most_common_start_station))

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('The most common end station is: {}'.format(most_common_end_station))

    # display most frequent combination of start station and end station trip
    most_common_trip = df['to_and_from_station'].mode()[0]
    print('The most common trip is: {}'.format(most_common_trip))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time in seconds and hours
    total_travel_time = np.sum(df['Trip Duration'])
    print('The total time spent traveling is: {} seconds which is {} hours'.format(total_travel_time, (total_travel_time/60/60)))

    # display mean travel time in seconds and minutes
    average_trip_time = np.mean(df['Trip Duration'])
    print('The average trip duration is: {} seconds which is {} minutes'.format(average_trip_time, (average_trip_time/60)))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df['User Type'].value_counts()
    print('The distribution of user types: \n{}'.format(user_type_counts))

    # Display counts of gender
    # includes exception handling for data set not containing gender data
    try:
        gender_counts = df['Gender'].value_counts()
        print('\nThe distribution of genders: \n{}\n'.format(gender_counts))
    except KeyError:
        print('\nNo gender data available\n')

    # Display earliest, most recent, and most common year of birth
    # convert values into int to remove the trailing '.0' in order to make the year more readable
    # includes exception handling for data set not containing birth year data

    try:
        min_birth_year = int(df['Birth Year'].min())
        max_birth_year = int(df['Birth Year'].max())
        mode_birth_year = int(df['Birth Year'].mode()[0])
        
        print('The earliest birth year is: {}'.format(min_birth_year))
        print('The most recent birth year is: {}'.format(max_birth_year))
        print('The most common birth year is: {}'.format(mode_birth_year))
    
    except KeyError:
        print('\nNo birth year data available\n')

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        #print(df)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes to restart or enter anything else to exit.\n')
        if restart.lower() != 'yes':
            break


if __name__ == '__main__':
	main()
