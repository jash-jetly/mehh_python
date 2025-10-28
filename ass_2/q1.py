while True:
    response = input("Have you submitted your assignment? ").lower()
    if response == "done":
        print("Great job! Finally submitted!")
        break
    else:
        print("Still waiting... Submit it already!")

