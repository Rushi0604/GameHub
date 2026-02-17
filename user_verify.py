import streamlit as st
import mysql.connector
class Verify_User:
    def login():
        data=st.text_input("Enter Email/Phone Number: ")
        password=st.text_input("Enter Password: ",type="password")
        phone,email=False,False
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="epic")
        if data=="Admin@123" and password=="Admin@123":
            st.success("Admin Login Successful")
            st.session_state.page="admin"
            st.rerun()
        if data.endswith("@gmail.com") or data.endswith("@yahoo.com"):
            cursor=conn.cursor()
            cursor.execute("select * from user")
            email=True
            user_info=cursor.fetchall()
            cursor.close()
        else:
            cursor= conn.cursor()
            cursor.execute("select * from user")
            user_info=cursor.fetchall()
            phone=True
            cursor.close()
        d,p=0,0
        for i in user_info:
            if data==str(i[0]):
                d=1
                if password==i[2]:
                    p=1
                    if st.button("Login"):
                        st.success("Login Successfull")
                        if email:
                            st.session_state.email=data
                            if data[1]!=0:
                                st.session_state.phone=i[1]
                        if phone:
                            st.session_state.phone=data
                            if data[0]!=" ":
                                st.session_state.email=i[0]
                        st.session_state.password=password
                        st.session_state.page="webpage"
                        st.rerun()
        if data and password:
            if d==0:
                st.error("Invalid Email/Phone Number")
            if p==0:
                st.error("Invalid Password")

    def register():
        data=st.text_input("Enter Email/Phone Number: ")
        password=st.text_input("Enter Password: ",type="password")
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="epic")
        if data.endswith("@gmail.com") or data.endswith("@yahoo.com"):
            if password and data:
                if Verify_User.verify_password(password):
                    cursor=conn.cursor()
                    cursor.execute("insert into user (user_email,user_phone,password) values (%s,%s,%s)",(data," ",password))
                    conn.commit()
                    cursor.close()
                    if st.button("Register"):
                        st.success("Registration Successful")    
                        st.session_state.email=data
                        st.session_state.password=password
                        st.session_state.page="webpage"
                        st.rerun()
                elif password!="":
                    st.error("Password must be at least 8 characters long and contain at least one special character (@#!?$&)xxxxx")
        else:
            if data.isdigit() and len(data)==10:
                if Verify_User.verify_password(password):
                    cursor=conn.cursor()
                    cursor.execute("insert into user (user_email,user_phone,password) values (%s,%s,%s)",(" ",data,password))
                    conn.commit()
                    cursor.close()
                    if st.button("Register"):
                        st.success("Registration Successful")
                        st.session_state.email=data
                        st.session_state.password=password
                        st.session_state.page="webpage"
                        st.rerun()
                elif password!="":
                    st.error("Password must be at least 8 characters long and contain at least one special character (@#!?$&)")
            else:
                st.error("Invalid Phone Number")

    def verify_password(password):
        s,d=0,0
        for i in password:
            if i in "@#!?$&":
                s+=1
            elif i.isdigit():
                d+=1
        if s>0 and d>0 and len(password)>8:
            return True