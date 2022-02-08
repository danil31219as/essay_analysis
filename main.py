import json

import streamlit as st
from annotated_text import annotated_text

st.title('Визуализация разметки эссе')
def show_annotations(text_type):
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
uploaded_file = st.file_uploader("Upload Files", type=['json', ])
if uploaded_file is not None:
    obj = json.loads(uploaded_file.read())
    open("data.json", 'w').write(str(uploaded_file.read(), 'utf8'))

    selected_option = st.selectbox("Options", ['meaning', 'error'])
    show_annotations(selected_option)