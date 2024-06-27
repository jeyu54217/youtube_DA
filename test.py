from pytrends.request import TrendReq
import pandas as pd

# Connect to Google
pytrends = TrendReq(hl='en-US', tz=360)

# Define the keywords list
kw_list = ["Python", "Java", "C++"]

# Build the payload
pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')

# Interest over time
interest_over_time_df = pytrends.interest_over_time()
print(interest_over_time_df.head())

# Interest by region
interest_by_region_df = pytrends.interest_by_region(resolution='COUNTRY')
print(interest_by_region_df.head())

# Related queries
related_queries_dict = pytrends.related_queries()
print(related_queries_dict)

# Trending searches in real time
trending_searches_df = pytrends.trending_searches(pn='united_states')
print(trending_searches_df.head())

# Top charts
top_charts_df = pytrends.top_charts(2023, hl='en-US', tz=300, geo='GLOBAL')
print(top_charts_df.head())

# Suggestions for a keyword
suggestions_dict = pytrends.suggestions(keyword='Python')
print(suggestions_dict)
