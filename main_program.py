from selenium import webdriver
import time
import json
import random
import os
import gui


def get_path():
    current_path = os.path.abspath(__file__)
    father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    print('present file path : ' + father_path)
    return father_path


def cookie_login(wd, father_path):
    try:
        wd.set_window_size(1200, 913)
        wd.get('https://bw.rsbsyzx.cn/')
        with open(father_path + r'\count.txt', 'r') as cookief:
            # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
            cookies_list = json.load(cookief)
            for cookie in cookies_list:
                wd.add_cookie(cookie)
        wd.refresh()
        time.sleep(5)
        wd.find_element_by_link_text("个人中心")
        print('login successful')
    except:
        choice1 = int(gui.show())
        if choice1 == 1:
            list_cookie = []
            for i, j, k in os.walk(father_path + r'\cookies_data'):
                print(i, j, k)
                list_cookie.append(k)
            choice2 = int(gui.choice(list_cookie[0]))
            with open(father_path + r'\cookies_data\\' + list_cookie[0][choice2], 'r') as cookief:
                # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
                cookies_list = json.load(cookief)
                for cookie in cookies_list:
                    wd.add_cookie(cookie)
            wd.refresh()
            time.sleep(5)
            wd.find_element_by_link_text("个人中心")
            print('login successful')
        elif choice1 == 2:
            zh = []
            mm = []
            file = open(father_path + r'\count_data.txt', 'r', encoding='utf8')
            for i in range(int(line_count(file)/2)):
                temp = file.readline()
                if temp[0] != '#':
                    zh.append(temp)
                    mm.append(file.readline())
            print(zh)
            choice2 = int(gui.choice(zh))
            wd.set_window_size(1200, 913)
            wd.implicitly_wait(5)
            print(zh[choice2])
            print(mm[choice2])
            wd.get('https://bw.rsbsyzx.cn/#/login')
            wd.find_element_by_css_selector("div:nth-child(1) > .iptbox:nth-child(1) .el-input__inner").send_keys(zh[choice2])
            wd.find_element_by_css_selector(".iptbox:nth-child(2) .el-input__inner").send_keys(mm[choice2])
            wd.find_element_by_css_selector(".code .el-input__inner").send_keys(str(gui.input_str()))
            wd.find_element_by_css_selector(".code .el-input__inner").send_keys('\n')
            time.sleep(2)
            wd.refresh()
            with open(father_path + r'\cookies_data\count_'+str(zh[choice2])[0:-1]+'.txt', 'w') as cookief:
                # 将cookies保存为json格式
                cookief.write(json.dumps(wd.get_cookies()))
        wd.implicitly_wait(2)


def check_if_need(wd):
    wd.implicitly_wait(10)
    date = []
    count = []
    done = 0
    y_d = 0
    time_n = list(time.localtime(time.time()))
    wd.get("https://bw.rsbsyzx.cn/")
    wd.find_element_by_link_text("个人中心").click()
    wd.find_element_by_link_text("做题记录").click()
    try:
        for i in range(5):
            date.append(wd.find_element_by_css_selector(".answer_div_g:nth-child("+str(i+1)+") .fl > span").text)
            count.append(wd.find_element_by_css_selector(".answer_div_g:nth-child("+str(i+1)+") span:nth-child(3)").text)
    except:
        pass
    try:
        for i in range(5):
            if int(time_n[0]) == int(date[i][9:13]) and int(time_n[1]) == int(date[i][14:16]) and int(time_n[2]) == int(date[i][17:19]):
                done += 1
                if 1 == int(count[i][3]):
                    y_d += 1
            else:
                break
    except:
        pass
    wd.back()
    wd.back()
    y_d = 2 - y_d
    done = 5 - done
    r_list = (done, y_d)
    print(r_list)
    return r_list


def line_count(data):
    line = 0
    while True:
        temp = list(data.readline())
        if temp == []:
            data.seek(0, 0)
            return line
        line += 1


def search(input_str, data, line_len):
    data.seek(0, 0)
    answer_n = []
    answer = []
    for i in range(line_len):
        seed = data.tell()
        temp = list(data.readline())
        bd_temp = len(temp)
        confirm = 0
        if temp[0] == 'A' or temp[0] == 'B' or temp[0] == 'C' or temp[0] == 'D' or temp[0] == '解' or temp[0] == '答':
            continue
        for j in input_str:
            for k in temp:
                if j == k:
                    confirm += 1
                    temp.remove(k)
                    break
        if len(input_str) >= bd_temp:
            answer_n.append(int(len(input_str) - confirm))
        elif len(input_str) < bd_temp:
            answer_n.append(int(bd_temp - confirm))
        answer.append(seed)
    answer_back = (answer_n, answer)
    data.seek(0, 0)
    return answer_back


