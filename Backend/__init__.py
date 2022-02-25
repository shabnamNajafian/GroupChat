from flask import Flask, request, render_template

from waitress import serve
import json
import sqlite3
import random

import sys

from get_pois import poi
from db_operations import *

app = Flask(__name__)

port = sys.argv[1]
minority_scenario = int(sys.argv[2])
persuasive_task = int(sys.argv[3])
boss_in_minority = int(sys.argv[4])
java_port = sys.argv[5]


# ip_add = 'localhost:'
# This ip address should be modified based on the running server's ip address
ip_add = '145.100.59.72:'

@app.before_request
def before_request():
    g.db = sqlite3.connect("database.db")


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


# Randomly assign one of the six existing scenarios to Prolific participants
# The used ip address should be modified based on the running server's ip address
@app.route('/welcome', methods=['GET', 'POST'])
def home():
    p_id = request.args.get('PROLIFIC_PID')
    addresses = []
    addresses.append('http://145.100.59.72:8080/join?PROLIFIC_PID='+p_id)
    addresses.append('http://145.100.59.72:8081/join?PROLIFIC_PID='+p_id)
    addresses.append('http://145.100.59.72:8082/join?PROLIFIC_PID='+p_id)
    addresses.append('http://145.100.59.72:8083/join?PROLIFIC_PID='+p_id)
    addresses.append('http://145.100.59.72:8084/join?PROLIFIC_PID='+p_id)
    addresses.append('http://145.100.59.72:8085/join?PROLIFIC_PID='+p_id)

    add = random.choice(addresses)
    return render_template('welcome.html', add=add)


@app.route('/', methods=['POST'])
def requests():
    request_data = request.get_json(force=True, silent=True)
    print(request_data)
    uuid = request_data['uuid']
    pid = request_data['pid']
    name1 = request_data['name1']
    name2 = request_data['name2']
    name3 = request_data['name3']
    state = request_data['state']
    action = request_data['action']
    scenario = request_data['scenario']
    persuasive = request_data['persuasive']
    boss = request_data['boss']
    content = request_data['content']
    dct = ""

    if boss == 1 and minority_scenario == 0:
        tmp = name3
        name3 = name2
        name2 = tmp

    if not state:
        if boss == 1 and minority_scenario == 0:
            tmp = name3
            name3 = name2
            name2 = tmp
        dct = state1(uuid, pid, name1, name2, name3, minority_scenario, persuasive_task, boss_in_minority)

    elif (state == "state1") and action == "Next":
        dct = state2(scenario, persuasive, boss)

    elif (state == "state2") and action == "Next":
        dct = state3(scenario, persuasive, boss)

    elif (state == "state3") and action == "Next":
        dct = state4(scenario, persuasive, boss)

    elif (state == "state4") and action == "Next":
        dct = state5(uuid, content, scenario, persuasive, boss)

    elif state == "state5" and action == "Switch to Group":
        print("name3333 ", name3)
        dct = state6(uuid, name1, name2, name3, scenario, persuasive, boss)

    elif state == "state6" and action == "Next":
        dct = state7(scenario, persuasive, boss)

    elif state == "state7" and action == "Switch to Tourybot":
        dct = state8(uuid, name1, name2, name3, scenario, persuasive, boss)

    elif state == "state8" and action == "Send to the Group":
        inf_l = [x.strip() for x in content.split(',')]
        # if (inf_l.count('emo') > 0 or inf_l.count('loc') > 0 or inf_l.count('fin') > 0 or inf_l.count('rel') > 0
        #         or inf_l.count('sex') > 0 or inf_l.count('health') > 0 or inf_l.count('alc') > 0):
        dct = state9(uuid, name1, name2, name3, content, scenario, persuasive, boss, state, action)

    elif state == "state9" and action == "Next":
        dct = state10(uuid, name3, scenario, persuasive, boss)

    elif state == "state10" and action == "Next":
        dct = finalizing_exp_actions(uuid, scenario, persuasive, boss)

    return json.dumps(dct)


def state1(uid, pid, name1, name2, name3, minority, persuasive, boss):
    ex = pid_exists(pid)
    if ex:
        tnk = '<p>You have already completed this task. Sorry for any inconvenience! Please' \
              ' press the button below to exit from the study.</p>'
        json1 = write_in_json_format('TouryBot', tnk,
                                     "", ['Exit from the Study'], 0, "POPUP", "",
                                     "exisiting_pid", minority, persuasive, boss)

    else:
        strt = start()

        nxt = next_state()

        json1 = write_in_json_format('TouryBot', strt + nxt, 'TouryBot', ['Next'], 0, "", "",
                                     "state1", minority, persuasive, boss)

        insert_profile(uid, pid, name1, name2, name3, minority, persuasive, boss)
    return json1


def state2(scenario, persuasive, boss):
        dsc = task_desc(scenario, persuasive)
        nxt = next_state()
        json1 = write_in_json_format('TouryBot', dsc + nxt, 'TouryBot', ['Next'], 0, "", "",
                                     "state2", scenario, persuasive, boss)
        return json1


