#!/usr/bin/env python3
"""
ESA 数据分析统一查询脚本

支持所有维度和指标的灵活查询。

使用前请配置凭证:
  export ALIBABA_CLOUD_ACCESS_KEY_ID="your-ak"
  export ALIBABA_CLOUD_ACCESS_KEY_SECRET="your-sk"

示例:
  # 查询 Top 维度数据
  python query_analytics.py --dimension ClientCountryCode --metric Traffic
  python query_analytics.py --dimension EdgeResponseStatusCode --metric Requests
  python query_analytics.py --dimension ClientRequestHost --metric Traffic,Requests

  # 查询时序数据
  python query_analytics.py --time-series --metric Traffic,Requests

  # 指定时间范围
  python query_analytics.py --dimension ClientIP --metric Requests --hours 72

  # 列出可用维度和指标
  python query_analytics.py --list-dimensions
  python query_analytics.py --list-metrics
"""

import os
import sys
import json
import argparse
import configparser
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Dict, Any

from alibabacloud_esa20240910.client import Client as EsaClient
from alibabacloud_esa20240910 import models as esa_models
from alibabacloud_tea_openapi import models as open_api_models


# ============================================================================
# 维度和指标定义 (来自 field.md)
# ============================================================================

METRICS = {
    "Traffic": "ESA 节点响应返回给客户端的大小，单位：Byte",
    "Requests": "请求数",
    "RequestTraffic": "客户端请求的大小，单位：Byte",
    "PageView": "页面浏览量",
}

DIMENSIONS = {
    "ALL": "用户维度全量数据",
    "ClientASN": "从客户端 IP 地址解析出的自治系统编号（ASN）信息",
    "ClientBrowser": "客户端浏览器类型",
    "ClientCountryCode": "从客户端 IP 地址解析出的 ISO-3166 Alpha-2 Code",
    "ClientDevice": "客户端设备类型",
    "ClientIP": "与 ESA 节点建立连接的客户端 IP",
    "ClientIPVersion": "与 ESA 节点建立连接的客户端 IP 版本",
    "ClientISP": "从客户端 IP 地址解析出的运营商信息",
    "ClientOS": "客户端系统型号",
    "ClientProvinceCode": "从客户端 IP 地址解析出的中国内地省份信息",
    "ClientRequestHost": "客户端请求的 Host 信息",
    "ClientRequestMethod": "客户端请求的 HTTP Method 信息",
    "ClientRequestPath": "客户端请求的路径信息",
    "ClientRequestProtocol": "客户端请求的协议信息",
    "ClientRequestQuery": "客户端请求的 Query 信息",
    "ClientRequestReferer": "客户端请求的 Referer 信息",
    "ClientRequestUserAgent": "客户端请求的 User-Agent 信息",
    "ClientSSLProtocol": "客户端的 SSL 协议版本，- 表示没有使用 SSL",
    "ClientXRequestedWith": "客户端携带的 X-Requested-With 请求头",
    "EdgeCacheStatus": "客户端请求的缓存状态",
    "EdgeResponseContentType": "ESA 节点响应的 Content-Type 信息",
    "EdgeResponseStatusCode": "ESA 节点响应返回给客户端的状态码",
    "OriginResponseStatusCode": "源站响应状态码",
    "SiteId": "当前站点的 ID",
    "Version": "版本管理的版本号",
}

# 缓存状态说明
CACHE_STATUS_INFO = {
    "HIT": "缓存命中 - 请求直接从 ESA 边缘节点缓存返回",
    "MISS": "缓存未命中 - 请求需要回源获取内容",
    "STALE": "过期缓存 - 返回过期缓存内容（源站不可用时）",
    "EXPIRED": "缓存过期 - 缓存已过期，需要重新验证",
    "BYPASS": "绕过缓存 - 请求绕过缓存",
    "UPDATING": "更新中 - 缓存正在后台更新",
    "REVALIDATED": "重新验证 - 源站确认缓存仍然有效",
    "DYNAMIC": "动态内容 - 不进行缓存",
    "NONE": "无缓存状态 - 请求未触发缓存逻辑",
}

