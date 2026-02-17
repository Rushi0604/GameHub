import mysql.connector
import streamlit as st
from method import Methods,Wishlist,Cart,Game_Details
st.set_page_config(layout="wide")

def load_webpage():
    w=Webpage()
    w.home()

class Games(Game_Details):
    def __init__(self):
        self.games_list=[]
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="epic")
        cursor = conn.cursor()
        cursor.execute("select * from games")
        data=cursor.fetchall()
        cursor.close()
        conn.commit()
        for gno,gtype,gname,gprice,gsize,grate,grelease_date,gdescription,gimage,gdiscount in data:
            self.games_list.append(Game_Details(gno,gtype,gname,gprice,gsize,grate,grelease_date,gdescription,gimage,gdiscount))

class Webpage():
    def home(self):
        g=Games()
        st.image("image\gamehub.jpg",width=1550)
        Recommended,Browes,Categories,Sort,Free,Wishlists,Carts,Library,Account=st.tabs(["Recommended","Browes","Categories","Sort","Free Games","Wishlist","Cart","Library","Account"])
        with Recommended:
            Methods.recomanded(g.games_list)
        with Browes:    
            Methods.browes(g.games_list)
        with Categories:
            Methods.category(g.games_list)
        with Sort:
            Methods.sort(g.games_list)
        with Free:
            Methods.free_games(g.games_list)
        with Account:
            Methods.account()
        with Carts:
            cart=Cart()
            cart.show_cart()
        with Wishlists:
            wishlist=Wishlist()
            wishlist.show_wishlist()
        with Library:
            Methods.library()
