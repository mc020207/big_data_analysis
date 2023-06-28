import re
import os 
import jieba.posseg as pseg

# input file folder path
file_base = './demorawdata/'
# output file folder path
out_base = './demodata/'
# input file encoding
file_encoding = 'gbk'
# output file encoding
out_encoding = 'utf-8'

def preprocess():
    file_names = os.listdir(file_base)
    for file_name in file_names:
        # input file path
        file_path = file_base + file_name
        # output file path
        out_path = out_base + 'data'
        with open(file_path, mode='r', encoding=file_encoding, errors="ignore") as fin:
            lines = list(line for line in fin.read().split('\n') if line != "")
        with open(out_path, mode='a', encoding=out_encoding) as fout:
            for line in lines:
                title = re.sub(r'(?:\s+)', ' ', line.strip()).split(' ')[2][1:-1]
                words = pseg.cut(str(title))
                split = []
                for word, flag in words:
                    if flag in ['m', 'q', 'r', 'p', 'c', 'u', 'xc', 'w', 'x']: continue
                    split.append(word)
                if len(split) > 0:
                    split = list(set(split))
                    fout.write(' '.join(split) + '\n')
        # debug info
        print(f'complete {file_path}')

if __name__ == '__main__':
    preprocess()
    