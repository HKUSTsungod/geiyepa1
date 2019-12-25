"""
将多个曲谱合并为一个pdf，1-2页的出一本，3页及以上出一本，全部出一本
"""
import os
# noinspection PyProtectedMember
from PyPDF2 import PdfFileReader, PdfFileWriter

root_path = "./result"
target_path = "./book"
oneTwoPages = []
threeMorePages = []

index_info = [] # 书页信息


def merge_pdf(infnList, outfn):
    """
    infnList: 需要合并的pdf列表
    outfn：合并之后的pdf名
    """
    iindex = 3
    global index_info
    index_info = []
    pdf_output = PdfFileWriter()
    for infn in infnList:
        if infn == ".DS_Store":
            continue
        pdf_input = PdfFileReader(open(root_path + "/" + infn, 'rb'))
        page_count = pdf_input.getNumPages()
        index_info.append(infn[:-4] + "--" + str(iindex))
        iindex += page_count
        for i in range(page_count):
            pdf_output.addPage(pdf_input.getPage(i))

    if not os.path.exists(target_path + "/" + outfn + ".pdf"):
        pdf_output.write(open(target_path + "/" + outfn + ".pdf", 'wb'))
        print("write!")


def divide_by_pages(pdfName):
    """
    :param pdf: 传入的pdf名字，不含路径
    :return: void
    """
    pdf_input = PdfFileReader(open(root_path + "/" + pdfName, 'rb'))
    page_count = pdf_input.getNumPages()
    if page_count < 3:
        oneTwoPages.append(pdfName)
    else:
        threeMorePages.append(pdfName)


def index_output(book):
    """
    given index_info list, output a txt file
    :argument book: 书名
    :return: void
    """
    with open(target_path + "/" + book + ".txt", "w") as f:
        for line in index_info:
            f.write(line + "    ")


if __name__ == '__main__':
    if not os.path.exists(target_path):
        os.mkdir(target_path)
    files = os.listdir(root_path)
    files.sort()
    for pdf in files:
        divide_by_pages(pdf)
    index = 3  # 书页
    merge_pdf(oneTwoPages, "oneTwoPages")
    index_output("oneTwoPages")
    print("12finish")
    merge_pdf(threeMorePages, "threeMorePages")
    index_output("threeMorePages")
    print("345finish")
    merge_pdf(files, "all")
    index_output("all")
    print("all finish")
