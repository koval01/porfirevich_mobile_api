import requests, json, random, string, re, time


def get_data() -> str:
    """Функция получения данных"""
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4421.5 Safari/537.36"}
    API_URL = 'https://porfirevich.ru/api/story/?orderBy=RAND()&limit=20'
    data = requests.get(API_URL, headers=headers)
    return data.text


def prepare_data(data) -> list:
    """Подготовка данных"""
    for i in data['data']:
        return i


def cleanhtml(raw_html) -> str:
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


def fix_string(string) -> str:
    """
    Удаление лишних пробелов в тексте
    :param string: Input term
    :return: Filtered string
    """
    in_word = string
    in_between_words = ['-', '–']
    in_sentences = ['«', '(', '[', '{', '"', '„', '\'']
    for item in in_between_words:
        regex = r'\w[%s]\s\w' % item
        in_word = re.findall(regex, string)

        for x in in_word:
            a = x[:1]; b = x[3:4]
            string = string.replace(x, a + '-' + b)

    for item in in_sentences:
        string = string.replace(f' {item} ', f' {item}')
    return string


# def cut_long_words(string) -> str:
#     """Обрізання занад-то довгих елементів"""
#     s = string.split()
#     array = []
#     for i in s:
#         if len(i) > 19:
#             y = ' '
#             if str(i)[:1] == y:
#                 x = y + str(i)[:19]
#             else:
#                 x = str(i)[:19]
#         else: 
#             x = i
#         array.append(x)
    
#     return ' '.join(array)


def check_long_words_in_string(string) -> bool:
    """Перевірка наявності занад-то довгих слів в строці"""
    status = True
    s = string.split()
    for i in s:
        if len(i) > 22:
            status = False

    return status


def decode_story_string(array) -> str:
    """Декодер текста записи"""
    struct_array = []
    array = json.loads(array)
    for i in array:
        text = cleanhtml(str(i[0]))
        text = fix_string(text)
        if check_long_words_in_string(text):
            text = text.replace('\n', '</br>')
            if i[1]:
                struct_array.append(f'<b id="{get_random_string()}">{text}</b>')
            else: 
                struct_array.append(f'<i id="{get_random_string()}">{text}</i>')
    return ''.join(struct_array)


def export_data(array) -> str:
    """Последний этап подготовки данных"""
    template = """
            <div id="_0" class="col-12 col-lg-12 padding-block-center-box">
                <div class="user box aos-init aos-animate" data-aos="fade-up">
                    <img style="image-rendering: pixelated; width: 60px; filter: invert(0.8); height: 60px" class="lazyloaded" data-src="file:///android_asset/static/my_web/images/logo-dark.svg" src="file:///android_asset/static/my_web/images/logo-dark.svg">
                    <div style="width: calc(1.0 - 90px); float: left; ">
                        <label class="status" data-toggle="tooltip" data-placement="top" data-original-title="1" style="color: 2"><svg style="filter: invert(0.8);" class="svg-inline--fa fa-circle fa-w-16" aria-hidden="true" focusable="false" data-prefix="fas" data-icon="circle" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" data-fa-i2svg=""><path fill="currentColor" d="M256 8C119 8 8 119 8 256s111 248 248 248 248-111 248-248S393 8 256 8z"></path></svg></label>
                        <label class="username">Пользовательская запись</label><br>
                        <label class="city">%s<br><br><b>%s</b> ❤️<br></label>
                    </div>
                </div>
            </div>
    """
    data_array = []
    for i in array:
        template_ = template % (str(i[0]), str(i[1]))
        data_array.append(template_)
        data_array.append(copyright())

    return ''.join(data_array)


def get_random_string(length = 16) -> str:
    """Генерация рандомной строки из цифр и букв"""
    letters = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def time_elapse(start_time):
    """Обчислюємо витрачений час"""
    time_elapsed = str(time.time() - start_time)[:5]
    return '<!-- %s %s -->' % (get_random_string(), time_elapsed)

def copyright() -> str:
    """Простая функция для удобной вставки сообщения о авторском праве"""
    text = 'The code you see now belongs to the porfirevich.ru project. You may not copy this code without permission.'
    return '<!-- %s %s -->' % (get_random_string(random.randint(12, 20)), text)


def api_get_data() -> str:
    """Основная функция которая возвращает готовые данные"""
    s = time.time()
    data = get_data()
    data = json.loads(data)

    array_data = []
    for i in data['data']:
        d = decode_story_string(i['content'])
        l = i['likesCount']
        # u = i['updatedAt']
        a = [d, l]
        array_data.append(a)
    
    result = export_data(array_data)
    result += time_elapse(s)

    return result