from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

# Главное меню
main_menu = KeyboardButton('Main menu')

# Кнопки главного меню
btn_questions = KeyboardButton('\U0001F4DDFollow-up')
btn_tasks = KeyboardButton('\U0001F3AFTasks')
btn_providers = KeyboardButton('\U0001F6D2Providers')
btn_YRFfiles = KeyboardButton('\U0001F4C1YRFfiles')

# Кнопки раздела Follow-up
btn_electronics = KeyboardButton('Electronics')
btn_design = KeyboardButton('Design')
btn_software = KeyboardButton('Software')
btn_decor = KeyboardButton('Decor')
btn_sprint = KeyboardButton('\U0001F3C3Sprint')
btn_other = KeyboardButton('Other')

# Кнопки раздела Tasks
btn_mytasks = KeyboardButton('NewTask')
btn_keypoints = KeyboardButton('KeyPoints')

# Кнопки раздела Providers
btn_hardware = KeyboardButton('Hardware')
btn_parts = KeyboardButton('Parts')
btn_electrica = KeyboardButton('Electrica')
btn_produced = KeyboardButton('Produced')

# Кнопки раздела YRFfiles
btn_documents = KeyboardButton('Documents')
btn_googledocs = KeyboardButton('GoogleDocs')
btn_chats = KeyboardButton('Chats')


# Кнопки раздела YRFfiles->Documents
btn_doverennost = KeyboardButton('Doverennost')
btn_reqvisits = KeyboardButton('Reqvisits')

# Кнопки раздела YRFfiles->GoogleDocs
btn_bom = KeyboardButton('BOM')
btn_genplan = KeyboardButton('Генплан YFR')
btn_drive = KeyboardButton('GoogleDrive')

# Кнопки подраздела Providers->Parts
btn_profiles = KeyboardButton('Profiles')
btn_screws = KeyboardButton('Screws')
btn_corner = KeyboardButton('Corners')
btn_sheets = KeyboardButton('Sheets')


# Кнопки подраздела Providers->Hardware
btn_motors = KeyboardButton('Motors')
btn_reductors = KeyboardButton('Reductors')
btn_drivers = KeyboardButton('Drivers')
btn_servo = KeyboardButton('Servo')


# Кнопки подраздела Providers->Electrica
btn_wires = KeyboardButton('Wires')
btn_connectors = KeyboardButton('Connectors')
btn_rele = KeyboardButton('Rele')


# Кнопки подраздела Providers->Produce
btn_lazermetal = KeyboardButton('Laser metal')
btn_lazeracril = KeyboardButton('Laser acril')


# Кнопки раздела myTasks
btn_todo = InlineKeyboardButton(text='Поставленные(0)', callback_data='dsc')
btn_doing = InlineKeyboardButton(text='Выполняемые(0)', callback_data='zc')
btn_notaprove = InlineKeyboardButton(text='Ожидают подтверждения(0)', callback_data='ad')
btn_uaprove = InlineKeyboardButton(text='Нужно подтвердить(0)', callback_data='zxcv')
btn_aprove = InlineKeyboardButton(text='Ожидают принятия(0)', callback_data='zcxcz')

kb_menu = ReplyKeyboardMarkup(resize_keyboard=True)
kb_tasks = ReplyKeyboardMarkup(resize_keyboard=True)
kb_providers = ReplyKeyboardMarkup(resize_keyboard=True)
kb_yfrfiles = ReplyKeyboardMarkup(resize_keyboard=True)
kb_parts = ReplyKeyboardMarkup(resize_keyboard=True)
kb_followup = ReplyKeyboardMarkup(resize_keyboard=True)
kb_hardware = ReplyKeyboardMarkup(resize_keyboard=True)
kb_electrica = ReplyKeyboardMarkup(resize_keyboard=True)
kb_produce = ReplyKeyboardMarkup(resize_keyboard=True)
kb_documents = ReplyKeyboardMarkup(resize_keyboard=True)
kb_googledocs = ReplyKeyboardMarkup(resize_keyboard=True)
kb_tasklist = InlineKeyboardMarkup(row_width=2)


kb_providers.add(btn_electrica).insert(btn_hardware).add(btn_parts).insert(btn_produced).add(main_menu)
kb_menu.add(btn_questions).insert(btn_tasks).add(btn_providers).insert(btn_YRFfiles)
kb_tasks.add(btn_mytasks).insert(btn_keypoints).add(main_menu)
kb_yfrfiles.add(btn_documents).add(btn_googledocs).add(main_menu)
kb_googledocs.add(btn_genplan).add(btn_bom).add(btn_drive).add(main_menu)
kb_parts.add(btn_profiles).add(btn_corner).add(btn_screws).add(btn_sheets).add(main_menu)
kb_hardware.add(btn_motors).add(btn_reductors).add(btn_drivers).add(btn_servo).add(main_menu)
kb_electrica.add(btn_wires).add(btn_connectors).add(btn_rele).add(main_menu)
kb_produce.add(btn_lazermetal).add(btn_lazeracril).add(main_menu)
kb_followup.add(btn_electronics).insert(btn_design).add(btn_software).insert(btn_decor).add(btn_other).add(main_menu)
kb_documents.add(btn_doverennost).add(btn_reqvisits).add(main_menu)

kb_tasklist.add(btn_todo).insert(btn_doing).add(btn_notaprove).add(btn_uaprove).add(btn_uaprove)