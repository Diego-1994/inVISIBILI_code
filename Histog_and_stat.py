# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 10:14:31 2024

@author: Diego
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
from scipy.stats import norm

# Ignore specific warnings
warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)

# File paths
file_paths = {
    'kindergarten': r'C:/Users/Diego/Desktop/Data/data_kindergart.xlsx',
    'primary_1': r'C:/Users/Diego/Desktop/Data/data_primary_1.xlsx',
    'primary_2': r'C:/Users/Diego/Desktop/Data/data_primary_2.xlsx',
    'primary_3': r'C:/Users/Diego/Desktop/Data/data_primary_3.xlsx',
    'primary_4': r'C:/Users/Diego/Desktop/Data/data_primary_4.xlsx',
    'primary_5': r'C:/Users/Diego/Desktop/Data/data_primary_5.xlsx',
    'secondary': r'C:/Users/Diego/Desktop/Data/data_secondary_1.xlsx'
}

# Prompt the user to enter the column name to analyze
column_name = input("Please enter the column name you want to analyze: ")

# Loop through files to obtain percentage for each answer:
for category, path in file_paths.items():
    try:
        # Load the data
        df = pd.read_excel(path)

        # Check if the column exists in the DataFrame
        if column_name not in df.columns:
            print(f"Column '{column_name}' does not exist in {category}. Skipping to the next file.")
            continue  # Skip to the next file

        # Filter the DataFrames to exclude the specified column's value 0
        df_male = df[(df['Gender'] == 'M') & (df[column_name] != 0)]
        df_female = df[(df['Gender'] == 'F') & (df[column_name] != 0)]

        # Determine the appropriate reindexing based on the data
        max_value_male = df_male[column_name].max()  # Find the maximum value for males
        max_value_female = df_female[column_name].max() # Find the maximum value for females

        # Set reindex values based on the maximum value
        if max_value_male > 3 or max_value_female > 3:
            range_values = [1, 2, 3, 4, 5]
        else:
            range_values = [1, 2, 3]

        counts_specific_male = df_male[column_name].value_counts().reindex(range_values, fill_value=0)
        print(f"Category: {category.capitalize()} - Boys")
        print(counts_specific_male)
        counts_percentage_male = counts_specific_male / counts_specific_male.sum() * 100

        counts_specific_female = df_female[column_name].value_counts().reindex(range_values, fill_value=0)
        print(f"Category: {category.capitalize()} - Girls")
        print(counts_specific_female)
        counts_percentage_female = counts_specific_female / counts_specific_female.sum() * 100

        # Plot histograms for both boys and girls side by side
        plt.figure(figsize=(8, 6))
        bar_width = 0.35
        positions_male = np.array(range_values) - bar_width / 2
        positions_female = np.array(range_values) + bar_width / 2
        plt.bar(positions_male, counts_percentage_male, width=bar_width, color='blue', edgecolor='black', label='Boys')
        plt.bar(positions_female, counts_percentage_female, width=bar_width, color='pink', edgecolor='black', label='Girls')
        
        event_context = "after events" if "2" in column_name else "before events"
        save_name = column_name
        
        if column_name == "who for" or column_name == "who for 2":
            plot_name = "Who is science for?"
        elif column_name == "who is able" or column_name == "who is able 2":
            plot_name = "Who is able to do science?"
        elif column_name == "who likes" or column_name == "who likes 2":
            plot_name = "Who likes science?"
        elif column_name == "like objects" or column_name == "like objects 2":
            plot_name = "Would you like to play with these objects?"
        elif column_name == "interest" or column_name == "interest 2":
            plot_name = "How much are you interested in science?"
        elif column_name == "like science" or column_name == "like science 2":
            plot_name = "Do you like science?"
        elif column_name == "becoming scientist" or column_name == "becoming scientist 2":
            plot_name = "Would you like to become a scientist?"            
        elif column_name == "good in science" or column_name == "good in science 2":
            plot_name = "Do you think you will be good at science in school?"

        plt.xticks(range_values)
        plt.xlabel('Answers')
        plt.ylabel('Percentage (%)')
        plt.title(f'{plot_name} ({event_context}) / {category.capitalize()} Boys and Girls')
        plt.legend(loc='upper right')

        # Save the plot to a file
        plot_filename = f'C:/Users/Diego/Desktop/Data/{category}_{save_name}_{event_context}.png'
        plt.savefig(plot_filename, format='png')  # Save the plot
        plt.close()  # Close the plot to free memory

    except KeyError:
        print(f"Column '{column_name}' does not exist in {category}. Skipping to the next file.")
        continue  # Skip to the next file if the column doesn't exist
        
for category, path in file_paths.items():
    try:
        # Load the data
        df = pd.read_excel(path)

        # Check if the column exists in the DataFrame
        if column_name not in df.columns:
            print(f"Column '{column_name}' does not exist in {category}. Skipping to the next file.")
            continue  # Skip to the next file

        # Filter the DataFrames to exclude the specified column's value 0
        df_male = df[(df['Gender'] == 'M') & (df[column_name] != 0)]
        df_female = df[(df['Gender'] == 'F') & (df[column_name] != 0)]

        # Normalize data for the bias analysis
        df_male[f'pre_bias_{column_name}'] = df_male[column_name] - 2
        df_female[f'pre_bias_{column_name}'] = df_female[column_name] - 2

        # Get statistics and print
        wholikes_stereotype_M = df_male[f'pre_bias_{column_name}'].describe()
        print(f"Statistics: {category.capitalize()} - Boys")
        print(wholikes_stereotype_M)
        
        wholikes_stereotype_F = df_female[f'pre_bias_{column_name}'].describe()
        print(f"Statistics: {category.capitalize()} - Girls")
        print(wholikes_stereotype_F)

        # Loop to create histograms for both boys and girls
        for gender_df, gender_label in zip([df_male, df_female], ['Boys', 'Girls']):
            # Calculate mean and standard deviation
            mean = gender_df[f'pre_bias_{column_name}'].mean()
            std_dev = gender_df[f'pre_bias_{column_name}'].std()

            # Create the histogram with Gaussian curve
            plt.figure(figsize=(8, 6))
            plt.hist(gender_df[f'pre_bias_{column_name}'], bins=[-1.5, -0.5, 0.5, 1.5], edgecolor='black', rwidth=0.8, density=True)

            # Create Gaussian curve
            x_values = np.linspace(-2, 2, 100)
            gaussian_y_values = norm.pdf(x_values, mean, std_dev)
            plt.plot(x_values, gaussian_y_values, color='red', linewidth=2, label='Gaussian Fit')

            # Create the plot and a box showing mean and standard deviation:
            plt.xticks(range(-2, 3))
            plt.xlabel('Deviation from gender-neutral')
            plt.ylabel('Density')
            plt.title(f'{column_name}? / {category.capitalize()} {gender_label} / Bias')
            plt.legend()

            textstr = f'Mean: {mean:.2f}\nStd Dev: {std_dev:.2f}'
            plt.text(0.05, 0.95, textstr, transform=plt.gca().transAxes, fontsize=12,
                     verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))

            plt.show()

    except KeyError:
        print(f"An error occurred while processing {category}. Skipping to the next file.")
        continue  # Skip to the next file if there's any error