# HTTP 状态码说明
STATUS_CODE_INFO = {
    200: "OK - 请求成功",
    201: "Created - 资源创建成功",
    204: "No Content - 无内容返回",
    206: "Partial Content - 部分内容",
    301: "Moved Permanently - 永久重定向",
    302: "Found - 临时重定向",
    304: "Not Modified - 未修改",
    307: "Temporary Redirect - 临时重定向",
    308: "Permanent Redirect - 永久重定向",
    400: "Bad Request - 请求格式错误",
    401: "Unauthorized - 未授权",
    403: "Forbidden - 禁止访问",
    404: "Not Found - 资源未找到",
    405: "Method Not Allowed - 方法不允许",
    408: "Request Timeout - 请求超时",
    429: "Too Many Requests - 请求过多",
    500: "Internal Server Error - 服务器内部错误",
    502: "Bad Gateway - 网关错误",
    503: "Service Unavailable - 服务不可用",
    504: "Gateway Timeout - 网关超时",
    522: "Connection Timed Out - 连接超时",
    524: "A Timeout Occurred - 发生超时",
}


# ============================================================================
# ESA 客户端
# ============================================================================

def create_client() -> EsaClient:
    """创建 ESA 客户端"""
    access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
    access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")

    if not access_key_id or not access_key_secret:
        cred_path = os.path.expanduser("~/.alibabacloud/credentials")
        if os.path.exists(cred_path):
            parser = configparser.ConfigParser()
            parser.read(cred_path)
            if "default" in parser:
                access_key_id = parser.get("default", "access_key_id", fallback=None)
                access_key_secret = parser.get("default", "access_key_secret", fallback=None)

    if not access_key_id or not access_key_secret:
        print("错误: 请配置凭证", file=sys.stderr)
        print("  export ALIBABA_CLOUD_ACCESS_KEY_ID='your-ak'", file=sys.stderr)
        print("  export ALIBABA_CLOUD_ACCESS_KEY_SECRET='your-sk'", file=sys.stderr)
        sys.exit(1)

    config = open_api_models.Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        region_id=os.environ.get("ALIBABA_CLOUD_REGION_ID", "cn-hangzhou"),
        endpoint="esa.cn-hangzhou.aliyuncs.com",
    )
    return EsaClient(config)


def list_sites(client: EsaClient) -> List:
    """列出所有站点"""
    resp = client.list_sites(esa_models.ListSitesRequest(
        page_number=1,
        page_size=50,
    ))
    return resp.body.sites or []


def select_site(sites: List, site_id: Optional[str] = None) -> Any:
    """选择站点"""
    if site_id:
        for site in sites:
            if str(site.site_id) == site_id:
                return site
        print(f"错误: 未找到站点 ID: {site_id}", file=sys.stderr)
        sys.exit(1)

    if len(sites) == 1:
        return sites[0]

    print("\n站点列表:")
    for i, site in enumerate(sites, 1):
        print(f"  {i}. {site.site_name} (ID: {site.site_id}, 状态: {site.status})")

    try:
        choice = int(input("\n请选择站点编号: "))
        if 1 <= choice <= len(sites):
            return sites[choice - 1]
    except (ValueError, EOFError):
        pass

    print("错误: 无效选择", file=sys.stderr)
    sys.exit(1)


# ============================================================================
# 查询函数
# ============================================================================

