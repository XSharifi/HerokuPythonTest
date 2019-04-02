#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os, sys
from flask import Flask, request, redirect
from flask_bcrypt import Bcrypt
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from queue import Queue
from threading import Thread
import json
import ast

import emoji
from collections import defaultdict


class AutoTree( dict ):
    def __missing__(self, key):
        value = self[key] = type( self )()
        return value


global Main_Dict
global temp_Main_Dict
global Temp_Dict
global Base_for_Selling
global Accepted_Bidding
global Base_for_Selling
global detemined_Base_sell
global Backage_Number_of_seller
global Backage_Number_of_buyer
global Dict_of_Username_id
global Dict_id_of_seller
global Dict_id_of_buyer
global temp_Dict_id_of_seller
global temp_Dict_id_of_buyer
global Dict_of_id_to_Username

Main_Dict = AutoTree()
Dict_id_of_buyer = AutoTree()
Dict_id_of_seller = AutoTree()
temp_Main_Dict = defaultdict( dict )
temp_Dict_id_of_seller = defaultdict( dict )
temp_Dict_id_of_buyer = defaultdict( dict )

Temp_Dict = {}
Dict_of_Username_id = {}
Dict_of_id_to_Username = {}
Dict_of_id_to_Username = {}

Backage_Number_of_seller = Backage_Number_of_buyer = 1
detemined_Base_sell = 0
Base_for_Selling = 1

TOKEN = "873380531:AAEhMfHcaTC8YwrqVeIyANJl7uqd0sZ8tFk"  # broker_navasan_bot
webhook_address = "https://broker-navasan-bot.herokuapp.com/" + TOKEN

bot = Bot( TOKEN )

update_queue = Queue()

dp = Dispatcher( bot, update_queue )

# Initialize application
app = Flask( __name__, static_folder=None )

# app configuration
app_settings = os.getenv( 'APP_SETTINGS', 'app.config.DevelopmentConfig' )
app.config.from_object( app_settings )

# Initialize Bcrypt
bcrypt = Bcrypt( app )


# ------------ function for doing something ------------------------------------


def Reset_all_the_data():
    global Base_for_Selling
    global Accepted_Bidding
    global Base_for_Selling
    global detemined_Base_sell
    global Backage_Number_of_seller
    global Backage_Number_of_buyer
    global Dict_of_Username_id
    global start_time
    global Main_Dict
    global Temp_Dict
    global Dict_id_of_seller
    global Dict_of_id_to_Username
    global Dict_id_of_buyer
    global temp_Dict_id_of_seller
    global temp_Dict_id_of_buyer
    global temp_Main_Dict

    temp_Main_Dict = defaultdict( dict )
    temp_Dict_id_of_seller = defaultdict( dict )
    temp_Dict_id_of_buyer = defaultdict( dict )
    Main_Dict = defaultdict( dict )
    Dict_id_of_buyer = defaultdict( dict )
    Dict_id_of_seller = defaultdict( dict )

    Dict_of_id_to_Username = {}
    Main_Dict = {}
    Temp_Dict = {}
    Dict_id_of_seller = {}
    Base_for_Selling = Accepted_Bidding = 1
    Backage_Number_of_seller = Backage_Number_of_buyer = 1
    Dict_of_Username_id = {}
    detemined_Base_sell = 0


def find_at(message):
    for text in message:
        if '@' in text:
            return text


def storing_Dict_of_id_to_Username(username, id):
    Dict_of_id_to_Username[id] = username


def calculating_for_int_number(texts, update):
    temp_price = temp_number_of_package = 0
    try:
        temp = [int( s ) for s in texts.split() if s.isdigit()]

        if len( temp ) == 1 and temp[0] <= 10 and temp[0] > 0:
            update.message.reply_text( "لطفا در وارد کردن متن توجه نماید- متن شما بدون قیمت یا مبلغ پیشنهادی است" )
            return
        elif len( temp ) == 1 and temp[0] > 10:
            temp_number_of_package = 1
            temp_price = temp[0]
        elif len( temp ) == 2:
            if temp[0] > temp[1] and temp[1] > 0:
                temp_number_of_package = temp[1]
                temp_price = temp[0]
            elif temp[0] < temp[1] and temp[0] > 0:
                temp_number_of_package = temp[0]
                temp_price = temp[1]

        return temp_price, temp_number_of_package
    except Exception:
        update.message.reply_text( "لطفا در وارد کردن متن توجه نماید" )
        return


def calculating_for_int_number_selling(texts, update):
    temp_price = temp_number_of_package = 0
    try:
        temp = [int( s ) for s in texts.split() if s.isdigit()]

        if len( temp ) == 1 and temp[0] <= 10 and temp[0] > 0:
            update.message.reply_text( "لطفا در وارد کردن متن توجه نماید- متن شما بدون قیمت یا مبلغ پیشنهادی است" )
            return
        elif len( temp ) == 1 and temp[0] > 10:
            temp_number_of_package = 1
            temp_price = temp[0]
        elif len( temp ) == 2:
            if temp[0] > temp[1]:
                temp_number_of_package = temp[1]
                temp_price = temp[0]
            elif temp[0] < temp[1]:
                temp_number_of_package = temp[0]
                temp_price = temp[1]

        return temp_price, temp_number_of_package
    except Exception:
        update.message.reply_text( "لطفا در وارد کردن متن توجه نماید" )
        return


def calculating_for_int_number_of_Buyer(texts, update, last_offer_id, Dict_message):
    temp_price = temp_number_of_package = 0

    print( 'package number of seller in calculating_for_int_number_of_Buyer : ',
           Dict_id_of_seller[str( Dict_message['message']['from']['id'] )][str( last_offer_id )]['package_number'] )
    print( 'price in calculating_for_int_number_of_Buyer : ',
           Dict_id_of_seller[str( Dict_message['message']['from']['id'] )][str( last_offer_id )][
               'seller_price_offered'] )

    try:
        temp = [int( s ) for s in texts.split() if s.isdigit()]

        if len( temp ) == 1 and temp[0] <= 10:
            update.message.reply_text( "لطفا در وارد کردن متن توجه نماید- متن شما بدون قیمت یا مبلغ پیشنهادی است" )
            return

        elif len( temp ) == 1 and temp[0] > 10:
            temp_number_of_package = \
            Dict_id_of_seller[str( Dict_message['message']['from']['id'] )][str( last_offer_id )]['package_number']
            temp_price = temp[0]
        elif len( temp ) == 2:
            if temp[0] > temp[1]:
                temp_number_of_package = temp[1]
                temp_price = temp[0]
            else:
                temp_number_of_package = temp[0]
                temp_price = temp[1]

        else:

            temp_number_of_package = \
            Dict_id_of_seller[str( Dict_message['message']['from']['id'] )][str( last_offer_id )]['package_number']
            temp_price = Dict_id_of_seller[str( Dict_message['message']['from']['id'] )][str( last_offer_id )][
                'seller_price_offered']

        return temp_price, temp_number_of_package
    except Exception:
        print( 'comming to new exception' )
        temp_number_of_package = Dict_id_of_seller[str( Dict_message['message']['from']['id'] )][str( last_offer_id )][
            'package_number']
        temp_price = Dict_id_of_seller[str( Dict_message['message']['from']['id'] )][str( last_offer_id )][
            'seller_price_offered']

        return temp_price, temp_number_of_package


def calculating_for_int_number_of_seller(texts, update, last_offer_id, Dict_message):
    temp_price = temp_number_of_package = 0

    try:
        temp = [int( s ) for s in texts.split() if s.isdigit()]

        if len( temp ) == 1 and temp[0] <= 10:
            update.message.reply_text( "لطفا در وارد کردن متن توجه نماید- متن شما بدون قیمت یا مبلغ پیشنهادی است" )
            return

        elif len( temp ) == 1 and temp[0] > 10:
            temp_number_of_package = \
            Dict_id_of_buyer[str( Dict_message['message']['from']['id'] )][str( last_offer_id )]['package_number']
            temp_price = temp[0]
        elif len( temp ) == 2:
            if temp[0] > temp[1]:
                temp_number_of_package = temp[1]
                temp_price = temp[0]
            else:
                temp_number_of_package = temp[0]
                temp_price = temp[1]

        else:

            temp_number_of_package = \
            Dict_id_of_buyer[str( Dict_message['message']['from']['id'] )][str( last_offer_id )]['package_number']
            temp_price = Dict_id_of_buyer[str( Dict_message['message']['from']['id'] )][str( last_offer_id )][
                'buyer_price_offered']

        return temp_price, temp_number_of_package
    except Exception:
        print( 'comming to new exception' )

        temp_number_of_package = Dict_id_of_buyer[str( Dict_message['message']['from']['id'] )][str( last_offer_id )][
            'package_number']
        temp_price = Dict_id_of_buyer[str( Dict_message['message']['from']['id'] )][str( last_offer_id )][
            'buyer_price_offered']

        return temp_price, temp_number_of_package


