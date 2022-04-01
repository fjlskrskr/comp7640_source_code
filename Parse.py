from database import Database
import re

#数据库做好后需要调整的地方：
#根据数据库连接速度来决定是否该进connect和close那里
#add_item()的价格、库存的数值类型
#add_item()的keyword空值在数据库的表示方式
#add_shop()的rating的数值类型

def sort_key(s):
    #sort_strings_with_embedded_numbers
    re_digits = re.compile(r'(\d+)')
    pieces = re_digits.split(s)  # 切成数字与非数字
    pieces[1::2] = map(int, pieces[1::2])  # 将数字部分转成整数
    return pieces

def getDiff2(arr1,arr2):
    set_1 = ()
    set_2 = ()

    #将列表转换为集合set()
    set_1 = set(arr1)
    print(set_1)
    set_2 = set(arr2)
    print(set_2)

    set_more1 = ()
    set_more2 = ()

    #集合运算
    set_1_2 = set_1 & set_2
    set_more1 = set_1 -set_1_2
    set_more2 = set_2 -set_1_2
    return list(set_more1)

def loginmenu():
    print("*"*38)
    print("Welcome to the online retail system!")
    print()
    print("1: login account")
    print("2: register account")
    print()
    print("0: exit system")
    print("*"*38)
    print('Please input the number corresponding to the command:')

def showmenu():
    print("*"*38)
    print("You have entered the 'show' command interface")
    print()
    print("1: show items of a specified shop")
    print("2: show all shop information")
    print("3: show your shopping cart contents")
    print("4: show your account orders")
    print()
    print("0: back to main menu")
    print("*"*38)
    print('Please input the number corresponding to the command:')

def addmenu():
    print("*"*38)
    print("You have entered the 'add' command interface")
    print()
    print("1: add a new item to a specified shop")
    print("2: add a new shop")
    print("3: add your cart as a new order")
    print()
    print("0: back to main menu")
    print("*"*38)
    print('Please input the number corresponding to the command:')

def deletemenu():
    print("*"*38)
    print("You have entered the 'delete' command interface")
    print()
    print("1: delete a specified item")
    print("2: delete a specified shop")
    print("3: delete contents of your shopping cart")
    print("4: delete contents of your order")
    print()
    print("0: back to main menu")
    print("*"*38)
    print('Please input the number corresponding to the command:')

def commandmenu(account):
    print("*"*38)
    print("Welcome to the online retail system!")
    print()
    print(f'Your login account id: {account}')
    print()
    print("1: search item")
    print("2: purchase item")
    print("3: command----show")
    print("4: command----add")
    print("5: command----delete")
    print()
    print("0: exit system")
    print("*"*38)
    print('Please input the number corresponding to the command:')

def login(stat):
    #done
    print('Please input your account id:')
    account = input()
    result = []
    if any(account):
        result = Database().show('customer','password','cid = ' + account)
    if any(result):
        print('Please input your password:')
        if input() == result[0]:
            print('Login success')
            stat = 1
            print()
            input("Please press enter to return to the system")
            return stat,account
        else:
            print('Wrong password')
    else:
        print('account not found')
    account = []
    return stat,account

def register():
    print('Please input the account id you want to register:')
    account = input()
    if any(account):
        result = Database().show('customer','password','cid = \'' + account + '\'')
        if not any(result):
            val = []
            val.append(account)
            print('Please input your telephone number:')
            val.append(input())
            print('Please input your address:')
            val.append(input())
            print('Please input your password:')
            val.append(input())
            if all(val):
                Database().add('customer','cid,tel,address,password',val)
                print('Register success')
            else:
                print('Register fail: invalid empty input')
        else:
            print('Register fail: This account id has already been registered')
    else:
        print('Register fail: invalid account id input')

def search():
    # if inp_split[0] == 'search':
    print('which search mode do you want to choose?')
    print("1: search items with specific key")
    print("2: search items with specific name")
    smode = input()

    #search items with specific key
    if smode == '1':  
        print('please input item keyword')
        itemkey = input()
        if any(itemkey):
            wherekey = 'feature1 = \'' + itemkey + '\' OR feature2 = \'' + itemkey + '\' OR feature3 = \'' + itemkey + '\''
            result = Database().show('item','iid,iname,price,quantity',wherekey)
            if any(result):
                #result =[[]]
                result = [list(i) for i in result]
                print(f'The following(s) is item with keyword {itemkey}:')
                print('{:^20}{:^20}{:^20}{:^20}'.format('iid','iname','price','quantity'))
                for i in result:
                    print('{:^20}{:^20}{:^20}{:^20}'.format(result[i][0],result[i][1],result[i][2],result[i][3]))
            else:
                print('item not found')
        else:
            print('invalid keyword input')

    #search items with specific name
    elif smode == '2':
        print('please input item name')
        itemname = input()
        if any(itemname):
            result = Database().show('item','iid,iname,price,quantity','iname = \'' + itemname + '\'')
            if any(result):
                #result =[[]]
                result = [list(i) for i in result]
                print(f'The following(s) is item named {itemname}:')
                print('{:^20}{:^20}{:^20}{:^20}'.format('iid','iname','price','quantity'))
                for i in result:
                    print('{:^20}{:^20}{:^20}{:^20}'.format(result[i][0],result[i][1],result[i][2],result[i][3]))
            else:
                print('item not found')
        else:
            print('command not executed:invalid name input')
    
    else:
        print('invalid mode selection')