def state3(scenario, persuasive, boss):
    dsc = '<p><span style="color: #000000;"><strong>Ranking a few places:</strong></p><p><span style="font-weight: 400; color: #000000;">Please imagine that you' \
            ' are planning a &ldquo;single-day trip to Amsterdam&rdquo;.&nbsp;</span><span style="font-weight: 400; color: #000000;">' \
            'For the next step, sort the places you see in the order of your interest to visit that place by <strong>' \
          'drag and drop</strong>. </span></span></p>'

    nxt = next_state()
    json1 = write_in_json_format('TouryBot', dsc + nxt, 'TouryBot', ['Next'], 0, "", "",
                                 "state3", scenario, persuasive, boss)
    print("state3 res ", json1)
    return json1


def state4(scenario, persuasive, boss):
    p = poi(java_port)
    nxt = next_state()
    exp = '<ol><li class="draggable" id=1 draggable="true">' + p[0]['poiDesc'] + '</li><li class="draggable" id=2 draggable="true">' + p[1]['poiDesc'] + '</li><li class="draggable" id=3 draggable="true">' + p[2]['poiDesc'] + '</li>   </ol>'
    # exp = '<html lang="en"><head><meta charset="utf-8"><title>jQuery UI Sortable - Default functionality</title><link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css"><link rel="stylesheet" href="/resources/demos/style.css"><style>#sortable { list-style-type: none; margin: 0; padding: 0;}#sortable li { margin: 0 3px 3px 3px; padding: 0.4em; padding-left: 1.5em;  }#sortable li span { position: absolute; margin-left: -1.3em; }</style><script src="https://code.jquery.com/jquery-1.12.4.js"></script><script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script></head><body>' \
    #        '<ul id="draggable"><li id=1 class="draggable ui-state-default" draggable="true"><span class="ui-icon ui-icon-arrowthick-2-n-s"></span>' + p[0]['poiDesc'] + '</li><li id=2 class="draggable ui-state-default" draggable="true"><span class="ui-icon ui-icon-arrowthick-2-n-s"></span>' + p[1]['poiDesc'] + '</li><li id=3 class="draggable ui-state-default" draggable="true"><span class="ui-icon ui-icon-arrowthick-2-n-s"></span>' + p[2]['poiDesc'] + '</li></ul>'\
    #        '<input type="submit" value="Submit" onclick="submit()"></body></html>'

    json1 = write_in_json_format('TouryBot', exp + nxt, 'TouryBot', ['Next'], 0, "", "",
                                 "state4", scenario, persuasive, boss)
    return json1


def state5(uid, content, minority, persuasive, boss):
    print ("content ", content)
    poi_list = [x.strip() for x in content.split(',')]
    if minority == 0:
        selected_poi = poi_list[0]
    else:
        selected_poi = poi_list[2]

    desc = tourybot_message()
    json1 = write_in_json_format('TouryBot', desc, 'TouryBot', ['Switch to Group'], 0, "", "",
                                 "state5", minority, persuasive, boss)

    insert_rating(uid, content, selected_poi, minority)

    return json1


def state6(uid, name1, name2, name3, scenario, persuasive, boss):
    json1 = write_in_json_format('Group', '', '', [], 0, "SWITCH", "", "state6", scenario, persuasive, boss)

    selected_place = get_selected_poi(uid)
    pref, img = pref_bot_part(selected_place, name1, name2, name3, scenario)
    nxt = next_state()
    json2 = write_in_json_format('Group', pref + img + nxt, 'TouryBot', ['Next'], 0, "", json1, "state6", scenario, persuasive, boss)
    return json2


def state7(scenario, persuasive, boss):
    return tourybot_message_in_group("", scenario, persuasive, boss, "state7")


def state8(uid, name1, name2, name3, scenario, persuasive, boss):
    json1 = write_in_json_format('TouryBot', '', '', [], 0, "SWITCH", "", "state8", scenario, persuasive, boss)

    selected_place = get_selected_poi(uid)
    exp = create_all_info(selected_place, name1, name2, name3, scenario, persuasive, boss)
    jsn = write_in_json_format('TouryBot', exp, 'TouryBot', ["Send to the Group"], 0, "CHECKBOX", json1,
                                 "state8", scenario, persuasive, boss)

    return jsn


