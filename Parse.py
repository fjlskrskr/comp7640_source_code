from database import Database
import re

def sort_key(s):
    #sort_strings_with_embedded_numbers
    re_digits = re.compile(r'(\d+)')
    pieces = re_digits.split(s)  # num and no num
    pieces[1::2] = map(int, pieces[1::2])  # turn num to integer
    return pieces

def getDiff2(arr1,arr2):
    #get different between two sets
    set_1 = ()
    set_2 = ()
    set_1 = set(arr1)
    set_2 = set(arr2)
    set_more1 = ()
    set_1_2 = set_1 & set_2
    set_more1 = set_1 -set_1_2
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
    #login account
    print('Please input your account id:')
    account = input()
    result = []
    if any(account):
        #get account's password for check
        result = Database().show('customer','password','cid = \'' + account + '\'')
    if any(result):
        print('Please input your password:')
        if input() == result[0][0]:
            print('Login success')
            stat = 1
            return stat,account
        else:
            print('Wrong password')
    else:
        print('account not found')
    account = []
    return stat,account

def register():
    #register account
    print('Please input the account id you want to register:')
    account = input()
    if any(account):
        #get something if account exist
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
                #valid information input can be added as new account
                Database().add('customer','cid,tel,address,password',val)
                print('Register success')
            else:
                print('Register fail: invalid empty input')
        else:
            print('Register fail: This account id has already been registered')
    else:
        print('Register fail: invalid account id input')

def search():
    #search item
    print('which search mode do you want to choose?')
    print("1: search items with specific key")
    print("2: search items with specific name")
    smode = input()

    #search items with specific key
    if smode == '1':  
        print('please input single item keyword:')
        itemkey = input()
        if any(itemkey):
            wherekey = 'feature1 = \'' + itemkey + '\' OR feature2 = \'' + itemkey + '\' OR feature3 = \'' + itemkey + '\''
            #get item search result
            result = Database().show('item','iid,iname,price,item_quantity',wherekey)
            if any(result):
                result = [list(i) for i in result]
                print(f'The following(s) is item with keyword {itemkey}:')
                print('{:^20}{:^20}{:^20}{:^20}'.format('iid','iname','price','quantity'))
                for i in result:
                    print('{:^20}{:^20}{:^20}{:^20}'.format(i[0],i[1],i[2],i[3]))
            else:
                print('item not found')
        else:
            print('invalid keyword input')

    #search items with specific name
    elif smode == '2':
        print('please input item name')
        itemname = input()
        if any(itemname):
            #get item search result
            result = Database().show('item','iid,iname,price,item_quantity','iname = \'' + itemname + '\'')
            if any(result):
                result = [list(i) for i in result]
                print(result)
                print(f'The following(s) is item named {itemname}:')
                print('{:^20}{:^20}{:^20}{:^20}'.format('iid','iname','price','quantity'))
                for i in result:
                    print('{:^20}{:^20}{:^20}{:^20}'.format(i[0],i[1],i[2],i[3]))
            else:
                print('item not found')
        else:
            print('command not executed:invalid name input')
    else:
        print('invalid mode selection')

