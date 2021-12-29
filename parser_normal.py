import json
import yt_dlp as yt
from colorama import Fore

class MyLogger:
    def error(self, msg):
        print(Fore.RED + '[HIBA] ' + msg + Fore.RESET)
    
    def warning(self, msg):
        pass
    
    def debug(self, msg):
        pass

    def info(self, msg):
        pass

def video_link_parser(input_link, input_mode):
    if input_mode == 'default':
        ydl = yt.YoutubeDL({'outtmpl': '%(id)s%(ext)s',
                            'quiet': True,
                            'warning': False,
                            'logger': MyLogger()})
    else:
        ydl = yt.YoutubeDL({'outtmpl': '%(id)s%(ext)s',
                            'quiet': True,
                            'ignoreerrors': True,
                            'warning': False,
                            'format': input_mode,
                            'logger': MyLogger()})

    response = dict()
    with ydl:
        try:
            result = ydl.extract_info(input_link,
                                      download=False,   # We just want to extract the info
                                      )
            if input_mode == 'default':
                response['url'] = input_link
                response['title'] = result.get('title', None)
                response['extractor'] = result.get('extractor_key', None)
                response['thumbnail'] = result.get('thumbnail', None)
                response['duration'] = result.get('duration', None)
                response['width'] = result.get('width', None)
                response['height'] = result.get('height', None)
            else:
                if 'url' not in result.keys() and 'entries' in result.keys():
                    result = result['entries'][0]
                
                if 'm3u' in result['protocol']:
                    formats = result['formats']
                    no_m3u8 = []
                    for format in formats:
                        if 'm3u' not in format['protocol']:
                            no_m3u8.append(format)
                    
                    result = no_m3u8[-1]                

                response['url'] = result.get('url', None)
                thumbnail = result.get('thumbnail', None)
                if thumbnail is not None:   # and output['default']['thumbnail'] is None:
                    response['thumbnail'] = result.get('thumbnail', None)


        except Exception as e:
            print(Fore.RED + '[HIBA] ' + Fore.RESET + str(e))
            response = None

    return response


if __name__ == '__main__':
    url = input('Link to test: ')

    output = {}
    modes = ['default', 'best', 'bestvideo', 'bestaudio']
    for mode in modes:
        print(mode)
        output[mode] = video_link_parser(url, mode)

    output_json = json.dumps(output, indent=4)
    print('Result:\n', output_json)