def purchase(cart):
    #purchase an item with specific item id
    #cart = {'i15':['apple',500,20],'i16':['banana',20,10]}
    print('please input the item id you want to purchase:')
    itemid = input()
    result = []
    if any(itemid):
        result = Database().show('item','iid,iname,price,quantity','iid = ' + itemid)
    if any(result):
        #result = ['i15','apple',500,20]
        result = list(result[0])
        #output the item information
        print('item found:')
        print('{:^20}{:^20}{:^20}{:^20}'.format('iid','iname','price','quantity'))
        print('{:^20}{:^20}{:^20}{:^20}'.format(result[0],result[1],result[2],result[3]))
        print('please enter the quantity you want to buy:')
        try:
            itemnum = int(input())
            if itemnum > 0 and itemnum <= result[3]:
                if itemid in list(cart.keys()):
                    #cart already have this item
                    cart[itemid][2] = cart[itemid][2] + itemnum
                    cart[itemid][1] = cart[itemid][1] + itemnum*cart[itemid][1]
                else:
                    #add new item to cart
                    result[2] = result[2]*itemnum
                    cart[itemid] = result[1:]
                print(f'you have successfully purchased {itemnum} {result[1]} to the shopping cart')
            else:
                print('invalid quantity input')
        except ValueError:
            print('invalid quantity input')
    else:
        print('item id not found')

    return cart

def show_item():
    #show items of a shop
    print('Please input a store id to display its items:')
    shopid = input()
    result = []
    if any(shopid):
        result = Database().show('item','iid,iname,price,quantity','sid = \'' + shopid + '\'')
    if any(result):
        #result = [['i15','apple',100,12],[...,...]]
        result = [list(i) for i in result]
        print('{:^20}{:^20}{:^20}{:^20}'.format('iid','iname','price','quantity'))
        for i in result:
            print('{:^20}{:^20}{:^20}{:^20}'.format(i[0],i[1],i[2],i[3]))
    else:
        print('item not found')
    return

def show_shop():
    #show all shop information
    result = Database().show('shop','*')
    if any(result):
        print('information for all shops is as follows:')
        #result = [['s15','aplshop','4','daipo'],[...,...]]
        result = [list(i) for i in result]
        print('{:^20}{:^20}{:^20}{:^20}'.format('sid','sname','rating','location'))
        for i in result:
            print('{:^20}{:^20}{:^20}{:^20}'.format(i[0],i[1],i[2],i[3]))
    else:
        print('no shop exists')

def show_cart(cart):
    #output the cart list
    if any(cart):
        print('This is your shopping cart content:')
        print()
        print('{:^20}{:^20}{:^20}{:^20}'.format('iid','iname','price','quantity'))
        for i in cart:
            print('{:^20}{:^20}{:^20}{:^20}'.format(i,cart[i][0],cart[i][1],cart[i][2]))
    else:
        print('your cart is empty')

def show_order(account_id):
    print('please input the command number you want:')
    print("1: show all orders you have")
    print("2: show the details of your order")
    selection = input()

    if selection == '1':
        #show all order information belongs to current account
        result = Database().show('order','oid,date','iid = \'' + account_id + '\'')
        if any(result):
            print('here are all the order(s) you have:')
            #result = [['i15',12],[...,...]]
            result = [list(i) for i in result]
            print('{:^20}{:^20}'.format('oid','date'))
            for i in result:
                print('{:^20}{:^20}'.format(i[0],i[1]))
        else:
            print('you dont have any orders')

    elif selection == '2':
        #check account_id first then show order details with specific order id
        #需要等数据库建好了测试一次，假设result = (('20132515'),)
        print('please input the order id you want to show details:')
        orderid = input()
        result = []
        if any(orderid):
            result = Database().show('order','cid','oid = \'' + orderid + '\'')
        if any(result):
            result = result[0]
            if result == account_id:
                result = Database().show('detail','iid,iname,price,quantity','oid = \'' + orderid + '\'')
                #cart转order有避免空order生成，这里默认一定有result
                #result = [['i15',12],[...,...]]
                result = [list(i) for i in result]
                print(f'here are all the details of your {orderid} order:')
                print('{:^20}{:^20}{:^20}{:^20}'.format('iid','iname','price','quantity'))
                for i in result:
                    print('{:^20}{:^20}{:^20}{:^20}'.format(i[0],i[1],i[2],i[3]))
            else:
                print('this is not your order, you cannot view the detail')
        else:
            print('order does not exist')
    
