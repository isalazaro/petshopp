from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required
from data import products

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "123"
jwt = JWTManager(app)

@app.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    preco_asc = request.args.get("preco_asc")
    preco_desc = request.args.get("preco_desc")
    description_part = request.args.get("description_part")

    result = products.copy()

    if preco_asc:
        result.sort(key=lambda x: x["product_price"])
    elif preco_desc:
        result.sort(key=lambda x: x["product_price"], reverse=True)
    elif description_part:
        result = [p for p in result if description_part.lower() in p["product_description"].lower()]

    return jsonify(result)


@app.route('/products/<int:product_id>', methods=['GET'])
@token_required
def get_product_by_id(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({"message": "Produto não encontrado"}), 404

if __name__ == '_main_':
    app.run(debug=True)