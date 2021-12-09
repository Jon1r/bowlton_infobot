from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


btn_chats = KeyboardButton('Chats')
btn_mytasks = KeyboardButton('MyTask')
btn_keypoints = KeyboardButton('KeyPoints')

# Раздел Providers->
btn_hardware = KeyboardButton('Hardware')
btn_parts = KeyboardButton('Parts')
btn_electrica = KeyboardButton('Electrica')
btn_produced = KeyboardButton('Produces')

# Раздел Providers->Hardware
btn_motors = KeyboardButton('Motors')
btn_reductors = KeyboardButton('Reductors')
btn_drivers = KeyboardButton('Drivers')
btn_servo = KeyboardButton('Servo')

# Раздел Providers->Electrica
btn_wires = KeyboardButton('Wires')
btn_connectors = KeyboardButton('Connectors')
btn_rele = KeyboardButton('Rele')

# Раздел Providers->Parts
btn_profiles = KeyboardButton('Profiles')
btn_screws = KeyboardButton('Screws')
btn_corner = KeyboardButton('Corners')
btn_sheets = KeyboardButton('Sheets')

# Раздел Providers->Produces
btn_lazermetal = KeyboardButton('Laser metal')
btn_lazeracril = KeyboardButton('Laser acril')

# Раздел Documents->
btn_doverennost = KeyboardButton('Doverennost')
btn_reqvisits = KeyboardButton('Reqvisits')

# Раздел GoogleDocs->
btn_bom = KeyboardButton('BOM')
btn_genplan = KeyboardButton('Генплан YFR')
btn_drive = KeyboardButton('GoogleDrive')

btn_del_providers = InlineKeyboardButton(text='Delete')
btn_change_providers = InlineKeyboardButton(text='Change', callback_data='change_providers')


kb_googledocs = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_doc = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_hardware = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_electrica = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_parts = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_produces = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_providers = ReplyKeyboardMarkup(resize_keyboard=True)
kb_in_del_providers = InlineKeyboardMarkup(row_width=2)


kb_in_del_providers.add(btn_del_providers).add(btn_change_providers)
kb_doc.add(btn_doverennost).add(btn_reqvisits)
kb_googledocs.add(btn_genplan).add(btn_bom).add(btn_drive)

kb_providers.add(btn_hardware).add(btn_electrica).add(btn_parts).add(btn_produced)

kb_hardware.add(btn_motors).add(btn_reductors).add(btn_drivers).add(btn_servo)
kb_electrica.add(btn_wires).add(btn_connectors).add(btn_rele)
kb_parts.add(btn_profiles).add(btn_screws).add(btn_corner).add(btn_sheets)
kb_produces.add(btn_lazeracril).add(btn_lazermetal)
