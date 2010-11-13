from app.db.question import CachedQuestionModel, CachedAnswersModel
import logging

CHUNK_SIZE = 150

def deferred_store_question_to_cache(question_id, service, question_data):
    CachedQuestionModel(key_name = '%s_%s' % (question_id, service ), data = question_data).put()

def deferred_store_answers_to_cache(question_id, service, answers_data):   
    id_service = '%s_%s' % (question_id, service)
    try:
        chunk_index = 0
        chunk_id = 1
        for chunk_index in range(CHUNK_SIZE, len(answers_data),  CHUNK_SIZE):
            CachedAnswersModel(key_name = '%s_%s' % (id_service, chunk_id), 
                               id_service = id_service,
                               chunk_id = chunk_id,
                               data = answers_data[chunk_index-CHUNK_SIZE:chunk_index]).put()  
            chunk_id += 1
        else:
             CachedAnswersModel(key_name = '%s_%s' % (id_service, chunk_id), 
                                id_service = id_service,
                                chunk_id = chunk_id,
                                data = answers_data[chunk_index:chunk_index + CHUNK_SIZE]).put()
    except Exception, ex:
        logging.error("Can't store answers of question_id : %s" % question_id)