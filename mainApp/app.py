# from flask_cors import CORS
from flask import jsonify,request
from flask_mail import Message
from flask_cors import CORS

import until
from __init__ import * 

# cors=CORS(app,resources = {r'/api/*':{'origins':'https://shopdb.netlify.app'}})
cors=CORS(app,resources = {r'*':{'origins':'*'}})

# CORS(app)
# ============================== send email ===========================
@app.route("/send",methods = ['POST'])
def Send_Email():
    if request.method == 'POST':
        data =request.json
        email = data.get('email')
        name = data.get('name')
        adress = data.get('adress')
        datas = data.get('datas')
        phone = data.get('phone')
        price =data.get('price')
        msg = Message("Hóa Đơn",sender="shop",recipients=[email])
        s = ''
        for c in datas:
            s=s+ """
                <tr>
                    <td style ="border:1px solid black">{}</td>
                    <td style ="border:1px solid black">
                    <img style ="object-fit:cover;" src={} alt="..." width="100" height="100">
                    </td>
                    <td style ="border:1px solid black">{}</td>
                    <td style ="border:1px solid black">{}</td>
                </tr>
            """.format(c['name'],c['image'],c['qly'],int(c['priceDown']) * int(c['qly']) )


        msg.html = """
                        <h3 style="color:green">Kính chào quí khách:{} </h3>
                        <p style="color:black">Email:{} </p>
                        <p style="color:black">Phone:{} </p>
                        <p style="color:black">Địa chỉ:{} </p>
                        <p style="color:black">Tổng tiền:{} </p>
                        <table style ="border:1px solid black">
                            <tr style ="background-color: #dddddd">
                                <th style ="border:1px solid black">Tên sản phẩm</th>
                                <th style ="border:1px solid black">image</th>
                                <th style ="border:1px solid black">Số lượng</th>
                                <th style ="border:1px solid black">Số tiền</th>
                            </tr>
                            {}
                            </table>
        """.format(name,email,phone,adress,price,s)
        mail.send(msg)
        return jsonify({'data':200 ,'datas':datas})


# ========================= post list image =================
@app.route("/api/list-image",methods = ['POST'])
def Post_listImage():
    data = request.json
    product_id = data.get('product_id')
    image = data.get('image')
    color =data.get('color')
    if request.method == 'POST':
        try:
            until.post_listImageProduct(product_id=product_id,image=image,color=color)
        except Exception as e :
            return jsonify({'error':str(e)})
        return jsonify({'code':200})
   

# ========================= put list image =================
@app.route("/api/list-image",methods = ['PUT'])
def Put_listImage():
    data = request.json
    image_id = data.get('image_id')
    image = data.get('image')
    color =data.get('color')
    if request.method == 'PUT':
        try:
            until.put_listImageProduct(image_id=image_id,image=image,color=color)
        except:
            return jsonify({'code':400})
        return jsonify({'code':200})

# ======================== product ======================
@app.route("/api/products",methods = ['GET'])
def Products_all():
    kw = request.args.get('keywork')
    caterogy_id=request.args.get('caterogy_id')
    page = request.args.get('page',1)
    pro=until.read_product(kw=kw,caterogy_id=caterogy_id,page=int(page))
    return jsonify({'data':pro})


# ========================= product by id =================
@app.route("/api/products/<int:product_id>",methods = ['GET'])
def Products_by_id(product_id):
    pro=until.read_product_by_id(product_id)
    return jsonify({'data':pro})

# ======================== post product ======================
@app.route("/api/products",methods = ['POST'])
def Post_product():
    if request.method == 'POST':
        data = request.json
        name=data.get('name')
        description =data.get('description')
        sale =data.get('sale')
        priceUp = data.get('priceUp')
        priceDown =data.get('priceDown')
        color=data.get('color')
        ram=data.get('ram')
        rom=data.get('rom')
        screen=data.get('screen')
        image =data.get('image')
        card=data.get('card')
        category_id=data.get('category_id')
        try:
            until.post_product(name=name,description=description,sale=sale,
                               priceUp=priceUp,priceDown=priceDown,color=color,
                               ram=ram,rom=rom,screen=screen,image=image,card=card,category_id=category_id)
        except:
            return jsonify({'code':400})
        return jsonify({'code':200})


# ======================== delete product ======================
@app.route("/api/products/<int:product_id>",methods = ['DELETE'])
def Delete_product(product_id):
    if request.method == 'DELETE':
        try:
            until.delete_product(product_id=product_id)
        except:
            return jsonify({'code':400})
        return jsonify({'code':200})

# ======================== put product ======================
@app.route("/api/products/<int:product_id>",methods = ['PUT'])
def PUT_product(product_id):
    if request.method == 'PUT':
        data = request.json
        name = data.get('name')
        description=data.get('description')
        sale=data.get('sale')
        priceUp=data.get('priceUp')
        priceDown=data.get('priceDown')
        color=data.get('color')
        ram=data.get('ram')
        rom=data.get('rom')
        screen=data.get('screen')
        image=data.get('image')
        card=data.get('card')
        category_id=data.get('category_id')
        try:
            until.put_product(product_id=product_id,name=name,description=description,sale=sale,priceUp=priceUp,priceDown=priceDown,
                            color=color,ram=ram,rom=rom,screen=screen,image=image,card=card,category_id=category_id)
        except:
            return jsonify({'code':400})
        return jsonify({'code':200})


# ============================ caterogy ========================
@app.route("/api/caterogy",methods = ['GET'])
def Caterogy_all():
    vaterogy=until.read_category()
    return jsonify({'data':vaterogy})



