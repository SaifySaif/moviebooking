from datetime import datetime #used to print current time at line 241
import mysql.connector as m
con = m.connect(host = "localhost",user="root",password="@Te3{oHgq$#B|h~pm[",database = "movies")
if con.is_connected:
    print("successful")
else:
    print("not connected")
mycursor = con.cursor()
mycursor.execute("select * from users")
data = mycursor.fetchall()
print(data)

users = {"employee1": {"pass":"emppass1", "status":"emp","date_of_join" : "2023-01-01", "experience": "2 years"},
         "employee2": {"pass":"emppass2", "status":"emp","date_of_join" : "2024-01-01", "experience": "2 years"},
         "admin1": {"pass":"adminpass1", "status":"admin", "date_of_join":"2023-02-2","experience" : "1 year"}, "dave":{"pass":"yo","status":"noob"},
         "admin2": {"pass":"adminpass2", "status":"admin", "date_of_join":"2024-02-2","experience" : "1 year"},
         "user1": {"pass":"userpass1","status":"user"},
         "user2": {"pass":"userpass2","status":"user"}} #database of users

movies = [
    {"title": "Peter Jonsson", "genre": "Action", "director": "Muge"},
    {"title": "Perry Park", "genre": "physiological", "director": "Cha Min Lee"},
] #database of movies

seats_available = [1000, 1500] #database of seats available for the respective movies

food_menu = {
    "1": {"item": "Popcorn", "price": 5},
    "2": {"item": "Soda", "price": 3},
} #database for the foods sold at the movies

bookings = {"user1":[{"booking1":"","title":"Peter Jonsson", "number of tickets":1, "venue":"Falter","time":"12 AM", "food":""},
                      {"booking2":"","title":"Perry Park", "number of tickets":1, "venue":"Falter","time":"12 AM", "food":""}],
            "user2":[]} #database of obokings

def register():
    username = input("Enter your new username: ")
    password = input("Enter your new password: ")
    users[username] = password
    print("Registration successful!")

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
    print(bookings)

def manage_movies():
    while True:
        print("─" * 90)
        print("1. Add Movie")
        print("2. Remove Movie")
        print("3. Update Movie")
        print("4. View Movies")
        print("5. Go Back")
        print("─" * 90)
        choice = input("Enter your choice (1-5): ")
        if choice == "1":
            add_movie()
        elif choice == "2":
            remove_movie()
        elif choice == "3":
            update_movie()
        elif choice == "4":
            display_movies()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

def add_movie():
    title = input("Enter movie title: ")
    genre = input("Enter movie genre: ")
    director = input("Enter movie director: ")
    movies.append({"title": title, "genre": genre, "director": director})
    seats_available.append(100)  # Default seat count
    print("Movie added successfully.")

def remove_movie():
    display_movies()
    movie_index = int(input("Enter the movie number to remove: ")) - 1
    if 0 <= movie_index < len(movies):
        removed_movie = movies.pop(movie_index)
        print(f"Removed movie: {removed_movie['title']} and seats {seats_available.pop(movie_index)} for the respective movie")
    else:
        print("Invalid movie selection.")

def update_movie():
    display_movies()
    movie_index = int(input("Enter the movie number to update: ")) - 1
    if 0 <= movie_index < len(movies):
        title = input("Enter new movie title: ")
        genre = input("Enter new movie genre: ")
        director = input("Enter new movie director: ")
        movies[movie_index] = {"title": title, "genre": genre, "director": director}
        print("Movie updated successfully.")
    else:
        print("Invalid movie selection.")

def display_movies():
    print("─" * 90)
    print("Welcome to the WYDEOS! A movie booking website")
    print("─" * 90)
    for i, movie in enumerate(movies):
        print(f"{i + 1}. {movie['title']} - {movie['genre']} ({movie['director']})")
        print(f"Seats Available: {seats_available[i]}")
        print("─" * 90)

