from flask import Flask, jsonify
from pydantic import BaseModel
import psycopg2
import os

app = Flask(__name__)

# PostgreSQL接続情報（環境変数から取得、なければデフォルト値）
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'testdb')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'password')

# Pydanticモデル
class ItemModel(BaseModel):
    id: str  # int型をstrで受ける
    name: str

    @classmethod
    def from_db(cls, row):
        return cls(id=str(row[0]), name=row[1])

@app.route('/item/<int:item_id>')
def get_item(item_id):
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS
    )
    cur = conn.cursor()
    cur.execute('SELECT id, name FROM items WHERE id = %s', (item_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        item = ItemModel.from_db(row)
        return jsonify(item.dict())
    else:
        return jsonify({'error': 'Item not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
