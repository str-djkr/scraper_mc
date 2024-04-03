import json

from flask import Flask, jsonify

app = Flask(__name__)


with open('menu_data.json', 'r') as f:
    menu_data = json.load(f)


@app.route('/all_products/', methods=['GET'])
def get_all_products():
    return jsonify(menu_data)


@app.route('/products/<product_name>', methods=['GET'])
def get_product_by_name(product_name):
    for product in menu_data:
        if product['name'] == product_name:
            return jsonify(product)
    return jsonify({'message': 'Product not found'}), 404


@app.route('/products/<product_name>/<field>', methods=['GET'])
def get_product_field(product_name, field):
    for product in menu_data:
        if product['name'] == product_name:
            if field in product:
                return jsonify({field: product[field]})
            else:
                return jsonify({'message': 'Field not found'}), 404
    return jsonify({'message': 'Product not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
