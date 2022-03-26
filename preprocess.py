import pandas as pd
import math
import numpy as np
import copy
import evaluater
import common_process
import simple_entropy_approach

word_list_master = list(pd.read_csv('wordlist.csv', header=None)[0])
word_list_len = len(word_list_master)

def main():
    # calc_first_entropy_honke(pd.read_csv('words_with_zero.csv', index_col=0))
    make_second_guess_list('soare')


def make_second_guess_list(first_guess : str):
    second_guesses = pd.DataFrame(index=[], columns=['word'])
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    for m in range(3):
                        entropies = pd.read_csv('words_with_zero.csv', index_col=0)
                        answer_candidates = list(pd.read_csv('candidates.csv', header=None)[0])
                        judge = [str(i), str(j), str(k), str(l), str(m)]
                        print(''.join(judge))
                        answer_candidates = copy.copy(common_process.narrow_down_candidates(answer_candidates, judge, first_guess))
                        simple_entropy_approach.calc_all_entropy(answer_candidates, entropies, [first_guess])
                        print(entropies['H'].idxmax())
                        second_guesses.loc[''.join(judge)] = [entropies['H'].idxmax()]
    second_guesses.to_csv('second_guesses.csv')


# すべての入力可能単語をすべての入力可能単語と総当たりして対象としてエントロピーの初期値を計算する
def calc_first_entropy_all(entropies : pd.DataFrame):
    # 総当りで各状態の出現回数を求める
    for word_num in range(word_list_len):
        # 各状態ごとの出現回数を記録する5次元配列
        count_each_judge = np.zeros((3,3,3,3,3), dtype= int)
        print(word_list_master[word_num])
        for obj_word in word_list_master:
            judge = [0, 0, 0, 0, 0]
            # 判定
            judge = evaluater.evaluate(word_list_master[word_num], obj_word)
            count_each_judge[judge[0]][judge[1]][judge[2]][judge[3]][judge[4]] += 1
        # 単語のエントロピーを計算
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        for m in range(3):
                            if count_each_judge[i][j][k][l][m] > 0: # == 0 の場合は確率も0なので自己エントロピーも0
                                entropies.iat[word_num, 0] -= (count_each_judge[i][j][k][l][m] / word_list_len) * math.log2(count_each_judge[i][j][k][l][m] / word_list_len)
    entropies.to_csv('init_entropies.csv')

# すべての入力可能単語を本家の解答候補と総当たりしてエントロピーの初期値を計算する
def calc_first_entropy_honke(entropies : pd.DataFrame):
    ans_can = list(pd.read_csv('candidates.csv', header=None)[0])
    # 総当りで各状態の出現回数を求める
    for word_num in range(word_list_len):
        # 各状態ごとの出現回数を記録する5次元配列
        count_each_judge = np.zeros((3,3,3,3,3), dtype= int)
        print(word_list_master[word_num])
        for obj_word in ans_can:
            # 判定
            judge = evaluater.evaluate(word_list_master[word_num], obj_word)
            count_each_judge[judge[0]][judge[1]][judge[2]][judge[3]][judge[4]] += 1
        # 単語のエントロピーを計算
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        for m in range(3):
                            if ''.join(map(str, [i,j,k,l,m])) not in entropies.columns.values:
                                entropies[''.join(map(str, [i,j,k,l,m]))] = 0
                            entropies.at[word_list_master[word_num], ''.join(map(str, [i,j,k,l,m]))] = count_each_judge[i][j][k][l][m]
                            if count_each_judge[i][j][k][l][m] > 0: # == 0 の場合は確率も0なので自己エントロピーも0
                                entropies.iat[word_num, 0] -= (count_each_judge[i][j][k][l][m] / word_list_len) * math.log2(count_each_judge[i][j][k][l][m] / word_list_len)
    entropies.to_csv('honke_init_entropies_with_count_each_judge.csv')                   


if __name__ == '__main__':
    main()