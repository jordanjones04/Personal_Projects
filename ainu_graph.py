#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 13:59:27 2023

@author: jordanjones
"""

import matplotlib.pyplot as plt
import locale

locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')


# Data
percentage_mastered = 4.6  # Replace with the actual percentage from the article
percentage_not_mastered = 100 - percentage_mastered

# Labels for the pie chart
labels = ['Mastered', 'Not Mastered']
sizes = [percentage_mastered, percentage_not_mastered]
colors = ['lightcoral', 'lightblue']
explode = (0.1, 0)  # Explode the "Mastered" slice for emphasis

# Create a pie chart
plt.figure(figsize=(6, 6))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
plt.title('Percentage of Ainu Speakers Who Feel They Can Master the Language')

# Display the pie chart
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()

# Japanese Version

# Data
percentage_mastered = 4.6  # Replace with the actual percentage from the article
percentage_not_mastered = 100 - percentage_mastered

# Labels for the pie chart in Japanese
labels = ['習得済み', '未習得']  # 'Mastered', 'Not Mastered' in Japanese
sizes = [percentage_mastered, percentage_not_mastered]
colors = ['lightcoral', 'lightblue']
explode = (0.1, 0)  # Explode the "習得済み" slice for emphasis

# Create a pie chart
plt.figure(figsize=(6, 6))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
plt.title('アイヌ語を習得と感じる話者の割合')

# Display the pie chart
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()


# Data
age_groups = ['Age 30s', 'Age 60s']
years = ['2006', '2013', '2017']
percentages = {
    'Age 30s': [0, 0, 2.3],
    'Age 60s': [2.3, 1.9, 0.4]
}

# Create a bar chart
fig, ax = plt.subplots(figsize=(10, 6))
width = 0.25

for i, age_group in enumerate(age_groups):
    x = range(len(years))
    y = [percentages[age_group][j] for j in range(len(years))]
    ax.bar([pos + width * i for pos in x], y, width=width, label=f'{age_group}')

# Set labels and title
ax.set_xlabel('Years')
ax.set_ylabel('Percentage')
ax.set_title('Percentage of Ainu People Who Can Have a Conversation in Ainu Language')
ax.set_xticks([pos + width for pos in x])
ax.set_xticklabels(years)
ax.legend(title='Age Groups')

# Display the bar chart
plt.tight_layout()
plt.show()



# Data
labels = ['Able to Have a Conversation', 'Able to Have a Conversation a Little', 'Have a Little Knowledge', 'Not Able to Have a Conversation']
percentages = [0.7, 3.4, 44.6, 48.1]
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
explode = (0.1, 0, 0, 0)  # Explode the first slice for emphasis

# Create a pie chart
plt.figure(figsize=(6, 6))
plt.pie(percentages, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
plt.title('Fluency in the Ainu Language (2017)')

# Display the pie chart
plt.axis('equal')
plt.show()




