import wikipedia

def malumot(text):
    try:
        wikipedia.set_lang("uz")
        result = wikipedia.summary(text)
    except:
        return "🤕 Afsuski bu xaqida malumot topilmadi"
    return result