def add_items_to_Main_Dict(ID_of_seller, package_number, price_of_agreement, ID_of_buyer, loss_profit_of_seller,
                           loss_profit_of_buyer, username_of_seller, username_of_buyer, Id_of_Buyer, Id_of_seller):
    global Main_Dict
    global Temp_Dict
    id_transaction_of_seller = id_transaction_of_buyer = 1

    if Main_Dict.get( str( ID_of_seller ) ):
        id_transaction_of_seller = (len( Main_Dict[str( ID_of_seller )] )) + 1
    else:
        id_transaction_of_seller = 1

    if Main_Dict.get( str( ID_of_buyer ) ):
        id_transaction_of_buyer = (len( Main_Dict[str( ID_of_buyer )] )) + 1
    else:
        id_transaction_of_buyer = 1

    Main_Dict[str( ID_of_seller )][id_transaction_of_seller] = {'package_number': package_number,
                                                                'price_of_agreement': price_of_agreement,
                                                                'loss_profit': loss_profit_of_seller,
                                                                'alternative_username': username_of_buyer,
                                                                'Id_of_alternative': Id_of_Buyer,
                                                                'Type_of_transaction': 'selling'}

    Main_Dict[str( ID_of_buyer )][id_transaction_of_buyer] = {'package_number': package_number,
                                                              'price_of_agreement': price_of_agreement,
                                                              'loss_profit': loss_profit_of_buyer,
                                                              'alternative_username': username_of_seller,
                                                              'Id_of_alternative': Id_of_seller,
                                                              'Type_of_transaction': 'buying'}


def complete_items_to_Temp_Dict(username_of_seller, package_number_of_buyer, price_of_agreement, username_of_buyer,
                                loss_profit_of_seller, loss_profit_of_buyer):
    global Main_Dict
    global Temp_Dict

    Temp_Dict[username_of_seller] = {'price_of_agreement': price_of_agreement, 'username_of_buyer': username_of_buyer,
                                     'package_number_of_buyer': package_number_of_buyer,
                                     'loss_profit_of_seller': loss_profit_of_seller,
                                     'loss_profit_of_buyer': loss_profit_of_buyer}


def add_item_to_Temp_Dict(username_of_seller, suggested_price, package_number_of_seller):
    global Main_Dict
    global Temp_Dict

    Temp_Dict[username_of_seller] = {'package_number_of_seller': package_number_of_seller,
                                     'suggested_price': suggested_price}


def del_item_from_Temp_Dict(username_of_seller):
    global Main_Dict
    global Temp_Dict
    if Temp_Dict['username_of_seller']:
        del Temp_Dict['username_of_seller']


def storing_info_of_seller(text_id, package_number, message_id, valid, Bidder, status, id_offer, seller_price_offered):
    Dict_id_of_seller[text_id][str( id_offer )] = {'package_number': package_number, 'message_id': message_id,
                                                   'valid': valid, 'Bidders': Bidder, 'status': status,
                                                   'seller_price_offered': seller_price_offered}
    print( 'all the data of seller is stored' )


def storing_info_of_buyer(text_id, package_number, message_id, valid, Bidder, status, id_offer, buyer_price_offered):
    Dict_id_of_buyer[text_id][str( id_offer )] = {'package_number': package_number, 'message_id': message_id,
                                                  'valid': valid, 'Bidders': Bidder, 'status': status,
                                                  'buyer_price_offered': buyer_price_offered}
    print( 'all the data of buyer is stored' )


def calculating_for_package_number(texts):
    if '-' in texts:
        temp = [int( s ) for s in texts.split( "-" ) if s.isdigit()]
        if temp[0]:
            return temp[0]
    else:
        return False


def calculating_loss_and_profit_of_seller_and_buyer(base, agreement_price, agreement_package):
    loss_and_profit_of_buyer = (base - agreement_price) * 10000

    if (loss_and_profit_of_buyer < -2000000):

        # agreement_price = (2000000 / (agreement_package * 10000)) + base
        loss_and_profit_of_buyer = -2000000 * agreement_package
        loss_and_profit_of_seller = 2000000 * agreement_package

    elif loss_and_profit_of_buyer > 2000000:

        # agreement_price = (-2000000 / (agreement_package * 10000)) + base
        loss_and_profit_of_buyer = 2000000 * agreement_package
        loss_and_profit_of_seller = -2000000 * agreement_package

    else:

        loss_and_profit_of_seller = (agreement_price - base) * agreement_package * 10000
        loss_and_profit_of_buyer = (base - agreement_price) * agreement_package * 10000

    # loss_and_profit_of_seller = (agreement_price - base) * agreement_package * 10000
    # if (loss_and_profit_of_seller < 0 and loss_and_profit_of_seller < -2000000):
    #     agreement_price = (-2000000 / (agreement_package * 10000)) - base
    #
    # elif loss_and_profit_of_seller>2000000:
    #     agreement_price = (2000000 / (agreement_package * 10000)) - base

    return agreement_price, loss_and_profit_of_seller - 10000 * agreement_package, loss_and_profit_of_buyer - 10000 * agreement_package


def complete_accounting_process(Base_price_for_Selling):
    for key, value in Main_Dict.items():
        print( key )
        for i in range( len( Main_Dict[str( key )] ) ):
            if Main_Dict[str( key )][str( i + 1 )]['loss_profit'] == 0:
                print( 'comming to new state in base processing ' )
                temp_agreement_price, loss_profit_of_seller, loss_profit_of_buyer = calculating_loss_and_profit_of_seller_and_buyer(
                    Base_price_for_Selling, Main_Dict[str( key )][str( i + 1 )]['price_of_agreement'],
                    Main_Dict[str( key )][str( i + 1 )]['package_number'] )

                print( 'temp_agreement_price, loss_profit_of_seller, loss_profit_of_buyer', temp_agreement_price,
                       loss_profit_of_seller, loss_profit_of_buyer )

                if Main_Dict[str( key )][str( i + 1 )]['Type_of_transaction'] == 'selling':
                    Main_Dict[str( key )][str( i + 1 )]['loss_profit'] = loss_profit_of_seller
                else:
                    Main_Dict[str( key )][str( i + 1 )]['loss_profit'] = loss_profit_of_buyer

                Main_Dict[str( key )][str( i + 1 )]['price_of_agreement'] = temp_agreement_price

    print( Main_Dict )


def calculating_for_base_price(txts, update):
    try:
        temp = [int( s ) for s in txts.split() if s.isdigit()]
        return temp[0]
    except Exception:
        update.message.reply_text( 'لطفا در وارد کردن قیمت پایه توجه نمایید، پیام شما بدون مقدار عددی قیمت پایه است' )
        return


