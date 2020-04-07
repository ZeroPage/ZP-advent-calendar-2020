from flask import Flask, g, Response, request
from flask_restful import Resource, Api
from flask_restful import reqparse
import sqlite3
import json
import traceback

app = Flask(__name__)
api = Api(app)

DATABASE = './advent_calendar.sqlite3'
LOG_DATABASE = './log.sqlite3'

def get_db():
    db = gettattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

class CreatePost(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('month', type=int)
            parser.add_argument('day', type=int)
            parser.add_argument('title', type=str)
            parser.add_argument('writer', type=str)
            parser.add_argument('addr', type=str)
            parser.add_argument('text', type=str)
            args = parser.parse_args()


            _month, _day, _title, _writer, _addr, _text\
             = args['month'], args['day'], args['title'], args['writer'], args['addr'], args['text']

            # logging
            with sqlite3.connect(LOG_DATABASE) as logcon:
                cur = logcon.cursor()
                cur.execute("INSERT INTO log (month, day, writer, ip_addr)\
                    VALUES (?,?,?,?)",(_month,_day,_writer, request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
                )

            if (_month==2 and not(_day>=0 and _day<=29)) or (_month==3 and not(_day>=0 and _day<=15)) or ((_month != 2) and (_month !=  3)) or len(_writer) <= 2:
                return {"status":"0", "message":"spam"}

            try:
                with sqlite3.connect(DATABASE) as con:
                    cur = con.cursor()

                    cur.execute("SELECT * FROM post WHERE month=? AND day=?",(_month,_day))
                    res_row = cur.fetchall()
                    print(len(res_row))

                    cur = con.cursor()
                    if len(res_row) != 0:
                        one_writer = ""
                        
                        for row in res_row:
                            one_writer = row[3]
                                
                        if one_writer == _writer:
                            cur.execute("UPDATE post\
                            SET title=?, writer=?, link=?, text=?\
                            WHERE month=? AND day=?",\
                            (_title, _writer, _addr, _text, _month, _day))
                        else:
                            cur.execute("SELECT * FROM post WHERE (month=2 and day >= 22) or (month=3 and day <= 15)")
                            empty_day_str = "" 
                            rows = cur.fetchall()
                            for row in rows:
                                empty_day_str += f'[month: {row[0]} day: {row[1]}, writer: {row[3]}]'
                            
                            response = {'status':'0','message':f'이미 글이 등록된 날짜입니다. 등록된 글의 수정은 동일한 작성자만 할 수 있습니다.','occupied_day_list': f'{empty_day_str}'}
                            json_string = json.dumps(response, ensure_ascii = False)
                            response = Response(json_string, content_type="application/json; charset=utf-8" )
                            # return Response(response, mimetype='text/json;charset=UTF-8')
                            return response
                    else:
                        cur.execute("INSERT INTO post (month, day, title, writer, link, text)\
                            VALUES (?,?,?,?,?,?)", (_month, _day, _title, _writer, _addr, _text))
                    con.commit()
            except Exception as e:
                con.rollback()
                return {'status':'0','error':'[DB ERROR]' + str(e)}
            
            finally:
                con.close()
            
            # Json file
            json_data = None
            feb = open('../nginx_root/20feb/private/calendar.json','r')
            mar = open('../nginx_root/20mar/private/calendar.json','r')
            if _month == 2:
                mar.close()
                json_data = json.load(feb)
            else:
                feb.close()
                json_data = json.load(mar)

            con = sqlite3.connect(DATABASE)
            cur = con.cursor()
            cur.execute("SELECT * FROM post WHERE month=?",(_month,))
            rows = cur.fetchall()
            #Write Json Dict
            for row in rows:
                __day = row[1]
                json_data[str(__day)] = {
                    'title':str(row[2]),
                    'legend': str(row[2]),
                    'text': str(row[5]),
                    'link': str(row[4]),
                    'writer': str(row[3]),
                }

            #Change Just one row
            json_data[str(_day)] = {
                'title':_title,
                'legend':_addr,
                'text': _text,
                'link': _addr,
                'writer': _writer,
            }

            if _month == 2:
                feb = open('../nginx_root/20feb/private/calendar.json','w')
                json.dump(json_data, feb)
                feb.close()
            else:
                mar = open('../nginx_root/20mar/private/calendar.json','w')
                json.dump(json_data, mar)
                mar.close()

            return {'status':'1'}
        except Exception as e:
            traceback.print_exc()
            return {
                'error': str(e) + ' [Post error]',
                'status':'0'
            }

api.add_resource(CreatePost, '/create_post')

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port='5001',
        debug=False,
    )
