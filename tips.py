# # Flask＋Pydantic＋psycopg2 サンプルコードの解説

# 以下の流れでコードを解説します。

# 1. 環境変数によるDB接続設定  
# 2. Pydanticモデルの定義  
# 3. `from_db` メソッドでの型キャスト  
# 4. Flaskルートの処理フロー  
# 5. 動作と応用ポイント  

# ---

# ## 1. 環境変数によるDB接続設定

# アプリ起動時に以下の環境変数を参照し、設定がなければデフォルト値を使います。

# - DB_HOST: ホスト名（デフォルト `localhost`）  
# - DB_PORT: ポート番号（デフォルト `5432`）  
# - DB_NAME: データベース名（デフォルト `testdb`）  
# - DB_USER: ユーザー名（デフォルト `postgres`）  
# - DB_PASS: パスワード（デフォルト `password`）  

# これにより、開発・本番環境で接続先を切り替えやすくなります。

# ---

# ## 2. Pydanticモデルの定義

# ```python
# class ItemModel(BaseModel):
#     id: str
#     name: str
# ```

# - `BaseModel` を継承  
# - レスポンスとして返すフィールドを `id: str`、`name: str` で型宣言  
# - `id` は DB から整数で取得するものの、外部APIでは文字列を返したいため `str` としています

# ---

# ## 3. `from_db` メソッドでの型キャスト

# ```python
# @classmethod
# def from_db(cls, row):
#     return cls(id=str(row[0]), name=row[1])
# ```

# - DB から取得したタプル（例: `(1, 'ペン')`）を受け取るクラスメソッド  
# - `row[0]` の整数を `str()` で文字列に変換  
# - `row[1]` はそのまま文字列として `name` にセット  
# - これにより Pydantic への渡し時点で型をそろえています

# ---

# ## 4. Flaskルートの処理フロー

# ```python
# @app.route('/item/<int:item_id>')
# def get_item(item_id):
#     conn = psycopg2.connect(...)
#     cur = conn.cursor()
#     cur.execute('SELECT id, name FROM items WHERE id = %s', (item_id,))
#     row = cur.fetchone()
#     cur.close(); conn.close()
#     if row:
#         item = ItemModel.from_db(row)
#         return jsonify(item.dict())
#     else:
#         return jsonify({'error': 'Item not found'}), 404
# ```

# - ルートパラメータ `item_id` を整数として受け取る  
# - psycopg2 で手動接続し、クエリ実行  
# - 結果が `None` の場合は 404 レスポンス  
# - 結果がある場合は `ItemModel.from_db` で Pydantic モデル化  
# - `item.dict()` で辞書化したあと `jsonify` で JSON レスポンスに  

# ---

# ## 5. 動作と応用ポイント

# - Pydantic で一貫した型検証が入り、外部仕様を守りやすくなる  
# - 手動接続ではなく Flask-SQLAlchemy へ置き換えると、セッション管理が自動化できる  
# - レスポンスモデルを増やす場合は共通 BaseModel を作成して validator を再利用可能  
# - 環境変数管理は Python の `python-dotenv` や Docker Compose で整備すると運用性が向上  

# このサンプルをベースに、エラーハンドリング強化やミドルウェア導入など、要件に合わせて拡張してみてください。

#-------------------------------------------------------------------------------------------------------------------------


# https://docs.pydantic.dev/latest/examples/custom_validators/#custom-datetime-validator-via-annotated-metadata
