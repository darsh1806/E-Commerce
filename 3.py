import pandas as pd
from flask import Flask, request, jsonify
from apriori_python import apriori
import warnings


warnings.filterwarnings('ignore')


app = Flask(__name__)


df = pd.read_csv('data1.csv', encoding='unicode_escape')
df.rename(columns={
    "InvoiceNo": "invoice_num",
    "StockCode": "stock_code",
    "Description": "description",
    "Quantity": "quantity",
    "InvoiceDate": "invoice_date",
    "UnitPrice": "unit_price",
    "CustomerID": "customer_id",
    "Country": "country"
}, inplace=True)

df['invoice_date'] = pd.to_datetime(df['invoice_date'], format='%m/%d/%Y %H:%M')
df['description'] = df['description'].str.lower().str.strip()  
df.drop_duplicates(keep='first', inplace=True)
df.dropna(inplace=True)
df = df[df['quantity'] > 0]

transactions = df.groupby('invoice_num')['description'].apply(set).tolist()


min_support = 0.04
min_confidence = 0.01


freq_itemsets, rules = apriori(transactions, minSup=min_support, minConf=min_confidence)


indices = {item.lower().strip(): idx for idx, item in enumerate(df['description'].unique())}


rule_map = {}
for rule in rules:
    for item in rule[0]:  
        if item not in rule_map:
            rule_map[item] = []
        rule_map[item].append(rule)


@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        
        input_product = request.json.get('product')
        
        if not input_product:
            return jsonify({'error': 'Please provide a valid product description.'}), 400

        
        input_product_normalized = input_product.lower().strip()

       
        if input_product_normalized not in indices:
            return jsonify({'error': 'Product not found in the dataset.'}), 404

        
        idx = indices[input_product_normalized]

        
        recommendations = set()

       
        for rule in rules:
            if set(rule[0]).issubset([input_product_normalized]) and not set(rule[1]).intersection([input_product_normalized]):
                recommendations.update(rule[1])

        return jsonify({
            'input_product': input_product,
            'recommendations': list(recommendations)
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'An error occurred while processing your request.',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)














# {
#   "product": "HAND WARMER SCOTTY DOG DESIGN"
# }
