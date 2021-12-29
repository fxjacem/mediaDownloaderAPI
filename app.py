from logging import debug
from colorama import Fore
from ip_address import ip_info
from parser_normal import video_link_parser, MyLogger
from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "27eduCBA09"

def data_collection(url):
    output = {}
    modes = ['default', 'best', 'bestvideo', 'bestaudio']
    for mode in modes:
        if app.debug:
            print(mode)
        output[mode] = video_link_parser(url, mode)
    
    return output

@app.route('/', methods=['GET', 'POST'])
def home():
    session["debug"] = app.debug
    geo_information = ip_info()

    info_string = Fore.GREEN + ' ' + request.method + ' - '
    info_string += Fore.YELLOW + ' ' + geo_information['ip'] + ' ' +  geo_information['country'] + ' ' +   geo_information['city'] + ' - ' + Fore.CYAN
    info_string += request.form['searched-link'] if request.method == 'POST' else 'HOME'
    info_string += Fore.RESET
    print(info_string)

    if request.method == 'POST':
        url = request.form['searched-link']

        if url != '':
            datas = data_collection(url)
            session["data"] = datas

            return redirect(url_for('result'))

    return render_template('index.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        return redirect(url_for('home'))
    
    # print('session:', session['data'])
    
    return render_template('result.html', datas=session['data'], debug=session['debug'])

@app.errorhandler(404)
def page_not_found(e):
    print('error:', e)

    return render_template('404.html')

if __name__ == '__main__':
    app.run(port=11111, debug=False)
