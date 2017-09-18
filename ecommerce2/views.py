from ecommerce2.models import *
from django.http import HttpResponse
from django.db.models import F, Count
# from django.db.models.functions import Length, Upper, Value
from django.shortcuts import *
from django.contrib.auth import authenticate
from datetime import datetime

def common_context(request,context):
	user=None
	in_cart=0
	if request.session.has_key('userfirstnameid'):
		user = request.session['userid']
		context['user_name']="Anonymus"
		firstname=Users.objects.filter(userid__exact=user)[0].userfirstname
		lastname=Users.objects.filter(userid__exact=user)[0].userlastname
		if firstname or lastname:
			context['user_name']=firstname+" "+lastname
		order_id=Orders.objects.filter(users_userid__exact=user,is_placed__iexact='no')[0].orderid
		in_cart=int(Orderdetails.objects.filter(orders_orderid=order_id).count())
		print user,in_cart,order_id
	cat=[[a,[]]  for a in Productcategories.objects.filter(super_categorie__isnull=True)]
	for a in cat:
		a[1].extend([[b,[]] for b in Productcategories.objects.all().filter(super_categorie=a[0].categoryid)])
	for a in cat:
		for b in a[1]:
			b[1].extend([c for c in Productcategories.objects.all().filter(super_categorie=b[0].categoryid)])
	context['cat']=cat
	context['user']=user
	context['in_cart']=in_cart

def logout(request):
	if request.session.has_key('userid'):
		del request.session['userid']
	return redirect("/ecommerce2")

def login(request):
	email=request.POST.get("email","")
	pas=request.POST.get("password","")
	if email=="" or pas=="":
			return redirect("/ecommerce2/404")
	print email+" "+" ofvd "+pas+" dcds "+str(request.POST)+" omo"
	user_id=-1
	test=Users.objects.filter(useremail=email,userpassword=pas).exists()
	if test:
		print "done"
		request.session['userid']=Users.objects.filter(useremail=email)[0].userid
		return redirect("/ecommerce2/customer-account.html")
	else:
		return logout(request)

def register(request):
	if request.session.has_key('userid'):
		return logout(request)
	context={}
	common_context(request,context)
	return render(request,'register.html',context)

def user_create(request):
	email=request.POST.get("email","")
	test=Users.objects.filter(useremail=email).exists()
	if test:
		return redirect("/ecommerce2/register.html")
	else:
		pas=request.POST.get("password","")
		if pas=="":
			return redirect("/ecommerce2/404")
		f_name=request.POST.get("firstname","")
		l_name=request.POST.get("lastname","")
		phone=request.POST.get("phone","")
		if len(str(phone)) != 10:
			return redirect("/ecommerce2/register.html")
		user=Users.objects.create(useremail=email,userfirstname=f_name,userlastname=l_name,userpassword=pas,userphone=phone)
		try:
			user.save()
			request.session['userid']=Users.objects.filter(useremail=email)[0].userid
			order=Orders.objects.create(users_userid=request.session['userid'],is_placed="no")
			return redirect("/ecommerce2/customer-account.html")
		except:
			return redirect("/ecommerce2/register.html")

def index(request):
	context={}
	common_context(request,context)
	return render(request,'index.html',context)

def four_04(request):
	context={}
	common_context(request,context)
	return render(request,'404.html',context)

def customer_home(request):
	if request.session.has_key('userid'):
		context={}
		common_context(request,context)
		user = request.session['userid']
		orders=Orders.objects.filter(users_userid__exact=user,is_placed__iexact='yes')
		context["orders"]=orders
		return render(request,'customer-orders.html',context)
	else:
		return redirect("/ecommerce2/404")

def customer_view(request):
	if request.session.has_key('userid'):
		user = request.session['userid']
		user_d=Users.objects.filter(userid__exact=user)[0]
		context={}
		common_context(request,context)
		context['user_d']=user_d
		return render(request,'customer-account.html',context)
	else:
		return redirect("/ecommerce2/404")

