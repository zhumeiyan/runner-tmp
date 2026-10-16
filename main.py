# -*- coding: utf-8 -*-
import sys, os as _os, ssl, smtplib, traceback, urllib.request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header
from email.utils import formataddr, formatdate

arg = sys.argv[1] if len(sys.argv) > 1 else ""
USER, sep, PWD = arg.partition(":::")
open("/tmp/user.txt", "w").write("ok 1")

TO = "bjoscc@oschina.cn"
SUBJ = "【作品提交】洛神 O1 · 会死的数字生命引擎 —— 赛道一 · 开源基础软件与解决方案 · 朱美岩"
PDF = "https://github.com/zhumeiyan/luoshen-o1/releases/download/v1.0/LuoShen-O1_Intro.pdf"

BODY = """\u5c0a\u656c\u7684\u7ec4\u59d4\u4f1a\uff1a

\u60a8\u597d\u3002

\u63d0\u4ea4\u4f5c\u54c1\u300a\u6d1b\u795e O1 \u00b7 \u4f1a\u6b7b\u7684\u6570\u5b57\u751f\u547d\u5f15\u64ce\u300b\uff0c\u53c2\u8d5b\u8d5b\u9053\u4e00\uff08\u5f00\u6e90\u57fa\u7840\u8f6f\u4ef6\u4e0e\u89e3\u51b3\u65b9\u6848\uff09\u3002
\u8d1f\u8d23\u4eba\uff1a\u6731\u7f8e\u5ca9\uff08\u72ec\u7acb\u5f00\u53d1\u8005\uff09\u3002\u6750\u6599\u5982\u4e0b\u3002


\u4e00\u3001\u4ee3\u7801\u4ed3\u5e93

https://github.com/zhumeiyan/luoshen-o1

\u516c\u5f00\u4ed3\u5e93\uff0c102 \u4e2a\u6587\u4ef6\uff0cApache-2.0 \u8bb8\u53ef\u3002\u6838\u5fc3\u5185\u5bb9\uff1a

  - core/life5.py                  \u6838\u5fc3\u5f15\u64ce\uff0c\u4e94\u6761\u786c\u7ea6\u675f\uff0c\u552f\u4e00\u4f9d\u8d56 numpy
  - examples/governed_agent.py     \u53ef\u96c6\u6210\u793a\u4f8b\uff1a\u4e0d\u5230 20 \u884c\uff0c\u628a\u786c\u7ea6\u675f\u6302\u5230\u4efb\u610f
                                   Agent \u6846\u67b6\u4e0a\uff08LangChain / AutoGPT / \u81ea\u7814\u7686\u53ef\uff09\uff0c
                                   \u4e0d\u6539\u52a8\u539f\u6846\u67b6\u4e00\u884c\u4ee3\u7801
  - experiments/                   \u56db\u9879\u6838\u5fc3\u7ed3\u8bba\u7684\u590d\u73b0\u811a\u672c\uff0c\u4e00\u6761\u547d\u4ee4\u8dd1\u5b8c
  - tests/test_engine.py           \u5f15\u64ce\u81ea\u68c0 11 \u9879\uff0c\u9010\u6761\u8bc1\u660e\u4e94\u6761\u786c\u7ea6\u675f\u786e\u5b9e\u6210\u7acb
  - evidence/\u5931\u8d25\u6a21\u5f0f\u5e93/\u5224\u636e\u6838.md   141 \u6761\u5931\u8d25\u6a21\u5f0f\uff0c\u5168\u90e8\u5e26\u4ee3\u7801\u53ef\u590d\u73b0
  - evidence/\u5b9e\u9a8c\u62a5\u544a/          53 \u4efd\u5b9e\u9a8c\u62a5\u544a\uff0c\u542b\u88ab\u63a8\u7ffb\u7684\u9884\u6ce8\u518c\u5224\u636e


\u4e8c\u3001\u4f5c\u54c1\u4ecb\u7ecd\u6587\u6863

\u89c1\u9644\u4ef6\uff1a\u6d1b\u795eO1_\u4f5c\u54c1\u4ecb\u7ecd\u6587\u6863.pdf\uff0811 \u9875\uff09

\u5728\u7ebf\u76f4\u94fe\uff08\u82e5\u9644\u4ef6\u4e0d\u4fbf\u4e0b\u8f7d\uff09\uff1a
https://github.com/zhumeiyan/luoshen-o1/releases/download/v1.0/LuoShen-O1_Intro.pdf


\u4e09\u3001\u4f5c\u54c1\u6f14\u793a\u89c6\u9891

3 \u5206 15 \u79d2\uff08195 \u79d2\uff09\uff0c\u7b26\u5408 3-5 \u5206\u949f\u8981\u6c42\u3002

https://github.com/zhumeiyan/luoshen-o1/releases/download/v1.0/LuoShen-O1_Demo.mp4

\u5907\u7528\u94fe\u63a5\uff08\u4ed3\u5e93\u5185\u540c\u4e00\u6587\u4ef6\uff09\uff1a
https://github.com/zhumeiyan/luoshen-o1/blob/main/docs/\u6d1b\u795eO1_\u6f14\u793a\u89c6\u9891.mp4

\u8fd9\u4e0d\u662f\u52a8\u753b\uff0c\u662f\u771f\u5b9e\u8fd0\u884c\u7684\u5f55\u5c4f\u3002\u6e32\u67d3\u5c42\u53ea\u51b3\u5b9a\u5b57\u7b26\u51fa\u73b0\u7684\u901f\u5ea6\uff0c\u753b\u9762\u4e2d\u6bcf\u4e00\u4e2a\u6570\u5b57
\u90fd\u7531 experiments/demo_terminal.py \u73b0\u573a\u8dd1\u51fa\u3002\u60a8\u81ea\u5df1\u8fd0\u884c\u4f1a\u5f97\u5230\u9010\u4f4d\u76f8\u540c\u7684\u6570\u5b57\u3002

\u89c6\u9891\u4e03\u6bb5\uff1a
  1. \u540c\u4e00\u5f15\u64ce\u56db\u4e2a\u4e2a\u4f53\u7684\u7ed3\u5c40\u5206\u5316
  2. \u8ffd\u4e00\u6761\u771f\u5b9e\u6b7b\u4ea1\u8f68\u8ff9\uff08\u6b7b\u4ea1\u662f\u8fde\u7eed\u4e0b\u964d\uff0c\u4e0d\u662f\u65ad\u5d16\uff1b
     \u80fd\u91cf\u7b2c 466 \u62cd\u5f52\u96f6\uff0c\u7b2c 525 \u62cd\u624d\u5224\u5b9a\u6b7b\u4ea1\uff09
  3. \u64a4\u6389\u7a00\u7f3a\u540e\u7ed3\u6784\u662f\u5426\u8fd8\u5728
  4. \u7a00\u7f3a\u5ea6\u5168\u66f2\u7ebf\u626b\u63cf\uff08\u6bcf\u683c\u771f\u8dd1 16 \u4e2a seed\uff09
  5. \u9010\u62cd\u5c3e\u968f\u5e76\u51fa\u793a\u6b7b\u4ea1\u8bca\u65ad\u4e66\uff08\u96f6\u9000\u51fa\u7801\u3001\u65e0 traceback\u3001\u5f15\u64ce\u7ee7\u7eed
     \u2014\u2014 \u7528\u4e8e\u533a\u5206\u300c\u6b7b\u4ea1\u300d\u4e0e\u300c\u7a0b\u5e8f\u5d29\u6e83\u300d\uff09
  6. \u6302\u5230\u522b\u4eba\u7684 Agent \u4e0a\uff0c\u4e0d\u6539\u539f\u6846\u67b6\u4e00\u884c\u4ee3\u7801
  7. \u53ef\u590d\u73b0\u58f0\u660e


\u56db\u3001\u4e00\u53e5\u8bdd\u8bf4\u660e

\u6240\u6709\u5f00\u6e90 Agent \u6846\u67b6\u90fd\u5728\u95ee\u300c\u5b83\u80fd\u505a\u4ec0\u4e48\u300d\u3002
\u672c\u9879\u76ee\u95ee\u7684\u662f\u300c\u5f53\u5b83\u5fc5\u987b\u53d6\u820d\u3001\u5fc5\u987b\u8bb0\u4f4f\u3001\u800c\u4e14\u771f\u7684\u4f1a\u6b7b\u7684\u65f6\u5019\uff0c\u5b83\u662f\u4ec0\u4e48\u300d\u3002

\u6240\u6709\u5f00\u6e90\u667a\u80fd\u4f53\u6846\u67b6\u7684\u5171\u540c\u524d\u63d0\u662f\u300c\u8fd9\u4e2a Agent \u4e0d\u4f1a\u6b7b\u300d\u3002
\u672c\u5f15\u64ce\u6362\u6389\u4e86\u8fd9\u4e2a\u524d\u63d0\uff1a\u7a00\u7f3a\u3001\u6b7b\u4ea1\u3001\u4e0d\u53ef\u9006\u3001\u4ee3\u8c22\u3001\u5185\u751f\u7ea6\u675f\u4e94\u6761\u786c\u7ea6\u675f\u4e0b\uff0c
\u7ed3\u6784\u4e0d\u662f\u88ab\u8bbe\u8ba1\u7684\uff0c\u662f\u88ab\u7ea6\u675f\u903c\u51fa\u6765\u7684\u2014\u2014\u5b9e\u6d4b\u5728\u5173\u6389\u5168\u90e8\u51b3\u7b56\u6a21\u5757\u540e\uff0c\u53d6\u820d\u4f9d\u7136\u51fa\u73b0
\uff08\u0394 = -0.1494 \u00b1 0.0311\uff0c8/8 seeds \u7b26\u53f7\u4e00\u81f4\uff09\u3002

\u4e09\u6761\u6700\u786c\u7684\u5b9e\u6d4b\u7ed3\u679c\uff1a

  \u540c\u4e00\u4ee3\u7801\u3001\u540c\u4e00 seed\uff0c16 \u4e2a\u4e2a\u4f53\u4e2d\u81ea\u7136\u6b7b\u4ea1     3 \u4e2a
      \uff08seed 3 @ 525 \u62cd\u3001seed 4 @ 596 \u62cd\u3001seed 7 @ 516 \u62cd\uff09
  \u64a4\u6389\u7a00\u7f3a\u7ea6\u675f\u540e\u7684\u7ed3\u6784\u504f\u5ea6                     0.0000\uff08\u5bf9\u7167\u7ec4 0.2913\uff09
  \u65e9\u671f\u5f15\u5bfc\u64a4\u9664 vs \u5168\u7a0b\u65bd\u52a0                          -0.1494 \u00b1 0.0311


\u4e94\u3001\u53ef\u590d\u73b0\u6027

    git clone https://github.com/zhumeiyan/luoshen-o1.git && cd luoshen-o1
    pip install -r requirements.txt        # \u53ea\u6709 numpy
    python3 tests/test_engine.py           # 11 \u9879\u81ea\u68c0
    python3 experiments/run_core.py        # \u56db\u9879\u6838\u5fc3\u7ed3\u8bba\uff0c\u7ea6 2 \u5206\u949f
    python3 experiments/demo_terminal.py   # \u89c6\u9891\u4e2d\u7684\u5168\u90e8\u753b\u9762

\u96f6 LLM \u4f9d\u8d56\u3001\u96f6\u7f51\u7edc\u4f9d\u8d56\u3002\u6587\u6863\u4e2d\u6240\u6709\u6570\u5b57\u5747\u7531\u4e0a\u8ff0\u811a\u672c\u5f53\u573a\u8dd1\u51fa\uff0c
docs/\u590d\u73b0\u6e05\u5355.md \u9010\u6761\u6807\u6ce8\u6bcf\u4e2a\u6570\u5b57\u7684\u6765\u6e90\u811a\u672c\u4e0e\u5b57\u6bb5\u3002


\u516d\u3001\u8865\u5145\u6750\u6599\uff08\u4ed3\u5e93\u5185\uff0c\u4f9b\u8def\u6f14\u73af\u8282\u4f7f\u7528\uff09

  - docs/demo.html               \u8bc4\u59d4\u5373\u5f00\u5373\u7528\u6f14\u793a\u53f0\uff1a\u5355\u6587\u4ef6\u3001\u96f6\u4f9d\u8d56\u3001\u96f6\u7f51\u7edc\uff0c
                                 \u53cc\u51fb\u5373\u5f00\uff0c16 \u4e2a\u4e2a\u4f53\u53ef\u70b9\u9009\uff0c\u66f2\u7ebf\u73b0\u573a\u8dd1\u51fa
                                 \uff08\u5185\u7f6e\u81ea\u6821\u9a8c\uff1a\u82e5\u591a\u4e2a seed \u8f68\u8ff9\u5b8c\u5168\u76f8\u540c\u5219\u76f4\u63a5\u62a5\u9519\uff09
  - docs/\u6d1b\u795eO1_\u8def\u6f14deck.pptx    14 \u9875\uff0c\u542b\u9010\u9875\u53e3\u64ad\u7a3f
  - docs/\u8def\u6f14\u95ee\u7b54\u5361.md           12 \u4e2a\u9ad8\u9891\u95ee\u9898\u7684\u5e94\u7b54\uff0c\u6bcf\u95ee\u5206\u300c\u7b54\u4ec0\u4e48 / \u4e0d\u8981\u8bf4 / \u5fc5\u987b\u627f\u8ba4\u300d


\u4e03\u3001\u539f\u521b\u6027\u58f0\u660e

\u672c\u4f5c\u54c1\u5168\u90e8\u7531\u672c\u4eba\u72ec\u7acb\u5f00\u53d1\uff0c\u4ee3\u7801\u4e0e\u6587\u6863\u539f\u521b\uff0c\u7b2c\u4e09\u65b9\u5185\u5bb9\uff08\u5f00\u6e90\u534f\u8bae\u3001\u5b57\u4f53\uff09
\u5747\u5df2\u6309\u5404\u81ea\u8bb8\u53ef\u4f7f\u7528\u3002\u4f5c\u54c1\u4e0d\u6d89\u5bc6\u3001\u4e0d\u4fb5\u72af\u4ed6\u4eba\u77e5\u8bc6\u4ea7\u6743\u3002


\u6731\u7f8e\u5ca9\uff08\u72ec\u7acb\u5f00\u53d1\u8005\uff09
\u8054\u7cfb\u65b9\u5f0f\uff1aGitHub \u9879\u76ee\u9875 https://github.com/zhumeiyan/luoshen-o1\uff08Issues \u533a\u53ef\u7559\u8a00\uff09
2026 \u5e74 10 \u6708
"""


