import datetime #used to print current time at line 241
import mysql.connector as m
db = "movies" #name of database
food_menu = "food_menu" #name of table containing food menu
users = "users" #name of table containing users
movies = "movies" #name of table containing movies
bookings = "bookings" #name of table containg bookings

con = m.connect(host = "localhost",user="root",password="@Te3{oHgq$#B|h~pm[",database = db)
if con.is_connected:
    print("successfully connected")
else:
    print("WARNING!: not connected")

mycursor = con.cursor()

def register():
    while True:
        username = input("Enter your new username: ")
        if username == "quit":
            print("quitting......")
            break

        is_user_in_db = f"select * from {users} where username =  '{username}'"
        mycursor.execute(is_user_in_db)
        data = mycursor.fetchall()
        if data != []:
            print("username taken")
            continue
        password = input("Enter your new password: ")
        if password == "quit":
            print("quitting......")
            break
        confirm_password = input("retype your password to confirm it: ")
        if confirm_password == "quit":
            print("quitting......")
            break
        if password != confirm_password:
            print("passwords do no match")
            continue
        newuser = f"insert into {users} values('{username}','{password}','user','{None}','{None}')"
        mycursor.execute(newuser) #executes newuser, tha
        con.commit() #Makes sure the changes gets stored in users table. Without this line the new user information will not be permanently stored in users table.
        print(f"Sucessfully registered {username}")
        break

def employee_menu():
    print("Welcome, employee!")
    while True:
        print("─" * 90)
        print("1. View All Bookings")
        print("2. Manage Movies")
        print("3. Log Out")
        print("─" * 90)
        choice = input("Enter your choice (1-3): ")
        if choice == "1":
            view_all_bookings()
        elif choice == "2":
            manage_movies()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

def view_all_bookings():
    sql = f"select * from {bookings}"
    mycursor.execute(sql)
    data = mycursor.fetchall()
    print(data)

def manage_movies():
    while True:
        print("─" * 90)
        print("1. View movies")
        print("2. Add Movies")
        print("3. Remove Movie")
        print("4. Update Movie")
        print("5. Go Back")
        print("─" * 90)
        choice = input("Enter your choice (1-5): ")
        if choice == "1":
            display_movies()
        elif choice == "2":
            add_movie()
        elif choice == "3":
            display_movies()
            cancel(movies,'movie')
        elif choice == "4":
            update_movie()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

def display_movies():
    print("─" * 90)
    print("Welcome to the WYDEOS! A movie booking website")
    print("─" * 90)
    count_movies = count(movies)
    for z in range(0,count_movies):
       sql = f"select * from {movies} having movie_index = {z+1}"
       mycursor.execute(sql)
       data = mycursor.fetchall()
       print(f"{z+1}) title: {data[0][0]}, genre:{data[0][1]},director:{data[0][2]},seats_available:{data[0][3]}")

def count(database):
    sql = f"select count(*) from {database}"
    mycursor.execute(sql)
    data = mycursor.fetchone()[0]
    return data

def add_movie():
    while True:
        choice_title = input("Enter movie title: ")
        if choice_title.lower() == "quit":
            break
    
        choice_genre = input("Enter movie genre: ")
        if choice_genre.lower() == "quit":
            break

        choice_director = input("Enter movie director: ")
        if choice_director.lower() == "quit":
            break
        break
    while True:
        try:
            if choice_title == "quit" or choice_genre == "quit" or choice_director == "quit":
                break

            choice_seats = input("enter number of seats available: ")
            if choice_seats.lower() == "quit":
                break
            choice_seats = int(choice_seats) #sql database stores seats as int datatype in movies table. If the user does not provide a number this will throw ValueError: invalid literal for int() with base 10:
        except:
            print("Error: you did not type a number")
            continue

        choice_movie_index = count(movies) + 1

        new_movie = f"insert into {movies} (title, genre, director,seats_available, movie_index) values('{choice_title}', '{choice_genre}', '{choice_director}', {choice_seats}, {choice_movie_index})"
        mycursor.execute(new_movie)
        con.commit()
        print(f"Movie {choice_title} was added successfully.")
        break

