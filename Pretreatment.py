# -*- coding: utf-8 -*-
import os
from pyltp import Segmentor
import config
from my_log_new import Logger


class pretreatment:
    @staticmethod
    def cut_process(Questioning_path, new_word_path='./data/new_word.txt'):
        cws_model_path = os.path.join(config.LTP_DATA_DIR, 'cws.model')
        segmentor = Segmentor()
        segmentor.load(cws_model_path)
        with open(Questioning_path, 'r', encoding='utf8') as f:
            lines = f.readlines()
        with open(config.stopword_path, 'r', encoding='utf8') as f:
            stopword_list = f.readlines()

        new_word = []
        for line in lines:
            words = segmentor.segment(line.replace(' ', ''))

            words_list_temp = list(words)
            words_list = []
            for w in words_list_temp:
                if w not in stopword_list:
                    words_list.append(w)

            for i in range(len(words_list) - 1):
                if len(words_list[i]) == 1 and len(words_list[i + 1]) == 1:
                    w = words_list[i] + words_list[i + 1]
                    if w not in new_word:
                        new_word.append(w)
            Logger.log_DEBUG.debug('分词结果：' + str(words_list))
        segmentor.release()
        Logger.log_DEBUG.debug('新词：' + str(new_word))
        fw = open(new_word_path, 'w', encoding='utf8')
        for w in new_word:
            fw.write(w + '\n')
        fw.close()
        return new_word


if __name__ == '__main__':
    new_word = pretreatment.cut_process(config.Questioning_path, config.new_word_path)
    print(new_word)
