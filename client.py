import requests, json
HEADER = "http://127.0.0.1:5000"

def get_all_flights():
    get_request = requests.get(HEADER + f'/dbInfo')
    response = get_request.text
    jsons = json.loads(response)
    
    string_to_return = ""

    for flight in jsons:
        flight_string = f"ID: {flight['id']}, From: {flight['city_from']}, To:{flight['city_to']}, Departure: {flight['departure']}, Arrival: {flight['arrival']}, Airplane: {flight['airplane']}, Passenger Number: {flight['passenger_number']}"
        string_to_return += flight_string+'\n'

    return string_to_return

def user_get_from_to(from_c, to_c):
    get_request = requests.get(HEADER + f'/flights/{from_c}/{to_c}')
    response = get_request.text
    jsons = json.loads(response)
    
    string_to_return = ""

    for flight in jsons:
        flight_string = f"From: {flight['city_from']}, To:{flight['city_to']}, Departure: {flight['departure']}, Arrival: {flight['arrival']}, Airplane: {flight['airplane']}, Passenger Number: {flight['passenger_number']}"
        string_to_return += flight_string+'\n'

    return string_to_return

def check_login(admin_email, admin_password):
    login_response = requests.post(HEADER + f"/authentication_authorization", {'email': admin_email, 'password': admin_password})
    token = login_response.text
    json_token = json.loads(token)
    return json_token

def add_to_db(fr, to, t1, t2, a_info, p_num, token):
    add_response = requests.post(HEADER + f"/flights", {'token': token, 'fromm': fr, 'to': to, 't1': t1, 't2': t2, 'a_info': a_info, 'p_num': p_num})

def delete_from_db(id, token):
    delete_response = requests.delete(HEADER + f"/flights", data={'token': token, 'id': id})

def update_db(id, fromCity, toCity, time1, time2, airplaneInfo, passengerNumber, token):
    put_response = requests.put(HEADER + f"/flights", data={'id': id, 'fromC': fromCity, "toC": toCity, "time1": time1, "time2": time2, "aInfo": airplaneInfo, "psngrNum": passengerNumber, 'token': token})

def end_session(token):
    delete_response = requests.delete(HEADER + f"/end_session", data={'token': token})

def main():
    while True:
        person=input('Role (user or admin): ')

        if person=="user":
            print('')
            print("User can make a GET request to http://127.0.0.1:5000/flights/<city_from>/<city_to>")
            print('')
            city_from = input("city_from: ")
            city_to = input("city_to: ")
            output = user_get_from_to(city_from, city_to)
            print('\nResults:')
            print(output)
        elif person=="admin":
            print('')
            email = input('Email: ')
            password = input('Password: ')
            
            tokenn = check_login(email, password)
            token = tokenn[0]['token']
            
            if(tokenn[0]['token'] != ''):
                #login is successful

                print()
                print('Original DB:\n')
                original_db = get_all_flights()
                print(original_db)

                print()
                print("-"*18)
                print('ADMIN OPTIONS:\n')
                print('*** please, enter flight data without spaces. For example: NOT "June 18, 08:00am", type "June_18,_08:00am"\n')
                print('1. POST <city_from> <city_to> <departure_time> <arrival_time> <airplane> <passenger_number>\n')
                print('2. DELETE <flight_id>\n')
                print('3. PUT <flight_id>\n')
                print('4. END_SESSION\n')
                print("-"*18)

                while True:
                    option = int(input('Which option would you like to use? '))
                    if(option == 1):
                        #POST Mexico Baku may_15,09:00am may_15,23:59pm airplane_5 566
                        command, fr, to, t1, t2, a_info, p_num = map(str, input('Type command: ').split())
                        add_to_db(fr, to, t1, t2, a_info, p_num, token)

                        print('\nDB after POST request:\n')
                        added_db = get_all_flights()
                        print(added_db)

                    elif(option == 2):
                        command, id = map(str, input('Type command: ').split())
                        delete_from_db(id, token)

                        print('\nDB after DELETE request:\n')
                        deleted_db = get_all_flights()
                        print(deleted_db)

                    elif(option == 3):
                        command, id = map(str, input('Type command: ').split())
                        print('')
                        fromCity = input('new city_from: ')
                        toCity = input('new city_to: ')
                        time1 = input('new departure_time: ')
                        time2 = input('new arrival_time: ')
                        airplaneInfo = input('new airplane_info: ')
                        passengerNumber = input('new passengerNumber: ')
                        update_db(id, fromCity, toCity, time1, time2, airplaneInfo, passengerNumber, token)

                        print('\nDB after PUT request:\n')
                        updated_dbb = get_all_flights()
                        print(updated_dbb)

                    elif(option == 4):
                        command = input('Type command: ')
                        end_session(token)
                        token=''
                        print(token)
                        break
            else:
                #login failed
                print('>>>>>> invlaid credentials !!!\n')
            

if __name__=="__main__":
    main()