def cancel(table,service,servicetype="int"):
       while True:
              if servicetype == "int":
                     try:
                            choice= input(f"Enter the {service} index to remove or type quit: ").lower()
                            if choice == "quit":
                                   break
                            choice = int(choice) #sql database stores movie index as int in movies table. If the user does not provide a number this will throw ValueError: invalid literal for int() with base 10:
                     except:
                            print("Error: you did not type an integer")

                     sql = f"select * from {table} where {service}_index = {choice}" 
                     mycursor.execute(sql)
                     data = mycursor.fetchall()
                     if data == []:
                            print(f"{service} index not found")
                            continue
                     
                     count_value = count(table)
              
                     sql = f"delete from {table} where {service}_index = {choice}"
                     mycursor.execute(sql)
                     con.commit()

                     for z in range(choice + 1,count_value + 1):
                            sql = f"update {table} set {service}_index = {z -1} where {service}_index = {z}"
                            mycursor.execute(sql)
                            con.commit()

                     print(f"{service} index {choice} has been removed")
                     break
              elif servicetype == "string":
                    choice = input(f"enter {service} to delete: ")
                    if choice.lower() == "quit":
                            break
                    is_in_db = f"select * from {table} where {service} =  '{choice}'"
                    mycursor.execute(is_in_db)
                    data = mycursor.fetchall()
                    if data == []:
                            print(f"{service} not found")
                            continue
                    
                    sql = f"delete from {table} where {service} = '{choice}'"
                    mycursor.execute(sql)
                    con.commit()
                    print(f"{choice} was deleted")
                    break
              else:
                    print("Error: service type not found")

def update_movie():
    display_movies()
    while True:
        choice_movie_index = input("Enter the movie index to update: ")
        if choice_movie_index.lower() == "quit":
            break
        choice_movie_index = int(choice_movie_index) #sql database stores movie index as int in movies table. If the user does not provide a number this will throw ValueError: invalid literal for int() with base 10:
        choice_title = input("Enter movie title: ")
        if choice_title.lower() == "quit":
            break
    
        choice_genre = input("Enter movie genre: ")
        if choice_genre.lower() == "quit":
            break

        choice_director = input("Enter movie director: ")
        if choice_director.lower() == "quit":
            break

        try:
            choice_seats = input("enter number of seats available: ")
            if choice_seats.lower() == "quit":
                break
            choice_seats = int(choice_seats) #sql database stores seats as int datatype in movies table. If the user does not provide a number this will throw ValueError: invalid literal for int() with base 10:
        except:
            print("Error: you did not type a number")
            continue
        sql = f"update {movies} set title = '{choice_title}', genre = '{choice_genre}', director = '{choice_director}', seats_available = '{choice_seats}' where movie_index = {choice_movie_index}"
        mycursor.execute(sql)
        con.commit()
        print("updated")
        break

def admin_menu():
    while True:
        print("─" * 90)
        print("1. View all employee details")
        print("2. Add employee details")
        print("3. Edit employee details")
        print("4. Delete Employee")
        print("5. Log Out")
        print("─" * 90)
        choice = input("Enter your choice (1-5): ")
        if choice == "1":
            view_all_users()
        elif choice == "2":
            add_employee()
        elif choice == "3":
            edit_employee()
        elif choice == "4":
            view_all_users()
            cancel(users,'username','string')
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")
            continue

def view_all_users():
    count_users = count(users)
    for z in range(0,count_users):
       sql = f"select * from {users}"
       mycursor.execute(sql)
       data = mycursor.fetchall()
       print(f"{z+1}) username: {data[z][0]}, pass:{data[z][1]},status:{data[z][2]},date_of_joining:{data[z][3]}, experience:{data[z][4]}")

