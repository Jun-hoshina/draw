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

np.set_printoptions(threshold=np.inf)

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
        result_list=[]
        index_list=[]
        enc_data  = request.form['img']
        #dec_data = base64.b64decode( enc_data )              # これではエラー  下記対応↓
        dec_data = base64.b64decode( enc_data.split(',')[1] ) # 環境依存の様(","で区切って本体をdecode)
        dec_img  = Image.open(BytesIO(dec_data))

        margin=int(400*0.5*1.2)
        dec_img = cv2.copyMakeBorder(np.array(dec_img), margin, margin, margin, margin, cv2.BORDER_CONSTANT, (0,0,0))
        #パディングすることによって端に描かれた数字も認識できるようにする
        
        im = dec_img.astype(np.uint8)
        im = Image.fromarray(im)
        im.save("image3.png")
        #なんかこの画像が他の画像と違うからちょっと気に入らないんだが

        nlabels, labels, stats, centroids=cv2.connectedComponentsWithStats(np.array(dec_img)[:,:,3])
        #cv2.connectedComponentsWithStatsで二桁以上の数も認識できるようにする

        print(centroids)
        print(stats[:,2:4])
        print(sorted(enumerate(centroids[1:,0]), key=lambda x:x[1]))
        if nlabels>=2:
            # for i in range(1,nlabels):
            for i in (j[0]+1 for j in sorted(enumerate(centroids[1:,0]), key=lambda x:x[1])):
                #centroidsの横軸の大きさの順にrange(1,nlabels)を並べる
                #centroids[1:]で背景の重心にマスクして，j[0]+1とすることでマスクをした分の補完をする

                figure=np.where(labels==i,255,0)  
                #置換もできるので条件を満たすもの以外0にする

                #np.uint8に変換しないと真っ黒なpngが出てくる
                im = figure.astype(np.uint8)
                im = Image.fromarray(im)
                im.save("image.png")

                # figure=np.nonzero(labels)
                # max=np.max(stats[i:,2],stats[i:,3])
                # max=stats[i,3]
                
                max=stats[i,3] if stats[i,3]>stats[i,2] else stats[i,2]
                #stats[i,2]とstas[i,3]の大きい方を取る

                dist=(max/2)*1.2
                left=int(centroids[i,0]-dist)
                right=int(centroids[i,0]+dist)
                bottom=int(centroids[i,1]-dist)
                up=int(centroids[i,1]+dist)
                #重心を中心として，高さ，幅の大きい方を一辺とした正方形を作る

                #枠からはみ出してはいけないので，比較する必要がある
                # left=int(centroids[i,0]-dist) if int(centroids[i,0]-dist) > 0 else 0
                # right=int(centroids[i,0]+dist) if int(centroids[i,0]+dist) < 400 else 400
                # bottom=int(centroids[i,1]-dist) if int(centroids[i,1]-dist) > 0 else 0
                # up=int(centroids[i,1]+dist) if int(centroids[i,1]+dist) > 400  else 400
                #この方法だと精度が良くなかった
                dec_img=figure[bottom:up,left:right]

                im = dec_img.astype(np.uint8)
                im = Image.fromarray(im)
                im.save("image1.png")

                # dec_img=np.resize(dec_img,(28,28))
                # dec_img = dec_img.resize(28, 28)
                # dec_img=dec_img.resize(28,28)

                im = dec_img.astype(np.uint8)
                im = Image.fromarray(im)
                im=im.resize((28,28))
                im.save("image0.png")
                # dec_sa.save('image0.png')

                # dec_img=np.array(dec_img)
                # dec_img=np.array(dec_img[:,:,3])

                # dec_img=dec_img.convert("RGB")
                # dec_img.save('image1.png')
                # dec_img=dec_img.convert("L")
                # print(dec_img.size)
                # dec_img.save('image2.png')
                # dec_img=np.array(dec_img)

                # pil_image=Image.fromarray(dec_img)
                # pil_image.save('image.png')
            
                dec_img=np.array(im)
                # dec_img.flags.writeable=True
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
                if np.max(result)<0.3:
                    result=[-2]
                    index=[-2]
                else:
                    index=np.where(result[0] >= 0.2)[0].tolist()
                    result=result[np.where(result >= 0.2)]
                    # result=np.argmax(result)
                
                    # result=int(result)
                    result=result.tolist()
                print(index)
                print(result)
                index_list.append(index)
                result_list.append(result)
        else:
            index=[-2]
            result=[-2]
            index_list.append(index)
            result_list.append(result)
       
        #indexには[2,[1,7],8]のようなlistが入っている
        return jsonify({'index':index_list,'result':result_list})

        # return redirect(url_for("draw.draw_view",result=result))

    # else:
    #     return render_template("draw.html",result=-1)
    

#　あとは結果をhtmlに表示するだけ
#　render_templateがhtmlに値を渡してくれない
#  url_forがうまく機能してない
#　ajaxで変になってる

# withstatsでcentroidとか求めて周りを白くして，文字の大きさによらないようにして精度を上げる

#カンマなしで表示できるようにする
#候補の数は分かりやすいように表示する
#二桁の数字を描いたときの数字の並べ方
#どうやら，二桁の数字ではより上に描いた数字が先頭になるらしい

#cv2とPILを統一して使った方がいい気がする

#recog_num.pyはいらない気がする
#result=-1とかいらないな