def show_answer(answer_temp, data):
    for i in range(10):
        for k in range(len(answer_temp[0])):
            if answer_temp[0][k] == i:
                data.seek(answer_temp[1][k])
                list1 = []
                for a in range(7):
                    list1.append(data.readline())
                return list1


def choice_list_built(answer, choices):
    choice_list = ['', '', '', '']
    for j in range(4):
        for k in answer:
            n = k.find(choices[j])
            m = 2
            if n != -1:
                for o in range(len(k) - 2 - n):
                    if k[m + n] == ' ' or k[m + n] == '\n' or k[m + n] == choices[j + 1]:
                        break
                    choice_list[j] += k[m + n]
                    m += 1
                break
    return choice_list


def format_searching(data):
    if data == '对':
        data = '正确'
    elif data == '错':
        data = '错误'
    return data


def answer_out_built(answer):
    answer_out = ''
    for j in answer:
        n = j.find('答案')
        m = 3
        if n != -1:
            for o in range(len(j) - 2 - n):
                if j[m + n] == ' ' or j[m + n] == '\n' or j[m + n] == '。':
                    break
                answer_out += j[m + n]
                m += 1
            return answer_out


def putin_answers_out_built(answer_out):
    answers_out = []
    temp = ''
    for i in answer_out:
        if i != '；' and i != '、':
            temp += i
        else:
            answers_out.append(temp)
            temp = ''
    answers_out.append(temp)
    return answers_out


def select_question(wd, file, answer_pool_line):
    wd.implicitly_wait(2)
    try:
        question = wd.find_element_by_css_selector('.fl > .f18').text
        temp_a = wd.find_element_by_css_selector(".fl:nth-child(3) dd").text
        temp_b = wd.find_element_by_css_selector(".fl:nth-child(4) dd").text
        temp_c = wd.find_element_by_css_selector(".fl:nth-child(5) dd").text
        temp_d = wd.find_element_by_css_selector(".fl:nth-child(6) dd").text
        choices = ['A', 'B', 'C', 'D', 'A']
        answer = show_answer(search(question, file, answer_pool_line), file)
        choice_list = choice_list_built(answer, choices)
        answer_out = answer_out_built(answer)
        print(answer)
        print(choice_list)
        print([temp_a, temp_b, temp_c, temp_d])
        print(answer_out)
        for j in answer_out:
            for k in range(4):
                if j == choices[k]:
                    if choice_list[k] == temp_a:
                        wd.find_element_by_css_selector(".fl:nth-child(3) dt").click()
                        time.sleep(random.random() * 3)
                    elif choice_list[k] == temp_b:
                        wd.find_element_by_css_selector(".fl:nth-child(4) dt").click()
                        time.sleep(random.random() * 3)
                    elif choice_list[k] == temp_c:
                        wd.find_element_by_css_selector(".fl:nth-child(5) dt").click()
                        time.sleep(random.random() * 3)
                    elif choice_list[k] == temp_d:
                        wd.find_element_by_css_selector(".fl:nth-child(6) dt").click()
                        time.sleep(random.random() * 3)
        wd.find_element_by_link_text("下一题").click()
        time.sleep(random.randint(2, 4) + random.random())
    except:
        t_g = random.randint(1, 4)
        if t_g == 1:
            wd.find_element_by_css_selector(".fl:nth-child(3) dt").click()
            time.sleep(random.random() * 3)
        elif t_g == 2:
            wd.find_element_by_css_selector(".fl:nth-child(4) dt").click()
            time.sleep(random.random() * 3)
        elif t_g == 3:
            wd.find_element_by_css_selector(".fl:nth-child(5) dt").click()
            time.sleep(random.random() * 3)
        elif t_g == 4:
            wd.find_element_by_css_selector(".fl:nth-child(6) dt").click()
            time.sleep(random.random() * 3)
        wd.find_element_by_link_text("下一题").click()
        time.sleep(random.randint(2, 4) + random.random())