def add_employee():
    while True:
        choice_username = input("Enter username : ")
        if choice_username.lower() == "quit":
            break

        choice_password= input("Enter password: ")
        if choice_password.lower() == "quit":
            break
        
        choice_status = input("enter status: ")
        if choice_status.lower() == "quit":
            break

        choice_date_of_joining= input("Enter date of join: ")
        if choice_date_of_joining.lower() == "quit":
            break

        choice_experience = input("Enter experience: ")
        if choice_experience.lower() == "quit":
            break

        sql = f"insert into {users} (username,pass,status,date_of_joining,experience) values('{choice_username}', '{choice_password}', '{choice_status}', '{choice_date_of_joining}', '{choice_experience}')"
        mycursor.execute(sql)
        con.commit()
        print(f"{choice_username} was added successfully to {users} database")
        break
def edit_employee():
    while True:
        old_username = input("enter old username: ")
        if old_username.lower() == "quit":
            break

        choice_username = input("Enter username : ")
        if choice_username.lower() == "quit":
            break

        choice_password= input("Enter password: ")
        if choice_password.lower() == "quit":
            break
        
        choice_status = input("enter status: ")
        if choice_status.lower() == "quit":
            break

        choice_date_of_joining= input("Enter date of join: ")
        if choice_date_of_joining.lower() == "quit":
            break

        choice_experience = input("Enter experience: ")
        if choice_experience.lower() == "quit":
            break

        sql = f"update {users} set username = '{choice_username}', pass = '{choice_password}', status = '{choice_status}', date_of_joining = '{choice_date_of_joining}', experience = '{choice_date_of_joining}' where username = '{old_username}'"
        mycursor.execute(sql)
        con.commit()
        print(f"{choice_username} was edited")
        break

def user_menu():
    while True:
        print("─" * 90)
        print("1. View Movies")
        print("2. Book Tickets")
        print("3. View Bookings")
        print("4. Cancel Booking")
        print("5. Logout")
        print("─" * 90)
        choice = input("Enter your choice (1-5): ")
        if choice == "1":
            display_movies()
        elif choice == "2":
            book_tickets()
        elif choice == "3":
            view_user_bookings()
        elif choice == "4":
            cancel(bookings,'booking')
        elif choice == "5":
            print("Logged out successfully.")
            break
        else:
            print("Invalid choice. Please try again.")

