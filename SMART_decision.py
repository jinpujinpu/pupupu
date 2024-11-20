import pandas as pd
from scikit-learn.preprocessing import MinMaxScaler

# Load dataset
file_path = 'sephora_website_dataset.xlsx'
sephora_data = pd.read_excel(file_path)

# Function to filter products by category
def search_products(dataset, category):
    """
    Filter products by category or keyword.

    Args:
    dataset (pd.DataFrame): The full dataset of products.
    category (str): The category or keyword to filter by.

    Returns:
    pd.DataFrame: Filtered dataset of similar products.
    """
    return dataset[dataset['category'].str.contains(category, case=False, na=False)]

# Function to calculate scores dynamically, skipping missing values
def calculate_scores_dynamic(filtered_data, weights):
    """
    Calculate scores dynamically, skipping missing values for each product.

    Args:
    filtered_data (pd.DataFrame): Filtered dataset.
    weights (dict): Initial weights for price, rating, number_of_reviews, and love.

    Returns:
    pd.DataFrame: DataFrame with calculated scores.
    """
    analysis_columns = ['price', 'rating', 'number_of_reviews', 'love']

    # Normalize the data for all products
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(filtered_data[analysis_columns])
    normalized_df = pd.DataFrame(normalized_data, columns=analysis_columns)

    # Invert 'price' since lower price is better
    normalized_df['price'] = 1 - normalized_df['price']

    # Calculate score dynamically for each row
    scores = []
    for idx, row in normalized_df.iterrows():
        valid_columns = row.dropna().index  # Columns without missing values
        valid_weights = {col: weights[col] for col in valid_columns}

        # Normalize weights to sum to 1
        total_weight = sum(valid_weights.values())
        valid_weights = {col: weight / total_weight for col, weight in valid_weights.items()}

        # Calculate score for the product
        score = sum(row[col] * valid_weights[col] for col in valid_columns)
        scores.append(score)

    # Add scores to the original DataFrame
    filtered_data['score'] = scores
    return filtered_data.sort_values(by='score', ascending=False)

# User-defined weights
user_weights = {
    'price': 0.3,
    'rating': 0.4,
    'number_of_reviews': 0.1,
    'love': 0.2
}

# Example usage
category = 'foundation'  # Example category
filtered_data = search_products(sephora_data, category)
ranked_products = calculate_scores_dynamic(filtered_data, user_weights)

# Display the top-ranked products
print(ranked_products[['name', 'brand', 'price', 'rating', 'number_of_reviews', 'love', 'score']].head())

# Optional: Save the results
ranked_products.to_excel('Ranked_Products_Dynamic.xlsx', index=False)
