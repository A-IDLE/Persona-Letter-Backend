import subprocess

def install_spacy_model():
    subprocess.run(['python', '-m', 'spacy', 'download', 'en_core_web_sm'])

if __name__ == '__main__':
    install_spacy_model()