def text_analysing(txts, Dict_message, update):
    texts = txts.split()
    global Base_for_Selling
    global Accepted_Bidding
    global detemined_Base_sell
    global Backage_Number_of_seller
    global Backage_Number_of_buyer
    global Main_Dict
    global Temp_Dict
    global Dict_id_of_seller
    global Dict_of_Username_id
    global Dict_of_id_to_Username
    global Dict_id_of_buyer
    global temp_Dict_id_of_seller
    global temp_Dict_id_of_buyer
    global temp_Main_Dict

    for text in texts:

        try:

            if text == "ف":  # text of sellerd

                try:
                    if Dict_message['message']['reply_to_message']['from']['id'] is not None:

                        temp_text = Dict_message['message']['reply_to_message']['text']  # text of buyer

                        print( temp_text )
                        temp_texts = temp_text.split()
                        print( temp_texts )
                        for txt in temp_texts:

                            if txt == 'خ':

                                buyer_id = Dict_message['message']['reply_to_message']['from']['id']
                                filepath = os.getcwd() + '//' + 'Dict_id_of_buyer.txt'
                                print( 'file path in heroku : ', filepath )
                                ls_file = os.listdir( os.getcwd() )

                                print( 'Checking for text file', ls_file )
                                if os.path.exists( 'Dict_id_of_buyer.txt' ):

                                    with open( filepath, 'r' ) as myfile:
                                        Dict_id_of_buyer = json.loads( myfile.read() )
                                        myfile.close()

                                    if Dict_id_of_buyer.get( str( buyer_id ) ) is not None:

                                        last_offer_id = len( Dict_id_of_buyer[str( buyer_id )] )
                                        print( 'last_offer_id : ', last_offer_id )
                                        print( 'after it be read by me', Dict_id_of_buyer )

                                        if Dict_id_of_buyer[str( buyer_id )][str( last_offer_id )][
                                            'status'] == 'unknown':

                                            if Dict_id_of_buyer[str( buyer_id )][str( last_offer_id )][
                                                'Bidders'] == 'nonbidder':

                                                Dict_id_of_buyer[str( buyer_id )][str( last_offer_id )][
                                                    'Bidders'] = str( Dict_message['message']['from']['id'] )
                                            else:
                                                Dict_id_of_buyer[str( buyer_id )][str( last_offer_id )]['Bidders'] = \
                                                    Dict_id_of_buyer[str( buyer_id )][str( last_offer_id )][
                                                        'Bidders'] + ',' + str(
                                                        Dict_message['message']['from']['id'] )

                                            print( Dict_id_of_buyer )
                                            with open( filepath, 'w+' ) as myfile1:
                                                myfile1.write( json.dumps( Dict_id_of_buyer ) )
                                                myfile1.close()


                                        elif Dict_id_of_buyer[str( seller_id )][str( last_offer_id )][
                                            'status'] == 'sold':
                                            update.message.reply_text(
                                                "فروشنده گرامی بسته ای که شما رپلای کرده اید قبلا فرخته شده است، لطفا بشتر دقت کنید " )
                                            return

                                        elif Dict_id_of_buyer[str( seller_id )][str( last_offer_id )][
                                            'status'] == 'changed':
                                            update.message.reply_text(
                                                "فروشنده بسته ای که شما رپلای کرده اید قبلا توسط خریدار تغییر یافته و یک پیشنهاد جدیدی را جایگزین آن کرده است لطفا بیشتر دقت کنید " )
                                            return



                                    else:
                                        update.message.reply_text(
                                            "فروشنده گرامی پیغام که شما رپلایی کرده اید، مربوط به خریدار نیست " )
                                        return


                                else:
                                    update.message.reply_text(
                                        "فروشنده گرامی پیغام که شما رپلایی کرده اید، مربوط به خریدار نیست " )
                                    return

                except KeyError:
                    # for this item it needs to be checked that it could not be replyed to check the selleing of goods
                    # but for selleing of vise the versa it means: buyer be a bidder and after that the seller accept the the bidd of buyer then it be delt

                    print( 'state of determined base sell : ', detemined_Base_sell )
                    price_for_selling, Backage_Number_of_seller = calculating_for_int_number_selling( txts, update )
                    print( 'price and package of seller : ', price_for_selling, Backage_Number_of_seller )
                    # text_id,package_number,message_id,valid,Bidder,status +++ offer_id

                    seller_id = str( Dict_message['message']['from']['id'] )
                    message_id = str( Dict_message['message']['message_id'] )
                    print( 'message of seller: ', message_id )

                    filepath = os.getcwd() + '//' + 'Dict_id_of_seller.txt'
                    print( 'file path in heroku :', filepath )
                    ls_file = os.listdir( os.getcwd() )
                    print( 'befor creating new text file', ls_file )
                    # if Dict_id_of_seller.get(str(seller_id)) is not None: # may be that [message.json['from']['id']]['valid']

                    if os.path.isfile( filepath ):
                        with open( filepath, 'r' ) as myfile:
                            Dict_id_of_seller = json.loads( myfile.read() )
                            Dict_id_of_seller = AutoTree( Dict_id_of_seller )
                            myfile.close()

                        if Dict_id_of_seller.get( str( seller_id ) ) is not None:

                            print( '-------Dict_id_of_seller :', Dict_id_of_seller )
                            last_offer_id = len( Dict_id_of_seller[str( Dict_message['message']['from']['id'] )] )

                            if Dict_id_of_seller[str( seller_id )][str( last_offer_id )]['valid'] == True:
                                # this if could be included status of 'unknown':
                                Dict_id_of_seller[str( seller_id )][str( last_offer_id )]['status'] = 'changed'
                                Dict_id_of_seller[str( seller_id )][str( last_offer_id )]['valid'] = False
                                storing_info_of_seller( str( seller_id ), Backage_Number_of_seller, message_id, True,
                                                        'nonbidder', 'unknown', last_offer_id + 1, price_for_selling )


                            elif Dict_id_of_seller[str( seller_id )][str( last_offer_id )]['valid'] == False:

                                if Dict_id_of_seller[str( seller_id )][str( last_offer_id )]['status'] == 'sold':
                                    storing_info_of_seller( str( seller_id ), Backage_Number_of_seller, message_id,
                                                            True, 'nonbidder', 'unknown', last_offer_id + 1,
                                                            price_for_selling )

                            with open( filepath, 'w+' ) as myfile1:
                                myfile1.write( json.dumps( Dict_id_of_seller ) )
                                myfile1.close()

                            print( Dict_id_of_seller )

                        else:

                            print( 'After converting :', type( Dict_id_of_seller ) )

                            print( 'new seller added to list 1 : ' + str( seller_id ) )
                            print( '**** +++++++++ ***', Dict_id_of_seller )
                            storing_info_of_seller( str( seller_id ), Backage_Number_of_seller, message_id, True,
                                                    'nonbidder', 'unknown', 1, price_for_selling )
                            print( '*******', Dict_id_of_seller )

                            with open( filepath, 'w+' ) as myfile1:
                                myfile1.write( json.dumps( Dict_id_of_seller ) )
                                myfile1.close()
                            ls_file = os.listdir( os.getcwd() )

                            print( 'After creating new text file', ls_file )
                            with open( filepath, 'r' ) as myfile:
                                Dict_id_of_seller = json.loads( myfile.read() )
                                print( '---------->', Dict_id_of_seller )
                                myfile.close()

                    else:

                        print( 'new seller added to list 2 : ' + str( seller_id ) )
                        storing_info_of_seller( str( seller_id ), Backage_Number_of_seller, message_id, True,
                                                'nonbidder', 'unknown', 1, price_for_selling )
                        print( '*******', Dict_id_of_seller )

                        with open( filepath, 'w+' ) as myfile1:
                            myfile1.write( json.dumps( Dict_id_of_seller ) )
                            myfile1.close()
                        ls_file = os.listdir( os.getcwd() )

                        print( 'After creating new text file', ls_file )
                        with open( filepath, 'r' ) as myfile:
                            Dict_id_of_seller = json.loads( myfile.read() )
                            print( '---------->', Dict_id_of_seller )
                            myfile.close()





            elif text.replace( " ", "" ) == '#پایه' and ( Dict_message['message']['from']['username'] == 'zanyar_sharifi' or
                                                          Dict_message['message']['from']['username'] == 'Xaniar_kh91' or
                                                          Dict_message['message']['from']['username'] == 'xaniar_sharifi' or
                                                          Dict_message['message']['from']['username'] == 'Nasrabed'or
                                                          Dict_message['message']['from']['username'] == 'ali_nazi_66'or
                                                          Dict_message['message']['from']['username'] == 'Ali1369Sadra'):

                Base_for_Selling = calculating_for_base_price( txts, update )
                # if str(Base_for_Selling).isdigit():

                print( "--------------------", Base_for_Selling )

                ls_file = os.listdir( os.getcwd() )
                print( 'befor determined the base price :', ls_file )

                if os.path.exists( 'Main_Dict.txt' ):
                    print( 'comming to new stage 1' )
                    filepath1 = os.getcwd() + '//' + 'detemined_Base_sell.txt'
                    if os.path.exists( 'detemined_Base_sell.txt' ):
                        with open( filepath1, 'r' ) as myfile:
                            detemined_Base_sell = (myfile.read())
                            myfile.close()
                            if detemined_Base_sell == '0':
                                filepath = os.getcwd() + '//' + 'Main_Dict.txt'
                                with open( filepath, 'r' ) as myfile:
                                    Main_Dict = json.loads( myfile.read() )
                                    myfile.close()

                                    print( 'processing of accounting is being done' )
                                    complete_accounting_process( Base_for_Selling )

                                    filepath = os.getcwd() + '//' + 'Main_Dict.txt'
                                    with open( filepath, 'w+' ) as myfile1:
                                        myfile1.write( json.dumps( Main_Dict ) )
                                        myfile1.close()

                                    filepath = os.getcwd() + '//' + 'Base_for_Selling.txt'
                                    with open( filepath, 'w+' ) as myfile1:
                                        myfile1.write( str( Base_for_Selling ) )
                                        myfile1.close()

                                    filepath = os.getcwd() + '//' + 'detemined_Base_sell.txt'
                                    with open( filepath, 'w+' ) as myfile1:
                                        myfile1.write( '1' )
                                        myfile1.close()


                            else:
                                update.message.reply_text( 'کاربر گرامی قیمت پایه قبلا تعیین شده' )
                                return
                    else:
                        print( 'comming to new stage 2' )
                        filepath = os.getcwd() + '//' + 'Main_Dict.txt'
                        with open( filepath, 'r' ) as myfile:
                            Main_Dict = json.loads( myfile.read() )
                            myfile.close()

                        print( 'processing of accounting is being done' )
                        complete_accounting_process( Base_for_Selling )

                        filepath = os.getcwd() + '//' + 'Main_Dict.txt'
                        with open( filepath, 'w+' ) as myfile1:
                            myfile1.write( json.dumps( Main_Dict ) )
                            myfile1.close()

                        filepath = os.getcwd() + '//' + 'Base_for_Selling.txt'
                        with open( filepath, 'w+' ) as myfile1:
                            myfile1.write( str( Base_for_Selling ) )
                            myfile1.close()

                        filepath = os.getcwd() + '//' + 'detemined_Base_sell.txt'
                        with open( filepath, 'w+' ) as myfile1:
                            myfile1.write( str( '1' ) )
                            myfile1.close()

                else:

                    filepath = os.getcwd() + '//' + 'Base_for_Selling.txt'
                    with open( filepath, 'w+' ) as myfile1:
                        myfile1.write( str( Base_for_Selling ) )
                        myfile1.close()

                    filepath = os.getcwd() + '//' + 'detemined_Base_sell.txt'
                    with open( filepath, 'w+' ) as myfile1:
                        myfile1.write( '1' )
                        myfile1.close()


            elif text == 'خ':

                # if it is done, check the last offer of seller if it is replyed by this buyer, submiting that id of buyer for the replyed buyer message as a bidder
                # if Main_Dict.get(str(Main_Dict[my_keys[i]][j + 1]['Id_of_Buyer'])+'#2', {}).get(j + 1, {}).get('loss_profit_of_buyer') is not None:
                # Dict_message.get(Dict_message['message'],{}).get('reply_to_message',{})

                try:
                    if Dict_message['message']['reply_to_message']['from'][
                        'id'] is not None:  # Dict_message.get('message',{}).get('reply_to_message'):

                        temp_text = Dict_message['message']['reply_to_message']['text']  # text of seller

                        print( temp_text )
                        temp_texts = temp_text.split()
                        print( temp_texts )
                        for txt in temp_texts:

                            if txt == 'ف':

                                print( '>>>>>>> id of seller',
                                       str( Dict_message['message']['reply_to_message']['from']['id'] ) )

                                seller_id = Dict_message['message']['reply_to_message']['from']['id']

                                filepath = os.getcwd() + '//' + 'Dict_id_of_seller.txt'
                                print( 'file path in heroku : ', filepath )

                                ls_file = os.listdir( os.getcwd() )
                                print( 'Checking for text file', ls_file )

                                if os.path.exists( 'Dict_id_of_seller.txt' ):

                                    with open( filepath, 'r' ) as myfile:
                                        Dict_id_of_seller = json.loads( myfile.read() )
                                        myfile.close()
                                        print( '########### dict_id_of_seller :', Dict_id_of_seller )

                                    if Dict_id_of_seller.get( str( seller_id ) ) is not None:

                                        last_offer_id = len( Dict_id_of_seller[str( seller_id )] )
                                        print( 'last_offer_id : ', last_offer_id )
                                        print( 'after it be read by meeee', Dict_id_of_seller )

                                        if Dict_id_of_seller[str( seller_id )][str( last_offer_id )][
                                            'status'] == 'unknown':

                                            if Dict_id_of_seller[str( seller_id )][str( last_offer_id )][
                                                'Bidders'] == 'nonbidder':

                                                Dict_id_of_seller[str( seller_id )][str( last_offer_id )][
                                                    'Bidders'] = str(
                                                    Dict_message['message']['from']['id'] )
                                            else:
                                                Dict_id_of_seller[str( seller_id )][str( last_offer_id )]['Bidders'] = \
                                                    Dict_id_of_seller[str( seller_id )][str( last_offer_id )][
                                                        'Bidders'] + ',' + str( Dict_message['message']['from']['id'] )

                                            with open( filepath, 'w+' ) as myfile1:
                                                myfile1.write( json.dumps( Dict_id_of_seller ) )
                                                myfile1.close()
                                                print( Dict_id_of_seller )


                                        elif Dict_id_of_seller[str( seller_id )][str( last_offer_id )][
                                            'status'] == 'sold':
                                            update.message.reply_text(
                                                "خریدار گرامی بسته ای که شما رپلای کرده اید قبلا فرخته شده است، لطفا بشتر دقت کنید " )
                                            return

                                        elif Dict_id_of_seller[str( seller_id )][str( last_offer_id )][
                                            'status'] == 'changed':
                                            update.message.reply_text(
                                                "خریدار گرامی بسته ای که شما رپلای کرده اید قبلا توسط فروشنده تغییر یافته و یک پیشنهاد جدیدی را جایگزین آن کرده است لطفا بیشتر دقت کنید " )
                                            return

                                    else:
                                        update.message.reply_text(
                                            "خریدار گرامی بسته ای که شما رپلای کرده اید، مربوط به فروشنده نیست" )
                                        return

                                else:

                                    update.message.reply_text(
                                        "خریدار گرامی پیغام که شما رپلایی کرده اید، مربوط به فروشنده نیست " )
                                    return


                except KeyError:

                    price_for_buying, Backage_Number_of_buyer = calculating_for_int_number( txts, update )
                    print( 'price and package of buyer : ', price_for_buying, Backage_Number_of_buyer )

                    buyer_id = str( Dict_message['message']['from']['id'] )
                    message_id = str( Dict_message['message']['message_id'] )

                    filepath = os.getcwd() + '//' + 'Dict_id_of_buyer.txt'
                    print( 'file path in heroku :', filepath )
                    ls_file = os.listdir( os.getcwd() )
                    print( 'befor creating new text file', ls_file )
                    if os.path.isfile( filepath ):

                        with open( filepath, 'r' ) as myfile:
                            Dict_id_of_buyer = json.loads( myfile.read() )
                            Dict_id_of_buyer = AutoTree( Dict_id_of_buyer )
                            myfile.close()

                            if Dict_id_of_buyer.get( str( buyer_id ) ) is not None:
                                print( '-------Dict_id_of_buyer :', Dict_id_of_buyer )
                                last_offer_id = len( Dict_id_of_buyer[str( buyer_id )] )

                                if Dict_id_of_buyer[str( buyer_id )][str( last_offer_id )]['valid'] == True:
                                    # this if could be included status of 'unknown':
                                    Dict_id_of_buyer[str( buyer_id )][str( last_offer_id )]['status'] = 'changed'
                                    Dict_id_of_buyer[str( buyer_id )][str( last_offer_id )]['valid'] = False
                                    storing_info_of_buyer( str( buyer_id ), Backage_Number_of_buyer, message_id, True,
                                                           'nonbidder', 'unknown', last_offer_id + 1, price_for_buying )


                                elif Dict_id_of_buyer[str( buyer_id )][str( last_offer_id )]['valid'] == False:

                                    if Dict_id_of_buyer[str( buyer_id )][str( last_offer_id )]['status'] == 'sold':
                                        storing_info_of_buyer( str( buyer_id ), Backage_Number_of_buyer, message_id,
                                                               True,
                                                               'nonbidder', 'unknown', last_offer_id + 1,
                                                               price_for_buying )

                                with open( filepath, 'w+' ) as myfile1:
                                    myfile1.write( json.dumps( Dict_id_of_buyer ) )
                                    myfile1.close()
                                    print( 'final-saving the data in Dict_id_of_buyer ', Dict_id_of_buyer )

                            else:
                                print( 'comming to this state' )
                                storing_info_of_buyer( str( buyer_id ), Backage_Number_of_buyer, message_id, True,
                                                       'nonbidder', 'unknown', 1, price_for_buying )

                                filepath = os.getcwd() + '//' + 'Dict_id_of_buyer.txt'
                                with open( filepath, 'w+' ) as myfile1:
                                    myfile1.write( json.dumps( Dict_id_of_buyer ) )
                                    myfile1.close()
                                ls_file = os.listdir( os.getcwd() )

                                print( 'After creating new text file', ls_file )
                                with open( filepath, 'r' ) as myfile:
                                    Dict_id_of_buyer = json.loads( myfile.read() )
                                    print( '---------->', Dict_id_of_buyer )
                                    myfile.close()

                    else:

                        print( 'comming to this state' )
                        storing_info_of_buyer( str( buyer_id ), Backage_Number_of_buyer, message_id, True, 'nonbidder',
                                               'unknown', 1, price_for_buying )

                        filepath = os.getcwd() + '//' + 'Dict_id_of_buyer.txt'
                        with open( filepath, 'w+' ) as myfile1:
                            myfile1.write( json.dumps( Dict_id_of_buyer ) )
                            myfile1.close()
                        ls_file = os.listdir( os.getcwd() )

                        print( 'After creating new text file', ls_file )
                        with open( filepath, 'r' ) as myfile:
                            Dict_id_of_buyer = json.loads( myfile.read() )
                            print( '---------->', Dict_id_of_buyer )
                            myfile.close()


            elif text == "برکت":  # text of seller

                try:
                    if Dict_message['message']['reply_to_message']['from'][
                        'id']:  # for checking that if this message is replyed or not  Dict_message.get(Dict_message['message'],{}).get('reply_to_message',{}) is not None:


                        # Reset_all_the_data()
                        # print('-------',message.json['from']['username'])
                        # print('------',message.json['reply_to_message']['from']['username'])

                        # Backage_Number_of_buyer = Backage_Number_of_seller
                        # temp_text = message.reply_to_message.json['text'] #text of buyer
                        temp_text = Dict_message['message']['reply_to_message']['text']  # text of buyer
                        # message_id = str( Dict_message['message']['message_id'] )
                        print( 'comming on new stage 1' )
                        temp_Dict_id_of_seller = defaultdict( dict )

                        print( temp_text )
                        temp_texts = temp_text.split()
                        print( temp_texts )
                        for txt in temp_texts:

                            # ********************************************************************************************************

                            if txt == 'خ':  # text of buyer
                                seller_id = Dict_message['message']['from']['id']
                                # print('++++++++++ dict id of seller in Barakat :',Dict_id_of_seller)
                                filepath = os.getcwd() + '//' + 'Dict_id_of_seller.txt'

                                if os.path.exists(
                                        'Dict_id_of_seller.txt' ):  # if Dict_id_of_seller.get(str(seller_id)) is not None:  # it is shown that it is a real seller

                                    with open( filepath, 'r' ) as myfile:
                                        temp_Dict_id_of_seller = json.loads( myfile.read() )
                                        myfile.close()

                                    Dict_id_of_seller = temp_Dict_id_of_seller
                                    print( 'comming on new stage 2' )
                                    last_offer_id = len( temp_Dict_id_of_seller[str( seller_id )] )
                                    print( 'last_offer_id: ', last_offer_id )

                                    if temp_Dict_id_of_seller[str( seller_id )][str( last_offer_id )][
                                        'Bidders'] is not 'nonbidder':

                                        print( str(
                                            temp_Dict_id_of_seller[str( seller_id )][str( last_offer_id )]['status'] ) )

                                        if temp_Dict_id_of_seller[str( seller_id )][str( last_offer_id )][
                                            'status'] == 'unknown':
                                            print( 'comming on new stage 3' )

                                            list_of_bidder = \
                                                temp_Dict_id_of_seller[str( seller_id )][str( last_offer_id )][
                                                    'Bidders'].split( ',' )
                                            buyer_id = Dict_message['message']['reply_to_message']['from']['id']

                                            if str(
                                                    buyer_id ) in list_of_bidder:  # it shows that the buyer is a person that replyed the offer of seller
                                                print( 'text of buyer', temp_texts )

                                                Accepted_Bidding, Backage_Number_of_buyer = calculating_for_int_number_of_Buyer(
                                                    temp_text, update, last_offer_id, Dict_message )

                                                print( 'Package number for buyer : ', Backage_Number_of_buyer )
                                                print( 'Number of package for seller',
                                                       temp_Dict_id_of_seller[str( seller_id )][str( last_offer_id )][
                                                           'package_number'] )
                                                Backage_Number_of_seller = int(
                                                    temp_Dict_id_of_seller[str( seller_id )][str( last_offer_id )][
                                                        'package_number'] )

                                                print( 'comming on new stage 4' )

                                                if Backage_Number_of_buyer <= Backage_Number_of_seller:

                                                    Backage_Number_of_seller = Backage_Number_of_buyer
                                                else:
                                                    update.message.reply_text(
                                                        "تعداد بسته پیشنهادی برای خریدار بیشتر از تعداد بسته ارائه شده برای فروش است " )
                                                    return

                                                filepath = os.getcwd() + '//' + 'detemined_Base_sell.txt'
                                                print( 'comming on new stage 5' )
                                                if os.path.exists( 'detemined_Base_sell.txt' ):
                                                    with open( filepath, 'r' ) as myfile:
                                                        detemined_Base_sell = (myfile.read())
                                                        myfile.close()
                                                        if detemined_Base_sell == '1':

                                                            filepath = os.getcwd() + '//' + 'Base_for_Selling.txt'
                                                            with open( filepath, 'r' ) as myfile1:
                                                                Base_for_Selling = myfile1.read()
                                                                myfile1.close()

                                                            # agreement_price,loss_and_profit_of_seller,loss_and_profit_of_buyer
                                                            temp_agreement_price, loss_profit_of_seller, loss_profit_of_buyer = calculating_loss_and_profit_of_seller_and_buyer(
                                                                int( Base_for_Selling ), Accepted_Bidding,
                                                                Backage_Number_of_buyer )
                                                            if temp_agreement_price != Accepted_Bidding:
                                                                Accepted_Bidding = temp_agreement_price
                                                        else:
                                                            loss_profit_of_seller = loss_profit_of_buyer = 0


                                                else:
                                                    print( 'comming on new stage 6' )
                                                    loss_profit_of_seller = loss_profit_of_buyer = 0

                                                # username_of_seller , package_number_of_buyer , price_of_agreement , username_of_buyer , loss_profit_of_seller , loss_profit_of_buyer
                                                # complete_items_to_Temp_Dict(message.json['from']['id'], Backage_Number_of_buyer,Accepted_Bidding,message.json['reply_to_message']['from']['id'],loss_profit_of_seller,loss_profit_of_buyer)

                                                # ID_of_seller,package_number,price_of_agreement,ID_of_buyer,loss_profit_of_seller,loss_profit_of_buyer,username_of_seller,username_of_buyer,Id_of_Buyer,Id_of_seller


                                                seller_username = Dict_message['message']['from']['username']
                                                buyer_username = Dict_message['message']['reply_to_message']['from'][
                                                    'username']

                                                filepath = os.getcwd() + '//' + 'Main_Dict.txt'
                                                if os.path.exists( 'Main_Dict.txt' ):
                                                    with open( filepath, 'r' ) as myfile:
                                                        Main_Dict = json.loads( myfile.read() )
                                                        Main_Dict = AutoTree( Main_Dict )
                                                        myfile.close()

                                                print( 'comming to new state 7' )

                                                add_items_to_Main_Dict( seller_id, Backage_Number_of_buyer,
                                                                        Accepted_Bidding, buyer_id,
                                                                        loss_profit_of_seller, loss_profit_of_buyer,
                                                                        seller_username, buyer_username, buyer_id,
                                                                        seller_id )

                                                print( 'comming to new state 8' )

                                                filepath = os.getcwd() + '//' + 'Dict_of_Username_id.txt'
                                                if os.path.exists( 'Dict_of_Username_id.txt' ):
                                                    with open( filepath, 'r' ) as myfile:
                                                        Dict_of_Username_id = json.loads( myfile.read() )
                                                        myfile.close()

                                                saving_Usernameid_of_Memebers( seller_username,
                                                                               seller_id )  # info of seller
                                                saving_Usernameid_of_Memebers( buyer_username,
                                                                               buyer_id )  # info of buyer

                                                filepath = os.getcwd() + '//' + 'Dict_of_id_to_Username.txt'
                                                if os.path.exists( 'Dict_of_id_to_Username.txt' ):
                                                    with open( filepath, 'r' ) as myfile:
                                                        Dict_of_id_to_Username = json.loads( myfile.read() )
                                                        myfile.close()

                                                storing_Dict_of_id_to_Username( seller_username, seller_id )
                                                storing_Dict_of_id_to_Username( buyer_username,
                                                                                buyer_id )  # info of buyer

                                                print( Main_Dict )
                                                filepath = os.getcwd() + '//' + 'Main_Dict.txt'
                                                with open( filepath, 'w+' ) as myfile1:
                                                    myfile1.write( json.dumps( Main_Dict ) )
                                                    myfile1.close()

                                                print( Dict_of_Username_id )
                                                filepath = os.getcwd() + '//' + 'Dict_of_Username_id.txt'
                                                with open( filepath, 'w+' ) as myfile1:
                                                    myfile1.write( json.dumps( Dict_of_Username_id ) )
                                                    myfile1.close()

                                                print( Dict_of_id_to_Username )
                                                filepath = os.getcwd() + '//' + 'Dict_of_id_to_Username.txt'
                                                with open( filepath, 'w+' ) as myfile1:
                                                    myfile1.write( json.dumps( Dict_of_id_to_Username ) )
                                                    myfile1.close()

                                                ls_file = os.listdir( os.getcwd() )
                                                print( 'َAfter submitting the data in files :', ls_file )

                                                Dict_id_of_seller[str( seller_id )][str( last_offer_id )][
                                                    'valid'] = False
                                                Dict_id_of_seller[str( seller_id )][str( last_offer_id )][
                                                    'status'] = 'sold'

                                                print( Dict_id_of_seller )

                                                filepath = os.getcwd() + '//' + 'Dict_id_of_seller.txt'
                                                with open( filepath, 'w+' ) as myfile1:
                                                    myfile1.write( json.dumps( Dict_id_of_seller ) )
                                                    myfile1.close()

                                                stt1 = stt2 = stt3 = stt4 = stt5 = sttt1 = sttt2 = sttt3 = sttt4 = ''

                                                try:

                                                    try:

                                                        # sttt1 = str(message.json['from']['first_name'])
                                                        sttt1 = Dict_message['message']['from']['first_name']
                                                    except Exception:
                                                        print( 'there is a problem in first_name of seller' )

                                                    try:
                                                        sttt2 = str( Dict_message['message']['from']['last_name'] )
                                                    except Exception:
                                                        print( 'there is a problem in last_name of seller' )

                                                    stt1 = '\n' + ' فروشنده: ' + sttt1 + ' ' + sttt2

                                                    try:
                                                        sttt3 = str(Dict_message['message']['reply_to_message']['from']['first_name'] )
                                                    except Exception:
                                                        print( 'there is a problem in first_name of Buyer' )

                                                    try:
                                                        sttt4 = str(Dict_message['message']['reply_to_message']['from']['last_name'] )
                                                    except Exception:
                                                        print( 'there is a problem in last_name of Buyer' )

                                                    stt2 = '\n' + ' خریدار: ' + sttt3 + ' ' + sttt4

                                                except Exception:
                                                    print( 'nothing' )

                                                stt3 = '\n' + ' بسته : ' + str( Backage_Number_of_buyer )
                                                stt4 = '\n' + ' قیمت  : ' + str( Accepted_Bidding )
                                                stt5 = '\n' + 'مدیریت نوسان بروکر'
                                                msg = stt1 + stt2 + stt3 + stt4 + stt5

                                                try:
                                                    update.message.reply_text( str( msg ) )
                                                except Exception:
                                                    print( 'the problem is bot.reply' )
                                                    sttt = 'معامله' + stt3 + stt4 + stt5
                                                    update.message.reply_text( sttt )
                                                    return


                                        elif temp_Dict_id_of_seller[str( seller_id )][str( last_offer_id )][
                                            'status'] is 'sold':
                                            update.message.reply_text(
                                                'فروشنده گرامی این بسته شما قبلا فروخته شده است - شما دیگر صاحب این بسته نیستید' )
                                            return


                                        elif temp_Dict_id_of_seller[str( seller_id )][str( last_offer_id )][
                                            'status'] is 'changed':
                                            update.message.reply_text(
                                                'فروشنده گرامی با پیشنهاد بسته جدید برای فروش بسته قدیمی شما غزیز فعال می شود' )
                                            return

                                    else:
                                        update.message.reply_text(
                                            "فروشنده گرامی این خریدار جنس شما را پیشنهاد نداده است، لطفا بیشتر دقت کنید" )
                                        return

                                        # ******************************************************************************************************

                            elif txt == 'ف':  # text of seller

                                buyer_id = Dict_message['message']['from']['id']

                                filepath = os.getcwd() + '//' + 'Dict_id_of_buyer.txt'

                                if os.path.exists(
                                        'Dict_id_of_buyer.txt' ):  # if Dict_id_of_seller.get(str(seller_id)) is not None:  # it is shown that it is a real seller

                                    with open( filepath, 'r' ) as myfile:
                                        Dict_id_of_buyer = json.loads( myfile.read() )
                                        myfile.close()

                                    print( 'comming on new stage 2' )
                                    last_offer_id = len( Dict_id_of_buyer[str( buyer_id )] )
                                    print( 'last_offer_id: ', last_offer_id )
                                    if Dict_id_of_buyer[str( buyer_id )][str( last_offer_id )][
                                        'Bidders'] is not 'nonbidder':

                                        print(
                                            str( Dict_id_of_buyer[str( buyer_id )][str( last_offer_id )]['status'] ) )

                                        if Dict_id_of_buyer[str( buyer_id )][str( last_offer_id )][
                                            'status'] == 'unknown':

                                            # it seems to be this if be eliminated because we do not need that, everyone can sell their packages to the buyer  if the buyer accept it

                                            print( 'comming on new stage 3' )

                                            list_of_bidder = Dict_id_of_buyer[str( buyer_id )][str( last_offer_id )][
                                                'Bidders'].split( ',' )
                                            seller_id = Dict_message['message']['reply_to_message']['from']['id']

                                            if str(
                                                    seller_id ) in list_of_bidder:  # it shows that the seller is a person that replyed the offer of buyer
                                                print( 'text of buyer', temp_texts )

                                                Accepted_Bidding, Backage_Number_of_seller = calculating_for_int_number_of_seller(
                                                    temp_text, update, last_offer_id, Dict_message )

                                                print( 'Package number for buyer : ', Backage_Number_of_buyer )
                                                print( 'Number of package for seller',
                                                       Dict_id_of_buyer[str( buyer_id )][str( last_offer_id )][
                                                           'package_number'] )
                                                Backage_Number_of_buyer = int(
                                                    Dict_id_of_buyer[str( buyer_id )][str( last_offer_id )][
                                                        'package_number'] )

                                                print( 'comming on new stage 4' )

                                                if Backage_Number_of_buyer <= Backage_Number_of_seller:

                                                    Backage_Number_of_seller = Backage_Number_of_buyer
                                                else:
                                                    update.message.reply_text(
                                                        "تعداد بسته پیشنهادی برای خریدار بیشتر از تعداد بسته ارائه شده برای فروش است " )
                                                    return

                                                filepath = os.getcwd() + '//' + 'detemined_Base_sell.txt'
                                                print( 'comming on new stage 5' )
                                                if os.path.exists( 'detemined_Base_sell.txt' ):
                                                    with open( filepath, 'r' ) as myfile:
                                                        detemined_Base_sell = (myfile.read())
                                                        myfile.close()
                                                        if detemined_Base_sell == '1':

                                                            filepath = os.getcwd() + '//' + 'Base_for_Selling.txt'
                                                            with open( filepath, 'r' ) as myfile1:
                                                                Base_for_Selling = myfile1.read()
                                                                myfile1.close()

                                                            # agreement_price,loss_and_profit_of_seller,loss_and_profit_of_buyer
                                                            temp_agreement_price, loss_profit_of_seller, loss_profit_of_buyer = calculating_loss_and_profit_of_seller_and_buyer(
                                                                int( Base_for_Selling ), Accepted_Bidding,
                                                                Backage_Number_of_buyer )
                                                            if temp_agreement_price != Accepted_Bidding:
                                                                Accepted_Bidding = temp_agreement_price
                                                        else:
                                                            loss_profit_of_seller = loss_profit_of_buyer = 0


                                                else:
                                                    print( 'comming on new stage 6' )
                                                    loss_profit_of_seller = loss_profit_of_buyer = 0

                                                # username_of_seller , package_number_of_buyer , price_of_agreement , username_of_buyer , loss_profit_of_seller , loss_profit_of_buyer
                                                # complete_items_to_Temp_Dict(message.json['from']['id'], Backage_Number_of_buyer,Accepted_Bidding,message.json['reply_to_message']['from']['id'],loss_profit_of_seller,loss_profit_of_buyer)
                                                # ID_of_seller,package_number,price_of_agreement,ID_of_buyer,loss_profit_of_seller,loss_profit_of_buyer,username_of_seller,username_of_buyer,Id_of_Buyer,Id_of_seller


                                                buyer_id = Dict_message['message']['from']['id']
                                                seller_id = Dict_message['message']['reply_to_message']['from']['id']
                                                seller_username = Dict_message['message']['reply_to_message']['from'][
                                                    'username']
                                                buyer_username = Dict_message['message']['from']['username']

                                                filepath = os.getcwd() + '//' + 'Main_Dict.txt'
                                                if os.path.exists( 'Main_Dict.txt' ):
                                                    with open( filepath, 'r' ) as myfile:
                                                        Main_Dict = json.loads( myfile.read() )
                                                        Main_Dict = AutoTree( Main_Dict )
                                                        myfile.close()

                                                print( 'comming to new stage 7' )

                                                add_items_to_Main_Dict( seller_id, Backage_Number_of_buyer,
                                                                        Accepted_Bidding, buyer_id,
                                                                        loss_profit_of_seller,
                                                                        loss_profit_of_buyer, seller_username,
                                                                        buyer_username, buyer_id, seller_id )

                                                print( 'comming to new stage 8' )

                                                filepath = os.getcwd() + '//' + 'Dict_of_Username_id.txt'
                                                if os.path.exists( 'Dict_of_Username_id.txt' ):
                                                    with open( filepath, 'r' ) as myfile:
                                                        Dict_of_Username_id = json.loads( myfile.read() )
                                                        myfile.close()

                                                saving_Usernameid_of_Memebers( seller_username,
                                                                               seller_id )  # info of seller
                                                saving_Usernameid_of_Memebers( buyer_username,
                                                                               buyer_id )  # info of buyer

                                                filepath = os.getcwd() + '//' + 'Dict_of_id_to_Username.txt'
                                                if os.path.exists( 'Dict_of_id_to_Username.txt' ):
                                                    with open( filepath, 'r' ) as myfile:
                                                        Dict_of_id_to_Username = json.loads( myfile.read() )
                                                        myfile.close()

                                                storing_Dict_of_id_to_Username( seller_username, seller_id )
                                                storing_Dict_of_id_to_Username( buyer_username,
                                                                                buyer_id )  # info of buyer

                                                print( Main_Dict )
                                                filepath = os.getcwd() + '//' + 'Main_Dict.txt'
                                                with open( filepath, 'w+' ) as myfile1:
                                                    myfile1.write( json.dumps( Main_Dict ) )
                                                    myfile1.close()

                                                print( Dict_of_Username_id )
                                                filepath = os.getcwd() + '//' + 'Dict_of_Username_id.txt'
                                                with open( filepath, 'w+' ) as myfile1:
                                                    myfile1.write( json.dumps( Dict_of_Username_id ) )
                                                    myfile1.close()

                                                print( Dict_of_id_to_Username )
                                                filepath = os.getcwd() + '//' + 'Dict_of_id_to_Username.txt'
                                                with open( filepath, 'w+' ) as myfile1:
                                                    myfile1.write( json.dumps( Dict_of_id_to_Username ) )
                                                    myfile1.close()

                                                ls_file = os.listdir( os.getcwd() )
                                                print( 'َAfter submitting the data in files :', ls_file )

                                                Dict_id_of_buyer[str( buyer_id )][str( last_offer_id )]['valid'] = False
                                                Dict_id_of_buyer[str( buyer_id )][str( last_offer_id )][
                                                    'status'] = 'sold'

                                                print( Dict_id_of_buyer )
                                                filepath = os.getcwd() + '//' + 'Dict_id_of_buyer.txt'
                                                with open( filepath, 'w+' ) as myfile1:
                                                    myfile1.write( json.dumps( Dict_id_of_buyer ) )
                                                    myfile1.close()

                                                stt1 = stt2 = stt3 = stt4 = stt5 = sttt1 = sttt2 = sttt3 = sttt4 = ''

                                                try:

                                                    try:

                                                        # sttt1 = str(message.json['from']['first_name'])
                                                        sttt1 = Dict_message['message']['reply_to_message']['from']['first_name']
                                                    except Exception:
                                                        print( 'there is a problem in first_name of seller' )

                                                    try:
                                                        sttt2 = str(Dict_message['message']['reply_to_message']['from']['last_name'] )

                                                    except Exception:
                                                        print( 'there is a problem in last_name of seller' )

                                                    stt1 = '\n' + ' فروشنده: ' + sttt1 + ' ' + sttt2

                                                    try:
                                                        sttt3 = str( Dict_message['message']['from']['first_name'] )
                                                    except Exception:
                                                        print( 'there is a problem in first_name of Buyer' )

                                                    try:
                                                        sttt4 = str( Dict_message['message']['from']['last_name'] )
                                                    except Exception:
                                                        print( 'there is a problem in last_name of Buyer' )

                                                    stt2 = '\n' + ' خریدار: ' + sttt3 + ' ' + sttt4

                                                except Exception:
                                                    print( 'nothing' )

                                                stt3 = '\n' + ' بسته : ' + str( Backage_Number_of_buyer )
                                                stt4 = '\n' + ' قیمت  : ' + str( Accepted_Bidding )
                                                stt5 = '\n' + 'مدیریت نوسان بروکر'
                                                msg = stt1 + stt2 + stt3 + stt4 + stt5

                                                try:
                                                    update.message.reply_text( str( msg ) )
                                                except Exception:
                                                    print( 'the problem is bot.reply' )
                                                    sttt = 'معامله' + stt3 + stt4 + stt5
                                                    update.message.reply_text( sttt )
                                                    return



                                        elif Dict_id_of_buyer[str( buyer_id )][str( last_offer_id )][
                                            'status'] is 'sold':
                                            update.message.reply_text(
                                                'خریدار گرامی این بسته قبلا فروخته شده است -و این فروشنده دیگر  صاحب این بسته نیست' )
                                            return


                                        elif Dict_id_of_buyer[str( buyer_id )][str( last_offer_id )][
                                            'status'] is 'changed':
                                            update.message.reply_text(
                                                'خریدار گرامی با پیشنهاد بسته جدید برای خرید پیشنهاد های  قبلی شما غیر فعال می شود' )
                                            return

                                    else:
                                        update.message.reply_text(
                                            "خریدار گرامی این فروشنده پیشنهاد جنس شما را  نداده است، لطفا بیشتر دقت کنید" )
                                        return

                except KeyError:
                    update.message.reply_text(
                        'شما فروشنده این محصول نیستین- اگر فروشنده یه محصول هستید لطفا بیشتر دقت کنید' )
                    return


        except Exception:
            # update.message.reply_text("لطفا در نوشتن پیامهای خود بیشتر دقت کنید- سعی کنید پیام ها را براساس قوانیین وضع شده بفرستید")
            print( 'take it easy and go on' )
            return


