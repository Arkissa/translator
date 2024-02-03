# 一款跨平台的中英翻译器

## 注意事项  

**安装** 
```shell
$ git clone https://github.com/New-arkssac/translator.git
$ pip install -r requiements.txt 
```

**用法**  
```shell
$ ./main.py -h
usage: main.py [-h] (-t TEXT | -l) [-p PROXY] [-d {text,json,notify}]

Translate between English and Chinese. # 中英翻译器

options:
  -h, --help            show this help message and exit # 帮助信息
  -t TEXT, --text TEXT  Text to translate. # 从程序参数中获取文本进行翻译
  -l, --listen          Enable listening mode, translate the text selected bythe mouse. (default: disable)                                   # 启动监听模式，监听鼠标选中的文本进行翻译
  -p PROXY, --proxy PROXY
                        Set request proxy URL (default: empty) # 设置翻译的时候使用的网络代理
  -d {text,json,notify}, --display {text,json,notify}
                        Set translation result display style. (default: text) # 设置翻译结果的显示方式
```
## 跨平台
目前只有Linux X11平台支持所有功能，  
其他平台不支持监听模式和使用通知栏显示翻译结果

### Linux
目前只在x11桌面上的监听模式需要依赖xclip, 使用包管理器装一下  
**arch**  
```shell
$ sudo pacman -S xclip
```

**ubuntu**  
```shell
$ sudo apt install xclip
```

以及需要把用户添加到input用户组里
```shell
$ sudo usermod -a -G input $USER  
```

## Windows
TODO  

## Darwin  
TODO

## 自行添加翻译器
我在`interface.py`中实现了翻译器的接口
```python
@runtime_checkable
class Translator(Protocol):
    @abstractmethod
    async def Do(self, text: str) -> Dict[str, str]:
        pass
```
只需要在`translator`目录下自行开发相应的对象，程序会自动加载  
>> `translator`目录下的python文件名应当与文件中要加载的类名相同

# TODO
程序完成度较高，后续只会添加以下功能
 * 可以通过参数来指定所使用的翻译器
 * Windows和Darwin下的监听模式通知栏显示翻译结果支持
