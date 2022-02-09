import json
from simpletransformers.ner import NERModel, NERArgs
import streamlit as st
from annotated_text import annotated_text

st.title('Визуализация разметки эссе')

custom_labels = ['АРГУМЕНТ',
                 'ИДЕЯ',
                 'ИСП',
                 'ЛОГИКА',
                 'ОТНОШЕНИЕ',
                 'ОЦЕНКА',
                 'ПОЗИЦИЯ',
                 'ПОНЯТИЕ',
                 'ПОЯСНЕНИЕ',
                 'ПРИМЕР',
                 'ПРИЧИНА',
                 'ПРОБЛЕМА',
                 'РОЛЬ',
                 'СВЯЗЬ',
                 'СЛЕДСТВИЕ',
                 'СЯП',
                 'ТЕОРИЯ']
model_args = NERArgs()
model_args.max_seq_length = 512
model_args.labels_list = custom_labels

model = NERModel(
    "bert", "danasone/rubert-tiny-essay", args=model_args, labels=custom_labels, use_cuda=False
)

def show_json_annotations(text_type):
    ranges = []
    for select in obj['selections']:
        if select['group'] == text_type:
            ranges.append([select['startSelection'], select['endSelection'] + 1,
                           select['type']])
    ranges.sort(key=lambda x: x[0])
    full_ranges = []
    last = 0
    for elem in ranges:
        full_ranges.append([last, elem[0], ''])
        full_ranges.append([elem[0], elem[1], elem[2]])
        last = elem[1]
    annotations = []
    for elem in full_ranges:
        if elem[2]:
            annotations.append((obj['text'][elem[0]:elem[1]], elem[2]))
        else:
            annotations.append(obj['text'][elem[0]:elem[1]])
    annotated_text(*annotations)


def sentence_samples(sentence):
    for punc in '.!?':
        sentence = sentence.split(f'{punc} ')
        sentence = '###'.join(
            [elem + punc for elem in sentence[:-1]] + sentence[-1:])
    return sentence.split('###')


def predict_meaning(text):
    predictions, raw_outputs = model.predict([sentence_samples(text)],
                                             split_on_space=False)
    annotations = []
    last = list(predictions[0][0].values())[0]
    last_i = 0
    for i in range(len(predictions[0])):
        key, val = list(predictions[0][i].items())[0]
        if val != last:
            new_sentence = ''
            for pred in predictions[0][last_i:i]:
                new_sentence += list(pred.keys())[0] + ' '
            annotations.append((new_sentence, last))
            last = val
            last_i = i
    new_sentence = ''
    for pred in predictions[0][last_i:]:
        new_sentence += list(pred.keys())[0] + ' '
        annotations.append((new_sentence, last))
    annotated_text(*annotations)


text = st.text_area('Текст для анализа', value='', height=None, max_chars=None,
                    key=None)
predict_meaning(text)
uploaded_file = st.file_uploader("Upload Files", type=['json', ])
if uploaded_file is not None:
    obj = json.loads(uploaded_file.read())
    # open("data.json", 'w').write(str(uploaded_file.read(), 'utf8'))

    selected_option = st.selectbox("Options", ['meaning', 'error'])
    show_json_annotations(selected_option)
