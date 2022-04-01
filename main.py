from Parse import *

def main():
    #Operation permission status (1:command mode; 0:login mode)
    status = 1
    #account id
    current_account = []
    shopping_cart = {}
    while 1:
        if status == 1:
            #该部分已完成，只等数据库做好再进行调整
            commandmenu(current_account)
            selection = input()
            print()
            #传递shopping_cart，current_account，接收shopping_cart
            #search item
            if selection == '1':
                search()
                print()
                input("Please press enter to continue")
            #purchase item
            elif selection == '2':
                shopping_cart = purchase(shopping_cart)
                print()
                input("Please press enter to continue")
            #show interface
            elif selection == '3':
                while 1:
                    showmenu()
                    showselection = input()
                    print()
                    if showselection == '1':
                        #show shop's item
                        show_item()
                    elif showselection == '2':
                        #show shop information
                        show_shop()
                    elif showselection == '3':
                        #show cart
                        show_cart(shopping_cart)
                    elif showselection == '4':
                        #show order
                        show_order(current_account)
                    elif showselection == '0':
                        #back to main menu
                        break
                    else:
                        print('invalid input')
                    print()
                    input("Please press enter to continue")         
            #add interface
            elif selection == '4':
                while 1:
                    addmenu()
                    addselection = input()
                    print()
                    if addselection == '1':
                        #add a new tiem
                        add_item()
                    elif addselection == '2':
                        #add a new shop
                        add_shop()
                    elif addselection == '3':
                        #add cart as order
                        shopping_cart = add_order(shopping_cart,current_account)
                    elif addselection == '0':
                        #back to main menu
                        break
                    else:
                        print('invalid input')
                    print()
                    input("Please press enter to continue")    
            #delete interface
            elif selection == '5':
                while 1:
                    deletemenu()
                    deleteselection = input()
                    print()
                    if deleteselection == '1':
                        #delete a item
                        delete_item()
                    elif deleteselection == '2':
                        #delete a shop
                        delete_shop()
                    elif deleteselection == '3':
                        #delete cart
                        shopping_cart = delete_cart(shopping_cart)
                    elif deleteselection == '4':
                        #delete order
                        delete_order(current_account)
                    elif deleteselection == '0':
                        #back to main menu
                        break
                    else:
                        print('invalid input')
                    print()
                    input("Please press enter to continue")    
            #exit
            elif selection == '0':
                break
            else:
                print('invalid input')
                print()
                input("Please press enter to continue")

        elif status == 0:
            #该部分已完成，只等数据库做好再进行调整
            loginmenu()
            selection = input()
            print()
            #login
            if selection == '1':
                status,current_account = login(status)     
            #register
            elif selection == '2':
                register()
            #exit
            elif selection == '0':
                break
            else:
                print('invalid input')   
            print()
            input("Please press enter to continue")

if __name__ == '__main__':
    main()