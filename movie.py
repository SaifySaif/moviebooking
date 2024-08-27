from datetime import datetime

users = {}

movies = [
    {"title": "Peter Jonsson", "genre": "Action", "director": "Muge"},
    {"title": "Perry Park", "genre": "physiological", "director": "Cha Min Lee"},
    {"title": "Jungle novel", "genre": "Family drama", "director": "Liam candy"},
    {"title": "Kasmiri", "genre": "Action", "director": "Kunal Rathum"},
    {"title": "la la place", "genre": "Romance", "director": "Luthe Mathew"},
    {"title": "Yesterday land", "genre": "Science Fiction", "director": "Newtfreeman"},
    {"title": "Die another day", "genre": "Action", "director": "Rodrick Mason"},
    {"title": "Noona", "genre": "Family drama", "director": "Dong Wook Soon"},
    {"title": "School for evil and evil", "genre": "Fantasy", "director": "Alexa Cooper"},
    {"title": "The Sign Board", "genre": "Romance", "director": "Roberts"},
    {"title": "Villain's need to live", "genre": "Family drama", "director": "Magpie Rami"},
    {"title": "The Summer Day", "genre": "Romance", "director": "Liam candy"},
    {"title": "Fresh Princess", "genre": "slice of life", "director": "Landon gremecK"},
    {"title": "Go behind", "genre": "Family drama", "director": "Mingy"},
    {"title": "I met a ghost", "genre": "Horror", "director": "Arnold Williams"},
    {"title": "How I died", "genre": "Horror", "director": "Sirighost"},
    {"title": "Love in a nutshell", "genre": "Romance", "director": "Manny Quinn"},
    {"title": "The great awakening", "genre": "Dystopian", "director": "Chris Peacock"},
    {"title": "The last day of living", "genre": "Tragedy", "director": "Emma Roids"},
    {"title": "Goodbye, John", "genre": "Family drama", "director": "Seymour Cox"},
    {"title": "Love and mercy", "genre": "Dark comedy", "director": "Krystal Ball"},
]

seats_available = [1000, 1500, 1200, 1700, 1100, 1500, 1400, 1500, 1200, 1400, 1900, 1200, 1000, 1400, 1300, 1800, 1100,
                   1900, 1100, 1000, 1400]

food_menu = {
    "1": {"item": "Popcorn", "price": 5},
    "2": {"item": "Soda", "price": 3},
    "3": {"item": "Burger", "price": 7},
    "4": {"item": "Burger", "price": 7},
    "5": {"item": "Nachos", "price": 8},
    "6": {"item": "Wrap", "price": 5},
    "7": {"item": "Ice Cream", "price": 4},
    "8": {"item": "Cotton Candy", "price": 4},
    "9": {"item": "French Fries", "price": 5},
    "10": {"item": "Sweet corn", "price": 3},
}

movie_times = ["9am", "12pm", "3pm", "6pm", "9pm", "12am"]

# Initialize food_cost as a global variable
food_cost = 0

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if username in users and password == users[username]:
        print("Login successful!")
    else:
        print("Invalid username or password. Please register.")
        register()

def register():
    username = input("Enter your new username: ")
    password = input("Enter your new password: ")
    users[username] = password
    print("Registration successful!")

def display_movies():
    print("─" * 90)
    print("Welcome to the WYDEOS! A movie booking website")
    print("─" * 90)
    for i, movie in enumerate(movies):
        print(f"{i + 1}. {movie['title']} - {movie['genre']} ({movie['director']})")
        print(f"Seats Available: {seats_available[i]}")
        print("─" * 90)

def book_tickets(movie_index, num_tickets):
    if movie_index < 0 or movie_index >= len(movies):
        print("Invalid movie selection.")
        print()
        return

    if num_tickets <= 0:
        print("Number of tickets should be greater than zero.")
        print()
        return

    if num_tickets > seats_available[movie_index]:
        print("Not enough seats available.")
        print()
        return

    print("─" * 90)
    print("Available venues:")
    movie_venue = {1: "Falter", 2: "Aescamyr", 3: "Enia", 4: "Tintagel", 5: "Lingen", 6: "Elmbow", 7: "Guildingston"}
    for i in range(1, 8):
        print(i, ":", movie_venue[i])
    venue = int(input("Enter the number of the desired venue: "))
    venue_user = movie_venue[venue]
    if venue not in range(1, 8):
        print("Invalid venue selection.")
        print()
        return

    print("─" * 90)

    seats_available[movie_index] -= num_tickets

    print("Available movie times:")
    for i, time in enumerate(movie_times, start=1):
        print(f"{i}. {time}")

    time_choice = int(input("Enter the number of the desired movie time: "))
    if time_choice < 1 or time_choice > len(movie_times):
        print("Invalid time selection.")
        print()
        return
    print("─" * 90)

    chosen_time = movie_times[time_choice - 1]
    date_time_str = input(f"Enter the date and time (DD-MM-YYYY {chosen_time}): ")
    date_time_str = f"{date_time_str} {chosen_time}"

    try:
        date_time = datetime.strptime(date_time_str, "%d-%m-%Y %I%p")
    except ValueError:
        print("Invalid date and time format. Please enter a valid date and time.")
        return

    print("─" * 90)
    print(f"Successfully booked {num_tickets} ticket(s) for {movies[movie_index]['title']} at venue {venue_user} on {date_time}!")

    print("─" * 90)
    order_food = input("Would you like to order food? (yes/no): ").lower()
    if order_food == "yes":
        display_food_menu()
        order_food_items(num_tickets)
    elif order_food == "no":
        print("No food ordered.")
    else:
        print("Invalid response. Please enter 'yes' or 'no'.")
    print("─" * 90)

    proceed_to_billing = input("Would you like to proceed to billing? (yes/no): ")
    if proceed_to_billing.lower() == "yes":
        calculate_and_display_bill(num_tickets, date_time, venue_user)

    print()