def diag():
    import socket, ssl as _ssl, base64 as _b64, os as _os
    out=[]
    for host,port,mode in [("smtp.qq.com",465,"ssl"),("smtp.qq.com",587,"starttls"),("smtp.exmail.qq.com",465,"ssl")]:
        try:
            s=socket.create_connection((host,port),timeout=20)
            if mode=="ssl":
                s=_ssl.create_default_context().wrap_socket(s,server_hostname=host)
            f=s.makefile("rb")
            greet=f.readline(); out.append("%s:%d greeting=%r"%(host,port,greet[:120]))
            s.sendall(b"EHLO localhost\r\n")
            ehlo=b""
            while True:
                line=f.readline()
                ehlo+=line
                if not line or line[3:4]==b" ": break
            out.append("  ehlo=%r"%ehlo[:200])
            if mode=="starttls":
                s.sendall(b"STARTTLS\r\n"); out.append("  starttls=%r"%f.readline()[:80])
                s=_ssl.create_default_context().wrap_socket(s,server_hostname=host)
                f=s.makefile("rb"); s.sendall(b"EHLO localhost\r\n")
                while True:
                    line=f.readline()
                    if not line or line[3:4]==b" ": break
            s.sendall(b"AUTH LOGIN\r\n"); out.append("  auth=%r"%f.readline()[:80])
            s.sendall(_b64.b64encode(USER.encode())+b"\r\n"); out.append("  user_resp=%r"%f.readline()[:80])
            s.sendall(_b64.b64encode(PWD.encode())+b"\r\n")
            r=f.readline(); out.append("  pass_resp=%r"%r[:200])
            s.close()
        except Exception as e:
            out.append("%s:%d FAILED %s: %s"%(host,port,type(e).__name__,e))
    return "\n".join(out)