def purchase(cart):
    #purchase an item with specific item id
    print('please input the item id you want to purchase:')
    itemid = input()
    result = []
    if any(itemid):
        #get item information if exist
        result = Database().show('item','iid,iname,price,item_quantity','iid = \'' + itemid + '\'')
    if any(result):
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
                    cart[itemid][1] = cart[itemid][1] + result[2]*itemnum
                else:
                    #add new item to cart
                    result[2] = result[2]*itemnum
                    result[3] = itemnum
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
        #get shop's items if exist
        result = Database().show('item','iid,iname,price,item_quantity','sid = \'' + shopid + '\'')
    if any(result):
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
        result = Database().show('orderinfo','oid,date','cid = \'' + account_id + '\'')
        if any(result):
            print('here are all the order(s) you have:')
            result = [list(i) for i in result]
            print('{:^20}{:^20}'.format('oid','date'))
            for i in result:
                print('{:^20}{:^20}'.format(i[0],str(i[1])))
        else:
            print('you dont have any orders')

    elif selection == '2':
        #check account_id first then show order details with specific order id
        print('please input the order id you want to show details:')
        orderid = input()
        result = []
        if any(orderid):
            result = Database().show('orderinfo','cid','oid = \'' + orderid + '\'')
        if any(result):
            result = result[0][0]
            if result == account_id:
                #get details of the order,no empty result here
                result = Database().show('detail','iid,iname,price,order_quantity','oid = \'' + orderid + '\'')       
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
    #add a new item to a shop with specific shop id
    print('please input the shop id of the item you want to add:')
    shopid = input()
    result = []
    if any(shopid):
        #check if shop exist
        result = Database().show('shop','sid','sid = \'' + shopid + '\'')
    if any(result):
        #get item name list of the shop
        namelist = Database().show('item','iname','sid = \'' + shopid + '\'')
        namelist = [i[0] for i in namelist]
        values = []
        print('please input the name of new item:')
        name = input()
        #check for duplicate names
        if name in namelist:
            print(f'{name} is already in the shop, do you want to add stock? input "yes" to continue')
            if input() == 'yes':
                print('please enter the amount of stock that needs to be increased:')
                num = input()
                addstock = f'item_quantity = item_quantity + {num}'
                #update corresponding item's stock
                Database().update('item',addstock,'iname = \'' + name + '\'' + ' AND sid = \'' + shopid + '\'')
                print(f'inventory of {name} has increased by {num}')
            else:
                print('command canceled, no item added')
        else:
            try:
                #generate new id for the new item
                idlist = Database().show('item','iid')
                idlist = [i[0] for i in idlist]
                idlist.sort(key=sort_key,reverse=True)
                pieces = re.compile(r'(\d+)').split(idlist[0])
                newid = pieces[0]+ str(int(pieces[1])+1)
                #set new id
                values.append(newid)
                #set new name
                values.append(name)
                print('please input the price(integer) of new item:')
                #set new price
                values.append(int(input()))
                print('please enter 1 to 3 keywords of the item new item:(multi-keyword should be separated by ",")')
                keyword = input().replace(' ','')
                keyword = keyword.split(',')
                #check keyword validity
                if all(keyword) and len(keyword) in range(1,4):
                    while len(keyword)<3:
                        #replace with NULL if keyword <3
                        keyword.append('NULL')
                    #set new keywords
                    values.extend(keyword)
                else:
                    print('invalid keyword input, no item added')
                    return
                    
                print('please input the quantity(integer) of new item:')
                #set new quantity
                values.append(int(input()))
                #set sid
                values.append(shopid)
                #if all setting valid,add new item to database
                Database().add('item','iid, iname, price, feature1, feature2, feature3, item_quantity, sid',values)
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
        #get all exist shops' names
        namelsit = Database().show('shop','sname')
        namelsit = [i[0] for i in namelsit]
        #check for duplicate names
        if name in namelsit:
            print(f'There is already a shop called {name}')
        else:
            try:
                values = []
                #generate new id for the new shop
                idlist = Database().show('shop','sid')
                idlist = [i[0] for i in idlist]
                idlist.sort(key=sort_key,reverse=True)
                pieces = re.compile(r'(\d+)').split(idlist[0])
                newid = pieces[0]+ str(int(pieces[1])+1)
                #set new id
                values.append(newid)
                #set new name
                values.append(name)
                print('please input the rating(integer) from 0 to 5 of new shop:')
                #set new rating
                rate = int(input())
                if rate<0 or rate >5:
                    raise ValueError
                values.append(rate)
                print('please input the location of new shop:')
                #set new location
                values.append(input())
                #if all setting valid,add new item to database
                Database().add('shop','sid, sname, rating, location',values)
                print(f'new shop has been added, Its assigned id is: {newid}')
            except ValueError:
                print('invalid numeric input')
    else:
        print('invalid name input')

