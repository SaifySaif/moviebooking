import datetime #used to print current time at line 241
import mysql.connector as m
db = "movies" #name of database
food_menu = "food_menu" #name of table containing food menu
users = "users" #name of table containing users
movies = "movies" #name of table containing movies
bookings = "bookings" #name of table containing bookings

con = m.connect(host = "localhost",user="root",password="@Te3{oHgq$#B|h~pm[",database = db) #tries to connect to database in variable db, make sure to set your password to the db database correctly.
if con.is_connected:
    print("successfully connected")
else:
    print("WARNING!: not connected")

mycursor = con.cursor() #As far as the author knows, this syntax is not needed to execute any mysql.connector commands but the author's school requires the author to use this line.

def main():
    global username
    global password
    while True:
        print("")
        print("1. Login")
        print("2. Register")

        choice = input(">")
        if choice == "1":
            while True:            
                username = input("Enter your username or type quit to head back to login/register page: ")
                if username == "quit":
                    print("quitting....")
                    break
                password = input("Enter your password or type quit to head back to login/register page: ") #note the password used in line 9's connection will be changed to what is inputted here. The rest of the code in this file doesn't require the connection password so this is not a problem. The reason I did this is to avoid creating another global variable.
                if password == "quit":
                    print("quitting....")
                    break

                mycursor.execute(f"select status from {users} where username = '{username}' and pass = '{password}'") #the execute method tries to execute code in brackets in sql. SO this tries to select values from status column from users where username = username and pass = password
                status = mycursor.fetchone() #Should fetch a tuple containing 1 value which is status of the username. If no username and password is present in the database which matches the inputted username and password then None is returned.
                if status == None:
                    print("username or password is incorrect")
                    continue
                elif status[0] == "user": #status[0] is the status of inputted username. Check comment on line 34 for understanding what status variable is 
                    user_menu() 
                elif status[0] == "admin":
                    admin_menu() 
                elif status[0] == "emp":
                    employee_menu() 
                else:
                    print(f"your status has been set to {status[0]} which cannot be detected. Most likely your status in the database has been incorrectly set. Contact admin to resolve the issue")
                    continue

        if choice == "2":
            register()

        else:
            print("type 1 to login or 2 to register")
            continue

def register():
    while True:
        print("")
        choice_username = input("Enter your new username or type quit to head back to login/register page: ")
        if choice_username == "quit":
            print("quitting......")
            break
        mycursor.execute(f"select * from {users} where username =  '{choice_username}'") #trying to fetch the inputted choice_username from users table, this is used in code from line 56 to 59 to check if the choice_username is already present in users table, if so then that is not allowed as it can create problems retrieving data from same named entries. So I will force the user to choose another username instead.
        data = mycursor.fetchall()
        if data != []:
            print("username taken")
            continue

        password = input("Enter your new password or type quit to head back to login/register page: ")
        if password == "quit":
            print("quitting...... ")
            break
        confirm_password = input("retype your password to confirm it or type quit to head back to login/register page: ")
        if confirm_password == "quit":
            print("quitting......")
            break
        if password != confirm_password:
            print("passwords do no match")
            continue
        
        mycursor.execute(f"insert into {users} (username,pass,status,date_of_joining,experience) values('{choice_username}','{password}','user','{None}','{None}')" )
        con.commit() #Makes sure the inserted row due to the code on line 73 is stored permanently in sql, in users table. Without this line the new user data will not be permanently stored in users table.
        print(f"Sucessfully registered {choice_username}")
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
    mycursor.execute(f"select * from {bookings}") 
    data = mycursor.fetchall()
    if data == []:
        print("no bookings found")
    else:
        for a in data:
            print(f'user:{a[0]} booking_index:{a[1]} title:{a[2]} number_of_tickets:{a[3]} venue:{a[4]} time:{a[5]} food_cost:{a[6]}')

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
    count_movies = count(movies) #returns cardinality (number of rows) of movies table
    for z in range(0,count_movies):
       mycursor.execute(f"select * from {movies} having movie_index = {z+1}")
       data = mycursor.fetchall()
       print(f"{z+1}) title:{data[0][0]}, genre:{data[0][1]},director:{data[0][2]},seats_available:{data[0][3]}")

