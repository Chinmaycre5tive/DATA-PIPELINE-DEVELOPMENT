import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from io import BytesIO

# --- ETL Functions ---
def preprocess_transform(df):
    if 'Name' in df.columns:
        df = df.drop(columns=['Name'])

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    categorical_cols = df.select_dtypes(include='object').columns.tolist()

    numeric_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())
    ])

    categorical_pipeline = Pipeline([
        ('encoder', OneHotEncoder(drop='first'))
    ])

    full_pipeline = ColumnTransformer([
        ('num', numeric_pipeline, numeric_cols),
        ('cat', categorical_pipeline, categorical_cols)
    ])

    transformed_data = full_pipeline.fit_transform(df)
    transformed_df = pd.DataFrame(
        transformed_data.toarray() if hasattr(transformed_data, 'toarray') else transformed_data
    )
    return transformed_df

def convert_df_to_csv_download(df):
    return df.to_csv(index=False).encode('utf-8')

# --- Streamlit App ---
st.title("🔁 ETL Pipeline Web App")

uploaded_file = st.file_uploader("📤 Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 Uploaded Data")
    st.dataframe(df)

    if st.button("🚀 Run ETL"):
        processed_df = preprocess_transform(df)
        st.subheader("✅ Transformed Data")
        st.dataframe(processed_df)

        # Download button
        csv_data = convert_df_to_csv_download(processed_df)
        st.download_button("📥 Download Cleaned CSV", csv_data, file_name="cleaned_data.csv", mime="text/csv")
    st.subheader("📈 Salary Distribution (if present)")
    if 'Salary' in df.columns:
        st.bar_chart(df['Salary'].fillna(0))
    