
def save_zakaz (namebot,user_id,namedoctor):
    import iz_func
    db,cursor = iz_func.connect ()
    sql = "INSERT INTO bot_deal (`about`,`description`,`name`,`namebot`,`status`,`unix_start`,`user_id_first`,`user_id_second`) VALUES ('{}','{}','{}','{}','{}',{},'{}','{}')".format ('','',namedoctor,namebot,'Заказал клиент',0,user_id,'')
    cursor.execute(sql)
    db.commit()
    lastid = cursor.lastrowid
    return lastid

def save_reting (namebot,user_id,rating,avtor,name_reting):
    import iz_func
    db,cursor = iz_func.connect ()
    sql = "INSERT INTO bot_rating (`about`,`avtor`,`description`,`name`,`namebot`,`rating`,`status`,`user_id`) VALUES ('{}','{}','{}','{}','{}',{},'{}','{}')".format ('',avtor,'',name_reting,namebot,rating,'','')
    cursor.execute(sql)
    db.commit()
    lastid = cursor.lastrowid
    return lastid

def update_zakaz (namebot,user_id,id_zakaz,user_id_second,status):
    import iz_func
    db,cursor = iz_func.connect ()
    if user_id_second != '':
        sql = "UPDATE bot_deal SET user_id_second = "+str(user_id_second) + " where id = "+str(id_zakaz)+""
        cursor.execute(sql) 
        db.commit()
    if status != '':
        sql = "UPDATE bot_deal SET status = '"+str(status) + "' where id = "+str(id_zakaz)+""
        cursor.execute(sql) 
        db.commit()

def get_zakaz (namebot,user_id,id_zakaz):
    import iz_func
    db,cursor = iz_func.connect ()
    sql = "select `about`,`description`,`name`,`status`,`unix_start`,`user_id_first`,`user_id_second` from bot_deal where id = '"+str(id_zakaz)+"' and namebot = '"+str(namebot)+"' limit 1"   ### 
    cursor.execute(sql)
    data = cursor.fetchall()
    about           = ''
    description     = '' 
    name            = ''
    status          = ''
    unix_start      = 0 
    user_id_first   = ''
    user_id_second  = ''
    for row in data:
        about,description,name,status,unix_start,user_id_first,user_id_second = row.values()   
    return about,description,name,status,unix_start,user_id_first,user_id_second 
        
def list_send (namebot,name_doctor):
    import iz_func
    db,cursor = iz_func.connect ()
    list = []
    sql = "select id,user_id from bot_active_user where 1=1 and namebot = '"+str(namebot)+"' ".format()
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data:
        id,user_id = rec.values()    
        list.append([id,user_id]) 
    return list    
        
def select_doctor (namebot,id_doctor):    
    import iz_func
    db,cursor = iz_func.connect ()
    sql = "select id,name from bot_product where user_id = '"+str(id_doctor)+"' and namebot = '"+str(namebot)+"' ".format()
    cursor.execute(sql)
    data = cursor.fetchall()
    name = "не найден"
    for rec in data:
        id,name = rec.values()    
    return name    
        
