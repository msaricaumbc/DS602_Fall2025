import pandas as pd

class SME:
    """
    Subject Matter Expert (SME) class for querying churn probabilities.
    
    This class simulates a domain expert who can answer questions about
    customer churn probabilities based on feature values.
    
    Usage:
        sme = SME()
        churn_prob = sme.ask({{
            'subscription_plan': 'basic',
            'monthly_price': 9.99,
            'billing_cycle': 'monthly',
            'payment_method': 'credit_card',
            # ...
        }})
    """
    
    def __init__(self):
        """
        Initialize the SME by loading the full dataset.
        """
        self.asked = 0
        self.base_url = 'https://raw.githubusercontent.com/msaricaumbc/DS_data/master/ds602/2025/';
        self.df = self._load_data()
    
    def _load_data(self):
        """
        Load the full dataset for querying.
        
        Returns:
        --------
        pandas.DataFrame
            Full dataset with features
        """
        try:
            X_train = pd.read_csv(self.base_url + 'streaming_churn_dataset.csv')
            y_train = pd.read_csv(self.base_url + 'streaming_churn_dataset_y.csv')
            X_train['will_churn'] = y_train['will_churn']
            return X_train
        except FileNotFoundError:
            raise FileNotFoundError(
                "SME requires streaming_churn_dataset_X.csv and streaming_churn_dataset_y.csv. "
                "Please run the generator first to create these files."
            )
    
    def ask(self, valuedict):
        """
        Query the SME for churn probability given feature values.
        
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
            Mean churn probability (0-1) for matching records
        
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
        
        return float(result['will_churn'].mean())


if __name__ == "__main__":
    sme = SME()
    churn_prob = sme.ask({
        'subscription_plan': 'basic',
        'monthly_price': 9.99,
        'billing_cycle': 'monthly',
        'payment_method': 'credit_card',
        # ...
    })
    print(f"Churn probability: {churn_prob}")