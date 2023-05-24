# 必要なモジュールのインポート
from flask import Flask, render_template
from flask import redirect, url_for
from flask import request
from datetime import datetime, timedelta
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
def get_results(interval):
    # MySQLサーバに接続する
    connection = pymysql.connect(host=hostname, port=port, user=username, password=password, database=database, ssl={'ca': ssl_ca})
    
    # テーブルからデータを取得する
    with connection.cursor() as cursor:
        if interval == 'day':
            # 現在の日付と時刻を取得
            current_datetime = datetime.now()
            # 終了時刻を現在の日付と時刻に設定
            end_datetime = current_datetime.replace(minute=0, second=0, microsecond=0)
            # 開始時刻を終了時刻から1日前に設定（1日前から現在までのデータを取得するため）
            start_datetime = end_datetime - timedelta(hours=24)
            # 1時間ごとのデータを取得するためのクエリ作成
           # sql = "SELECT * FROM datatable WHERE DATE_FORMAT(time, '%%Y-%%m-%%d %%H:00:00') BETWEEN %s AND %s"
            sql = "SELECT * FROM datatable WHERE time BETWEEN %s AND %s AND MINUTE(time) = 0 ORDER BY time ASC"
            


            #クエリの実行
            cursor.execute(sql, (start_datetime, end_datetime))
            
       # elif interval == 'week':
            #sql = 'SELECT * FROM datatable WHERE DATE(time) BETWEEN CURDATE() - INTERVAL 7 DAY AND CURDATE()'
        #else:
           # sql = 'SELECT * FROM datatable'

        elif interval == 'week':
            sql = 'SELECT * FROM datatable WHERE DATE(time) BETWEEN CURDATE() - INTERVAL 7 DAY AND CURDATE() ORDER BY time ASC'
            # クエリの実行
            cursor.execute(sql)
        else:
            sql = 'SELECT * FROM datatable ORDER BY time ASC'

            #クエリの実行
            cursor.execute(sql)
        # 取り出したものを1件ずつ表示させるfetchall()
        results = cursor.fetchall()
        results = [(int(row[0]), row[1], float(row[2]), float(row[3])) for row in results]
    return results



# ルートディレクトリへのアクセス時の処理

@app.route('/', methods=['GET'])
def index():
    interval = request.args.get('interval', '')
    
    if interval == 'day':
        results = get_results('day')
    elif interval == 'week':
        results = get_results('week')
    else:
        results = get_results('')
    
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