def order_detail(request,order_id):
	print order_id
	if request.session.has_key('userid') and order_id:
		user = request.session['userid']
		order=Orders.objects.filter(orderid__exact=order_id)
		if order.exists():
			order_d=order[0]
			if order.filter(users_userid__exact=user).exists():
				context={}
				common_context(request,context)
				
				def product_detail(x):
					return Products.objects.filter(productid__exact=x)[0]

				products=[]
				net_total=0
				for orderz in Orderdetails.objects.filter(orders_orderid__exact=order_id):
					total=orderz.detailprice*orderz.detailquantity
					net_total+=total
					products.append((product_detail(orderz.products_productid),orderz.detailquantity,orderz.detailprice,total))
				context['products']=products
				context['net_total']=net_total
				if order_d.ordershipped==0:
					context['shipped']=" is being prepared"
				elif order_d.ordershipped==1:
					context['shipped']=" has been shipped"
				else:
					context['shipped']=" has been delivered"
				context['order_d']=order_d
				return render(request,'customer-order.html',context)
			else:
				return redirect("/ecommerce2/404")
		else:
			return redirect("/ecommerce2/404")
	else:
		return redirect("/ecommerce2/404")

def sub_prod_dfs(cat_id):
	prods=Productcategories.objects.filter(super_categorie=cat_id)
	cat_list=[]
	if prods.exists():
		for prod in prods:
			cat_list.append(prod.categoryid)
			cat_list.extend(sub_prod_dfs(prod.categoryid))
	return cat_list

def cat_view(request,cat_id):
	prod=Productcategories.objects.filter(categoryid__exact=cat_id)
	if(prod.exists()):
		context={}
		common_context(request,context)
		sup_prods=[]
		prod=prod[0]
		context['cat_view']=prod
		sup_prods.append(prod)
		while prod.super_categorie:
			sup_prod=Productcategories.objects.filter(categoryid__exact=prod.super_categorie)
			if sup_prod.exists():
				sup_prods.append(sup_prod[0])
				prod=sup_prod[0]
			else:
				break
		sup_prods.reverse()
		context['sup_cats']=sup_prods
		sub_cats=sub_prod_dfs(cat_id)
		context['sub_cats']=sub_cats
		sub_cats.append(context['cat_view'].categoryid)
		print context['cat_view'].categoryid,	sub_cats
		products=Products.objects.filter(productcategories_categoryid__in=sub_cats)
		context['products']=products
		context['prod_num']=products.count()
		return render(request,'category.html',context)
	else:
		return redirect("/ecommerce2/404")

def prod_view(request,prod_id):
	prod=Products.objects.filter(productid__exact=prod_id)
	if prod.exists():
		context={}
		common_context(request,context)
		sup_prods=[]
		prod=prod[0]
		context['prod_view']=prod
		cat_this=Productcategories.objects.filter(categoryid__exact=prod.productcategories_categoryid)
		if cat_this.exists():
			cat_this=cat_this[0]
			sup_prods.append(cat_this)
			while cat_this.super_categorie:
				sup_prod=Productcategories.objects.filter(categoryid__exact=cat_this.super_categorie)
				if sup_prod.exists():
					sup_prods.append(sup_prod[0])
					cat_this=sup_prod[0]
				else:
					break
			sup_prods.reverse()
			context['sup_cats']=sup_prods
		else:
			context['sup_cats']=[]
		context['review']=False

		if request.session.has_key('userid'):
			user = request.session['userid']
			orders=[str(order.orderid) for order in Orders.objects.filter(users_userid__exact=user, is_placed__iexact="yes")]
			produtsss=[str(details.products_productid) for details in Orderdetails.objects.filter(orders_orderid__in=orders)]
			print orders,produtsss
			if prod_id in produtsss:
				context['review']=True

		rev=[(rev,Users.objects.get(userid=rev.users_userid).userfirstname+" "+Users.objects.get(userid=rev.users_userid).userlastname) for rev in Reviews.objects.filter(products_productid=prod_id)]
		context['rev']=rev
		if len(rev)==0:
			context['rev']=False
		return render(request,'detail.html',context)
	else:
		return redirect("/ecommerce2/404")

