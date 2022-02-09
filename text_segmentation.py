from simpletransformers.config.model_args import NERArgs
from simpletransformers.ner import NERModel

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


def sentence_samples(sentence):
    for punc in '.!?':
        sentence = sentence.split(f'{punc} ')
        sentence = '###'.join(
            [elem + punc for elem in sentence[:-1]] + sentence[-1:])
    return sentence.split('###')


class SegmentationPredictor:
    def __init__(self):
        model_args = NERArgs()
        model_args.max_seq_length = 512
        model_args.labels_list = custom_labels
        self.model = NERModel(
            "bert", "danasone/rubert-tiny-essay", args=model_args,
            labels=custom_labels, use_cuda=False
        )

    def get_annotations(self, text):
        predictions, raw_outputs = self.model.predict([sentence_samples(text)],
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
        return annotations
