# coding:utf-8
from Semantic_annotation_jieba import semantic_annotation_jieba
import re
from log import logger
from flask import Flask, request, jsonify
import traceback
import json
import argparse
from zmq_client_new.client import BertClient


app = Flask(__name__)


#curl -H "Content-Type:application/json" -X POST --data '{"mask_question":["缴费方式查询"], "dic":{"代扣":"n"}' http://0.0.0.0:20002/predict
@app.route('/predict', methods=['post'])
def mask_question():
    try:
        try:
            temp_data = request.get_data()
            json_data = json.loads(temp_data)
        except Exception as e:
            logger.warning("request failed or request load failed!!!" + traceback.format_exc())
            return jsonify({"state": "request failed or request load failed!!!",
                            'trace': traceback.format_exc()})
        if 'mask_question' not in json_data:
            logger.warning("must input data, mask_question field must be in json_data")
            return jsonify({'state': 'mask_question field must be in json_data'})


        lines = json_data['mask_question']
        if len(lines) == 0:
            return jsonify({'input data must be non-empty!!!'})
        if type(lines) == 'str':
            lines = list(lines)
        elif type(lines) == list:
            lines = lines
        else:
            return jsonify({"format iscorrect": "mask_question field must be str or list"})

        if 'dic' not in json_data:
            dic = {}
        else:
            dic_old = json_data['dic']
            dic = {}
            for key in dic_old.keys():
                value = dic_old[key]
                if value == '':
                    continue
                else:
                    dic[key] = value

        client = BertClient()
        res = []
        try:
            lines = [re.sub('\n', '', line) for line in lines]
            lines = [line for line in lines if len(line)]
            lines_len = len(lines)
            for key in dic.keys():
                lines.append(key + '____' + str(dic[key]))
            tmp_res =client.encode(lines)[:lines_len]

            for tmp in tmp_res:
                tmp_dic = {}
                tagger_and_words = tmp.split('++')
                for tagger_and_word in tagger_and_words:
                    tagger, word = tagger_and_word.split('==>')
                    if word == '__':
                        word = ''
                    tmp_dic[tagger] = word
                res.append(tmp_dic)
            # print(client.encode(lines)[:lines_len])
        except Exception:
            logger.warning("annotation error: ".format(traceback.format_exc()))
            return jsonify({'trace': traceback.format_exc()})
        return jsonify({'state ': 'success',
                        'res ': res})
    except Exception:
        return jsonify({'trace': traceback.format_exc()})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--host", default='0.0.0.0')
    parser.add_argument("-p", "--post", default=20002)
    options = vars(parser.parse_args())
    vocab_bag_dict = {}
    # get_wordvector_dict(os.path.join(path, 'word2vec_vectors300.txt'), vocab_bag_dict)
    app.run(host=options['host'], port=int(options['post']), debug=False)

# if __name__ == '__main__':
#     test_file = '/root/PycharmProjects/Semantic_annotation_Utry/data/test.txt'
#     dict_file = '/root/PycharmProjects/Semantic_annotation_Utry/data/dic.txt'
#     sheet2_name = '专业词'
#     with open(test_file) as f:
#         lines = f.readlines()
#         lines = [re.sub("\n", "", line) for line in lines]
#     dic = {}
#     with open(dict_file) as f:
#         lines = f.readlines()
#         lines = [re.sub('\n', '', line) for line in lines]
#         for s in lines:
#             if len(s) == 2 and s[0] not in dic.keys():
#                 dic[s[0]] = s[1]
#         result_output(lines, dic)
