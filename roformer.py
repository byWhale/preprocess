import torch
from transformers import RoFormerModel, RoFormerTokenizer
tokenizer = RoFormerTokenizer.from_pretrained("junnyu/roformer_chinese_sim_char_ft_base")
pt_model = RoFormerModel.from_pretrained("junnyu/roformer_chinese_sim_char_ft_base")
text = "所述荧光探针是以NaYF4、NaGdF4、CaF2、LiYF4、NaLuF4、LiLuF4、KMnF3或Y2O3为发光基质"
print("原text：" + text)
# text = tokenizer.tokenize(text)
# print("tokenized:")
# print(text)

pt_inputs = tokenizer(text, max_length=64, padding=True, return_tensors="pt")
# print(tokenizer.tokenize(text))
# print(pt_inputs["input_ids"])
# print(tokenizer.decode(pt_inputs["input_ids"][0]))
# with torch.no_grad():
pt_outputs = pt_model(**pt_inputs)
print(pt_outputs["last_hidden_state"][0][0])


# def similarity(text1, text2):
#     """"计算text1与text2的相似度
#     """
#     input1 = tokenizer(text1, max_length=64, padding=True, return_tensors="pt")
#     input2 = tokenizer(text2, max_length=64, padding=True, return_tensors="pt")
#     v1 = pt_model(**input1)["last_hidden_state"][0][0]
#     v2 = pt_model(**input2)["last_hidden_state"][0][0]
#     # Z /= (Z**2).sum(axis=1, keepdims=True)**0.5
#     # return (Z[0] * Z[1]).sum()
#     similarity = torch.cosine_similarity(v1, v2, dim=0)
#     print(text1 + " " + text2)
#     print(similarity)
#     return similarity
#
# similarity(u'今天天气不错', u'今天天气很好')
# similarity(u'今天天气不错', u'今天天气不好')
# similarity(u'我喜欢北京', u'我很喜欢北京')
# similarity(u'我喜欢北京', u'我不喜欢北京')
# similarity(u'电影不错', u'电影很好')
# similarity(u'电影不错', u'电影不好')
# similarity(u'红色的苹果', u'绿色的苹果')
# similarity(u'给我推荐一款红色的车', u'给我推荐一款黑色的车')
# similarity(u'给我推荐一款红色的车', u'推荐一辆红车')
# similarity(u'给我推荐一款红色的车', u'麻烦来一辆红车')
# similarity(u'用铜做的锤子', u'用金属做的钉子')
# similarity(u'用铜做的锤子', u'用RNN做的模型')
# similarity(u'计算机', u'计算器')
# similarity(u'计算机', u'电脑')
# similarity(u'计算机', u'电视')