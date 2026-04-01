# ossutil 2.0 安装（按平台）

> 请优先使用官方文档中的最新地址。历史路径（例如 `/ossutil/2.2.0/...`）可能返回 404。

## Linux

```bash
if command -v yum >/dev/null 2>&1; then
  sudo yum install -y unzip
else
  sudo apt-get update && sudo apt-get install -y unzip
fi
curl -fL -o ossutil.zip https://gosspublic.alicdn.com/ossutil/v2/2.2.1/ossutil-2.2.1-linux-amd64.zip
unzip ossutil.zip
sudo chmod 755 ossutil-2.2.1-linux-amd64/ossutil
sudo mv ossutil-2.2.1-linux-amd64/ossutil /usr/local/bin/ossutil
ossutil version
```

## macOS

```bash
curl -fL -o ossutil.zip https://gosspublic.alicdn.com/ossutil/v2/2.2.1/ossutil-2.2.1-darwin-amd64.zip
unzip ossutil.zip
sudo chmod 755 ossutil-2.2.1-darwin-amd64/ossutil
sudo mv ossutil-2.2.1-darwin-amd64/ossutil /usr/local/bin/ossutil
ossutil version
```

## Windows

- 下载对应平台压缩包并解压。
- 将 `ossutil.exe` 所在目录加入系统 `PATH`。
- 在 PowerShell/CMD 中运行 `ossutil version` 验证安装。
