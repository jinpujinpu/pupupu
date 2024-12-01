from pip._internal import main
main(['install', 'openpyxl'])

import streamlit as st
import pandas as pd
import re

# Upload functionality
uploaded_file = st.file_uploader("Upload your Excel file containing product data:", type="xlsx")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

# Define your allergen dictionary
allergens = {
    "Phenoxyethanol", "avocados", "bananas", "latex", "vitamin e", "tocopherol", "tocopherol acetate",
    "almonds", "Carmine", "fragrance", "Sulphur", "lactic acid", "coconut", "palm", "tree nuts", "peanuts",
    "Linalool", "Hydroperoxides", "Latex", "Natural Rubber Latex", "Rubber Latex", "Amyl cinnamal",
    "Amylcinnamyl alcohol", "Anisyl alcohol", "Benzyl alcohol", "Benzyl benzoate", "Benzyl cinnamate",
    "Benzyl salicylate", "Cinnamyl alcohol", "Cinnamaldehyde", "Citral", "Citronellol", "Coumarin",
    "Eugenol", "Farnesol", "Geraniol", "Hexyl cinnamaladehyde", "Hydroxycitronellal", "Lyral",
    "Isoeugenol", "Lilial", "Limonene", "Methyl 2-octynoate", "Methylionone", "Oak moss extract",
    "Tree moss extract", "Methylparaben", "Ethylparaben", "Propylparaben", "Butylparaben"
}

# Function to search for a product by name
def search_product(product_name):
    product = df[df['name'].str.contains(product_name, case=False, na=False)]
    if product.empty:
        return None
    else:
        return product

# Function to check for allergens in product ingredients
def check_allergens(ingredients):
    found_allergens = []
    for allergen in allergens:
        if re.search(rf'\b{re.escape(allergen)}\b', ingredients, re.IGNORECASE):
            found_allergens.append(allergen)
    return found_allergens

# Streamlit app logic
def main():
    st.title("Sephora Product Allergy Checker")

    # User input: product name
    product_name = st.text_input("Enter the product name to search for:", "")

    if uploaded_file is not None and product_name:
        product = search_product(product_name)

        if product is not None:
            st.write(f"**Product Name:** {product.iloc[0]['name']}")

            # Check for allergens
            ingredients = product.iloc[0]['ingredients']
            found_allergens = check_allergens(ingredients)

            if found_allergens:
                st.warning(f"Warning! The following allergens were found: {', '.join(found_allergens)}")
            else:
                st.success("No known allergens found in this product.")
        else:
            st.error(f"Product '{product_name}' not found. Please check the name and try again.")

if __name__ == "__main__":
    main()
