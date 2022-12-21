
from __init__ import *

from modal import * 

from sqlalchemy import func
# =================pay momo================
import json
import uuid
import requests
import hmac
import hashlib



# ============================== read banner =====================
def read_banner():
    banner = Banner.query.order_by(-Banner.id).all()
    datas = []
    for b in banner:
        datas.append({
            'image':b.image
        })
    return datas
# ============================== post banner =====================
def post_banner(img):
    b = Banner(image = img)
    db.session.add(b)
    db.session.commit()

# ============================== delete banner =====================
def delete_banner(id):
    Banner.query.filter(Banner.id == id).delete()
    db.session.commit()


# ============================== put banner =====================
def put_banner(id,img):
    b = Banner.query.filter(Banner.id == id).all()
    b.image = img
    db.session.commit()
    



# ============================== read user login =====================
def check_login(name,password):
    user = User.query.filter(User.username == name ,User.password == password).first()
    return user

# =================================== read user ============================
def read_user():
    user = User.query.all()
    data=[]
    for u in user:
        data.append({
            'id':u.id,
            'name':u.username,
            'email':u.email,
        })
    return data
# =================================== read user by name ============================
def read_user_by_name(name):
    return User.query.filter(User.username == name).first()
# =================================== read user by email============================
def read_user_by_email(email):
    return User.query.filter(User.email == email).first()
# ================================ add user ================================
def add_user(name,password,email):
    user = User(username = name,password = password,email = email)
    db.session.add(user)
    db.session.commit()
    return user


# ============================== read caterogy =====================
def read_category():
    # caterogy = Caterogy.query.all()
    caterogy = db.session.query(Caterogy.id,Caterogy.username,func.count(Product.id))\
            .join(Product,Caterogy.id ==Product.category_id )\
            .group_by(Caterogy.id,Caterogy.username)
    data=[]
    for c in caterogy:
        data.append({
            'id':c.id,
            'name':c.username,
            'count_products':c[2],
        })
    return data


# ============================== post caterogy =====================
def post_category(name):
   c = Caterogy(username=name)
   db.session.add(c)
   db.session.commit()

# ============================== delete caterogy =====================
def delete_category(id):
   Caterogy.query.filter(Caterogy.id == id).delete()
   db.session.commit()


# ============================== put caterogy =====================
def put_category(name,newName):
   c = Caterogy.query.filter(Caterogy.username == name).first()
   c.username = newName
   db.session.commit()


# ============================== post list image product =====================
def post_listImageProduct(product_id , image,color):
    img =ListImageProduct(products_id = product_id , image = image,color =color)
    db.session.add(img)
    db.session.commit()
# ============================== put list image product =====================
def put_listImageProduct(image_id , image,color):
    img = ListImageProduct.query.filter(ListImageProduct.id == image_id).first()
    img.image = image
    img.color = color
    db.session.commit()

# ============================== delete list image product =====================
def delete_listImageProduct(image_id):
    ListImageProduct.query.filter(ListImageProduct.id == image_id).delete()
    db.session.commit()

# ============================== đọc product ====================

def read_product(product_id=None,kw=None,caterogy_id=None,page=1):
    products = Product.query.order_by(-Product.id).all()
    listImage = ListImageProduct.query.all()
    if product_id:
        products = Product.query.filter(Product.id == product_id).first()
    if kw:
        products = Product.query.filter(Product.name.contains(kw)).all()
    
    if caterogy_id:
        products = Product.query.filter(Product.category_id == caterogy_id).all()
    data = []
    for p in products:
        data.append({
            'id':p.id,
            'name':p.name,
            'description': p.description,
            'sale':p.sale,
            'priceUp':p.priceUp,
            'priceDown':p.priceDown,
            'color':p.color,
            'ram':p.ram,   
            'rom':p.rom,
            'screen':p.screen,
            'image':p.image,
            'create_time':p.create_time,
            'active':p.active,
            'card':p.card,
            'category_id':p.category_id,
            'listImage':[{'id':img.id,'image':img.image,'color':img.color} for img in listImage if p.id == img.products_id]
        })
        
    size = app.config['SIZE_PRODUCT']
    start = (page -1) * size
    end = start + size
    return data[start:end]