def add_item():
    #add a new item to a shop
    print('please input the shop id of the item you want to add:')
    shopid = input()
    result = []
    if any(shopid):
        #add a new item to a shop with specific shop id
        #check if shop exist
        result = Database().show('shop','sid','sid = ' + shopid)
        #result = () or result = ((...),)
    if any(result):
        #get item name list of the shop
        namelist = Database().show('item','iname','sid = ' + shopid)
        #namelist = ['apple','banana']
        values = []
        print('please input the name of new item:')
        name = input()
        #check for duplicate names
        if name in namelist:
            print(f'{name} is already in the shop, do you want to add stock? input "yes" to continue')
            if input() == 'yes':
                print('please enter the amount of stock that needs to be increased:')
                num = input()
                addstock = f'quantity = quantity + {num}'
                Database().update('item',addstock,'iname = \'' + name + '\'' + ' AND sid = \'' + shopid + '\'')
                print(f'inventory of {name} has increased by {num}')
            else:
                print('command canceled, no item added')
        else:
            try:
                #generate new id for the new item
                #idlist = ['i15','i16']
                idlist = Database().show('item','iid')
                idlist.sort(key=sort_key,reverse=True)
                #idlist = ['i16','i15']
                pieces = re.compile(r'(\d+)').split(idlist[0])
                newid = pieces[0]+ str(int(pieces[1])+1)
                #set id
                values.append(newid)
                #set name
                values.append(name)
                print('please input the price of new item:')
                #int?float?
                #set price
                values.append(int(input()))
                print('please enter 1 to 3 keywords of the item new item:(multi-keyword should be separated by ",")')
                keyword = input().replace(' ','')
                keyword = keyword.split(',')
                #check keyword validity
                if all(keyword) and len(keyword) in range(1,4):
                    while len(keyword)<3:
                        #null value in sql
                        keyword.append(None)
                    #set keywords
                    values.extend(keyword)
                else:
                    print('invalid keyword input, no item added')
                    return
                    
                print('please input the quantity of new item:')
                #set quantity
                values.append(int(input()))
                #if all setting valid,add new item to database
                Database().add('item','iid, iname, price, feature1, feature2, feature3, quantity, sid',values)
                print(f'new item has been added, Its assigned id is: {newid}')
            except ValueError:
                print('invalid numeric input, no item added')
    else:
        print('shop id not found')

def add_shop():
    print('please input the name of new shop:')
    name = input()
    namelsit = []
    if any(name):
        namelsit = Database().show('shop','sname')
        #check for duplicate names
        if name in namelsit:
            print(f'There is already a shop called {name}')
        else:
            try:
                values = []
                #generate new id for the new shop
                idlist = Database().show('shop','sid')
                idlist.sort(key=sort_key,reverse=True)
                pieces = re.compile(r'(\d+)').split(idlist[0])
                newid = pieces[0]+ str(int(pieces[1])+1)
                #set id
                values.append(newid)
                #set name
                values.append(name)
                print('please input the rating of new shop:')
                #int?float?
                #set rating
                values.append(int(input()))
                print('please input the location of new shop:')
                #set location
                values.append(input())
                #if all setting valid,add new item to database
                Database().add('shop','sid, sname, rating, location',values)
                print(f'new shop has been added, Its assigned id is: {newid}')
            except ValueError:
                print('invalid numeric input')
    else:
        print('invalid name input')

def add_order(cart:dict,account_id):
    print('you are adding your shopping cart as a new order, press enter to continue')
    input()
    #Generate shopping cart content as a new order, if done: clean up shopping cart
    #check if cart is empty
    if any(cart):
        #check if cart item unfound or invetory lack  
        lacklist = []
        unfoundlist = []
        #cart_item_id = ['i15','i22']
        cart_item_id = list(cart.keys())
        id_str = str(cart_item_id).strip('[]')
        #current_item = (('i15','apple',50,100),(...))
        current_item = Database().show('item','iid, iname, price, quantity',f'iid IN ({id_str})')
        #current_item = [['i15','apple',500,100],[...]]
        current_item = [list(i) for i in current_item]
        #current_dict = {'i15':quantity,'i16':30}
        current_dict = {}
        for i in current_item:
            current_dict[i[0]] = i[3]
        #list(current_item.keys() = ['i15','i22']
        unfound = getDiff2(cart_item_id,list(current_dict.keys()))
        for j in cart:
            if j in unfound:
                unfoundlist.append(cart[j][0])
            elif cart[j][2] > current_dict[j]:
                lacklist.append(cart[j][0])
        #if any unfound or lack, order can not be add
        if any(unfound) or any(lacklist):
            if any(unfound):
                unfoundlist = str(unfoundlist).strip('[]')
                print(f'{unfoundlist} may have been removed')
            if any(lacklist):
                lacklist = str(lacklist).strip('[]')
                print(f'inventory of {lacklist} cannot meet quantity demand')
            print('please modify your cart before adding order again')
            #必要return
            return cart
        #if all item in cart valid
        values = []
        #generate new id for the new order
        idlist = Database().show('order','oid')
        idlist.sort(key=sort_key,reverse=True)
        pieces = re.compile(r'(\d+)').split(idlist[0])
        newid = pieces[0]+ str(int(pieces[1])+1)
        #generate order information
        values.append(newid)
        values.append(account_id)
        #add order information to order table
        Database().add('order','oid, cid, date',values,date=True)
        #cart = {'i15':['apple',500,20],'i16':['banana',20,10]}
        #detail_list = [['i15', 'apple', 500, 20], ['i16', 'banana', 20, 10]]
        detail_list = []
        #where_list = ['iid = i15','iid = i16']
        where_list = []
        #set_list = ['quantity = quantity - cart[j][2]']
        set_list = []
        for j in cart:
            val = [j]
            val.extend(cart[j])
            detail_list.append(val)
            where_list.append(f'iid = \'{j}\'')
            set_list.append(f'quantity = quantity - {cart[j][2]}')
        #update the inventory
        Database().update('item',set_list,where_list,mutiupdate=True)
        #add new order details to detail table
        Database().add('datail','oid, iid, price, quantity',detail_list,mutiadd=True)
        print(f'new order {newid} has been added and the cart has been cleaned up')
        #clean up cart
        cart = {}
    else:
        print('your cart is empty')
    return cart