def judge_question(wd, file, answer_pool_line):
    wd.implicitly_wait(2)
    try:
        question = wd.find_element_by_css_selector('.fl > .f18').text
        answer = show_answer(search(question, file, answer_pool_line), file)
        answer_out = answer_out_built(answer)
        temp_a = wd.find_element_by_css_selector(".mt20:nth-child(4) > dd").text
        temp_b = wd.find_element_by_css_selector(".mt20:nth-child(5) > dd").text
        temp_a = format_searching(temp_a)
        temp_b = format_searching(temp_b)
        print(answer)
        print(answer_out)
        print([temp_a, temp_b])
        for j in range(2):
            if answer_out == temp_a:
                wd.find_element_by_css_selector(".mt20:nth-child(4) > dt").click()
                time.sleep(random.random() * 3)
            elif answer_out == temp_b:
                wd.find_element_by_css_selector(".mt20:nth-child(5) > dt").click()
                time.sleep(random.random() * 3)
        wd.find_element_by_link_text("下一题").click()
        time.sleep(random.randint(2, 4) + random.random())
    except:
        wd.find_element_by_link_text("下一题").click()
        time.sleep(random.randint(2, 4) + random.random())


def filling_question(wd, file, answer_pool_line):
    wd.implicitly_wait(2)
    try:
        question = wd.find_element_by_css_selector(".fl > .f18").text
        answer = show_answer(search(question, file, answer_pool_line), file)
        answer_out = answer_out_built(answer)
        putin_answers_out = putin_answers_out_built(answer_out)
        print(answer)
        print(answer_out)
        print(putin_answers_out)
        start = 3
        for j in putin_answers_out:
            try:
                wd.find_element_by_css_selector(".fl:nth-child(" + str(start) + ") .el-input__inner").send_keys(j)
                start += 1
                time.sleep(random.randint(2, 4) + random.random())
            except:
                wd.find_element_by_css_selector(".fl:nth-child(" + str(start) + ") .el-input__inner").clear()
                wd.find_element_by_css_selector(".fl:nth-child(" + str(start - 1) + ") .el-input__inner").send_keys(
                    answer_out)
        time.sleep(random.randint(4, 6) + random.random())
        wd.find_element_by_link_text("下一题").click()
    except:
        time.sleep(random.randint(4, 6) + random.random())
        wd.find_element_by_link_text("下一题").click()


def main_program_of_practice(wd, father_path):
    wd.implicitly_wait(10)
    wd.find_element_by_css_selector('li:nth-child(2) > .Clearfix > img').click()
    try:
        wd.implicitly_wait(2)
        wd.find_element_by_link_text("再来一套").click()
    except:
        try:
            wd.find_element_by_link_text("继续答题").click()
        except:
            wd.find_element_by_link_text("开始答题").click()
    wd.implicitly_wait(5)
    wd.find_element_by_css_selector(".fl > .f18")
    for i in range(3):
        file = open(father_path + r'\data\dan_xuan.txt', 'r', encoding='utf8')
        select_question(wd, file, line_count(file))
    for i in range(3):
        file = open(father_path + r'\data\duo_xuan.txt', 'r', encoding='utf8')
        select_question(wd, file, line_count(file))
    for i in range(2):
        file = open(father_path + r'\data\pan_duan.txt', 'r', encoding='utf8')
        judge_question(wd, file, line_count(file))
    for i in range(2):
        file = open(father_path + r'\data\kong.txt', 'r', encoding='utf8')
        filling_question(wd, file, line_count(file))
    wd.implicitly_wait(10)
    wd.find_element_by_css_selector(".el-button > span").click()
    wd.find_element_by_css_selector(".el-button--primary > span").click()
    wd.find_element_by_link_text("确定").click()


def main_program_of_daily(wd):
    wd.implicitly_wait(10)
    wd.find_element_by_css_selector("li > img").click()
    try:
        wd.implicitly_wait(2)
        wd.find_element_by_link_text("继续答题").click()
    except:
        wd.implicitly_wait(2)
        wd.find_element_by_link_text("开始答题").click()
    wd.implicitly_wait(10)
    time.sleep(2 + random.random())
    wd.find_element_by_css_selector(".cursor:nth-child("+str(random.randint(1, 6))+") > a").click()
    time.sleep(2 + random.random())
    window_sum = wd.window_handles
    wd.switch_to.window(window_sum[-1])
    for i in range(15):
        try:
            temp = random.randint(1, 4)
            if temp == 1:
                wd.find_element_by_link_text("A").click()
            elif temp == 2:
                wd.find_element_by_link_text("B").click()
            elif temp == 3:
                wd.find_element_by_link_text("C").click()
            elif temp == 4:
                wd.find_element_by_link_text("D").click()
            time.sleep(2 + random.random())
            try:
                wd.find_element_by_link_text("下一题").click()
            except:
                wd.find_element_by_link_text("重新开始").click()
                wd.find_element_by_css_selector(".el-button--primary").click()
        except:
            wd.find_element_by_link_text("重新开始").click()
            wd.find_element_by_css_selector(".el-button--primary").click()
    wd.find_element_by_link_text("结束学习").click()
    time.sleep(random.random())
    wd.find_element_by_css_selector(".el-button--primary > span").click()
    wd.close()
    window_sum = wd.window_handles
    wd.switch_to.window(window_sum[-1])
    wd.refresh()


