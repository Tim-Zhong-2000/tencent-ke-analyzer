import os
import sys
import argparse
import pandas as pd
from student import Student

student_list = []

# get student by key
# if student not exist return -1


def get_student(key):
    for i in range(len(student_list)):
        if student_list[i].get_key() == key:
            return i
    return -1


def process_excel(path):
    excel = pd.read_excel(path)
    rows_num = len(excel.index.values)
    # read the excel
    for i in range(rows_num):
        if i > 3:
            key = excel.iloc[i, 4]
            index = get_student(key)
            if index == -1:
                student_list.append(Student(str(key)))
                index = len(student_list) - 1

            student_list[index].record_name(excel.iloc[i, 3])
            if excel.iloc[i, 5] == "是":
                student_list[index].record_live(excel.iloc[i, 7])
            if excel.iloc[i, 8] == "是":
                student_list[index].record_playback(excel.iloc[i, 9])


if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.argv.append('--help')
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help="输入存放考勤表格目录", required=True)
    parser.add_argument('-o', '--output', help="输出的文件名", required=True)
    args = parser.parse_args()

    rootdir = args.input
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    print("开始导入")
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        if os.path.isfile(path) & path.endswith(".xlsx"):
            process_excel(path)
    print("导入成功")

    print("开始输出")
    outname = args.output
    outpath = rootdir + outname
    try:
        f = open(outpath, 'w')
        print("正在输出")
        # write the result
        for student in student_list:
            f.write(student.get_student_id() + '\t'
                    + student.get_name() + '\t'
                    + student.get_live_num() + '\t'
                    + student.get_live_time() + '\t'
                    + student.get_playback_num() + '\t'
                    + student.get_playback_time() + '\n'
                    )
        f.close()
        print("输出成功")
    except:
        print("输出文件失败")