def delete_item():
    print('please input the item id you want to delete:')
    itemid = input()
    if any(itemid):
        #delete an item with specific item id,whether it exists or not
        Database().delete('item','iid = \'' + itemid + '\'')
        print(f'item with id {itemid} has been deleted')
    else:
        print('invalid item id input')

def delete_shop():
    print('please input the shop id you want to delete:')
    shopid = input()
    if any(shopid):
        print('when the store is deleted, all its products will also be deleted!')
        print('please input "yes" to confirm the deletion:')
        if input() == 'yes':
            #delete a shop with specific shop id,whether it exists or not
            #数据库trigger，shop被删对应item表的shopiditem都被删
            Database().delete('shop','sid = \'' + shopid + '\'')
            print(f'shop with id {shopid} and all its items have been deleted')
        else:
            print('command canceled, no shop deleted')
    else:
        print('invalid shop id input')

def delete_cart(cart):
    if any(cart):
        show_cart(cart)
        print()
        print('please input the command number you want:')
        print("1: delete the entire shopping cart")
        print("2: delete some contents of the shopping cart")
        selection = input()
        if selection == '1':
            cart = {}
            print('your shopping cart has been completely deleted')
        if selection == '2':
            #cancel items from cart with specic item ids
            print('please input the item id(s) you want to delete from your shopping cart. ids should be separated by ","')
            #item_cancel = ['i15','i16'] or ['i15']
            item_cancel = input().replace(' ','')
            item_cancel = item_cancel.split(',')
            #cart = {'i15':[iname,price,quantity],'i16':[...,...]}
            delitem = []
            copycart = cart.copy()
            try:
                for i in item_cancel:
                    popdel = copycart.pop(i)
                    delitem.append(popdel[0])
                delitem = str(delitem).strip('[]')
                print(f'{delitem} have been deleted from shopping cart')
                cart = copycart.copy()
            except KeyError:
                print('some item id not found in shopping cart, nothing deleted')
        else:
            print('invalid command nunmber input, nothing deleted')
    else:
        print('your cart is empty')
    
    return cart

def delete_order(account_id):
    print('please input the order id you want to delete:')
    orderid = input()
    if any(orderid):
        #list order details and cancel some items of with specific order id
        result = Database().show('order','cid','oid = ' + orderid)
        if any(result):
            #if this order belongs to this account
            if account_id == result[0]:
                #oid存在则一定有detail内容
                result = Database().show('detail','iid, iname, price, quantity','oid = \'' + orderid + '\'')
                #result = [('i15','apple',1000,20),(...)]
                result_dict = {}
                #result_dict = {'i15':['apple',2000,35],'i16':[pen',1200,45],...}
                result_id = []
                for i in result:
                    result_dict[i[0]] = list(i)[1:]
                    result_id.append(i[0])
                print(f'this is your order {orderid} :')
                print()
                print('{:^20}{:^20}{:^20}{:^20}'.format('iid','iname','price','quantity'))
                for j in result_dict:
                    print('{:^20}{:^20}{:^20}{:^20}'.format(j,result_dict[j][0],result_dict[j][1],result_dict[j][2]))
                print()                
                print('please input the command number you want:')
                print("1: delete the entire order")
                print("2: delete some contents of the order")
                cancel_type = input()

                if cancel_type == '1':
                    #delete entire order
                    #where_list = ['iid = i15','iid = i16']
                    where_update_list = []
                    where_delete_list = []
                    #set_list = ['quantity = quantity + cart[j][2]']
                    set_list = []
                    for k in result_dict:
                        where_update_list.append(f'iid = {k}')
                        where_delete_list.append(f'iid = {k}' + ' AND oid = \'' + orderid + '\'')
                        set_list.append(f'quantity = quantity + {result_dict[k][2]}')
                    #cancel all order details
                    Database().delete('detail',where_delete_list,mutidel=True)
                    #cancel order in order talbe
                    Database().delete('order','oid = \'' + orderid + '\'')
                    #update corresponding items inventory
                    Database().update('item',set_list,where_update_list)
                    print(f'your order {orderid} has been completely deleted')

                elif cancel_type == '2':
                    #part delete
                    print('please input the item id(s) you want to delete from your order. ids should be separated by ","')
                    #item_cancel = ['i15','i16'] or ['i15']
                    item_cancel = input().replace(' ','')
                    item_cancel = item_cancel.split(',')
                    #check if there a empty input
                    if all(item_cancel):
                        item_cancel_set = set(item_cancel)
                        #check if there a duplicate input
                        if len(item_cancel_set) == len(item_cancel):
                            #check if there a input id not in thist order
                            if len(item_cancel_set) == len(item_cancel_set & set(result_id)):
                                #check id or ids
                                if len(item_cancel) == 1:
                                    #delete item from detail table with specific item id
                                    Database().delete('detail','iid = ' + item_cancel[0] + ' AND oid = \'' + orderid + '\'')
                                    #update corresponding item inventory
                                    Database().update('item','quantity = quantity + ' + str(result_dict[item_cancel[0]][2]),'iid = ' + item_cancel[0])
                                else:
                                    #delete items from detail table with specific item id list
                                    #where_list = ['iid = i15','iid = i16']
                                    where_update_list = []
                                    where_delete_list = []
                                    #set_list = ['quantity = quantity + cart[j][2]']
                                    set_list = []
                                    for k in item_cancel:
                                        where_update_list.append(f'iid = {k}')
                                        where_delete_list.append(f'iid = {k}' + ' AND oid = \'' + orderid + '\'')
                                        set_list.append(f'quantity = quantity + {result_dict[k][2]}')
                                    
                                    #delete items from detail table with specific item ids
                                    Database().delete('detail',where_delete_list,mutidel=True)
                                    alldel = False
                                    if item_cancel_set == set(result_id):
                                        #if all deleted,cancel order in order table
                                        Database().delete('order','oid = \'' + orderid + '\'')
                                        alldel = True
                                    #update corresponding items inventory
                                    Database().update('item',set_list,where_update_list,mutiupdate=True)
                                cancel = []
                                for i in item_cancel:
                                    cancel.append(result_dict[i][0])
                                cancel = str(cancel).strip('[]')
                                print(f'you have deleted {cancel} from your order')
                                if alldel:
                                    print('you have deleted all items in your order, your entire order has been deleted')
                            else:
                                print('command not executed: your input contains an id that does not exist in order')
                        else:    
                            print('command not executed: your input contains duplicate ids')
                    else:
                        print('command not executed: invalid input')
                else:
                    print('invalid command number input, nothing deleted')
            else:
                print('this is not your order, you cannot delete it')
        else:
            print('order id not found')
    else:
        print('invalid order id input')