# ==================================== list image post product ===========================================
def readimage_product():
    data = ListImageProduct.query.all()
    return data


# ==================================== post product ===========================================
def post_product(name,description,sale,priceUp,priceDown,color,ram,rom,screen,image,card,category_id):
    p = Product(name=name,description=description,sale=sale
                ,priceUp=priceUp,priceDown=priceDown,color=color,ram=ram,
                rom=rom,screen=screen,image=image,card=card,category_id=category_id)
    db.session.add(p)
    db.session.commit()

# ==================================== delete product ===========================================
def delete_product(product_id):
    Product.query.filter(Product.id == product_id).delete()
    db.session.commit()

# ==================================== put product ===========================================
def put_product(product_id,name,description,sale,priceUp,priceDown,color,ram,rom,screen,image,card,category_id ):
    p = Product.query.filter(Product.id == product_id).first()
    p.name = name
    p.description = description
    p.sale=sale
    p.priceUp=priceUp
    p.priceDown=priceDown
    p.color=color
    p.ram=ram
    p.rom=rom
    p.screen=screen
    p.image=image
    p.card=card
    p.category_id=category_id
    db.session.commit()

# ============================== đọc product by id ====================

def read_product_by_id(product_id):
    products = Product.query.filter(Product.id == product_id).first()
    listImage = ListImageProduct.query.all()
    data = []
    data.append({
        'id':products.id,
        'name':products.name,
        'description': products.description,
        'sale':products.sale,
        'priceUp':products.priceUp,
        'priceDown':products.priceDown,
        'color':products.color,
        'ram':products.ram,   
        'rom':products.rom,
        'screen':products.screen,
        'image':products.image,
        'create_time':products.create_time,
        'active':products.active,
        'card':products.card,
        'category_id':products.category_id,
        'listImage':[{'id':img.id,'image':img.image,'color':img.color} for img in listImage if products.id == img.products_id]
    })
        
    return data



# # ========================================= add comment ==================================

def add_comment(user_id,product_id,content):
    comment = Comment(user_id = user_id,product_id = product_id,content = content)
    db.session.add(comment)
    db.session.commit()
    return comment

# ============================================ đọc commetn theo product id ====================

def read_comment_by_product_id(product_id):
    comment = Comment.query.filter(Comment.product_id == product_id).order_by(-Comment.id).all()
    return comment


# ============================================ đọc commetn theo product id vơi user_id ====================

def read_comment_by_product_id_user(product_id):
    comment = db.session.query(Comment,User).filter(Comment.user_id == User.id,Comment.product_id== str(product_id)).order_by(-Comment.id).all()
    data =[]
    for c in comment:
        data.append({
            'id':c[0].id,
            'content':c[0].content,
            'create_time':c[0].create_time,
            'name':c[1].username,
            'avatar':c[1].avatar
        })
    
    
    return data


# ========================================= add thanh toán ===========================

def add_recetail(user_id,cart,paymethod):
    if cart:
        receipt = Receipt(user_id=user_id)
        db.session.add(receipt)
        for c in cart:
            d =ReceiptDetail(receipt = receipt,
                             product_id = c['id'],
                             price=c['priceDown'],
                             qly=c['qly'],
                             sum_price = float(c['qly']) * float(c['priceDown']),
                             payMethod=paymethod)
            db.session.add(d)
        db.session.commit()



# ========================================= read hóa đoen ===========================

def read_receipts():
    receipt = db.session.query(ReceiptDetail,Receipt.user_id,Product,User)\
            .filter(ReceiptDetail.receipt_id==Receipt.id,ReceiptDetail.product_id == Product.id)\
            .filter(Receipt.user_id == User.id)\
            .order_by(-ReceiptDetail.id).all()
    data = []
    for r in receipt:
        data.append({
            'qly':r[0].qly,
            'receip':r[0].id,
            'sum_price':r[0].sum_price,
            'create_time':r[0].creat_time,
            'payMethod':r[0].payMethod,
            'user_id':r[1],
            'product_name':r[2].name,
            'product_image':r[2].image,
            'user_name':r[3].username,
            'user_email':r[3].email,
        })
    return data