def admin_menu():
    while True:
        print("─" * 90)
        print("1. View all employee details")
        print("2. Add or edit employee details")
        print("3. Delete Employee")
        print("4. Log Out")
        print("─" * 90)
        choice = input("Enter your choice (1-5): ")
        if choice == "1":
            view_all_employees()
        elif choice == "2":
            add_edit_employee()
        elif choice == "3":
            delete_employee()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

def view_all_employees():
    for username in users:
        if users[username]["status"] == "emp":
            print("\nusername is",username)
            print("date of joining is", users[username]["date_of_join"])
            print("experience is", users[username]["experience"])

def add_edit_employee():
    username = input("Enter new username(if username is already present in database, the details of that username will get changed to the ones you will put.): ")
    password = input("enter new password: ")
    date_of_join = input("Enter new date of join (YYYY-MM-DD): ")
    experience = input("Enter new experience (e.g., 2 years): ")

    users[username] = {"pass":password,"status":"emp","date_of_join":date_of_join,"experience":experience}

    print("Employee added successfully.")

def delete_employee():
    username = input("Enter username of the employee to delete: ")
    try:
        users.pop(username)
    except:
        print(username,"not present in database")

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
            cancel_booking()
        elif choice == "5":
            print("Logged out successfully.")
            break
        else:
            print("Invalid choice. Please try again.")

def book_tickets():
    while True: #gets movie index for the movie you want to book
        try:
            display_movies()
            try:
                movie_index = int(input("Enter the movie number to book tickets for: ")) - 1 #gives index of element (element is a dictionary, containing info about movie) in 'movies' variable
            except:
                print("type a number eg: 1 for 1st movie\n\n")
                continue
            if movie_index < 0 or movie_index >= len(movies): #if movie_index is negative or greater than max index present in movies variable, it raises an exception
                print("Invalid movie selection. Out of bounds.\n\n")
                raise Exception
            break
        except:
            continue
    while True: #gets number of tickets you want to book
        try:
            try:
                num_tickets = int(input("Enter the number of tickets to book: "))
            except:
                print("type a number (eg: 1 for 1 ticket) \n\n")
                continue

            if num_tickets <= 0: #if num_tickets is negative, it raises exception
                print("Number of tickets should be greater than zero.\n\n")
                raise Exception
            if num_tickets > seats_available[movie_index]: #if num_tickets > available seats for the movie, it raises exception
                print("Not enough seats available.\n\n")
                raise Exception
            break
        except:
            continue
    while True: #gets venue you want to book
        try:
            print("─" * 90)
            print("Available venues:")
            movie_venue = {1: "Falter", 2: "Aescamyr", 3: "Enia", 4: "Tintagel", 5: "Lingen", 6: "Elmbow", 7: "Guildingston"}
            for i in range(1, 8):#prints items in movie_venu dictionary
                print(i, ":", movie_venue[i])
            try:
                venue = int(input("Enter the number of the desired venue: "))
            except:
                print("type a number eg: 1 for  Falter")
                continue
            venue_user = movie_venue.get(venue)
            if not venue_user: #if venue is not present in movie_venue, then movie_venue.get(venue) returns none, this none gets stored in venue_user. This is if block is checking if venue user is none
                print("Invalid venue selection.\n\n")
                raise Exception
            print("─" * 90)            
            
            break
        except:
            continue

    curtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #stores current time %Y stands for Year, full version. eg: 2018, %m stands for Month as a number 01-12. eg:20, %d stands for day of the month 01-31. eg: 31, %H stands for Hour 00-23. eg:17,%M stands for minute 00-59. eg: 41, %S stands for second 00-59. eg: 08
    booking_num = 1
    for x in bookings[username]:
        booking_num = booking_num + 1
    bookings[username].append({'booking' + str(booking_num):'','title':movies[movie_index],'number of tickets':num_tickets,'venue':venue_user,'food':{}})
    food_cost = 0
    print("─" * 90)

    print("─"*90)
    print("Food Menu")
    print("─" * 90)
    for key, item in food_menu.items():
        print(f"{key}. {item['item']} - ${item['price']}")
    while True:
        try:
            order_food = input("Would you like to order food or finish ordering? (yes/no): ").lower()
            if order_food == "yes":
                choice = input("Enter the item number to order or 'done' to finish: ")
                if choice in food_menu:
                    try:
                        quantity = int(input("Enter the quantity: "))
                    except:
                        print("type a number")
                    if quantity < 0:
                        print("quantity cannot be less than 0")
                        raise Exception
                    elif quantity > 1000:
                        print("we can't serve that much")
                        raise Exception
                    food_cost += food_menu[choice]['price'] * quantity

                    for x in bookings[username]:
                        if 'booking' + str(booking_num) in x:     
                            bookings[username][bookings[username].index(x)].update({'food':{food_menu[choice]['item']:quantity}})

                elif choice == "done":
                    break
                else:
                    print("Invalid item number. Please try again.")
            elif order_food == "no":
                print("No food ordered.")
                break
            else:
                print("Invalid response. Please enter 'yes' or 'no'.\n\n")
                raise Exception
        except:
            continue
    while True:
        try:
            print("─" * 90)
            proceed_to_billing = input("Would you like to continue booking this ticket? (yes/no): ").lower()
            if proceed_to_billing == "yes":
                seats_available[movie_index] -= num_tickets #removes the booked seats from available seats
                print("─" * 90)
                print("Billing Details")
                print("─" * 90)
                print(f"Number of tickets: {num_tickets}")
                print(f"Ticket Cost: ${num_tickets * 10}")
                print(f"Food Cost: ${food_cost}")
                total_cost = num_tickets * 10 + food_cost
                print(f"Total Cost: ${total_cost}")
                print("Thank you for booking with WYDEOS!")
                print("─" * 90)
            elif proceed_to_billing == "no":
                print("ticket canceled.")
            else:
                print("Invalid response. Please enter 'yes' or 'no'.\n\n")
                raise Exception
            break
        except:
            continue

