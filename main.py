#!/usr/bin/env python3

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
from mpl_toolkits import axisartist

work_path = sys.argv[1]
# work_path = r'F:\OneDrive - mail.ecust.edu.cn/Code_git/Python/draw_xvg/348K-70-2'
file_rdf_name = ['#rdf.xvg.1#','#rdf.xvg.2#','rdf.xvg']
file_cn_name = ['#rdf_cn.xvg.1#','#rdf_cn.xvg.2#','rdf_cn.xvg']
output_data_rdf_name = 'rdf.xyyy'
output_data_cn_name = 'cn.xyyy'

# 获取文件夹
def get_dir():
    os.chdir(work_path)
    name_list = os.listdir()
    return name_list

# 获得rdf与cn数据
def read_file(file_path):
    file_x_list=[]
    file_y_list=[]

    with open(file_path,"r",encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines:
        if (line.find('   ') == 0):
            x = float(line[0:11])
            file_x_list.append(x)
            y = float(line[12:22])
            file_y_list.append(y)
        else:
            continue
    
    # 文件头补零
    if (file_x_list[0] != 0.0):
        file_x_list.insert(0,0.0)
        file_y_list.insert(0,0.0)
    
    return (file_x_list,file_y_list)

# 合并rdf文件
def combin_rdf():
    (x_tmp,y_tmp) = read_file(f'./{file_rdf_name[0]}')
    all_np = np.asarray(x_tmp)
    for i in file_rdf_name:
        file_path=f'./{i}'
        (x_list,y_list) = read_file(file_path)
        # 利用np进行数组纵向合并转向
        all_np = np.column_stack((all_np, y_list))
    return all_np
# 合并cn文件
def combin_cn():
    (x_tmp,y_tmp) = read_file(f'./{file_cn_name[0]}')
    all_np = np.asarray(x_tmp)
    for i in file_cn_name:
        file_path=f'./{i}'
        (x_list,y_list) = read_file(file_path)
        # 利用np进行数组纵向合并转向
        all_np = np.column_stack((all_np, y_list))
    return all_np

# 写入数组文件
def write_file(np_list,name):
    np.savetxt(name,np_list)

# 画图
def draw(np_rdf,np_cn,i):
    host = host_subplot(111, axes_class=axisartist.Axes)
    par1 = host.twinx()
    par1.axis["right"].toggle(all=True)
    np_rdf_tr = np_rdf.transpose()
    np_cn_tr =np_cn.transpose()
    p1, = host.plot(np_rdf_tr[0],np_rdf_tr[1], 'r,-')
    p11, = host.plot(np_rdf_tr[0],np_rdf_tr[2], 'g,-')
    p12, = host.plot(np_rdf_tr[0],np_rdf_tr[3], 'b,-')
    p2, = par1.plot(np_cn_tr[0],np_cn_tr[1], 'r,:')
    p21, = par1.plot(np_cn_tr[0],np_cn_tr[2], 'g,:')
    p22, = par1.plot(np_cn_tr[0],np_cn_tr[3], 'b,:')
    
    # 坐标轴长度
    host.set_xlim(0.15, 0.8)   
    host.set_ylim(-1, 82)
    par1.set_ylim(-1, 15)
    
    host.set_xlabel("r(nm)")
    host.set_ylabel("g(r)")
    par1.set_ylabel("Coordination number")
    
    # host.legend()

    # plt.show()
    plt.plot()
    plt.savefig(f"./{i}.jpg")

# 写入数组文件，格式.xyyy 位宽9保留3位小数
def write_file(np_rdf,np_cn):
    with open(output_data_rdf_name,"w",encoding="utf-8") as f:
        for i in np_rdf:
            x = '%.3f' % i[0]
            y1 = '%.3f' % i[1]
            y2 = '%.3f' % i[2]
            y3 = '%.3f' % i[3]
            line = '{:>9s}{:>9s}{:>9s}{:>9s}\n'.format(x,y1,y2,y3)
            f.write(line)

    with open(output_data_cn_name,"w",encoding="utf-8") as f:
        for i in np_cn:
            x = '%.3f' % i[0]
            y1 = '%.3f' % i[1]
            y2 = '%.3f' % i[2]
            y3 = '%.3f' % i[3]
            line = '{:>9s}{:>9s}{:>9s}{:>9s}\n'.format(x,y1,y2,y3)
            f.write(line)


# 提取文件内容，在同目录下合并为单个文件
def main():
    name_list = get_dir()
    for i in name_list:
        os.chdir(f"{work_path}/{i}")
        print(f"Go to dir --> {i}...")
        np_rdf = combin_rdf()
        np_cn = combin_cn()
        write_file(np_rdf,np_cn)
        draw(np_rdf,np_cn,i)
        # break
    print("Successful Finished Draw!!!")


if __name__ == '__main__':
    main()