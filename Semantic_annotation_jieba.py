# -*- coding: utf-8 -*-
import os
import sys
import jieba.posseg
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import Parser

import config
from Sentence import sentence_class
import traceback
from log import logger


class semantic_annotation_jieba:
    ATT_ADV = ['ATT', 'ADV']
    N = ['a', 'd', 'b']
    dp_arcs = ['VOB', 'SBV', 'FOB']

    def __init__(self, dic):
        cws_model_path = os.path.join(config.LTP_DATA_DIR, 'cws.model')
        self.segmentor = Segmentor()
        self.segmentor.load(cws_model_path)

        self.segmentor.load_with_lexicon(cws_model_path, config.dic_path)

        pos_model_path = os.path.join(config.LTP_DATA_DIR, 'pos.model')
        self.postagger = Postagger()
        self.postagger.load(pos_model_path)

        par_model_path = os.path.join(config.LTP_DATA_DIR,
                                      'parser.model')
        self.parser = Parser()
        self.parser.load(par_model_path)

        jieba.load_userdict(dic.keys())

        self.dic = dic

    def Model_release(self):
        self.segmentor.release()
        self.postagger.release()
        self.parser.release()

    def set_sentence(self, sentence):
        try:
            result = jieba.posseg.cut(sentence)
            words_list = []
            for w in result:
                words_list.append(w.word)
            postags = self.postagger.postag(words_list)
            postags_list = list(postags)
            for i in range(len(postags_list)):
                if words_list[i] in self.dic.keys():
                    postags_list[i] = self.dic[words_list[i]]
            arcs = self.parser.parse(words_list, postags_list)
            arcs_list = list(arcs)
            s = '句法分析结果：'
            for a in arcs_list:
                s = s + str(a.head) + ":" + a.relation + '  '

            sen = sentence_class(words_list, postags_list, arcs_list)
            return sen
        except Exception as e:
            s = "设置句子属性发生异常set_sentence" + str(e)
            print(traceback.format_exc())
            logger.warning(s)
            logger.warning(sys.exc_info())

    def semantic_annotation_jieba(self, sentence):
        try:
            sen = self.set_sentence(sentence)
            dic_r = {}
            ap_ID = self.find_ap(sen)
            if ap_ID >= 0:
                dic_r['ap'] = sen.class_word_list[ap_ID].name
            else:
                dic_r['ap'] = '__'
            indiv_ID = self.find_indiv(sen)
            if indiv_ID >= 0:
                dic_r['indiv'] = sen.class_word_list[indiv_ID].name
            else:
                dic_r['indiv'] = '__'
            adv = self.find_AdvAdj(sen, ap_ID, 'adv')
            dic_r['adv'] = adv
            dp_ID = self.find_dp(sen)
            if dp_ID >= 0:
                dic_r['dp'] = sen.class_word_list[dp_ID].name
            else:
                dic_r['dp'] = '__'
            adj = self.find_AdvAdj(sen, dp_ID, 'adj')
            dic_r['adj'] = adj

            other = ''
            for w in sen.class_word_list:
                if w.Semantic_markup == 'other':
                    other = other + ',' + w.name
            dic_r['other'] = other if other != '' else '__'
            return dic_r

        except Exception as e:
            s = "语义标注主函数运行发生异常semantic_annotation_jieba" + str(e)
            logger.warning(s)
            logger.warning(sys.exc_info())

    def find_dp(self, sen):
        try:
            self.word_merge_A(sen)
            self.word_merge_COO(sen)
            self.word_merge_VOB(sen)
            self.word_merge_HED_VOB(sen)
            cwl = sen.class_word_list
            dp = []
            for i in range(len(cwl)):
                if cwl[i].Semantic_markup == 'other' and cwl[i].pos not in semantic_annotation_jieba.N \
                        and cwl[i].arcs_relation in semantic_annotation_jieba.dp_arcs and \
                        cwl[i].arcs_head == sen.ap_ID + 1:
                    dp.append(i)
            if len(dp) <= 0:
                for i in range(len(cwl)):
                    if cwl[i].Semantic_markup == 'other' and cwl[i].pos not in semantic_annotation_jieba.N \
                            and cwl[i].pos == 'n':
                        dp.append(i)
            if len(dp) > 0:
                sen.dp_ID = dp[0]
                cwl[dp[0]].Semantic_markup = 'dp'

            return sen.dp_ID
        except Exception as e:
            s = "确定数属发生异常find_dp" + str(e)
            logger.warning(s)
            logger.warning(sys.exc_info())
            raise TypeError(s)

    def word_merge_HED_VOB(self, sen):

        try:
            if sen.ap_ID != sen.hed_ID and sen.hed_ID >= 0:
                cwl = sen.class_word_list
                for i in range(len(cwl)):
                    if cwl[i].Semantic_markup == 'other' \
                            and cwl[i].arcs_relation == 'VOB' and cwl[i].arcs_head == sen.hed_ID + 1:
                        if self.is_merge(sen, sen.hed_ID + 1, i + 1):
                            if sen.hed_ID > i:
                                cwl[i].name = cwl[i].name + cwl[sen.hed_ID].name
                            else:
                                cwl[i].name = cwl[sen.hed_ID].name + cwl[i].name
                            cwl[i].arcs_relation = 'VOB'
                            cwl[sen.hed_ID].Semantic_markup = 'merge'
        except Exception as e:
            s = "当动作属性不是核心动词时核心动词和其宾语合并发生异常word_merge_HED_VOB" + str(e)
            logger.warning(s)
            logger.warning(sys.exc_info())

    def word_merge_VOB(self, sen):
        try:
            cwl = sen.class_word_list
            VOB_num = 0
            for i in range(len(cwl)):
                if cwl[i].Semantic_markup == 'other' \
                        and cwl[i].arcs_relation == 'VOB' and cwl[i].arcs_head == sen.hed_ID + 1:
                    VOB_num = VOB_num + 1

            for n in range(VOB_num):
                for i in range(len(cwl)):
                    if cwl[i].Semantic_markup == 'other' \
                            and cwl[i].arcs_relation == 'VOB' and cwl[i].arcs_head == sen.hed_ID + 1:
                        ioc = i + 1
                        for j in range(i, len(cwl)):
                            if cwl[j].Semantic_markup == 'other' \
                                    and cwl[j].arcs_relation == 'VOB' and cwl[j].arcs_head == sen.hed_ID + 1:
                                if self.is_merge(sen, ioc, j + 1):
                                    cwl[ioc - 1].name = cwl[ioc - 1].name + cwl[j].name
                                    cwl[ioc - 1].arcs_relation = 'VOB'
                                    cwl[j].Semantic_markup = 'merge'

        except Exception as e:
            s = "合并核心词宾语发生异常word_merge_VOB" + str(e)
            logger.warning(s)
            logger.warning(sys.exc_info())

    def word_merge_COO(self, sen):
        try:
            cwl = sen.class_word_list
            COO_num = 0
            for i in range(len(cwl)):
                if (cwl[i].Semantic_markup) == 'other' \
                        and (cwl[i].pos) not in semantic_annotation_jieba.N and cwl[i].arcs_relation == 'COO' \
                        and cwl[i].arcs_head == sen.ap_ID + 1:
                    COO_num = COO_num + 1
            for n in range(COO_num):
                for i in range(len(cwl)):
                    if cwl[i].Semantic_markup == 'other' and cwl[i].pos not in semantic_annotation_jieba.N \
                            and cwl[i].arcs_relation == 'COO' and cwl[i].arcs_head == sen.ap_ID + 1:
                        ioc = i + 1
                        for j in range(len(cwl)):
                            if cwl[j].Semantic_markup == 'other' and cwl[j].arcs_head == ioc \
                                    and cwl[j].arcs_relation == 'VOB':
                                if self.is_merge(sen, ioc, j + 1):
                                    if ioc > j + 1:
                                        cwl[ioc - 1].name = cwl[j].name + cwl[ioc - 1].name
                                    else:
                                        cwl[ioc - 1].name = cwl[ioc - 1].name + cwl[j].name
                                    cwl[ioc - 1].arcs_relation = 'VOB'
                                    cwl[j].Semantic_markup = 'merge'

        except Exception as e:
            s = "合并与动属并列的动词与其宾语发生异常word_merge_COO" + str(e)
            logger.warning(s)
            logger.warning(sys.exc_info())

    def word_merge_A(self, sen):
        try:
            cwl = sen.class_word_list
            A_num = 0
            for i in range(len(cwl)):
                if cwl[i].Semantic_markup == 'other' and cwl[i].pos not in semantic_annotation_jieba.N \
                        and cwl[i].arcs_relation in semantic_annotation_jieba.ATT_ADV:
                    A_num = A_num + 1
            for n in range(A_num):
                for i in range(len(cwl)):
                    if cwl[i].Semantic_markup == 'other' and cwl[i].pos not in semantic_annotation_jieba.N \
                            and cwl[i].arcs_relation in semantic_annotation_jieba.ATT_ADV:
                        Ioc = cwl[i].arcs_head
                        if cwl[Ioc - 1].Semantic_markup == 'other' and self.is_merge(sen, i + 1, Ioc):
                            s = '合并: ' + cwl[i].name + ' 和 ' + cwl[Ioc - 1].name
                            if i + 1 > Ioc:
                                cwl[Ioc - 1].name = cwl[Ioc - 1].name + cwl[i].name
                            else:
                                cwl[Ioc - 1].name = cwl[i].name + cwl[Ioc - 1].name

                            cwl[i].Semantic_markup = 'merge'
                            break
        except Exception as e:
            s = "合并定中和状中关系发生异常word_merge_A" + str(e)
            logger.warning(s)
            logger.warning(sys.exc_info())

    def is_merge(self, sen, A, Ioc):
        try:
            markup_List = ['merge']
            if abs(A - Ioc) == 1:
                return True
            if A > Ioc:
                for i in range(Ioc - 1, A):
                    if sen.class_word_list[i].Semantic_markup in markup_List:
                        return True
            else:
                for i in range(A - 1, Ioc):
                    if sen.class_word_list[i].Semantic_markup in markup_List:
                        return True
            return False
        except Exception as e:
            s = "判断两个词是否可以合并发生异常is_merge" + str(e)
            logger.warning(s)
            logger.warning(sys.exc_info())

    def find_AdvAdj(self, sen, ID, s_markup):
        try:
            advAdj = ''
            if ID < 0:
                return advAdj

            cwl = sen.class_word_list

            for i in range(len(cwl)):
                if cwl[i].arcs_head == ID + 1 and cwl[i].pos in semantic_annotation_jieba.N \
                        and cwl[i].Semantic_markup == 'other':
                    advAdj = advAdj + cwl[i].name + ","
                    cwl[i].Semantic_markup = s_markup
                if s_markup == 'adj':
                    if cwl[i].pos in semantic_annotation_jieba.N and \
                            cwl[i].Semantic_markup == 'other' and cwl[i].name not in advAdj:
                        advAdj = advAdj + cwl[i].name + ","
                        cwl[i].Semantic_markup = s_markup
            return advAdj
        except Exception as e:
            s = "确定状语和定语发生异常find_AdvAdj" + str(e)
            logger.warning(s)
            logger.warning(sys.exc_info())

    def find_indiv(self, sen):
        try:
            if len(sen.class_word_list) <= 3:
                for i in range(len(sen.class_word_list)):
                    if sen.class_word_list[i].Semantic_markup == 'other':
                        sen.class_word_list[i].Semantic_markup = 'indiv'
                        sen.indiv_ID = i
                        return sen.indiv_ID

            flag_1 = -1
            flag_2 = -1
            for i in range(len(sen.class_word_list)):
                if sen.class_word_list[i].Semantic_markup == 'other':
                    if flag_1 < 0:
                        flag_1 = i
                        continue
                    elif flag_2 < 0:
                        flag_2 = i
                        break
            if flag_2 - flag_1 != 1:
                sen.class_word_list[flag_1].Semantic_markup = 'indiv'
                sen.indiv_ID = flag_1
                return sen.indiv_ID

            wc0 = sen.class_word_list[flag_1]
            wc1 = sen.class_word_list[flag_2]

            if wc0.arcs_head == flag_2 + 1 and wc0.arcs_relation in semantic_annotation_jieba.ATT_ADV:
                if wc1.Semantic_markup == 'other' and wc1.pos == 'n':
                    wc1.name = wc0.name + wc1.name
                    wc1.Semantic_markup = 'indiv'
                    wc0.Semantic_markup = 'indiv_ATT'
                    sen.indiv_ID = flag_2
                else:
                    wc0.Semantic_markup = 'indiv'
                    sen.indiv_ID = flag_1
            else:
                wc0.Semantic_markup = 'indiv'
                sen.indiv_ID = flag_1
            return sen.indiv_ID
        except Exception as e:
            s = "确定个体发生异常find_indiv" + str(e)
            logger.warning(s)
            logger.warning(sys.exc_info())

    def find_ap(self, sen):
        try:
            cwl = sen.class_word_list
            for i in range(len(cwl)):
                if cwl[i].pos == 'v':
                    sen.V_ID = i
                    break
            if sen.V_ID < 0:
                logger.debug('该句子分词经过词性标注后没有动词')
                sen.ap_ID = -1
                return sen.ap_ID
            for i in range(len(cwl)):
                if cwl[i].arcs_relation == 'HED':
                    sen.hed_ID = i
                    break
            if sen.hed_ID < 0:
                logger.debug('经过句法分析没有核心词')
                sen.ap_ID = sen.V_ID
                return sen.ap_ID

            if sen.V_ID == sen.hed_ID:
                sen.ap_ID = sen.hed_ID
                cwl[sen.ap_ID].Semantic_markup = 'ap'
                return sen.ap_ID

            if cwl[sen.hed_ID].pos != 'v':
                new_hed = self.find_late(sen.hed_ID, sen.postags_list)
                if new_hed == sen.V_ID:
                    sen.ap_ID = sen.V_ID
                else:
                    if cwl[new_hed].arcs_head == sen.V_ID or cwl[sen.V_ID].arcs_head == new_hed:
                        sen.ap_ID = sen.V_ID
                    else:
                        sen.ap_ID = new_hed
            else:
                if cwl[sen.V_ID].arcs_head == sen.hed_ID + 1:
                    sen.ap_ID = sen.V_ID
                else:
                    sen.ap_ID = sen.hed_ID

            cwl[sen.ap_ID].Semantic_markup = 'ap'
            cwl[sen.hed_ID].arcs_head = cwl[sen.ap_ID].arcs_head
            cwl[sen.hed_ID].arcs_relation = cwl[sen.ap_ID].arcs_relation
            return sen.ap_ID
        except Exception as e:
            s = "确定动作属性发生异常find_ap" + str(e)
            logger.warning(s)
            logger.warning(sys.exc_info())

    def find_late(self, flag_hed, postags_list):
        try:
            flag_L = -1
            flag_R = -1
            for i in range(0, flag_hed):
                if postags_list[i] == 'v':
                    flag_L = i
            for i in range(flag_hed, len(postags_list)):
                if postags_list[i] == 'v':
                    flag_R = i
            if flag_L > 0 and flag_R > 0:
                if abs(flag_L - flag_hed) <= abs(flag_R - flag_hed):
                    return flag_L
                else:
                    return flag_R
            else:
                if flag_L > 0:
                    return flag_L
                else:
                    return flag_R

        except Exception as e:
            s = "找最近动词发生异常find_late" + str(e)
            logger.warning(s)
            logger.warning(sys.exc_info())


# if __name__ == '__main__':
#     s = '贷记卡自助还款'
#     sa = semantic_annotation_jieba()
#     r = sa.semantic_annotation_jieba(s)
#     print(r)
#     sa.Model_release()
