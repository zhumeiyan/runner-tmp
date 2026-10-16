# -*- coding: utf-8 -*-
import sys, os, ssl, smtplib, traceback, urllib.request, io as _io
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

BODY = open("body.txt", encoding="utf-8").read() if os.path.exists("body.txt") else "(body missing)"

CANDS = [(USER, PWD), ("778131400", PWD), (USER, "778131400"), ("778131400", "778131400")]

def try_login(u, p):
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465, context=ssl.create_default_context(), timeout=60)
        s.login(u, p)
        return s
    except Exception as e:
        return "%s: %s" % (type(e).__name__, str(e)[:150])

def send_with(srv, u, lines):
    pdf = None
    try:
        req = urllib.request.Request(PDF, headers={"User-Agent": "Mozilla/5.0"})
        pdf = urllib.request.urlopen(req, timeout=120).read()
        lines.append("pdf bytes: %d" % len(pdf))
    except Exception as e:
        lines.append("WARN pdf: %s" % e)
    msg = MIMEMultipart("mixed")
    msg["From"] = formataddr(("朱美岩", u))
    msg["To"] = TO
    msg["Cc"] = u
    msg["Subject"] = Header(SUBJ, "utf-8")
    msg["Date"] = formatdate(localtime=True)
    msg.attach(MIMEText(BODY, "plain", "utf-8"))
    if pdf:
        part = MIMEApplication(pdf, _subtype="pdf")
        part.add_header("Content-Disposition", "attachment",
                        filename=("utf-8", "", "洛神O1_作品介绍文档.pdf"))
        msg.attach(part)
    srv.sendmail(u, [TO, u], msg.as_string())
    lines.append("SENT OK to %s" % TO)

def main():
    lines = []
    lines.append("parsed: user=%r pwd_len=%d" % (USER, len(PWD)))
    for u, p in CANDS:
        res = try_login(u, p)
        if isinstance(res, str):
            lines.append("TRY %s -> FAIL %s" % (u, res))
        else:
            lines.append("TRY %s -> SUCCESS" % u)
            try:
                send_with(res, u, lines)
            except Exception as e:
                lines.append("SEND FAIL %s: %s" % (type(e).__name__, str(e)[:200]))
            break
    return lines

if __name__ == "__main__":
    out = []
    try:
        out = main()
    except Exception:
        buf = _io.StringIO(); traceback.print_exc(file=buf)
        out.append("EXCEPTION\n" + buf.getvalue())
    txt = "\n".join(out)
    for s in filter(None, [USER, PWD]):
        txt = txt.replace(s, "<redacted>")
    open("out.txt", "w", encoding="utf-8").write(txt)
    print(txt)
    sys.exit(0)
