from sys import argv
from src.buying_controller import BuyingController
from src.programme import Programme
def main():
    if len(argv) != 2:
        raise Exception("File path not entered")
    file_path = argv[1]
    f = open(file_path, 'r')
    commands = f.readlines()
    transaction=BuyingController()
    for command in commands:
        command=command.replace('\n','')
        command=command.split(' ')
        if command[0]=='ADD_PROGRAMME':
            programme_name=command[1].lower()
            programme_qty=int(command[2])
            p1=Programme(programme_name,programme_qty)
            transaction.add_programme(p1)
        elif command[0]=='APPLY_COUPON':
            coupon_name=command[1]
            transaction.add_coupon(coupon_name)
        elif command[0]=='ADD_PRO_MEMBERSHIP':
            transaction.add_pro_membership()
        elif command[0]=='PRINT_BILL':
            transaction.print_bill()
        else:
            raise Exception('Wrong command is entered')

if __name__ == "__main__":
    main()