def reviews(request):
	rat=request.POST.get("rating","")
	rev=request.POST.get("review","")
	p_id=request.POST.get("productid","")
	if p_id=="" or rat=="":
		return redirect("/ecommerce2/404")
	if request.session.has_key('userid'):
		user = request.session['userid']
		orders=[order.orderid for order in Orders.objects.filter(users_userid__exact=user, is_placed__iexact="yes")]
		produtsss=[str(details.products_productid) for details in Orderdetails.objects.filter(orders_orderid__in=orders)]
		print p_id,produtsss,orders
		if p_id in produtsss:
			r=Reviews.objects.filter(users_userid=user,products_productid=p_id)
			if r.exists():
				r.update(rating=rat,review=rev)
			else:
				Reviews.objects.create(users_userid=user,products_productid=p_id,rating=rat,review=rev)
			return redirect("/ecommerce2/detail.html/"+p_id)
		else:
			return redirect("/ecommerce2/404")
	else:
		return redirect("/ecommerce2/404")

def cart_addproduct(request):
	if request.session.has_key('userid'):
		user = request.session['userid']
		p_id=request.POST.get("productid","")
		if p_id=="":
			return redirect("/ecommerce2/404")
		quantity=abs(int(float(request.POST.get("quantity",""))))
		print p_id,quantity,type(p_id),type(quantity)
		product=Products.objects.filter(productid__exact=p_id)
		if product.exists():
			product=product[0]
			order_cart_s=Orders.objects.filter(users_userid__exact=user,is_placed__iexact='no')
			if order_cart_s.exists():
				order_cart=order_cart_s[0]
				name=str(product.productid)+" "+str(user)
				price=float(product.productprice)
				price=float(product.productprice)
				if product.productstock and quantity > product.productstock:
					return redirect("/ecommerce2/category.html")
				amount=0
				if Orderdetails.objects.filter(orders_orderid=order_cart.orderid,products_productid=p_id).exists():
					det=Orderdetails.objects.filter(orders_orderid=order_cart.orderid,products_productid=p_id)
					det.update(detailquantity=(det[0].detailquantity+quantity))
				else:
					Orderdetails.objects.create(detailname=name,detailprice=price,detailquantity=quantity,orders_orderid=order_cart.orderid,products_productid=p_id)
				if not order_cart.orderamount:
					amount=price*quantity
				else:
					amount=price*quantity+float(order_cart.orderamount)
				order_cart_s.update(orderamount=amount)
				return redirect("/ecommerce2/basket.html")
			else:
				raise Exception("This user "+user+" does't have a cart. This should never happen.")
		else:
			return redirect("/ecommerce2/404")
	else:
		return redirect("/ecommerce2/register.html")

def cart_defadd(request,p_id):
	if request.session.has_key('userid'):
		user = request.session['userid']
		quantity=1
		print p_id,quantity,type(p_id),type(quantity)
		product=Products.objects.filter(productid__exact=p_id)
		if product.exists():
			product=product[0]
			order_cart_s=Orders.objects.filter(users_userid__exact=user,is_placed__iexact='no')
			if order_cart_s.exists():
				order_cart=order_cart_s[0]
				name=str(product.productid)+" "+str(user)
				price=float(product.productprice)
				if product.productstock and quantity > product.productstock:
					return redirect("/ecommerce2/category.html")
				amount=0
				if Orderdetails.objects.filter(orders_orderid=order_cart.orderid,products_productid=p_id).exists():
					det=Orderdetails.objects.filter(orders_orderid=order_cart.orderid,products_productid=p_id)
					det.update(detailquantity=(det[0].detailquantity+quantity))
				else:
					Orderdetails.objects.create(detailname=name,detailprice=price,detailquantity=quantity,orders_orderid=order_cart.orderid,products_productid=p_id)
				if not order_cart.orderamount:
					amount=price*quantity
				else:
					amount=price*quantity+float(order_cart.orderamount)
				order_cart_s.update(orderamount=amount)
				return redirect("/ecommerce2/basket.html")
			else:
				raise Exception("This user "+user+" does't have a cart. This should never happen.")
		else:
			return redirect("/ecommerce2/404")
	else:
		return redirect("/ecommerce2/register.html")

