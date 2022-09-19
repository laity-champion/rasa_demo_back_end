# response:utf8
import os
import re
import json
import codecs
import threading
from py2neo import Graph
from tqdm import tqdm


def print_data_info(data_path):
    triples = []
    i = 0
    with open(data_path, 'r', encoding='unicode_escape') as f:
        for line in f.readlines():
            data = json.loads(line)
            print(json.dumps(data, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))
            i += 1
            if i >= 5:
                break
    return triples


class MedicalExtractor(object):
    def __init__(self):
        super(MedicalExtractor, self).__init__()
        self.g = Graph('http://localhost:7474/', auth=("neo4j", "neo4jneo4j"))
        self.graph = Graph(
            host="127.0.0.1",
            http_port=7474,
            user="neo4j",
            password="neo4jneo4j")

        # 共8类节点
        self.drugs = []  # 药品
        self.recipes = []  # 菜谱
        self.foods = []  # 食物
        self.checks = []  # 检查
        self.departments = []  # 科室
        self.producers = []  # 药企
        self.diseases = []  # 疾病
        self.symptoms = []  # 症状

        self.disease_infos = []  # 疾病信息 #疾病实体是有属性的

        # 构建节点实体关系（11个关系）
        self.rels_department = []  # 科室－科室关系
        self.rels_noteat = []  # 疾病－忌吃食物关系
        self.rels_doeat = []  # 疾病－宜吃食物关系
        self.rels_recommandeat = []  # 疾病－推荐吃食物关系
        self.rels_commonddrug = []  # 疾病－通用药品关系
        self.rels_recommanddrug = []  # 疾病－热门药品关系
        self.rels_check = []  # 疾病－检查关系
        self.rels_drug_producer = []  # 厂商－药物关系

        self.rels_symptom = []  # 疾病症状关系
        self.rels_acompany = []  # 疾病并发关系
        self.rels_category = []  # 疾病与科室之间的关系

    def extract_triples(self, data_path):
        print("从json文件中转换抽取三元组")
        with open(data_path, 'r', encoding='unicode_escape') as f:
            for line in tqdm(f.readlines(), ncols=80):  # 遍历每一行
                data_json = json.loads(line)  # 逐行读取打开的文件
                disease_dict = {}  # 疾病实体的属性定义为一个字典
                disease = data_json['name']
                disease_dict['name'] = disease
                self.diseases.append(disease)
                disease_dict['desc'] = ''  # 这些是疾病的一些属性
                disease_dict['prevent'] = ''
                disease_dict['cause'] = ''
                disease_dict['easy_get'] = ''
                disease_dict['cure_department'] = ''
                disease_dict['cure_way'] = ''
                disease_dict['cure_lasttime'] = ''
                disease_dict['symptom'] = ''
                disease_dict['cured_prob'] = ''

                if 'symptom' in data_json:  # 如果症状存在于这个新文件里面的话
                    self.symptoms += data_json['symptom']  # 把列表中的所有症状添加到症状实体里面
                    for symptom in data_json['symptom']:  # 添加之后再通过for循环处理每一个症状
                        self.rels_symptom.append([disease, 'has_symptom', symptom])  # 构建疾病-症状关系

                if 'acompany' in data_json:  # 并发症
                    for acompany in data_json['acompany']:  # for循环每一个并发症
                        self.rels_acompany.append([disease, 'acompany_with', acompany])  # 为疾病和并发添加关系
                        self.diseases.append(acompany)  # 在疾病中添加并发

                if 'desc' in data_json:
                    disease_dict['desc'] = data_json['desc']  # 将数据中简介添加到疾病字典的简介中

                if 'prevent' in data_json:
                    disease_dict['prevent'] = data_json['prevent']  # 定义疾病属性，直接把值赋值给字典的相应值作为属性就可以

                if 'cause' in data_json:
                    disease_dict['cause'] = data_json['cause']

                if 'get_prob' in data_json:
                    disease_dict['get_prob'] = data_json['get_prob']

                if 'easy_get' in data_json:
                    disease_dict['easy_get'] = data_json['easy_get']

                if 'cure_department' in data_json:  # 因为是列表，如果只有一个值直接添加到
                    cure_department = data_json['cure_department']  # 这个语句就是把值赋值给相应列
                    if len(cure_department) == 1:
                        self.rels_category.append([disease, 'cure_department', cure_department[0]])  # 疾病-科室
                    if len(cure_department) == 2:  # 如果有两个科室的话
                        big = cure_department[0]  # 第一个是大科室，上级科室
                        small = cure_department[1]  # 第二个是小科室，下一级科室
                        self.rels_department.append([small, 'belongs_to', big])  # 大小科室之间存在科室-科室的关系
                        self.rels_category.append([disease, 'cure_department', small])  # 将小科室作为疾病-科室的值

                    disease_dict['cure_department'] = cure_department  # 将治疗科室增加到疾病字典中的治疗科室中去
                    self.departments += cure_department  # 将所有科室添加到科室实体列表中去

                if 'cure_way' in data_json:
                    disease_dict['cure_way'] = data_json['cure_way']

                if 'cure_lasttime' in data_json:
                    disease_dict['cure_lasttime'] = data_json['cure_lasttime']

                if 'cured_prob' in data_json:
                    disease_dict['cured_prob'] = data_json['cured_prob']

                if 'common_drug' in data_json:
                    common_drug = data_json['common_drug']
                    for drug in common_drug:
                        self.rels_commonddrug.append([disease, 'has_common_drug', drug])  # 定义疾病-通用药品关系
                    self.drugs += common_drug  # 将通用药品添加到药品实体中去

                if 'recommand_drug' in data_json:
                    recommand_drug = data_json['recommand_drug']
                    self.drugs += recommand_drug
                    for drug in recommand_drug:
                        self.rels_recommanddrug.append([disease, 'recommand_drug', drug])

                if 'not_eat' in data_json:
                    not_eat = data_json['not_eat']
                    for _not in not_eat:
                        self.rels_noteat.append([disease, 'not_eat', _not])

                    self.foods += not_eat
                    do_eat = data_json['do_eat']
                    for _do in do_eat:
                        self.rels_doeat.append([disease, 'do_eat', _do])

                    self.foods += do_eat  # 将宜吃食物添加到食物实体中去

                if 'recommand_eat' in data_json:
                    recommand_eat = data_json['recommand_eat']
                    for _recommand in recommand_eat:
                        self.rels_recommandeat.append([disease, 'recommand_recipes', _recommand])
                    self.recipes += recommand_eat

                if 'check' in data_json:
                    check = data_json['check']
                    for _check in check:
                        self.rels_check.append([disease, 'need_check', _check])  # 头尾节点，修改关系名称
                    self.checks += check

                if 'drug_detail' in data_json:  # 药品详情-药企名称（药物名称）
                    for det in data_json['drug_detail']:
                        det_spilt = det.split('(')  # 使用左括号进行切分
                        if len(det_spilt) == 2:  # 如果切分为两个
                            p, d = det_spilt  # p.d分别为药企和药品名称
                            d = d.rstrip(')')  # 删除药品的右括号
                            if p.find(d) > 0:  # 如果药企名称中包含药物名称，则药企名称中去掉药物名称
                                p = p.rstrip(d)
                            self.producers.append(p)  # 把药企名称添加到实体名称中
                            self.drugs.append(d)  # 把药物名称添加到药物实体名称中去
                            self.rels_drug_producer.append([p, 'production', d])  # 构建药企和药物之间的关系为生产
                        else:
                            d = det_spilt[0]
                            self.drugs.append(d)

                self.disease_infos.append(disease_dict)

    def write_nodes(self, entitys, entity_type):
        print("写入 {0} 实体".format(entity_type))
        for node in tqdm(set(entitys), ncols=80):  # 集合去重
            cql = """MERGE(n:{label}{{name:'{entity_name}'}})""".format(
                label=entity_type, entity_name=node.replace("'", ""))
            try:
                self.graph.run(cql)
            except Exception as e:
                print(e)
                print(cql)  # try防止报错，程序终止

    def write_edges(self, triples, head_type, tail_type):
        print("写入 {0} 关系".format(triples[0][1]))
        for head, relation, tail in tqdm(triples, ncols=80):
            cql = """MATCH(p:{head_type}),(q:{tail_type})
                    WHERE p.name='{head}' AND q.name='{tail}'
                    MERGE (p)-[r:{relation}]->(q)""".format(
                head_type=head_type, tail_type=tail_type, head=head.replace("'", ""),
                tail=tail.replace("'", ""), relation=relation)
            try:
                self.graph.run(cql)
            except Exception as e:
                print(e)
                print(cql)

    def set_attributes(self, entity_infos, etype):  # 只有疾病实体有属性，这里只定义疾病的属性
        print("写入 {0} 实体的属性".format(etype))
        for e_dict in tqdm(entity_infos[892:], ncols=80):
            name = e_dict['name']
            del e_dict['name']
            for k, v in e_dict.items():
                if k in ['cure_department', 'cure_way']:  # 因为这两个属性都是列表，其他都是字符串，所以单独进行处理
                    cql = """MATCH (n:{label})
                        WHERE n.name='{name}'
                        set n.{k}={v}""".format(label=etype, name=name.replace("'", ""), k=k, v=v)
                else:
                    cql = """MATCH (n:{label})
                        WHERE n.name='{name}'
                        set n.{k}='{v}'""".format(label=etype, name=name.replace("'", ""), k=k,
                                                  v=v.replace("'", "").replace("\n", ""))
                try:
                    self.graph.run(cql)
                except Exception as e:
                    print(e)
                    print(cql)

    # 直接执行如下三个方法
    def create_entitys(self):  # 将它导入到neo4j中去，创建实体8
        self.write_nodes(self.drugs, '药品')  # 方法名称：write_nodes
        self.write_nodes(self.recipes, '菜谱')
        self.write_nodes(self.foods, '食物')
        self.write_nodes(self.checks, '检查')
        self.write_nodes(self.departments, '科室')
        self.write_nodes(self.producers, '药企')
        self.write_nodes(self.diseases, '疾病')
        self.write_nodes(self.symptoms, '症状')

    def create_relations(self):  # 创建关系11
        self.write_edges(self.rels_department, '科室', '科室')  # 方法名称：write_edges
        self.write_edges(self.rels_noteat, '疾病', '食物')
        self.write_edges(self.rels_doeat, '疾病', '食物')
        self.write_edges(self.rels_recommandeat, '疾病', '菜谱')
        self.write_edges(self.rels_commonddrug, '疾病', '药品')
        self.write_edges(self.rels_recommanddrug, '疾病', '药品')
        self.write_edges(self.rels_check, '疾病', '检查')
        self.write_edges(self.rels_drug_producer, '药企', '药品')
        self.write_edges(self.rels_symptom, '疾病', '症状')
        self.write_edges(self.rels_acompany, '疾病', '疾病')
        self.write_edges(self.rels_category, '疾病', '科室')

    def set_diseases_attributes(self):
        # self.set_attributes(self.disease_infos,"疾病")
        t = threading.Thread(target=self.set_attributes, args=(self.disease_infos, "疾病"))
        t.setDaemon(False)
        t.start()

    # 将数据进行导出
    def export_data(self, data, path):
        if isinstance(data[0], str):
            data = sorted([d.strip("...") for d in set(data)])
        with codecs.open(path, 'w', encoding='unicode_escape') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def export_entitys_relations(self):
        self.export_data(self.drugs, './graph_data/recipes.json')
        self.export_data(self.recipes, './graph_data/recipes.json')
        self.export_data(self.foods, './graph_data/foods.json')
        self.export_data(self.checks, './graph_data/checks.json')
        self.export_data(self.departments, './graph_data/departments.json')
        self.export_data(self.producers, './graph_data/producers.json')
        self.export_data(self.diseases, './graph_data/diseases.json')
        self.export_data(self.symptoms, './graph_data/symptoms.json')

        self.export_data(self.rels_department, './graph_data/rels_department.json')
        self.export_data(self.rels_noteat, './graph_data/rels_noteat.json')
        self.export_data(self.rels_doeat, './graph_data/rels_doeat.json')
        self.export_data(self.rels_recommandeat, './graph_data/rels_recommandeat.json')
        self.export_data(self.rels_commonddrug, './graph_data/rels_commonddrug.json')
        self.export_data(self.rels_recommanddrug, './graph_data/rels_recommanddrug.json')
        self.export_data(self.rels_check, './graph_data/rels_check.json')
        self.export_data(self.rels_drug_producer, './graph_data/rels_drug_producer.json')
        self.export_data(self.rels_symptom, './graph_data/rels_symptom.json')
        self.export_data(self.rels_acompany, './graph_data/rels_acompany.json')
        self.export_data(self.rels_category, './graph_data/rels_category.json')


if __name__ == '__main__':
    path = "./medical.json"
    # print_data_info(path)
    extractor = MedicalExtractor()
    extractor.extract_triples(path)
    extractor.create_entitys()
    extractor.create_relations()
    extractor.set_diseases_attributes()
    extractor.export_entitys_relations()