def view_user_bookings():
    print(bookings[username])
            
def cancel_booking():
    try:
        cancel_booking_num = input("enter the booking number which you want to cancel: ")
        for i in bookings[username]:
            if 'booking' + str(cancel_booking_num) in i:
                index_of_i = bookings[username].index(i)
        print(bookings[username].pop(index_of_i),"was removed")
    except:
        print("booking number not found")
class statuserror(Exception):
    pass
class loginerror(Exception):
    pass
def login():
    global username
    global password
    while True:
        try:
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            if username in users and password == users[username]["pass"]:
                print("\nUsername and password present in database.")   
            else:
                raise loginerror

            if "status" not in users[username].keys():
                raise statuserror
            elif users[username]["status"] == "admin":
                admin_menu()
            elif users[username]["status"] == "emp":
                employee_menu()
            elif users[username]["status"] == "user":
                user_menu()

            else:
                raise statuserror
        except statuserror:
            print("You're status in the database has not been set to employee or admin. File a complaint with this error to IT to get this issue sorted.")
        except loginerror:
            print("invalid username or password")

class password_mismatch_error(Exception):
    pass

def register():
    while True:
        try:
            choice = input("do you want to register as user yes or no?: ")
            if choice == "yes":
                newusername = input("enter new username: ")
                if newusername in users:
                    print("username already present in database")
                    continue
                newpassword = input("enter new password: ")
                confirmnewpassword = input("confirm your password: ")
                bookings[newusername] = []
                if confirmnewpassword != newpassword:
                    raise password_mismatch_error
                users[newusername] = {"pass":newpassword,"status":"user"}
                break
            elif choice == "no":
                break
            else:
                raise loginerror
        except loginerror:
            print("please type yes or no")
            continue
        except password_mismatch_error:
            print("passwords do not match")
            continue


register()
login()



