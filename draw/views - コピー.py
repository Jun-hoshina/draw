import tempfile
import os
import io
from flask import request, redirect, url_for, render_template, flash, Blueprint,make_response,jsonify
from numpy import float32
from draw.python.deep_convnet import *
import cv2
import base64
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

game = Blueprint("draw", __name__, template_folder='templates', static_folder="static")

@game.route("/draw", methods=["GET"])
def draw_view():
    # result=request.args.get("result")
    # print(result)
    # iresult=int(result)
    # print(iresult)
    # resp = make_response(render_template("draw.html",iresult=iresult))
    # resp = make_response(render_template("draw.html",iresult=10))

    # resp.headers['X-Something'] = 'A value'
    # print(resp.data)
    # return resp
    # return render_template("draw.html",iresult=iresult)
    return render_template("draw.html")



@game.route("/draw_png", methods=["POST"])
def draw_png():
    if request.method == 'POST':
        enc_data  = request.form['img']
        #dec_data = base64.b64decode( enc_data )              # これではエラー  下記対応↓
        dec_data = base64.b64decode( enc_data.split(',')[1] ) # 環境依存の様(","で区切って本体をdecode)
        dec_img  = Image.open(BytesIO(dec_data))
        
        dec_img = dec_img.resize((28, 28))
        # dec_img.save('image0.png')
        dec_img=np.array(dec_img)
        dec_img=np.array(dec_img[:,:,3])
        # dec_img=dec_img.convert("RGB")
        # dec_img.save('image1.png')
        # dec_img=dec_img.convert("L")
        # print(dec_img.size)
        # dec_img.save('image2.png')
        # dec_img=np.array(dec_img)

        # pil_image=Image.fromarray(dec_img)
        # pil_image.save('image.png')
       
        dec_img.flags.writeable=True
        dec_img=dec_img.reshape((1,1,28,28))


        dec_img=dec_img.astype('float32')/255
        #  maxcol,maxrow=dec_img.shape
        # for i in range(maxrow):
        #     for j in range(maxcol):
        #         if(dec_img[i,j]>50):
        #             dec_img[i,j]=1
        #         else:
        #             dec_img[i,j]=0
        # deca_img = img_to_matrix(dec_img)
        # print(dec_img.shape)
        # dec_img = np.expand_dims(dec_img, axis = 0)
        # dec_img = np.expand_dims(dec_img, axis = 0)

        # print(dec_img.shape)
        # print(dec_img)

        # pn=request.files['image']  #ここの入力がnoneになってる
        # png = request.files['image'].stream
        # png = io.BytesIO(png)
        # form = cgi.FieldStorage()
        # png = form.getvalue("image")
        # png.seek(0)
        # png1 = np.asarray(bytearray(png), dtype=np.uint8) 
        # img=cv2.imdecode(png1,-1)    
        ins=DeepConvNet()
        ins.load_params()
        result=ins.predict(dec_img)
        result=softmax(result)
        print(result)
        if np.max(result)<0.2:
            result=-2
            index=-2
        else:
            index=np.where(result[0] >= 0.2)[0].tolist()
            result=result[np.where(result >= 0.2)]
            # result=np.argmax(result)
           
            # result=int(result)
            result=result.tolist()
        print(index)
        print(result)
       
        return jsonify({'index':index,'result':result})

        # return redirect(url_for("draw.draw_view",result=result))

    # else:
    #     return render_template("draw.html",result=-1)
    

#　あとは結果をhtmlに表示するだけ
#　render_templateがhtmlに値を渡してくれない
#  url_forがうまく機能してない
#　ajaxで変になってる

# withstatsでcentroidとか求めて周りを白くして，文字の大きさによらないようにして精度を上げる

#recog_num.pyはいらない気がする
#result=-1とかいらないな