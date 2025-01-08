import pandas


def to_dict(a):
    dictionary = {a.column.name: getattr(a, a.column.name) for a.column in a.__table__.columns}
    return dictionary


def tabulate(dictionary):
    seen_questions = set()
    filtered_dictionary = []

    for item in dictionary:
        question = item['question']
        user_id = item['user_id']
        if (question, user_id) not in seen_questions:
            filtered_dictionary.append(item)
            seen_questions.add((question, user_id))

    df = pandas.DataFrame(filtered_dictionary)
    reshaped_df = df.pivot(index='user_id', columns=['question'], values=['choice', 'score'])
    reshaped_df['mean'] = reshaped_df.score.mean(axis=1)
    reshaped_df.to_excel("ques/static/resources/output.xlsx")