def doing_accounting_of_a_member(text, update):
    totall = 0
    Disp = ''
    counter = 0

    print( 'details of Main_Dict befor doing accounting a member : ', Main_Dict )
    if Main_Dict:
        # Dict_of_Username_id
        id = Dict_of_Username_id[text]
        print( 'ID for getting reporting : ', id )

        for key, value in Main_Dict.items():

            print( 'the key : ', key )
            print( '+++++++++ ', Main_Dict[str( key )] )

            if str( key ) == str( id ):
                for i in range( len( Main_Dict[str( key )] ) ):
                    print( '***** comming to new state in reporting' )
                    counter = counter + 1
                    transaction_number = '\n' + ' معامله ' + str( counter )
                    print( 'transaction_number', transaction_number )

                    package_number = '\n' + ' بسته ' + str( Main_Dict[str( key )][str( i + 1 )]['package_number'] )
                    print( 'package_number', package_number )

                    price_of_agreement = '\n' + 'قیمت: ' + str(
                        Main_Dict[str( key )][str( i + 1 )]['price_of_agreement'] )
                    print( 'price_of_agreement', price_of_agreement )

                    loss_profit = '\n' + 'سود یا زیان  :' + '\n' + str(
                        Main_Dict[str( key )][str( i + 1 )]['loss_profit'] )
                    print( 'loss_profit', loss_profit )

                    if Main_Dict[str( key )][str( i + 1 )]['Type_of_transaction'] == 'buying':
                        other_dealing_person = '\n' + ' خریدار ' + str(
                            Main_Dict[str( key )][str( i + 1 )]['alternative_username'] )
                        print( 'other_dealing_person', other_dealing_person )

                    else:
                        other_dealing_person = '\n' + ' فروشنده ' + str(
                            Main_Dict[str( key )][str( i + 1 )]['alternative_username'] )
                        print( 'other_dealing_person', other_dealing_person )

                    distinct_var = '\n------------------\n'
                    Disp = Disp + transaction_number + package_number + loss_profit + other_dealing_person + price_of_agreement + distinct_var
                    totall = int( Main_Dict[str( key )][str( i + 1 )]['loss_profit'] ) + totall

        print( str( totall ) + str( Disp ) )
        try:
            update.message.reply_text( '\n' + 'مجموع  سود و زیان : ' + '\n' + str( totall ) + '\n' + str( Disp ) )
        except Exception:
            update.message.reply_text( str( Disp ) )