def query_top_data(
    client: EsaClient,
    site_id: str,
    dimension: str,
    metrics: List[str],
    hours: int = 24,
    limit: int = 150
):
    """查询 Top 数据"""
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours)

    fields = [
        esa_models.DescribeSiteTopDataRequestFields(
            field_name=metric,
            dimension=[dimension]
        )
        for metric in metrics
    ]

    resp = client.describe_site_top_data(
        esa_models.DescribeSiteTopDataRequest(
            site_id=site_id,
            start_time=start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            end_time=end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            fields=fields,
            limit=str(limit)
        )
    )

    return resp.body, start_time, end_time


def query_time_series(
    client: EsaClient,
    site_id: str,
    metrics: List[str],
    dimension: str = "ALL",
    hours: int = 24
):
    """查询时序数据"""
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours)

    # 根据时间范围选择时间粒度
    if hours <= 3:
        interval = "60"
    elif hours <= 12:
        interval = "300"
    elif hours <= 24:
        interval = "900"
    else:
        interval = "3600"

    fields = [
        esa_models.DescribeSiteTimeSeriesDataRequestFields(
            field_name=metric,
            dimension=[dimension]
        )
        for metric in metrics
    ]

    resp = client.describe_site_time_series_data(
        esa_models.DescribeSiteTimeSeriesDataRequest(
            site_id=site_id,
            start_time=start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            end_time=end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            interval=interval,
            fields=fields
        )
    )

    return resp.body, start_time, end_time


# ============================================================================
# 格式化输出
# ============================================================================

def format_bytes(value: int) -> str:
    """格式化字节数"""
    if value >= 1024 * 1024 * 1024:
        return f"{value / (1024*1024*1024):.2f} GB"
    elif value >= 1024 * 1024:
        return f"{value / (1024*1024):.2f} MB"
    elif value >= 1024:
        return f"{value / 1024:.2f} KB"
    return f"{value} B"


def format_number(value: int) -> str:
    """格式化数字"""
    return f"{value:,}"


def get_dimension_display(dimension: str, value: str) -> str:
    """获取维度值的显示文本"""
    if dimension == "EdgeCacheStatus":
        return f"{value} - {CACHE_STATUS_INFO.get(value.upper(), '')}"
    if dimension == "EdgeResponseStatusCode":
        try:
            code = int(value)
            return f"{value} - {STATUS_CODE_INFO.get(code, '')}"
        except ValueError:
            return value
    return value


# ============================================================================
# 打印结果
# ============================================================================

def print_top_data(result, dimension: str, metrics: List[str], start_time, end_time, top_n: int = 20):
    """打印 Top 数据"""
    print(f"\n{'='*80}")
    print(f"Top {DIMENSIONS.get(dimension, dimension)} 分析")
    print(f"时间范围: {start_time.strftime('%Y-%m-%d %H:%M')} - {end_time.strftime('%Y-%m-%d %H:%M')} UTC")
    print(f"采样率: {result.sampling_rate}%")
    print(f"{'='*80}\n")

    if not result.data:
        print("暂无数据")
        return {}

    # 解析数据
    data_by_dimension = {}
    for item in result.data:
        if not item.detail_data:
            continue
        for p in item.detail_data:
            key = p.dimension_value
            if key not in data_by_dimension:
                data_by_dimension[key] = {}
            data_by_dimension[key][item.field_name] = p.value

    if not data_by_dimension:
        print("暂无数据")
        return {}

    # 计算总数用于百分比
    totals = {metric: 0 for metric in metrics}
    for values in data_by_dimension.values():
        for metric in metrics:
            totals[metric] += values.get(metric, 0)

    # 按第一个指标排序
    primary_metric = metrics[0]
    sorted_data = sorted(
        data_by_dimension.items(),
        key=lambda x: x[1].get(primary_metric, 0),
        reverse=True
    )

    # 打印表头
    header = f"{'Rank':<6}{dimension[:30]:<32}"
    for metric in metrics:
        if metric == "Traffic":
            header += f"{metric:>14}"
        else:
            header += f"{metric:>12}"
    header += f"{'%':>8}"
    print(header)
    print("-" * 80)

    # 打印数据
    for i, (key, values) in enumerate(sorted_data[:top_n], 1):
        # 显示值
        display_key = key[:30] + ".." if len(key) > 32 else key
        row = f"#{i:<5}{display_key:<32}"

        for metric in metrics:
            val = values.get(metric, 0)
            if metric == "Traffic":
                row += f"{format_bytes(val):>14}"
            else:
                row += f"{format_number(val):>12}"

        # 百分比（基于第一个指标）
        primary_val = values.get(primary_metric, 0)
        total = totals.get(primary_metric, 1)
        percentage = (primary_val / total * 100) if total > 0 else 0
        row += f"{percentage:>7.1f}%"

        print(row)

    if len(sorted_data) > top_n:
        print(f"\n  ... 还有 {len(sorted_data) - top_n} 条数据")

    # 打印汇总
    print(f"\n汇总:")
    for metric in metrics:
        val = totals.get(metric, 0)
        if metric == "Traffic":
            print(f"  总{metric}: {format_bytes(val)}")
        else:
            print(f"  总{metric}: {format_number(val)}")

    return data_by_dimension


