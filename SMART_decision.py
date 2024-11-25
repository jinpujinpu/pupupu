import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# Load dataset
@st.cache
def load_data(file_path):
    return pd.read_excel(file_path)

# Function to filter products by category
def search_products(dataset, category):
    """
    Filter products by category or keyword.
    """
    return dataset[dataset['category'].str.contains(category, case=False, na=False)]

# Function to calculate scores dynamically
def calculate_scores_dynamic(filtered_data, weights):
    """
    Calculate scores dynamically based on user-defined weights.
    """
    analysis_columns = ['price', 'rating', 'number_of_reviews', 'love']
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(filtered_data[analysis_columns])
    normalized_df = pd.DataFrame(normalized_data, columns=analysis_columns)

    # Invert 'price' since lower price is better
    normalized_df['price'] = 1 - normalized_df['price']

    # Calculate score for each product
    scores = []
    for idx, row in normalized_df.iterrows():
        valid_columns = row.dropna().index
        valid_weights = {col: weights[col] for col in valid_columns}
        total_weight = sum(valid_weights.values())
        valid_weights = {col: weight / total_weight for col, weight in valid_weights.items()}
        score = sum(row[col] * valid_weights[col] for col in valid_columns)
        scores.append(score)

    filtered_data['score'] = scores
    return filtered_data.sort_values(by='score', ascending=False)

# Load the dataset
file_path = 'sephora_website_dataset.xlsx'  # Replace with your dataset path
sephora_data = load_data(file_path)

# Streamlit Interface
st.title("Best-Fit Decision Scale")
st.write("This tool helps you find the best products tailored to your preferences.")

# Step 1: Input Category
category = st.text_input("Enter the product category you are looking for (e.g., 'foundation'):")

if category:
    filtered_data = search_products(sephora_data, category)

    if filtered_data.empty:
        st.warning(f"No products found for category: {category}")
    else:
        # Step 2: Personalized Scale for Features
        st.sidebar.header("Set Feature Importance")
        st.sidebar.write("Adjust the sliders to indicate how important each feature is to you.")

        # Sliders for weights
        weights = {
            'price': st.sidebar.slider("Weight for Price", 0.0, 1.0, 0.3, step=0.1),
            'rating': st.sidebar.slider("Weight for Rating", 0.0, 1.0, 0.4, step=0.1),
            'number_of_reviews': st.sidebar.slider("Weight for Popularity", 0.0, 1.0, 0.2, step=0.1),
            'love': st.sidebar.slider("Weight for Favorites Count", 0.0, 1.0, 0.1, step=0.1),
        }

        # Normalize weights to sum to 1
        total_weight = sum(weights.values())
        normalized_weights = {k: v / total_weight for k, v in weights.items()}

        # Step 3: Visualize Weights with Updated Names
        st.subheader("Your Personalized Feature Importance")
        fig, ax = plt.subplots()
        renamed_columns = {
            'price': 'Price',
            'rating': 'Rating',
            'number_of_reviews': 'Popularity',
            'love': 'Favorites Count'
        }
        ax.bar([renamed_columns[col] for col in normalized_weights.keys()], normalized_weights.values())
        ax.set_ylabel("Normalized Weight")
        ax.set_title("Feature Importance")
        st.pyplot(fig)

        # Step 4: Calculate and Display Results
        st.subheader(f"Top Products for: {category}")
        ranked_products = calculate_scores_dynamic(filtered_data, normalized_weights)

        # Rename columns for display
        display_columns = {
            'name': 'Product Name',
            'brand': 'Brand',
            'price': 'Price',
            'rating': 'Rating',
            'number_of_reviews': 'Popularity',
            'love': 'Favorites Count',
            'score': 'Final Score'
        }
        st.dataframe(ranked_products.rename(columns=display_columns))

        # Optional: Save Results
        if st.button("Download Results"):
            ranked_products.to_excel('Ranked_Products_Dynamic.xlsx', index=False)
            st.success("Results saved to 'Ranked_Products_Dynamic.xlsx'")
else:
    st.info("Please enter a category to start!")