def add_order(cart:dict,account_id):
    #Generate shopping cart content as a new order, if done: clean up shopping cart
    print('you are adding your shopping cart as a new order, press enter to continue')
    input()  
    if any(cart):
        #check if cart item unfound or invetory lack  
        lacklist = []
        unfoundlist = []
        cart_item_id = list(cart.keys())
        id_str = str(cart_item_id).strip('[]')
        #get information of items in cart
        current_item = Database().show('item','iid, iname, price, item_quantity',f'iid IN ({id_str})')
        current_item = [list(i) for i in current_item]
        current_dict = {}
        for i in current_item:
            current_dict[i[0]] = i[3]
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
            return cart
        #if all item in cart valid
        values = []
        #generate new id for the new order
        idlist = Database().show('orderinfo','oid')
        idlist = [i[0] for i in idlist]
        idlist.sort(key=sort_key,reverse=True)
        pieces = re.compile(r'(\d+)').split(idlist[0])
        newid = pieces[0]+ str(int(pieces[1])+1)
        #generate order information
        values.append(newid)
        values.append(account_id)
        #add order information to order table
        Database().add('orderinfo','oid, cid, date',values,date=True)
        detail_list = []
        where_list = []
        set_list = []
        for j in cart:
            val = [newid]
            val.append(j)
            val.extend(cart[j])
            detail_list.append(val)
            where_list.append(f'iid = \'{j}\'')
            set_list.append(f'item_quantity = item_quantity - {cart[j][2]}')
        #trigger will update the inventory
        #add new order details to detail table
        Database().add('detail','oid, iid, iname, price, order_quantity',detail_list,mutiadd=True)
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
            Database().delete('shop','sid = \'' + shopid + '\'')
            #affter deletion, shop's item with be cascade deleted
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
            #clean up cart
            cart = {}
            print('your shopping cart has been completely deleted')
        if selection == '2':
            #cancel items from cart with specic item ids
            print('please input the item id(s) you want to delete from your shopping cart. ids should be separated by ","')
            item_cancel = input().replace(' ','')
            item_cancel = item_cancel.split(',')
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
    #list order details and cancel some items of with specific order id
    print('please input the order id you want to delete:')
    orderid = input()
    if any(orderid):
        #check if order id exist
        result = Database().show('orderinfo','cid','oid = \'' + orderid + '\'')
        if any(result):
            #check if this order belongs to this account
            if account_id == result[0][0]:
                #get details of this order
                result = Database().show('detail','iid, iname, price, order_quantity','oid = \'' + orderid + '\'')
                result_dict = {}
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
                    where_update_list = []
                    set_list = []
                    for k in result_dict:
                        where_update_list.append(f'iid = \'{k}\'')
                        set_list.append(f'item_quantity = item_quantity + {result_dict[k][2]}')
                    #cancel order in orderinfo talbe
                    Database().delete('orderinfo','oid = \'' + orderid + '\'')
                    #affter deletion, details will be cascade deleted
                    #update corresponding items inventory
                    Database().update('item',set_list,where_update_list,mutiupdate=True)
                    print(f'your order {orderid} has been completely deleted')

                elif cancel_type == '2':
                    #part delete
                    print('please input the item id(s) you want to delete from your order. ids should be separated by ","')
                    item_cancel = input().replace(' ','')
                    item_cancel = item_cancel.split(',')
                    #check if there a empty input
                    if all(item_cancel):
                        item_cancel_set = set(item_cancel)
                        #check if there a duplicate input
                        if len(item_cancel_set) == len(item_cancel):
                            #check if there a input id not in thist order
                            if len(item_cancel_set) == len(item_cancel_set & set(result_id)):
                                where_update_list = []
                                where_delete_list = []
                                set_list = []
                                for k in item_cancel:
                                    where_update_list.append(f'iid = \'{k}\'')
                                    where_delete_list.append(f'iid = \'{k}\'' + ' AND oid = \'' + orderid + '\'')
                                    set_list.append(f'item_quantity = item_quantity + {result_dict[k][2]}')
                                #if acctually deleting all details,cancel order in order table
                                if item_cancel_set == set(result_id):
                                    Database().delete('orderinfo','oid = \'' + orderid + '\'')
                                    #after deletion, details will be cascade deleted
                                    Database().update('item',set_list,where_update_list,mutiupdate=True)
                                    print('you have deleted all items in your order, your entire order has been deleted')
                                    return
                                #delete items from detail table with specific item ids
                                Database().delete('detail',where_delete_list,mutidel=True)
                                #trigger will update items stock
                                cancel = []
                                for i in item_cancel:
                                    cancel.append(result_dict[i][0])
                                cancel = str(cancel).strip('[]')
                                print(f'you have deleted {cancel} from your order')
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