def operating_account_of_all_members(update):
    global Dict_of_id_to_Username

    seperator = '***************************'
    Username = ''
    totall = 0
    Disp = ''

    for key, value in Main_Dict.items():

        Username = Dict_of_id_to_Username[str( key )]
        print( 'the current username fo doing its accounting : ', str( Username ) )
        totall = 0
        counter = 0
        Disp = ''
        for i in range( len( Main_Dict[key] ) ):
            print( '---------comming to new state in reporting' )
            counter = counter + 1
            transaction_number = '\n' + ' معامله ' + str( counter )
            print( 'transaction_number', transaction_number )

            package_number = '\n' + ' بسته ' + str( Main_Dict[str( key )][str( i + 1 )]['package_number'] )
            print( 'package_number', package_number )

            price_of_agreement = '\n' + 'قیمت: ' + str( Main_Dict[str( key )][str( i + 1 )]['price_of_agreement'] )
            print( 'price_of_agreement', price_of_agreement )

            loss_profit = '\n' + 'سود یا زیان  :' + '\n' + str( Main_Dict[str( key )][str( i + 1 )]['loss_profit'] )
            print( 'loss_profit', loss_profit )

            if Main_Dict[str( key )][str( i + 1 )]['Type_of_transaction'] == 'buying':
                other_dealing_person = '\n' + '  فروشنده ' + str(
                    Main_Dict[str( key )][str( i + 1 )]['alternative_username'] )
                print( 'other_dealing_person', other_dealing_person )

            else:
                other_dealing_person = '\n' + '  خریدار ' + str(
                    Main_Dict[str( key )][str( i + 1 )]['alternative_username'] )
                print( 'other_dealing_person', other_dealing_person )

            distinct_var = '\n----------------------------\n'
            Disp = transaction_number + package_number + loss_profit + other_dealing_person + price_of_agreement + distinct_var + Disp
            totall = Main_Dict[str( key )][str( i + 1 )]['loss_profit'] + totall

        Disp = seperator + '\n' + Username + ' تعداد تراکنش مالی ' + '\n' + str( counter ) + '\n' + str(
            totall ) + '\n' + 'مجموع سود و زیان' + '\n' + Disp

        update.message.reply_text( Disp )