def cart(request):
	if request.session.has_key('userid'):
		user = request.session['userid']
		order_cart_s=Orders.objects.filter(users_userid__exact=user,is_placed__iexact='no')
		if order_cart_s.exists():
			context={}
			common_context(request,context)
			order_cart=order_cart_s[0]
			details=[]
			net_total=0
			shipping=0
			for detail in Orderdetails.objects.filter(orders_orderid__exact=order_cart.orderid):
				prods=Products.objects.filter(productid__exact=detail.products_productid)
				prod=prods[0]
				total=detail.detailprice*detail.detailquantity
				net_total+=total
				if not prod.productweight:
					prods.update(productweight=100)
				shipping+=0.01*prod.productweight*detail.detailquantity
				details.append((prod,detail,total))
			print net_total
			tax=0.12*net_total
			order_cart_s.update(orderamount=net_total+tax+shipping,ordertax=tax,ordershipping=shipping)
			context['details']=details
			context['tax']=tax
			context['shipping']=shipping
			context['total']=net_total
			context['order']=order_cart
			return render(request,'basket.html',context)
		else:
			raise Exception("This user "+user+" does't have a cart. This should never happen.")
	else:
		return redirect("/ecommerce2/404")

def update_cart(request):
	if request.session.has_key('userid'):
		user = request.session['userid']
		order_cart_s=Orders.objects.filter(users_userid__exact=user,is_placed__iexact='no')
		if order_cart_s.exists():
			order_cart=order_cart_s[0]
			details=Orderdetails.objects.filter(orders_orderid__exact=order_cart.orderid)
			for prod in details:
				prod_id=prod.products_productid
				quantity=abs(int(float(request.POST.get(str(prod_id),""))))
				product_stock=Products.objects.filter(productid__exact=prod_id)[0].productstock
				if product_stock and quantity > product_stock:
					return redirect("/ecommerce2/basket.html")
				Orderdetails.objects.filter(orders_orderid__exact=order_cart.orderid,products_productid__exact=prod_id).update(detailquantity=quantity)	
			return redirect("/ecommerce2/basket.html")
		else:
			raise Exception("This user "+user+" does't have a cart. This should never happen.")

def cart_delproduct(request,prod_id):
	if request.session.has_key('userid'):
		user = request.session['userid']
		product=Products.objects.filter(productid__exact=prod_id)
		if product.exists():
			product=product[0]
			order_cart_s=Orders.objects.filter(users_userid__exact=user,is_placed__iexact='no')
			if order_cart_s.exists():
				deldet=Orderdetails.objects.filter(orders_orderid__exact=order_cart_s[0].orderid,products_productid=prod_id)
				if deldet.exists():
					q=abs(int(deldet[0].detailquantity))
					price=float(deldet[0].detailprice)
					new=order_cart_s[0].orderamount-(q*price)
					if new==0:
						new=None
					order_cart_s.update(orderamount=new)
					deldet.delete()
					return redirect("/ecommerce2/basket.html")
				else:
					return redirect("/ecommerce2/404")
			else:
				raise Exception("This user "+user+" does't have a cart. This should never happen.")
		else:
			return redirect("/ecommerce2/404")
	else:
		return redirect("/ecommerce2/404")

def checkout_common(request,context):
	if request.session.has_key('userid'):
		user = request.session['userid']
		order_cart_s=Orders.objects.filter(users_userid__exact=user,is_placed__iexact='no')
		if order_cart_s.exists():
			common_context(request,context)
			order_cart=order_cart_s[0]
			context['cart_d']=order_cart
			if order_cart.orderamount:
				context['total']=order_cart.orderamount-(order_cart.ordertax+order_cart.ordershipping)
				return True
			else:
				return False
		else:
			raise Exception("This user "+user+" does't have a cart. This should never happen.")
	else:
		return False

def checkout1(request):
	context={}
	if checkout_common(request,context):
		user = request.session['userid']
		user_d=Users.objects.filter(userid__exact=user)
		context['user_d']=user_d[0]
		return render(request,'checkout1.html',context)
	else:
		return redirect("/ecommerce2/404")

def checkout2(request):
	context={}
	zipcode=request.POST.get("zipcode","")
	if zipcode=="":
		return redirect("/ecommerce2/404")
	if checkout_common(request,context):
		email=request.POST.get("email","")
		f_name=request.POST.get("firstname","")
		l_name=request.POST.get("lastname","")
		phone=request.POST.get("phone","")
		house=request.POST.get("house","")
		street=request.POST.get("street","")
		state=request.POST.get("state","")
		country=request.POST.get("country","")
		user = request.session['userid']
		order_cart_s=Orders.objects.filter(users_userid__exact=user,is_placed__iexact='no')
		order_cart_s.update(ordername=f_name+" "+l_name,ordershipaddress=house,ordershipaddress2=street,orderzip=zipcode,\
			orderphone=phone, orderstate=state,ordercountry=country,orderemail=email)
		return render(request,'checkout2.html',context)
	else:
		return redirect("/ecommerce2/404")