# ============================ post caterogy ========================
@app.route("/api/caterogy",methods = ['GET','POST'])
def Post_caterogy():
    if request.method =='POST':
        data =request.json
        name = data.get('name')
        until.post_category(name=name)
        vaterogy=until.read_category()
    return jsonify({'code':200,'data':vaterogy})

# ============================ delete caterogy ========================
@app.route("/api/caterogy/<int:id>",methods = ['DELETE'])
def Delete_caterogy(id):
    if request.method =='DELETE':
        until.delete_category(id=id)
        vaterogy=until.read_category()
    return jsonify({'code':200,'data':vaterogy})
# ============================ put caterogy ========================
@app.route("/api/caterogy/<name>",methods = ['PUT'])
def Put_caterogy(name):
    if request.method =='PUT':
        data = request.json
        newName = data.get('name')
        until.put_category(name=name,newName=newName)
        vaterogy=until.read_category()
    return jsonify({'code':200,'data':vaterogy})

# ============================ read banner ========================
@app.route("/api/banner",methods = ['GET'])
def Banner_all():
    banner=until.read_banner()
    return jsonify({'data':banner})

# ============================ post banner ========================
@app.route("/api/banner",methods = ['GET','POST'])
def Post_one():
    if request.method == 'POST':
        try:
            data = request.json
            img = data.get('image')
            until.post_banner(img=img)
        except:
            return jsonify({'code':400})
    return jsonify({'code':200})

# ============================ delete banner ========================
@app.route("/api/banner/<int:id>",methods = ['DELETE'])
def Delete_one(id):
    if request.method == 'DELETE':
        try:
            until.delete_banner(id=id)
        except:
            return jsonify({'code':400})
    return jsonify({'code':200})

# ============================ put banner ========================
@app.route("/api/banner/<int:id>",methods = ['PUT'])
def Put_one(id):
    if request.method == 'PUT':
        data = request.json
        img = data.get('image')
        try:
            until.put_banner(id=id,img=img)
        except:
            return jsonify({'code':400})
    return jsonify({'code':200})



# ===================================== read user ===========================
@app.route("/api/user",methods = ['GET'])
def User_all():
    user=until.read_user()
    return jsonify({'data':user})



# =============================== login =========================
@app.route("/user",methods = ['GET'])
def Check_user():
    name = request.args.get('name')
    password = request.args.get('password')
    user = until.check_login(name=name,password=password)
    if user==None:
        return jsonify({'user':False})
    elif user.user_role == UserRole.USER:
        return jsonify({'user':True,'id':user.id,'name':user.username,'avatar':user.avatar})
    else:
        return jsonify({'Admin':True,'id':user.id,'name':user.username,'avatar':user.avatar})

        

# ================================== register =====================

@app.route('/register',methods =['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.args.get('name')
        password = request.args.get('password')
        email =request.args.get('email')
        checkUser = until.read_user_by_name(name=name)
        checkEmail =until.read_user_by_email(email=email)
        if checkUser or checkEmail:
            return jsonify(False)
        else:
            user_regis = until.add_user(name=name,password=password,email=email)
            return jsonify({'status':True,'id':user_regis.id,'name':user_regis.username,'avatar':user_regis.avatar})




# ========================================= app coment ============================
@app.route('/api/comment',methods = ['GET','POST'])
def add_comment():
    if request.method == 'POST':
        data = request.json
        user_id = data.get('user_id')
        product_id  = data.get('product_id')
        content = data.get('content')
        try:
            comment = until.add_comment(user_id=user_id,product_id=product_id,content=content)
        except:
            return jsonify({'code':400})
        return jsonify({'code':200,'comment':{
            'content':comment.content,
            'create_time':comment.create_time
        }})

# ======================================= dọc commen theo product id ============================
@app.route('/api/comment/<int:product_id>',methods = ['GET'])
def Comment_product_id(product_id):
    comment =until.read_comment_by_product_id_user(product_id=product_id)
    return jsonify({'comment':comment})



# ==================================== thanh toán ===============================
@app.route('/api/pay',methods = ['POST'])
def pay_cart():
    data =request.json
    user_id = data.get('user_id')
    cart = data.get('cart')
    payMethod = data.get('payMethod')
    try:
        until.add_recetail(user_id=user_id,cart=cart,paymethod=payMethod)
    except:
        return jsonify({'code':400})
    return jsonify({'code':200})


# ==================================== list hóa đơn ===============================
@app.route('/api/re',methods = ['GET'])
def r_cart():
    r = until.read_receipts()
    return jsonify({'data':r})


# ==================================== thah toán momo ===============================
@app.route('/pay/paymomo',methods = ['POST'])
def adsdasdas_cart():
    if request.method == 'POST':
        k = request.json
        mo = k.get('money')
        try:
            link = until.pay_momo(money=mo)
        except:
            return jsonify({'Code':400})
        return jsonify({'Code':200,'link':link})

# ==================================== thah toán ATM ===============================
@app.route('/pay/payATM',methods = ['POST'])
def adsdasdas_cartATM():
    if request.method == 'POST':
        k = request.json
        mo = k.get('money')
        try:
            link = until.pay_ATM(money=mo)
        except:
            return jsonify({'Code':400})
        return jsonify({'Code':200,'link':link})

# ========================= product by id =================
@app.route("/api/thongke",methods = ['GET'])
def thongkehoadon():
    pro=until.Thong_ke_receipts()
    return jsonify({'data':pro})


if __name__ == '__main__':
    from admin import *
    app.run(debug=True)