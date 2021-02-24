import requests, json, random, string


def get_data():
    """Функция получения данных"""
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4421.5 Safari/537.36"}
    API_URL = 'https://porfirevich.ru/api/story/?orderBy=RAND()&limit=20'
    data = requests.get(API_URL, headers=headers)
    return data.text


def prepare_data(data):
    """Подготовка данных"""
    for i in data['data']:
        return i


def decode_story_string(array):
    """Декодер текста записи"""
    struct_array = []
    array = json.loads(array)
    for i in array:
        if i[1]: struct_array.append(f'<b id="{get_random_string()}">{i[0]}</b>')
        else: struct_array.append(f'<i id="{get_random_string()}">{i[0]}</i>')
    return ''.join(struct_array)


def export_data(array):
    """Последний этап"""
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

    return ''.join(data_array)


def get_random_string(length = 16):
    letters = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def api_get_data() -> str:
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

    return result