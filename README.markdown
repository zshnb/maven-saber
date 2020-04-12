### maven依赖命令行工具箱
- 命令行搜索maven依赖，可直接复制搜索结果到pom.xml里。
  - 命令格式：`python cli.py -artifact artifactId -a`
  - 使用前的准备：首先使用docker运行下面的代理池容器。
      ```shell script
      docker pull jhao104/proxy_pool
      docker run --env db_type=REDIS --env db_host=x.x.x.x --env db_port=6379 --env db_password=pwd_str -p 5010:5010 jhao104/proxy_pool
      ```
    等待容器运行成功，访问 127.0.0.1:5010/get 验证，查看是否能访问。
  - 命令常用参数：
    参数名|描述
    -----|---
    -artifact|依赖的artifactId
    -a|是否精确匹配artifactId
    
  