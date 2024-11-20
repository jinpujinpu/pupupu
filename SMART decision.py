<<<<<<< HEAD
=======
import streamlit as st
>>>>>>> 1b1be73bb92656fe7bf591c4cf391955e3b0ada5
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load dataset
<<<<<<< HEAD
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
=======
@st.cache
def load_data():
    file_path = 'sephora_website_dataset.xlsx'  # Ensure the correct path
    return pd.read_excel(file_path)

sephora_data = load_data()

# Function to filter products by category
def search_products(dataset, category):
    return dataset[dataset['category'].str.contains(category, case=False, na=False)]

# Function to calculate scores dynamically
def calculate_scores_dynamic(filtered_data, weights):
    analysis_columns = ['price', 'rating', 'number_of_reviews', 'love']
    filtered_data = filtered_data.dropna(subset=analysis_columns)
    
    # Normalize the data
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(filtered_data[analysis_columns])
    normalized_df = pd.DataFrame(normalized_data, columns=analysis_columns)
    
    # Invert 'price' since lower price is better
    normalized_df['price'] = 1 - normalized_df['price']
    
    # Calculate dynamic score for each product
    scores = []
    for idx, row in normalized_df.iterrows():
        valid_columns = row.dropna().index
        valid_weights = {col: weights[col] for col in valid_columns}
        
        # Normalize weights to sum to 1
        total_weight = sum(valid_weights.values())
        valid_weights = {col: weight / total_weight for col, weight in valid_weights.items()}
        
        # Calculate score
        score = sum(row[col] * valid_weights[col] for col in valid_columns)
        scores.append(score)
    
    filtered_data['score'] = scores
    return filtered_data.sort_values(by='score', ascending=False)

# Streamlit app interface
st.title("Sephora Smart Assistant")
st.subheader("Search and Compare Products Dynamically")

# Search bar
category = st.text_input("Enter product category (e.g., 'foundation')", 'foundation')
filtered_data = search_products(sephora_data, category)

if not filtered_data.empty:
    st.write(f"Results for '{category}'")

    # Sidebar sliders for attribute weights
    st.sidebar.header("Adjust Weights for Ranking:")
    price_weight = st.sidebar.slider("Price Weight", 0.0, 1.0, 0.2)
    rating_weight = st.sidebar.slider("Rating Weight", 0.0, 1.0, 0.3)
    reviews_weight = st.sidebar.slider("Number of Reviews Weight", 0.0, 1.0, 0.2)
    love_weight = st.sidebar.slider("Love Count Weight", 0.0, 1.0, 0.3)

    # Normalize weights
    total_weight = price_weight + rating_weight + reviews_weight + love_weight
    user_weights = {
        'price': price_weight / total_weight,
        'rating': rating_weight / total_weight,
        'number_of_reviews': reviews_weight / total_weight,
        'love': love_weight / total_weight
    }

    # Calculate scores and rank products
    ranked_products = calculate_scores_dynamic(filtered_data, user_weights)

    # Display ranked products
    st.dataframe(ranked_products[['name', 'brand', 'price', 'rating', 'number_of_reviews', 'love', 'score']])

    # Option to download results
    st.download_button(
        label="Download Ranked Products as CSV",
        data=ranked_products.to_csv(index=False),
        file_name='ranked_products.csv',
        mime='text/csv'
    )
else:
    st.warning(f"No products found for '{category}'. Please try a different category.")
>>>>>>> 1b1be73bb92656fe7bf591c4cf391955e3b0ada5
