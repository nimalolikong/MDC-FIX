# 基于官方 code-server 镜像
FROM codercom/code-server:latest

USER root

# 安装 Python3.11、构建依赖、Firefox 与 geckodriver（尽量使用 apt 包），以及常见系统库（face_recognition 需要编译依赖）
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
       build-essential cmake git wget unzip curl pkg-config net-tools \
       ca-certificates apt-transport-https software-properties-common \
       libdbus-glib-1-2 libgtk-3-0 libx11-xcb1 libxtst6 libxrandr2 libasound2 \
       libxcomposite1 libxdamage1 libxfixes3 libxrender1 libnss3 libxss1 libxi6 \
       libglib2.0-0 libdrm2 libgbm1 libpci3 libgl1-mesa-dri libgl1-mesa-glx libegl1 \
       libxcb-glx0 fonts-liberation fonts-dejavu-core fonts-noto-color-emoji \
       python3 python3-venv python3-pip python3-dev firefox-esr xvfb 

RUN apt-get clean && rm -rf /var/lib/apt/lists/* 

# 安装 geckodriver 最新版
RUN GECKO_VER=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep "tag_name" | cut -d '"' -f4) && \
    wget -qO /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/${GECKO_VER}/geckodriver-${GECKO_VER}-linux64.tar.gz && \
    tar -C /usr/bin -xzf /tmp/geckodriver.tar.gz && \
    rm /tmp/geckodriver.tar.gz && chmod +x /usr/bin/geckodriver

RUN firefox --version && geckodriver --version



# 升级 pip 并安装 Python 库（Selenium4 + face_recognition 等）
# face_recognition 依赖 dlib，可能会编译较久；如在 QNAP/ARM 上编译失败，请参考说明使用预编译包或在宿主机预编译 wheel
RUN pip3 install --no-cache-dir --break-system-packages --upgrade pip


RUN pip3 install --no-cache-dir --break-system-packages  cloudscraper==1.2.71 face_recognition==1.3.0 lxml==4.9.3 MechanicalSoup==1.3.0 \
    opencc_python_reimplemented==0.1.7 Pillow==11.3.0 Requests==2.32.5 selenium==4.26.1 urllib3==1.26.13 dlib==19.24.6

# （可选）在镜像构建时安装你常用的 VS Code 扩展
# 例如安装 Python 插件、Remote - SSH 等；以 root 身份调用 code-server CLI，然后修正权限
# 你可以在这里添加更多 `--install-extension` 命令
RUN /usr/bin/code-server --install-extension ms-python.python --install-extension ms-toolsai.jupyter || true

# 修正 /home/coder 的权限（官方镜像用户为 coder）
RUN chown -R 1000:1000 /home/coder || true

# 切回非 root（code-server 官方镜像以用户 coder 启动）
USER coder

# 保持默认 entrypoint / cmd（使用官方镜像的行为）

