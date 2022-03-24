import copy

# 解候補を絞り込む
def narrow_down_candidates(answer_candidates : list, judge : list, inp):
    new_answer_candidates = copy.copy(answer_candidates)
    # 一度入力した語は削除してよい
    if inp in new_answer_candidates:
        new_answer_candidates.remove(inp)
    for word in answer_candidates:
        for nth in range(5):
            # 一度削除した単語は処理しなくてよい
            if word in new_answer_candidates:
                # 各桁の判定によって、解答候補に残らないものを除外する。
                if (judge[nth] == '2') and (inp[nth] != word[nth]):
                    new_answer_candidates.remove(word)
                elif (judge[nth] == '1') and (inp[nth] not in word):
                    new_answer_candidates.remove(word)
                elif (judge[nth] == '0'):
                    # judge[nth]がNBであり、かつ、inp[nth]がwordに含まれていても解答候補として残る場合を考える。
                    # このとき、inp[nth]がinpに2つ以上含まれている。1つだけだった場合、解答候補からは除外される。
                    # 以下の場合に分ける。
                    # (1)inp[nth]より左に同じ文字がある場合
                    #     (1-a) 左側の文字でEAT or BITEする場合 : 解答候補に残る(もし、左側のEAT or BITEがwordの条件に合致しない場合、そのEAT or BITE処理で弾かれている)
                    #     (1-b) 左側の文字がEATもBITEもしない場合 : 左側の文字のNB処理で既に除外されている
                    # (2)inp[nth]より右に同じ文字がある場合
                    #     (2-a) 右側の文字でEATする場合 : 解答候補に残る(もし、右側のEATがwordに合致しない場合、そのEAT処理で弾かれる)
                    #     (2-b) 右側の文字がBITE or NBの場合 : 解答候補から除外
                    if inp[nth] in word: # 基本的には、judge[nth]が0で、wordにinp[nth]が含まれていたら排除したい。
                        if inp.count(inp[nth]) >= 2: # 例外として、inp[nth]がinp内に2文字以上ある場合を考える
                            skip_condition = False
                            if inp.find(inp[nth], 0, nth) >= 0: # 左側に同じ文字がある場合
                                # nth より左側にある同じ文字のインデックスを取得し、judgeの値が1以上でないか調査
                                i = 0
                                while i < nth and i >= 0: # 左側すべてを探索する(左側に複数同じ文字がある場合を想定)。i < 0の場合は見つからなかった場合
                                    i = inp.find(inp[nth], i, nth)
                                    if i >= 0 and int(judge[i]) >= 1:
                                        skip_condition = True
                                        break
                                if skip_condition:
                                    continue
                            else: # 右側に同じ文字がある場合
                                i = nth+1
                                while i >= 0: # i < 0の場合は見つからなかった場合
                                    i = inp.find(inp[nth], i, 5)
                                    if i >= 0 and int(judge[i]) == 2:
                                        skip_condition = True
                                        break
                                if skip_condition:
                                    continue
                        new_answer_candidates.remove(word)
    return new_answer_candidates