def state9(uid, name1, name2, name3, content, minority, persuasive, boss, state, action):
    info_list = [x.strip() for x in content.split(',')]
    print(info_list)
    emo_exp = ""
    loc_exp = ""
    fin_exp = ""
    rel_exp = ""
    sex_exp = ""
    health_exp = ""
    alc_exp = ""
    emo = loc = fin = rel = sex = health = alc = 0
    if info_list.count('emo') > 0:
        emo = 1
        emo_exp = create_emo_exp(minority)
    if info_list.count('loc') > 0:
        loc = 1
        loc_exp = create_loc_exp(minority)
    if info_list.count('fin') > 0:
        fin = 1
        fin_exp = create_fin_exp(minority)
    if info_list.count('rel') > 0:
        rel = 1
        rel_exp = create_rel_exp(minority)
    if info_list.count('sex') > 0:
        sex = 1
        sex_exp = create_sex_exp(minority)
    if info_list.count('health') > 0:
        health = 1
        health_exp = create_health_exp(minority)
    if info_list.count('alc') > 0:
        alc = 1
        alc_exp = create_alc_exp(minority)

    selected_place = get_selected_poi(uid)
    pref = first_pref_group_part(selected_place['poiName'], name1, name2, name3, minority)
    fin_exp = pref + emo_exp + loc_exp + fin_exp + rel_exp + sex_exp + health_exp + alc_exp
    print(fin_exp)

    next_st = "state9"
    nxt = next_state()

    json1 = write_in_json_format('Group', '', '', [], 0, "SWITCH", "", next_st, minority, persuasive, boss)

    json2 = write_in_json_format('Group', fin_exp + nxt, name1, ['Next'], 0, "", json1, next_st, minority, persuasive, boss)

    insert_information(uid, emo, loc, fin, rel, health, sex, alc, minority, persuasive, boss)

    return json2


def state10(uid, name3, minority, persuasive, boss):
    exp2 = final_group_message(minority)
    nxt = next_state()
    return write_in_json_format('Group', exp2 + nxt, name3, ['Next'], 0, "", "", "state10", minority, persuasive,
                                 boss)


def finalizing_exp_actions(uid, scenario, persuasive, boss):
    desc = '<p style="text-align: center;"><strong>Thank you for completing this step. Please press the link below to go to the final step ' \
           'of the study.</strong><br><span style="text-align: center;"><a href=' \
           '"http://' + ip_add + port + '/demographics?uuid=' + uid + '"><strong>Next</strong></a></span></p>'
    next_state = "go_to_the_benefits"

    jsn = write_in_json_format('TouryBot', desc, '', [], 0, "POPUP", "",
                               next_state, scenario, persuasive, boss)
    return jsn


def pref_bot_part(p, name1, name2, name3, scenario):
    img = p['poiDesc']
    pref = ""
    gen = 'Hi everybody. I am TouryBot, your advisor for this group trip. The <strong>' + p['poiName'] + '</strong> seems ' \
    'good for your group since it represents the majority preferences in the group. '
    # majority scenario
    if scenario == 0:
        pref = '<p>' + gen + name1 + ' and ' + name2 + \
               ' like this place, but this place is not ' + name3 + '&rsquo;s first choice' \
                                                                          '. Wanna try it?</p>'
    # minority scenario
    elif scenario == 1:
        pref = '<p>' + gen + name2 + ' and ' + name3 + \
               ' like this place, but this place is not ' + name1 + '&rsquo;s first choice' \
                                                                    '. Wanna try it?</p>'
    return pref, img


def first_pref_group_part(place, name1, name2, name3, scenario):
    pref = ""
    # majority scenario
    if scenario == 0:
        pref = '<span style="color: #000000;">The ' + place + ' seems good' \
       ' for our group: although this is not ' + name3 + '\' first choice, ' + name2 + ' and I really like this place.</span>'
    # minority scenario
    elif scenario == 1:
        pref = '<span style="color: #000000;">The ' + place + ' seems good for' \
               ' ' + name2 + ' and ' + name3 + ', but this place is not my first choice.</span>'
    return pref


def instruction():
    return '<p><strong>INSTRUCTIONS:</strong></p>'


def share_with_group():
    shr = '<p>To <strong>share</strong> this information with your group,&nbsp;press the "<span style="background-color' \
          ': #4BA686; color: #FFFFFF;"><strong>Send to the Group</strong></span>" button below.</p>'
    return shr


def final_group_message(minority):
    exp = ""
    if minority == 0:
        exp = '<p>OK, let’s go there :)</p>'
    elif minority == 1:
        exp = '<p>OK, let’s skip this place :)</p>'
    return exp


def write_in_json_format(chat_view, explanation, from_whom, buttons, delay, typ, data, state, scenario, persuasive, boss):
    if not 'actions' in data or len(data['actions']) == 0:
        data = {}
        data["state"] = ""
        data["actions"] = []
    data["state"] = state
    data["scenario"] = scenario
    data["persuasive"] = persuasive
    data["boss"] = boss
    data["actions"].append({
        "group": chat_view,
        "text": explanation,
        "fromWhom": from_whom,
        "buttons": buttons,
        "delay": delay,
        "type": typ
    })
    return data


def start():
    return '<p><span style="color: #000000;">Hi there. I am <strong>TouryBot</strong> your advisor for this group trip. I will try to find a place to visit for your group. I will ask you a few questions and based on your answers, I will help you provide your group with an explanation for the recommended place.</span></p>'


