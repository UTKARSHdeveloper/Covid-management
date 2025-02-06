import mysql.connector
import matplotlib.pyplot as plt

def visualizeData():
    mycursor.execute("SELECT age, date FROM patients")
    ageb = []
    dateb = []
    
    for age, date in mycursor:
        ageb.append(int(age))  # Convert age to integer
        dateb.append(date.strftime("%Y-%m-%d"))  # Convert date to string format
    
    plt.xlabel("AGE OF PATIENTS")
    plt.ylabel("DATE OF BECOMING COVID POSITIVE")
    plt.bar(ageb, dateb)
    plt.xticks(rotation=45)  # Improve readability
    plt.show()

# Database Connection
mydb = mysql.connector.connect(host="localhost", user="root", passwd="123456")
mycursor = mydb.cursor()

# Ensure the database exists
mycursor.execute("CREATE DATABASE IF NOT EXISTS covid_management")
mycursor.execute("USE covid_management")

# Table Creation
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        sno INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(25) NOT NULL,
        age INT NOT NULL,
        gender CHAR(1) NOT NULL,
        date DATE NOT NULL
    )
""")

mycursor.execute("""
    CREATE TABLE IF NOT EXISTS login (
        admin VARCHAR(25) NOT NULL,
        password VARCHAR(25) NOT NULL
    )
""")

# Initialize Login Table
mycursor.execute("SELECT COUNT(*) FROM login")
if mycursor.fetchone()[0] == 0:
    mycursor.execute("INSERT INTO login (admin, password) VALUES (%s, %s)", ('admin', 'ut'))
    mydb.commit()

while True:
    print("_____________")
    print("1. Admin")
    print("2. Patient")
    print("3. Exit")
    print("_____________")
    
    try:
        ch1 = int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        continue

    if ch1 == 1:
        pas = input("Enter your password: ")
        mycursor.execute("SELECT password FROM login")
        stored_password = mycursor.fetchone()
        
        if stored_password and pas == stored_password[0]:
            while True:
                print("_________________________")
                print("1. Add Patients")
                print("2. Display Patient Record")
                print("3. Change Password")
                print("4. Remove Patient")
                print("5. Visualize Patient Data (Age vs Date)")
                print("6. Log out")
                print("_________________________")
                
                try:
                    ch2 = int(input("Enter your choice: "))
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue

                if ch2 == 1:
                    name = input("Enter patient name: ")
                    age = input("Enter patient age: ")
                    gender = input("Enter patient gender (M/F): ")
                    date = input("Enter date of becoming COVID positive (YYYY-MM-DD): ")

                    mycursor.execute("INSERT INTO patients (name, age, gender, date) VALUES (%s, %s, %s, %s)",
                                     (name, age, gender, date))
                    mydb.commit()
                    print("Patient record saved successfully.")

                elif ch2 == 2:
                    idd = input("Enter patient ID: ")
                    mycursor.execute("SELECT * FROM patients WHERE sno = %s", (idd,))
                    patient = mycursor.fetchone()
                    
                    if patient:
                        print("| ID | Name | Age | Gender | COVID-19 Positive Date |")
                        print(f"| {patient[0]} | {patient[1]} | {patient[2]} | {patient[3]} | {patient[4]} |")
                    else:
                        print("Patient not found.")

                elif ch2 == 3:
                    old_pass = input("Enter old password: ")
                    mycursor.execute("SELECT password FROM login")
                    stored_password = mycursor.fetchone()

                    if stored_password and old_pass == stored_password[0]:
                        new_pass = input("Enter new password: ")
                        mycursor.execute("UPDATE login SET password = %s", (new_pass,))
                        mydb.commit()
                        print("Password updated successfully.")
                    else:
                        print("Incorrect password.")

                elif ch2 == 4:
                    idd = input("Enter patient ID: ")
                    mycursor.execute("DELETE FROM patients WHERE sno = %s", (idd,))
                    mydb.commit()
                    print("Patient record removed successfully.")

                elif ch2 == 5:
                    visualizeData()

                elif ch2 == 6:
                    break  # Logout
                
                else:
                    print("Invalid choice.")

        else:
            print("Incorrect password.")

    elif ch1 == 2:
        print("Thank you for coming forward for your test.")
        icough = input("Are you feeling cough (y/n): ").lower()
        dry_cough, cough = 'n', 'n'

        if icough == 'y':
            dry_cough = input("Are you feeling dry cough (y/n): ").lower()
            cough = input("Are you having normal cough (y/n): ").lower()

        sneeze = input("Are you feeling sneeze (y/n): ").lower()
        pain = input("Are you feeling pain in your body (y/n): ").lower()
        weakness = input("Are you feeling weakness (y/n): ").lower()
        mucus = input("Are you feeling any mucus (y/n): ").lower()

        try:
            itemp = int(input("Enter your body temperature: "))
        except ValueError:
            print("Invalid temperature input.")
            continue

        temp = 'high' if itemp > 100 else 'low'
        breath = input("Are you having any breathing difficulty (y/n): ").lower()

        if dry_cough == 'y' and sneeze == 'y' and pain == 'y' and weakness == 'y' and mucus == 'y' and temp == 'high' and breath == 'y':
            print("You are likely COVID positive. Please get tested at the nearest health center.")
        elif dry_cough == 'y' and sneeze == 'y' and pain == 'n' and weakness == 'n' and mucus == 'n' and temp == 'low' and breath == 'n':
            print("Likely due to air pollution.")
        elif dry_cough == 'y' and sneeze == 'y' and mucus == 'y' and temp == 'low' and breath == 'n':
            print("It seems like a common cold.")
        else:
            print("You are not COVID positive. If you feel unwell, please consult a doctor.")

    elif ch1 == 3:
        print("Exiting system. Stay safe!")
        break

    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
