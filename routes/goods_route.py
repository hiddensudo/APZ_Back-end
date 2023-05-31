from bson import ObjectId, json_util
from flask import jsonify, request, json
from app import app, mongo


@app.route('/api/goods/get_all', methods=['GET'])
def get_all_goods():
    goods = list(mongo.db.goods.find())
    return jsonify(json.loads(json_util.dumps(goods))), 200


@app.route('/api/goods/add', methods=['POST'])
def add_goods():
    data = request.get_json()
    name = data['name']
    description = data['description']
    price = data['price']

    goods_id = mongo.db.goods.insert_one({
        'name': name,
        'description': description,
        'price': price
    }).inserted_id

    return jsonify({'message': 'Goods add successfully'}), 201


@app.route('/api/goods/update', methods=['PUT'])
def update_goods():
    data = request.get_json()
    goods_id = data['goods_id']
    name = data['name']
    description = data['description']
    price = data['price']

    mongo.db.goods.update_one(
        {'_id': ObjectId(goods_id)},
        {'$set': {
            'name': name,
            'description': description,
            'price': price
        }}
    )

    return jsonify({'message': 'Goods update successfully'}), 200


@app.route('/api/goods/delete', methods=['DELETE'])
def delete_goods():
    data = request.get_json()
    goods_id = data['goods_id']

    mongo.db.goods.delete_one({'_id': ObjectId(goods_id)})

    return jsonify({'message': 'Goods deleted successfully'}), 200