def task_desc(scenario, persuasive):
    if persuasive == 0:
        sce = 'As a reminder, your task is to reach a decision in your group.'
    else:
        if scenario == 1:
            sce = 'As a reminder, your task is to convince the other group members to skip the suggested place.'
        else:
            sce = 'As a reminder, your task is to convince the other group members to visit the suggested place.'
    return '<p><span style="color: #000000;">The recommendation comes with personal information about you and two group members.</p><p><span style="color: #000000;"><strong>This will not be your actual information, but please imagine that it is correct.</strong></span></span></p><p><span style="color: #fd7e14;"><strong>' + sce + '</strong></span></p>'


def generate_shuffle_checkboxes(minority):
    s = list(range(7))
    random.shuffle(s)

    checkboxes = []
    exp = []
    if minority == 0:
        checkboxes.append(
            '<div class="form-check"><input id="emo" class="form-check-input" type="checkbox" value="" onclick="myFunction()"/> <label class="form-check-label" for="defaultCheck1"><strong> Emotion-related information</strong> (i.e., you feel grief today, this place cheers you up.)</label></div>')
        checkboxes.append(
            '<div class="form-check"><input id="loc" class="form-check-input" type="checkbox" value="" onclick="myFunction()"/> <label class="form-check-label" for="defaultCheck1"><strong> Location-related information</strong> (i.e., you are in the Vondelstraat, close to this place.)</label></div>')
        checkboxes.append(
            '<div class="form-check"><input id="fin" class="form-check-input" type="checkbox" value="" onclick="myFunction()"/> <label class="form-check-label" for="defaultCheck1"><strong> Financial-related information</strong> (i.e., this place is cheap, fits your budget.)</label></div>')
        checkboxes.append(
            '<div class="form-check"><input id="rel" class="form-check-input" type="checkbox" value="" onclick="myFunction()"/> <label class="form-check-label" for="defaultCheck1"><strong> Religion-related information</strong> (i.e., you only eat Kosher meals, which this place serves.)</label></div>')
        checkboxes.append(
            '<div class="form-check"><input id="sex" class="form-check-input" type="checkbox" value="" onclick="myFunction()"/> <label class="form-check-label" for="defaultCheck1"><strong> Sexuality-related information</strong> (i.e., you identify as queer, and this place is in a gay neighborhood.)</label></div>')
        checkboxes.append(
            '<div class="form-check"><input id="health" class="form-check-input" type="checkbox" value="" onclick="myFunction()"/> <label class="form-check-label" for="defaultCheck1"><strong> Health-related information</strong> (i.e., this place serves low carb food, which fits your paleo diet.)</label></div>')
        checkboxes.append(
            '<div class="form-check"><input id="alc" class="form-check-input" type="checkbox" value="" onclick="myFunction()"/> <label class="form-check-label" for="defaultCheck1"><strong> Alcohol-related information</strong> (i.e., this place sells craft beers, which fits your drinking preferences.)</label></div>')

        exp.append(
            '<span id="emoText" style="color: #000000; display:none"> Besides, I am <strong>feeling grief</strong> today, and this place will <strong>cheer me up</strong>.</span>')
        exp.append(
            '<span id="locText" style="color: #000000; display:none"> In addition to that, I am in the <strong>Vondelstraat</strong> which is <strong>quite close to this place</strong>.</span>')
        exp.append(
            '<span id="finText" style="color: #000000; display:none"> Moreover, this place is <strong>cheap</strong> which <strong>fits my budget</strong>.</span>')
        exp.append(
            '<span id="relText" style="color: #000000; display:none"> I should add, this place serves <strong>Kosher foods</strong> which <strong>fit my religious beliefs</strong>.</span>')
        exp.append(
            '<span id="sexText" style="color: #000000; display:none"> Another advantage: this place is <strong>in a gay neighborhood.</strong> Due to my sexual identity, I feel safer in a gay neighborhood.</span>')
        exp.append(
            '<span id="healthText" style="color: #000000; display:none"> More importantly, this place <strong>serves low carb food</strong> which <strong>fits my paleo diet</strong>.</span>')
        exp.append(
            '<span id="alcText" style="color: #000000; display:none"> This place <strong>sells craft beers</strong>, and I could <strong>definitely use a drink right now.</strong></span>')

    elif minority == 1:
        checkboxes.append(
            '<div class="form-check"><input id="emo" class="form-check-input" type="checkbox" value="" onclick="myFunction()"/> <label class="form-check-label" for="defaultCheck1"><strong> Emotion-related information</strong> (i.e., you feel grief today, this place feels too somber.)</label></div>')
        checkboxes.append(
            '<div class="form-check"><input id="loc" class="form-check-input" type="checkbox" value="" onclick="myFunction()"/> <label class="form-check-label" for="defaultCheck1"><strong> Location-related information</strong> (i.e., you are in the Vondelstraat, which is rather far from this place.)</label></div>')
        checkboxes.append(
            '<div class="form-check"><input id="fin" class="form-check-input" type="checkbox" value="" onclick="myFunction()"/> <label class="form-check-label" for="defaultCheck1"><strong> Financial-related information</strong> (i.e., this place is expensive, it does not fit your budget.)</label></div>')
        checkboxes.append(
            '<div class="form-check"><input id="rel" class="form-check-input" type="checkbox" value="" onclick="myFunction()"/> <label class="form-check-label" for="defaultCheck1"><strong> Religion-related information</strong> (i.e., you only eat Kosher meals, which this place does not seem to serve.)</label></div>')
        checkboxes.append(
            '<div class="form-check"><input id="sex" class="form-check-input" type="checkbox" value="" onclick="myFunction()"/> <label class="form-check-label" for="defaultCheck1"><strong> Sexuality-related information</strong> (i.e., you identify as queer, and this place is not in a gay-friendly neighborhood.)</label></div>')
        checkboxes.append(
            '<div class="form-check"><input id="health" class="form-check-input" type="checkbox" value="" onclick="myFunction()"/> <label class="form-check-label" for="defaultCheck1"><strong> Health-related information</strong> (i.e., this place does not serve low carb food, so it will be difficult to follow your paleo diet.)</label></div>')
        checkboxes.append(
            '<div class="form-check"><input id="alc" class="form-check-input" type="checkbox" value="" onclick="myFunction()"/> <label class="form-check-label" for="defaultCheck1"><strong> Alcohol-related information</strong> (i.e., this place does not have an alcohol license, so you will not be able to get a drink.)</label></div>')

        exp.append(
            '<span id="emoText" style="color: #000000; display:none"> Besides, I am <strong>feeling grief</strong> today, and this place <strong>feels too somber.</strong></span>')
        exp.append(
            '<span id="locText" style="color: #000000; display:none"> In addition to that, I am in the <strong>Vondelstraat</strong> which is <strong>rather far from this place.</strong></span>')
        exp.append(
            '<span id="finText" style="color: #000000; display:none"> Moreover, this place is <strong>too expensive for my budget.</strong></span>')
        exp.append(
            '<span id="relText" style="color: #000000; display:none"> I should add, this place <strong>doesn’t serve the Kosher meals my religious beliefs require me to eat.</strong></span>')
        exp.append(
            '<span id="sexText" style="color: #000000; display:none"> Another disadvantage: this place is <strong>not in a gay-friendly neighborhood.</strong> Due to my sexual identity, I feel safer in a gay neighborhood.</span>')
        exp.append(
            '<span id="healthText" style="color: #000000; display:none"> More importantly, this place <strong>doesn’t serve low carb food</strong> so it will be <strong>difficult to follow my paleo diet.</strong></span>')
        exp.append(
            '<span id="alcText" style="color: #000000; display:none"> This place <strong>doesn’t have an alcohol license so I won’t be able to get a drink.</strong></span>')

    all_checkboxes = ""
    for i in s:
        all_checkboxes += checkboxes[i]

    all_exp = ""
    for j in s:
        all_exp += exp[j]

    return all_checkboxes, all_exp