def count(database):
    mycursor.execute(f"select count(*) from {database}")
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
            choice_seats = int(choice_seats) #sql database stores seats as int datatype in movies table. If the user does not provide a number this will throw ValueError and code will go to exception block
        except:
            print("Error: you did not type a number")
            continue

        choice_movie_index = count(movies) + 1

        new_movie = f"insert into {movies} (title, genre, director,seats_available, movie_index) values('{choice_title}', '{choice_genre}', '{choice_director}', {choice_seats}, {choice_movie_index})"
        mycursor.execute(new_movie)
        con.commit()
        print(f"Movie {choice_title} was added successfully.")
        break

def cancel(table,service,servicetype="int",check = False): #check is used to check whether retrieved data belongs to user or not, check line 198
       while True:
              if servicetype == "int":
                     try:
                            choice= input(f"Enter the {service} index to remove or type quit: ").lower()
                            if choice == "quit":
                                   break
                            choice = int(choice) #sql database stores movie index as int in movies table. If the user does not provide a number this will throw ValueError and code will go to exception block
                     except:
                            print("Error: you did not type an integer")
                    
                     mycursor.execute(f"select * from {table} where {service}_index = {choice}") 
                     data = mycursor.fetchall()
                     if data == []:
                            print(f"{service} index not found")
                            continue
                     
                     if check == True:
                         mycursor.execute(f"select user from {table} where {service}_index = {choice}")
                         data = mycursor.fetchone()[0]
                         if data != username:
                            print("choose an index which belongs to you")
                            break
                     
                     count_value = count(table)
              
                     mycursor.execute(f"delete from {table} where {service}_index = {choice}")
                     con.commit()

                     for z in range(choice + 1,count_value + 1):
                            mycursor.execute(f"update {table} set {service}_index = {z -1} where {service}_index = {z}")
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
                    
                    mycursor.execute(f"delete from {table} where {service} = '{choice}'")
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
        choice_movie_index = int(choice_movie_index) #sql database stores movie index as int in movies table. If the user does not provide a number this will throw ValueError and code will go to exception block
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
            choice_seats = int(choice_seats) #sql database stores seats as int datatype in movies table. If the user does not provide a number this will throw ValueError and code will go to exception block
        except:
            print("Error: you did not type a number")
            continue
        mycursor.execute(f"update {movies} set title = '{choice_title}', genre = '{choice_genre}', director = '{choice_director}', seats_available = '{choice_seats}' where movie_index = {choice_movie_index}")
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
    mycursor.execute(f"select * from {users}")
    data = mycursor.fetchall()
    if data == []:
        print("no users found")
    else:
        for z in range(0,count_users):
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

        mycursor.execute(f"insert into {users} (username,pass,status,date_of_joining,experience) values('{choice_username}', '{choice_password}', '{choice_status}', '{choice_date_of_joining}', '{choice_experience}')"
)
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

        mycursor.execute(f"update {users} set username = '{choice_username}', pass = '{choice_password}', status = '{choice_status}', date_of_joining = '{choice_date_of_joining}', experience = '{choice_date_of_joining}' where username = '{old_username}'"
)
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
            cancel(bookings,'booking',"int",True)
        elif choice == "5":
            print("Logged out successfully.")
            break
        else:
            print("Invalid choice. Please try again.")

