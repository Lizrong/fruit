from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from axf.forms.login import LoginForm
from axf.models import *
from axf2 import settings



def home(request):
    title='主页'
    wheelsList=Wheel.objects.all()
    navList=Nav.objects.all()
    mustbuyList=Mustbuy.objects.all()
    shopList=Shop.objects.all()
    shop1=shopList[0]
    shop2=shopList[1:3]
    shop3=shopList[3:7]
    shop4=shopList[7:11]
    mainList=MainShow.objects.all()
    return render(request,'axf/home.html',locals())

def market(request,categoryid,cid,sortid):
    title= "闪送超市"
    leftSlider = FoodTypes.objects.all()
    if cid == '0':
        productList = Goods.objects.filter(categoryid=categoryid)
    else:
        productList = Goods.objects.filter(categoryid=categoryid, childcid=cid)
    #排序
    if sortid == '1':
        productList.order_by("productnum")
    elif sortid == '2':
        productList = productList.order_by("price")
    elif sortid == '3':
        productList = productList.order_by("-price")
    group = leftSlider.get(typeid=categoryid)
    childList = []
    # 全部分类:0#进口水果:103534#国产水果:103533
    childnames = group.childtypenames
    arr1 = childnames.split("#")
    for str in arr1:
        # 全部分类:0
        arr2 = str.split(":")
        obj = {"childName": arr2[0], "childId": arr2[1]}
        childList.append(obj)

    user_id=request.session.get("user_id")
    if user_id:
        for good in productList:
            carts=Cart.objects.filter(goods_id=good.id,user_id=user_id)
            if carts:
                cart=carts.first()
                good.cart_num=cart.goods_num
            else:
                good.cart_num=0

    return render(request,'axf/market.html',locals())

def mine(request):
    title= "我的"
    user_id=request.session.get("user_id")
    if user_id:
        user = UserModel.objects.get(id=user_id)
        userImg=user.figure
        username=user.username
        userrank=user.userrank
        userImg = "/static/uploads/icons/" + username+".jpg"
    else:
        username = "未登录"
    return render(request,'axf/mine.html',locals())

def check_username(request):
    username = request.GET.get("username")
    users = UserModel.objects.filter(username=username)

    data = {
        "color":"green",
        "msg":"恭喜，可以使用该用户名~~~",
        "status":"ok"
    }
    if users.exists():
        data["color"] = "red"
        data["msg"] = "该用户名已被注册，请使用其他用户名！"
        data["status"] = "fail"
    return JsonResponse(data)
#md5加密
import hashlib
def generate_password(password):
    m5=hashlib.md5()
    m5.update(password.encode('utf-8'))
    return m5.hexdigest()
#注册
import os
def user_register(request):
    if request.method=="GET":
        title = "注册"
        return render(request,'axf/register.html',locals())
    else:
        username=request.POST["userAccount"]
        userpwd=request.POST["userPassword"]
        usernickname=request.POST["userNickname"]
        userphone=request.POST["userPhone"]
        useraddress=request.POST["userAddress"]
        userrank=request.POST["userRank"]
        userpwd=generate_password(userpwd)
        userimg = request.FILES["userImg"]
        dest_path = os.path.join(settings.MEDIA_ROOT,username+".jpg")
        with open(dest_path,'wb') as f:
            for chunk in userimg.chunks():
                f.write(chunk)
        try:
            user=UserModel.objects.create(username=username,password=userpwd,usernickname=usernickname,userphone=userphone,useraddress=useraddress,figure=dest_path,userrank=userrank)
        except:
            return redirect(reverse("axf:userreg"))
        request.session["user_id"]=user.id
        return redirect(reverse("axf:mine"))
#登录
def user_login(request):
    if request.method=="POST":
        logform=LoginForm(request.POST)
        if logform.is_valid():
            logname=logform.cleaned_data["logname"]
            logpwd=logform.cleaned_data["logpwd"]
            logpwd=generate_password(logpwd)

            users = UserModel.objects.filter(username=logname, password=logpwd)
            if users:
                user = users.first()
                request.session["user_id"] = user.id
                return redirect(reverse("axf:mine"))
            else:
                msg= "用户名或密码错误，请重新登录！"
                return render(request,"axf/login.html",locals())
    else:
        logform=LoginForm()
        title="登录"
        return render(request,'axf/login.html',locals())
#用户详细信息
def user_detail(request):
    title = "详细信息"
    user_id = request.session.get("user_id")
    if user_id:
        user = UserModel.objects.get(id=user_id)
        username=user.username
        userpwd=user.password
        usernickname = user.usernickname
        userrank = user.userrank
        userphone=user.userphone
        useraddress=user.useraddress
    else:
        username = "未登录"
    return render(request, 'axf/usetdetail.html', locals())
#退出登录
def quit(request):
    request.session.flush()
    return redirect(reverse("axf:mine"))


def cart(request):
    user_id = request.session.get("user_id")
    cartslist = Cart.objects.filter(user_id=user_id)
    infolist = []
    for cart in cartslist:
        goods = cart.goods
        temp_dict = {}
        temp_dict["productimg"] = goods.productimg
        temp_dict["productname"] = goods.productname
        temp_dict["productid"] = goods.productid
        temp_dict["price"] = goods.price
        temp_dict["ischoose"] = cart.is_choose
        temp_dict["goods_num"] = cart.goods_num
        temp_dict["cartid"] = cart.id
        infolist.append(temp_dict)
    return render(request, 'axf/cart.html', locals())

def add_to_cart(request):
    goods_id=request.GET.get("goods_id")
    user_id=request.session.get("user_id")
    data={
        "status":"200",
    }
    if  not user_id:
        data["status"]="900"
        return JsonResponse(data)
    else:
        carts=Cart.objects.filter(goods_id=goods_id,user_id=user_id)
        if carts:
            cart=carts.first()
            cart.goods_num=cart.goods_num+1
            cart.save()
            data["cart_num"]=cart.goods_num
        else:
            Cart.objects.create(goods_id=goods_id,user_id=user_id)
            data["cart_num"]=1
    return JsonResponse(data)

def sub_to_cart(request):
    goods_id=request.GET.get("goods_id")
    user_id=request.session.get("user_id")
    data={
        "status":"200",
    }
    if not user_id:
        data["status"]="900"
        return JsonResponse(data)
    else:
        carts=Cart.objects.filter(goods_id=goods_id,user_id=user_id)
        if carts:
            cart=carts.first()
            if cart.goods_num==1:
                cart.delete()
                data["cart_num"]=0
            else:
                cart.goods_num = cart.goods_num -1
                cart.save()
                data["cart_num"] = cart.goods_num
        else:
            data["msg"]="购物车中无此商品"
            data["status"]="901"
    return JsonResponse(data)

def change_cart_select(request):
    cartid=request.GET.get("cartid")
    carts=Cart.objects.filter(pk=cartid)  #根据主键查询购物车记录
    cart=carts.first()
    cart.is_choose= not cart.is_choose
    cart.save()
    return JsonResponse({"seleceed":cart.is_choose})

def change_all_select(request):
    notselects=request.GET.get("notselects")
    noselects_id=notselects.split("#")
    for noselectid in noselects_id:
        cart=Cart.objects.get(id=noselectid)
        cart.is_choose=True
        cart.save()
    return JsonResponse({"status":"200"})








