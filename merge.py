"""
对pdf进行归类并合并, 每首歌合并为一个pdf
"""
# noinspection PyProtectedMember
from PyPDF2 import PdfFileReader, PdfFileWriter
import os
root_path = "./pdf"
target_path = "./result"
pdf_dic = {}

if not os.path.exists(root_path):
    os.mkdir(root_path)
if not os.path.exists(target_path):
    os.mkdir(target_path)

def merge_pdf(infnList, outfn):
    """
    infnList: 需要合并的pdf列表
    outfn：合并之后的pdf名
    """
    pdf_output = PdfFileWriter()
    for infn in infnList:
        pdf_input = PdfFileReader(open(root_path + "/" + infn, 'rb'))
        page_count = pdf_input.getNumPages()

        for i in range(page_count):
            pdf_output.addPage(pdf_input.getPage(i))

    if not os.path.exists(target_path + "/" + outfn + ".pdf"):
        pdf_output.write(open(target_path + "/" + outfn + ".pdf", 'wb'))
        print("write!")


for file in os.listdir(root_path):
    if file == ".DS_Store":
        continue
    base = file[:-5]
    if base[-1] == "1" or base[-1] == "2":
        base = base[:-1]

    if base not in pdf_dic:
        pdf_dic[base] = []
    pdf_dic[base].append(file)

for pdf in pdf_dic:
    print(pdf, pdf_dic[pdf])
    merge_pdf(pdf_dic[pdf], pdf)

