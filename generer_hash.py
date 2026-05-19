from werkzeug.security import generate_password_hash
passord = input("Skriv inn admin-passord: ")
print(generate_password_hash(passord))