def print_time_series(result, metrics: List[str], start_time, end_time):
    """打印时序数据"""
    print(f"\n{'='*80}")
    print(f"时序数据分析")
    print(f"时间范围: {start_time.strftime('%Y-%m-%d %H:%M')} - {end_time.strftime('%Y-%m-%d %H:%M')} UTC")
    print(f"采样率: {result.sampling_rate}%")
    print(f"{'='*80}\n")

    if not result.data:
        print("暂无数据")
        return

    for item in result.data:
        if not item.detail_data:
            continue

        metric = item.field_name
        values = [p.value for p in item.detail_data if p.value is not None]

        if not values:
            continue

        print(f"\n{metric} 趋势:")
        print("-" * 50)

        if metric == "Traffic":
            print(f"  总计: {format_bytes(sum(values))}")
            print(f"  平均: {format_bytes(sum(values)/len(values))}")
            print(f"  最大: {format_bytes(max(values))}")
            print(f"  最小: {format_bytes(min(values))}")
        else:
            print(f"  总计: {format_number(sum(values))}")
            print(f"  平均: {format_number(int(sum(values)/len(values)))}")
            print(f"  最大: {format_number(max(values))}")
            print(f"  最小: {format_number(min(values))}")

        # 打印最近数据点
        print(f"\n  最近数据点:")
        for point in item.detail_data[-10:]:
            ts = point.time_stamp.replace("T", " ").replace("Z", "")
            if metric == "Traffic":
                print(f"    {ts}  {format_bytes(point.value)}")
            else:
                print(f"    {ts}  {format_number(point.value)}")


# ============================================================================
# 导出数据
# ============================================================================

def export_data(data: Dict, site_info: Dict, args, filename_prefix: str):
    """导出数据到 JSON 文件"""
    output_dir = "output/esa-analytics"
    os.makedirs(output_dir, exist_ok=True)

    output_file = f"{output_dir}/{filename_prefix}_{site_info['site_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    export_data = {
        "site_id": site_info["site_id"],
        "site_name": site_info["site_name"],
        "query": {
            "dimension": args.dimension,
            "metrics": args.metric.split(","),
            "hours": args.hours,
        },
        "start_time": site_info.get("start_time"),
        "end_time": site_info.get("end_time"),
        "data": data
    }

    with open(output_file, "w") as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)

    print(f"\n结果已保存到: {output_file}")


