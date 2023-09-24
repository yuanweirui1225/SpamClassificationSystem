from flask import Flask, render_template, request, redirect,session,url_for
import os,re,jieba,numpy as np
import datetime
import db
app = Flask(__name__)
app.config['DEBUG']=True
app.secret_key = "sdkfjlqjlo2wdad"
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'post'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']
        if not (email and password):
            raise ValueError
    except:
        return render_template('login.html')
    sql1 = "select * from user;"
    all_row=db.select(sql1)
    session['login']=0 #1代表成功 2代表数据库中有email但是密码错误 3数据库中无此email直接注册
    for row in all_row:
        session['login'] = 3
        if row[1]==email:
            if row[2] ==password:
                session['login']=1
                break
            else:
                session['login']=2
                break
    if session['login']==2:
        return render_template('login.html')
    sql3 = "select * from email;"
    all_row3 = db.select(sql3)
    session['all_row3']=all_row3
    session['email']=email
    temp_list=[]
    sql4 = "select * from email;"
    all_row4 = db.select(sql4)
    # for i in all_row4:
    #     temp_list.append(list(i))
    # emaillist=[]
    # for i in range(len(temp_list)):
    #     if temp_list[i][5]==session['email']:
    #         emaillist.append(temp_list[i])
    # for i in range(len(emaillist)):
    #     time = emaillist[i][6][-18:]
    #     emaillist[i].append(time)
    # for i in range(len(emaillist)):
    #     with open(emaillist[i][6], "r",encoding="utf-8") as f:  # 打开文件
    #         data = f.read()  # 读取文件
    #         emaillist[i].append(data[:50])
    # for i in range(len(emaillist)):
    #     emaillist[i][0]=i+1
    temp_list = [list(i) for i in all_row4]
    emaillist = [row for row in temp_list if row[5] == session['email']]

    for i, row in enumerate(emaillist, start=1):
        time = row[6][-18:]
        row.append(time)
        with open(row[6], "r", encoding="utf-8") as f:
            data = f.read()
            row.append(data[:50])
        row[0] = i
    emaildict=[]
    for i in range(len(emaillist)):
        edict = {}
        edict['id']=emaillist[i][0]
        edict['title']=emaillist[i][1]
        edict['exemail']=emaillist[i][3]
        edict['imemail']=emaillist[i][5]
        edict['address']=emaillist[i][7]
        edict['text']=emaillist[i][8]
        emaildict.append(edict)
    if session['login'] == 1:
        return render_template('user.html', email=session['email'], all_row=session['all_row3'],emaildict=emaildict)
    elif session['login'] == 3:
        sql2 = "insert into user (email,password) \
                           values (%s,%s);"
        db.insert(sql2, (email, password))
        return render_template('user.html', email=session['email'],all_row=session['all_row3'],emaildict=emaildict)

@app.route('/sendemail/<email>', methods=['GET', 'post'])
def sendemail(email):
    if email==session['email']:
        return render_template('sendemail.html', email=session['email'])
    else:
        return render_template('login.html')

@app.route('/user/<email>', methods=['GET', 'post'])
def user(email):
    if email == session['email']:
        temp_list = []
        sql4 = "select * from email;"
        all_row4 = db.select(sql4)
        temp_list = [list(i) for i in all_row4]
        emaillist = [row for row in temp_list if row[5] == session['email']]

        for i, row in enumerate(emaillist, start=1):
            time = row[6][-18:]
            row.append(time)
            with open(row[6], "r", encoding="utf-8") as f:
                data = f.read()
                row.append(data[:50])
            row[0] = i
        emaildict = []
        for i in range(len(emaillist)):
            edict = {}
            edict['id'] = emaillist[i][0]
            edict['title'] = emaillist[i][1]
            edict['exemail'] = emaillist[i][3]
            edict['imemail'] = emaillist[i][5]
            edict['address'] = emaillist[i][7]
            edict['text'] = emaillist[i][8]
            emaildict.append(edict)
        return render_template('user.html', email=session['email'],all_row=session['all_row3'],emaildict=emaildict)
    else:
        return render_template('login.html')

@app.route('/sending/<email>', methods=['GET', 'post'])
def sending(email):
    if email == session['email']:
        import_email = request.form['Recipientemail']
        title = request.form['title']
        Message = request.form['Message']
        export_email = email
        sql1 = "select * from user;"
        all_row1 = db.select(sql1)
        for row in all_row1:
            if row[1]==import_email:
                import_email_id=row[0]
            if row[1] == export_email:
                export_email_id = row[0]
        current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        filename='.//text/' +current_time+'.txt'
        file = open(filename, "w",encoding="utf-8")
        file.write("{}\n".format(title))
        file.write("{}\n".format(Message))
        file.close()
        email_address=filename
        sql2 = "insert into email (title,export_email_id,export_email,import_email_id,import_email,email_address) \
                                   values (%s,%s,%s,%s,%s,%s);"
        db.insert(sql2, (title,export_email_id,export_email,import_email_id,import_email,email_address))
        urll = url_for('user',email=email)
        return redirect(urll)
    else:
        return render_template('login.html')

