from pathlib import Path
import re  # 正则表达式
import os

# =========================
# 配置
# =========================

# 当前 Git 仓库根目录
# 获取当前python脚本所在的目录，并将其作为仓库根目录
# __file__ 是一个特殊变量，表示当前脚本的路径,Path() 将__file__转换为 Path 对象，.resolve() 方法将路径解析为绝对路径，.parent 获取该路径的父目录，即脚本所在的目录
ROOT = Path(__file__).resolve().parent

# 支持的图片格式
IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".svg",
    ".bmp",
}

# True：只预览，不修改文件
# False：真正修改 Markdown 文件
DRY_RUN = False


# =========================
# 建立图片索引
# =========================

def build_image_index():
    """
    将整个仓库的图片找出来，建立一个“文件名-->图片路径”的索引，方便后续查找图片
    例如：
        image_index = {
            "image1.png": [Path("/path/to/image1.png")],
            "image2.jpg": [Path("/path/to/image2.jpg"), Path("/path/to/another/image2.jpg")],
        }
    """

    image_index = {}

    # 遍历仓库所有文件,使用 rglob("*") 方法递归地查找所有文件和目录
    # rglob("*") 方法会递归地查找ROOT下面的所有文件和目录，返回一个生成器，生成器会遍历所有匹配的路径对象
    for path in ROOT.rglob("*"):

        # 只处理文件，rglob("*")还会返回目录，所以需要判断是否为文件
        # is_file() 方法用于判断路径是否为文件，如果是文件则返回 True，否则返回 False
        if not path.is_file():
            continue

        # 排除 .git，path.parts 属性返回路径的各个部分组成的元组，例如 Path("/a/b/c").parts 返回 ('/', 'a', 'b', 'c')
        if ".git" in path.parts:
            continue

        # 只处理图片
        # suffix 属性用于获取路径的后缀名（包括点号），lower() 方法将后缀名转换为小写，以便进行不区分大小写的比较
        if path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        # 拿到文件名
        # name 属性用于获取路径的文件名部分，例如 Path("/a/b/c.txt").name 返回 "c.txt"
        name = path.name

        # 同名图片可能存在于不同目录
        # setdefault() 方法用于在字典中设置键值对，如果键不存在则添加键值对，如果键已存在则不做任何操作
        # 这里使用 setdefault() 方法将图片文件名作为键，图片完整路径作为值，存储在 image_index 字典中
        image_index.setdefault(name, []).append(path)

    return image_index


# =========================
# 计算 Markdown 图片相对路径
# =========================

def make_relative_path(md_file, image_file):
    """
    计算图片相对于 Markdown 文件的相对路径，更新的图片链接后括号中的路径
    """

    # 计算相对路径
    # os.path.relpath() 方法用于计算两个路径之间的相对路径，第一个参数是目标路径，第二个参数是起始路径
    relative = os.path.relpath(
        image_file,
        start=md_file.parent
    )

    # Windows 兼容处理，Mac/Linux 本身就是 /
    relative = relative.replace("\\", "/")

    # URL 中空格需要编码
    # quote模块用于对 URL 中的特殊字符进行编码，确保生成的链接在浏览器中可以正确访问
    from urllib.parse import quote

    # quote() 方法用于对 URL 中的特殊字符进行编码，safe 参数用于指定哪些字符不需要编码，这里指定了 /:@-._~ 这些字符不需要编码
    return quote(relative, safe="/:@-._~")


# =========================
# 转换单个 Markdown 文件
# 打开一个 Markdown 文件，把里面的 Obsidian 图片链接全部找出来，然后转换。
# =========================