def book_tickets():
    while True: #gets movie index for the movie you want to book
        display_movies()
        try:
            choice_movie_index = input("Enter the movie index to book tickets for: ") 
            if choice_movie_index == "quit":
                break
            choice_movie_index = int(choice_movie_index) #sql database stores movie index as int in movies table. If the user does not provide a number this will throw ValueError: invalid literal for int() with base 10:
        except:
            print("type an integer eg: type 1 for 1st movie\n\n")
            continue
        count_movies = count(movies)
        if choice_movie_index < 0 or choice_movie_index >= count_movies:
            print("Invalid movie selection. Out of bounds.\n\n")
            continue
        break

    while True: #gets number of tickets you want to book
        if choice_movie_index == "quit":
            break

        try:
            choice_num_tickets = input("Enter the number of tickets to book: ")
            if choice_num_tickets == "quit":
                break
            choice_num_tickets = int(choice_num_tickets)
        except:
            print("type a number (eg: 1 for 1 ticket) \n\n")
            continue

        if choice_num_tickets <= 0: 
            print("Number of tickets should be greater than zero.\n\n")
            continue
    
        sql = f"select seats_available from {movies} where movie_index = {choice_movie_index}"
        mycursor.execute(sql)
        seats = mycursor.fetchone()[0]
        if choice_num_tickets > seats: 
            print("Not enough seats available.\n\n")
            continue
        break

    while True: #gets venue you want to book
        if choice_movie_index == "quit" or choice_num_tickets == "quit":
            break

        print("─" * 90)
        print("Available venues:")
        movie_venue = {1: "Falter", 2: "Aescamyr", 3: "Enia", 4: "Tintagel", 5: "Lingen", 6: "Elmbow", 7: "Guildingston"}
        for i in range(1, 8):#prints items in movie_venue dictionary
            print(i, ":", movie_venue[i])
        try:
            choice_venue = input("Enter the number of the desired venue: ")
            if choice_venue == "quit":
                break
            choice_venue = int(choice_venue)
        except:
            print("type a number eg: 1 for  Falter")
            continue
        venue_user = movie_venue.get(choice_venue)
        if not venue_user: #if venue is not present in movie_venue, then movie_venue.get(venue) returns none, this none gets stored in venue_user. This is if block is checking if venue user is none
            print("Invalid venue selection.\n\n")
            continue
        print("─" * 90)            
        break

    print("─" * 90)
    print("─"*90)
    print("Food Menu")
    print("─" * 90)

    count_foods = count(food_menu)
    for z in range(1,count_foods+1):
        sql = f"select item,price from {food_menu} where item_index = {z}"
        mycursor.execute(sql)
        data = mycursor.fetchall()
        print(f"{z}) item:{data[0][0]},price:{data[0][1]}")

    food_cost = 0
    while True: #ordering items
        global quantity
        if choice_movie_index == "quit" or choice_num_tickets == "quit" or choice_venue == "quit":
            break

        try:
            choice_item_index = input("type the item number to order or type done to finish ordering: ")
            if choice_item_index.lower() == "quit" or choice_item_index.lower() == 'done':
                break
            choice_item_index= int(choice_item_index)

            quantity = input("enter quantity: ")
            if quantity.lower() == "quit":
                break
            quantity = int(quantity)
            if quantity > 10:
                print("we can only serve up to 10 foods")
                continue
            elif quantity < 0:
                print("negative not allowed")
                continue
        
            sql = f"select price from {food_menu} where item_index = {choice_item_index}"
            mycursor.execute(sql)
            choice_item_cost = mycursor.fetchone()[0]
            food_cost += choice_item_cost*quantity
        except:
            print("enter a number")
            continue

    while True:
            if choice_movie_index == "quit" or choice_num_tickets == "quit" or choice_venue == "quit" or choice_item_index == "quit":
                break

            print("─" * 90)
            proceed_to_billing = input("Would you like to continue booking this ticket? (yes/no): ").lower()
            if proceed_to_billing == "yes":
                print("─" * 90)
                print("Billing Details")
                print("─" * 90)
                print(f"Number of tickets: {choice_num_tickets}")
                print(f"Ticket Cost: ${choice_num_tickets * 10}")
                print(f"Food Cost: ${food_cost}")
                total_cost = choice_num_tickets * 10 + food_cost
                print(f"Total Cost: ${total_cost}")
                print("Thank you for booking with WYDEOS!")
                print("─" * 90)
                sql = f"select title from {movies} where movie_index = {choice_movie_index}"
                mycursor.execute(sql)
                choice_title = mycursor.fetchone()[0]
                x = datetime.datetime.now()
                cur_time = f"{x.year}-{x.month}-{x.day}"
                print(cur_time)

                booking_index = count(bookings) + 1
                sql = f"insert into {bookings} (user,booking_index,title,number_of_tickets,venue,time,food_cost) values('{username}',{booking_index},'{choice_title}',{choice_num_tickets},'{choice_venue}','{cur_time}',{food_cost})"
                mycursor.execute(sql)
                con.commit()
            elif proceed_to_billing == "no":
                print("ticket cancelled.")
            else:
                print("Invalid response, type yes or no.\n\n")
                continue

            break

def view_user_bookings():
    sql = f"select * from {bookings} where user = '{username}'"
    mycursor.execute(sql)
    print(mycursor.fetchall())
            
def login():
    global username
    global password
    while True:
        choice = input("do you want to register a new user? (yes/no): ".lower())
        if choice == 'yes':
            register()
        elif choice == 'no':
            pass
        else:
            print("type yes or no")
            continue
            
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        sql = f"select status from {users} where username = '{username}' and pass = '{password}'"
        mycursor.execute(sql)
        status = mycursor.fetchone()
        if status == None:
            print("username or password is incorrect")
            continue
        elif status[0] == "user":
            user_menu()
        elif status[0] == "admin":
            admin_menu()
        elif status[0] == "emp":
            employee_menu()
        else:
            print(f"your status has been set to {status[0]} which cannot be detected.Most likely your status in the database has been incorrectly set. Contact admin to resolve the issue")
            continue

login()
