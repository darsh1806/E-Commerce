README for Python File: Apriori-Based Product Recommendation System
Overview
This Python script implements a product recommendation system using the Apriori algorithm. It is built using Flask to provide a REST API endpoint for generating product recommendations based on transactional data.

Dependencies
To run this script, ensure you have the following Python libraries installed:

pandas: For data manipulation and analysis.
flask: For creating the REST API.
apriori_python: For implementing the Apriori algorithm.

You can install these dependencies using pip.

Data Preparation
The script reads a CSV file (data1.csv) containing transactional data. The data is preprocessed as follows:

Column Renaming: Columns are renamed for better readability.
Date Parsing: The invoice_date column is converted to a datetime format.
Text Normalization: Product descriptions are converted to lowercase and stripped of leading/trailing spaces.
Data Cleaning: Duplicates and rows with missing values are removed. Only transactions with a positive quantity are retained.

Apriori Algorithm
The Apriori algorithm is used to generate frequent itemsets and association rules from the transactional data. The parameters used are:

Minimum Support (min_support): 0.04
Minimum Confidence (min_confidence): 0.01

API Endpoint
The script exposes a single REST API endpoint for generating product recommendations:

Endpoint: /recommend
Method: POST
Request Body : {
  "product": "HAND WARMER SCOTTY DOG DESIGN"
}



Error Handling
The API handles the following errors:

400 Bad Request: If the product field is missing in the request body.
404 Not Found: If the product is not found in the dataset.
500 Internal Server Error: If an unexpected error occurs during processing.

Limitations
The dataset must be preprocessed and cleaned before running the script.
The Apriori algorithm's performance may degrade with very large datasets due to its computational complexity.

Future Enhancements
Add support for dynamic adjustment of min_support and min_confidence parameters via API.
Implement caching for frequent itemsets and rules to improve response times.
Add more robust error handling and logging.


