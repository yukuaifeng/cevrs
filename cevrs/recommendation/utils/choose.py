import math
import numpy as np
import pandas as pd
from skfuzzy.cluster import cmeans
from ..models import GradeAll, ControlLine, StudentNumber, Schoolgrade
import pysnooper


def choose_school(rank, radio, first_value, second_value, third_value, fourth_value,
                  risk_number, surely_number, def_number):

    kind = "理工类" if radio == '2' else "文史类"

    # 首先根据分科和排名，筛选出50所高校来
    grade_template = GradeAll()
    fifty_schools = grade_template.get_fifty_schools(kind, rank)

    # 然后对于所选的四个因素的位次排序，重新排序
    rank_list = [first_value, second_value, third_value, fourth_value]
    normal_rank_list = ['1', '2', '3', '4']
    normal_time_list = [2, 1.5, 1, 0.5]
    rank_dict = dict(zip(rank_list, normal_time_list))
    sorted_dict = map(lambda x: {x: rank_dict[x]}, normal_rank_list)

    # 想办法找到排名最靠前的两个因素，是哪两个
    time_list = []
    for key in sorted_dict:
        for v in key.values():
            time_list.append(v)

    for i in range(0, len(normal_rank_list)):
        if normal_rank_list[i] == rank_list[0]:
            num1 = i
        if normal_rank_list[i] == rank_list[1]:
            num2 = i

    riskly_results, surely_results, definite_results = assess_school(fifty_schools, rank, kind, risk_number,
                                                                     surely_number, def_number, time_list, num1, num2)
    return riskly_results, surely_results, definite_results


