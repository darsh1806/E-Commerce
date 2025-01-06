from flask import Flask, request, jsonify
import pandas as pd
from apriori_python import apriori


app = Flask(__name__)



data = pd.read_csv('data1.csv', encoding='unicode_escape')  



data_cleaned = data[['Description']].drop_duplicates().dropna()



transactions = data.groupby('InvoiceNo')['Description'].apply(list).tolist()



freq_itemsets, rules = apriori(transactions, minSup=0.05, minConf=0.1)  


indices = pd.Series(data_cleaned.index, index=data_cleaned['Description']).drop_duplicates()


@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        input_product = request.json.get('product')
        
        if not input_product:
            return jsonify({'error': 'Please provide a valid product description.'}), 400

        if input_product not in indices:
            return jsonify({'error': 'Product not found in the dataset.'}), 404

        
        idx = indices[input_product]

        
        recommendations = set()
        for rule in rules:
            if set(rule[0]).issubset([input_product]) and not set(rule[1]).intersection([input_product]):
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







#  {
#     "product": "KNITTED UNION FLAG HOT WATER BOTTLE"
# }
