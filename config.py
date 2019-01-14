# coding:utf-8
import os


parent = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
LTP_DATA_DIR = parent + '/ltp_data'

log_info_path = parent + '/log/info/'
if not os.path.exists(log_info_path):
    os.makedirs(log_info_path)
log_err_path = parent + '/log/err/'
if not os.path.exists(log_err_path):
        os.makedirs(log_err_path)
info_file = log_info_path + 'info_log.txt'
err_file = log_err_path + 'err_log.txt'

data = parent+'/data/'
Questioning_path = data+'Questioning_HZRQ.txt'
new_word_path = data+'new_word.txt'
dic_path = data+'dic.txt'
stopword_path = data+'stopword.txt'

fr = data+'question_HZRQ.xlsx'
fo = data+'result.xlsx'
