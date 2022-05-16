import pymysql.cursors
import re
import string

# 输入一个长度大于 500 的字符串
def spilit_by_len(str, length):
    if(len(str) <= length):
        return
    textArr = re.findall(r'.{500}', str)
    textArr.append(str[(len(textArr) * length):])
    return textArr


def slide_split(str, max_length):
    if (len(str) <= max_length):
        return
    results = []
    stop_list = ['!', '。', '！', '；', ';', '?', '？', ',']
    begin = 0
    end = max_length
    while(begin < len(str)):
        i = end
        while i > begin + 200 and str[i - 1] not in stop_list:
            i -= 1
        if(i <= begin + 200):
            while i > begin and str[i - 1] not in stop_list and str not in string.punctuation:
                i -= 1
        if(i <= begin):
            results.append(str[begin : end])
            begin = end
            end = min(begin + max_length, len(str))
        else:
            results.append(str[begin : i])
            begin = i
            end = min(begin + max_length, len(str))
    return results


def list_slide_split(strlist, max_len):
    print("list split")
    i = 0
    while i < len(strlist):
        if len(strlist[i]) > max_len:
            arr = slide_split(strlist[i], max_len)
            strlist = strlist[: i] + arr + strlist[i + 1 :]
            i = i + len(arr)
        else:
            i += 1
    return strlist


def check_prefix(results):
    # 统计第一个字符 列表
    pre1 = []
    # 统计第一个字符 字典
    pre1_dict = {}
    pre2 = {}
    pre2_sum = {}
    pre2_spec = {}
    pre5 = {}
    for re in results:
        if(re['signory_item'] is not None and len(re['signory_item']) > 0 ):
            #去除空格
            # re['signory_item'] = re['signory_item'].replace(" ", "")
            cur_char = re['signory_item'][0]
            pre1.append(re['signory_item'][0])
            if cur_char not in pre1_dict:
                pre1_dict[cur_char] = 0
            pre1_dict[cur_char] += 1
        if (re['signory_item'] is not None and len(re['signory_item']) > 2):
            cur_pre2 = re['signory_item'][0:2]
            pre2[re['id']] = cur_pre2
            #输入spec
            if(cur_pre2 == '[权' and len(re['signory_item']) > 500):
                pre2_spec[re['id']] = cur_pre2
            if cur_pre2 not in pre2_sum:
                pre2_sum[cur_pre2] = 0
            pre2_sum[cur_pre2] += 1
        if(re['signory_item'] is not None and len(re['signory_item']) > 8 and re['signory_item'][0] == '[' ):
            cur_pre5 = re['signory_item'][0:8]
            pre5[re['id']] = cur_pre5
    pre2_sum = {k:v for k, v in pre2_sum.items() if v > 20}
    s = set(pre1)
    # print(results)


# return signory_list
def longtext_split(ori, max_len):
    signory_dict = {}
    multi_sig_dict= {}
    sig_dict = {}
    for item in ori:
        if (item['signory_item'] is not None and len(item['signory_item']) > 0):
            # 去空格
            item['signory_item'] = item['signory_item'].replace(" ", "")
            # 去
            item['signory_item'] = re.sub("<imgfile=.*\/>", "", item['signory_item'])
            # 去“权利要求书”
            if(item['signory_item'][0:5] == "权利要求书"):
                item['signory_item'] = item['signory_item'][5:]
            signory_list = []
            # 按序号分割
            if(item['signory_item'][0:2] == '1.'):
                signory_list = list(filter(None, re.split("\d+\.(?!\d)", item['signory_item'])))
            elif(item['signory_item'][0:2] == '1．'):
                signory_list = list(filter(None, re.split("\d+．(?!\d)", item['signory_item'])))
            elif (item['signory_item'][0:2] == '1、'):
                # signory_list = list(filter(None, re.split("\d+、(?!\d)", item['signory_item'])))
                signory_list = [item['signory_item'][2:]]
            elif (item['signory_item'][0:2] == '[权'):
                signory_list = list(filter(None, re.split("\[权利要求\d+\]", item['signory_item'])))
            else:
                signory_list = [item['signory_item']]
            # 长度大于max_length的按长度分割
            signory_list = list_slide_split(signory_list, max_len)
            sig_dict[item['id']] = signory_list
            if(len(signory_list) > 1):
                multi_sig_dict[item['id']] = signory_list
            signory_dict[item['id']] = signory_list
    check_prefix(ori)
    return sig_dict

def insert_signory(sig_dict):
    connection = pymysql.connect(host='10.1.0.177',
                                 user='root',
                                 password='root',
                                 database='patent',
                                 cursorclass=pymysql.cursors.DictCursor)
    values = []
    for patent_id in sig_dict:
        for sig in sig_dict[patent_id]:
            values.append((patent_id, sig))
    with connection:
        with connection.cursor() as cursor:
                    # Create a new record
                    sql = "INSERT INTO `signory_seg` (`patent_id`, `signory_seg`) VALUES (%s, %s)"
                    try:
                        cursor.executemany(sql, values)
                        connection.commit()
                    except:
                        connection.rollback()

if __name__ == '__main__':
    # Connect to the database
    connection = pymysql.connect(host='10.1.0.177',
                                 user='bwj',
                                 password='bwj',
                                 database='patent',
                                 cursorclass=pymysql.cursors.DictCursor)

    results = []

    with connection:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT  `id`, `signory_item` FROM `patent`"
            cursor.execute(sql)
            results = cursor.fetchall()
    sig_dict = longtext_split(results, 500)
    # check_prefix(results)
    insert_signory(sig_dict)
