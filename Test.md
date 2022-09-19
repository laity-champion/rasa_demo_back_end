```python
from py2neo import Graph


# 执行sql语句
class AnswerSearcher:
    def __init__(self):
        self.g = Graph("http://localhost:7474/", username="neo4j", password="neo4jneo4j")
        self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''

    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.g.run(query).data()
                answers += ress
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    '''根据对应的qustion_type，调用相应的回复模板'''

    async def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''

        # 1-1疾病-症状（症状+并发症）
        if question_type == 'disease_symptom':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            # final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
            # final_answer = '{0}的并发症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
            final_answer = '{0}的症状包括：{1}\n的并发症状包括：{2}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]),
                                                              '；'.join(list(set(desc))[:self.num_limit]))
            # final_answer = '{0}宜食的食物包括有：{1}\n推荐食谱包括有：{2}'.format(subject, ';'.join(list(set(do_desc))[:self.num_limit]),
            #                                                      ';'.join(list(set(recommand_desc))[:self.num_limit]))

        # 1-2疾病-科室
        elif question_type == 'check_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '{1}疾病应该去挂{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        # elif question_type == 'disease_food':
        #     desc = [i['n.name'] for i in answers]
        #     subject = answers[0]['m.name']
        #     final_answer = '{0}忌食的食物包括有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        # 1-3 疾病-食物（宜吃+推荐食谱+忌食）
        elif question_type == 'disease_food':
            do_desc = [i['n.name'] for i in answers if i['r.name'] == 'do_eat']
            recommand_desc = [i['n.name'] for i in answers if i['r.name'] == 'recommand_recipes']
            not_desc = [i['n.name'] for i in answers if i['r.name'] == 'not_eat']
            subject = answers[0]['m.name']
            final_answer = '{0}宜食的食物包括有：{1}\n推荐食谱包括有：{2}\n忌食的食物包括有：{3}'.format(subject,
                                                                               '；'.join(
                                                                                   list(set(do_desc))[:self.num_limit]),
                                                                               '；'.join(list(set(recommand_desc))[
                                                                                        :self.num_limit]),
                                                                               '；'.join(list(set(not_desc))[
                                                                                        :self.num_limit]))

        # 1-4 疾病-药品
        elif question_type == 'disease_drug':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}通常的使用的药品包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        # 1-5 疾病-检查
        elif question_type == 'disease_check':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}通常可以通过以下方式检查出来：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'symptom_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '症状{0}可能染上的疾病有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cause':
            desc = [i['m.cause'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}可能的成因有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_prevent':
            desc = [i['m.prevent'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的预防措施包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_lasttime':
            desc = [i['m.cure_lasttime'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}治疗可能持续的周期为：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cureway':
            desc = [';'.join(i['m.cure_way']) for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}可以尝试如下治疗：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cureprob':
            desc = [i['m.cured_prob'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}治愈的概率为（仅供参考）：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_easyget':
            desc = [i['m.easy_get'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的易感人群包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_desc':
            desc = [i['m.desc'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0},熟悉一下：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        # elif question_type == 'disease_acompany':
        #     desc1 = [i['n.name'] for i in answers]
        #     desc2 = [i['m.name'] for i in answers]
        #     subject = answers[0]['m.name']
        #     desc = [i for i in desc1 + desc2 if i != subject]
        #     final_answer = '{0}的并发症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        # elif question_type == 'disease_not_food':
        #     desc = [i['n.name'] for i in answers]
        #     subject = answers[0]['m.name']
        #     final_answer = '{0}忌食的食物包括有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        #
        # elif question_type == 'disease_do_food':
        #     do_desc = [i['n.name'] for i in answers if i['r.name'] == 'do_eat']
        #     recommand_desc = [i['n.name'] for i in answers if i['r.name'] == 'recommand_recipes']
        #     subject = answers[0]['m.name']
        #     final_answer = '{0}宜食的食物包括有：{1}\n推荐食谱包括有：{2}'.format(subject, ';'.join(list(set(do_desc))[:self.num_limit]), ';'.join(list(set(recommand_desc))[:self.num_limit]))

        elif question_type == 'food_not_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '患有{0}的人最好不要吃{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)

        elif question_type == 'food_do_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '患有{0}的人建议多试试{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)


        elif question_type == 'drug_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '{0}主治的疾病有{1},可以试试'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        # elif question_type == 'check_disease':
        #     desc = [i['m.name'] for i in answers]
        #     subject = answers[0]['n.name']
        #     final_answer = '通常可以通过{0}检查出来的疾病有{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()
```





Traceback (most recent call last):
  File "C:\Users\YD\AppData\Roaming\Python\Python36\site-packages\rasa\shared\utils\io.py", line 126, in read_file
    return f.read()
  File "c:\users\yd\appdata\local\programs\python\python36\lib\codecs.py", line 321, in decode
    (result, consumed) = self._buffer_decode(data, self.errors, final)
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xbd in position 29: invalid start byte