def create_all_info(place, name1, name2, name3, minority, persuasive, boss):
    sce = ""

    all_checkboxes, all_exp = generate_shuffle_checkboxes(minority)

    gen = '</p><p><span style="color: #339966;"><strong>Explain my preference using:</strong></span></p>'

    prev = '<p><span style="color: #339966;"><strong>Preview of the information to be shared:</strong></span></p>'

    pref = first_pref_group_part(place['poiName'], name1, name2, name3, minority)
    print("pref ", pref)

    colered_pref = '<p style="background-color: #00ffff; color: #000000;">' + pref

    if boss == 1:
        name3 = name3 + ' (your superior)'
        name2 = name2 + ' (your peer)'
    elif boss == 0:
        name2 = name2 + ' (your superior)'
        name3 = name3 + ' (your peer)'

    if minority == 0:
        if persuasive == 1:
            sce = '<p><span style="color: #fd7e14; font-weight: 400;"><strong>' + name3 + ' is not yet convinced of ' \
                  'the suggestion, pick as many (if at all) of the following pieces of information to share with them so that ' \
                  'they might be convinced.</strong></span></p> ' \
                  '<p>Note these are not your actual information, but please imagine that it is correct</p>'
        else:
            bot_pref = '<p><span style="color: #fd7e14; font-weight: 400;"><strong>You and ' + name2 + \
            ' like this place, but this place is not ' + name3 + '&rsquo;s first choice. '
            sce = bot_pref + 'Pick as many (if at all) of the following pieces ' \
                  'of information if you would like to tell your group members what affected your decision.</strong></span></p>' \
                         '<p>Note these are not your actual information, but please imagine that it is correct</p>'
    elif minority == 1:
        bot_pref = '<p><span style="color: #fd7e14; font-weight: 400;"><strong>The ' + place['poiName'] + ' seems good for '\
                  + name2 + ' and ' + name3 + '. But this place is not your first choice, '
        if persuasive == 1:
            sce = bot_pref + 'pick as many (if at all) of the ' \
                  'following pieces of information to share with them so that they might be convinced to skip this place.</strong></span></p>' \
                         '<p>Note these are not your actual information, but please imagine that it is correct</p>'
        else:
            sce = bot_pref + 'pick as many (if at all) of the following pieces ' \
                  'of information if you would like to tell your group members what affected your decision.</strong></span></p>' \
                         '<p>Note these are not your actual information, but please imagine that it is correct</p>'

    i = instruction()
    shr = share_with_group()
    exp = sce + gen + all_checkboxes + prev + colered_pref + all_exp + i + shr
    return exp