# def parse(inp,account_id,cart):
#     inp_split = inp.split('.')

#     if len(inp_split) in [2,3] and all(inp_split[1:]):
#         if inp_split[0] == 'show':
#             # if inp_split[1] == 'item' and not any(inp_split[2:]):
#             #     #考虑取消
#             #     #show all items (100?) order by popular?
#             #     Commodity().commodity_show()
#             #输出模板先做好，参考cart
#             if inp_split[1] == 'shop':
#                 if any(inp_split[2:]):
#                     #show items with specific shop id
#                     #result = ((),)
#                     result = Database().show('item','iid,iname,price,quantity','sid = ' + inp_split[2])
#                     if any(result):
#                         #result = [['i15',12],[...,...]]
#                         result = [list(i) for i in result]
#                         print('{:^20}{:^20}{:^20}{:^20}'.format('iid','iname','price','quantity'))
#                         for i in result:
#                             print('{:^20}{:^20}{:^20}{:^20}'.format(i[0],i[1],i[2],i[3]))
#                     else:
#                         print('item not found')
                    
#                 else:
#                     #show all shop information
#                     result = Database().show('shop','*')
#                     if any(result):
#                         #result = [['i15',12],[...,...]]
#                         result = [list(i) for i in result]
#                         print('{:^20}{:^20}{:^20}{:^20}'.format('sid','sname','rating','location'))
#                         for i in result:
#                             print('{:^20}{:^20}{:^20}{:^20}'.format(i[0],i[1],i[2],i[3]))
#                     else:
#                         print('ERROR: no store exists')

#             elif inp_split[1] == 'cart' and not any(inp_split[2:]):
#                 #check if cart is empty
#                 if any(cart):
#                     #output the cart list
#                     print('{:^20}{:^20}{:^20}{:^20}'.format('iid','iname','price','quantity'))
#                     for i in cart:
#                         print('{:^20}{:^20}{:^20}{:^20}'.format(i,cart[i][0],cart[i][1],cart[i][2]))
#                 else:
#                     print('your cart is empty')

#             elif inp_split[1] == 'order':
#                 if any(inp_split[2:]):
#                     #check account_id first then show order details with specific order id
#                     #需要等数据库建好了测试一次，假设result = (('20132515'),)
#                     result = Database().show('order','cid','oid = ' + inp_split[2])
#                     if any(result):
#                         result = result[0]
#                         if result == account_id:
#                             result = Database().show('detail','iid,iname,price,quantity','oid = ' + inp_split[2])
#                             #cart转order有避免空order生成，这里默认一定有result
#                             #result = [['i15',12],[...,...]]
#                             result = [list(i) for i in result]
#                             print('{:^20}{:^20}{:^20}{:^20}'.format('iid','iname','price','quantity'))
#                             for i in result:
#                                 print('{:^20}{:^20}{:^20}{:^20}'.format(i[0],i[1],i[2],i[3]))
#                         else:
#                             print('this is not your order, you cannot view the detail')
#                     else:
#                         print('order does not exist')
#                 else:
#                     #show all order information belongs to current account
#                     result = Database().show('order','oid,date','iid = ' + account_id)
#                     if any(result):
#                         #result = [['i15',12],[...,...]]
#                         result = [list(i) for i in result]
#                         print('{:^20}{:^20}'.format('oid','date'))
#                         for i in result:
#                             print('{:^20}{:^20}'.format(i[0],i[1]))
#                     else:
#                         print('you dont have any orders')
                    
