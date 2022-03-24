def evaluate(inp, word):
    # 判定結果
    judge = [0] * 5
    # すでに評価した文字かを管理するためのフラグ
    is_already_judged = [False] * 5

    # 入力値の評価
    # 先にEATのみ評価する。BITEした答えの文字が評価済みとなってEAT判定されない状況を防ぐ
    for i in range(5):
        if inp[i] == word[i]:
            judge[i] = 2
            is_already_judged[i] = True

    # BITE判定
    for i in range(5): # 入力したアルファベットのインデックス
        if judge[i] == 2: # EAT判定が出ている入力文字はスキップ
            continue
        for j in range(5): # 解答のアルファベットのインデックス
            if is_already_judged[j]: # すでに評価された解答のアルファベットはスキップ
                continue
            elif inp[i] == word[j]: # EAT判定はすでに終えており、EAT判定が出た文字はスキップするのでi == jになることはない
                judge[i] = 1
                is_already_judged[j] = True
                break
    return judge