# ============================================================================
# 主函数
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="ESA 数据分析统一查询脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --dimension ClientCountryCode --metric Traffic
  %(prog)s --dimension EdgeResponseStatusCode --metric Requests
  %(prog)s --dimension ClientRequestHost --metric Traffic,Requests
  %(prog)s --time-series --metric Traffic,Requests
  %(prog)s --list-dimensions
  %(prog)s --list-metrics
        """
    )

    # 查询类型
    parser.add_argument("--time-series", action="store_true",
                        help="查询时序数据（默认查询 Top 数据）")

    # 查询参数
    parser.add_argument("-d", "--dimension", type=str,
                        help=f"查询维度，可选: {', '.join(DIMENSIONS.keys())}")
    parser.add_argument("-m", "--metric", type=str, default="Traffic",
                        help="查询指标，多个用逗号分隔，默认: Traffic")
    parser.add_argument("--hours", type=int, default=24,
                        help="查询时间范围（小时），默认: 24")
    parser.add_argument("--limit", type=int, default=150,
                        help="Top 数据返回数量，默认: 150")
    parser.add_argument("--top-n", type=int, default=20,
                        help="显示 Top N 条数据，默认: 20")
    parser.add_argument("--site-id", type=str,
                        help="站点 ID，不指定则交互选择")

    # 列出可用选项
    parser.add_argument("--list-dimensions", action="store_true",
                        help="列出所有可用维度")
    parser.add_argument("--list-metrics", action="store_true",
                        help="列出所有可用指标")

    args = parser.parse_args()

    # 列出维度
    if args.list_dimensions:
        print("可用维度:")
        for dim, desc in DIMENSIONS.items():
            print(f"  {dim:<30} {desc}")
        return

    # 列出指标
    if args.list_metrics:
        print("可用指标:")
        for metric, desc in METRICS.items():
            print(f"  {metric:<20} {desc}")
        return

    # 验证参数
    if not args.time_series and not args.dimension:
        parser.error("查询 Top 数据需要指定 --dimension 参数")

    if args.dimension and args.dimension not in DIMENSIONS:
        print(f"错误: 无效的维度 '{args.dimension}'", file=sys.stderr)
        print(f"可用维度: {', '.join(DIMENSIONS.keys())}", file=sys.stderr)
        sys.exit(1)

    metrics = [m.strip() for m in args.metric.split(",")]
    for m in metrics:
        if m not in METRICS:
            print(f"错误: 无效的指标 '{m}'", file=sys.stderr)
            print(f"可用指标: {', '.join(METRICS.keys())}", file=sys.stderr)
            sys.exit(1)

    # 创建客户端
    client = create_client()

    # 获取站点
    print("正在获取站点列表...")
    sites = list_sites(client)

    if not sites:
        print("未找到任何站点", file=sys.stderr)
        sys.exit(1)

    site = select_site(sites, args.site_id)
    print(f"已选择站点: {site.site_name}")

    # 查询数据
    if args.time_series:
        print(f"\n正在查询时序数据 ({args.metric})...")
        result, start_time, end_time = query_time_series(
            client, site.site_id, metrics, hours=args.hours
        )
        print_time_series(result, metrics, start_time, end_time)

        # 导出
        result_data = {
            "metrics": {},
        }
        for item in result.data:
            if item.detail_data:
                result_data["metrics"][item.field_name] = [
                    {"timestamp": p.time_stamp, "value": p.value}
                    for p in item.detail_data
                ]

        export_data(result_data, {
            "site_id": str(site.site_id),
            "site_name": site.site_name,
            "start_time": start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "end_time": end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }, args, "time_series")
    else:
        print(f"\n正在查询 Top {args.dimension} ({args.metric})...")
        result, start_time, end_time = query_top_data(
            client, site.site_id, args.dimension, metrics,
            hours=args.hours, limit=args.limit
        )
        data = print_top_data(result, args.dimension, metrics, start_time, end_time, top_n=args.top_n)

        # 导出
        export_list = [
            {"dimension_value": k, **v}
            for k, v in data.items()
        ]
        export_data(export_list, {
            "site_id": str(site.site_id),
            "site_name": site.site_name,
            "start_time": start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "end_time": end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }, args, f"top_{args.dimension.lower()}")


if __name__ == "__main__":
    main()