# ================================ thống kê danh thu hóa đơn ============================
def Thong_ke_receipts():
    receipt = db.session.query(Product.id,Product.name,func.sum(ReceiptDetail.sum_price))\
            .join(ReceiptDetail,ReceiptDetail.product_id == Product.id)\
        .group_by(Product.id,Product.name)
    data = []
    for r in receipt:
        data.append({
            'id':r[0],
            'name':r[1],
            'price':r[2],
        })
    return data




def pay_momo(money):
    endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
    partnerCode = "MOMO"
    accessKey = "F8BBA842ECF85"
    secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
    orderInfo = "pay with MoMo"
    redirectUrl = "http://localhost:3000/cart"
    ipnUrl = "http://localhost:3000/cart"
    amount = str(money)
    orderId = str(uuid.uuid4())
    requestId = str(uuid.uuid4())
    requestType = "captureWallet"
    extraData = ""  # pass empty value or Encode base64 JsonString
    
    rawSignature = "accessKey=" + accessKey + "&amount=" + amount + "&extraData=" + extraData + "&ipnUrl=" + ipnUrl + "&orderId=" + orderId + "&orderInfo=" + orderInfo + "&partnerCode=" + partnerCode + "&redirectUrl=" + redirectUrl + "&requestId=" + requestId + "&requestType=" + requestType
    h = hmac.new(bytes(secretKey, 'ascii'), bytes(rawSignature, 'ascii'), hashlib.sha256)
    signature = h.hexdigest()
    data = {
        'partnerCode': partnerCode,
        'partnerName': "Test",
        'storeId': "MomoTestStore",
        'requestId': requestId,
        'amount': amount,
        'orderId': orderId,
        'orderInfo': orderInfo,
        'redirectUrl': redirectUrl,
        'ipnUrl': ipnUrl,
        'lang': "vi",
        'extraData': extraData,
        'requestType': requestType,
        'signature': signature
    }
    print("--------------------JSON REQUEST----------------\n")
    data = json.dumps(data)
    print(data)

    clen = len(data)
    response = requests.post(endpoint, data=data, headers={'Content-Type': 'application/json', 'Content-Length': str(clen)})

    # f.close()
    print("--------------------JSON response----------------\n")
    print(response.json())
    return response.json()['payUrl']


def pay_ATM(money):
    endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
    partnerCode = "MOMO"
    accessKey = "F8BBA842ECF85"
    secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
    orderInfo = "pay with MoMo"
    redirectUrl = "http://localhost:3000/cart"
    ipnUrl = "http://localhost:3000/cart"
    amount = str(money)
    orderId = str(uuid.uuid4())
    requestId = str(uuid.uuid4())
    requestType = "payWithATM"
    extraData = ""  # pass empty value or Encode base64 JsonString
    
    rawSignature = "accessKey=" + accessKey + "&amount=" + amount + "&extraData=" + extraData + "&ipnUrl=" + ipnUrl + "&orderId=" + orderId + "&orderInfo=" + orderInfo + "&partnerCode=" + partnerCode + "&redirectUrl=" + redirectUrl + "&requestId=" + requestId + "&requestType=" + requestType
    h = hmac.new(bytes(secretKey, 'ascii'), bytes(rawSignature, 'ascii'), hashlib.sha256)
    signature = h.hexdigest()
    data = {
        'partnerCode': partnerCode,
        'partnerName': "Test",
        'storeId': "MomoTestStore",
        'requestId': requestId,
        'amount': amount,
        'orderId': orderId,
        'orderInfo': orderInfo,
        'redirectUrl': redirectUrl,
        'ipnUrl': ipnUrl,
        'lang': "vi",
        'extraData': extraData,
        'requestType': requestType,
        'signature': signature
    }
    print("--------------------JSON REQUEST----------------\n")
    data = json.dumps(data)
    print(data)

    clen = len(data)
    response = requests.post(endpoint, data=data, headers={'Content-Type': 'application/json', 'Content-Length': str(clen)})

    # f.close()
    print("--------------------JSON response----------------\n")
    print(response.json())
    return response.json()['payUrl']




        
# with app.app_context():
#     k = Thong_ke_receipts()
#     for i in k:
#         print(i)