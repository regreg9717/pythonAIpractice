# 爬取 doc.hnumi.com 大数据学习知识点
import requests
import csv
from lxml import html

BASE_URL = "https://doc.hnumi.com"
START_URL = BASE_URL + "/"

# ==================== 通用工具 ====================

def get_tree(url):
    """请求页面并返回 lxml ElementTree 对象"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    resp = requests.get(url, headers=headers, timeout=20)
    resp.encoding = resp.apparent_encoding
    return html.fromstring(resp.text)


def text(node):
    """提取节点内每个文本段拼接并用空格分隔"""
    frags = [t.strip() for t in node.itertext() if t.strip()]
    return " ".join(frags)


# ==================== 爬取逻辑 ====================

def get_nav_links(tree):
    """
    从首页/导航栏解析：大数据学习 相关的子页面链接
    如果实际页面结构不同，可调整下方的 XPath
    """
    links = []
    # 常见侧边栏 / 目录结构：
    #   <nav> <ul> <li> <a href="...">大数据学习</a>
    # 可能有多层嵌套，需要根据实际 HTML 调整 XPath
    for a in tree.xpath(
        '//nav//a[@href]'
        ' | //aside//a[@href]'
        ' | //div[contains(@class,"sidebar")]//a[@href]'
    ):
        title = text(a)
        href = a.get("href", "").strip()
        if not href or not title:
            continue
        # 将相对路径转为绝对路径
        if href.startswith("/"):
            href = BASE_URL + href
        elif not href.startswith("http"):
            href = BASE_URL + "/" + href
        # 如果导航标签没有明显的大数据标识，可以先全量爬取再过滤
        links.append((title, href))
    return links


def parse_article(url, title):
    """爬取单个文章页面的知识点内容，返回字典"""
    tree = get_tree(url)

    # ---- 根据实际页面结构调整 XPath ----
    # 常见文章容器：<article>, <main>, <div class="content">, <div class="markdown-body"> 等
    article = tree.xpath(
        '//article'
        ' | //main'
        ' | //div[contains(@class,"content")]'
        ' | //div[contains(@class,"markdown-body")]'
    )
    if article:
        content_node = article[0]
    else:
        content_node = tree  # 兜底用整页

    # 提取所有标题
    headings = []
    for h in content_node.xpath(
        './/h1 | .//h2 | .//h3'
    ):
        headings.append({
            "level": h.tag,          # h1 / h2 / h3
            "title": text(h),
        })

    # 提取全文文本
    full_text = text(content_node)

    # 提取代码块（如果有）
    codes = []
    for pre in content_node.xpath('.//pre//code | .//pre'):
        codes.append(text(pre))

    return {
        "page_title": title,
        "url": url,
        "headings": [h["title"] for h in headings],
        "content": full_text[:2000],  # 截取前2000字符作为摘要
        "code_blocks": codes,
    }


def crawl():
    """主入口：依次爬取所有子页面，写入 CSV"""
    print("正在请求首页:", START_URL)
    tree = get_tree(START_URL)
    nav_links = get_nav_links(tree)

    # 过滤只保留与 "大数据" 相关的页面（按需调整关键词）
    target_links = [
        (t, u) for t, u in nav_links
        if any(kw in t for kw in ["大数据", "Spark", "Hadoop", "Flink",
                                    "Hive", "HBase", "Kafka", "数仓",
                                    "数据湖", "ETL", "MapReduce"])
    ]
    if not target_links:
        # 如果过滤后为空，保留所有链接
        print("未匹配到大数据关键词，将爬取全部导航链接")
        target_links = nav_links

    print(f"共解析到 {len(target_links)} 个目标页面")

    results = []
    for idx, (title, url) in enumerate(target_links, 1):
        print(f"[{idx}/{len(target_links)}] 正在爬取: {title}")
        try:
            data = parse_article(url, title)
            results.append(data)
        except Exception as e:
            print(f"  !! 爬取失败: {e}")
            results.append({
                "page_title": title,
                "url": url,
                "headings": [],
                "content": f"[错误] {e}",
                "code_blocks": [],
            })

    # 写入 CSV
    csv_path = "bigdata_knowledge.csv"
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["页面标题", "URL", "知识点标题", "内容摘要", "代码块"])
        for r in results:
            headings_str = " | ".join(r["headings"])
            codes_str = "\n---\n".join(r["code_blocks"])
            writer.writerow([
                r["page_title"],
                r["url"],
                headings_str,
                r["content"],
                codes_str,
            ])

    print(f"\n完成！共爬取 {len(results)} 个页面，结果保存至: {csv_path}")


if __name__ == "__main__":
    crawl()
