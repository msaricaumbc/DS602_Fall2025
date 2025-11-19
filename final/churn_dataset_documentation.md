
# Streaming Service Customer Churn Prediction

## Business Context

**StreamFlix** is a popular streaming service that wants to identify customers who are likely to cancel their subscription within the next 30 days. Early identification allows the company to implement targeted retention strategies, such as personalized content recommendations, promotional offers, or customer support outreach, to reduce churn and maintain revenue.

This dataset does NOT include the target variable. The data scientist must analyze the data and ask the subject matter expert if a customer will churn for a limited number of times. 

## Dataset Overview

- **Total Records**: 50,000
- **Features**: 37
- **Target Variable**: NOT INCLUDED

- **Missing Values**: 12500

## Feature Categories

### 1. Subscription Features
- `subscription_start_date`: Date when customer first subscribed
- `subscription_length_days`: Number of days since subscription started
- `subscription_length_months`: Number of months since subscription started
- `subscription_plan`: basic, standard, premium, family, student
- `monthly_price`: Monthly subscription price ($)
- `billing_cycle`: monthly, annual
- `payment_method`: credit_card, debit_card, paypal, apple_pay, google_pay, bank_transfer

### 2. Usage Behavioral Features (Last 30 Days)
- `total_watch_time_hours`: Total hours of content watched
- `sessions_count`: Number of viewing sessions
- `avg_session_duration_minutes`: Average length of viewing sessions
- `days_since_last_watch`: Days since customer last watched content
- `unique_titles_watched`: Number of different titles watched
- `content_completion_rate`: Percentage of started content that was completed
- `abandoned_series_count`: Number of series started but not finished
- `binge_sessions_count`: Number of binge-watching sessions (>3 hours)

### 3. Content Preference Features
- `primary_genre`: Most watched genre (Action, Comedy, Drama, etc.)
- `genres_watched_count`: Number of different genres watched
- `genres_watched`: Comma-separated list of genres watched
- `content_type_preference`: movies, tv_shows, both
- `new_content_ratio`: Ratio of new releases vs catalog content watched

### 4. Device and Platform Features
- `primary_device`: smart_tv, mobile, tablet, desktop, game_console, streaming_device
- `devices_used_count`: Number of different devices used
- `devices_used`: Comma-separated list of devices used
- `primary_os`: Operating system of primary device

### 5. Engagement and Interaction Features
- `has_profile`: Binary flag for profile creation (1) or not (0)
- `number_of_profiles`: Number of user profiles on account
- `watchlist_size`: Number of titles in watchlist
- `ratings_given_count`: Number of content ratings provided
- `reviews_written_count`: Number of reviews written
- `downloads_count`: Number of titles downloaded for offline viewing

### 6. Support and Service Features
- `support_tickets_count`: Number of support tickets opened (last 90 days)
- `support_ticket_reasons`: Comma-separated reasons for support tickets
- `payment_failures_count`: Number of payment failures (last 90 days)
- `account_on_hold`: Binary flag for account suspension (1) or not (0)
- `used_free_trial`: Binary flag if customer used free trial before subscribing

### 7. Temporal Features
- `current_month`: Current month (1-12) for seasonality analysis
- `days_until_next_billing`: Days until next billing date

## Using the Subject Matter Expert (SME)

The SME class allows you to query churn probabilities for specific customer profiles.

### Example Usage:

```python
from streamflix_sme import SME

# Initialize SME
sme = SME()

# Query churn probability
# Pass a dictionary with feature values
churn_prob = sme.ask({
    'subscription_plan': 'basic',
    'days_since_last_watch': 25,
    'total_watch_time_hours': 3,
    'payment_failures_count': 2
})

print(f"Churn probability: {churn_prob}")
```

### Important Notes:
- You can ask up to 500 times (sme has other tasks.)
- Pass feature values as a dictionary
- String values should be passed as strings
- Numeric values should be passed as numbers
- If no matching records found, SME will raise an exception
- The SME returns the mean churn rate (0-1) for matching records
