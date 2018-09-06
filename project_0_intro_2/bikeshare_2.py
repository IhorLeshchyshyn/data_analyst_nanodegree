import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    city=input('Which city would you like to see data from?Chicago, New York, or Washington?\n').lower()
    while city not in ['chicago', 'new york', 'washington']:
        print ("Try again")
        city=input().lower()
    if city=='new york':
        city='new york city'
    # get user input for month (all, january, february, ... , june)
    month=input('Which month would you like to see data from?January, February, March, April, May, June?Type \'all\' for all months\n').lower()
    while month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
        print ("Try again")
        month=input().lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day=input('Which day of week would you like to see data from? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday? Type \'all\' for all days\n').lower()
    while day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
        print ("Try again")
        day=input().lower()

    print('-'*40)
    return city, month, day


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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] =df['Start Time'].dt.hour
    
    
    # filter by month if applicable
    if month != 'all':
    # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        
        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]
    
    # filter by day of week if applicable
    if day != 'all':
    # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
        Args:
        df - Pandas DataFrame containing city data filtered by month and day
        Input : takes the df which was filtred in load_data() as input.
        Output : print some statistics such as : popular month, day and hour."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month
    popular_month=df['month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print ('The most popular month:',months[popular_month-1].title())
    #the variable "popular_month" is an integer, so in order to get the month(as a string rather than a int), it requires to minus - 1 to get the correct index for list "months".
    
    # display the most common day of week
    popular_day=df['day_of_week'].mode()[0]
    print ('The most popular day:',popular_day)
    # display the most common start hour
    popular_hour=df['hour'].mode()[0]
    print ('The most popular hour:',popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
        Args:
        df - Pandas DataFrame containing city data filtered by month and day
        Input : takes the df which was filtred in load_data() as input.
        Output : print some statistics such as : the most commonly used start station, end station
        and the most frequent combination of start station and end station trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_common_station=df['Start Station'].mode()[0]
    print ('The most commonly used start station:', start_common_station)

    # display most commonly used end station
    end_common_station=df['End Station'].mode()[0]
    print ('The most commonly used end station:', end_common_station)

    # display most frequent combination of start station and end station trip
    combination=df.groupby(['Start Station','End Station']).count()['Start Time'].idxmax()            #was changed
    print ('The most frequent combination of start station and end station trip: {} and {}'.format(*combination))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
        Args:
        df - Pandas DataFrame containing city data filtered by month and day
        Input : takes the df which was filtred in load_data() as input.
        Output : print some statistics such as : total travel time and mean travel time."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time=df['Trip Duration'].sum()
    print ('The total travel time:',total_travel_time)

    # display mean travel time
    mean_travel_time=df['Trip Duration'].mean()
    print ('The mean travel time:',mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users.
        Args:
        df - Pandas DataFrame containing city data filtered by month and day
        Input : takes the df which was filtred in load_data() as input.
        Output : print some statistics such as : counts of user types, counts of gender and
        earliest, most recent, and most common year of birth.
        For Washington, the data isn't available, so the output will be only counts of user types."""
    
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print ('What is the breakdown of users?')
    counts_of_users=df['User Type'].value_counts()
    print (counts_of_users)

    # Display counts of gender
    #Gender column isn't available in 'Washington.csv'
    if 'Gender' not in df.columns:
        print ('Gender data isn\'t available')
    else:
        print ('What is the breakdown of gender?')
        counts_of_gender=df['Gender'].value_counts()
        print (counts_of_gender)

    # Display earliest, most recent, and most common year of birth
    #Birth Year column isn't available in 'Washington.csv'
    if 'Birth Year' not in df.columns:
        print ('Birth year data isn\'t available')
    else:
        earliest=df['Birth Year'].min()
        recent=df['Birth Year'].max()
        common_year_birth=df['Birth Year'].mode()[0]
        print ('The earliest year of birth: {}\nThe most recent year of birth: {}\nThe most common year of birth {}'.format(earliest,recent,common_year_birth))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
