This document introduces the field names and their meanings returned when calling ESA data analysis APIs. These fields are data analysis results obtained through API calls, used to support deeper data analysis and business insights. Through these fields, you can get detailed traffic, requests, cache status, and other information to comprehensively understand business performance and system operation status.

## **Metrics**

Data analysis provides you with rich data metric values, including response traffic, request count, request traffic, page views, etc. These metrics can comprehensively show your business performance and help you deeply understand business activity, traffic distribution, user behavior patterns, and system performance. Through these detailed data analyses, you can more accurately evaluate business operation status, timely discover potential issues, and formulate corresponding optimization strategies to improve user experience and business efficiency.

| **Field Name** | **Data Type** | **Description** |
| --- | --- | --- |
| Traffic | int | Size of ESA node response returned to client, unit: Byte |
| Requests | int | Number of requests |
| RequestTraffic | int | Size of client request, unit: Byte |
| PageView | int | Page views |

## **Dimensions**

Data analysis provides multiple dimensions for data metrics, helping you analyze business performance from different angles. Helps you comprehensively understand traffic geographic distribution, user behavior patterns, request details, cache status, and system performance. Multi-dimensional data analysis not only helps optimize business processes and improve user experience, but also helps you quickly locate issues and formulate targeted solutions to better manage business operations.

| **Field Name** | **Description** |
| --- | --- |
| ALL | User dimension full data |
| ClientASN | [Autonomous System Number (ASN)](https://help.aliyun.com/zh/edge-security-acceleration/esa/support/what-is-asn) information parsed from client IP address |
| ClientBrowser | Client browser type |
| ClientCountryCode | `ISO-3166 Alpha-2 Code` parsed from client IP address |
| ClientDevice | Client device type |
| ClientIP | Client IP that established connection with ESA node |
| ClientIPVersion | Client IP version that established connection with ESA node |
| ClientISP | ISP information parsed from client IP address |
| ClientOS | Client system model |
| ClientProvinceCode | China mainland province information parsed from client IP address |
| ClientRequestHost | Client request `Host` information |
| ClientRequestMethod | Client request `HTTP Method` information |
| ClientRequestPath | Client request path information |
| ClientRequestProtocol | Client request protocol information |
| ClientRequestQuery | Client request `Query` information |
| ClientRequestReferer | Client request `Referer` information |
| ClientRequestUserAgent | Client request `User-Agent` information |
| ClientSSLProtocol | Client SSL protocol version, `-` indicates no SSL used |
| ClientXRequestedWith | Client `X-Requested-With` request header |
| EdgeCacheStatus | Cache status of client request |
| EdgeResponseContentType | `Content-Type` information of ESA node response |
| EdgeResponseStatusCode | Status code returned by ESA node response to client |
| OriginResponseStatusCode | Origin response status code |
| SiteId | Current site ID |
| Version | Version management version number |
