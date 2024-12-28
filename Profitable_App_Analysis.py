# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 10:21:14 2024

@author: User
"""

#Profitable App Profiles for the App Store and Google Play Markets#
#Our aim in this project is to find mobile app profiles that are profitable for the App Store and Google Play markets.#

#open the CSV files for Google play dataset and ios dataset##
from csv import reader


# Google play dataset
open_file =open('googleplaystore.csv')
read_file = reader(open_file)
android = list(read_file)
android_header = android[0]
android_file = android[1:]

# ios dataset
open_file =open('AppleStore.csv')
read_file = reader(open_file)
ios       = list(read_file)
ios_header = ios[0]
ios_file = ios[1:]

# Function to explore a slice of the dataset

def explore_data(dataset,start,end,row_and_column = False):
    dataset_slice =dataset[start:end]
    for row in dataset_slice:
        print(row)
        print('\n') # Add a empty line in between for readibility
        
    if row_and_column:
        print('Number of row:', len(dataset))
        print('Number of Column:', len(dataset[0]))
        
# Display headers and a sample of data        
print(android_header)
print('\n')
explore_data(android_file, 0, 3, True)

print(ios_header)
print('\n')
explore_data(ios_file, 0, 3, True)

print(len(android_file))

## Section 1: Removing the wrong data##


# investigate inaccurate data in the dataset
print(android_file[10472]) #'Category is missing'
print('\n')
print(android_header)
print('\n')
print(android_file[1])


# Remove inaccurate data
del android_file[10472]
print(len(android_file))

for app in android_file:
    name = app[0]
    if name == 'Instagram':
        print(app)


## Section 2: Removing the duplicate data##

# Identify duplicate apps


duplicate_apps = []
unique_apps = []

for app in android_file:
    name = app[0]
    if name in unique_apps:
        duplicate_apps.append(name)
    else:
        unique_apps.append(name)
        
        
# Determine the number of duplicate apps

print('Number os duplicate apps: ', len(duplicate_apps))
print('\n')

print('Example of duplicate apps: ', duplicate_apps[:15])

# Expected length of dataset after removing the dataset

print('Expected length',len(android_file) -1181)

## Section 3: To get the most popular apps ##

##Create a dict to catch the highest reviews##

reviews_max = {}

for app in android_file:
    name = app[0]
    n_reviews = float(app[3])
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
    elif name not in reviews_max:
        reviews_max[name] = n_reviews
        
print('Actual Length:', len(reviews_max))


# Remove duplicate rows, keeping the one with highest reviews

android_clean = []
already_added = []

for app in android_file:
    name = app[0]
    n_reviews = float(app[3])
    
    if (reviews_max[name] == n_reviews) and (name not in already_added):
        android_clean.append(app)
        already_added.append(name) 
        
        
print(len(android_clean))  

# Verify the cleaned dataset


explore_data(android_clean, 0, 3, True)

## Section 4: Explore non-English app names 

print(ios[813][1]) # Example non-English apps
print(ios[6731][1])

print(android_clean[4412][0])
print(android_clean[7940][0])


# Function to determine the a string containing the most English Character 

def is_english(string):
    non_ascii = 0
    
    for character in string:
        if ord(character) > 127:
            non_ascii += 1
        if non_ascii > 3:
            return False
        else:
            return True
            
# Test is_english function
print(is_english('Docs To Go™ Free Office Suite'))
print(is_english('Instachat 😜'))

# Filter dataset to include only English apps

android_english = []
ios_english = []

for app in android_clean:
    name = app[0]
    if is_english(name):
        android_english.append(app)
        
for app in ios:
    name = app[1]
    if is_english(name):
        ios_english.append(app)
        



# Verify English apps Datasets 

explore_data(android_english, 0, 3, True)
print('\n')
explore_data(ios_english, 0, 3, True)


## Section 5: To include only free apps
android_final = []
ios_final = []

for app in android_english:
    price = app[7]
    if price == '0':
        android_final.append(app)
        
for app in ios_english:
    price = app[4]
    if price == '0.0':
        ios_final.append(app)
        
print(len(android_final))
print(len(ios_final))

# Function to generate frequency tables 

def freq_table(dataset, index):
    table = {}
    total = 0
    
    for row in dataset:
        total += 1
        value = row[index]
        if value in table:
            table[value] += 1
        else:
            table[value] = 1
    
    table_percentages = {}
    for key in table:
        percentage = (table[key] / total) * 100
        table_percentages[key] = percentage 
    
    return table_percentages

# Function to display frequency table in descending order 

def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)
        
    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])
        
# Display frequency Tables 
print('iOS Genres:')        
display_table(ios_final, -5)

print('\nAndroid Categories:')
display_table(android_final, 1) 

print('\nAndroid Genres:')
display_table(android_final, -4)

# Analyze the most popular apps by genre on the App Store

genres_ios = freq_table(ios_final, -5)

for genre in genres_ios:
    total = 0
    len_genre = 0
    for app in ios_final:
        genre_app = app[-5]
        if genre_app == genre:            
            n_ratings = float(app[5])
            total += n_ratings
            len_genre += 1
    avg_n_ratings = total / len_genre
    print(genre, ':', avg_n_ratings)


# Example: Navigation apps    
for app in ios_final:
    if app[-5] == 'Navigation':
        print(app[1], ':', app[5]) 
        
# Analyze the most popular genres on Google Play

categories_android = freq_table(android_final, 1)

for category in categories_android:
    total = 0
    len_category = 0
    for app in android_final:
        category_app = app[1]
        if category_app == category:
            n_installs = app[5]
            n_installs =n_installs.replace(',','')
            n_installs =n_installs.replace('+','')
            total += float(n_installs)
            len_category += 1
    avg_n_installs = total / len_category
    print(category, ':', avg_n_installs)
    
# Example: Communication apps with high installs    
for app in android_final:
    if app[1] == 'COMMUNICATION' and (app[5] == '1,000,000,000+'
                                      or app[5] == '500,000,000+'
                                      or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])
    
        











































