from sys import argv

def main():
    if len(argv) != 2:
        raise Exception("File path not entered")
    #getting file path
    file_path = argv[1]
    #opening the file to read its content
    f = open(file_path, 'r')
    #separating the read lines of the file into a list
    lines = f.readlines()
    for line in lines:
        #removing \n character added to last word of each line
        line=line.replace('\n','')
        #splitting the words of each line based on space between them and save it into a list
        line=line.split(' ')
        #the first word of each line is assumed to be a command hence callling a method for each command
        if(line[0]=='BALANCE'):
            #initialise card balance
            init_card_balance(line[1],line[2])
        elif(line[0]=='CHECK_IN'):
            #check in passenger
            check_in(line[1],line[2],line[3])
        elif(line[0]=='PRINT_SUMMARY'):
            print_summary()
        else:
            #if some other command is inputed from console then throw error
            raise Exception('Wrong inout parameter is passed')

def init_card_balance(card_number,amount):
    """
    PARAMS
    ------
    card_number: card id or unique identification number of the card
    amount: amount which is present initially in the card

    DESCRIPTION
    -----------
    this method adds balance of a card against its number
    """
    #aading card number and amount in the card balance dictionary
    CARD_BALANCE[card_number]=int(amount)

def check_in(card_number,passenger_type,station):
    """
    PARAMS
    ------
    card_number: card id or unique identification number of the card
    passenger_type: type of passenger either ADULT, KID or SENIOR_CITIZEN
    station: station in which check in happens

    DESCRIPTION:
    -----------
    it calculates the total fare dedcuted during check-in, updates the card balance
    and then updates or create new entry of  STATION_TRANSACTION and STATION_PASSENGERS dictionary
    """
    discount=0
    #discount rate is 50% of the fare if it is a round trip
    discount_rate=0.5
    #get fare according to passenger type
    fare=get_fare(passenger_type)
    #find whether it is a round or not. If round trip then updates the fare and discount
    if is_round_trip(card_number,station):
        #if it is a round trip then charge only 50% of the fee for that trip
        fare=int(fare*discount_rate)
        discount=fare
    #find total charges which includes total fare and service charge, which can be applied if card is auto recharged
    total_charges=fare+find_service_charge(fare,card_number)
    #find balance after check in
    balance=CARD_BALANCE[card_number]-total_charges
    #update new balance in card
    CARD_BALANCE[card_number]=balance

    #updates station transaction which contains an entry of total charges and total discount happens for a station
    if STATION_TRANSACTION.get(station):
        updated_charges=STATION_TRANSACTION[station][0]+total_charges
        updated_discount=STATION_TRANSACTION[station][1]+discount
        STATION_TRANSACTION[station]=(updated_charges,updated_discount)
    else:
        STATION_TRANSACTION[station]=(total_charges,discount)

    #updates station passengers which contains an entry of passenger type and its number of check-ins for same station
    if STATION_PASSENGERS.get(station):
        if STATION_PASSENGERS[station].get(passenger_type):
            STATION_PASSENGERS[station][passenger_type]+=1
        else:
            STATION_PASSENGERS[station][passenger_type]=1
    else:
        STATION_PASSENGERS[station]={passenger_type:1}

def print_summary():
    print(f"TOTAL_COLLECTION CENTRAL {STATION_TRANSACTION['CENTRAL'][0]} {STATION_TRANSACTION['CENTRAL'][1]}")
    print('PASSENGER_TYPE_SUMMARY')
    passengers=sorted(STATION_PASSENGERS['CENTRAL'].items(),key=lambda x:(x[0],x[1]))
    for passenger in passengers:
        print(passenger[0]+' '+str(passenger[1]))
    print(f"TOTAL_COLLECTION AIRPORT {STATION_TRANSACTION['AIRPORT'][0]} {STATION_TRANSACTION['AIRPORT'][1]}")
    print('PASSENGER_TYPE_SUMMARY')
    passengers=sorted(STATION_PASSENGERS['AIRPORT'].items(),key=lambda x:(x[0],x[1]))
    for passenger in passengers:
        print(passenger[0]+' '+str(passenger[1]))

def is_round_trip(card_number,station):
    """
    PARAMS
    ------
    card_number: card id or unique identification number of the card
    station: station in which check in happens

    DESCRIPTION:
    -----------
    It finds whether a trip is round trip based on whether same card number has different station entry in CARD_CHECK_IN dict
    """
    #if there is no key in CARD_CHECK_IN dict for the specific card number then creates a new entry
    if CARD_CHECK_IN.get(card_number):
        #if station defines in the CARD_CHECK_IN dict is different than current station,
        # then it means that it is a round trip
        if CARD_CHECK_IN[card_number]!=station:
            #pop previous saved data as for this data round trip is already counted
            CARD_CHECK_IN.pop(card_number)
            return True
    else:
        #update check in detail in the card
        CARD_CHECK_IN[card_number]=station
    return False

def get_fare(passenger_type):
    return CHARGES[passenger_type]

def find_service_charge(fare,card_number):
    """
    PARAM:
    -----
    fare: charge deducted for check in
    card_number: card id or unique identification number of the card

    DESCRIPTION
    -----------
    returns the service charge applicable for the transaction based on the balance
    of the card"""
    service_charge=0
    #deduct 2 % service charge for auto recharge of code
    service_charge_rate=0.02
    #if the balance of card is low than fare , then 2 % of the difference amount is to be taken
    if CARD_BALANCE[card_number]<fare:
        service_charge=(fare-CARD_BALANCE[card_number])*service_charge_rate
        #updates new balance in the card after auto recharge
        CARD_BALANCE[card_number]=fare
    return int(service_charge)

#dictionary which holds the card number as key and its balance as value
#structure: {'MC1': '400'}
CARD_BALANCE={}

#dictionary which holds the card number as key and checked in station as value
#structure: {'MC1': 'AIRPORT'}
CARD_CHECK_IN={}

#dictionary which holds the station as key and total charges and discount as values
#structure:{'CENTRAL':(457,50)}
STATION_TRANSACTION={}

#dictionary which holds data of station against its passenger type and number of check-in's into that station
#structure:{'AIRPORT':{'ADULT':1}}
STATION_PASSENGERS={}

#contains fare against passenger_type
CHARGES={
    'ADULT':200,
    'SENIOR_CITIZEN':100,
    'KID':50
}

if __name__ == "__main__":
    main()