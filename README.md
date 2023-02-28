# X11桌面下的划词翻译

## 注意事项

复制需要以来xclip, 使用包管理器装一下  
**arch**  
```shell
$ sudo pacman -S xclip
```

**ubuntu**  
```shell
$ sudo apt install xclip
```

需要把用户添加到input用户组里
```shell
$ sudo usermod -a -G input $USER  
```

以及安装基础python依赖
```shell
$ pip install -r requiements.txt 
```
