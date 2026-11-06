# -*- coding: utf-8 -*-
"""机时链排程器（M2 逐章串行 · 会话间不空转 CPU）：
等当前批量进程（--wait-pid）退出后，自动启动下一章的 MITRA 批量试译。

边界（诚实声明）：
- 不碰数据层、不做实质判断——唯一动作 = 启动**用户已批准序列**（M2 逐章·
  「逐步推进」）中预先排定的下一环；验收（页面/门禁/commit）仍归后续会话人工侧。
- 本机重启则本链失效（可接受：可续跑器 status!=done 自动补段，无数据损失）。
- 日志 mitra_chain_log.txt 与批量日志同目录，落盘可查。

用法（项目根）：
  python -X utf8 workspace/tibetan-avatamsaka-translation/tools/mitra_chain_next.py \
    --wait-pid 39520 --chapter 15
"""
import sys, os, io, time, argparse, subprocess


def alive(pid):
    r = subprocess.run(['tasklist', '/FI', 'PID eq %d' % pid, '/NH'],
                       capture_output=True, text=True)
    return str(pid) in (r.stdout or '')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--wait-pid', type=int, required=True)
    ap.add_argument('--chapter', type=int, required=True)
    ap.add_argument('--interval', type=int, default=120)
    a = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    log = io.open(os.path.join(here, 'mitra_chain_log.txt'), 'a',
                  encoding='utf-8', buffering=1)
    log.write('[chain] waiting pid=%d -> next chapter %d\n' % (a.wait_pid, a.chapter))
    while alive(a.wait_pid):
        time.sleep(a.interval)
    log.write('[chain] pid %d gone at %s; launching --chapter %d\n'
              % (a.wait_pid, time.strftime('%H:%M:%S'), a.chapter))
    r = subprocess.run([sys.executable, '-X', 'utf8',
                        os.path.join(here, 'mitra_batch_translate.py'),
                        '--chapter', str(a.chapter)])
    log.write('[chain] batch chapter %d exit=%d\n' % (a.chapter, r.returncode))


if __name__ == '__main__':
    main()
