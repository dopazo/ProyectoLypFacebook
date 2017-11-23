from langid import classify
from langdetect import detect  
from textblob import TextBlob

class LanguageDetector(object):
    """
    Class used to detect the language of a text
    """

    def __init__(self):
        pass

    def langid_safe(self, text):
        try:
            return langid.classify(text)[0]
        except Exception as e:
            pass

    def langdetect_safe(self, text):  
        try:
            return detect(text)
        except Exception as e:
            pass

    def textblob_safe(self, text):  
        try:
            return TextBlob(text).detect_language()
        except Exception as e:
            pass 

    def detect(self, text=None):
        if text is None:
            raise ValueError('text cannot be None')
        try:
            return self.langid_safe(text) or self.langdetect_safe(text) or self.textblob_safe(text)
        except Exception as e:
            pass

    def check(self, text=None, lang='en'):
        if text is None:
            raise ValueError('text cannot be None')
        try:
            detected = self.detect(text)
            return True if detected == lang else False
        except Exception as e:
            return False

if __name__ == '__main__':
    ld = LanguageDetector()
    print(ld.detect("Portada 'Público', viernes. Fabra al banquillo por 'orden' del Supremo; Wikileaks 'retrata' a 160 empresas espías. http://t.co/YtpRU0fd")) 
