## maven依赖命令行工具箱
### 命令行搜索maven依赖，可直接复制搜索结果到pom.xml里。
#### 下载安装
- 下载源码 `git clone https://github.com/zshnb/maven-saber.git`
- 安装依赖
  - 需要python3以及pip环境
  - 进入程序目录 `cd maven-saver`
  - 安装依赖 `sudo pip install -r requirements.txt`
- 命令格式：
  - Linux: `./saber.sh -artifact artifactId [-repo aliyun] [-ac] [-asc] [-limit 5]`
  - Windows: `python cli.py -artifact artifactId [-repo aliyun] [-ac] [-asc] [-limit 5]`
- 命令常用参数：
参数名|描述|是否可选|默认值
-----|---|-------|----
-artifact|依赖的artifactId|否|
-ac|是否精确匹配artifactId|是|否|模糊
-asc|按照version的排序顺序|是|降序
-limit|返回依赖数量|是|5
-repo|查询依赖的依赖仓库|是|sonatype

- 提示：可以使用下面的代理池，以避免本机ip查找过于频繁而被拉黑名单
  ```shell script
  docker pull jhao104/proxy_pool
  docker run --env db_type=REDIS --env db_host=x.x.x.x --env db_port=6379 --env db_password=pwd_str -p 5010:5010 jhao104/proxy_pool
  ```
  等待容器运行成功，访问 127.0.0.1:5010/get 验证，查看是否能访问。

