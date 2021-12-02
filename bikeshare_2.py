import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

WEEK_DAYS   = ['Sunday',
              'Monday',
              'Tuesday',
              'Wednesday',
              'Thursday',
              'Friday',
              'Saturday']

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    city, month, day = '', '', ''
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city == '':
        city = input("Enter cityname (chicago, new york city or washington): ")
        if city.lower() in CITY_DATA.keys():
            break
        else:
            print('Invalid input for city: ' + city)
            city = ''
    # get user input for month (all, january, february, ... , june)
    while month == '':
        month = input("Enter Month (all, january, february, ... , june): ")
        if month.lower() in MONTHS or month.lower() == 'all':
            month = month.lower()
            break
        else:
            print('Invalid input for month: ' + month)
            month = ''

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day == '':
        day = input("Enter day (all, monday, tuesday, ... sunday): ")
        if day.title() in WEEK_DAYS or day.lower() == 'all':
            day = day.lower()
            break
        else:
            print('Invalid input for day: ' + day)
            day = ''

    print('-'*40)
    return city.lower(), month.lower(), day

# reassemble complete code - just c+p from solution 3
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

    # load data file into a dataframe
    print('Filename=', CITY_DATA[city])
    df = pd.read_csv(CITY_DATA[city], sep=',')
    print('Rows loaded: ', len(df.index))

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_of_week

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # extract Start Station and End station and combine
    df['Start End Station'] = df['Start Station'] + ' to ' + df['End Station']

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == WEEK_DAYS.index(day.title())]

    print('Rows filtered: ', len(df.index))

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    # find the most popular month
    popular_month = df['month'].mode()[0]
    print('Most Popular Start Month:', MONTHS[popular_month-1].title())

    # display the most common day of week
    popular_dayofweek = df['day_of_week'].mode()[0]
    print('Most Popular Day of Week:', WEEK_DAYS[popular_dayofweek])

    # print performance time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_startstation = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_startstation)

    # display most commonly used end station
    popular_endstation = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_endstation)

    # display most frequent combination of start station and end station trip
    popular_startendstation = df['Start End Station'].mode()[0]
    print('Most Popular Start End Station:', popular_startendstation)

    # print performance time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time_total = df['Trip Duration'].sum()
    print('Total travel time: ', travel_time_total)

    # display mean travel time
    travel_time_mean = df['Trip Duration'].mean()
    print('Mean travel time: ', travel_time_mean)

    # print performance time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    # print value counts for each user type
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    # TODO: Gender not available for each city
    if 'Gender' in df:
        user_types = df['Gender'].value_counts()
        print(user_types)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print('Earliest year of birth: ', df['Birth Year'].min())
        print('Most recent year of birth: ', df['Birth Year'].max())
        print('Most common year of birth: ', df['Birth Year'].mode()[0])

    # print performance time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def printRows(df, rows):
    """ Displays n rows of a dataframe and asks user to show more"""
    more = True
    row_start = 0
    row_stop = 0

    # loop until user stops or end of dataframe reached
    while more:
        row_stop = row_start + rows
        if (len(df.index)<=row_stop):
            # end of dataframe reached - show only remaining rows
            print(df[row_start:])
        print(df[row_start:row_stop])

        # user decision: more rows to show?
        show_more = input('\nWould you like to see {} more? Enter yes or no.\n'.format(rows))
        if show_more.lower() != 'yes':
            break

        # assign pointer to next row to show
        row_start = row_stop

def main():
    # loop until user stops
    while True:
        # let user specify filter criteria
        city, month, day = get_filters()
        print('Filter set to: city={}, month={}, day={}'.format(city, month, day))

        # load the data from specified files
        df = load_data(city, month, day)

        # call the stats
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # show 5 rows and ask for more
        printRows(df, 5)

        # user decision: more stats to show?
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