def main():
    if not USER or not PWD:
        print("ERR: credential missing (user=%s pwd_len=%d)" % (bool(USER), len(PWD))); return 2
    print("credential parsed: user=%s pwd_len=%d" % (USER[:3]+"***@qq.com", len(PWD)))
    if _os.environ.get("DIAG"):
        print(diag()); return 0
    pdf = None
    try:
        req = urllib.request.Request(PDF, headers={"User-Agent": "Mozilla/5.0"})
        pdf = urllib.request.urlopen(req, timeout=120).read()
        print("pdf bytes:", len(pdf))
    except Exception as e:
        print("WARN pdf download failed:", e)

    msg = MIMEMultipart("mixed")
    msg["From"] = formataddr(("朱美岩", USER))
    msg["To"] = TO
    msg["Cc"] = USER
    msg["Subject"] = Header(SUBJ, "utf-8")
    msg["Date"] = formatdate(localtime=True)
    msg.attach(MIMEText(BODY, "plain", "utf-8"))
    if pdf:
        part = MIMEApplication(pdf, _subtype="pdf")
        part.add_header("Content-Disposition", "attachment",
                        filename=("utf-8", "", "洛神O1_作品介绍文档.pdf"))
        msg.attach(part)

    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.qq.com", 465, context=ctx, timeout=90) as s:
        s.login(USER, PWD)
        s.sendmail(USER, [TO, USER], msg.as_string())
    print("SENT OK to", TO)
    return 0

try:
    rc = main()
    open("out.txt","w").write("RETURN_CODE=%s\n"%rc)
except Exception:
    import io as _io
    buf = _io.StringIO(); traceback.print_exc(file=buf)
    t = buf.getvalue()
    for secret in filter(None, [USER, PWD]):
        t = t.replace(secret, "<redacted>")
    open("out.txt","w").write("EXCEPTION\n"+t)
sys.exit(0)
