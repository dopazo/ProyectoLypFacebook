from corpus import CorpusHelper, CorpusModel

from language_detector import LanguageDetector

if __name__ == '__main__':
    ch = CorpusHelper(language='spanish')
    ch.load()
    cm = CorpusModel(corpus=ch)
    params = cm.fit() 
    print(cm.x_validation(params))

    texts = ['El candidato es un ladrón y un mentiroso', '@AlgoMortal Muchas felicidades que lo pases muy bien :)', '@eslatarde @PPopular En una palabra, INSULTANTE!!!']
    ld = LanguageDetector()
    texts = [text for text in texts if ld.detect(text) == 'es']
    print(cm.predict(texts, params))
