import json
import uuid
import requests
import hmac
import hashlib


def pay_momo(money):
    endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
    accessKey = "F8BBA842ECF85"
    secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
    orderInfo = "PAY WITH MOMO"
    partnerCode = "MOMO"
    redirectUrl = "http://localhost:3000/"
    ipnUrl = "http://localhost:3000/"
    amount = money
    orderId = str(uuid.uuid4())
    requestId = str(uuid.uuid4())
    extraData = ""
    partnerName = "MoMo Payment"
    requestType = "payWithMethod"
    storeId = "Test Store"
    orderGroupId = ""
    autoCapture = True
    lang = "vi"
    orderGroupId = ""


    rawSignature = "accessKey=" + accessKey + "&amount=" + amount + "&extraData=" + extraData + "&ipnUrl=" + ipnUrl + "&orderId=" + orderId \
                + "&orderInfo=" + orderInfo + "&partnerCode=" + partnerCode + "&redirectUrl=" + redirectUrl\
                + "&requestId=" + requestId + "&requestType=" + requestType


    print("--------------------RAW SIGNATURE----------------")
    print(rawSignature)
    # signature
    
    h = hmac.new(bytes(secretKey, 'ascii'), bytes(rawSignature, 'ascii'), hashlib.sha256)
    signature = h.hexdigest()
    print("--------------------SIGNATURE----------------")
    print(signature)

    # json object send to MoMo endpoint

    data = {
        'partnerCode': partnerCode,
        'orderId': orderId,
        'partnerName': partnerName,
        'storeId': storeId,
        'ipnUrl': ipnUrl,
        'amount': amount,
        'lang': lang,
        'requestType': requestType,
        'redirectUrl': redirectUrl,
        'autoCapture': autoCapture,
        'orderInfo': orderInfo,
        'requestId': requestId,
        'extraData': extraData,
        'signature': signature,
        'orderGroupId': orderGroupId
    }

    print("--------------------JSON REQUEST----------------\n")
    data = json.dumps(data)
    print(data)

    clen = len(data)
    response = requests.post(endpoint, data=data, headers={'Content-Type': 'application/json', 'Content-Length': str(clen)})

    # f.close()
    print("--------------------JSON response----------------\n")
    print(response.json())
    print(response.json()['payUrl'])
    return response.json()['payUrl']