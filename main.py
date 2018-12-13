# coding=utf-8
import os
import translate


def output(result, to_clipboard, location):
    os.environ['result'] = result
    if location == '屏幕右上角通知':
        shell = 'exec ./dialog/Contents/MacOS/cocoaDialog bubble \
                --title "翻译结果" \
                --icon-file result.png \
                --text "$result"'
    else:
        shell = 'rv=`./dialog/Contents/MacOS/cocoaDialog msgbox \
            --title "MicroSoft Translate" \
            --text "翻译结果" \
            --icon-file result.png \
            --informative-text "$result" \
            --button1 "完成" --button3 "复制"` '
        shell = shell + '\n if [ "$rv" == "3" ]; then echo "$result" | /usr/bin/pbcopy ;fi'
    os.system(shell)
    if to_clipboard == '复制':
        os.system('echo "$result" |/usr/bin/pbcopy')


LANGUAGES = {
    '简体中文': 'zh-Hans',
    '英语': 'en'
}

if __name__ == '__main__':
    mother_lang = os.environ['POPCLIP_OPTION_MOTHERLANG']
    dest_lang = os.environ['POPCLIP_OPTION_DESTLANG']
    to_clipboard = os.environ['POPCLIP_OPTION_TOCLIPBOARD']
    location = os.environ['POPCLIP_OPTION_LOCATION']
    text = os.environ['POPCLIP_TEXT']

    translator = translate.Translator()
    result = translator.translate(text=text, to_lang=LANGUAGES[mother_lang])
    detected = result[0].get('detectedLanguage').get('language')

    if LANGUAGES[mother_lang] == detected:
        result = translator.translate(text=text, to_lang=LANGUAGES[dest_lang])

    output(result=result[0].get('translations')[0].get('text').encode('utf-8')
           , to_clipboard=to_clipboard
           , location=location)
