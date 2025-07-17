# etl_pipeline.py

import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

# Step 1: Extract (Load Data)
def extract_data():
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [25, 30, None, 22],
        'Gender': ['F', 'M', 'M', 'M'],
        'Salary': [50000, 60000, 55000, None]
    }
    df = pd.DataFrame(data)
    print("✅ Extracted Data:")
    print(df)
    return df

# Step 2: Preprocess and Transform
def preprocess_transform(df):
    df = df.drop(columns=['Name'])

    numeric_cols = ['Age', 'Salary']
    categorical_cols = ['Gender']

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
    print("\n🔧 Transformed Data:")
    print(transformed_df)
    return transformed_df

# Step 3: Load
def load_data(df, filename='processed_data.csv'):
    df.to_csv(filename, index=False)
    print(f"\n📁 Data saved to '{filename}'")

# Run ETL Process
def run_pipeline():
    df = extract_data()
    transformed_df = preprocess_transform(df)
    load_data(transformed_df)

# Main
if __name__ == "__main__":
    run_pipeline()