def process_markdown(md_file, image_index):

    # 读取 Markdown 文件内容
    try:
        content = md_file.read_text(encoding="utf-8") # 读取文件内容，指定编码为 utf-8
    except UnicodeDecodeError:
        print(f"⚠️ 无法读取：{md_file}") 
        return False

    # 备份原始内容，用于后续比较是否有修改
    original_content = content

    # 匹配：
    #
    # ![[xxx.png]]
    #
    # ![[xxx.jpg|300]]
    #
    # ![[xxx.png|alt text]]
    pattern = re.compile(
        r'!\[\[([^\]|]+?)(?:\|[^\]]*)?\]\]' 
    )

    # 替换函数，用于将匹配到的 Obsidian 图片链接转换为 Markdown 图片链接
    
    def replace_image(match):

        # 获取图片名称
        # match.group(1) 获取正则表达式中第一个捕获组的内容，即图片名称
        # strip() 方法用于去除字符串两端的空白字符，包括空格、制表符和换行符
        image_name = match.group(1).strip()

        # 如果没有扩展名，尝试判断
        image_path_candidates = []

        # 如果有扩展名，根据文件名找图片路径
        #Path(image_name) 将图片名称转换为 Path 对象，.suffix 属性用于获取路径的后缀名（包括点号），如果有后缀名则直接在 image_index 中查找对应的图片路径列表
        # suffix 属性用于获取路径的后缀名（包括点号），如果有后缀名则直接在 image_index 中查找对应的图片路径列表
        if Path(image_name).suffix:
            # Path(image_name).name 获取图片名称的文件名部分（不包含路径），然后在 image_index 中查找对应的图片路径列表，如果找不到则返回空列表
            # get() 方法用于从字典中获取指定键的值，如果键不存在则返回默认值，这里默认值为空列表 []
            image_path_candidates = image_index.get(
                Path(image_name).name,
                []
            )
        else:
            for ext in IMAGE_EXTENSIONS:
                # extend() 方法用于将一个可迭代对象中的元素添加到列表的末尾，这里将 image_index 中对应扩展名的图片路径列表添加到 image_path_candidates 列表中
                image_path_candidates.extend(
                    image_index.get(
                        image_name + ext,
                        []
                    )
                )

        # 没找到
        if not image_path_candidates:
            print(
                f"⚠️ 找不到图片：{image_name}"
                f"\n   Markdown：{md_file}"
            )

            # 保持原样
            # group(0) 方法用于获取整个匹配的字符串，即原始的 Obsidian 图片链接
            return match.group(0)

        # 如果同名图片有多个
        if len(image_path_candidates) > 1:

            # 优先选择 Markdown 所在目录下的图片
            # sorted() 方法用于对列表进行排序，这里根据图片路径相对于 Markdown 文件的相对路径的层级数进行排序，层级数越少的图片路径越靠前
            # key=lambda p: len(os.path.relpath(p, start=md_file.parent).split(os.sep)) 这里使用了一个匿名函数作为排序的键，计算图片路径相对于 Markdown 文件的相对路径的层级数，层级数越少的图片路径越靠前
            # os.sep 是操作系统的路径分隔符，在 Windows 上是 \，在 Mac/Linux 上是 /
            candidates = sorted(
                image_path_candidates,
                key=lambda p: len(
                    os.path.relpath(
                        p,
                        start=md_file.parent
                    ).split(os.sep)
                )
            )

            
            image_file = candidates[0]

            print(
                f"⚠️ 发现同名图片，选择最近的："
                f"\n   {image_name}"
                f"\n   → {image_file}"
            )

        else:
            image_file = image_path_candidates[0]

        # make_relative_path() 函数用于计算图片相对于 Markdown 文件的相对路径，返回一个字符串，表示图片在 Markdown 文件中的链接路径
        relative_path = make_relative_path(
            md_file,
            image_file
        )

        # 图片 alt 使用文件名
        # stem 属性用于获取路径的文件名部分（不包含扩展名），例如 Path("/a/b/c.txt").stem 返回 "c"
        alt = Path(image_name).stem

        new_link = f"![{alt}]({relative_path})"

        print(
            f"\n{md_file.relative_to(ROOT)}"
            f"\n  {match.group(0)}"
            f"\n  ↓"
            f"\n  {new_link}"
        )

        return new_link

    # 正则找到一个符合的图片链接就调用一次replace_image()
    content = pattern.sub(replace_image, content)

    # 没有变化
    if content == original_content:
        return False

    # 预览模式
    if DRY_RUN:
        return True

    # 真正写入
    md_file.write_text(
        content,
        encoding="utf-8"
    )

    return True


# =========================
# 主程序
# =========================

def main():

    print("=" * 60)
    print("Obsidian 图片 Wiki Link → Markdown Link")
    print("=" * 60)

    print(f"\n仓库目录：{ROOT}")
    print(f"预览模式：{DRY_RUN}")

    print("\n正在扫描图片……")

    image_index = build_image_index()

    # sum() 函数用于计算所有图片路径列表的长度之和，即总共发现的图片数量
    total_images = sum(
        len(v)
        for v in image_index.values()
    )

    print(f"发现图片：{total_images} 张")

    # 找所有 Markdown
    markdown_files = []

    for path in ROOT.rglob("*.md"):

        if ".git" in path.parts:
            continue

        # 不处理脚本自己
        if path.name == "convert_images.py":
            continue

        markdown_files.append(path)

    print(f"发现 Markdown：{len(markdown_files)} 个")

    changed = 0

    print("\n开始扫描图片链接……")

    for md_file in markdown_files:

        if process_markdown(
            md_file,
            image_index
        ):
            changed += 1

    print("\n" + "=" * 60)

    if DRY_RUN:

        print(
            f"预览完成，共发现 {changed} 个需要修改的 Markdown 文件。"
        )

        print(
            "\n如果确认转换结果没有问题："
        )

        print(
            "把脚本中的："
        )

        print(
            "DRY_RUN = True"
        )

        print(
            "改成："
        )

        print(
            "DRY_RUN = False"
        )

        print(
            "\n然后重新执行："
        )

        print(
            "python3 convert_images.py"
        )

    else:

        print(
            f"转换完成，共修改 {changed} 个 Markdown 文件。"
        )


if __name__ == "__main__":
    main()
