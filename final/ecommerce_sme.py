import pandas as pd

class SME:
    """
    Subject Matter Expert (SME) class for querying purchase probabilities.
    
    This class simulates a domain expert who can answer questions about
    customer purchase probabilities based on feature values.
    
    Usage:
        sme = SME()
        purchase_prob = sme.ask({
            'session_start_time': '2024-08-21 13:28:14', 
            'hour': 13, 
            'day_of_week': 2, 
            'month': 8, 
            'is_weekend': 0, 
            # ...
        })
    """
    
    def __init__(self):
        """
        Initialize the SME by loading the full dataset.
        """
        self.asked = 0
        self.base_url = 'https://raw.githubusercontent.com/msaricaumbc/DS_data/master/ds602/2025/'
        self.df = self._load_data()
    
    def _load_data(self):
        """
        Load the full dataset for querying.
        
        Returns:
        --------
        pandas.DataFrame
            Full dataset with features and target
        """
        try:
            X_train = pd.read_csv(self.base_url + 'ecommerce_sessions_X.csv')
            y_train = pd.read_csv(self.base_url + 'ecommerce_sessions_y.csv')
            X_train['will_purchase'] = y_train['will_purchase']
            return X_train
        except FileNotFoundError:
            raise FileNotFoundError(
                "SME requires ecommerce_sessions_X.csv and ecommerce_sessions_y.csv. "
                "Please run the generator first to create these files."
            )
    
    def ask(self, valuedict):
        """
        Query the SME for purchase probability given feature values.
        
        Parameters:
        -----------
        valuedict : dict
            Dictionary of feature names and values to query.
            String values should be passed as strings.
            Numeric values should be passed as numbers.
            None values are ignored.
        
        Returns:
        --------
        float
            Mean purchase probability (0-1) for matching records
        
        Raises:
        -------
        Exception
            If query limit exceeded or no matching records found
        """
        self.asked += 1
        
        if self.asked > 500:
            raise Exception("Sorry, you have asked enough (500 query limit)")
        
        arr = []
        for prop in valuedict:
            val = valuedict[prop]
            if val is None:
                continue
            
            # Format value for query
            if isinstance(val, str):
                val = f"'{val}'"
            
            arr.append(f'{prop} == {val}')

        print("Query parameters:", arr)
        
        if not arr:
            raise Exception("No valid query parameters provided")
        
        query = ' and '.join(arr)
        
        try:
            result = self.df.query(query)
        except Exception as e:
            raise Exception(f"Query error: {str(e)}")
        
        if len(result) == 0:
            raise Exception("I don't know (no matching records found)")
        
        return float(result['will_purchase'].mean())


if __name__ == "__main__":
    sme = SME()
    purchase_prob = sme.ask({
        'session_start_time': '2024-08-21 13:28:14', 
        'hour': 13, 
        'day_of_week': 2, 
        'month': 8, 
        'is_weekend': 0, 
        'session_duration_minutes': 17.32306284931649, 
        'days_since_last_visit': 3.0440417800824724, 
        'page_views': 6.132344927823966, 
        'clicks': 2.0696937867669893, 
        'avg_scroll_depth': 0.2616319121119533, 
        'items_added_to_cart': 2, 
        'items_removed_from_cart': 1, 
        'search_queries_count': 0, 
        'product_page_time_minutes': 2.9052534476815746, 
        'categories_viewed_count': 3, 
        'avg_price_viewed': 29.511092255927167, 
        'device_type': 'mobile', 
        'traffic_source': 'social_media', 
        'customer_segment': 'returning_customer', 
        'region': 'Middle_East_Africa',
        'browser': 'Chrome',
        'operating_system': 'Windows',
        'user_type': 'returning_user',
        'search_queries': None,
        'categories_viewed': 'Jewelry, Sports & Outdoors, Electronics',
        'user_agent': 'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
        'will_purchase': 0
    })
    print(f"Purchase probability: {purchase_prob}")