def start_prog (user_id,namebot,first_name,last_name,username,is_bot,language_code,status,message_id,name_file_picture,telefon_nome,refer,FIO_id,lastid_log,message_in,message_old,user_id_refer):
    import iz_func
    import iz_telegram 
    import time
    import datetime
    currency = 'Валюта бота'

    if message_in == 'Поступление денежных средств': 
        message_out,menu = iz_telegram.get_message (user_id,'Поступление денежных средств',namebot)
        balans = iz_telegram.get_balans (user_id,namebot,currency)
        #message_out = message_out.replace('%%Сумма%%',str(name_doctor))
        #message_out = message_out.replace('%%Валюта%%',str(name_doctor))
        message_out = message_out.replace('%%Баланс%%',str(balans))
        markup = ''
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0)
        message_in = 'Список докторов'

    if message_in == 'Список докторов':    
        #balans = iz_telegram.get_balans (user_id,namebot,currency)
        #if balans < 100:
        #    message_out,menu = iz_telegram.get_message (user_id,'На Вашем балансе нет средств',namebot)
        #    markup = iz_telegram.get_menu (user_id,menu,namebot)
        #    markup = ""
        #    answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)
        #else:
        if 1==1:
            message_out,menu = iz_telegram.get_message (user_id,'Список докторов - бот',namebot)
            markup = iz_telegram.get_menu (user_id,menu,namebot)
            markup = iz_telegram.add_menu (user_id,markup,namebot,['Назад','Главное меню назад'])
            answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)

    if message_in == 'Ознакомлен, согласен' or message_in == "Главное меню назад" or message_in == "Назад":
        message_out,menu = iz_telegram.get_message (user_id,'Ознакомлен',namebot)
        markup = ''
        namekey01,menu   = iz_telegram.get_message (user_id,'Кнопка Заказать консультацию',namebot)        
        namekey02,menu   = iz_telegram.get_message (user_id,'Кнопка Оформить подписку',namebot)
        balans = iz_telegram.get_balans (user_id,namebot,currency)
        price      = iz_telegram.load_setting_int (namebot,"Сумма оплаты за услуги",0)
        if  balans < price:
            answer = ("не хватает средств")
        else:
            answer = str(balans) 
        namekey01 = namekey01.replace('%%Баланс%%',str(answer)) 
        data_subscription = iz_telegram.get_date_subscription (user_id,namebot) 
        if data_subscription == '':
            date_obj = 'нет подписки'
            namekey02 = namekey02.replace('%%Дата подписки%%',str(date_obj))
        else:            
            namekey02,menu   = iz_telegram.get_message (user_id,'Кнопка действия подписки',namebot)
            date_obj = data_subscription
            namekey02 = namekey02.replace('%%Дата подписки%%',str(date_obj))
        list_menu = [[namekey01,'Список докторов'],[namekey02,"Оформить подписку"]]
        markup = iz_telegram.simple_menu_main (user_id,namebot,list_menu,1) 
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)

    if message_in == 'QIWI':
        price      = iz_telegram.load_setting_int (namebot,"Сумма оплаты за услуги",0)
        link,cheque_id = iz_telegram.get_QIWI_link (user_id,namebot,price)        
        markup = iz_telegram.menu_url ('Перейти на оплату','','',link,'','','Назад','Назад')
        message_out,menu = iz_telegram.get_message (user_id,'Выставленный счет QIWI',namebot)
        message_out = message_out.replace('%%Номер счета%%',str(cheque_id)) 
        message_out = message_out.replace('%%Сумма оплаты%%',str(price))
        message_out = message_out.replace('%%Услуга%%',str('Пополнение счета'))
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)

    if message_in == 'QIWI Подписка':
        price      = iz_telegram.load_setting_int (namebot,"Стоимость подписки",0)
        link,cheque_id = iz_telegram.get_QIWI_link (user_id,namebot,price)        
        markup = iz_telegram.menu_url ('Перейти на оплату','','',link,'','','Назад','Назад')
        message_out,menu = iz_telegram.get_message (user_id,'Выставленный счет QIWI',namebot)
        message_out = message_out.replace('%%Номер счета%%',str(cheque_id)) 
        message_out = message_out.replace('%%Сумма оплаты%%',str(price))
        message_out = message_out.replace('%%Услуга%%',str('Оформление подписки'))
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)
            
    if message_in == '/start':    
        role = iz_telegram.get_role (user_id,namebot)
        if role != 'active':
            message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Сообщение при старте 1','S',0)
            time_wait = iz_telegram.load_setting_int (namebot,"Ожидание между сообщением",1)
            time.sleep (time_wait)
            message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Сообщение при старте 2','S',0)
            #time.sleep (time_wait)
        else:    
            message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Сообщение при старте доктор','S',0)

    if message_in == 'Продолжить':    
            message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Сообщение при старте 3','S',message_id)

    if message_in == 'Настройки' or message_in == '/balans':
        message_out,menu = iz_telegram.get_message (user_id,'Настройки пользователя',namebot)
        balans = iz_telegram.get_balans (user_id,namebot,currency)
        message_out = message_out.replace('%%Баланс%%',str(balans))        
        markup = ''
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0)  
                
    if message_in.find('doctor_main_') != -1:  
        balans = iz_telegram.get_balans (user_id,namebot,currency)
        price      = iz_telegram.load_setting_int (namebot,"Сумма оплаты за услуги",0)
        if balans < price:
            message_out,menu = iz_telegram.get_message (user_id,'На Вашем балансе нет средств',namebot)
            markup = iz_telegram.get_menu (user_id,menu,namebot)
            answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)
        else:         
            id_doctor = message_in.replace('doctor_main_',"")
            dict_f = {"o":"send","id_doctor":id_doctor}
            key = iz_telegram.build_jsom (dict_f)        
            name_doctor = select_doctor (namebot,id_doctor)        
            namekey01,menu   = iz_telegram.get_message (user_id,'Кнопка оплатить',namebot)        
            namekey02,menu   = iz_telegram.get_message (user_id,'Кнопка начать консультацию',namebot)
            message_out,menu = iz_telegram.get_message (user_id,'doctor_main',namebot)   
            message_out = message_out.replace('%%Доктор%%',str(name_doctor))
            #price_cons  = iz_telegram.load_setting (namebot,'Стоимость услуги')
            price      = iz_telegram.load_setting_int (namebot,"Сумма оплаты за услуги",0)
            namekey02      = namekey02.replace('%%Цена%%',str(price))        
            markup = ''
            balans = iz_telegram.get_balans (user_id,namebot,currency)
            namekey01 = namekey01.replace('%%Баланс%%',str(balans)) 
            list_menu = [[namekey01,"Оплатить / Оплата успешно"],[namekey02,key]]  
            markup = iz_telegram.simple_menu_main (user_id,namebot,list_menu,1)        
            answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id) 
                
    if message_in.find ('info') != -1:
        import json
        json_string  = iz_func.change_back(message_in.replace('info_',''))
        data_json = json.loads(json_string)
        operation = data_json['o']
              
        if operation == 'send':
            id_doctor   = data_json['id_doctor']
            namedoctor = select_doctor (namebot,id_doctor)
            message_out,menu = iz_telegram.get_message (user_id,'Вызов докторов отправлен',namebot)  
            markup = ""
            answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)
            list_doctor = list_send (namebot,select_doctor (namebot,id_doctor))
            for send_user in list_doctor:
                markup = ''
                id_zakaz = save_zakaz (namebot,user_id,str(namedoctor))
                dict_f = {"o":"get_zakaz","id_zakaz":id_zakaz}
                key = iz_telegram.build_jsom (dict_f)
                namekey03,menu = iz_telegram.get_message (user_id,'Кнопка получить заказ',namebot)				
                list_menu = [[namekey03,key]]  
                message_out,menu = iz_telegram.get_message (user_id,'Приглашение доктору',namebot)  
                markup = iz_telegram.simple_menu_main (user_id,namebot,list_menu,1)
                answer = iz_telegram.bot_send (send_user[1],namebot,message_out,markup,0) 
           
        if operation == 'get_zakaz':
            id_zakaz   = data_json['id_zakaz']         
            markup = ""
            update_zakaz (namebot,"",id_zakaz,user_id,"Доктор согласился")
            dict_f = {"o":"end_zakaz","id_zakaz":id_zakaz}
            key = iz_telegram.build_jsom (dict_f)
            namekey04,menu   = iz_telegram.get_message (user_id,'Кнопка завершить заказ',namebot)				           
            message_out,menu = iz_telegram.get_message (user_id,"Завершить звонок",namebot)       
            from pyzoom import ZoomClient
            from datetime import datetime as dt
            PUBLIC_KEY = iz_telegram.load_setting (namebot,"YOUR_ZOOM_API_KEY")
            SECRET_KEY = iz_telegram.load_setting (namebot,"YOUR_ZOOM_API_SECRET") 
            client = ZoomClient(PUBLIC_KEY,SECRET_KEY)
            meeting = client.meetings.create_meeting('Auto created 1', start_time=dt.now().isoformat(), duration_min=60, password='not-secure')
            url_start = meeting.join_url           
            message_out = message_out.replace('%%Ссылка на конференцию%%',str(url_start))                      
            list_menu = [[namekey04,key]]              
            markup = iz_telegram.menu_url ("Ссылка на конференцию","","",url_start,"","",namekey04,key)
            answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id) 
            message_out,menu = iz_telegram.get_message (user_id,"Передать ссылку клиенту",namebot)            
            about,description,name,status,unix_start,user_id_first,user_id_second = get_zakaz (namebot,user_id,id_zakaz)
            message_out = message_out.replace('%%Ссылка на конференцию%%',str(url_start)) 
            message_out = message_out.replace('%%Ваш доктор%%',str(user_id))             
            markup = iz_telegram.menu_url ("Перейти в ZOOM","","",url_start,"","","","")
            answer = iz_telegram.bot_send (user_id_first,namebot,message_out,markup,0) 
            
        if operation == 'end_zakaz':
            id_zakaz   = data_json['id_zakaz']    
            about,description,name,status_zakaz,unix_start,user_id_first,user_id_second = get_zakaz (namebot,user_id,id_zakaz) 

            if status_zakaz != 'Закрыт':
                price      = iz_telegram.load_setting_int (namebot,"Сумма оплаты за услуги",0)
                lastid = iz_telegram.add_money (namebot,user_id_first ,-1*price,'Оплата за услуги','Валюта бота')            
                lastid = iz_telegram.add_money (namebot,user_id_second,price,'Пополнение баланса','Валюта бота')            
                update_zakaz (namebot,"",id_zakaz,"","Закрыт")
                markup = ""
                
                ##### ОТПРАЛЯЕМ РЕЙТИНГ #####
                dict_Y = {"o":"reting_client_y","id_zakaz":id_zakaz}
                dict_N = {"o":"reting_client_n","id_zakaz":id_zakaz}
                key_Y  = iz_telegram.build_jsom (dict_Y)
                key_N  = iz_telegram.build_jsom (dict_N)
                namekey05,menu = iz_telegram.get_message (user_id,'Кнопка хороший рейтинг',namebot)
                namekey06,menu = iz_telegram.get_message (user_id,'Кнопка плохой  рейтинг',namebot)                         
                message_out,menu = iz_telegram.get_message (user_id,"Выставить рейтинг клиент",namebot)                            
                list_menu = [[namekey05,key_Y],[namekey06,key_N]]  
                markup = iz_telegram.simple_menu_main (user_id,namebot,list_menu,1)
                print ('[+] Рейтинг Клиент',user_id_first)
                answer = iz_telegram.bot_send (user_id_first,namebot,message_out,markup,message_id)             
                ##### КОНЕЦ #####
                
                ##### ОТПРАЛЯЕМ РЕЙТИНГ #####
                dict_Y = {"o":"reting_doctor_y","id_zakaz":id_zakaz}
                dict_N = {"o":"reting_doctor_n","id_zakaz":id_zakaz}
                key_Y  = iz_telegram.build_jsom (dict_Y)
                key_N  = iz_telegram.build_jsom (dict_N)
                namekey05,menu = iz_telegram.get_message (user_id,'Кнопка хороший рейтинг',namebot)
                namekey06,menu = iz_telegram.get_message (user_id,'Кнопка плохой  рейтинг',namebot)                         
                message_out,menu = iz_telegram.get_message (user_id,"Выставить рейтинг доктор",namebot)            
                list_menu = [[namekey05,key_Y],[namekey06,key_N]]  
                markup = iz_telegram.simple_menu_main (user_id,namebot,list_menu,1)
                print ('[+] Рейтинг Доктор',user_id_second)
                answer = iz_telegram.bot_send (user_id_second,namebot,message_out,markup,message_id) 
                ##### КОНЕЦ ##### 
                
                time.sleep (10)
                
                ##### Процедура Главного меню ##### 
                message_out,menu = iz_telegram.get_message (user_id_first,'Ознакомлен',namebot)
                markup = ''
                namekey01,menu   = iz_telegram.get_message (user_id_first,'Кнопка Заказать консультацию',namebot)        
                namekey02,menu   = iz_telegram.get_message (user_id_first,'Кнопка Оформить подписку',namebot)
                balans = iz_telegram.get_balans (user_id_first,namebot,currency)
                price      = iz_telegram.load_setting_int (namebot,"Сумма оплаты за услуги",0)
                if  balans < price:
                    answer = ("не хватает средств")
                else:
                    answer = str(balans) 
                namekey01 = namekey01.replace('%%Баланс%%',str(answer)) 
                data_subscription = iz_telegram.get_date_subscription (user_id_first,namebot) 
                if data_subscription == '':
                    date_obj = 'нет подписки'
                    namekey02 = namekey02.replace('%%Дата подписки%%',str(date_obj))
                else:            
                    namekey02,menu   = iz_telegram.get_message (user_id_first,'Кнопка действия подписки',namebot)
                    date_obj = data_subscription
                    namekey02 = namekey02.replace('%%Дата подписки%%',str(date_obj))
                list_menu = [[namekey01,'Список докторов'],[namekey02,"Оформить подписку"]]
                markup = iz_telegram.simple_menu_main (user_id_first,namebot,list_menu,1) 
                answer = iz_telegram.bot_send (user_id_first,namebot,message_out,markup,0)

                
                
            else:
                message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Заказ закрыт','S',message_id)    

        if operation == 'reting_client_y':
            id_zakaz   = data_json['id_zakaz'] 
            name_reting = "Клиент за Доктора"        
            markup = ""
            message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Зафиксирован положительный отзыв','S',message_id)
            save_reting (namebot,user_id,5,str(id_zakaz),name_reting)
   
        if operation == 'reting_client_n':
            name_reting = "Клиент против Доктора"
            id_zakaz   = data_json['id_zakaz']         
            markup = ""
            message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Зафиксирова отицательный отзыв','S',message_id)
            save_reting (namebot,user_id,1,str(id_zakaz),name_reting)

        if operation == 'reting_doctor_y':
            name_reting = "Доктор за Клиента"
            id_zakaz   = data_json['id_zakaz']         
            markup = ""
            message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Зафиксирован положительный отзыв','S',message_id)
            save_reting (namebot,user_id,5,str(id_zakaz),name_reting)
   
        if operation == 'reting_doctor_n':
            name_reting = "Доктор против Клиента"
            id_zakaz   = data_json['id_zakaz']         
            markup = ""
            message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Зафиксирова отицательный отзыв','S',message_id)
            save_reting (namebot,user_id,1,str(id_zakaz),name_reting)