def saving_Usernameid_of_Memebers(username, id):
    global Dict_of_Username_id

    Dict_of_Username_id[username] = id


def Delete_all_the_files():
    """ param <path> could either be relative or absolute. """

    global Main_Dict
    global Dict_id_of_seller
    global Dict_of_Username_id
    global Dict_of_id_to_Username
    global Dict_id_of_buyer
    global Dict_of_Deposit

    print( 'comming to deleteing files' )

    ls_file = os.listdir( os.getcwd() )
    print( '+++++++++++++++++++++++++++++++++++++++  befor deleteing the files', ls_file )

    # filepath = os.getcwd() + '//' + 'Main_Dict.txt'
    # if os.path.exists( os.getcwd() + "//" + filepath ):
    #     os.remove( 'Main_Dict.txt' )  # remove the file
    #

    filepath = os.getcwd() + '//' + 'Main_Dict.txt'
    if os.path.exists( os.getcwd() + "//" + 'Main_Dict.txt' ):
        with open( filepath, 'r' ) as myfile:
            Main_Dict = json.loads( myfile.read() )
            myfile.close()
            Main_Dict = defaultdict( dict )
        with open( filepath, 'w+' ) as myfile:
            myfile.write( json.dumps( Main_Dict ) )
            myfile.close()

    filepath = os.getcwd() + '//' + 'Dict_of_Username_id.txt'
    if os.path.exists( os.getcwd() + "//" + 'Dict_of_Username_id.txt' ):
        with open( filepath, 'r' ) as myfile:
            Dict_of_Username_id = json.loads( myfile.read() )
            myfile.close()
            Dict_of_Username_id = dict()
            # Dict_of_Username_id.clear()
        with open( filepath, 'w+' ) as myfile:
            myfile.write( json.dumps( Dict_of_Username_id ) )
            myfile.close()

    filepath = os.getcwd() + '//' + 'Dict_of_id_to_Username.txt'
    if os.path.exists( os.getcwd() + "//" + 'Dict_of_id_to_Username.txt' ):
        with open( filepath, 'r' ) as myfile:
            Dict_of_id_to_Username = json.loads( myfile.read() )
            myfile.close()
            Dict_of_id_to_Username = dict()
            # Dict_of_id_to_Username.clear()
        with open( filepath, 'w+' ) as myfile:
            myfile.write( json.dumps( Dict_of_id_to_Username ) )
            myfile.close()

    filepath = os.getcwd() + '//' + 'Dict_id_of_buyer.txt'
    if os.path.exists( os.getcwd() + '//' + 'Dict_id_of_buyer.txt' ):
        with open( filepath, 'r' ) as myfile:
            Dict_id_of_buyer = json.loads( myfile.read() )
            myfile.close()
            Dict_id_of_buyer = defaultdict( dict )
        with open( filepath, 'w+' ) as myfile:
            myfile.write( json.dumps( Dict_id_of_buyer ) )
            myfile.close()

    filepath = os.getcwd() + '//' + 'Dict_id_of_seller.txt'
    if os.path.exists( os.getcwd() + "//" + 'Dict_id_of_seller.txt' ):
        with open( filepath, 'r' ) as myfile:
            Dict_id_of_seller = json.loads( myfile.read() )
            myfile.close()
            Dict_id_of_seller = defaultdict( dict )
        with open( filepath, 'w+' ) as myfile:
            myfile.write( json.dumps( Dict_id_of_seller ) )
            myfile.close()

    Base_for_Selling = ''
    filepath = os.getcwd() + '//' + 'Base_for_Selling.txt'
    if os.path.exists( os.getcwd() + "//" + 'Base_for_Selling.txt' ):
        with open( filepath, 'r' ) as myfile:
            Base_for_Selling = json.loads( myfile.read() )
            myfile.close()
            Base_for_Selling = ''
            with open( filepath, 'w+' ) as myfile:
                myfile.write( json.dumps( Base_for_Selling ) )
                myfile.close()

    detemined_Base_sell = '0'
    filepath = os.getcwd() + '//' + 'detemined_Base_sell.txt'
    if os.path.exists( os.getcwd() + "//" + 'detemined_Base_sell.txt' ):
        with open( filepath, 'r' ) as myfile:
            detemined_Base_sell = json.loads( myfile.read() )
            myfile.close()
            detemined_Base_sell = '0'
        with open( filepath, 'w+' ) as myfile:
            myfile.write( detemined_Base_sell )
            myfile.close()

    filepath = os.getcwd() + '//' + 'Dict_of_Deposit.txt'
    if os.path.exists( 'Dict_of_Deposit.txt' ):
        with open( filepath, 'r' ) as myfile:
            Dict_of_Deposit = json.loads( myfile.read() )
            myfile.close()
        t_Dict_of_Deposit = dict()
        with open( filepath, 'w+' ) as myfile:
            myfile.write( json.dumps( t_Dict_of_Deposit ) )
            myfile.close()

    ls_file = os.listdir( os.getcwd() )
    print( '************************************************    After deleteing the files', ls_file )


