
def poi(java_port):

    desc1 = '<head><meta charset="UTF-8"><style type="text/css">td{padding-right:15px;}</style></head>' \
               '<body><div class="wDYxhc" lang="en-NL" data-md="50" data-hveid="CCkQAA" data-ved="2ahUKEwj3' \
               'nbarsLTvAhXP0aQKHc8MDCAQkCkwGHoECCkQAA">&nbsp;</div><div class="xsZWvb EfDVh wDYxhc" lang="en-NL"' \
               ' data-attrid="kc:/location/location:address" data-md="1002" data-hveid="CD4QAA" data-ved="2ahUKEwj3' \
               'nbarsLTvAhXP0aQKHc8MDCAQkCkwGnoECD4QAA"><div class="Z1hOCe"><table style="width: 535px;"><tbody><tr>' \
               '<td style="width: 148px;"><img src="http://145.100.59.72:'+java_port+'/images/OCHA.jpg" alt="" width="200" height="100" /></td>' \
               '<td style="width: 371px; text-align: left;"><strong>OCHA</strong> is a Thai restaurant that serves spicy food.' \
            '<span style="background-color: #ffffff;"><a href="https://foursquare.com/v/ocha/4b06f081f964a52098f322e3" target="_blank" rel="noopener noreferrer">Read more</a></span>&nbsp;</td></tr></tbody></table>' \
               '</div></div></body>'

    desc2 = '<head><meta charset="UTF-8"><style type="text/css">td{padding-right:15px;}</style></head>' \
             '<body><div class="wDYxhc" lang="en-NL" data-md="50" data-hveid="CCkQAA" data-ved="2ahUKEwj3' \
             'nbarsLTvAhXP0aQKHc8MDCAQkCkwGHoECCkQAA">&nbsp;</div><div class="xsZWvb EfDVh wDYxhc" lang="en-NL"' \
             ' data-attrid="kc:/location/location:address" data-md="1002" data-hveid="CD4QAA" data-ved="2ahUKEwj3' \
             'nbarsLTvAhXP0aQKHc8MDCAQkCkwGnoECD4QAA"><div class="Z1hOCe"><table style="width: 535px;"><tbody><tr>' \
             '<td style="width: 148px;"><img src="http://145.100.59.72:'+java_port+'/images/hannekes.jpg" alt="" width="200" height="100" /></td>' \
             '<td style="width: 371px; text-align: left;"><strong>Hannekes Boom</strong> is an easygoing dockside restaurant with a terrace serving seafood, meat & veggie dishes.' \
             '<span style="background-color: #ffffff;"><a href="http://www.hannekesboom.nl/" target="_blank" rel="noopener noreferrer">Read more</a></span>&nbsp;</td></tr></tbody></table>' \
             '</div></div></body>'

    desc3 = '<head><meta charset="UTF-8"><style type="text/css">td{padding-right:15px;}</style></head>' \
             '<body><div class="wDYxhc" lang="en-NL" data-md="50" data-hveid="CCkQAA" data-ved="2ahUKEwj3' \
             'nbarsLTvAhXP0aQKHc8MDCAQkCkwGHoECCkQAA">&nbsp;</div><div class="xsZWvb EfDVh wDYxhc" lang="en-NL"' \
             ' data-attrid="kc:/location/location:address" data-md="1002" data-hveid="CD4QAA" data-ved="2ahUKEwj3' \
             'nbarsLTvAhXP0aQKHc8MDCAQkCkwGnoECD4QAA"><div class="Z1hOCe"><table style="width: 535px;"><tbody><tr>' \
             '<td style="width: 148px;"><img src="http://145.100.59.72:'+java_port+'/images/oriental.jpg" alt="" width="200" height="100" /></td>' \
             '<td style="width: 371px; text-align: left;"><strong>Oriental City, </strong> bustling multi-floor Cantonese restaurant serving fresh seafood specials & a vast choice of dim sum.' \
             '<span style="background-color: #ffffff;"><a href="http://www.oriental-city.com/" target="_blank" rel="noopener noreferrer">Read more</a></span>&nbsp;</td></tr></tbody></table>' \
             '</div></div></body>'



    data = {}
    data['pois'] = []

    data['pois'].append({
        "poiID": 1,
        "poiName": 'OCHA',
        "poiDesc": desc1
    })

    data['pois'].append({
        "poiID": 2,
        "poiName": 'Hannekes Boom',
        "poiDesc": desc2
    })

    data['pois'].append({
        "poiID": 3,
        "poiName": ' Oriental City',
        "poiDesc": desc3
    })

    return data['pois']