# @pysnooper.snoop()
def assess_school(schools, rank, kind, risk_number, surely_number, def_number, time_list, num1, num2):
    # 首先，循环得到的schools，也就是里面的学校
    # 循环体中，也就是每一个学校内，首先查询它的每一年的数据，存储在form中
    # 然后进行四次运算：
    # 首先是达到要求的年份占比计算
    # 再就是计算五年内数据与目标rank的距离
    # 然后就是五年内数据与高考人数、省控线距离的rank值

    selected_schools = []
    rates = []
    clazzs = []
    riskly_results = []
    surely_results = []
    definite_results = []

    # 存放所有院校的评估数据
    school_quality = []

    stu_template = StudentNumber()
    grade_template = GradeAll()
    control_template = ControlLine()

    for school in schools:
        if school.school == "桂林理工大学" or '中外合作办学' in school.school or school.school == "天津师范大学" or school.school == "南京审计大学":
            continue
        selected_schools.append(school.school)

    for school in selected_schools:
        # 首先通过学校的名称和满足rank的排名来获取学习的编号和批次
        # 这里是因为有些学校的编号一致而批次不一样或者是学校名称一样但是录取的分数线同一年有多个
        school_infos = grade_template.get_school_info(school, rank, kind)
        school_clazz = school_infos[0].clazz
        school_number = school_infos[0].number
        for school_info in school_infos:
            clazzs.append(school_info.clazz)

        ranks = []
        years = []
        i = 0

        # 存储该学校历年的录取排名，获得占比
        for s in school_infos:
            ranks.append(s.rank)
            years.append(s.year)
            if s.rank > rank:
                i += 1

        # 计算学校的历年排名与目标排名的距离
        distance = compute_distance(ranks, rank)
        number = i / len(school_infos)

        stu_nums = []
        ctrl_ranks = []

        # 通过年份来查询相应年份的对应的高考人数和省控线的排位
        # 这里是因为不是每个学校的每一年数据都是完整的
        for year in years:
            num = stu_template.get_student_num(year, kind)
            stu_nums.append(num)

            school_template = GradeAll()
            school_rank = school_template.get_exact_info(school_number, school_clazz, kind, year)
            rank_template = school_rank[0].rank

            ctrl_rank_template = control_template.get_rank_by_year(year, kind, rank_template)
            ctrl_rank = ctrl_rank_template.ctrl_rank
            ctrl_ranks.append(ctrl_rank)

        num_variances = compute_variance(ranks, stu_nums)
        rank_variances = compute_variance(ranks, ctrl_ranks)

        single_school_quality = [school, number, distance, num_variances, rank_variances]

        # 如果学校的录取排名与目标排名差距过大，是因为目标名次数值太小，所以差距越小应该取值越小
        # 但是要归一化到0-1的范围之中
        if distance > 1:
            distance = distance / (distance + 1)

        # 这里是归一化均方差值
        # 如果均方差过大，也是数值越小应该越好，归一化的值也应该越小
        if num_variances > 1:
            num_variances = num_variances / (num_variances + 1)

        if rank_variances > 1:
            rank_variances = rank_variances / (rank_variances + 1)

        # 然后将四个数据按照一定的比例将其计算出推荐的概率
        # 因为占比肯定是最重要的，占比为78%
        # 再就是与目标rank值之间的距离，占比为12%
        # 其余的两项指标各占5%

        if rank > 2000:
            if i < len(school_infos):
                rate = (1 - distance) * 0.12 + number * 0.78 + (1 - num_variances) * 0.05 + (1 - rank_variances) * 0.05
            else:
                rate = distance * 0.12 + number * 0.78 + (1 - num_variances) * 0.05 + (1 - rank_variances) * 0.05
        else:
            rate = (1 - distance) * 0.12 + number * 0.78 + (1 - num_variances) * 0.05 + (1 - rank_variances) * 0.05

        # print(school, distance, num_variances, rank_variances)
        rate = '%.2f%%' % (rate * 100)
        school_quality.append(single_school_quality)
        rates.append(rate)

    # school_quality_df = pd.DataFrame(school_quality,
    #                                  columns=['school', 'number', 'distance', 'num_variances', 'rank_variances'])
    # school_quality_df.to_csv('D:\硕士毕业论文\论文\school_quality.csv', encoding='utf_8_sig')
    #
    # school_grade_template = Schoolgrade()
    # school_grade_list = []
    # for single_school in school_quality:
    #     school = single_school[0]
    #     sg = school_grade_template.get_school_grade(school)
    #     school_grade = [sg.school, sg.citygrade, sg.strength, sg.employment, sg.fund]
    #     school_grade_list.append(school_grade)
    # school_grade_df = pd.DataFrame(school_grade_list, columns=['school', 'citygrade', 'strength', 'employment', 'fund'])
    # school_grade_df.to_csv('D:\硕士毕业论文\论文\school_grade.csv', encoding='utf_8_sig', index=False)

    clazz_dict = dict(zip(selected_schools, clazzs))
    school_dict = dict(zip(selected_schools, rates))

    # 这里按照推荐概率对得到的结果进行分组
    riskly_dict = {k: v for k, v in school_dict.items() if v < "60%"}
    surely_dict = {k: v for k, v in school_dict.items() if "60%" < v < "85%"}
    definite_dict = {k: v for k, v in school_dict.items() if v > "85%"}

    # 然后对分组后的结果进行组内排序,注意，排序后的结果，就变成了list
    riskly_dict = sorted(riskly_dict.items(), key=lambda x: x[1], reverse=False)
    surely_dict = sorted(surely_dict.items(), key=lambda x: x[1], reverse=False)
    definite_dict = sorted(definite_dict.items(), key=lambda x: x[1], reverse=False)

    risky_list = []
    surely_list = []
    definite_list = []
    for key in riskly_dict:
        risky_list.append(key)
    for key in surely_dict:
        surely_list.append(key)
    for key in definite_dict:
        definite_list.append(key)
    if len(risky_list) > 0:
        risk_a, risk_c, risk_h, risk_r = compute_results(rank, risky_list)
        print(risk_a, risk_c, risk_h, risk_r)
    if len(surely_list) > 0:
        surely_a, surely_c, surely_h, surely_r = compute_results(rank, surely_list)
        print(surely_a, surely_c, surely_h, surely_r)
    if len(definite_list) > 0:
        definite_a, definite_c, definite_h, definite_r = compute_results(rank, definite_list)
        print(definite_a, definite_c, definite_h, definite_r)
    print(risky_list, surely_list, definite_list)
    print(len(risky_list), len(surely_list), len(definite_list))



    # 交给聚类程序去参与聚类的过程
    # riskly_dict = cluster(riskly_dict, time_list, num1, num2)
    # surely_dict = cluster(surely_dict, time_list, num1, num2)
    # definite_dict = cluster(definite_dict, time_list, num1, num2)
    # 如果数目不够，就去找上面那个去借，再删除掉,避免重复
    # 所以将最远离目标的target的值借到上一个等级

    if len(riskly_dict) < risk_number:
        for i in range(0, risk_number - len(riskly_dict)):
            riskly_dict.append(surely_dict[i])
            del surely_dict[i]

    if len(surely_dict) < surely_number:
        for i in range(0, surely_number - len(surely_dict)):
            surely_dict.append(definite_dict[i])
            del definite_dict[i]

    if len(definite_dict) < def_number:
        for i in range(0, def_number - len(definite_dict)):
            definite_dict.append(surely_dict[-len(definite_dict) + i])

    # 将筛选出来的学校的其他信息查询出来，放置到后面传入前端，方便之后的展示环节
    # 近几年的排名
    riskly_school_ranks = []
    surely_school_ranks = []
    definite_school_ranks = []

    # 学校所有录取分数以及所有的对应批次的省录取分数线
    riskly_school_grades = []
    surely_school_grades = []
    definite_school_grades = []
    riskly_ctrl_grades = []
    surely_ctrl_grades = []
    definite_ctrl_grades = []

    for school_temp in riskly_dict:
        school_number = grade_template.get_school_number(school_temp[0], kind)
        school_ranks = grade_template.get_school_ranks(school_temp[0], kind, school_number)
        riskly_school_ranks.append(school_ranks)

        school_grades = grade_template.get_school_grades(school_temp[0], kind, school_number)
        riskly_school_grades.append(school_grades)

        ctrl_grades = control_template.get_grades_by_clazz(kind, clazz_dict[school_temp[0]])
        riskly_ctrl_grades.append(ctrl_grades)

    for school_temp in surely_dict:
        school_number = grade_template.get_school_number(school_temp[0], kind)
        school_ranks = grade_template.get_school_ranks(school_temp[0], kind, school_number)
        surely_school_ranks.append(school_ranks)

        school_grades = grade_template.get_school_grades(school_temp[0], kind, school_number)
        surely_school_grades.append(school_grades)

        ctrl_grades = control_template.get_grades_by_clazz(kind, clazz_dict[school_temp[0]])
        surely_ctrl_grades.append(ctrl_grades)

    for school_temp in definite_dict:
        school_number = grade_template.get_school_number(school_temp[0], kind)
        school_ranks = grade_template.get_school_ranks(school_temp[0], kind, school_number)
        definite_school_ranks.append(school_ranks)

        school_grades = grade_template.get_school_grades(school_temp[0], kind, school_number)
        definite_school_grades.append(school_grades)

        ctrl_grades = control_template.get_grades_by_clazz(kind, clazz_dict[school_temp[0]])
        definite_ctrl_grades.append(ctrl_grades)

    # 加入录取批次，加入到相应地组内，与学校对应起来
    for i in range(0, len(riskly_dict)):
        riskly_dict[i] = riskly_dict[i] + (clazz_dict[riskly_dict[i][0]], riskly_school_ranks[i],
                                           riskly_school_grades[i], riskly_ctrl_grades[i])

    for i in range(0, len(surely_dict)):
        surely_dict[i] = surely_dict[i] + (clazz_dict[surely_dict[i][0]], surely_school_ranks[i],
                                           surely_school_grades[i], surely_ctrl_grades[i])

    for i in range(0, len(definite_dict)):
        definite_dict[i] = definite_dict[i] + (clazz_dict[definite_dict[i][0]], definite_school_ranks[i],
                                               definite_school_grades[i], definite_ctrl_grades[i])

    # 取出所需要的三项分类个数，这里的个数也是可以设置的
    for i in range(0, risk_number):
        riskly_results.append(riskly_dict[i])

    for i in range(0, surely_number):
        surely_results.append(surely_dict[i])

    for i in range(0, def_number):
        definite_results.append(definite_dict[i])

    return riskly_results, surely_results, definite_results
        

