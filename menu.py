#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sys
import termios
import tty


class Menu(object):
    def __init__(self, clear_screen=True):
        self.offset = " " * 8   # 菜单距离左侧偏移量
        self.id_show = True  # 是否显示列表id
        self.title_show = True  # 标题是否显示
        self.foot_show = True   # 页脚是否显示
        self.page_size = 10  # 每页显示多少条
        self.back_code = "back"  # 定义"返回"时应当return的状态码
        self.title_delimiter = " > "  # 定义标题分隔符
        self.pointer = "->"   # 定义选择指示器
        self.title_color = "purple"
        self.foot_color = "yellow"
        self.body_word_color = ""
        self.body_word_switch_color = "blue"

        if clear_screen:
            os.system("clear")

    def menu_style(self, offset=8, id_show=True, title_show=True, foot_show=True,
                   page_size=10, back_code="back", title_delimiter=" > ", pointer="->",
                   title_color="purple", foot_color="yellow", body_word_color="",
                   body_word_switch_color="blue"):
        """
        菜单样式设置
        供选择的颜色：'black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white'
        :param offset:
        :param id_show:
        :param title_show:
        :param foot_show:
        :param page_size:
        :param back_code:
        :param title_delimiter:
        :param pointer:
        :param title_color: 'black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white'
        :param foot_color: 'black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white'
        :param body_word_color: 'black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white'
        :param body_word_switch_color: 'black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white'
        :return:
        """
        self.offset = " " * offset   # 菜单距离左侧偏移量
        self.id_show = id_show  # 是否显示列表id
        self.title_show = title_show  # 标题是否显示
        self.foot_show = foot_show   # 页脚是否显示
        self.page_size = page_size  # 每页显示多少条
        self.back_code = back_code  # 定义"返回"时应当return的状态码
        self.title_delimiter = title_delimiter  # 定义标题分隔符
        self.pointer = pointer   # 定义选择指示器
        self.title_color = title_color   # 标题颜色
        self.foot_color = foot_color  # 页脚颜色
        self.body_word_color = body_word_color  # 主体文字颜色
        self.body_word_switch_color = body_word_switch_color  # 选择的主体文字颜色

    def _font_style(self, string, mode='', fg='', bg=''):
        """字体样式选择"""
        styles = {
            'fg': {
                'black': 30, 'red': 31, 'green': 32, 'yellow': 33,
                'blue': 34, 'purple': 35, 'cyan': 36, 'white': 37,
            },
            'bg': {
                'black': 40, 'red': 41, 'green': 42, 'yellow': 43,
                'blue': 44, 'purple': 45, 'cyan': 46, 'white': 47,
            },
            'mode': {
                'bold': 1, 'underline': 4, 'blink': 5, 'invert': 7,
            },
            'default': {
                'end': 0,
            }
        }
        mode = '%s' % styles['mode'][mode] if mode in styles['mode'].keys() else ''
        fore = '%s' % styles['fg'][fg] if fg in styles['fg'].keys() else ''
        back = '%s' % styles['bg'][bg] if bg in styles['bg'].keys() else ''
        style = ';'.join([s for s in [mode, fore, back] if s])
        style = '\033[%sm' % style if style else ''
        end = '\033[%sm' % styles['default']['end'] if style else ''
        return '%s%s%s' % (style, string, end)

    def clr_scr(self):
        """
        清理屏幕
        用空格覆盖原来的菜单(清空菜单)，再将光标移动到第一行重新开始写入数据
        """
        if self.title_show and self.foot_show:
            back_line = self.page_size + 5
        elif self.title_show:
            back_line = self.page_size + 3  # 3 因为标题占三行
        elif self.foot_show:
            back_line = self.page_size + 2  # 2 因为foot占两行
        else:
            back_line = self.page_size
        s = [" " * 100 for i in range(0, back_line)]
        sys.stdout.write('\033[%dA\033[K' % (back_line,))
        sys.stdout.flush()
        sys.stdout.write("\n".join(s))
        sys.stdout.flush()
        sys.stdout.write('\033[%dA\033[K' % (back_line - 1,))
        sys.stdout.flush()

    def getch(self):
        """获取键盘输入"""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ch == "\x1b":
                ch += sys.stdin.read(2)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def title_box(self, title):
        if self.title_show:
            title_base = "\n" + self.offset + (len(self.pointer) + 1) * " " + "主菜单"
            if title is not None and isinstance(title, list):
                title_info = title_base + self.title_delimiter + self.title_delimiter.join(title)
            else:
                title_info = title_base
            sys.stdout.write(self._font_style(title_info, mode="bold", fg=self.title_color) + '\n\n')
            sys.stdout.flush()

    def body_box(self, pos, choose, id_start):
        i = 0
        s = ""
        while i < self.page_size:
            if i >= len(choose):
                s += "\r\n"
                i += 1
                continue
            if i == pos:
                if self.id_show:
                    content = str(id_start + i) + ". " + str(choose[i])
                else:
                    content = str(choose[i])
                temp = self.pointer + " " + content
                temp = self._font_style(temp, fg=self.body_word_switch_color, bg="")
            else:
                if self.id_show:
                    content = str(id_start + i) + ". " + str(choose[i])
                else:
                    content = str(choose[i])
                temp = (len(self.pointer) + 1) * " " + content
                temp = self._font_style(temp, fg=self.body_word_color)
            s += "\r" + self.offset + temp + "\n"
            i += 1
        sys.stdout.write(s)
        sys.stdout.flush()

    def foot_box(self, total, start, page):
        # 菜单页脚显示
        s = ""
        next_page = False
        prev_page = False
        if self.foot_show:
            if start + self.page_size < total:
                next_page = True
            if start - self.page_size >= 0:
                prev_page = True

            foot = "\n" + self.offset + (len(self.pointer) + 1) * " " + "<第{}页".format(page)
            if next_page and prev_page:
                foot = foot + " 上一页:有 下一页:有"
            elif next_page:
                foot = foot + "  下一页:有"
            elif prev_page:
                foot = foot + " 上一页:有"
            foot += ">"
            s = s + self._font_style(foot, fg=self.foot_color) + "\n"
        sys.stdout.write(s)
        sys.stdout.flush()

    def tty_menu(self, choose, title=None):
        pos = 0
        start = 0
        page = 1
        page_size = self.page_size
        total = len(choose)

        if start + page_size < total:
            page_list = choose[start:start + page_size]
        else:
            page_list = choose[start:len(choose)]
        self.title_box(title)
        self.body_box(pos, page_list, start)
        self.foot_box(total, start, page)

        while True:
            key = self.getch()
            if key == "\x03":  # ctrl + c
                break

            elif key == "\r":  # enter
                real_id = page_size * (page - 1) + pos
                return real_id, choose[real_id]

            elif key in ["\x1b[A", "k", "K"]:
                pos -= 1

            elif key in ["\x1b[B", "j", "J"]:
                pos += 1

            elif key in ["\x1b[D", "h", "H"]:  # 上一页
                if start - page_size >= 0:
                    pos = 0
                    start = start - page_size
                    page -= 1

            elif key in ["\x1b[C", "l", "L"]:  # 下一页
                if start + page_size < len(choose):
                    pos = 0
                    start = start + page_size
                    page += 1

            elif key in ["b", "B"]:  # 返回
                return "back", None

            elif key in ["q", "Q"]:  # 退出
                sys.exit(0)

            if pos < 0:
                pos = len(page_list) - 1
            elif pos >= len(page_list):
                pos = 0

            if start + page_size < len(choose):
                page_list = choose[start:start + page_size]
            else:
                page_list = choose[start:len(choose)]
            self.clr_scr()
            self.title_box(title)
            self.body_box(pos, page_list, start)
            self.foot_box(total, start, page)


if __name__ == '__main__':
    l = list(range(0, 24))
    l = ["选择项-" + str(i) for i in range(0, 24) ]
    m = Menu(clear_screen=False)
    m.menu_style(id_show=True, title_show=False, foot_show=False, page_size=9, title_color="red", body_word_color="red")
    pos, value = m.tty_menu(l, title=["功能", "数字选择"])
    print(pos, value)