def book_tickets():
    quit_check = False
    while True: #gets movie index for the movie you want to book
        display_movies()
        try:
            choice_movie_index = input("Enter the movie index to book tickets for: ") 
            if choice_movie_index == "quit":
                quit_check = True
                break
            choice_movie_index = int(choice_movie_index) #sql database stores movie index as int in movies table. If the user does not provide a number this will throw ValueError: invalid literal for int() with base 10:
        except:
            print("type an integer eg: type 1 for 1st movie\n\n")
            continue
        count_movies = count(movies)
        if choice_movie_index < 0 or choice_movie_index > count_movies:
            print("Invalid movie selection. Out of bounds.\n\n")
            continue
        break

    while True: #gets number of tickets you want to book
        if quit_check == True:
            break

        try:
            choice_num_tickets = input("Enter the number of tickets to book: ")
            if choice_num_tickets == "quit":
                quit_check = True
                break
            choice_num_tickets = int(choice_num_tickets)
        except:
            print("type a number (eg: 1 for 1 ticket) \n\n")
            continue

        if choice_num_tickets <= 0: 
            print("Number of tickets should be greater than zero.\n\n")
            continue
    
        mycursor.execute(f"select seats_available from {movies} where movie_index = {choice_movie_index}")
        seats = mycursor.fetchone()[0]
        if choice_num_tickets > seats: 
            print("Not enough seats available.\n\n")
            continue
        break

    while True: #gets venue you want to book
        if quit_check == True:
            break

        print("─" * 90)
        print("Available venues:")
        movie_venue = {1: "Falter", 2: "Aescamyr", 3: "Enia", 4: "Tintagel", 5: "Lingen", 6: "Elmbow", 7: "Guildingston"}
        for i in range(1, 8):#prints items in movie_venue dictionary
            print(i, ":", movie_venue[i])
        try:
            choice_venue = input("Enter the number of the desired venue: ").lower()
            if choice_venue == "quit":
                quit_check == True
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

        print("─" * 90)
        print("─"*90)
        print("Food Menu")
        print("─" * 90)

        count_foods = count(food_menu)
        for z in range(1,count_foods+1):
            mycursor.execute(f"select item,price from {food_menu} where item_index = {z}")
            data = mycursor.fetchall()
            print(f"{z}) item:{data[0][0]},price:{data[0][1]}")
        break

    print("")
    food_cost = 0
    while True: #ordering items
        global quantity
        if quit_check == True:
            break

        try:
            choice_item_index = input("type the item number to order or type done to finish ordering: ").lower()
            if choice_item_index == "quit":
                quit_check = True
                break
            elif choice_item_index == 'done':
                break
            choice_item_index= int(choice_item_index)

            quantity = input("enter quantity: ").lower()
            if quantity == "quit":
                quit_check == True
                break
            quantity = int(quantity)
            if quantity > 10:
                print("we can only serve up to 10 foods")
                continue
            elif quantity < 0:
                print("negative not allowed")
                continue
        
            mycursor.execute(f"select price from {food_menu} where item_index = {choice_item_index}")
            choice_item_cost = mycursor.fetchone()[0]
            food_cost += choice_item_cost*quantity
        except:
            print("enter a number")
            continue

    while True:
            if quit_check == True:
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
                mycursor.execute(f"select title from {movies} where movie_index = {choice_movie_index}")
                choice_title = mycursor.fetchone()[0]
                x = datetime.datetime.now()
                cur_time = f"{x.year}-{x.month}-{x.day}"
                print(cur_time)

                booking_index = count(bookings) + 1
                mycursor.execute(f"insert into {bookings} (user,booking_index,title,number_of_tickets,venue,time,food_cost) values('{username}',{booking_index},'{choice_title}',{choice_num_tickets},'{choice_venue}','{cur_time}',{food_cost})")
                con.commit()

                mycursor.execute(f"select seats_available from movies where movie_index = {choice_movie_index}")
                data = mycursor.fetchone()[0]
                new_seats = data - choice_num_tickets
                mycursor.execute(f"update movies set seats_available = {new_seats} where movie_index = {choice_movie_index}")
                con.commit()

            elif proceed_to_billing == "no":
                print("ticket cancelled.")
            else:
                print("Invalid response, type yes or no.\n\n")
                continue

            break

def view_user_bookings():
    mycursor.execute(f"select * from {bookings} where user = '{username}'")
    data = mycursor.fetchall()
    if data == []:
        print("no bookings found")
    else:
        for z in data:
            print(f"user:{z[0]} booking_index:{z[1]} title:{z[2]} number_of_tickets:{z[3]} venue:{z[4]} time:{z[5]} food_cost:{z[6]}")
main()