# @pysnooper.snoop()
def compute_distance(ranks, rank):
    # 把这个学校里的所有的录取名次和查询的名次进行求平方差再取均值
    # 这里是采用范数，p=2
    tmp = 0.0
    for r in ranks:
        tmp += ((r-rank)/rank)**2
    distance = math.sqrt(tmp)/len(ranks)
    # distance = tmp/rank
    return distance


# @pysnooper.snoop()
def compute_variance(ranks, targets):
    # 这里是要求所有的与高考的距离或者是与省控线的rank值的标准方差
    listtmp = [ranks[i]/targets[i] for i in range(len(ranks))]
    listtmp = [listtmp[i]/sum(listtmp) for i in range(len(listtmp))]
    if len(listtmp) == 1:
        variance = 1
    else:
        variance = np.std(listtmp, ddof=1)
#    print(variance)
    return variance


# @pysnooper.snoop()
def cluster(schools, time_list, num1, num2):
    school_names = []
    school_grade_list = []
    for i in range(0, len(schools)):
        school_names.append(schools[i][0])

    school_grade_template = Schoolgrade()

    for school in school_names:
        school_grade = school_grade_template.get_school_grade(school)
        school_grade = [school_grade.citygrade, school_grade.strength, school_grade.employment, school_grade.fund]

        for i in range(0, len(time_list)):
            school_grade[i] = school_grade[i] * time_list[i]

        school_grade_list.append(school_grade)

    kind1, kind2, kind3, kind_num1, kind_num2 = classify(school_grade_list, school_names, num1, num2)

    # 这里将得到的list根据分类的结果，进行分类和匹配，又将原来的学校得分重新排序起来
    kindlist = [kind1, kind2, kind3]
    # 得到用户排序的最前面两个目标
    target_1 = kindlist[kind_num1]
    target_2 = kindlist[kind_num2]
    kindlist.remove(target_1)
    kindlist.remove(target_2)
    target_3 = kindlist[0]
    school_list_selected = []
    target = [target_1, target_2, target_3]
    for i in range(0, 3):
        tar = target[i]
        for s in tar:
            school = s[0]
            for m in schools:
                if m[0] == school:
                    school_list_selected.append(m)
    return school_list_selected


