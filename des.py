import pandas as pd
import shutil
import os,random
from datetime import datetime
import csv

def asx(jsondict,filename):
    df = pd.DataFrame.from_dict(jsondict)
    df.to_csv(f'downloads/{filename}.csv',index=False)

def combine_csv_files():
    input_directory = './downloads'
    output_directory = './downloads'
    output_file = os.path.join(output_directory, f'FinalSheet_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
    dataframes = []
    for filename in os.listdir(input_directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(input_directory, filename)
            df = pd.read_csv(file_path)
            dataframes.append(df)
    combined_df = pd.concat(dataframes, ignore_index=True)
    combined_df.to_csv(output_file, index=False)

def split_csv_file(n : int | str):
    chunk_size=125
    input_file_path = f'./resources/Main/gtx{n}.csv'
    output_directory = f'./resources/Temp/Splits{n}'
    output_file_prefix = 'Resource'
    shutil.rmtree(output_directory, ignore_errors=True)
    os.makedirs(output_directory, exist_ok=True)
    if f"gtx{n}.csv" in os.listdir("./resources/Main/"):
        df = pd.read_csv(input_file_path)
    else:
        print(f"gtx{n}.csv not found in the resources/Main directory. Please make sure the file exists.")
        raise FileNotFoundError(f"gtx{n}.csv not found in the resources/Main directory. Please make sure the file exists.")
    header = list(df.columns)
    total_rows = df.shape[0]
    num_chunks = (total_rows + chunk_size - 1) // chunk_size
    for i in range(num_chunks):
        start_index = i * chunk_size
        end_index = (i + 1) * chunk_size
        chunk_df = df.iloc[start_index:end_index]
        output_file = os.path.join(output_directory, f'{output_file_prefix}{i + 1}.csv')
        chunk_df.to_csv(output_file, index=False, header=header)

def choose_random_file():
    a=random.choice(os.listdir("./resources/Splits"))
    return a

def writeto(finame,text):
    writer = csv.writer(open(finame, "a+"))
    writer.writerow(text)

def checkforstring(filename,stringg) -> bool:
    with open(filename) as f:
        if stringg in f.read():
            return  True
        else:
            return False

if __name__ == "__main__":
    split_csv_file("1")
    split_csv_file("2")
    split_csv_file("3")