def checkout3(request):
	context={}
	delivery=request.POST.get("delivery","")
	if delivery=="":
		return redirect("/ecommerce2/404")
	if checkout_common(request,context):
		user = request.session['userid']
		order_cart_s=Orders.objects.filter(users_userid__exact=user,is_placed__iexact='no')
		order_cart_s.update(ordershipname=delivery)
		return render(request,'checkout3.html',context)
	else:
		return redirect("/ecommerce2/404")

def checkout4(request):
	context={}
	payment=request.POST.get("payment","")
	if payment=="":
		return redirect("/ecommerce2/404")
	if checkout_common(request,context):
		user = request.session['userid']
		order_cart_s=Orders.objects.filter(users_userid__exact=user,is_placed__iexact='no')
		order_cart_s.update(orderpay=payment)
		order_cart=order_cart_s[0]
		details=[]
		for detail in Orderdetails.objects.filter(orders_orderid__exact=order_cart.orderid):
			prods=Products.objects.filter(productid__exact=detail.products_productid)
			prod=prods[0]
			total=detail.detailprice*detail.detailquantity
			details.append((prod,detail,total))
		context['details']=details
		return render(request,'checkout4.html',context)
	else:
		return redirect("/ecommerce2/404")

def order(request):
	if request.session.has_key('userid'):
		user = request.session['userid']
		order_cart_s=Orders.objects.filter(users_userid__exact=user,is_placed__iexact='no')
		if order_cart_s.exists():
			confirm=request.POST.get("confirmed","")
			if confirm=="True":
				order_cart_s.update(orderdate=datetime.now(),is_placed='yes',ordershipped=0)
				Orders.objects.create(users_userid=user,is_placed='no')
				prods=Orderdetails.objects.filter(orders_orderid__exact=order_cart_s[0].orderid)
				for prod in prods:
					ps=Products.objects.filter(productid__exact=prod.products_productid)
					stock=ps[0].productstock
					qun=prod.detailquantity
					print "jjoi",stock,qun
					if stock and stock >= qun:
						ps.update(productstock=stock-qun)
				return redirect("/ecommerce2/customer-orders.html")
			else:
				return redirect("/ecommerce2/404")
		else:
			raise Exception("This user "+user+" does't have a cart. This should never happen.")
	else:
		return redirect("/ecommerce2/404")


def blog(request):
	context={}
	common_context(request,context)
	return render(request,'blog.html',context)

def search(request):
	print "okmpl"
	from collections import OrderedDict
	context={}
	term=request.POST.get("search","")
	context['term']=term
	if term=="":
		return redirect("/ecommerce2/")
	cats=[]
	prod=[]
	common_context(request,context)
	cats.extend([cat for cat in Productcategories.objects.filter(categoryname__iexact=term)])
	cats.extend([cat for cat in Productcategories.objects.filter(categoryname__istartswith=term)])
	cats.extend([cat for cat in Productcategories.objects.filter(categoryname__iendswith=term)])
	cats.extend([cat for cat in Productcategories.objects.filter(categoryname__icontains=term)])
	prod.extend([cat for cat in Products.objects.filter(productname__iexact=term)])
	prod.extend([cat for cat in Products.objects.filter(productname__istartswith=term)])
	prod.extend([cat for cat in Products.objects.filter(productname__iendswith=term)])
	prod.extend([cat for cat in Products.objects.filter(productname__icontains=term)])
	context['products']=list(OrderedDict.fromkeys(prod))
	context['cats']=list(OrderedDict.fromkeys(cats))
	print context['cats']
	cat_total=len(cats)
	p_total=len(prod)
	total=cat_total+p_total
	context['total']=total
	context['pt']=p_total
	context['ct']=cat_total
	return render(request,'search.html',context)

def contact(request):
    context={}
    common_context(request,context)
    return render(request,'contact.html',context)
def faq(request):
    context={}
    common_context(request,context)
    return render(request,'faq.html',context)
def text(request):
    context={}
    common_context(request,context)
    return render(request,'text.html',context)
def post(request):
    context={}
    common_context(request,context)
    return render(request,'post.html',context)