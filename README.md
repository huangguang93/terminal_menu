# terminal_menu

## terminal_menu  

一个快速创建命令行菜单的工具, fork:[tty_menu](https://github.com/gojuukaze/tty_menu) 

## 截图
1. 基本样式

  ![avatar](assets/第一页.png) 
  ![avatar](assets/第二页.png)
  ![avatar](assets/第三页.png)

2. 无页脚
  ![avatar](assets/无页脚.png)

3. 无标题无页脚
  ![avatar](assets/无页脚标题.png)

## Example

```
from menu import Menu
l = list(range(0, 24))
m = Menu(clear_screen=False) 
m.menu_style(page_size=10)
pos, value = m.tty_menu(l, title=["功能", "数字选择"])
print(pos, value)
```