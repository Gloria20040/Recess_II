print("WORLD CUP 2026 WINNER !!!")

while True:
    country = input("\nEnter a country (or type 'exit' to quit): ")

    if country.lower() == "exit":
        print("Program ended.")
        break     

    if country == "":
        print("You did not enter a country.")
        continue   

    if country.lower() == "uganda":
        pass        

    print(f"{country} is predicted to win the 2026 World Cup!")

    answer = input("Do you want to try another country? (yes/no): ")

    if answer.lower() == "no":
        print("Thank you for using the simulator.")
        break