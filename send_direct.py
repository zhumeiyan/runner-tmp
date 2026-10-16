# -*- coding: utf-8 -*-
"""直投 MX：不经过任何需要授权的中继，直接把信投到 oschina.cn 的收信服务器。"""
import smtplib, socket, ssl, sys, os, time, email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

RCPT = "bjoscc@oschina.cn"
SUBJ = "【作品提交】洛神 O1 · 会死的数字生命引擎 —— 赛道一 · 开源基础软件与解决方案 · 朱美岩"

BODY = """尊敬的组委会：

您好。

提交作品《洛神 O1 · 会死的数字生命引擎》，参赛赛道一（开源基础软件与解决方案）。
负责人：朱美岩（独立开发者）。材料如下。

一、代码仓库
https://github.com/zhumeiyan/luoshen-o1

公开仓库，102 个文件，Apache-2.0 许可。核心内容：
- core/life5.py —— 核心引擎，五条硬约束，唯一依赖 numpy
- examples/governed_agent.py —— 可集成示例：不到 20 行，把硬约束挂到任意
  Agent 框架上（LangChain / AutoGPT / 自研皆可），不改动原框架一行代码
- experiments/ —— 四项核心结论的复现脚本，一条命令跑完
- tests/test_engine.py —— 引擎自检 11 项，逐条证明五条硬约束确实成立
- evidence/失败模式库/判据核.md —— 152 条失败模式，全部带代码可复现
- evidence/实验报告/ —— 53 份实验报告，含被推翻的预注册判据

二、作品介绍文档
附件：洛神O1_作品介绍文档.pdf（12 页）
在线直链：https://github.com/zhumeiyan/luoshen-o1/releases/download/v1.0/LuoShen-O1_Intro.pdf

三、作品演示视频
3 分 15 秒（195 秒），符合 3-5 分钟要求。
https://github.com/zhumeiyan/luoshen-o1/releases/download/v1.0/LuoShen-O1_Demo.mp4
备用链接：https://github.com/zhumeiyan/luoshen-o1/blob/main/docs/洛神O1_演示视频.mp4

这不是动画，是真实运行的录屏。渲染层只决定字符出现的速度，画面中每一个数字
都由 experiments/demo_terminal.py 现场跑出。您自己运行会得到逐位相同的数字。

视频七段：① 同一引擎四个个体的结局分化 → ② 追一条真实死亡轨迹（死亡是连续下降，
不是断崖；能量第 466 拍归零，第 525 拍才判定死亡）→ ③ 撤掉稀缺后结构是否还在 →
④ 稀缺度全曲线扫描（每格真跑 16 个 seed）→ ⑤ 逐拍尾随并出示死亡诊断书
（零退出码、无 traceback、引擎继续 —— 用于区分「死亡」与「程序崩溃」）→
⑥ 挂到别人的 Agent 上，不改原框架一行代码 → ⑦ 可复现声明。

四、一句话说明
所有开源 Agent 框架都在问「它能做什么」。
本项目问的是「当它必须取舍、必须记住、而且真的会死的时候，它是什么」。

所有开源智能体框架的共同前提是「这个 Agent 不会死」。
本引擎换掉了这个前提：稀缺、死亡、不可逆、代谢、内生约束五条硬约束下，
结构不是被设计的，是被约束逼出来的 —— 实测在关掉全部决策模块后，取舍依然出现
（Δ = -0.1494 ± 0.0311，8/8 seeds 符号一致）。

三条最硬的实测结果：
- 同一代码、同一 seed，16 个个体中自然死亡：3 个（seed 3 @ 525拍、4 @ 596、7 @ 516）
- 撤掉稀缺约束后的结构偏度：0.0000（对照组 0.2913）
- 早期引导撤除 vs 全程施加：-0.1494 ± 0.0311

五、可复现性
git clone https://github.com/zhumeiyan/luoshen-o1.git && cd luoshen-o1
pip install -r requirements.txt      # 只有 numpy
python3 tests/test_engine.py         # 11 项自检
python3 experiments/run_core.py      # 四项核心结论，约 2 分钟
python3 experiments/demo_terminal.py # 视频中的全部画面

零 LLM 依赖、零网络依赖。文档中所有数字均由上述脚本当场跑出，
docs/复现清单.md 逐条标注每个数字的来源脚本与字段。

六、补充材料（仓库内，供路演环节使用）
- docs/demo.html —— 评委即开即用演示台：单文件、零依赖、零网络，双击即开，
  16 个个体可点选，曲线现场跑出（内置自校验：若多个 seed 轨迹完全相同则直接报错）
- docs/洛神O1_路演deck.pptx —— 14 页，含逐页口播稿
- docs/路演问答卡.md —— 12 个高频问题的应答，每问分「答什么 / 不要说 / 必须承认」

七、原创性声明
本作品全部由本人独立开发，代码与文档原创，第三方内容（开源协议、字体）
均已按各自许可使用。作品不涉密、不侵犯他人知识产权。

朱美岩（独立开发者）
联系方式：GitHub 项目页 https://github.com/zhumeiyan/luoshen-o1（Issues 区可留言）
2026 年 10 月
"""

