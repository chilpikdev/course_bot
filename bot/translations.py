# bot/translations.py

MESSAGES = {
    # Til tańlaw
    'welcome_prompt_language': {
        'qr': "Assalawma aleykum! Til tańlań: \nАссалому алайкум! Тилни танланг:",
        'uz': "Ассалому алайкум! Тилни танланг:",
    },
    'language_chosen_button': {
        'qr': "Qaraqalpaqsha",
        'uz': "O'zbekcha",
    },
    'language_selected': {
        'qr': 'Til saylandı',
        'uz': 'Тил таланди',
    },


    # Baslaw hám kontakt alıw
    'welcome_after_lang': {
        'qr': ("🎓 Kurs satıp alıw ushın mo'lsherlengen botqa xosh kelipsiz!\n\n"
               "Men sizge qolaylı kurstı tańlaw hám satıp alıwǵa járdem beremen.\n"
               "Baslaw ushın telefon nomerińizdi jiberiń."),
        'uz': ("🎓 Курс сотиб олиш учун мўлжалланган ботга хуш келибсиз!\n\n"
               "Мен сизга қулай курсни танлаш ва сотиб олишга ёрдам бераман.\n"
               "Бошлаш учун телефон рақамингизни юборинг."),
    },
    'request_contact_button': {
        'qr': "📱 Nomerdi jiberiw",
        'uz': "📱 Рақамни юбориш",
    },
    'contact_saved': {
        'qr': ("✅ Raxmet! Telefon nomerińiz saqlandı.\n\n"
               "Endi siz kurstı tańlay alasız:"),
        'uz': ("✅ Раҳмат! Телефон рақамингиз сақланди.\n\n"
               "Энди сиз курсни танлашингиз мумкин:"),
    },
    'returning_to_main_menu': {
        'qr': "🏠 Bas menyuǵa qaytıp atırmız.",
        'uz': "🏠 Бош менюга қайтмоқдамиз.",
    },

    # Bas menyu
    'main_menu_title': {
        'qr': '🏠 <b>Bas menyu</b>',
        'uz': '🏠 <b>Бош меню</b>',
    },
    'courses_button': {
        'qr': '📚 Kurslar',
        'uz': '📚 Курслар',
    },
    'about_button': {
        'qr': 'ℹ️ Biz haqqımızda',
        'uz': 'ℹ️ Биз ҳақимизда',
    },
    'support_button': {
        'qr': '📞 Qollap-quwatlaw',
        'uz': '📞 Қўллаб-қувватлаш',
    },

    # Kurslar dizimi
    'courses_list_title': {
        'qr': "📚 <b>Kurslar:</b>\n\nTolıq maǵlıwmat alıw hám satıp alıw ushın kurstı tańlań:",
        'uz': "📚 <b>Курслар:</b>\n\nТўлиқ маълумот олиш ва сотиб олиш учун курсни танланг:",
    },
    'no_courses_yet': {
        'qr': "😔 Házirshe kurslar joq.\nKeyinirek urınıp kóriń.",
        'uz': "😔 Ҳозирча курслар мавжуд эмас.\nКейинроқ уриниб кўринг.",
    },
    'back_to_menu_button': {
        'qr': "🏠 Bas menyu",
        'uz': "🏠 Бош меню",
    },

    # Kurs haqqında maǵlıwmat
    'course_details_header': {
        'qr': "📚 <b>{course_name}</b>\n\n{course_description}\n\n",
        'uz': "📚 <b>{course_name}</b>\n\n{course_description}\n\n",
    },
    'price_label': {
        'qr': "💰 Bahası:",
        'uz': "💰 Нархи:",
    },
    'discount_label': {
        'qr': "🔥 <b>(-{discount}%)</b>\n\n",
        'uz': "🔥 <b>(-{discount}%)</b>\n\n",
    },
    'old_price_label': {
        'qr': "<s>{old_price}</s> <b>{price} sum</b>",
        'uz': "<s>{old_price}</s> <b>{price} сўм</b>",
    },
    'current_price_label': {
        'qr': "<b>{price} sum</b>\n\n",
        'uz': "<b>{price} сўм</b>\n\n",
    },
    'taken_slots': {
        'qr': "👥 Bánt orınlar: {current}/{max}\n",
        'uz': "👥 Банд ўринлар: {current}/{max}\n",
    },
    'no_slots_left': {
        'qr': "❌ <b>Orınlar qalmadi</b>\n\n",
        'uz': "❌ <b>Ўринлар қолмади</b>\n\n",
    },
    'free_slots': {
        'qr': "✅ Bos orınlar: {free}\n\n",
        'uz': "✅ Бўш ўринлар: {free}\n\n",
    },
    'buy_button': {
        'qr': "💳 {price} sum-ǵa satıp alıw",
        'uz': "💳 {price} сўмга сотиб олиш",
    },
    'back_to_courses_button': {
        'qr': "◀️ Kurslar dizimine",
        'uz': "◀️ Курслар рўйхатига",
    },

    # Satıp alıw procesi
    'course_not_available': {
        'qr': "❌ Ókinishke oray, bul kurs endi qoljetimli emes.",
        'uz': "❌ Афсуски, бу курс энди мавжуд эмас.",
    },
    'already_bought_course': {
        'qr': "✅ Siz \"{course_name}\" kursın satıp alıp bolǵansız.\n\nGruppaǵa silteme: {group_link}",
        'uz': "✅ Сиз \"{course_name}\" курсини сотиб олиб бўлгансиз.\n\nГуруҳга ҳавола: {group_link}",
    },
    'payment_already_pending': {
        'qr': "⏳ Sizde \"{course_name}\" kursın satıp alıw ushın arza bar.\nStatusı: {status}\n\nAdministratordıń tekseriwin kútiń.",
        'uz': "⏳ Сизда \"{course_name}\" курсини сотиб олиш учун ариза мавжуд.\nҲолати: {status}\n\nАдминистраторнинг текширувини кутинг.",
    },
    'no_payment_methods_available': {
        'qr': "❌ Ókinishke oray, házir tólemniń qoljetimli usılları joq.\nQollap-quwatlaw xızmetine múrájat etiń.",
        'uz': "❌ Афсуски, ҳозир тўловнинг мавжуд усуллари йўқ.\nҚўллаб-қувватлаш хизматига мурожаат қилинг.",
    },
    'select_payment_method_title': {
        'qr': "💳 <b>Kurs satıp alıw: {course_name}</b>\n\n💰 Bahası: <b>{price} sum</b>\n\nTólem usılın tańlań:",
        'uz': "💳 <b>Курс сотиб олиш: {course_name}</b>\n\n💰 Нархи: <b>{price} сўм</b>\n\nТўлов усулини танланг:",
    },
    'back_button': {
        'qr': "◀️ Artqa",
        'uz': "◀️ Ортга",
    },
    'cancel_button': {
        'qr': "❌ Biykar etiw",
        'uz': "❌ Бекор қилиш",
    },

    # Tólem rekvizitleri hám chek jiberiw
    'payment_details_title': {
        'qr': "💳 <b>Kurs tólemi: {course_name}</b>\n\n",
        'uz': "💳 <b>Курс тўлови: {course_name}</b>\n\n",
    },
    'amount_to_pay': {
        'qr': "💰 Tólem ushın summa: <b>{price} sum</b>\n\n",
        'uz': "💰 Тўлов учун сумма: <b>{price} сўм</b>\n\n",
    },
    'payment_requisites': {
        'qr': "📋 <b>Tólem ushın rekvizitler:</b>\n\n",
        'uz': "📋 <b>Тўлов учун реквизитлар:</b>\n\n",
    },
    'important_note': {
        'qr': "\n\n⚠️ <b>Áhmiyetli:</b>\n",
        'uz': "\n\n⚠️ <b>Муҳим:</b>\n",
    },
    'important_note_1': {
        'qr': "• Anıq <b>{price} sum</b> ótkeriwiz kerek\n",
        'uz': "• Аниқ <b>{price} сўм</b> ўтказишингиз керак\n",
    },
    'important_note_2': {
        'qr': "• Tólemnen keyin chektiń skrinshotın jiberiń\n",
        'uz': "• Тўловдан кейин чекнинг скриншотини юборинг\n",
    },
    'important_note_3': {
        'qr': "• Administrator tólemdi tekseredi hám gruppa siltemesin jiberedi\n\n",
        'uz': "• Администратор тўловни текширади ва гуруҳ ҳаволасини юборади\n\n",
    },
    'send_receipt_prompt': {
        'qr': "📸 Chektiń skrinshotın yamasa PDF hújjetin jiberiń:",
        'uz': "📸 Чекнинг скриншотини ёки PDF ҳужжатини юборинг:",
    },
    'cancel_purchase_button': {
        'qr': "❌ Satıp alıwdı biykarlaw",
        'uz': "❌ Харидни бекор қилиш",
    },
    'purchase_cancelled': {
        'qr': ("❌ Satıp alıw biykar etildi.\n\n"
               "Siz basqa kurs tańlawıńız yamasa keyinirek qaytıwıńız múmkin."),
        'uz': ("❌ Харид бекор қилинди.\n\n"
               "Сиз бошқа курс танлашингиз ёки кейинроқ қайтишингиз мумкин."),
    },

    # Chekti qayta islew
    'receipt_accepted_photo': {
        'qr': "✅ <b>Chek qabıllandı!</b>\n\n",
        'uz': "✅ <b>Чек қабул қилинди!</b>\n\n",
    },
    'receipt_accepted_document': {
        'qr': "✅ <b>Hújjet qabıllandı!</b>\n\n",
        'uz': "✅ <b>Ҳужжат қабул қилинди!</b>\n\n",
    },
    'course_label': { 'qr': "📚 Kurs:", 'uz': "📚 Курс:", },
    'amount_label': { 'qr': "💰 Summa:", 'uz': "💰 Сумма:", },
    'payment_method_label': { 'qr': "💳 Tólem usılı:", 'uz': "💳 Тўлов усули:", },
    'file_label': { 'qr': "📄 Fayl:", 'uz': "📄 Файл:", },
    'payment_pending_admin_review': {
        'qr': ("\n⏳ Siziń tólemińiz administratorǵa tekseriw ushın jiberildi.\n"
               "Ádette tekseriw 2 saatqa shekem waqıt aladı.\n\n"
               "Tastıyıqlanǵannan keyin siz kurs gruppasına silteme alasız."),
        'uz': ("\n⏳ Сизнинг тўловингиз администраторга текшириш учун юборилди.\n"
               "Одатда текширув 2 соатгача вақт олади.\n\n"
               "Тасдиқлангандан кейин сиз курс гуруҳига ҳавола оласиз."),
    },

    # Tólem nátiyjeleri
    'payment_approved_title': {
        'qr': "✅ <b>Tólem tastıyıqlandı!</b>\n\n",
        'uz': "✅ <b>Тўлов тасдиқланди!</b>\n\n",
    },
    'congratulations_on_purchase': {
        'qr': "🎉 Satıp alıwıńız benen qutlıqlaymız!\n\n",
        'uz': "🎉 Харидингиз билан табриклаймиз!\n\n",
    },
    'group_link_message': {
        'qr': "🔗 <b>Kurs gruppasına silteme:</b>\n{group_link}\n\n",
        'uz': "🔗 <b>Курс гуруҳига ҳавола:</b>\n{group_link}\n\n",
    },
    'join_group_and_start': {
        'qr': "Gruppaǵa qosılıń hám oqıwdı baslań!\nEger sorawlarıńız bolsa, qollap-quwatlaw xızmetine múrájat etiń.",
        'uz': "Гуруҳга қўшилинг ва ўқишни бошланг!\nАгар саволларингиз бўлса, қўллаб-қувватлаш хизматига мурожаат қилинг.",
    },
    'other_courses_button': {
        'qr': "📚 Basqa kurslar",
        'uz': "📚 Бошқа курслар",
    },
    'payment_rejected_title': {
        'qr': "❌ <b>Tólem biykar etildi</b>\n\n",
        'uz': "❌ <b>Тўлов бекор қилинди</b>\n\n",
    },
    'payment_rejected_body': {
        'qr': "Ókinishke oray, siziń tólemińiz tekseriwden ótpedi.\n\n",
        'uz': "Афсуски, сизнинг тўловингиз текширувдан ўтмади.\n\n",
    },
    'admin_comment_message': {
        'qr': "💬 <b>Administrator kommentariyi:</b>\n{comment}\n\n",
        'uz': "💬 <b>Администратор изоҳи:</b>\n{comment}\n\n",
    },
    'if_questions_contact_support': {
        'qr': "Eger sorawlarıńız bolsa, qollap-quwatlaw xızmetine múrájat etiń.\nSiz taǵı bir márte tólewge urınıp kóriwińizge boladı.",
        'uz': "Агар саволларингиз бўлса, қўллаб-қувватлаш хизматига мурожаат қилинг.\nСиз яна бир бор тўлашга уриниб кўришингиз мумкин.",
    },
    'retry_payment_button': {
        'qr': "🔄 Qaytadan urınıp kóriw",
        'uz': "🔄 Қайтадан уриниб кўриш",
    },
    'payment_method_card_number': {
        'qr': "Karta nomeri:",
        'uz': "Карта рақами:",
    },
    'payment_method_cardholder': {
        'qr': "Qabıllawshı:",
        'uz': "Қабул килувчи:",
    },
    'payment_method_bank': {
        'qr': "Bank:",
        'uz': "Банк:",
    },
    'payment_method_instructions': {
        'qr': "\nInstrukciya:",
        'uz': "\nИнструкция:",
    },

    # Járdem
    'help_text': {
        'qr': ("🤖 <b>Járdem</b>\n\n"
               "Qoljetimli buyrıqlar:\n"
               "/start - Bot penen islewdi baslaw\n"
               "/help - Usı kórsetpeni kórsetiw\n"
               "/cancel - Bas menyuǵa qaytıw\n\n"
               "Navigaciya ushın túymelerden paydalanıń.\n\n"
               "📚 <b>Kurs qalay satıp alınadı:</b>\n"
               "1. \"📚 Kurslar\" di tańlań\n"
               "2. Qızıqtırǵan kurstı tańlań\n"
               "3. \"💳 Satıp alıw\" di basıń\n"
               "4. Tólem usılın tańlań\n"
               "5. Rekvizitler boyınsha tóleń\n"
               "6. Chek skrinshotın jiberiń\n"
               "7. Tastıyıqlanıwın kútiń\n\n"
               "Qanday da bir másele payda bolsa, qollap-quwatlaw xızmetine múrájat etiń."),
        'uz': ("🤖 <b>Ёрдам</b>\n\n"
               "Мавжуд буйруқлар:\n"
               "/start - Бот билан ишлашни бошлаш\n"
               "/help - Ушбу йўриқномани кўрсатиш\n"
               "/cancel - Бош менюга қайтиш\n\n"
               "Навигация учун тугмалардан фойдаланинг.\n\n"
               "📚 <b>Курс қандай сотиб олинади:</b>\n"
               "1. \"📚 Курслар\"ни танланг\n"
               "2. Қизиқтирган курсни танланг\n"
               "3. \"💳 Сотиб олиш\"ни босинг\n"
               "4. Тўлов усулини танланг\n"
               "5. Реквизитлар бўйича тўланг\n"
               "6. Чек скриншотини юборинг\n"
               "7. Тасдиқланишини кутинг\n\n"
               "Бирор муаммо пайдо бўлса, қўллаб-қувватлаш хизматига мурожаат қилинг."),
    },

    # Qátelikler
    'error_start_command': {
        'qr': "Qátelik júz berdi. /start buyrıǵın qaytadan teriń",
        'uz': "Хатолик юз берди. /start буйруғини қайтадан теринг",
    },
    'error_not_your_contact': {
        'qr': "❌ Ótinish, tek óz telefon nomerińizdi jiberiń.",
        'uz': "❌ Илтимос, фақат ўз телефон рақамингизни юборинг.",
    },
    'error_contact_save': {
        'qr': "Kontaktıńızdı saqlawda qátelik júz berdi. Qaytadan urınıp kóriń.",
        'uz': "Контактингизни сақлашда хатолик юз берди. Қайтадан уриниб кўринг.",
    },
    'info_not_found': {
        'qr': "Maǵlıwmat tabılmadı.",
        'uz': "Маълумот топилмади.",
    },
    'support_info_not_found': {
        'qr': "Qollap-quwatlaw haqqında maǵlıwmat tabılmadı.",
        'uz': "Қўллаб-қувватлаш ҳақида маълумот топилмади.",
    },
    'error_loading_course_details': {
        'qr': "Kurs haqqında maǵlıwmat júklewde qátelik júz berdi.",
        'uz': "Курс ҳақида маълумот юклашда хатолик юз берди.",
    },
    'error_loading_courses': {
        'qr': "Kurslardı júklewde qátelik júz berdi.",
        'uz': "Курсларни юклашда хатолик юз берди.",
    },
    'error_buy_course': {
        'qr': "Satıp alıwdı rásmiylestiriwde qátelik júz berdi.",
        'uz': "Сотиб олишни расмийлаштиришда хатолик юз берди.",
    },
    'error_payment_method_selection': {
        'qr': "Tólem usılın tańlawda qátelik júz berdi.",
        'uz': "Тўлов усулини танлашда хатолик юз берди.",
    },
    'error_purchase_data_lost': {
        'qr': "❌ Qátelik: satıp alıw haqqında maǵlıwmatlar joǵalǵan. Qaytadan baslań.",
        'uz': "❌ Хатолик: сотиб олиш ҳақида маълумотлар йўқолган. Қайтадан бошланг.",
    },
    'error_photo_not_found': {
        'qr': "❌ Foto tabılmadı. Qaytadan urınıp kóriń.",
        'uz': "❌ Фотосурат топилмади. Қайтадан уриниб кўринг.",
    },
    'error_photo_download': {
        'qr': "❌ Fotanı júklep alıw múmkin bolmadı. Qaytadan urınıp kóriń.",
        'uz': "❌ Фотосуратни юклаб олиш мумкин бўлмади. Қайтадан уриниб кўринг.",
    },
    'error_document_not_found': {
        'qr': "❌ Hújjet tabılmadı. Qaytadan urınıp kóriń.",
        'uz': "❌ Ҳужжат топилмади. Қайтадан уриниб кўринг.",
    },
    'error_file_too_large': {
        'qr': "❌ Fayl júdá úlken. Maksimum 10 MB.",
        'uz': "❌ Файл жуда катта. Максимум 10 МБ.",
    },
    'error_unsupported_format': {
        'qr': "❌ Qollap-quwatlanbaytuǵın format. PDF, JPG yamasa PNG formatlarınan paydalanıń.",
        'uz': "❌ Қўллаб-қувватланмайдиган формат. PDF, JPG ёки PNG форматларидан фойдаланинг.",
    },
    'error_file_download': {
        'qr': "❌ Fayldı júklep alıw múmkin bolmadı. Qaytadan urınıp kóriń.",
        'uz': "❌ Файлни юклаб олиш мумкин бўлмади. Қайтадан уриниб кўринг.",
    },
    'error_payment_save': {
        'qr': "❌ Tólemdi saqlawda qátelik júz berdi. Qaytadan urınıp kóriń.",
        'uz': "❌ Тўловни сақлашда хатолик юз берди. Қайтадан уриниб кўринг.",
    },
    'error_processing_receipt': {
        'qr': "Chekti qayta islewde qátelik júz berdi.",
        'uz': "Чекни қайта ишлашда хатолик юз берди.",
    },
    'error_processing_document': {
        'qr': "Hújjet qayta islewde qátelik júz berdi.",
        'uz': "Ҳужжатни қайта ишлашда хатолик юз берди.",
    },

    # Fayl alǵanda (satıp alıwdan tıs)
    'photo_received_outside_payment': {
        'qr': ("📸 Men siziń fotońızdı aldım.\n\n"
               "Eger siz kurs tólemi haqqında chekti jiberiwdi qáleseńiz, "
               "dáslep kurstı tańlap, \"💳 Satıp alıw\" túymesin basıń."),
        'uz': ("📸 Мен сизнинг фотосуратингизни олдим.\n\n"
               "Агар сиз курс тўлови ҳақида чекни юбормоқчи бўлсангиз, "
               "аввал курсни танлаб, \"💳 Сотиб олиш\" тугмасини босинг."),
    },
    'document_received_outside_payment': {
        'qr': ("📄 Men siziń hújjetińizdi aldım.\n\n"
               "Eger siz kurs tólemi haqqında chekti jiberiwdi qáleseńiz, "
               "dáslep kurstı tańlap, \"💳 Satıp alıw\" túymesin basıń."),
        'uz': ("📄 Мен сизнинг ҳужжатингизни олдим.\n\n"
               "Агар сиз курс тўлови ҳақида чекни юбормоқчи бўлсангиз, "
               "аввал курсни танлаб, \"💳 Сотиб олиш\" тугмасини босинг."),
    },
}

def get_text(key, lang_code='qr'):
    """
    Kilt hám til kodi arqalı tekstti alıw. Eger awdarma tabılmasa, qaraqalpaqsha versiyasın qaytaradı.
    """
    # Eger nadurıs til kodi berilse, standart tilge ótiw
    if lang_code not in ['qr', 'uz']:
        lang_code = 'qr'
        
    message_set = MESSAGES.get(key)
    if message_set:
        # Dáslep paydalanıwshı tilindegi tekstti, eger ol joq bolsa standart (qr) tildegi tekstti qaytarıw
        return message_set.get(lang_code, message_set.get('qr', f"NO_TRANSLATION_FOUND_FOR_LANG:{lang_code}"))
    
    # Eger kilt ulıwma tabılmasa
    return f"KEY_NOT_FOUND: {key}"