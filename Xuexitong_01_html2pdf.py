import os
import re
import pdfkit
from pathlib import Path

# 配置 wkhtmltopdf 路径（根据实际安装路径修改）
config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')


def read_file_with_fallback(file_path):
    """
    尝试使用 UTF-8 编码读取文件，失败后使用 GBK 编码。
    返回内容和实际使用的编码。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content, 'utf-8'
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='gbk') as f:
                content = f.read()
            return content, 'gbk'
        except Exception as e:
            print(f"读取 {file_path} 时出错: {e}")
            return None, None


def write_file_with_encoding(file_path, content, encoding):
    """
    按指定编码写入文件内容。
    """
    try:
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
    except Exception as e:
        print(f"写入 {file_path} 时出错: {e}")


def insert_base_tag(html_path):
    """
    检查并在HTML文件的<head>标签中插入<base>标签，指向HTML所在目录的绝对路径。
    采用合适的编码方式读取文件。
    """
    content, encoding_used = read_file_with_fallback(html_path)
    if content is None:
        print(f"无法读取 {html_path}，跳过预处理。")
        return

    try:
        # 查找<head>标签
        head_match = re.search(r'<head.*?>', content, flags=re.IGNORECASE)
        if head_match:
            # 如果不存在 <base> 标签，则插入
            if not re.search(r'<base\s', content, flags=re.IGNORECASE):
                abs_dir = Path(html_path).parent.resolve()
                base_tag = f'<base href="file:///{abs_dir.as_posix()}/">'
                pos = head_match.end()
                content = content[:pos] + base_tag + content[pos:]
                write_file_with_encoding(html_path, content, encoding_used)
                print(f"已为 {html_path} 插入 <base> 标签")
    except Exception as e:
        print(f"预处理 {html_path} 时出错: {e}")


def html_to_pdf(html_path, pdf_path):
    """将HTML文件转换为PDF"""
    try:
        # 预处理HTML文件，插入<base>标签
        insert_base_tag(html_path)

        options = {
            'enable-local-file-access': None,  # 允许访问本地资源
            'load-error-handling': 'ignore',  # 忽略加载错误
            'load-media-error-handling': 'ignore'  # 忽略媒体加载错误
        }
        pdfkit.from_file(html_path, pdf_path, configuration=config, options=options)
        return True
    except Exception as e:
        print(f"转换失败 {html_path}: {e}")
        return False


def convert_html_files_in_directory(directory):
    """
    递归遍历目录，转换所有HTML文件为PDF
    """
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith(('.htm', '.html')):
                html_path = os.path.join(root, filename)
                pdf_path = os.path.splitext(html_path)[0] + '.pdf'
                print(f"正在处理: {html_path}")
                if html_to_pdf(html_path, pdf_path):
                    if os.path.exists(pdf_path):
                        try:
                            os.remove(html_path)
                            print(f"转换成功并已删除原始文件: {html_path}")
                        except Exception as e:
                            print(f"删除原始文件失败 {html_path}: {e}")
                    else:
                        print(f"PDF文件未生成: {pdf_path}")


if __name__ == "__main__":
    # 指定要处理的目录
    target_directory = r"D:\Alpha\StoreLatestYears\Store2025\B教学_教学与人才培养_A03_学生竞赛"

    if not os.path.isdir(target_directory):
        print("错误: 指定的路径不是一个有效的目录!")
        exit(1)

    print(f"开始处理目录: {target_directory}")
    print("将把所有HTML文件(.htm, .html)转换为PDF并删除原始文件")

    convert_html_files_in_directory(target_directory)
    print("处理完成!")
