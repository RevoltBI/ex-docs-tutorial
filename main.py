#!/usr/bin/env python3

import constant
import requests
import xmltodict
import csv

print("Starting downloading process...")

#get dealers list
dealersUrl = constant.AUTOCARIS_DEALERS_URL_FINAL
adsUrl = constant.AUTOCARIS_ADS_URL_FINAL
response = requests.post(dealersUrl, data = { 'name' : constant.AUTOCARIS_LOGIN_NAME, 'password' : constant.AUTOCARIS_LOGIN_PW })

#get dealer ids from xml
doc = xmltodict.parse(response.text)

#get cars from dealers
cars = []

with open('/data/out/tables/data.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)

    writer.writerow([
        "id",
        "bid",
        "inserted",
        "edited",
        "del",
        "category",
        "sport_car",
        "producer_text",
        "model_text",
        "model_supplement",
        "specification",
        "gen_equip",
        "content_dec",
        "content_cm",
        "engine_spec",
        "color",
        "state",
        "gear",
        "gearing",
        "constr",
        "fuel",
        "constr_year",
        "model_year",
        "to_operation",
        "km",
        "seats",
        "kw",
        "stk",
        "me",
        "doors_number",
        "speeds_number",
        "service_book",
        "nocrash",
        "vat_expel_flag",
        "vat_expel_text",
        "new_flag",
        "sales_price",
        "burza_price",
        "new_car_price",
        "payment",
        "payment_count",
        "repayment",
        "extras",
        "remarks",
        "etc",
        "prvni_majitel",
        "owner",
        "leasing",
        "credit",
        "show_flag",
        "carstore",
        "akce",
        "kodpobo",
        "autoplus",
        "skodaplus",
        "rocni_vuz",
        "payment_price",
        "monthly_from",
        "cebnumber",
        "naceste",
        "finpoz",
        "nadstvyb",
        "websklad",
        "refvuz",
        "consumption",
        "celkhmotn",
        "uzihmotn",
        "provhmotn",
        "delkavuz",
        "sirkavuz",
        "vyskavuz",
        "delkaplocha",
        "sirkaplocha",
        "vyskaplocha",
        "citroenselect",
        "operativnileasing",
        "leasing_pos",
        "su_pos",
        "currency",
        "photos"
    ])

    for shopitem in doc['subjects']['subject']:
        id = shopitem['id']

        #download ads for current dealer id
        adsResponse = requests.post(adsUrl, data = { 'name' : constant.AUTOCARIS_LOGIN_NAME, 'password' : constant.AUTOCARIS_LOGIN_PW, 'id' : id })
        adsResponse = adsResponse.text

        #parse data
        doc = xmltodict.parse(adsResponse)
        error = doc['cars']['error']

        if error['@is_error'] == "1":
            continue

        for car in doc['cars']['car']:
            extras = []
            remarks = []
            photos = []

            if isinstance(car, str):
                continue

            try:
                tempExtras = car['extras']['extra']

                if tempExtras:
                    for extra in tempExtras:
                        extras.append(extra)

                tempRemarks = car['remarks']['remark']

                if tempRemarks:
                    for remark in tempRemarks:
                        remarks.append(remark)

                tempPhotos = car['photos']['photo']

                if tempPhotos:
                    for photo in tempPhotos:
                        if isinstance(photo, dict):
                            photos.append(photo['#text'])
            except:
                print("No extras, remarks or photos")

            writer.writerow([
                car['id'],
                car['bid'],
                car['inserted'],
                car['edited'],
                car['del'],
                car['category'],
                car['sport_car'],
                car['producer_text'],
                car['model_text'],
                car['model_supplement'],
                car['specification'],
                car['gen_equip'],
                car['content_dec'],
                car['content_cm'],
                car['engine_spec'],
                car['color'],
                car['state'],
                car['gear'],
                car['gearing'],
                car['constr'],
                car['fuel'],
                car['constr_year'],
                car['model_year'],
                car['to_operation'],
                car['km'],
                car['seats'],
                car['kw'],
                car['stk'],
                car['me'],
                car['doors_number'],
                car['speeds_number'],
                car['service_book'],
                car['nocrash'],
                car['vat_expel_flag'],
                car['vat_expel_text'],
                car['new_flag'],
                car['sales_price'],
                car['burza_price'],
                car['new_car_price'],
                car['payment'],
                car['payment_count'],
                car['repayment'],
                extras,
                remarks,
                car['etc'],
                car['prvni_majitel'],
                car['owner'],
                car['leasing'],
                car['credit'],
                car['show_flag'],
                car['carstore'],
                car['akce'],
                car['kodpobo'],
                car['autoplus'],
                car['skodaplus'],
                car['rocni_vuz'],
                car['payment_price'],
                car['monthly_from'],
                car['cebnumber'],
                car['naceste'],
                car['finpoz'],
                car['nadstvyb'],
                car['websklad'],
                car['refvuz'],
                car['consumption'],
                car['celkhmotn'],
                car['uzihmotn'],
                car['provhmotn'],
                car['delkavuz'],
                car['sirkavuz'],
                car['vyskavuz'],
                car['delkaplocha'],
                car['sirkaplocha'],
                car['vyskaplocha'],
                car['citroenselect'],
                car['operativnileasing'],
                car['leasing_pos'],
                car['su_pos'],
                car['currency'],
                photos
            ])

print("Job done!")