def main_program_of_yyb(wd, father_path):
    wd.implicitly_wait(10)
    file = open(father_path + r'\data\yyb.txt', 'r', encoding='utf8')
    answer_pool_line = line_count(file)
    wd.find_element_by_css_selector("li:nth-child(3) > .Clearfix > img").click()
    wd.find_element_by_css_selector(".f16").click()
    # 人机
    wd.find_element_by_css_selector(".imgText:nth-child(2) > .Clearfix").click()
    # 党建理论
    wd.find_element_by_css_selector(".cursor:nth-child(2) > b").click()
    time.sleep(1)
    wd.implicitly_wait(2)
    for i in range(15):
        try:
            try:
                try:
                    question = wd.find_element_by_css_selector(".answerBattleTitle > p").text
                    temp_a = wd.find_element_by_css_selector("li:nth-child(1) > p > p").text
                    temp_b = wd.find_element_by_css_selector("li:nth-child(2) > p > p").text
                    temp_c = wd.find_element_by_css_selector("li:nth-child(3) > p > p").text
                    temp_d = wd.find_element_by_css_selector("li:nth-child(4) > p > p").text
                    print(1)
                except:
                    question = wd.find_element_by_css_selector(".answerBattleTitle").text
                    temp_a = wd.find_element_by_css_selector("li:nth-child(1) > p").text
                    temp_b = wd.find_element_by_css_selector("li:nth-child(2) > p").text
                    temp_c = wd.find_element_by_css_selector("li:nth-child(3) > p").text
                    temp_d = wd.find_element_by_css_selector("li:nth-child(4) > p").text
                    print(2)
                print('xuan ze')
                choices = ['A', 'B', 'C', 'D', 'A']
                answer = show_answer(search(question, file, answer_pool_line), file)
                choice_list = choice_list_built(answer, choices)
                answer_out = answer_out_built(answer)
                print(answer)
                print(choice_list)
                print([temp_a, temp_b, temp_c, temp_d])
                print(answer_out)
                for j in answer_out:
                    for k in range(4):
                        if j == choices[k]:
                            if choice_list[k] == temp_a:
                                wd.find_element_by_css_selector("li:nth-child(1) .answerNumber").click()
                            elif choice_list[k] == temp_b:
                                wd.find_element_by_css_selector("li:nth-child(2) .answerNumber").click()
                            elif choice_list[k] == temp_c:
                                wd.find_element_by_css_selector("li:nth-child(3) .answerNumber").click()
                            elif choice_list[k] == temp_d:
                                wd.find_element_by_css_selector("li:nth-child(4) .answerNumber").click()
                wd.find_element_by_css_selector(".nextAnswerBtn").click()
                time.sleep(2)
            except:
                try:
                    try:
                        question = wd.find_element_by_css_selector(".answerBattleTitle > p").text
                        temp_a = wd.find_element_by_css_selector("li:nth-child(1) > p > p").text
                        temp_b = wd.find_element_by_css_selector("li:nth-child(2) > p > p").text
                        print(1)
                    except:
                        question = wd.find_element_by_css_selector(".answerBattleTitle").text
                        temp_a = wd.find_element_by_css_selector("li:nth-child(1) > p").text
                        temp_b = wd.find_element_by_css_selector("li:nth-child(2) > p").text
                        print(2)
                    print('pan duan')
                    answer = show_answer(search(question, file, answer_pool_line), file)
                    answer_out = answer_out_built(answer)
                    temp_a = format_searching(temp_a)
                    temp_b = format_searching(temp_b)
                    print(answer)
                    print(answer_out)
                    print([temp_a, temp_b])
                    for j in range(2):
                        if answer_out == temp_a:
                            wd.find_element_by_css_selector("li:nth-child(1) .answerNumber").click()
                        elif answer_out == temp_b:
                            wd.find_element_by_css_selector("li:nth-child(2) .answerNumber").click()
                    wd.find_element_by_css_selector(".nextAnswerBtn").click()
                    time.sleep(2)
                except:
                    print('mei sou dao ti mu')
                    wd.find_element_by_css_selector(".nextAnswerBtn").click()
                    time.sleep(2)
        except:
            time.sleep(3)
            wd.find_element_by_link_text("查看对战详情").click()
            break
    file = open(father_path + r'\data\yyb.txt', 'a', encoding='utf8')
    wd.implicitly_wait(5)
    for i in range(15):
        try:
            try:
                my_answer = str(wd.find_element_by_css_selector("li:nth-child(" + str(i+1) + ") .mt5:nth-child(2)").text)
                true_answer = str(wd.find_element_by_css_selector("li:nth-child(" + str(i+1) + ") .mt5:nth-child(1)").text)
                print(i)
                print(my_answer[4:])
                print(true_answer[4:])
                if my_answer[4:] != true_answer[4:]:
                    print(str(i)+'wrong')
                    try:
                        temp = str(str(i) + '.' + wd.find_element_by_css_selector("li:nth-child(" + str(i+1) + ") > .f18 > p").text)
                    except:
                        temp = str(str(i) + '.' + wd.find_element_by_css_selector("li:nth-child(" + str(i + 1) + ") > .f18").text)
                    file.write(temp)
                    print(str(i)+'有题目')
                    file.write('\n')
                    temp = str(wd.find_element_by_css_selector("li:nth-child(" + str(i+1) + ") > .oh:nth-child(3) dd").text)
                    file.write('A．'+temp)
                    file.write('\n')
                    temp = str(wd.find_element_by_css_selector("li:nth-child(" + str(i+1) + ") > .oh:nth-child(4) dd").text)
                    file.write('B．'+temp)
                    file.write('\n')
                    try:
                        temp = str(wd.find_element_by_css_selector("li:nth-child(" + str(i+1) + ") > .oh:nth-child(5) p").text)
                        file.write('C．'+temp)
                        file.write('\n')
                        temp = str(wd.find_element_by_css_selector("li:nth-child(" + str(i+1) + ") > .oh:nth-child(6) p").text)
                        file.write('D．'+temp)
                        file.write('\n')
                        file.write('答案：'+true_answer[7:])
                        print('1答案：'+true_answer[7:])
                        file.write('\n')
                        time.sleep(1)
                    except:
                        temp = str(wd.find_element_by_css_selector("li:nth-child(" + str(i + 1) + ") .mt5:nth-child(1)").text)
                        file.write('答案：' + temp[7:])
                        print('2答案：' + temp[7:])
                        file.write('\n')
                        time.sleep(1)
                else:
                    pass
            except:
                print('no ti mu')
        except:
            pass
    wd.find_element_by_link_text("首页").click()


