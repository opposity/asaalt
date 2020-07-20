from project import pusher_client


def run_algorithm(search_term, number, pick_type, pick_algorithm, job_id):
    response_dict = {"cols_list": [''], "data_list": [['No Result Found!']], "job_id": job_id}
    print("run_algorithm", search_term, number, pick_type, pick_algorithm, job_id)
    data_frame = None
    try:
        if pick_type == "social_media" and pick_algorithm == "spacy_md":
            from project.scripts.spacymodelmd import spacymdscraper
            data_frame = spacymdscraper(search_term, number)
        elif pick_type == "social_media" and pick_algorithm == "spacy_sm":
            from project.scripts.spacymodelsm import spacysmscraper
            data_frame = spacysmscraper(search_term, number)
        elif pick_type == "magazines" and pick_algorithm == "spacy_md":
            from project.scripts.spacymagazinemodelmd import spacy_md_magazine_scraper
            data_frame = spacy_md_magazine_scraper(search_term, number)
        elif pick_type == "magazines" and pick_algorithm == "spacy_sm":
            from project.scripts.spacymagazinemodelsm import spacy_sm_magazine_scraper
            data_frame = spacy_sm_magazine_scraper(search_term, number)
        cols = list(data_frame.columns.values)
        data_list = [[str(i) if str(i) != 'nan' else '' for i in x] for x in data_frame.T.values.tolist()]
        data_list = list(map(list, zip(*data_list)))
        # data_list = [['Video Friday: This Terrifying Robot Will Cut Your Hair With Scissors', 'IEEE', '[]'],
        #              ['Six great science reads to pass the time', 'PopScience', '[]'],
        #              ['This Citizen Science Gig Pays People to Match Space Photos', 'Wired', '[]'],
        #              ['Trailblazers: Women in Science', 'Scientific American', '[]'],
        #              ['Crucial Choices for the Nascent ERC', 'Science Mag', '[]'],
        #              ['Data science is not a science project', 'MIT Tech Review', '[]'],
        #              ['About Us', 'American Scientist', '[]'],
        #              ['March for Science 2018 hosts rallies worldwide', 'New Scientist', '[]'],
        #              ['Can science help create a more just society?', 'ScienceNews', '[]']]
        # cols = ['Text', 'Type', 'NER Model']
        # print(data_list)
        # print(cols)
        response_dict['cols_list'] = cols
        response_dict['data_list'] = data_list
    except Exception as e:
        print("Exception:", str(e))
    finally:
        print("finally")
        pusher_client.trigger('my-channel', 'my-event', response_dict)
        print("pushed")