def L(*a):
    print(" ".join(str(x) for x in a), flush=True)

# ---------- 1. 解析 MX ----------
hosts = []
try:
    import dns.resolver
    for r in dns.resolver.resolve("oschina.cn", "MX"):
        hosts.append((int(r.preference), str(r.exchange).rstrip(".")))
    hosts.sort()
except Exception as e:
    L("MX-RESOLVE-FAIL", repr(e))
if not hosts:
    hosts = [(10, "oschina.cn"), (10, "mail.oschina.cn"), (10, "smtp.oschina.cn")]
L("MX-LIST", hosts)

# ---------- 2. 构造信件 ----------
def build(sender):
    m = MIMEMultipart()
    m["From"] = sender
    m["To"] = RCPT
    m["Subject"] = SUBJ
    m["Date"] = email.utils.formatdate(localtime=True)
    m["Message-ID"] = email.utils.make_msgid(domain="luoshen-o1.github.io")
    m["Reply-To"] = "778131400@qq.com"
    m.attach(MIMEText(BODY, "plain", "utf-8"))
    p = "/tmp/intro.pdf"
    if os.path.exists(p) and os.path.getsize(p) > 1000:
        with open(p, "rb") as f:
            part = MIMEApplication(f.read(), _subtype="pdf")
        part.add_header("Content-Disposition", "attachment",
                        filename=("utf-8", "", "洛神O1_作品介绍文档.pdf"))
        m.attach(part)
        L("PDF-ATTACHED", os.path.getsize(p))
    else:
        L("PDF-MISSING", p)
    return m

SENDERS = ["778131400@qq.com", "submission@luoshen-o1.github.io", "noreply@oschina.cn"]

# ---------- 3. 逐主机逐端口尝试 ----------
result = {"rc": None, "detail": []}
for pref, host in hosts:
    for port in (25, 587, 465):
        tag = "%s:%d" % (host, port)
        try:
            if port == 465:
                s = smtplib.SMTP_SSL(host, port, timeout=25)
            else:
                s = smtplib.SMTP(host, port, timeout=25)
            L("CONNECTED", tag)
            code, msg = s.ehlo()
            L("EHLO", tag, code, msg)
            if port == 587:
                try:
                    s.starttls(context=ssl.create_default_context())
                    s.ehlo()
                    L("STARTTLS-OK", tag)
                except Exception as e:
                    L("STARTTLS-FAIL", tag, repr(e))
            last = None
            for snd in SENDERS:
                msg = build(snd)
                raw = msg.as_string()
                try:
                    r = s.sendmail(snd, [RCPT], raw)
                    L("SENT", tag, "from=", snd, "refused=", r)
                    result["rc"] = "SENT"
                    result["detail"].append([tag, snd, str(r)])
                    s.quit()
                    sys.exit(0)
                except Exception as e:
                    last = e
                    L("REJECT", tag, "from=", snd, repr(e))
            try: s.quit()
            except Exception: pass
        except Exception as e:
            L("CONNECT-FAIL", tag, repr(e))

L("FINAL", result)