def main_program():
    father_path = get_path()
    wd = webdriver.Chrome(father_path + '\chromedriver.exe')
    cookie_login(wd, father_path)
    r_list = check_if_need(wd)
    r_time = r_list[1]
    if r_time > 0:
        for i in range(r_list[0]):
            if r_time > 0:
                main_program_of_practice(wd, father_path)
                date = []
                count = []
                y_d = 0
                time_n = list(time.localtime(time.time()))
                try:
                    for j in range(5):
                        date.append(
                            wd.find_element_by_css_selector(".answer_div_g:nth-child(" + str(i + 1) + ") .fl > span").text)
                        count.append(wd.find_element_by_css_selector(
                            ".answer_div_g:nth-child(" + str(i + 1) + ") span:nth-child(3)").text)
                except:
                    pass
                try:
                    for j in range(5):
                        if int(time_n[0]) == int(date[i][9:13]) and int(time_n[1]) == int(date[i][14:16]) and int(
                                time_n[2]) == int(date[i][17:19]):
                            if 1 == int(count[i][3]):
                                y_d += 1
                        else:
                            break
                except:
                    pass
                r_time = 2 - y_d
                print(r_time)
                time.sleep(3)
                wd.implicitly_wait(10)
                wd.find_element_by_link_text("首页").click()
                time.sleep(3)
            else:
                break
    main_program_of_daily(wd)
    '''main_program_of_yyb(wd, father_path)'''


main_program()

