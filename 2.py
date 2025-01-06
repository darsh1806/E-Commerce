
from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


app = Flask(__name__)


data = pd.read_csv('data.csv')  


data_cleaned = data[['Description']].drop_duplicates().dropna()


tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(data_cleaned['Description'])


cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

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

        
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:11]

       
        product_indices = [i[0] for i in sim_scores]
        recommendations = data_cleaned['Description'].iloc[product_indices].tolist()

        return jsonify({
            'input_product': input_product,
            'recommendations': recommendations
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'An error occurred while processing your request.',
            'details': str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True)