# @pysnooper.snoop()
def classify(school_grade_list, school_names, num1, num2):
    # 聚类函数，将所有学校的四个所选的分数评分然后聚类
    # 然后根据最先选的两个因素选出来
    school_array = np.array(school_grade_list)
    school_array.dtype = np.float64
    school_array = school_array.T

    center, u, u0, d, jm, p, fpc = cmeans(school_array, m=1.1, c=3, error=0.005, maxiter=1000)

    print(center)
    print(fpc)

    for i in u:
        label = np.argmax(u, axis=0)

    kind1 = []
    kind2 = []
    kind3 = []

    target_list1 = []
    target_list2 = []
    for row in center:
        target_list1.append(row[num1])
        target_list2.append(row[num2])

    kind_num1 = target_list1.index(max(target_list1))
    kind_num2 = target_list2.index(max(target_list2))

    if kind_num1 == kind_num2:
        target_list1.remove(max(target_list1))
        kind_num2 = target_list1.index(max(target_list1))

    for i in range(0, len(school_grade_list)):
        if label[i] == 0:
            kind1.append([school_names[i], label[i]])
        elif label[i] == 1:
            kind2.append([school_names[i], label[i]])
        elif label[i] == 2:
            kind3.append([school_names[i], label[i]])

    return kind1, kind2, kind3, kind_num1, kind_num2


def compute_results(target, school_list):
    a = 0
    c = 0
    grade2019 = pd.read_csv("D:\Evolution\湖南省2019年理科一本二本各高校录取分数线与排名.csv", index_col=False, encoding='utf_8_sig')
    for s in school_list:
        # print(grade2019['rank'][grade2019['院校名称'] == s[0]].values)
        if grade2019['rank'][grade2019['院校名称'] == s[0]].values.any():
            rank = grade2019['rank'][grade2019['院校名称'] == s[0]].values[0]
            if rank > target:
                a += 1
                if (rank-target)/target < 0.1:
                    c += 1
    return a, c, a/len(school_list), c/len(school_list)