@app.route('/user/showemail/<email>/<address>')
def showemail(email, address):
    if email == session['email']:
        filepath = 'D:/项目/人工智能实训/text/' + address
        # print(filepath)
        os.startfile(filepath)
        urll = url_for('user', email=email)
        return redirect(urll)
    else:
        return render_template('login.html')
#标记垃圾邮件
EmailsIndex="./full/index"  #标记文件（读取数据路径的文件）
def filterEmail(email):  # 正则表达式过滤所有非中文词语
    email = re.sub("[a-zA-Z0-9_]+|\W", "", email)
    return email
def readEmail(filename):  # 根据路径读取邮件
    if '.txt' in filename:
        with  open(filename, "r", encoding="utf-8") as fp:
            content = fp.read()  # 读取邮件
            content = filterEmail(content)  # 根据正则表达式去掉非中文字符
            words = set(jieba.cut(content))  # 用jieba中文分词库把连续中文字符分成单词\
    else:
        with  open(filename, "r", encoding='GB2312', errors='ignore') as fp:
            content = fp.read()  # 读取邮件
            content = filterEmail(content)  # 根据正则表达式去掉非中文字符
            words = set(jieba.cut(content))  # 用jieba中文分词库把连续中文字符分成单词\
    return words
def loadAllEmails(IndexFile):  # 加载所有邮件
    Emails = []
    with  open(IndexFile, "r",encoding="utf-8") as fp:
        lines = fp.readlines()  # 按行读取
        for line in lines:
            spam, filename = line.split()  # 划分为两部分
            Emails.append((spam, readEmail(filename)))  # 添加到Emails列表中（邮件类型垃圾或正常、各个邮件中文词的列表）
        # if IndexFile=='./full/testindex':
        #     for i in range(len((Emails))):
        #         print('Emails')
        #         print(Emails)
        #         #Emails[i][1]=re.sub(r'\\n','',Emails[i][1])
    return Emails
def calWordsFreqTable(Emails):
    table = dict()  # 用于保存字词各自在正常邮件和垃圾邮件中出现的次数（数据结构为字典  {键：[正常邮件概率，垃圾邮件概率]}    ）
    spamCount = 0  # 垃圾邮件的封数
    hamCount = 0  # 正常邮件的封数

    for email in Emails:  # 遍历邮件列表对于其中的每一封邮件
        flag, words = email  # 把邮件类型和单词列表读取出来
        if flag == 'spam':  # 是垃圾邮件
            spamCount += 1  # 垃圾邮件的封数
            for word in words:  # 遍历单词列表中每个单词
                if word in table:  # 如果单词在table字典中的键中
                    table[word][1] += 1  # 对应单词在垃圾邮件中出现的次数+1
                else:
                    table[word] = [0, 1]  # 单词在table字典中未出现，则置对应单词垃圾邮件次数为1，正常邮件次数为0.
        else:
            hamCount += 1
            for word in words:
                if word in table:
                    table[word][0] += 1
                else:
                    table[word] = [1, 0]
    for word in table:  # 遍历table字典，对于其中的(正常/垃圾)邮件的次数/(正常/垃圾)邮件的封数得到概率。
        table[word][0] = table[word][0] / hamCount
        table[word][1] = table[word][1] / spamCount
    return table  # 返回概率表
def saveTable(table, filename="tablespam.txt"):  # 保存概率表
    with open(filename, "w", encoding='utf8', ) as f:
        lines = []
        for item in sorted(table.items(), key=lambda x: x[1][1], reverse=True):  # 根据垃圾邮件的概率进行降序，得到三个元素相应的值
            string = '{} '.format(item[0])  # {的：[0.975 0.882]} item 是这样的数据类型
            string += '                 '
            string += '{:.3f} '.format(float(item[1][0]))
            string += '                 '
            string += '{:.3f} \n'.format(float(item[1][1]))
            lines.append(string)  # 写成一个字符串保存到lines列表中
        f.writelines(lines)  # 写入文件
def loadTable(filename="tablespam.txt"):  # 加载概率表(把文件读取转换为字典{键：[正常邮件概率，垃圾邮件概率]})
    table = {}
    with open(filename, "r", encoding='utf8', ) as fp:
        lines = fp.readlines()
        for line in lines:
            word, hamRate, spamRate = line.split()
            table[word] = [float(hamRate), float(spamRate)]
    return table
def checkOneEmail(table, emailwords):  # 识别一封新邮件     #table 为概率表 emailwords对应的是单个邮件中的汉语单词的集合
    RateSpam = 0.5
    RateHam = 0.5

    for word in emailwords:  # 比如会出现0的情况，如果邮件很长，概率比较小，浮点数是有上下届
        if word not in table:  # 1.针对没有出现过的词，我们直接跳过这个词不处理
            continue
        if table[word][0] == 0 or table[word][1] == 0:
            continue
        # table[word][0] = 1e-3 if table[word][0] < 1e-3 else table[word][0]

        table[word][0] = max(table[word][0], 1e-4)  # 2.出现0条件概率
        table[word][1] = max(table[word][1], 1e-4)

        RateSpam *= table[word][1]
        RateHam *= table[word][0]
        if RateSpam < 1e-50 or RateHam < 1e-50:  # 3.如果邮件特别长，导致除零错误
            break

    SpamRate = RateSpam / (RateSpam + RateHam)

    if SpamRate > 0.9999:
        return 'spam'
    else:
        return 'ham'