#         if inp_split[0] == 'add':
#             if inp_split[1] == 'item':
#                 if any(inp_split[2:]):
#                     #add a new item to a shop with specific shop id
#                     #check if shop exist
#                     result = Database().show('shop','sid','sid = ' + inp_split[2])
#                     #result = () or result = ((...),)
#                     if any(result):
#                         namelist = Database().show('item','iname','sid = ' + inp_split[2])
#                         #namelist = ['apple','banana']
#                         values = []
#                         print('please input the name of new item:')
#                         name = input()
#                         #check for duplicate names
#                         if name in namelist:
#                             print(f'{name} is already in the shop, do you want to add stock? type "yes" to continue')
#                             if input() == 'yes':
#                                 print('please enter the amount of stock that needs to be increased:')
#                                 num = input()
#                                 addstock = f'quantity = quantity + {num}'
#                                 Database().update('item',addstock,'iname = ' + name)
#                                 print(f'{name} inventory has increased by {num}')
#                             else:
#                                 print('command canceled')
#                         else:
#                             try:
#                                 #generate new id for the new item
#                                 #idlist = ['i15','i16']
#                                 idlist = Database().show('item','iid')
#                                 idlist.sort(key=sort_key,reverse=True)
#                                 #idlist = ['i16','i15']
#                                 pieces = re.compile(r'(\d+)').split(idlist[0])
#                                 newid = pieces[0]+ str(int(pieces[1])+1)
#                                 #set id
#                                 values.append(newid)
#                                 #set name
#                                 values.append(name)
#                                 print('please input the price of new item:')
#                                 #int?float?
#                                 #set price
#                                 values.append(int(input()))
#                                 print('please enter 1 to 3 keywords of the item new item:(multi-keyword should be separated by ",")')
#                                 keyword = input().split(',')
#                                 #check keyword validity
#                                 if keyword[:1] != [''] and len(keyword) in range(1,4):
#                                     while len(keyword)<3:
#                                         #null value in sql
#                                         keyword.append(None)
#                                     #set keywords
#                                     values.extend(keyword)
#                                 else:
#                                     print('invalid keyword input')
#                                     #必要return
#                                     return cart
#                                 print('please input the quantity of new item:')
#                                 #set quantity
#                                 values.append(int(input()))
#                             except ValueError:
#                                 print('invalid input')
#                                 #必要return
#                                 return cart
#                             #add new item to database
#                             Database().add('item','iid, iname, price, feature1, feature2, feature3, quantity, sid',values)
#                             print('new item has been added')

#                         # Commodity().commodity_add(inp_split[2])
#                     else:
#                         print('shop id not found')
#                 else:
#                     print('forget shop id')

#             elif inp_split[1] == 'shop' and not any(inp_split[2:]):
#                 namelsit = Database().show('shop','sname')
#                 values = []
#                 print('please input the name of new shop:')
#                 name = input()
#                 #check for duplicate names
#                 if name in namelsit:
#                     print(f'There is already a shop called {name}')
#                 else:
#                     try:
#                         #generate new id for the new shop
#                         idlist = Database().show('shop','sid')
#                         idlist.sort(key=sort_key,reverse=True)
#                         pieces = re.compile(r'(\d+)').split(idlist[0])
#                         newid = pieces[0]+ str(int(pieces[1])+1)
#                         #set id
#                         values.append(newid)
#                         #set name
#                         values.append(name)
#                         print('please input the rating of new shop:')
#                         #int?float?
#                         #set rating
#                         values.append(int(input()))
#                         print('please input the location of new shop:')
#                         #set location
#                         values.append(input())
#                         Database().add('shop','sid, sname, rating, location',values)
#                         print('new shop has been added')
#                     except ValueError:
#                         print('invalid input')


#             elif inp_split[1] == 'order' and not any(inp_split[2:]):
#                 #Generate shopping cart content as a new order, if done: clean up shopping cart
#                 #check if cart is empty
#                 if any(cart):
#                     #check if cart item unfound or invetory lack  
#                     lacklist = []
#                     unfoundlist = []
#                     #cart_item_id = ['i15','i22']
#                     cart_item_id = list(cart.keys())
#                     id_str = str(cart_item_id).strip('[]')
#                     #current_item = (('i15','apple',50,100),(...))
#                     current_item = Database().show('item','iid, iname, price, quantity',f'iid IN ({id_str})')
#                     #current_item = [['i15','apple',50,100],[...]]
#                     current_item = [list(i) for i in current_item]
#                     #current_dict = {'i15':20,'i16':30}
#                     current_dict = {}
#                     for i in current_item:
#                         current_item[i[0]] = i[3]
#                     #list(current_item.keys() = ['i15','i22']
#                     checkdiff,unfound = getDiff2(cart_item_id,list(current_item.keys()))
#                     for j in cart:
#                         if j in unfound:
#                             unfoundlist.append(cart[j][0])
#                             continue
#                         if cart[j][1] > current_dict[j]:
#                             lacklist.append(cart[j][0])
#                     #if any unfound or lack, order can not be add
#                     if checkdiff or any(lacklist):
#                         if checkdiff:
#                             unfoundlist = str(unfoundlist).strip('[]')
#                             print(f'{unfoundlist} may have been removed')
#                         if any(lacklist):
#                             lacklist = str(lacklist).strip('[]')
#                             print(f'inventory of {lacklist} cannot meet quantity demand')
#                         print('please modify your cart before adding order again')
#                         #必要return
#                         return cart
                    
