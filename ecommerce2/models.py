# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = True
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'django_session'


class Options(models.Model):
    optionid = models.AutoField(db_column='OptionID', primary_key=True)  # Field name made lowercase.
    optiongroupid = models.IntegerField(db_column='OptionGroupID', blank=True, null=True)  # Field name made lowercase.
    optionname = models.CharField(db_column='OptionName', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'options'


class Orderdetails(models.Model):
    detailid = models.AutoField(db_column='DetailID', primary_key=True)  # Field name made lowercase.
    detailname = models.CharField(db_column='DetailName', max_length=250)  # Field name made lowercase.
    detailprice = models.FloatField(db_column='DetailPrice')  # Field name made lowercase.
    detailquantity = models.IntegerField(db_column='DetailQuantity')  # Field name made lowercase.
    orders_orderid = models.IntegerField(db_column='orders_OrderID')  # Field name made lowercase.
    products_productid = models.IntegerField(db_column='products_ProductID')  # Field name made lowercase.
    def __unicode__(self):
        return str(self.orders_orderid)+" "+str(self.products_productid)

    class Meta:
        managed = True
        db_table = 'orderdetails'


class Orders(models.Model):
    orderid = models.AutoField(db_column='OrderID', primary_key=True)  # Field name made lowercase.
    ordername = models.CharField(db_column='OrderName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    orderamount = models.FloatField(db_column='OrderAmount', blank=True, null=True)  # Field name made lowercase.
    ordershipname = models.CharField(db_column='OrderShipName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ordershipaddress = models.CharField(db_column='OrderShipAddress', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ordershipaddress2 = models.CharField(db_column='OrderShipAddress2', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ordercity = models.CharField(db_column='OrderCity', max_length=50, blank=True, null=True)  # Field name made lowercase.
    orderstate = models.CharField(db_column='OrderState', max_length=50, blank=True, null=True)  # Field name made lowercase.
    orderzip = models.CharField(db_column='OrderZip', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ordercountry = models.CharField(db_column='OrderCountry', max_length=50, blank=True, null=True)  # Field name made lowercase.
    orderphone = models.CharField(db_column='OrderPhone', max_length=20, blank=True, null=True)  # Field name made lowercase.
    orderpay = models.CharField(db_column='OrderFax', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ordershipping = models.FloatField(db_column='OrderShipping', blank=True, null=True)  # Field name made lowercase.
    ordertax = models.FloatField(db_column='OrderTax', blank=True, null=True)  # Field name made lowercase.
    orderemail = models.CharField(db_column='OrderEmail', max_length=100, blank=True, null=True)  # Field name made lowercase.
    orderdate = models.DateTimeField(db_column='OrderDate', blank=True, null=True)  # Field name made lowercase.
    ordershipped = models.IntegerField(db_column='OrderShipped', blank=True, null=True)  # Field name made lowercase.
    ordertrackingnumber = models.CharField(db_column='OrderTrackingNumber', max_length=80, blank=True, null=True)  # Field name made lowercase.
    users_userid = models.IntegerField(db_column='users_UserID')  # Field name made lowercase.
    is_placed = models.CharField(max_length=10)
    ordertest = models.CharField(db_column='OrderTest', max_length=80, blank=True, null=True)
    def __unicode__(self):
        return str(self.users_userid)+" "+str(self.orderid)
    class Meta:
        managed = True
        db_table = 'orders'


class Productcategories(models.Model):
    categoryid = models.AutoField(db_column='CategoryID', primary_key=True)  # Field name made lowercase.
    categoryname = models.CharField(db_column='CategoryName', max_length=50)  # Field name made lowercase.
    super_categorie = models.IntegerField(blank=True, null=True)
    def __unicode__(self):
        return str(self.categoryname)+" "+str(self.categoryid)+" "+str(self.super_categorie)

    class Meta:
        managed = True
        db_table = 'productcategories'


class Products(models.Model):
    productid = models.AutoField(db_column='ProductID', primary_key=True)  # Field name made lowercase.
    productname = models.CharField(db_column='ProductName', max_length=100)  # Field name made lowercase.
    productprice = models.FloatField(db_column='ProductPrice')  # Field name made lowercase.
    productweight = models.FloatField(db_column='ProductWeight')  # Field name made lowercase.
    productcartdesc = models.CharField(db_column='ProductCartDesc', max_length=250)  # Field name made lowercase.
    productshortdesc = models.CharField(db_column='ProductShortDesc', max_length=1000)  # Field name made lowercase.
    productlongdesc = models.TextField(db_column='ProductLongDesc')  # Field name made lowercase.
    productthumb = models.CharField(db_column='ProductThumb', max_length=1000)  # Field name made lowercase.
    productimage = models.CharField(db_column='ProductImage', max_length=1000)  # Field name made lowercase.
    productimage2 = models.CharField(db_column='ProductImage2', max_length=1000)
    productupdatedate = models.DateTimeField(db_column='ProductUpdateDate')  # Field name made lowercase.
    productstock = models.FloatField(db_column='ProductStock', blank=True, null=True)  # Field name made lowercase.
    productlive = models.IntegerField(db_column='ProductLive', blank=True, null=True)  # Field name made lowercase.
    productunlimited = models.IntegerField(db_column='ProductUnlimited', blank=True, null=True)  # Field name made lowercase.
    productlocation = models.CharField(db_column='ProductLocation', max_length=250, blank=True, null=True)  # Field name made lowercase.
    productcategories_categoryid = models.IntegerField(db_column='productcategories_CategoryID')  # Field name made lowercase.
    productcost = models.IntegerField(db_column='productCost')  # Field name made lowercase.

    def __unicode__(self):
        return str(self.productname)+" "+str(self.productid)
    class Meta:
        managed = True
        db_table = 'products'
        unique_together = (('productid', 'productcategories_categoryid'),)


class ProductsHasOptions(models.Model):
    option_price_increment = models.FloatField(blank=True, null=True)
    option_group_id = models.IntegerField()
    products_productid1 = models.IntegerField(db_column='products_ProductID1')  # Field name made lowercase.
    options_optionid1 = models.IntegerField(db_column='options_OptionID1')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'products_has_options'


class Reviews(models.Model):
    reviewid = models.AutoField(db_column='ReviewID', primary_key=True)  # Field name made lowercase.
    rating = models.IntegerField(db_column='Rating')  # Field name made lowercase.
    review = models.CharField(db_column='Review', max_length=50, blank=True, null=True)  # Field name made lowercase.
    products_productid = models.IntegerField(db_column='products_ProductID')  # Field name made lowercase.
    users_userid = models.IntegerField(db_column='users_UserID')  # Field name made lowercase.
    def __unicode__(self):
        return str(self.users_userid)+" "+str(self.products_productid)

    class Meta:
        managed = True
        db_table = 'reviews'


class Users(models.Model):
    userid = models.AutoField(db_column='UserID', primary_key=True)  # Field name made lowercase.
    useremail = models.CharField(db_column='UserEmail', max_length=500)  # Field name made lowercase.
    userpassword = models.CharField(db_column='UserPassword', max_length=500)  # Field name made lowercase.
    userfirstname = models.CharField(db_column='UserFirstName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    userlastname = models.CharField(db_column='UserLastName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    usercity = models.CharField(db_column='UserCity', max_length=90, blank=True, null=True)  # Field name made lowercase.
    userstate = models.CharField(db_column='UserState', max_length=20, blank=True, null=True)  # Field name made lowercase.
    userzip = models.CharField(db_column='UserZip', max_length=12, blank=True, null=True)  # Field name made lowercase.
    useremailverified = models.IntegerField(db_column='UserEmailVerified', blank=True, null=True)  # Field name made lowercase.
    userregistrationdate = models.DateTimeField(db_column='UserRegistrationDate', blank=True, null=True)  # Field name made lowercase.
    userverificationcode = models.CharField(db_column='UserVerificationCode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    userip = models.CharField(db_column='UserIP', max_length=50, blank=True, null=True)  # Field name made lowercase.
    userphone = models.CharField(db_column='UserPhone', max_length=20, blank=True, null=True)  # Field name made lowercase.
    userfax = models.CharField(db_column='UserFax', max_length=20, blank=True, null=True)  # Field name made lowercase.
    usercountry = models.CharField(db_column='UserCountry', max_length=20, blank=True, null=True)  # Field name made lowercase.
    useraddress = models.CharField(db_column='UserAddress', max_length=100, blank=True, null=True)  # Field name made lowercase.
    useraddress2 = models.CharField(db_column='UserAddress2', max_length=50, blank=True, null=True)  # Field name made lowercase.

    def __unicode__(self):
        return str(self.useremail)+" "+str(self.userid)

    class Meta:
        managed = True
        db_table = 'users'
