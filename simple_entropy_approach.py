import pandas as pd
import math
import numpy as np
import copy
import evaluater
import common_process

word_list_master = list(pd.read_csv('./data/wordlist.csv', header=None)[0])
word_list_len = len(word_list_master)

def main():

    entropies = pd.read_csv('./data/honke_init_entropies.csv', index_col=0)
    # entropies = pd.read_csv('init_entropies.csv', index_col=0)
    answer_candidates = list(pd.read_csv('./data/candidates.csv', header=None)[0])
    guess_count = 0
    judge = ['','','','','']
    inp = ''
    inp_history = []

    # 通常。効率測定の再にはコメントアウトする
    #'''
    while True:
        guess_count += 1
        # エントロピー計算。初手、二手目は既に計算済み。解答候補1つのときは計算不要、2つを絞るのはエントロピーの計算では難しいのでどちらかを出す。
        if guess_count > 2 and len(answer_candidates) > 2:
            reset_entropy(entropies)
            calc_all_entropy(answer_candidates, entropies, inp_history)

        if guess_count != 2: # 2手目は別のファイルに保存済み
            inp = get_best_input(answer_candidates, entropies)
        else:
            # pandas、read_csvでindexの型を指定する方法がなく'00001'みたいな値はintにキャストされてしまう模様
            # 一度dtype=strとして全列読み込み、後にindexとして読ませることにする
            sg = pd.read_csv('./data/soare_second_guesses.csv', dtype=str).set_index('judge')
            inp = sg.at[''.join(judge), 'word']

        if len(answer_candidates) > 1:
            print('Candidates: ' + str(len(answer_candidates)))
        else:
            print('Answer:')

        # 現在のエントロピーと解答候補を出力。デバッグ用
        # entropies.to_csv('./outputs/temp_entropy.csv')
        # pd.DataFrame(answer_candidates).to_csv('./outputs/temp_answer_can.csv')

        inp_history.append(inp)
        print(inp)
        judge = list(input())
        answer_candidates = copy.copy(common_process.narrow_down_candidates(answer_candidates, judge, inp))
    #'''

    # 効率計測用
    '''
    question_num = 0
    answer_list = list(pd.read_csv('./data/candidates_for_test.csv', header=None)[0])
    results = pd.read_csv('./outputs/results.csv', index_col=0)

    for ans in answer_list:
        question_num += 1
        print('##################')
        print('Q' + str(question_num) + ' : ' + ans)
        print('##################')
        while True:
            guess_count += 1
            # エントロピー計算。初手、二手目は既に計算済み。解答候補1つのときは計算不要、2つを絞るのはエントロピーの計算では難しいのでどちらかを出す。
            if guess_count > 2 and len(answer_candidates) > 2:
                reset_entropy(entropies)
                # calc_candidate_entropy(answer_candidates, entropies)
                calc_all_entropy(answer_candidates, entropies, inp_history)

            if guess_count != 2: # 2手目は別のファイルに保存済み
                inp = get_best_input(answer_candidates, entropies)
            else:
                # pandas、read_csvでindexの型を指定する方法がなく'00001'みたいな値はintにキャストされてしまう模様
                # 一度dtype=strとして全列読み込み、後にindexとして読ませることにする
                sg = pd.read_csv('./data/soare_second_guesses.csv', dtype=str).set_index('judge')
                inp = sg.at[''.join(judge), 'word']

            if len(answer_candidates) > 1:
                print('Candidates: ' + str(len(answer_candidates)))
            else:
                print('Answer:')

            inp_history.append(inp)
            print(inp)
            judge = list(''.join(map(str, evaluater.evaluate(inp,ans))))
            print(judge)
            # judge = list(input())
            if judge == ['2','2','2','2','2'] or guess_count > 10:
                results.loc[inp] = guess_count
                guess_count = 0
                inp_history = []
                entropies = pd.read_csv('./data/honke_init_entropies.csv', index_col=0)
                answer_candidates = list(pd.read_csv('./data/candidates.csv', header=None)[0])
                break
            else:
                answer_candidates = copy.copy(common_process.narrow_down_candidates(answer_candidates, judge, inp))
    results.to_csv('./outputs/results.csv')
    '''

def reset_entropy(entropies : pd.DataFrame):
    for i in range(len(entropies)):
        entropies.iat[i, 0] = 0

def get_best_input(answer_candidates : list, entropies : pd.DataFrame):
    if 0 < len(answer_candidates) <= 2: # 候補が残り2つのときもうだうだ減らそうとする。候補2つのときの処理は改良予定
        return answer_candidates[0]
    else:
        return entropies['H'].idxmax()

# すべての入力可能な単語に対してエントロピーを再計算する
def calc_all_entropy(answer_candidates : list, entropies : pd.DataFrame, inp_history : list):
    # 総当りで各状態の出現回数を求める
    for word_num in range(word_list_len):
        # 既に入力したことのある単語は情報量0
        if word_list_master[word_num] in inp_history:
            entropies.iat[word_num, 0] = 0
            continue
        count_each_judge = np.zeros((3,3,3,3,3), dtype= int) # 各状態ごとの出現回数を記録する5次元配列
        for obj_word in answer_candidates:
            # 判定
            judge = evaluater.evaluate(word_list_master[word_num], obj_word)
            count_each_judge[judge[0]][judge[1]][judge[2]][judge[3]][judge[4]] += 1
        # 単語のエントロピーを計算
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        for m in range(3):
                            if count_each_judge[i][j][k][l][m] > 0: # == 0 の場合は確率0なので自己エントロピーも0
                                entropies.iat[word_num, 0] -= count_each_judge[i][j][k][l][m] / len(answer_candidates) * math.log2(count_each_judge[i][j][k][l][m] / len(answer_candidates))
if __name__ == '__main__':
    main()