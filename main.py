# coding=utf-8
import os
import translate


def output(translate_result, to_clip_board, alert_location):
    os.environ['result'] = translate_result
    if alert_location == '屏幕右上角通知':
        # 输出结果到右上角
        shell = 'exec ./dialog/Contents/MacOS/cocoaDialog bubble \
                --title "翻译结果" \
                --icon-file result.png \
                --text "$result"'
    else:
        # 输出结果到屏幕中央
        shell = 'rv=`./dialog/Contents/MacOS/cocoaDialog msgbox \
            --title "MicroSoft Translate" \
            --text "翻译结果" \
            --icon-file result.png \
            --informative-text "$result" \
            --button1 "完成" --button3 "复制"` '
        shell = shell + '\n if [ "$rv" == "3" ]; then echo "$result" | /usr/bin/pbcopy ;fi'
    os.system(shell)
    # 复制翻译结果到剪贴板
    if to_clip_board == '复制':
        os.system('echo "$result" |/usr/bin/pbcopy')


LANGUAGES = {
    '简体中文': 'zh-Hans',
    '英语': 'en'
}

if __name__ == '__main__':
    # 获取设置信息
    mother_lang = os.environ['POPCLIP_OPTION_MOTHERLANG']
    dest_lang = os.environ['POPCLIP_OPTION_DESTLANG']
    to_clipboard = os.environ['POPCLIP_OPTION_TOCLIPBOARD']
    location = os.environ['POPCLIP_OPTION_LOCATION']
    # 获取需要翻译的文本
    text = os.environ['POPCLIP_TEXT']
    # 初始化翻译器
    translator = translate.Translator()
    # 初次翻译
    result = translator.translate(text=text, to_lang=LANGUAGES[mother_lang])
    # 获取返回的翻译文本语言的类型
    detected = result[0].get('detectedLanguage').get('language')
    # 如果需要翻译的文本类型和母语类型一致，调转目标语言和母语再次翻译
    if LANGUAGES[mother_lang] == detected:
        result = translator.translate(text=text, to_lang=LANGUAGES[dest_lang])
    # 输出结果
    output(translate_result=result[0].get('translations')[0].get('text').encode('utf-8')
           , to_clip_board=to_clipboard
           , alert_location=location)
