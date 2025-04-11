import pandas as pd
import requests

# Load data from a CSV file
def load_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        print("Data loaded successfully.")
        return data
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None

# Example usage
if __name__ == "__main__":
    file_path = "/Users/chitrang.dave/source/data/kol_engagement.csv"  # Replace with your CSV file path
    data = load_csv(file_path)
    if data is not None:
        print(data.head())  # Display the first few rows of the data
        # Define the API endpoint

        # Iterate through the DataFrame rows
        for index, row in data.iterrows():
            fname = row.get("kol_first_name")  # Replace with the actual column name for 'name'
            lname = row.get("kol_last_name")  # Replace with the actual column name for 'name'
            city = row.get("city")  # Replace with the actual column name for 'city'
            state = row.get("state")  # Replace with the actual column name for 'state'

            if pd.notna(fname) and pd.notna(lname) and pd.notna(city) and pd.notna(state):
                api_url = f"https://npiregistry.cms.hhs.gov/api/?number=&enumeration_type=&taxonomy_description=&name_purpose=&first_name={fname}&use_first_name_alias=&last_name={lname}&organization_name=&address_purpose=&city={city}&state={state}&postal_code=&country_code=&limit=&skip=&pretty=&version=2.1"

            try:
                response = requests.get(api_url)
                if response.status_code == 200:
                    result = response.json()
                    if "results" in result and len(result["results"]) > 0:
                        npi = result["results"][0].get("number", None)  # Extract the 'number' attribute
                        data.at[index, "npi_number"] = npi  # Add the value to a new column in the DataFrame
                    else:
                        data.at[index, "npi_number"] = None  # Set None if no results are found
                    print(f"API call successful for index {index}:") # {response.json()}")
                else:
                    print(f"API call failed for index {index}: {response.status_code}, {response.text}")
            except Exception as e:
                print(f"Error during API call for index {index}: {e}")
        # Save the updated DataFrame to a new CSV file
        output_file_path = "/Users/chitrang.dave/source/data/kol_engagement_with_npi.csv"  # Replace with your desired output file path
        data.to_csv(output_file_path, index=False)
        print(f"Updated data saved to {output_file_path}")
