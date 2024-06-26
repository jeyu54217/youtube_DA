
from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt

# List of keywords to compare
KEYWORDS = [
    "London",
    "Edinburgh",
    "Manchester",
    "Birmingham",
    "Glasgow",
    "Liverpool",
    "Bristol",
    "Oxford",
    "Cambridge",
    "York",
    "Bath",
    "Newcastle upon Tyne",
    "Brighton",
    "Leeds",
    "Cardiff",
    "Belfast",
    "Nottingham",
    "Sheffield",
    "Aberdeen",
    "Dundee",
    "Inverness",
    "Norwich",
    "Chester",
    "Canterbury",
    "Windsor",
    "Durham",
    "St Albans",
    "Portsmouth",
    "Exeter",
    "Stratford-upon-Avon"
    
]

# GROUP='youtube'

def get_google_trend(keywords=[], 
                     gprop='', 
                     chunk_size=5,
                     geo=''):
    # Function to split list into chunks of a specific size
    def chunker(keywords, chunk_size=chunk_size):
        return (keywords[pos:pos + chunk_size] for pos in range(0, len(keywords), chunk_size))
    

    # Initialize pytrends
    pytrends = TrendReq(hl='en-GB', tz=360)

    # Get data for each chunk
    all_data = []
    for chunk in chunker(keywords, chunk_size):
        pytrends.build_payload(chunk, timeframe='today 24-m', gprop=gprop, geo=geo)
        interest_over_time_df = pytrends.interest_over_time()
        all_data.append(interest_over_time_df)

    

    # Combine all dataframes
    combined_df = pd.concat(all_data, axis=1)
    
    # Drop the 'isPartial' column
    combined_df = combined_df.loc[:,~combined_df.columns.duplicated()]
    combined_df = combined_df.drop(columns=['isPartial'])
    print(combined_df)
    
    return combined_df

def to_csv(df, filename='google_trends.csv'):
    try:
        df.to_csv(filename)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(e)



def drop_low_values(df, threshold=20):
    # Calculate the average value for each city
    average_values = df.mean()

    # Drop cities with mean value lower than 20
    filtered_average_values = average_values[average_values >= threshold]

    # Filter the dataframe
    filtered_df = df[filtered_average_values.index]

    return filtered_df

def plot_google_trends(df):
    '''
    # Calculate the average value for each city
    average_values = df.mean()

    # Drop cities with mean value lower than 20
    filtered_average_values = average_values[average_values >= 20]

    # Plotting the average values
    plt.figure(figsize=(14, 8))
    filtered_average_values.plot(kind='bar', color='skyblue')

    # Add title and labels
    plt.title('Average Google Trends Over Time for Popular Travel Cities in the UK (Filtered)')
    plt.xlabel('Cities')
    plt.ylabel('Average Interest Over Time')
    plt.xticks(rotation=45)
    plt.grid(True, axis='y')

    # Show plot
    plt.tight_layout()
    plt.show()
    '''
    # Calculate the average value for each city
    average_values = df.mean()
    print(average_values)
    # Plotting the data
    plt.figure(figsize=(14, 8))
    for column in df.columns:
        plt.plot(df.index, df[column], label=column)

    # Add title and labels
    plt.title('Google Trends Over Time for Popular Travel Cities in the UK')
    plt.xlabel('Date')
    plt.ylabel('Interest Over Time')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.xticks(rotation=60)
    plt.grid(True)

    # Show plot
    plt.tight_layout()
    plt.show()



def main():
    try:
        # Get Google Trends data

        df = get_google_trend(gprop='youtube', keywords=KEYWORDS, geo='GB')
        # Drop cities with low values
        df = drop_low_values(df)  
        
        # Save data to a CSV file
        to_csv(df)
        
        # Plot the data
        plot_google_trends(df)
        
    except Exception as e:  
        print(e)

        
    
    
if __name__ == "__main__":
    main()
    