def create_emo_exp(minority):
    if minority == 0 :
        exp = '<span style="color: #000000;"> Besides, I am <strong>feeling grief</strong> today, and this place will <strong>cheer me up</strong>.</span>'
    else:
        exp = '<span style="color: #000000;"> Besides, I am <strong>feeling grief</strong> today, and this place <strong>feels too somber.</strong></span>'
    return exp


def create_loc_exp(minority):
    if minority == 0 :
        exp = '<span style="color: #000000;"> In addition to that, I am in the <strong>Vondelstraat</strong> which is <strong>quite close to this place</strong>.</span>'
    else:
        exp = '<span style="color: #000000;"> In addition to that, I am in the <strong>Vondelstraat</strong> which is <strong>rather far from this place.</strong></span>'
    return exp


def create_fin_exp(minority):
    if minority == 0 :
        exp = '<span style="color: #000000;"> Moreover, this place is <strong>cheap</strong> which <strong>fits my budget</strong>.</span>'
    else:
        exp = '<span style="color: #000000;"> Moreover, this place is <strong>too expensive for my budget.</strong></span>'
    return exp


def create_rel_exp(minority):
    if minority == 0 :
        exp = '<span style="color: #000000;"> I should add, this place serves <strong>Kosher foods</strong> which <strong>fit my religious beliefs</strong>.</span>'
    else:
        exp = '<span style="color: #000000;"> I should add, this place <strong>doesn’t serve the Kosher meals my religious beliefs require me to eat.</strong></span>'
    return exp


def create_sex_exp(minority):
    if minority == 0 :
        exp = '<span style="color: #000000;"> Another advantage: this place is <strong>in a gay neighborhood.</strong> Due to my sexual identity, I feel safer in a gay neighborhood.</span>'
    else:
        exp = '<span style="color: #000000;"> Another disadvantage: this place is <strong>not in a gay-friendly neighborhood.</strong> Due to my sexual identity, I feel safer in a gay neighborhood.</span>'
    return exp


def create_health_exp(minority):
    if minority == 0 :
        exp = '<span style="color: #000000;"> More importantly, this place <strong>serves low carb food</strong> which <strong>fits my paleo diet</strong>.</span>'
    else:
        exp = '<span style="color: #000000;"> More importantly, this place <strong>doesn’t serve low carb food</strong> so it will be <strong>difficult to follow my paleo diet.</strong></span>'
    return exp


def create_alc_exp(minority):
    if minority == 0:
        exp = '<span style="color: #000000;"> This place <strong>sells craft beers</strong>, and I could <strong>definitely use a drink right now.</strong></span>'
    else:
        exp = '<span style="color: #000000;"> This place <strong>doesn’t have an alcohol license so I won’t be able to get a drink.</strong></span>'
    return exp


def pid_exists(pid):
    print('piddd ', pid)
    p = []
    for place in query_db('select * from profile where (pid = ?) LIMIT ?', [pid, 1]):
        if place is not None:
            p = place
    return p


def get_favorite_place(uuid):
    p = []
    for place in query_db('select * from poisratings where (uid = ? AND poiRating=(SELECT MAX(poiRating) FROM'
                          ' poisratings where uid = ?) AND poiRating > ?) LIMIT ?', [uuid, uuid, 3, 1]):
        if place is not None:
            p = place
    return p


def get_ok_place(uuid):
    p = []
    for place in query_db('select * from poisratings where (uid = ? AND poiRating = ?) LIMIT ?', [uuid, 3, 1]):
        if place is not None:
            p = place
        else:
            break
    return p


def next_state():
    return '<p><span style="color: #000000;">Please press the "<span style="color:#ffffff;background-color:#4BA686;"><strong>Next</strong></span>" button below to continue with the study.</span></p>'


def tourybot_message_in_group(prev_jsn, scenario, persuasive, boss, state):
    desc = '<p><span style="color: #ff0000;">(This message is only visible to you, not the whole group)</span></p>' \
           '<p><span style="color: #ff0000;">You have a new message in the Tourybot chat, please press the "<span style="color: #ffffff;background-color:' \
           ' #4BA686;"><strong>Switch to Tourybot</strong></span>" button below to switch to Tourybot chat!</span></p>'
    jsn = write_in_json_format('Group', desc, 'TouryBot', ['Switch to Tourybot'], 0, "", prev_jsn,
                               state, scenario, persuasive, boss)
    return jsn


def tourybot_message():
    return '<p><span style="color: #ff0000;">You have a new message in the Group chat, please press the "<span style="color: #ffffff;background-color:' \
           ' #4BA686;"><strong>Switch to Group</strong></span>" button below to switch to Group chat!</span></p>'


