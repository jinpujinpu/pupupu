import streamlit as st
import pandas as pd
import re

uploaded_file = st.file_uploader("上传xslx文件", type="xlsx")
if uploaded_file is not None:
    data = pd.read_excel(uploaded_file)

# Load your dataset
df = pd.read_excel('sephora_website_dataset.xlsx')

# Your allergy dictionary (use a set for faster lookups)
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

# Search for a product by name
def search_product(product_name):
    product = df[df['name'].str.contains(product_name, case=False, na=False)]
    if product.empty:
        return None
    else:
        return product

# Check for allergens in the product ingredients
def check_allergens(ingredients):
    found_allergens = []
    for allergen in allergens:
        if re.search(rf'\b{re.escape(allergen)}\b', ingredients, re.IGNORECASE):
            found_allergens.append(allergen)
    return found_allergens

# Streamlit App
def main():
    st.title("Sephora Product Allergy Checker")

    # User input: product name search
    product_name = st.text_input("Enter the product name to search for:", "")

    if product_name:
        product = search_product(product_name)

        if product is not None:
            st.write(f"**Product Name:** {product.iloc[0]['name']}")
            st.write(f"**Ingredients:** {product.iloc[0]['ingredients']}")

            ingredients = product.iloc[0]['ingredients']
            found_allergens = check_allergens(ingredients)

            if found_allergens:
                st.warning(f"Warning! The following allergens were found: {', '.join(found_allergens)}")
            else:
                st.success("No known allergens found in this product.")
        else:
            st.error(f"Product '{product_name}' not found.")

if __name__ == "__main__":
    main()

     