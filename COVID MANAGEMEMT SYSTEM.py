import mysql.connector
import matplotlib.pyplot as plt
ageb=list()
dateb=list()
def visualizeData():
    mycursor.execute("select * from patients")
    for v in mycursor:
        t_idv, namev, agev, genderv, datev=v
        ageb.append(agev)
        dateb.append(datev)
    plt.xlabel("AGE OF PATIENTS")
    plt.ylabel("DATE OF BECOMING COVID POSITIVE")
    plt.bar(ageb,dateb)
    plt.show()



print("************************************************************")
print("          WELCOME TO COVID MANAGEMENT SYSTEM                ")
print("************************************************************")
mydb=mysql.connector.connect(host="localhost",user="root",passwd="123456")
mycursor=mydb.cursor()
mycursor.execute("create database if not exists covid_management")
mycursor.execute("use covid_management")
mycursor.execute("create table if not exists patients(sno varchar(25) not null,name varchar(25) not null, age varchar(25) not null, GENDER char(1) not null, date date not null)")
mycursor.execute("create table if not exists login(admin varchar(25) not null,password varchar(25) not null)")
mycursor.execute("create table if not exists sno(patient varchar(25))")
#mycursor.execute("insert into login values('utkarsh','1234')")
mycursor.execute("select * from sno")
z=0
for i in mycursor:
    z=1
if z==0:
    mycursor.execute("insert into sno values('0','0')")
mydb.commit()
j=0
mycursor.execute("select * from login")
for i in mycursor:
    j=1
if j==0:
    mycursor.execute("insert into login values('admin','ut')")
    mydb.commit()
loop1='y'
while(loop1=='y') or (loop1=='Y'):
    print("_____________")
    print("1.Admin")
    print("2.Patient")
    print("3.Exit")
    print("_____________")
    ch1=int(input("Enter your choice"))
    if(ch1==1):
        pas=input("Enter your password")
        mycursor.execute("select * from login")
        for i in mycursor:
            username,password=i
        if (pas==password):
            loop2='n'
            while (loop2=='n') or (loop2=='N'):
                print("_________________________")
                print("1.Add  patients")
                print("2.Display patients records")
                print("3.change password")
                print("4.Remove patients")
                print("5.Visualize patient data on age vs date of covid positive")
                print("6.Log out")
                print("___________________________")
                ch2=int(input("enter your choice:"))
                if(ch2==1):
                    loop3='y'
                    while (loop3=='y') or (loop3=='Y'):
                        name=input("Enter patient name")
                        age=input("Enter patient age")
                        gender=input("Enter patient gender")
                        date=input("Enter date of becoming covid positive")
                        mycursor.execute("select* from sno")
                        for i in mycursor:
                            patient,staff=i
                            patient=int(patient)+1
                        mycursor.execute("insert into patients values('"+str(patient)+"','"+name+"','"+age+"','"+gender+"','"+date+"')")
                        mycursor.execute("update sno set patient='"+str(patient)+"'")
                        mydb.commit()
                        print("Data of patient has been saved successfully.....")
                        mycursor.execute("select * from patients")
                        t=0
                        for i in mycursor:
                            t+=1
                            t_id1,name1,age1,gender1,date1=i
                        print(f"Total number of corona infected patients--> {patient}")
                        print(f"Active corona cases--> {t}")
                        print(f"This patient with id {t_id1} will be quarantine upto 14 days from {date1}")
                        loop3=input("Due you want to enter more patients(y/n):")
                    loop2=input("Do you want to logout (y/n):")
                elif(ch2==2):
                    idd=input("Enter patient ID:")
                    t_id2,name2,age2,gender2,date2=["","","","",""]
                    mycursor.execute("select * from patients where sno='"+idd+"'")
                    for i in mycursor:
                        t_id2,name2,age2,gender2,date2=i
                    print("|  ID  |  NAME  |  AGE  |  GENDER  |  COVID-19 POSITIVE DATE  |")
                    print(f"|  {t_id2}  |  {name2}  |  {age2}  |  {gender2}  |  {date2}  |")
                elif(ch2==3):
                    pas=input("Enter old password:")
                    mycursor.execute("select * from login")
                    for i in mycursor:
                        username,password=i
                    if(pas==password):
                        npas=input("Enter new password")
                        mycursor.execute("update login set password='"+npas+"'")
                        mydb.commit()
                    else:
                        print("You have entered a wrong password")
                elif(ch2==4):
                    loop3='y'
                    while(loop3=='y') or (loop3=='Y'):
                        idd=input("Enter patient ID:")
                        mycursor.execute("delete from patients where sno='"+idd+"'")
                        mydb.commit()
                        print("Patient has been successfully removed......")
                        loop3=input("Do you want to remove more patient(y/n):")
                elif(ch2==5):
                    visualizeData()
                elif(ch2==6):
                    break
    elif(ch1==2):
        print("Thankyou for coming forward for your test.....")
        icough=input("Are you feeling cough (y/n):").lower()
        dry_cough='n'
        cough='n'
        if (icough=='y') or (icough=='Y'):
            dry_cough=input("Are you feeling dry cough (y/n):").lower()
            cough=input("Are you having normal cough (y/n):").lower()
        sneeze=input("Are you feeling sneeze (y/n):").lower()
        pain=input("Are you feeling pain in your body (y/n):").lower()
        weakness=input("Are you feeling weakness (y/n):").lower()
        mucus=input("Are you feeling any mucus (y/n):").lower()
        itemp=int(input("Enter your body temperature: "))
        if(itemp<=100):
            temp='low'
        else:
            temp='high'
        breath=input("Are you having any breathing difficulty (y/n) : ")
        if (dry_cough=='y' and sneeze=='y' and pain=='y' and weakness=='y' and mucus=='y' and temp=='high' and breath=='y'):
            print("Sorry to say but according to us you are corona positive....")
            name=input("Enter your name: ")
            age=input("Enter your age: ")
            gender=input("Enter your gender(m/f): ")

            mycursor.execute("select * from sno")
            for i in mycursor:
                patient,staff=i
                patient=int(patient)+1
            mycursor.execute("insert into patients values('"+str(patient)+"','"+name+"','"+age+"','"+gender+"',now())")
            mycursor.execute("update sno set patient='"+str(patient)+"'")
            mydb.commit()
            print("Patient data has been saved successfully....")
            print(f"Total no. of corona infected persons ----> {patient}")
            mycursor.execute("select * from patients")
            t=0
            for i in mycursor:
                t+=1
            print(f"Active corona cases--> {t}")
            mycursor.execute("select * from patients")
            for i in mycursor:
                t_id5,name5,age5,gender5,date5=i
            print(f"Patient with id {t_id5} will be quarantine for 14 days from {date5}")

        elif (dry_cough=='y' and sneeze=='y' and pain=='n' and weakness=='n' and mucus=='n' and temp=='low' and breath=='n'):
            print("Nothing to worry it is just due to Air pollution..")
        elif (dry_cough=='y' and sneeze=='y' and pain=='n' and weakness=='n' and mucus=='y' and temp=='low' and breath=='n'):
            print("nothing to worry it is just a common cold....")
        else:
            print("You are not corona positive, if you are feeling something wrong, you just need some rest..  ")
            print("Also you can consult to a doctor")
    elif(ch1==3):
        break