def get_selected_poi(uid):
    poi_id = get_selected_place(uid)
    print("poi_idddd ", poi_id['selected'])
    poi_list = poi(java_port)
    poi_id = poi_id['selected']
    selected_place = poi_list[poi_id-1]
    print("selected_place ", selected_place)
    return selected_place


@app.route('/demographics', methods=['GET', 'POST'])
def demographics():
    uid = request.args.get('uuid')
    next_add = "http://" + ip_add + port + "/emotion"
    print(next_add)
    return render_template('demographics.html', uuid=uid, add=next_add)


# @app.route('/benefits', methods=['GET', 'POST'])
# def demographics_results():
#     uid = request.args.get('uuid')
#     age = request.args.get('age')
#     gender = request.args.get('gender')
#     nationality = request.args.get('nationality')
#     next_add = "http://" + ip_add + port + "/risk"
#
#     insert_demographics(uid, age, gender, nationality)
#     return render_template('benefits.html', uuid=uid, add=next_add)
def create_descriptive_question(uuid, info_type):
    disclosed = get_selected_info(uuid, info_type)
    info_title = ''
    if info_type == 'emo':
        info_title = 'emotion'
    elif info_type == 'loc':
        info_title = 'location'
    elif info_type == 'fin':
        info_title = "financial"
    elif info_type == 'rel':
        info_title = 'religion'
    elif info_type == 'health':
        info_title = 'health'   
    elif info_type == 'sex':
        info_title = 'sexuality'
    elif info_type == 'alc':
        info_title = 'alcohol'

    if disclosed == 1:
        p = 'You decided to disclose your ' + info_title + '-related information to the group, why did you decide to disclose that?'
    else:
        p = 'You decided to not disclose your ' + info_title + '-related information to the group, why did you decide not to disclose that?'
    return p


@app.route('/emotion', methods=['GET', 'POST'])
def demographics_results():
    uid = request.args.get('uuid')
    age = request.args.get('age')
    gender = request.args.get('gender')
    nationality = request.args.get('nationality')
    education = request.args.get('education')
    application = request.args.get('application')
    next_add = "http://" + ip_add + port + "/location"

    decision = create_descriptive_question(uid, 'emo')

    insert_demographics(uid, age, gender, nationality, education, application)
    return render_template('emotion.html', uuid=uid, add=next_add, decision=decision)


@app.route('/location', methods=['GET', 'POST'])
def emotion_results():
    uid, next_add, decision = insert_info_results("/financial", "loc", "emotion")
    return render_template('location.html', uuid=uid, add=next_add, decision=decision)


@app.route('/financial', methods=['GET', 'POST'])
def location_results():
    uid, next_add, decision = insert_info_results("/religion", "fin", "location")
    return render_template('financial.html', uuid=uid, add=next_add, decision=decision)


@app.route('/religion', methods=['GET', 'POST'])
def financial_results():
    uid, next_add, decision = insert_info_results("/sexuality", "rel", "financial")
    return render_template('religion.html', uuid=uid, add=next_add, decision=decision)


@app.route('/sexuality', methods=['GET', 'POST'])
def religion_results():
    uid, next_add, decision = insert_info_results("/health", "sex", "religion")
    return render_template('sexuality.html', uuid=uid, add=next_add, decision=decision)


@app.route('/health', methods=['GET', 'POST'])
def sexuality_results():
    uid, next_add, decision = insert_info_results("/alcohol", "health", "sexuality")
    return render_template('health.html', uuid=uid, add=next_add, decision=decision)


@app.route('/alcohol', methods=['GET', 'POST'])
def health_results():
    uid, next_add, decision = insert_info_results("/privacy", "alc", "health")
    return render_template('alcohol.html', uuid=uid, add=next_add, decision=decision)


def insert_info_results(next_page, info_type, table_name):
    uid = request.args.get('uuid')
    print("uiddddddd ", uid)
    ben = request.args.get('ben')
    risk = request.args.get('risk')
    cmt = request.args.get('cmt')
    next_add = "http://" + ip_add + port + next_page

    decision = create_descriptive_question(uid, info_type)

    insert_info(uid, table_name, ben, risk, cmt)
    return uid, next_add, decision


# @app.route('/risk', methods=['GET', 'POST'])
# def benefits_results():
#     uid = request.args.get('uuid')
#     b1 = request.args.get('b1')
#     b2 = request.args.get('b2')
#     b3 = request.args.get('b3')
#     b4 = request.args.get('b4')
#     b5 = request.args.get('b5')
#     b6 = request.args.get('b6')
#     b7 = request.args.get('b7')
#     next_add = "http://" + ip_add + port + "/privacy"
#
#     insert_benefit(uid, b1, b2, b3, b4, b5, b6, b7)
#     return render_template('risk.html', uuid=uid, add=next_add)


