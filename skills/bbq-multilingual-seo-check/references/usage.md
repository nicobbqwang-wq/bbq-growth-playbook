# Run and interpret / 运行与解释

From the repository root (Python 3.9+, no third-party dependencies):

```sh
python3 skills/bbq-multilingual-seo-check/scripts/check.py \
  --url https://bbqgrowthlab.com/zh-cn/services/ \
  --url https://bbqgrowthlab.com/en/services/ \
  --sitemap https://bbqgrowthlab.com/sitemap.xml \
  --output seo-report.json
```

This sends public GET requests. Use your own URLs for your audit. Default maximum 70 requests, at most 20 seed pages and 20 sitemap documents; each response max 5 MB, timeout 15s. Cached URLs are not requested twice. Cross-origin targets are unknown unless their origin was explicitly supplied as a seed or sitemap. No browser or model integration is required.

The JSON includes requested/final URL, HTTP status, response SHA-256, extracted canonical/hreflang/html-lang, target and return-link evidence, sitemap completeness, pass/review/fail/unknown per check. Original requested redirects remain visible. Report files can be inspected without extra software.

中文：在仓库根目录运行上面命令。把 --url 换为自有页面的中英文配对，用 --sitemap 指定真实地图。输出是证据报告；review 表示需要人工查看，unknown 表示未判定，不等于故障。canonical 是页面声明的首选地址；hreflang 是语言版本对应关系。脚本检查目标状态、目标声明语言和返回链接，并对照 sitemap。

Limits: no JavaScript rendering, HTTP Link header annotations or XML hreflang extensions; no content-language detector, translation/semantic-equivalence judgment, robots/noindex/indexing/rankings. Regions can validly fall back to a broader language. Absence from sitemap may be intentional. HTML base elements require manual URL resolution review. Network errors or limited sitemap traversal produce unknown membership, not a missing-page verdict. The script handles sitemap indexes but not compressed .gz sitemaps. It does not make requests to model APIs or alter the website.

[Google's localized-page documentation](https://developers.google.com/search/docs/specialty/international/localized-versions) explains HTML, HTTP and sitemap annotation options. This tool checks only the declared subset above and is not a search-engine validator. Checked 2026-09-15.
