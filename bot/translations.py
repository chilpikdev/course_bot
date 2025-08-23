# bot/translations.py

MESSAGES = {
    # Til tańlaw
    'welcome_prompt_language': {
        'qr': "Assalawma aleykum! Til tańlań: \nAssalomu alaykum! Tilni tanlang:",
        'uz': "Assalomu alaykum! Tilni tanlang:",
    },
    'language_chosen_button': {
        'qr': "Qaraqalpaqsha",
        'uz': "O‘zbekcha",
    },
    'language_selected': {
        'qr': 'Til saylandı',
        'uz': 'Til tanlandi',
    },

    # Baslaw hám kontakt alıw
    'welcome_after_lang': {
        'qr': ("🎓 Kurs satıp alıw ushın mo'lsherlengen botqa xosh kelipsiz!\n\n"
               "Men sizge qolaylı kurstı tańlaw hám satıp alıwǵa járdem beremen.\n"
               "Baslaw ushın telefon nomerińizdi jiberiń."),
        'uz': ("🎓 Kurs sotib olish uchun mo‘ljallangan botga xush kelibsiz!\n\n"
               "Men sizga qulay kursni tanlash va sotib olishda yordam beraman.\n"
               "Boshlash uchun telefon raqamingizni yuboring."),
    },
    'request_contact_button': {
        'qr': "📱 Nomerdi jiberiw",
        'uz': "📱 Raqamni yuborish",
    },
    'contact_saved': {
        'qr': ("✅ Raxmet! Telefon nomerińiz saqlandı.\n\n"
               "Endi siz kurstı tańlay alasız:"),
        'uz': ("✅ Rahmat! Telefon raqamingiz saqlandi.\n\n"
               "Endi siz kursni tanlashingiz mumkin:"),
    },
    'returning_to_main_menu': {
        'qr': "🏠 Bas menyuǵa qaytıp atırmız.",
        'uz': "🏠 Bosh menyuga qaytmoqdamiz.",
    },

    # Bas menyu
    'main_menu_title': {
        'qr': '🏠 <b>Bas menyu</b>',
        'uz': '🏠 <b>Bosh menyu</b>',
    },
    'courses_button': {
        'qr': '📚 Kurslar',
        'uz': '📚 Kurslar',
    },
    'about_button': {
        'qr': 'ℹ️ Biz haqqımızda',
        'uz': 'ℹ️ Biz haqimizda',
    },
    'support_button': {
        'qr': '📞 Qollap-quwatlaw',
        'uz': '📞 Qo‘llab-quvvatlash',
    },

    # Kurslar dizimi
    'courses_list_title': {
        'qr': "📚 <b>Kurslar:</b>\n\nTolıq maǵlıwmat alıw hám satıp alıw ushın kurstı tańlań:",
        'uz': "📚 <b>Kurslar:</b>\n\nTo‘liq ma’lumot olish va sotib olish uchun kursni tanlang:",
    },
    'no_courses_yet': {
        'qr': "😔 Házirshe kurslar joq.\nKeyinirek urınıp kóriń.",
        'uz': "😔 Hozircha kurslar mavjud emas.\nKeyinroq urinib ko‘ring.",
    },
    'back_to_menu_button': {
        'qr': "🏠 Bas menyu",
        'uz': "🏠 Bosh menyu",
    },

    # Kurs haqqında maǵlıwmat
    'course_details_header': {
        'qr': "📚 <b>{course_name}</b>\n\n{course_description}\n\n",
        'uz': "📚 <b>{course_name}</b>\n\n{course_description}\n\n",
    },
    'price_label': {
        'qr': "💰 Bahası:",
        'uz': "💰 Narxi:",
    },
    'discount_label': {
        'qr': "🔥 <b>(-{discount}%)</b>\n\n",
        'uz': "🔥 <b>(-{discount}%)</b>\n\n",
    },
    'old_price_label': {
        'qr': "<s>{old_price}</s> <b>{price} sum</b>",
        'uz': "<s>{old_price}</s> <b>{price} so‘m</b>",
    },
    'current_price_label': {
        'qr': "<b>{price} sum</b>\n\n",
        'uz': "<b>{price} so‘m</b>\n\n",
    },
    'taken_slots': {
        'qr': "👥 Bánt orınlar: {current}/{max}\n",
        'uz': "👥 Band o‘rinlar: {current}/{max}\n",
    },
    'no_slots_left': {
        'qr': "❌ <b>Orınlar qalmadi</b>\n\n",
        'uz': "❌ <b>O‘rinlar qolmadi</b>\n\n",
    },
    'free_slots': {
        'qr': "✅ Bos orınlar: {free}\n\n",
        'uz': "✅ Bo‘sh o‘rinlar: {free}\n\n",
    },
    'buy_button': {
        'qr': "💳 {price} sum-ǵa satıp alıw",
        'uz': "💳 {price} so‘mga sotib olish",
    },
    'back_to_courses_button': {
        'qr': "◀️ Kurslar dizimine",
        'uz': "◀️ Kurslar ro‘yxatiga",
    },

    # Satıp alıw procesi
    'course_not_available': {
        'qr': "❌ Ókinishke oray, bul kurs endi qoljetimli emes.",
        'uz': "❌ Afsuski, bu kurs endi mavjud emas.",
    },
    'already_bought_course': {
        'qr': "✅ Siz \"{course_name}\" kursın satıp alıp bolǵansız.\n\nGruppaǵa silteme: {group_link}",
        'uz': "✅ Siz \"{course_name}\" kursini sotib olib bo‘lgansiz.\n\nGuruhga havola: {group_link}",
    },
    'payment_already_pending': {
        'qr': "⏳ Sizde \"{course_name}\" kursın satıp alıw ushın arza bar.\nStatusı: {status}\n\nAdministratordıń tekseriwin kútiń.",
        'uz': "⏳ Sizda \"{course_name}\" kursini sotib olish uchun ariza mavjud.\nHolati: {status}\n\nAdministratorning tekshiruvini kuting.",
    },
    'no_payment_methods_available': {
        'qr': "❌ Ókinishke oray, házir tólemniń qoljetimli usılları joq.\nQollap-quwatlaw xızmetine múrájat etiń.",
        'uz': "❌ Afsuski, hozir to‘lovning mavjud usullari yo‘q.\nQo‘llab-quvvatlash xizmatiga murojaat qiling.",
    },
    'select_payment_method_title': {
        'qr': "💳 <b>Kurs satıp alıw: {course_name}</b>\n\n💰 Bahası: <b>{price} sum</b>\n\nTólem usılın tańlań:",
        'uz': "💳 <b>Kurs sotib olish: {course_name}</b>\n\n💰 Narxi: <b>{price} so‘m</b>\n\nTo‘lov usulini tanlang:",
    },
    'back_button': {
        'qr': "◀️ Artqa",
        'uz': "◀️ Orqaga",
    },
    'cancel_button': {
        'qr': "❌ Biykar etiw",
        'uz': "❌ Bekor qilish",
    },

        # Tólem rekvizitleri hám chek jiberiw
    'payment_details_title': {
        'qr': "💳 <b>Kurs tólemi: {course_name}</b>\n\n",
        'uz': "💳 <b>Kurs to‘lovi: {course_name}</b>\n\n",
    },
    'amount_to_pay': {
        'qr': "💰 Tólem ushın summa: <b>{price} sum</b>\n\n",
        'uz': "💰 To‘lov uchun summa: <b>{price} so‘m</b>\n\n",
    },
    'payment_requisites': {
        'qr': "📋 <b>Tólem ushın rekvizitler:</b>\n\n",
        'uz': "📋 <b>To‘lov uchun rekvizitlar:</b>\n\n",
    },
    'important_note': {
        'qr': "\n\n⚠️ <b>Áhmiyetli:</b>\n",
        'uz': "\n\n⚠️ <b>Muhim:</b>\n",
    },
    'important_note_1': {
        'qr': "• Anıq <b>{price} sum</b> ótkeriwiz kerek\n",
        'uz': "• Aniq <b>{price} so‘m</b> o‘tkazishingiz kerak\n",
    },
    'important_note_2': {
        'qr': "• Tólemnen keyin chektiń skrinshotın jiberiń\n",
        'uz': "• To‘lovdan keyin chek skrinshotini yuboring\n",
    },
    'important_note_3': {
        'qr': "• Administrator tólemdi tekseredi hám gruppa siltemesin jiberedi\n\n",
        'uz': "• Administrator to‘lovni tekshiradi va guruh havolasini yuboradi\n\n",
    },
    'send_receipt_prompt': {
        'qr': "📸 Chektiń skrinshotın yamasa PDF hújjetin jiberiń:",
        'uz': "📸 Chek skrinshotini yoki PDF hujjatini yuboring:",
    },
    'cancel_purchase_button': {
        'qr': "❌ Satıp alıwdı biykarlaw",
        'uz': "❌ Xaridni bekor qilish",
    },
    'purchase_cancelled': {
        'qr': ("❌ Satıp alıw biykar etildi.\n\n"
               "Siz basqa kurs tańlawıńız yamasa keyinirek qaytıwıńız múmkin."),
        'uz': ("❌ Xarid bekor qilindi.\n\n"
               "Siz boshqa kurs tanlashingiz yoki keyinroq qaytishingiz mumkin."),
    },

    # Chekti qayta islew
    'receipt_accepted_photo': {
        'qr': "✅ <b>Chek qabıllandı!</b>\n\n",
        'uz': "✅ <b>Chek qabul qilindi!</b>\n\n",
    },
    'receipt_accepted_document': {
        'qr': "✅ <b>Hújjet qabıllandı!</b>\n\n",
        'uz': "✅ <b>Hujjat qabul qilindi!</b>\n\n",
    },
    'course_label': { 'qr': "📚 Kurs:", 'uz': "📚 Kurs:", },
    'amount_label': { 'qr': "💰 Summa:", 'uz': "💰 Summa:", },
    'payment_method_label': { 'qr': "💳 Tólem usılı:", 'uz': "💳 To‘lov usuli:", },
    'file_label': { 'qr': "📄 Fayl:", 'uz': "📄 Fayl:", },
    'payment_pending_admin_review': {
        'qr': ("\n⏳ Siziń tólemińiz administratorǵa tekseriw ushın jiberildi.\n"
               "Ádette tekseriw 2 saatqa shekem waqıt aladı.\n\n"
               "Tastıyıqlanǵannan keyin siz kurs gruppasına silteme alasız."),
        'uz': ("\n⏳ Sizning to‘lovingiz administratorga tekshiruv uchun yuborildi.\n"
               "Odatda tekshiruv 2 soatgacha vaqt oladi.\n\n"
               "Tasdiqlangandan keyin siz kurs guruhiga havola olasiz."),
    },

    # Tólem nátiyjeleri
    'payment_approved_title': {
        'qr': "✅ <b>Tólem tastıyıqlandı!</b>\n\n",
        'uz': "✅ <b>To‘lov tasdiqlandi!</b>\n\n",
    },
    'congratulations_on_purchase': {
        'qr': "🎉 Satıp alıwıńız benen qutlıqlaymız!\n\n",
        'uz': "🎉 Xaridingiz bilan tabriklaymiz!\n\n",
    },
    'group_link_message': {
        'qr': "🔗 <b>Kurs gruppasına silteme:</b>\n{group_link}\n\n",
        'uz': "🔗 <b>Kurs guruhiga havola:</b>\n{group_link}\n\n",
    },
    'join_group_and_start': {
        'qr': "Gruppaǵa qosılıń hám oqıwdı baslań!\nEger sorawlarıńız bolsa, qollap-quwatlaw xızmetine múrájat etiń.",
        'uz': "Guruhga qo‘shiling va o‘qishni boshlang!\nAgar savollaringiz bo‘lsa, qo‘llab-quvvatlash xizmatiga murojaat qiling.",
    },
    'other_courses_button': {
        'qr': "📚 Basqa kurslar",
        'uz': "📚 Boshqa kurslar",
    },
    'payment_rejected_title': {
        'qr': "❌ <b>Tólem biykar etildi</b>\n\n",
        'uz': "❌ <b>To‘lov bekor qilindi</b>\n\n",
    },
    'payment_rejected_body': {
        'qr': "Ókinishke oray, siziń tólemińiz tekseriwden ótpedi.\n\n",
        'uz': "Afsuski, sizning to‘lovingiz tekshiruvdan o‘tmadi.\n\n",
    },
    'admin_comment_message': {
        'qr': "💬 <b>Administrator kommentariyi:</b>\n{comment}\n\n",
        'uz': "💬 <b>Administrator izohi:</b>\n{comment}\n\n",
    },
    'if_questions_contact_support': {
        'qr': "Eger sorawlarıńız bolsa, qollap-quwatlaw xızmetine múrájat etiń.\nSiz taǵı bir márte tólewge urınıp kóriwińizge boladı.",
        'uz': "Agar savollaringiz bo‘lsa, qo‘llab-quvvatlash xizmatiga murojaat qiling.\nSiz yana bir bor to‘lashga urinib ko‘rishingiz mumkin.",
    },
    'retry_payment_button': {
        'qr': "🔄 Qaytadan urınıp kóriw",
        'uz': "🔄 Qaytadan urinib ko‘rish",
    },
    'payment_method_card_number': {
        'qr': "Karta nomeri:",
        'uz': "Karta raqami:",
    },
    'payment_method_cardholder': {
        'qr': "Qabıllawshı:",
        'uz': "Qabul qiluvchi:",
    },
    'payment_method_bank': {
        'qr': "Bank:",
        'uz': "Bank:",
    },
    'payment_method_instructions': {
        'qr': "\nInstrukciya:",
        'uz': "\nInstruksiya:",
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
        'uz': ("🤖 <b>Yordam</b>\n\n"
               "Mavjud buyruqlar:\n"
               "/start - Bot bilan ishlashni boshlash\n"
               "/help - Ushbu yo‘riqnomani ko‘rsatish\n"
               "/cancel - Bosh menyuga qaytish\n\n"
               "Navigatsiya uchun tugmalardan foydalaning.\n\n"
               "📚 <b>Kurs qanday sotib olinadi:</b>\n"
               "1. \"📚 Kurslar\"ni tanlang\n"
               "2. Qiziqtirgan kursni tanlang\n"
               "3. \"💳 Sotib olish\"ni bosing\n"
               "4. To‘lov usulini tanlang\n"
               "5. Rekvizitlar bo‘yicha to‘lang\n"
               "6. Chek skrinshotini yuboring\n"
               "7. Tasdiqlanishini kuting\n\n"
               "Biror muammo paydo bo‘lsa, qo‘llab-quvvatlash xizmatiga murojaat qiling."),
    },

    # Qátelikler
    'error_start_command': {
        'qr': "Qátelik júz berdi. /start buyrıǵın qaytadan teriń",
        'uz': "Xatolik yuz berdi. /start buyrug‘ini qaytadan tering",
    },
    'error_not_your_contact': {
        'qr': "❌ Ótinish, tek óz telefon nomerińizdi jiberiń.",
        'uz': "❌ Iltimos, faqat o‘z telefon raqamingizni yuboring.",
    },
    'error_contact_save': {
        'qr': "Kontaktıńızdı saqlawda qátelik júz berdi. Qaytadan urınıp kóriń.",
        'uz': "Kontaktni saqlashda xatolik yuz berdi. Qaytadan urinib ko‘ring.",
    },
    'info_not_found': {
        'qr': "Maǵlıwmat tabılmadı.",
        'uz': "Ma’lumot topilmadi.",
    },
    'support_info_not_found': {
        'qr': "Qollap-quwatlaw haqqında maǵlıwmat tabılmadı.",
        'uz': "Qo‘llab-quvvatlash haqida ma’lumot topilmadi.",
    },
    'error_loading_course_details': {
        'qr': "Kurs haqqında maǵlıwmat júklewde qátelik júz berdi.",
        'uz': "Kurs haqida ma’lumot yuklashda xatolik yuz berdi.",
    },
    'error_loading_courses': {
        'qr': "Kurslardı júklewde qátelik júz berdi.",
        'uz': "Kurslarni yuklashda xatolik yuz berdi.",
    },
    'error_buy_course': {
        'qr': "Satıp alıwdı rásmiylestiriwde qátelik júz berdi.",
        'uz': "Sotib olishni rasmiylashtirishda xatolik yuz berdi.",
    },
    'error_payment_method_selection': {
        'qr': "Tólem usılın tańlawda qátelik júz berdi.",
        'uz': "To‘lov usulini tanlashda xatolik yuz berdi.",
    },
    'error_purchase_data_lost': {
        'qr': "❌ Qátelik: satıp alıw haqqında maǵlıwmatlar joǵalǵan. Qaytadan baslań.",
        'uz': "❌ Xatolik: sotib olish haqida ma’lumotlar yo‘qolgan. Qaytadan boshlang.",
    },
    'error_photo_not_found': {
        'qr': "❌ Foto tabılmadı. Qaytadan urınıp kóriń.",
        'uz': "❌ Fotosurat topilmadi. Qaytadan urinib ko‘ring.",
    },
    'error_photo_download': {
        'qr': "❌ Fotanı júklep alıw múmkin bolmadı. Qaytadan urınıp kóriń.",
        'uz': "❌ Fotosuratni yuklab olish mumkin bo‘lmadi. Qaytadan urinib ko‘ring.",
    },
    'error_document_not_found': {
        'qr': "❌ Hújjet tabılmadı. Qaytadan urınıp kóriń.",
        'uz': "❌ Hujjat topilmadi. Qaytadan urinib ko‘ring.",
    },
    'error_file_too_large': {
        'qr': "❌ Fayl júdá úlken. Maksimum 10 MB.",
        'uz': "❌ Fayl juda katta. Maksimum 10 MB.",
    },
    'error_unsupported_format': {
        'qr': "❌ Qollap-quwatlanbaytuǵın format. PDF, JPG yamasa PNG formatlarınan paydalanıń.",
        'uz': "❌ Qo‘llab-quvvatlanmaydigan format. PDF, JPG yoki PNG formatlaridan foydalaning.",
    },
    'error_file_download': {
        'qr': "❌ Fayldı júklep alıw múmkin bolmadı. Qaytadan urınıp kóriń.",
        'uz': "❌ Faylni yuklab olish mumkin bo‘lmadi. Qaytadan urinib ko‘ring.",
    },
    'error_payment_save': {
        'qr': "❌ Tólemdi saqlawda qátelik júz berdi. Qaytadan urınıp kóriń.",
        'uz': "❌ To‘lovni saqlashda xatolik yuz berdi. Qaytadan urinib ko‘ring.",
    },
    'error_processing_receipt': {
        'qr': "Chekti qayta islewde qátelik júz berdi.",
        'uz': "Chekni qayta ishlashda xatolik yuz berdi.",
    },
    'error_processing_document': {
        'qr': "Hújjet qayta islewde qátelik júz berdi.",
        'uz': "Hujjatni qayta ishlashda xatolik yuz berdi.",
    },

    # Fayl alǵanda (satıp alıwdan tıs)
    'photo_received_outside_payment': {
        'qr': ("📸 Men siziń fotońızdı aldım.\n\n"
               "Eger siz kurs tólemi haqqında chekti jiberiwdi qáleseńiz, "
               "dáslep kurstı tańlap, \"💳 Satıp alıw\" túymesin basıń."),
        'uz': ("📸 Men sizning fotosuratingizni oldim.\n\n"
               "Agar siz kurs to‘lovi haqida chek yubormoqchi bo‘lsangiz, "
               "avval kursni tanlab, \"💳 Sotib olish\" tugmasini bosing."),
    },
    'document_received_outside_payment': {
        'qr': ("📄 Men siziń hújjetińizdi aldım.\n\n"
               "Eger siz kurs tólemi haqqında chekti jiberiwdi qáleseńiz, "
               "dáslep kurstı tańlap, \"💳 Satıp alıw\" túymesin basıń."),
        'uz': ("📄 Men sizning hujjatingizni oldim.\n\n"
               "Agar siz kurs to‘lovi haqida chek yubormoqchi bo‘lsangiz, "
               "avval kursni tanlab, \"💳 Sotib olish\" tugmasini bosing."),
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