def display_food_menu():
    print("─" * 90)
    print("Food Menu:")
    for key, item in food_menu.items():
        print(f"{key}. {item['item']} - ${item['price']}")
    print("─" * 90)

def order_food_items(num_tickets):
    total_cost = 0
    global food_cost
    while True:
        item_choice = input("Enter the number of the food item you want to order (press 'q' to quit): ")
        if item_choice.lower() == 'q':
            break
        elif item_choice in food_menu:
            quantity = int(input("Enter the quantity: "))
            total_cost += food_menu[item_choice]['price'] * quantity
        else:
            print("Invalid choice. Please try again.")
    food_cost = total_cost  # Assign total_cost to food_cost

    print(f"Total cost for food: ${total_cost}")

def create_bill(movie_title, num_tickets, ticket_cost, food_cost, total_cost, contact_info, credit_card_number, venue, date_time):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\n" + "-" * 90)
    print("======= Receipt =======")
    print(f"Today's Date and Time: {current_datetime}")
    print(f"Date and Time: {date_time}")
    print(f"Venue: {venue}")
    print(f"Movie: {movie_title}")
    print(f"Number of Tickets: {num_tickets}")
    print(f"Ticket Cost: ${ticket_cost}")
    print(f"Food Cost: ${food_cost}")
    print(f"Total Cost: ${total_cost}")
    print("=======================")
    print("Contact Information: ", contact_info)
    print("Credit Card Number: ", credit_card_number)
    print("=======================")

def calculate_and_display_bill(num_tickets, date_time, venue_user):
    ticket_cost = num_tickets * 10
    total_cost = ticket_cost + food_cost

    print(f"Successfully booked {num_tickets} ticket(s) for {movies[movie_index]['title']} at venue {venue_user} on {date_time}!")
    print(f"Total cost for tickets: ${ticket_cost}")
    print(f"Total cost for food: ${food_cost}")
    print(f"Grand Total: ${total_cost}")

    print("─" * 90)
    while True:
        contact_info = input("Enter your mobile number (10 digits): ")

        if len(contact_info) != 10 or not contact_info.isdigit():
            print("Invalid mobile number. Please enter a 10-digit numeric mobile number.")
        else:
            break

    while True:
        user_otp = input("Enter the OTP received (4 digits): ")

        if len(user_otp) != 4 or not user_otp.isdigit():
            print("Invalid OTP. Please enter a 4-digit numeric OTP.")
        else:
            print("OTP verification successful.")
            print("─" * 90)
            break

    print("─" * 90)
    while True:
        credit_card_number = input("Enter your credit card number (16 digits): ")

        if len(credit_card_number) != 16 or not credit_card_number.isdigit():
            print("Invalid credit card number. Please enter a 16-digit numeric credit card number.")
        else:
            break

    while True:
        credit_card_pin = input("Enter your credit card pin (3 digits): ")

        if len(credit_card_pin) != 3 or not credit_card_pin.isdigit():
            print("Invalid credit card PIN. Please enter a 3-digit numeric credit card PIN.")
        else:
            break

    print("─" * 90)

    create_bill(
        movies[movie_index]['title'],
        num_tickets,
        ticket_cost,
        food_cost,
        total_cost,
        contact_info,
        credit_card_number,
        venue_user,
        date_time
    )

    print("Billing Details:")
    print(f"Contact Information: {contact_info}")
    print(f"Credit Card Number: {credit_card_number}")
    print(f"Total Amount: ${total_cost}")

    print("─" * 90)
    confirmation = input("Confirm and complete the transaction? (yes/no): ")
    if confirmation.lower() == "yes":
        print("Transaction completed. You will receive a confirmation message.")
        print("Thank you for using the Movie Booking Website!")
    else:
        print("Transaction canceled.")
    print("─" * 90)

print("─" * 90)
print("Welcome to the WYDEOS! A movie booking website")
while True:
    print("─" * 90)
    print("1. Register")
    print("2. Login")
    print("3. Book Tickets")
    print("4. Exit")
    print("─" * 90)

    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        register()
    elif choice == "2":
        login()
    elif choice == "3":
        display_movies()
        movie_index = int(input("Enter the movie number: ")) - 1
        num_tickets = int(input("Enter the number of tickets to book: "))
        book_tickets(movie_index, num_tickets)
    elif choice == "4":
        print("Thank you for using the Movie Booking Website!")
        break
    else:
        print("Invalid choice. Please try again.")