def extract_emojis(str):
    print( '************************** checking for emoji', str( emoji.emoji_count( str ) ) )
    return emoji.emoji_count( str )


# ---------------------------------------------------------------------------------------------------



@app.route( '/' + TOKEN, methods=['GET', 'POST'] )
def webhook():
    if request.method == "POST":
        # retrieve the message in JSON and then transform it to Telegram object
        update = Update.de_json( request.get_json( force=True ), bot )

        dp.process_update( update )
        update_queue.put( update )
        return "OK"


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     bot.sendMessage(update.message.chat_id, text="Index")


@app.route( '/set_webhook', methods=['GET', 'POST'] )
def set_webhook():
    s = bot.set_webhook( webhook_address )
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


# Edit here below
def start(bot, update, args):
    telegram_user = update.message.from_user

    bot.sendMessage( update.message.chat_id, text="به ربات مدیریت نوسان بروکر خوش آمدید " )


def help(bot, update):
    s1 = '\n' + 'کاربر گرامی جهت اینکه بتوانید در این گروه فعالیت درست داشته و معاملات شما دچار اشکال نشود،  نیاز است که موارد زیر را عایت کنید: '
    s2 = '\n' + 'قیمت پایه را مدیر اصلی گروه قرا می دهد، برای قرار دادن  قیمت پایه  ابتدا از کلمه کلیدی #پایه  بعد فاصه و سپس مبلغ مورد نظر را وارد کنید '
    s3 = '\n' + 'برای مثال : #پایه 12000'
    s4 = '\n' + 'برای قرار دادن فروش بسته های خود : کلمه کلیدی  ف  بعد فاصله و سپس تعداد بسته ، سپس فاصله بعد مبلغ مورد نظر را وارد کنید '
    s5 = '\n' + 'توجه شود که وارد کردن کلمه بسته اختیاری است. '
    s51 = '\n' + 'برای مثال: ف 3 بسته 11900'
    s6 = '\n' + 'برای قرار دادن پیشنهاد های خود برای خرید بسته: پینهاد فروشنده را رپلای نموده، سپس اینگونه عمل می کنید: ابتدا کلمه کلیدی خ  بعد فاصله و سپس تعداد بسته ، بعد فاصله سپس مبلغ پیشنهادی خود را وارد کنید. همچنیین می توانید خریدی را بدون وارد کردن قیمت پیشنهادی و وبسته وارد کنید که در این حالت قیمت و تعداد بسته براساس تعداد بسته و قیمت پیشنهادی فروشنده محاسبه می شود '
    s61 = '\n' + 'برای مثال: خ 2 بسته 12000 '
    s7 = '\n' + 'برای اینکه فروشنده اعلام تایید فروش خود را نسبت به یک پیشنهاد نشان دهد لازم است که پیام پیشنهاد دهنده را رپلای نموده و سپس از کلمه کلیدی برکت استفاده نماید. برای مثال :  برکت'
    s8 = '\n' + 'توجه: 1-فروشنده ای که پیشنهاد فروش بسته ای را بدهد و بسته یا بسته های آن به فروش نرسد، چنانچه بخواهد برای بسته های پیشنهاد دهد، پیشنهاد قبلی ایشان نادیده گرفته میشود.'
    s9 = '\n' + '2- فروشنده ای که پیشنهاد فروش چند بسته را داده، چنانچه در اولین معامله چند بسته از بسته های  ایشان به فروش برسد، برای بقیه بسته ها فروشنده موظف است که برای بقیه بسته ها یک پیشنهاد جدید را اعلام کند. '
    s10 = '\n' + '\n' + 'لازم به توضیح است که هر کدام از اعضای گروه که معامله انجام داده اند می توانند با ارسال آیدی خود به ربات از صورت حساب مالی خود مطلع شوند'
    text_of_help = s1 + s2 + s3 + s4 + s5 + s51 + s6 + s61 + s7 + s8 + s9 + s10

    bot.sendMessage( update.message.chat_id, text=text_of_help )


