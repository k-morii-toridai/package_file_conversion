""" This module is written for convert POSCAR to pd.DataFrame. """


import pandas as pd
# 表示オプションを設定
pd.set_option('display.float_format', '{:.6f}'.format)


def poscar2df(poscar_path='./POSCAR'):
    """
    This func converts POSCAR to pd.DataFrame.

    Usage:
    -------
    df_poscar = poscar2df(poscar_path=poscar_path)

    Parameter:
    ------------
    poscar_path: str or pathlib.Path

    Return:
    -------
    pd.DataFrame
    """
    # POSCARファイルを読み込む
    with open(poscar_path, 'r') as file:
        lines = file.readlines()

    # 原子種とその数を含む行を抽出
    species_names = lines[5].split()
    ions_per_species = [int(s) for s in lines[6].split()]
    # 原子種のリストと対応する数のリストを抽出
    species_list = [species_name for species_name, count in zip(species_names, ions_per_species) for _ in range(count)]
    # 原子種とその数からDataFrameを作成
    df_species = pd.DataFrame(species_list, columns=['atom_symbol'])

    # 原子ごと（行ごと）に，idを割り振る
    df_atom_ids = pd.DataFrame(list(range(1, len(df_species) + 1)), columns=['atom_id'])

    # 構造情報が始まる行を特定
    for i, line in enumerate(lines):
        if ('Direct' in line) or ('Cartesian' in line):
            start_line = i + 1
    # 原子座標データを取得
    ion_positions_list = lines[start_line:]
    df_xyz = pd.DataFrame([ion_position_line.split() for ion_position_line in ion_positions_list], columns=['x', 'y', 'z'])

    # 原子idのDataFrameと構造情報のDataFrameと原子集のDataFrameを結合
    df_poscar = pd.concat([df_atom_ids, df_xyz, df_species], axis=1)

    # 列ごとにデータ型を変更
    df_poscar['atom_id'] = df_poscar['atom_id'].astype(str)
    df_poscar[['x', 'y', 'z']] = df_poscar[['x', 'y', 'z']].astype(float)

    return df_poscar


if __name__ == '__main__':
    # poscar_path='sample_test_files/POSCAR'
    poscar_path = '/mnt/ssd_elecom_c2c_960gb/cif/1/00/00/1000033/POSCAR'
    df_poscar = poscar2df(poscar_path=poscar_path)
