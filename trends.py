
from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt
import time

# List of keywords to compare
KEYWORDS = [
    "London",
    "Edinburgh",
    "Manchester",
    "Birmingham",
]

def get_google_trend(keywords=None, 
                     gprop='', 
                     geo='', 
                     timeframe='today 12-m',
                     chunk_size=5, 
                     retries=3, 
                     delay=5
                     ) -> pd.DataFrame:
    if keywords is None:
        keywords = []
    
    def chunker(keywords, chunk_size):
        for pos in range(0, len(keywords), chunk_size):
            yield keywords[pos:pos + chunk_size]
            
    pytrends = TrendReq(hl='en-US', tz=360)
    
    all_data = []
    for chunk in chunker(keywords, chunk_size):
        for attempt in range(retries):
            try:
                pytrends.build_payload(chunk, timeframe=timeframe, gprop=gprop, geo=geo)
                interest_over_time_df = pytrends.interest_over_time()
                if not interest_over_time_df.empty:
                    all_data.append(interest_over_time_df)
                break
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(delay)
        else:
            print(f"Failed to retrieve data for chunk: {chunk}")

    if all_data:
        combined_df = pd.concat(all_data, axis=1)
        # Remove duplicate columns
        combined_df = combined_df.loc[:, ~combined_df.columns.duplicated()]
        # Drop the 'isPartial' column
        combined_df = combined_df.drop(columns=['isPartial'], errors='ignore')
        return combined_df
    else:
        print("No data retrieved")
        return pd.DataFrame()

def to_csv(df, filename='google_trends.csv')-> None:
    try:
        df.to_csv(filename)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(e)

def drop_low_values(df, threshold=20) -> pd.DataFrame: 
    average_values = df.mean()
    filtered_columns = average_values[average_values >= threshold].index
    return df[filtered_columns]

def plot_google_trends(df) -> None:
    average_values = df.mean()
    print(average_values)

    plt.figure(figsize=(14, 8))
    for column in df.columns:
        plt.plot(df.index, df[column], label=column)

    plt.title('Google Trends Over Time for Popular Travel Cities in the UK')
    plt.xlabel('Date')
    plt.ylabel('Interest Over Time')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.xticks(rotation=60)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    try:
        df = get_google_trend(
                keywords=KEYWORDS,
                gprop = 'youtube',
                geo = '',
                timeframe= 'today 12-m',
                )
        if not df.empty:
            df = drop_low_values(df)
            to_csv(df)
            plot_google_trends(df)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()