def echo(bot, update):
    """Echo the user message."""

    print( str( update ) )

    dict = ast.literal_eval( str( update ) )
    print( dict )
    print( str( dict['message']['chat']['type'] ) )
    global Dict_of_Username_id
    global Main_Dict
    global Dict_of_id_to_Username

    # update.message.reply_text(str(update))
    # if extract_emojis(update.message.text) == 0:

    if dict['message']['chat']['type'] == 'group' or dict['message']['chat']['type'] == 'supergroup':

        print( 'comming to new stage in text_analysing' )
        text_analysing( update.message.text, dict, update )





    elif    (dict['message']['chat']['type'] == 'private' and dict['message']['from']['username'] == 'zanyar_sharifi' and update.message.text == 'all') or \
            (dict['message']['chat']['type'] == 'private' and dict['message']['from']['username'] == 'Xaniar_kh91' and update.message.text == 'all') or \
            (dict['message']['chat']['type'] == 'private' and dict['message']['from']['username'] == 'Nasrabed' and update.message.text == 'all')or \
            (dict['message']['chat']['type'] == 'private' and dict['message']['from']['username'] == 'ali_nazi_66' and update.message.text == 'all')or \
            (dict['message']['chat']['type'] == 'private' and dict['message']['from']['username'] == 'Ali1369Sadra' and update.message.text == 'all')or \
            (dict['message']['chat']['type'] == 'private' and dict['message']['from']['username'] == 'xaniar_sharifi' and update.message.text == 'all'):

        filepath = os.getcwd() + '//' + 'Main_Dict.txt'
        if os.path.exists( 'Main_Dict.txt' ):
            with open( filepath, 'r' ) as myfile:
                Main_Dict = json.loads( myfile.read() )
                myfile.close()

        filepath = os.getcwd() + '//' + 'Dict_of_id_to_Username.txt'
        if os.path.exists( 'Dict_of_id_to_Username.txt' ):
            with open( filepath, 'r' ) as myfile:
                Dict_of_id_to_Username = json.loads( myfile.read() )
                myfile.close()

        operating_account_of_all_members( update )

    elif    (dict['message']['chat']['type'] == 'private' and dict['message']['from'][ 'username'] == 'zanyar_sharifi' and (update.message.text == 'reset' or update.message.text == 'Reset')) or \
            (dict['message']['chat']['type'] == 'private' and dict['message']['from']['username'] == 'Xaniar_kh91' and (update.message.text == 'reset' or update.message.text == 'Reset'))or \
            (dict['message']['chat']['type'] == 'private' and dict['message']['from']['username'] == 'Nasrabed' and (update.message.text == 'reset' or update.message.text == 'Reset'))or \
            (dict['message']['chat']['type'] == 'private' and dict['message']['from']['username'] == 'ali_nazi_66' and (update.message.text == 'reset' or update.message.text == 'Reset'))or \
            (dict['message']['chat']['type'] == 'private' and dict['message']['from']['username'] == 'Ali1369Sadra' and (update.message.text == 'reset' or update.message.text == 'Reset'))or \
            (dict['message']['chat']['type'] == 'private' and dict['message']['from']['username'] == 'xaniar_sharifi' and (update.message.text == 'reset' or update.message.text == 'Reset')):

        print( 'comming to new stage for ' )
        Delete_all_the_files()


    elif    (dict['message']['chat']['type'] == 'private' and dict['message']['from']['username'] == update.message.text) or \
            (dict['message']['chat']['type'] == 'private' and dict['message']['from']['username'] == 'zanyar_sharifi') or \
            (dict['message']['chat']['type'] == 'private' and dict['message']['from']['username'] == 'Xaniar_kh91')or \
            (dict['message']['chat']['type'] == 'private' and dict['message']['from']['username'] == 'Nasrabed')or \
            (dict['message']['chat']['type'] == 'private' and dict['message']['from']['username'] == 'ali_nazi_66')or \
            (dict['message']['chat']['type'] == 'private' and dict['message']['from']['username'] == 'Ali1369Sadra')or \
            (dict['message']['chat']['type'] == 'private' and dict['message']['from']['username'] == 'xaniar_sharifi'):

        filepath = os.getcwd() + '//' + 'Dict_of_Username_id.txt'

        if os.path.exists( 'Dict_of_Username_id.txt' ):
            with open( filepath, 'r' ) as myfile:
                Dict_of_Username_id = json.loads( myfile.read() )
                myfile.close()

        filepath = os.getcwd() + '//' + 'Main_Dict.txt'

        if os.path.exists( 'Main_Dict.txt' ):
            with open( filepath, 'r' ) as myfile:
                Main_Dict = json.loads( myfile.read() )
                myfile.close()

        print( Dict_of_Username_id )
        if Dict_of_Username_id.get( update.message.text.replace( " ", "" ) ) is not None:
            # .replace(" ","")
            doing_accounting_of_a_member( update.message.text, update )
        else:
            update.message.reply_text( "کاربر گرامی نام کاربری (آیدی) با این مشخصات وجود ندارد" )


def main():
    # dp.start()
    dp.add_handler( CommandHandler( 'start', start, pass_args=True ) )
    dp.add_handler( CommandHandler( "help", help ) )
    dp.add_handler( MessageHandler( Filters.text, echo ) )
    # thread = Thread(target=dp.start(), name='dp')
    # thread.start()


main()



