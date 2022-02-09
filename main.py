import json

import streamlit as st
from annotated_text import annotated_text

from text_segmentation import SegmentationPredictor

st.title('Визуализация разметки эссе')


@st.cache
def get_segmentation_model():
    model = SegmentationPredictor()
    return model


def show_json_annotations(obj, text_type):
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
    model = get_segmentation_model()
    annotated_text(*model.get_annotations(text))


def main():
    selected_mode = st.selectbox("Mode", ['segmentation', 'visualization'])
    if selected_mode == 'segmentation':
        text = st.text_area('Текст для анализа', value='', height=None,
                            max_chars=None,
                            key=None)
        if text:
            predict_meaning(text)
    if selected_mode == 'visualization':
        uploaded_file = st.file_uploader("Upload Files", type=['json', ])
        if uploaded_file is not None:
            obj = json.loads(uploaded_file.read())
            # open("data.json", 'w').write(str(uploaded_file.read(), 'utf8'))

            selected_option = st.selectbox("Options", ['meaning', 'error'])
            show_json_annotations(obj, selected_option)


if __name__ == '__main__':
    main()
