import os

import pandas as pd
import tomllib


def read_config(config_file):
    with open(config_file, "rb") as f:
        config = tomllib.load(f)
    return config


# my_config = read_config("example/config.toml")
# print(my_config)
def read_components(info) -> pd.DataFrame:
    path = info.get("file", "")
    df = pd.DataFrame()
    if not os.path.exists(path):
        print(f"Could not find {path}, please check your config input")
        return pd.DataFrame()
    else:
        mtype = info.get("type", "")
        if len(mtype) == 0:
            print(
                f"Could not decide file type of {path}, please check your config input"
            )
            return pd.DataFrame()
        elif mtype == "csv" or mtype == "tsv":
            if mtype == "csv":
                df = pd.read_csv(path)
            elif mtype == "tsv":
                df = pd.read_csv(path, sep="\t")
            id_col = info.get("id", "sample_id")
            other_cols = info.get("column", [])
            try:
                df_sub = df[[id_col] + other_cols]
                df_sub.colnames = ["sample_id"] + other_cols
                return df_sub.to_frame()
            except:
                print(
                    "Could not find all the columns from the config inputs, please check your input file and config"
                )
                return pd.DataFrame()
        elif mtype == "noname":
            id_col_n = info.get("id", 0)
            other_col_n = info.get("columns", [])
            colnames = info.get("colnames", [])
            usecols = [id_col_n] + other_col_n
            names = ["sample_id"] + colnames
            df = pd.read_csv(path, sep="\t", usecols=usecols, names=names)
            return df
        elif mtype == "keyvalue":
            delimit = info.get("deli", "\t")
            cols = []
            values = []
            with open(path, "r") as myfile:
                for line in myfile:
                    key, value = line.strip().split(delimit)
                    cols.append(key)
                    values.append(value)
            df = pd.DataFrame(data=[values], columns=cols)
            return df
        return pd.DataFrame()


def collapse_info(config, output="all_summary.csv"):
    config_data = read_config(config)
    df_merge = pd.DataFrame()
    for key in config_data:
        if key == "title":
            continue
        else:
            value = config_data[key]
            df = read_components(value)
            if df.empty:
                continue
            if df_merge.empty:
                df_merge = df.copy()
            elif "sample_id" in list(df_merge.columns):
                df_merge = df_merge.merge(
                    df, on="sample_id", how="left"
                ).drop_duplicates()
            else:
                df_merge = df_merge.merge(df, how="cross")
    df_merge.to_csv(output, index=False)


if __name__ == "__main__":
    collapse_info("sample/config.toml")
