# File and Directory Renamer / 文件和目录重命名器

This script renames files and directories in a specified directory according to a specific set of rules. It cleans the names by replacing certain characters, removes duplicate underscores, and prepends the last modification date to the names. Temporary directories are created and used to facilitate the renaming process.

该脚本根据特定规则重命名指定目录中的文件和目录。它通过替换某些字符来清理名称，删除重复的下划线，并在名称前添加最后修改日期。临时目录被创建和使用以便于重命名过程。

## Features / 功能
- Sanitize file and directory names by replacing specific characters.
- Prepend the last modification date to file and directory names.
- Create and use a temporary directory to avoid conflicts during renaming.

- 通过替换特定字符来清理文件和目录名称。
- 在文件和目录名称前添加最后修改日期。
- 创建并使用临时目录以避免重命名过程中的冲突。

## Usage / 使用方法

1. Clone the repository / 克隆仓库:
   ```sh
   git clone https://github.com/yourusername/file-dir-renamer.git
   cd file-dir-renamer
   ```

2. Update the base directory in the `main` function / 更新 `main` 函数中的基础目录:
   ```python
   basedir = r'C:\Users\DELL\Desktop\ToDo'
   ```

3. Run the script / 运行脚本:
   ```sh
   python rename_script.py
   ```

## Functions / 函数

### `create_temp_dir(directory)`
Creates a temporary directory for processing.

创建一个用于处理的临时目录。

### `sanitize_filename(filename)`
Cleans the filename by replacing specific characters and removing duplicate underscores.

通过替换特定字符和删除重复的下划线来清理文件名。

### `prepend_date_to_filename(filename, date)`
Prepends the last modification date to the filename.

在文件名前添加最后修改日期。

### `move_files_with_new_names(src_dir, dst_dir)`
Moves and renames files from the source directory to the destination directory.

移动并重命名文件从源目录到目标目录。

### `move_directories_with_new_names(src_dir, dst_dir)`
Moves and renames directories from the source directory to the destination directory.

移动并重命名目录从源目录到目标目录。

### `main()`
Main function that sets the base directory, creates a temporary directory, and processes the renaming of files and directories.

设置基础目录、创建临时目录并处理文件和目录重命名的主函数。

## Example / 示例

Before running the script / 运行脚本之前:
```
ToDo/
├── example file.txt
├── example-directory/
└── another file (2022).txt
```

After running the script / 运行脚本之后:
```
ToDo/
├── D20230701_example_file.txt
├── D20230701_example_directory/
└── D20230701_another_file_2022.txt
```

## License / 许可

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

此项目是根据 MIT 许可的。有关详细信息，请参阅 [LICENSE](LICENSE) 文件。
