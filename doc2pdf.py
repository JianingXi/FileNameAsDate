import os
import win32com.client

def convert_doc_to_pdf(input_path, output_path):
    """
    使用 Word COM 接口将单个 .doc 文件转换为 .pdf
    FileFormat=17 对应 PDF 格式
    """
    word = win32com.client.Dispatch('Word.Application')
    word.Visible = False
    doc = word.Documents.Open(input_path, ReadOnly=1)
    try:
        doc.SaveAs(output_path, FileFormat=17)
        print(f"转换成功: {input_path} -> {output_path}")
    except Exception as e:
        print(f"转换失败: {input_path} ，原因：{e}")
    finally:
        doc.Close()

def batch_convert(folder_path):
    """
    遍历 folder_path 下所有 .doc 文件（不含 .docx），并转换为同名 .pdf
    """
    # 启动一次 Word 应用，加快批量处理
    word_app = win32com.client.Dispatch('Word.Application')
    word_app.Visible = False

    for filename in os.listdir(folder_path):
        base, ext = os.path.splitext(filename)
        if ext.lower() == '.doc':
            doc_path = os.path.join(folder_path, filename)
            pdf_path = os.path.join(folder_path, base + '.pdf')
            try:
                doc = word_app.Documents.Open(doc_path, ReadOnly=1)
                doc.SaveAs(pdf_path, FileFormat=17)
                doc.Close()
                print(f"[OK] {filename} → {base}.pdf")
            except Exception as e:
                print(f"[FAIL] {filename} 转换出错：{e}")

    # 处理完毕，退出 Word
    word_app.Quit()

if __name__ == '__main__':
    folder = r"C:\MyDocument\教材撰写\E04_原稿三审修改\教材pdf勘误\FileDocs"
    batch_convert(folder)