def checkEmails(table, emails):  # 检测多封邮件                   #table 为概率表 #testEmails  所有测试集邮件的数据结构为:  {spam，各个邮件的集合}
    predict_flags = []
    for email in emails:  # testEmails  所有测试集邮件的数据结构为: {spam，各个邮件的集合}
        predict_flag_result = checkOneEmail(table, email[1])  # table 为概率表 email[1]对应的是单个邮件中的汉语单词的集合。
        predict_flags.append(predict_flag_result)
    return predict_flags  # 返回准确率和每一封邮件的预测值

def train_test_split(Emails, testSize):  # 切分数据集,顺序切分
    arrayEmails = np.array(Emails)  # 把邮件列表转换为数组
    test_size = int(len(Emails) * testSize)  # 按比例划分数据集
    shuffle_indexes = np.random.permutation(len(arrayEmails))  # 对邮件数组的序号进行随机排序，得到乱序后的数组序号。
    test_indexs, train_indexs = np.split(shuffle_indexes, [test_size])  # 测试数据序号，训练数据序号根据乱序后的序号和划分比例划分数据集。
    return arrayEmails[train_indexs], arrayEmails[test_indexs]  # 返回训练数据集和测试数据集（根据乱序划分后的序号）
def train(trainEmails):
    table = calWordsFreqTable(trainEmails)  # 根据测试集数据训练得出概率表
    saveTable(table)  # 保存概率表
def test(testEmails):  # testEmails   所有测试集邮件的数据结构为: {spam，各个邮件的集合}
    table = loadTable()  # 加载概率表
    predict_flags = checkEmails(table, testEmails)  # 检测邮件
    return predict_flags
    # print(testEmails)                                      #查看测试邮件类型
    # print(predict_flags)                                   #预测得到的测试邮件类型
#检测垃圾邮件链接
@app.route('/trash/<email>')
def trash(email):
    if email == session['email']:
        temp_list = []
        sql4 = "select * from email;"
        all_row4 = db.select(sql4)
        temp_list = [list(i) for i in all_row4]
        emaillist = [row for row in temp_list if row[5] == session['email']]

        for i, row in enumerate(emaillist, start=1):
            time = row[6][-18:]
            row.append(time)
            with open(row[6], "r", encoding="utf-8") as f:
                data = f.read()
                row.append(data[:50])
            row[0] = i

        #print(emaillist)
        filename = './full/testindex'
        file = open(filename, "w", encoding="utf-8")
        for i in range(len(emaillist)):
            file.write("{} {}\n".format('spam',emaillist[i][6]))
        file.close()
        #检测垃圾邮件
        #trainEmail = loadAllEmails(EmailsIndex)  # 读取邮件内容并分成单词列表（由集合构成） {spam，各个邮件的集合}
        testEmail= loadAllEmails(filename)
        #print('testEmail',testEmail)
        # print(Emails[0])                                      #可以查看列表的第一个元素来判读邮件是否正确
        #trainEmails, testEmails = train_test_split(trainEmail,0)  # 切分数据集,设置为零是因为上面的切分数据集是针对一整个txt,这里用0直接用这里的直接当做训练集，邮件数据都是测试集
        trainEmails1, testEmails1=train_test_split(testEmail,1)
        #train(trainEmails)  # 用训练邮件进行计算，保存概率表
        predict_flags=test(testEmails1)  # 加载概率表模型，对测试邮件进行预测，计算准确率
        # print(predict_flags)
        for i in range(len(emaillist)):
            emaillist[i].append(predict_flags[i])
        trashlist=[]
        for i in range(len(emaillist)):
            if emaillist[i][9] =='spam':
                trashlist.append(emaillist[i])
        for i in range(len(trashlist)):
            trashlist[i][0]=i+1
        emaildict = []
        for i in range(len(trashlist)):
            edict = {}
            edict['id'] = trashlist[i][0]
            edict['title'] = trashlist[i][1]
            edict['exemail'] = trashlist[i][3]
            edict['imemail'] = trashlist[i][5]
            edict['address'] = trashlist[i][7]
            edict['text'] = trashlist[i][8]
            emaildict.append(edict)
        return render_template('trash.html', email=session['email'], all_row=session['all_row3'], emaildict=emaildict)
    else:
        return render_template('login.html')

if __name__ == '__main__':
    trainEmail = loadAllEmails(EmailsIndex)
    trainEmails, testEmails = train_test_split(trainEmail, 0)
    train(trainEmails)  # 用训练邮件进行计算，保存概率表
    app.run(debug=True)