#                     values = []
#                     #generate new id for the new order
#                     idlist = Database().show('order','oid')
#                     idlist.sort(key=sort_key,reverse=True)
#                     pieces = re.compile(r'(\d+)').split(idlist[0])
#                     newid = pieces[0]+ str(int(pieces[1])+1)
#                     #generate order information
#                     values.append(newid)
#                     values.append(account_id)
#                     #add order information to order table
#                     Database().add('order','oid, cid, date',values,date=True)
#                     #cart = {'i15':['apple',500,20],'i16':['banana',20,10]}
#                     #detail_list = [['i15', 'apple', 500, 20], ['i16', 'banana', 20, 10]]
#                     detail_list = []
#                     #where_list = ['iid = i15','iid = i16']
#                     where_list = []
#                     #set_list = ['quantity = quantity - cart[j][2]']
#                     set_list = []
#                     for j in cart:
#                         val = [j]
#                         val.extend(cart[j])
#                         detail_list.append(val)
#                         where_list.append(f'iid = {j}')
#                         set_list.append(f'quantity = quantity - {cart[j][2]}')
#                     #update the inventory
#                     Database().update('item',set_list,where_list,mutiupdate=True)
#                     #add new order details to detail table
#                     Database().add('datail','oid, iid, price, quantity',detail_list,mutiadd=True)
#                     print(f'new order {newid} has been added and the cart has been cleaned up')
#                     #clean up cart
#                     cart = {}
#                 else:
#                     print('your cart is empty')

#         if inp_split[0] == 'Delete':
#             #涉及插入，修改数值时要考虑好数据先验和对应trigger。add order还没写trigger
#             if inp_split[1] == 'item':
#                 if any(inp_split[2:]):
#                     #delete an item with specific item id,whether it exists or not
#                     Database().delete('item','iid = ' + inp_split[2:])
#                 else:
#                     print('forget item id')

#             elif inp_split[1] == 'shop':
#                 if any(inp_split[2:]):
#                     #delete a shop with specific shop id,whether it exists or not
#                     #数据库trigger，shop被删对应item表的shopiditem都被删
#                     Database().delete('shop','sid = ' + inp_split[2:])
#                 else:
#                     print('forget shop id')

#         if inp_split[0] == 'cancel':
#             if inp_split[1] == 'cart':
#                 if any(inp_split[2:]):
#                     #cancel a item from cart with specic item id
#                     #cart = {'i15':[iname,price,quantity],'i16':[...,...]}
#                     try:
#                         delitem = cart.pop(inp_split[2])
#                         print(f'{delitem} has been removed from shopping cart')
#                     except KeyError:
#                         print('item not found in shopping cart')
#                 else:
#                     print('Are you sure to clean up your cart? input "yes" for confrim')
#                     if input() == 'yes':
#                         #clean up cart
#                         cart = {}
#                     else:
#                         print('command not executed')

#             elif inp_split[1] == 'order':
#                 if any(inp_split[2:]):
#                     #list order details and cancel some items of with specific order id
#                     #做好了考虑应用回cancel cart,cart 那里留到cli优化再改，这里也是
#                     result = Database().show('order','cid','oid = ' + inp_split[2])
#                     if any(result):
#                         if account_id == result[0]:
#                             result = Database().show('detail','iid, iname, price, quantity','oid = ' + inp_split[2])
#                             result_dict = {}
#                             result_id = []
#                             for i in result:
#                                 result_dict[i[0]] = list(i)[1:]
#                                 result_id.append(i[0])
#                             #result_dict = {'i15':['apple',20,35],'i16':[pen',120,45]]
#                             print('{:^20}{:^20}{:^20}{:^20}'.format('iid','iname','price','quantity'))
#                             for j in result_dict:
#                                 print('{:^20}{:^20}{:^20}{:^20}'.format(j,result_dict[j][0],result_dict[j][1],result_dict[j][2]))
#                             print(f'this is your order {inp_split[2]}')
#                             print(f'do you want to cancel all or part of the order? 1:all 2:part')
#                             cancel_type = input()
#                             if cancel_type == '1':
#                                 #all cancel
#                                 #where_list = ['iid = i15','iid = i16']
#                                 where_update_list = []
#                                 where_delete_list = []
#                                 #set_list = ['quantity = quantity + cart[j][2]']
#                                 set_list = []
#                                 for k in result_dict:
#                                     where_update_list.append(f'iid = {k}')
#                                     where_delete_list.append(f'iid = {k}' + ' AND oid = ' + inp_split[2])
#                                     set_list.append(f'quantity = quantity + {result_dict[k][2]}')
#                                 #cancel all order details
#                                 Database().delete('detail',where_delete_list,mutidel=True)
#                                 #cancel order in order talbe
#                                 Database().delete('order','oid = ' + inp_split[2])
#                                 #update corresponding items inventory
#                                 Database().update('item',set_list,where_update_list)

