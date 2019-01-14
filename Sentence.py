# -*- coding: utf-8 -*-
from Word import word_class


class sentence_class:
    def __init__(self, words_list, postags_list, arcs_list):
        self.class_word_list = self.set_word_list(words_list, postags_list, arcs_list)
        self.words_list = words_list
        self.postags_list = postags_list
        self.arcs_list = arcs_list
        self.ap_ID = -1
        self.dp_ID = -1
        self.hed_ID = -1
        self.indiv_ID = -1
        self.V_ID = -1

    def set_word_list(self, words_list, postags_list, arcs_list):
        class_word_list = []
        self.words_list = words_list
        self.words_list = words_list
        self.arcs_list = arcs_list
        for i in range(len(words_list)):
            w = word_class()
            w.name = words_list[i]
            w.pos = postags_list[i]
            w.arcs_head = arcs_list[i].head
            w.arcs_relation = arcs_list[i].relation
            class_word_list.append(w)
        return class_word_list