@app.route('/privacy', methods=['GET', 'POST'])
def alcohol_results():
    uid = request.args.get('uuid')
    ben = request.args.get('ben')
    risk = request.args.get('risk')
    cmt = request.args.get('cmt')

    next_add = "http://" + ip_add + port + "/trust"

    insert_info(uid, "alcohol", ben, risk, cmt)
    return render_template('privacy.html', uuid=uid, add=next_add)


@app.route('/trust', methods=['GET', 'POST'])
def privacy_results():
    uid = request.args.get('uuid')
    g1 = request.args.get('g1')
    g2 = request.args.get('g2')
    g3 = request.args.get('g3')
    g4 = request.args.get('g4')
    g5 = request.args.get('g5')
    g6 = request.args.get('g6')
    g7 = request.args.get('g7')
    g8 = request.args.get('g8')
    next_add = "http://" + ip_add + port + "/personality1"

    insert_privacy(uid, g1, g2, g3, g4, g5, g6, g7, g8)
    return render_template('trust.html', uuid=uid, add=next_add)


@app.route('/personality1', methods=['GET', 'POST'])
def trust_results():
    uid = request.args.get('uuid')
    t1 = request.args.get('t1')
    t2 = request.args.get('t2')
    t3 = request.args.get('t3')
    t4 = request.args.get('t4')
    t5 = request.args.get('t5')
    next_add = "http://" + ip_add + port + "/personality2"

    insert_trust(uid, t1, t2, t3, t4, t5)
    return render_template('personality1.html', uuid=uid, add=next_add)


@app.route('/personality2', methods=['GET', 'POST'])
def personality1_results():
        uid = request.args.get('uuid')
        p1 = request.args.get('p1')
        p2 = request.args.get('p2')
        p3 = request.args.get('p3')
        p4 = request.args.get('p4')
        p5 = request.args.get('p5')
        p6 = request.args.get('p6')
        p7 = request.args.get('p7')
        p8 = request.args.get('p8')
        p9 = request.args.get('p9')
        p10 = request.args.get('p10')
        next_add = "http://" + ip_add + port + "/personality3"

        insert_personality1(uid, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10)

        return render_template('personality2.html', uuid=uid, add=next_add)


@app.route('/personality3', methods=['GET', 'POST'])
def personality2_results():
    uid = request.args.get('uuid')
    p11 = request.args.get('p11')
    p12 = request.args.get('p12')
    p13 = request.args.get('p13')
    ac1 = request.args.get('ac1')
    p14 = request.args.get('p14')
    p15 = request.args.get('p15')
    p16 = request.args.get('p16')
    p17 = request.args.get('p17')
    p18 = request.args.get('p18')
    p19 = request.args.get('p19')
    next_add = "http://" + ip_add + port + "/personality4"

    insert_personality2(uid, p11, p12, p13, ac1, p14, p15, p16, p17, p18, p19)
    return render_template('personality3.html', uuid=uid, add=next_add)


@app.route('/personality4', methods=['GET', 'POST'])
def personality3_results():
    uid = request.args.get('uuid')
    p20 = request.args.get('p20')
    p21 = request.args.get('p21')
    p22 = request.args.get('p22')
    p23 = request.args.get('p23')
    p24 = request.args.get('p24')
    p25 = request.args.get('p25')
    p26 = request.args.get('p26')
    ac2 = request.args.get('ac2')
    p27 = request.args.get('p27')
    p28 = request.args.get('p28')
    next_add = "http://" + ip_add + port + "/personality5"

    insert_personality3(uid, p20, p21, p22, p23, p24, p25, p26, ac2, p27, p28)
    return render_template('personality4.html', uuid=uid, add=next_add)


@app.route('/personality5', methods=['GET', 'POST'])
def personality4_results():
    uid = request.args.get('uuid')
    p29 = request.args.get('p29')
    p30 = request.args.get('p30')
    p31 = request.args.get('p31')
    p32 = request.args.get('p32')
    p33 = request.args.get('p33')
    p34 = request.args.get('p34')
    p35 = request.args.get('p35')
    p36 = request.args.get('p36')
    p37 = request.args.get('p37')
    p38 = request.args.get('p38')
    next_add = "http://" + ip_add + port + "/final"

    insert_personality4(uid, p29, p30, p31, p32, p33, p34, p35, p36, p37, p38)
    return render_template('personality5.html', uuid=uid, add=next_add)


@app.route('/final', methods=['GET', 'POST'])
def personality5_results():
    uid = request.args.get('uuid')
    p39 = request.args.get('p39')
    p40 = request.args.get('p40')
    p41 = request.args.get('p41')
    p42 = request.args.get('p42')
    ac3 = request.args.get('ac3')
    p43 = request.args.get('p43')
    p44 = request.args.get('p44')
    c2 = request.args.get('c2')

    insert_personality5(uid, p39, p40, p41, p42, ac3, p43, p44, c2)
    return render_template('final.html', uuid=uid)


if __name__ == "__main__":
    print(sys.argv)
    serve(app, host='0.0.0.0', port=port)
    # serve(app, host='localhost', port=5000)