#                             elif cancel_type == '2':
#                                 #part cancel
#                                 print('which item id(s) do you want to cancel? ids should be separated by ","')
#                                 #item_cancel = ['i15','i16'] or ['i15']
#                                 item_cancel = input().split(',')
#                                 #check if there a empty input
#                                 if all(item_cancel):
#                                     item_cancel_set = set(item_cancel)
#                                     #check if there a duplicate input
#                                     if len(item_cancel_set) == len(item_cancel):
#                                         #check if there a input id not in thist order
#                                         if len(item_cancel_set) == len(item_cancel_set & set(result_id)):
#                                             #check id or ids
#                                             if len(item_cancel) == 1:
#                                                 #delete item from detail table with specific item id
#                                                 Database().delete('detail','iid = ' + item_cancel[0] + ' AND oid = ' + inp_split[2])
#                                                 #update corresponding item inventory
#                                                 Database().update('item','quantity = quantity + ' + str(result_dict[item_cancel[0]][2]),'iid = ' + item_cancel[0])
#                                             else:
#                                                 #delete items from detail table with specific item id list
#                                                 #where_list = ['iid = i15','iid = i16']
#                                                 where_update_list = []
#                                                 where_delete_list = []
#                                                 #set_list = ['quantity = quantity + cart[j][2]']
#                                                 set_list = []
#                                                 for k in item_cancel:
#                                                     where_update_list.append(f'iid = {k}')
#                                                     where_delete_list.append(f'iid = {k}' + ' AND oid = ' + inp_split[2])
#                                                     set_list.append(f'quantity = quantity + {result_dict[k][2]}')
                                                
#                                                 #delete items from detail table with specific item ids
#                                                 Database().delete('detail',where_delete_list,mutidel=True)
#                                                 if item_cancel_set == set(result_id):
#                                                     #if all deleted,cancel order in order talbe
#                                                     Database().delete('order','oid = ' + inp_split[2])
#                                                 #update corresponding items inventory
#                                                 Database().update('item',set_list,where_update_list,mutiupdate=True)
#                                             cancel = []
#                                             for i in item_cancel:
#                                                 cancel.append(result_dict[i][0])
#                                             cancel = str(cancel).strip('[]')
#                                             print(f'you have cancelled {cancel} from your order')
#                                         else:
#                                             print('command not executed: your input contains an id that does not exist in order')
#                                     else:    
#                                         print('command not executed: your input contains duplicate ids')
#                                 else:
#                                     print('command not executed: invalid input')
#                             else:
#                                 print('command not executed:invalid input')
                            
#                         else:
#                             print('this is not your order, you cannot cancel it')
#                     else:
#                         print('order id not found')
#                 else:
#                     print('forget order id')

#         if inp_split[0] == 'purchase':
#             #purchase an item with specific item id
#             #cart = {'i15':['apple',500,20],'i16':['banana',20,10]}
#             print('please input the item id that you want to purchase')
#             itemid = input()
#             result = Database().show('item','iid,iname,price,quantity','iid = ' + itemid)
#             if any(result):
#                 #result = ['i15','apple',500,20]
#                 result = list(result[0])
#                 #output the item information
#                 print('item found:')
#                 print('{:^20}{:^20}{:^20}{:^20}'.format('iid','iname','price','quantity'))
#                 print('{:^20}{:^20}{:^20}{:^20}'.format(result[0],result[1],result[2],result[3]))
#                 print('please enter the quantity you want to buy')
#                 try:
#                     itemnum = int(input())
#                     if itemnum > 0 and itemnum <= result[3]:
#                         if itemid in list(cart.keys()):
#                             #cart already have this item
#                             cart[itemid][2] = cart[itemid][2] + itemnum
#                             cart[itemid][1] = cart[itemid][1] + itemnum*cart[itemid][1]
#                         else:
#                             #add new item to cart
#                             result[2] = result[2]*itemnum
#                             cart[itemid] = result[1:]
#                         print(f'you have successfully purchased {itemnum} {result[1]} to the shopping cart')
#                     else:
#                         print('invalid quantity input')
#                 except ValueError:
#                     print('invalid quantity input')
#             else:
#                 print('item id not found')

#         if inp_split[0] == 'search':
#             print('Which search mode do you want to choose? 1:keyword of item 2:name of item')
#             smode = input()
#             if smode == '1':
#                 #search items with specific key
#                 print('please enter item keyword')
#                 itemkey = input()
#                 if any(itemkey):
#                     wherekey = 'feature1 = \'' + itemkey + '\' OR feature2 = \'' + itemkey + '\' OR feature3 = \'' + itemkey + '\''
#                     result = Database().show('item','iid,iname,price,quantity',wherekey)
#                     if any(result):
#                         #result =[[]]
#                         result = [list(i) for i in result]
#                         print(f'The following(s) is item with keyword {itemkey}:')
#                         print('{:^20}{:^20}{:^20}{:^20}'.format('iid','iname','price','quantity'))
#                         for i in result:
#                             print('{:^20}{:^20}{:^20}{:^20}'.format(result[0][0],result[0][1],result[0][2],result[0][3]))
#                     else:
#                         print('item not found')
#                 else:
#                     print('command not executed:invalid keyword input')

#             elif smode == '2':
#                 #search items with specific name
#                 print('please enter item name')
#                 itemname = input()
#                 if any(itemname):
#                     result = Database().show('item','iid,iname,price,quantity','iname = \'' + itemname + '\'')
#                     if any(result):
#                         #result =[[]]
#                         result = [list(i) for i in result]
#                         print(f'The following(s) is item named {itemname}:')
#                         print('{:^20}{:^20}{:^20}{:^20}'.format('iid','iname','price','quantity'))
#                         for i in result:
#                             print('{:^20}{:^20}{:^20}{:^20}'.format(result[0][0],result[0][1],result[0][2],result[0][3]))
#                     else:
#                         print('item not found')
#                 else:
#                     print('command not executed:invalid name input')
#             else:
#                 print('command not executed:invalid mode input')

#         return cart

#     else:
#         print("unsupported operation")
#         return cart