# 必要なモジュールのインポート
from flask import Flask, render_template
from flask import redirect, url_for
import pymysql

# Flaskアプリケーションの設定
app = Flask(__name__)

# MySQLサーバへの接続情報を設定する
hostname = 'solution-db.mysql.database.azure.com'
port = 3306
username = 'ono'
password = 'Solution123'
database = 'solution-test'
ssl_ca = 'C://Users//yudai//gitwork1//DigiCertGlobalRootCA.crt.pem'

# index関数とother関数どちらもresults変数が使用できるMySQLからデータを取得する共通の関数
def get_results():
    # MySQLサーバに接続する
    connection = pymysql.connect(host=hostname, port=port, user=username, password=password, database=database, ssl={'ca': ssl_ca})
    
    # テーブルからデータを取得する
    with connection.cursor() as cursor:
        sql = 'SELECT * FROM datatable'
        cursor.execute(sql)
        # 取り出したものを1件ずつ表示させるfetchall()
        results = cursor.fetchall()
        results = [(int(row[0]), row[1], float(row[2]), float(row[3])) for row in results]
    return results

# ルートディレクトリへのアクセス時の処理
@app.route('/')
def index():
    results = get_results()
    print(results)
    
    # テンプレートを使用してHTMLをレンダリングする
    return render_template('index.html', results=results)
    

# 他のページに移動する
@app.route('/other')
def other():
    results = get_results()
    return render_template('other.html', results=results)

@app.route('/redirect')
def redirect_to_other():
    return redirect(url_for('other'))
    
if __name__ == '__main__':
    app.run(debug=True)
