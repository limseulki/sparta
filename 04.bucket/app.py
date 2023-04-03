from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.er12y5s.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']

    bucket_list = list(db.bucket.find({}, {'_id': False}))
    count = len(bucket_list) + 1
    doc = {
        'num':count,
        'bucket':bucket_receive,
        'done' : 0
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})
    
@app.route("/bucket", methods=["GET"])
def bucket_get():
    all_buckets = list(db.bucket.find({},{'_id':False}))
    return jsonify({'result': all_buckets})

@app.route("/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    bucket_receive = request.form['bucket_give']
    done_receive = request.form['done_give']
    print(num_receive,bucket_receive,done_receive)

    if int(done_receive) == 1:
        return jsonify({'msg': '이미 완료한 버킷리스트!'})
    else :
        doc = {
                'bucket':bucket_receive+" 완료!!",
                'done' : 1
            }
        db.bucket.update_one({'num':int(num_receive)},{'$set':doc})
        return jsonify({'msg': '버킷 완료!'})

# @app.route("/delete", methods=["DELETE"])
# def bucket_delete():
#     num_receive = request.form['num_give']

#     db.bucket.delete_one({'num':int(num_receive)})
#     return jsonify({'msg': '삭제 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)